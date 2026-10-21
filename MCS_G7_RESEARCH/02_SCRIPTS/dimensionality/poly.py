"""Polychoric/tetrachoric correlations (two-step ML), pairwise-complete; parallel analysis; minres EFA on a correlation matrix."""
import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize_scalar

def _thresholds(x, C):
    cnt = np.bincount(x, minlength=C).astype(float); cum = np.cumsum(cnt)[:-1] / cnt.sum()
    return np.r_[-np.inf, norm.ppf(np.clip(cum, 1e-9, 1 - 1e-9)), np.inf]

def polychoric_pair(x, y, Cx, Cy):
    m = (x >= 0) & (y >= 0); x, y = x[m], y[m]
    if len(x) < 30 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2: return np.nan
    O = np.zeros((Cx, Cy)); np.add.at(O, (x, y), 1)
    tx, ty = _thresholds(x, Cx), _thresholds(y, Cy)
    ia, ib = np.meshgrid(np.arange(Cx), np.arange(Cy), indexing="ij"); ia, ib = ia.ravel(), ib.ravel()
    Ov = O.ravel(); keep = Ov > 0
    def cdf(a, b, r):
        a = np.clip(a, -8, 8); b = np.clip(b, -8, 8)
        return multivariate_normal(mean=[0, 0], cov=[[1, r], [r, 1]]).cdf(np.c_[a, b])
    def nll(r):
        p = (cdf(tx[ia + 1], ty[ib + 1], r) - cdf(tx[ia], ty[ib + 1], r) - cdf(tx[ia + 1], ty[ib], r) + cdf(tx[ia], ty[ib], r))
        return -(Ov[keep] * np.log(np.clip(p[keep], 1e-12, None))).sum()
    return float(minimize_scalar(nll, bounds=(-0.98, 0.98), method="bounded", options=dict(xatol=1e-4)).x)

def polychoric_matrix(X, ncat):
    J = X.shape[1]; R = np.eye(J)
    for j in range(J):
        for l in range(j + 1, J):
            R[j, l] = R[l, j] = polychoric_pair(X[:, j], X[:, l], ncat[j], ncat[l])
    return R

def nearest_psd(R, eps=1e-6):
    w, v = np.linalg.eigh(np.nan_to_num(R)); w = np.clip(w, eps, None); A = (v * w) @ v.T
    d = np.sqrt(np.diag(A)); return A / np.outer(d, d)

def parallel_analysis(X, ncat, n_iter=50, seed=0, pct=95):
    """Horn's PA on polychoric matrix: resample each column independently (permutation)."""
    rng = np.random.default_rng(seed); J = X.shape[1]
    ev = np.linalg.eigvalsh(nearest_psd(polychoric_matrix(X, ncat)))[::-1]
    sims = []
    for _ in range(n_iter):
        Xp = X.copy()
        for j in range(J):
            idx = np.where(X[:, j] >= 0)[0]; Xp[idx, j] = X[rng.permutation(idx), j]
        sims.append(np.linalg.eigvalsh(nearest_psd(polychoric_matrix(Xp, ncat)))[::-1])
    return ev, np.percentile(np.array(sims), pct, axis=0)

def minres(R, nf, n_iter=500):
    """Minimum-residual factor analysis (principal-axis iteration on communalities); returns loadings, communalities, RMSR."""
    R = nearest_psd(R); J = R.shape[0]
    h = 1 - 1 / np.diag(np.linalg.inv(R))
    for _ in range(n_iter):
        Rr = R.copy(); np.fill_diagonal(Rr, h)
        w, v = np.linalg.eigh(Rr); idx = np.argsort(w)[::-1][:nf]
        L = v[:, idx] * np.sqrt(np.clip(w[idx], 1e-9, None)); hn = (L ** 2).sum(1)
        if np.abs(hn - h).max() < 1e-7: h = hn; break
        h = hn
    resid = R - L @ L.T; np.fill_diagonal(resid, 0)
    rmsr = np.sqrt((resid[np.triu_indices(J, 1)] ** 2).mean())
    return L, h, rmsr

def varimax_oblimin_promax(L, power=4):
    """Promax rotation (oblique)."""
    def varimax(L, q=50, tol=1e-6):
        p, k = L.shape; Rm = np.eye(k); d = 0
        for _ in range(q):
            Lr = L @ Rm; u, s, vh = np.linalg.svd(L.T @ (Lr ** 3 - Lr @ np.diag((Lr ** 2).sum(0)) / p))
            Rm = u @ vh; dn = s.sum()
            if dn < d * (1 + tol): break
            d = dn
        return L @ Rm
    if L.shape[1] == 1: return L, np.eye(1)
    V = varimax(L); Q = V * np.abs(V) ** (power - 1)
    U = np.linalg.lstsq(V, Q, rcond=None)[0]; d = np.diag(np.linalg.inv(U.T @ U)); U = U @ np.diag(np.sqrt(d))
    P = V @ U; Phi = np.linalg.inv(U.T @ U); return P, Phi
