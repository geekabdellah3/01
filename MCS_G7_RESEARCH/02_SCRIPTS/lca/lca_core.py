"""Categorical latent-variable engines (numpy only; poLCA/R unavailable in this environment).

* fit_lca      : K-class latent class model, FIML for item-level missing (code -1), optional case weights,
                 multi-start EM, local-maximum diagnostics.
* fit_lca_mg   : multi-group LCA (class prevalences free by group; item-response probs shared or free per item).
* fit_param    : parametric latent-state models on the same likelihood scale:
                 'nrm1' = 1-D nominal response (continuous trait), 'nrm2' = 2-D, 'hyb' = K classes x 1-D trait
                 (factor-mixture; class-specific intercepts, shared slopes).
All models are label-invariant (categories are NOMINAL; no order is assumed).
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax

EPS = 1e-10

def onehot(X, ncat):
    Z = []
    for j, C in enumerate(ncat):
        z = np.zeros((X.shape[0], C)); m = X[:, j] >= 0
        z[np.where(m)[0], X[m, j]] = 1.0
        Z.append(z)
    return Z

def _loglik_states(Z, logT):          # logT: list of (S,C_j) -> (N,S)
    L = 0.0
    for z, lt in zip(Z, logT): L = L + z @ lt.T
    return L

# ------------------------------------------------------------------ plain LCA
def _em_lca(Z, w, theta, pi, max_iter=3000, tol=1e-9):
    ll_old = -np.inf; W = w.sum()
    for it in range(max_iter):
        L = np.log(pi + EPS)[None, :] + _loglik_states(Z, [np.log(t + EPS) for t in theta])
        lse = logsumexp(L, axis=1); post = np.exp(L - lse[:, None])
        ll = float((w * lse).sum())
        pw = post * w[:, None]
        pi = pw.sum(0) / W
        theta = []
        for z in Z:
            c = pw.T @ z; c = c + 1e-12
            theta.append(c / c.sum(1, keepdims=True))
        if abs(ll - ll_old) < tol * (abs(ll) + 1): break
        ll_old = ll
    return ll, pi, theta, it + 1

def n_par_lca(K, ncat): return (K - 1) + K * sum(c - 1 for c in ncat)

def posterior_lca(Z, theta, pi):
    L = np.log(pi + EPS)[None, :] + _loglik_states(Z, [np.log(t + EPS) for t in theta])
    lse = logsumexp(L, axis=1)
    return np.exp(L - lse[:, None]), lse

def fit_lca(X, ncat, K, w=None, n_starts=40, n_full=6, seed=1, short_iter=40, return_all=False):
    X = np.asarray(X); N = X.shape[0]; w = np.ones(N) if w is None else np.asarray(w, float)
    Z = onehot(X, ncat); rng = np.random.default_rng(seed)
    starts = []
    for s in range(n_starts):
        theta = [rng.dirichlet(np.ones(c), size=K) for c in ncat]
        pi = rng.dirichlet(np.ones(K) * 5)
        ll, pi_, th_, _ = _em_lca(Z, w, theta, pi, max_iter=short_iter, tol=1e-6)
        starts.append((ll, pi_, th_))
    starts.sort(key=lambda t: -t[0])
    fulls = []
    for ll0, pi_, th_ in starts[:n_full]:
        ll, pi_, th_, it = _em_lca(Z, w, th_, pi_)
        fulls.append(dict(ll=ll, pi=pi_, theta=th_, iters=it))
    fulls.sort(key=lambda d: -d["ll"])
    best = fulls[0]
    lls = np.array([f["ll"] for f in fulls])
    best["n_full"] = len(fulls)
    best["n_reaching_best"] = int((lls > lls[0] - 1e-4 * max(1, abs(lls[0])) * 1e-2).sum())
    best["n_distinct_solutions"] = int(len(np.unique(np.round(lls, 2))))
    best["ll_all_full"] = lls
    post, lse = posterior_lca(Z, best["theta"], best["pi"])
    best["post"] = post; best["K"] = K; best["ncat"] = ncat
    best["N"] = N; best["n_par"] = n_par_lca(K, ncat)
    best["converged"] = best["iters"] < 3000
    return (best, fulls) if return_all else best

def information(ll, n_par, N):
    return dict(AIC=-2 * ll + 2 * n_par, BIC=-2 * ll + n_par * np.log(N),
                aBIC=-2 * ll + n_par * np.log((N + 2) / 24), CAIC=-2 * ll + n_par * (np.log(N) + 1))

def entropy_stats(post):
    K = post.shape[1]
    if K == 1: return dict(rel_entropy=1.0, avepp=[1.0], min_avepp=1.0, modal_share=[1.0])
    H = -(post * np.log(post + 1e-300)).sum()
    ent = 1 - H / (post.shape[0] * np.log(K))
    modal = post.argmax(1)
    avepp = [float(post[modal == k, k].mean()) if (modal == k).any() else np.nan for k in range(K)]
    return dict(rel_entropy=float(ent), avepp=avepp, min_avepp=float(np.nanmin(avepp)),
                modal_share=[float((modal == k).mean()) for k in range(K)])

def bvr(X, ncat, theta, pi):
    """Bivariate residuals (Pearson chi2 / df) for all item pairs, using observed pairs."""
    J = X.shape[1]; rows = []
    for j in range(J):
        for l in range(j + 1, J):
            m = (X[:, j] >= 0) & (X[:, l] >= 0); n = m.sum()
            O = np.zeros((ncat[j], ncat[l]))
            np.add.at(O, (X[m, j], X[m, l]), 1)
            E = n * np.einsum("k,ka,kb->ab", pi, theta[j], theta[l])
            chi = float(((O - E) ** 2 / np.maximum(E, 1e-9)).sum())
            df_ = (ncat[j] - 1) * (ncat[l] - 1)
            rows.append((j, l, chi, df_, chi / df_))
    return rows

def sample_lca(pi, theta, ncat, N, rng, miss_mask=None):
    K = len(pi); c = rng.choice(K, size=N, p=pi)
    X = np.zeros((N, len(ncat)), int)
    for j, C in enumerate(ncat):
        cum = np.cumsum(theta[j], 1)[c]; u = rng.random(N)[:, None]
        X[:, j] = (u > cum).sum(1).clip(max=C - 1)
    if miss_mask is not None: X[miss_mask] = -1
    return X

def align_classes(theta_ref, pi_ref, theta, pi):
    """Hungarian matching of classes to a reference on item-response distance."""
    from scipy.optimize import linear_sum_assignment
    K = len(pi)
    D = np.zeros((K, K))
    for a in range(K):
        for b in range(K):
            D[a, b] = sum(np.abs(tr[a] - t[b]).sum() for tr, t in zip(theta_ref, theta))
    r, c = linear_sum_assignment(D)
    return c, D[r, c].sum() / len(theta)

# ------------------------------------------------------------------ multi-group LCA
def fit_lca_mg(X, ncat, K, g, free_items=(), init=None, n_starts=20, seed=3, max_iter=2000, tol=1e-9, w=None):
    """pi free by group always; theta_j shared across groups unless j in free_items."""
    X = np.asarray(X); N, J = X.shape; g = np.asarray(g).astype(int); G = int(g.max()) + 1
    w = np.ones(N) if w is None else np.asarray(w, float)
    Z = onehot(X, ncat); rng = np.random.default_rng(seed)
    def run(theta0, pi0):
        theta = [np.repeat(t[None], G, 0) if (j in free_items and t.ndim == 2) else t for j, t in enumerate(theta0)]
        pi = pi0.copy(); ll_old = -np.inf
        for it in range(max_iter):
            L = np.log(pi[g] + EPS)
            for j, z in enumerate(Z):
                lt = np.log(theta[j] + EPS)
                L = L + (z @ lt.T if lt.ndim == 2 else np.einsum("nc,nkc->nk", z, lt[g]))
            lse = logsumexp(L, 1); post = np.exp(L - lse[:, None]); ll = float((w * lse).sum())
            pw = post * w[:, None]
            for gg in range(G):
                pi[gg] = pw[g == gg].sum(0) / pw[g == gg].sum()
            for j, z in enumerate(Z):
                if j in free_items:
                    for gg in range(G):
                        c = pw[g == gg].T @ z[g == gg] + 1e-12; theta[j][gg] = c / c.sum(1, keepdims=True)
                else:
                    c = pw.T @ z + 1e-12; theta[j] = c / c.sum(1, keepdims=True)
            if abs(ll - ll_old) < tol * (abs(ll) + 1): break
            ll_old = ll
        return ll, pi, theta, post, it + 1
    best = None
    if init is not None:
        res = run(init["theta"], np.repeat(init["pi"][None], G, 0)); best = res
    else:
        for s in range(n_starts):
            th = [rng.dirichlet(np.ones(c), size=K) for c in ncat]
            res = run(th, np.repeat(rng.dirichlet(np.ones(K) * 5)[None], G, 0))
            if best is None or res[0] > best[0]: best = res
    ll, pi, theta, post, it = best
    npar = G * (K - 1) + sum((G if j in free_items else 1) * K * (c - 1) for j, c in enumerate(ncat))
    return dict(ll=ll, pi=pi, theta=theta, post=post, n_par=npar, iters=it, K=K, G=G)

# ------------------------------------------------------------------ parametric latent-state models
def gh_nodes(Q):
    x, wq = np.polynomial.hermite_e.hermegauss(Q); return x, wq / wq.sum()

def _design(kind, K, Q):
    if kind == "nrm1":
        th, wq = gh_nodes(Q); Xs = np.c_[np.ones(Q), th]; cls = np.zeros(Q, int); lw = np.log(wq)
    elif kind == "nrm2":
        th, wq = gh_nodes(Q); a, b = np.meshgrid(th, th, indexing="ij"); wa = np.outer(wq, wq)
        Xs = np.c_[np.ones(Q * Q), a.ravel(), b.ravel()]; cls = np.zeros(Q * Q, int); lw = np.log(wa.ravel())
    elif kind == "hyb":
        th, wq = gh_nodes(Q); Xs = []; cls = []; lw = []
        for k in range(K):
            oh = np.zeros((Q, K)); oh[:, k] = 1; Xs.append(np.c_[oh, th]); cls += [k] * Q; lw += list(np.log(wq))
        Xs = np.vstack(Xs); cls = np.array(cls); lw = np.array(lw)
    return Xs, cls, lw

def _mstep_item(Xs, n_sk, Beta0, ridge=1e-3):
    S, C = n_sk.shape; P = Xs.shape[1]; Ns = n_sk.sum(1)
    def f(b):
        B = b.reshape(P, C - 1); eta = np.c_[np.zeros(S), Xs @ B]
        lse = logsumexp(eta, 1); lp = eta - lse[:, None]
        val = -(n_sk * lp).sum() + ridge * (b ** 2).sum()
        p = np.exp(lp); grad = -(Xs.T @ (n_sk[:, 1:] - Ns[:, None] * p[:, 1:])) + 2 * ridge * B
        return val, grad.ravel()
    r = minimize(f, Beta0.ravel(), jac=True, method="L-BFGS-B", options=dict(maxiter=200))
    return r.x.reshape(P, C - 1)

def fit_param(X, ncat, kind="nrm1", K=1, Q=15, w=None, max_iter=300, tol=1e-7, seed=5, n_starts=3):
    X = np.asarray(X); N = X.shape[0]; w = np.ones(N) if w is None else np.asarray(w, float)
    Z = onehot(X, ncat); Xs, cls, lw = _design(kind, K, Q if kind != "nrm2" else 7)
    S, P = Xs.shape; rng = np.random.default_rng(seed); best = None
    for st in range(n_starts):
        Beta = [rng.normal(0, 0.3, (P, c - 1)) for c in ncat]
        if kind == "hyb" and K > 1:      # spread class intercepts
            for B in Beta: B[:K, :] += rng.normal(0, 1.0, (K, B.shape[1]))
        pik = np.ones(K) / K; ll_old = -np.inf
        for it in range(max_iter):
            logT = [np.log(softmax(np.c_[np.zeros(S), Xs @ B], 1) + EPS) for B in Beta]
            L = _loglik_states(Z, logT) + lw[None, :] + (np.log(pik)[cls][None, :] if kind == "hyb" else 0)
            lse = logsumexp(L, 1); post = np.exp(L - lse[:, None]); ll = float((w * lse).sum())
            pw = post * w[:, None]
            if kind == "hyb":
                pik = np.array([pw[:, cls == k].sum() for k in range(K)]); pik /= pik.sum()
            Beta = [_mstep_item(Xs, pw.T @ z + 1e-9, B) for z, B in zip(Z, Beta)]
            if abs(ll - ll_old) < tol * (abs(ll) + 1): break
            ll_old = ll
        if best is None or ll > best["ll"]: best = dict(ll=ll, Beta=Beta, pik=pik, post=post, iters=it + 1, Xs=Xs, cls=cls)
    nthe = {"nrm1": 1, "nrm2": 2, "hyb": 1}[kind]
    if kind == "nrm1": npar = sum(2 * (c - 1) for c in ncat)
    elif kind == "nrm2": npar = sum(3 * (c - 1) for c in ncat) - sum(1 for c in ncat[:1]) * (1)  # rotation constraint
    else: npar = (K - 1) + sum((K + 1) * (c - 1) for c in ncat)
    best.update(n_par=npar, N=N, kind=kind, K=K)
    return best

def eap_scores(res, dim=0, Q=15):
    """Posterior mean of the latent trait (dim-th) for param models."""
    Xs, post = res["Xs"], res["post"]
    th = Xs[:, -1] if res["kind"] != "nrm2" else Xs[:, 1 + dim]
    return post @ th
