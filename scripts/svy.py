"""Survey-design-aware OLS / logit estimators (Taylor linearisation, strata, no PSU variable).

WBES files carry weights (wstrict) and a strata id but NO cluster/PSU id, so every firm is its own PSU:
  V(b) = A^-1 B A^-1,   A = sum_i w_i x_i x_i' (OLS)  or  sum_i w_i p_i(1-p_i) x_i x_i' (logit)
  B    = sum_h  n_h/(n_h-1) * sum_{i in h} (s_i - s_h_bar)(s_i - s_h_bar)'      with s_i = w_i x_i e_i
Single-firm strata ("lonely PSUs") are centred on the grand mean of scores (Stata 'centered' option style) and
contribute with factor 1.  Inference uses t(n - H) for OLS/logit as in Stata svy (df = #PSU - #strata).
When strata=None the estimator reduces to a standard HC1-type sandwich, which is used for the unweighted runs.
"""
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm

class Res:
    def __init__(self, names, b, V, n, df, extra=None):
        self.names, self.b, self.V, self.n, self.df = list(names), np.asarray(b), np.asarray(V), n, df
        self.se = np.sqrt(np.diag(self.V)); self.t = self.b / self.se
        self.p = 2 * stats.t.sf(np.abs(self.t), df)
        self.extra = extra or {}
    def table(self, level=0.95):
        q = stats.t.ppf(0.5 + level / 2, self.df)
        return pd.DataFrame({"term": self.names, "coef": self.b, "se": self.se, "t": self.t, "p": self.p,
                             "ci_low": self.b - q * self.se, "ci_high": self.b + q * self.se})
    def cov(self): return pd.DataFrame(self.V, index=self.names, columns=self.names)

def _meat(S, strata):
    """S: n x k score matrix; strata: array of stratum ids (or None -> HC1-like with one stratum)."""
    n, k = S.shape
    if strata is None:
        Sc = S - S.mean(axis=0)
        return n / (n - 1) * Sc.T @ Sc, 1
    st = pd.Series(strata).values
    B = np.zeros((k, k)); H = 0
    gm = S.mean(axis=0)
    for h in np.unique(st):
        m = st == h; nh = m.sum(); Sh = S[m]; H += 1
        if nh == 1:
            d = Sh[0] - gm; B += np.outer(d, d)                 # lonely PSU centred on grand mean (factor 1)
        else:
            Sc = Sh - Sh.mean(axis=0); B += nh / (nh - 1) * Sc.T @ Sc
    return B, H

def ols(y, X, w=None, strata=None, names=None):
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    A = (X * w[:, None]).T @ X; Ai = np.linalg.inv(A)
    b = Ai @ (X * w[:, None]).T @ y
    e = y - X @ b
    S = X * (w * e)[:, None]
    B, H = _meat(S, strata)
    V = Ai @ B @ Ai
    df = n - (H if strata is not None else k)
    r2 = 1 - (w * e ** 2).sum() / (w * (y - np.average(y, weights=w)) ** 2).sum()
    return Res(names or [f"x{i}" for i in range(k)], b, V, n, df, {"r2": r2, "resid": e})

def logit(y, X, w=None, strata=None, names=None):
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    m = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=w).fit(maxiter=200)
    b = m.params; p = m.predict(X)
    A = (X * (w * p * (1 - p))[:, None]).T @ X; Ai = np.linalg.inv(A)
    S = X * (w * (y - p))[:, None]
    B, H = _meat(S, strata)
    V = Ai @ B @ Ai
    df = n - (H if strata is not None else k)
    ll0 = (w * (y * np.log(y.mean()) + (1 - y) * np.log(1 - y.mean()))).sum() if 0 < y.mean() < 1 else np.nan
    ll = (w * (y * np.log(np.clip(p, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-12, 1)))).sum()
    r = Res(names or [f"x{i}" for i in range(k)], b, V, n, df, {"pseudo_r2": 1 - ll / ll0 if ll0 else np.nan, "p_hat": p})
    return r

def fracit(y, X, w=None, strata=None, names=None):
    """Fractional logit (quasi-binomial, Papke-Wooldridge): same estimating equations as logit but y in [0,1]."""
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    m = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=w).fit(maxiter=200)
    b = m.params; p = m.predict(X)
    A = (X * (w * p * (1 - p))[:, None]).T @ X; Ai = np.linalg.inv(A)
    S = X * (w * (y - p))[:, None]
    B, H = _meat(S, strata)
    V = Ai @ B @ Ai
    return Res(names or [f"x{i}" for i in range(k)], b, V, n, n - (H if strata is not None else k), {"p_hat": p})

def wald(res, idx, R=None, r=None):
    """Joint Wald F-test that coefficients at positions idx are zero (or R b = r)."""
    b = res.b; V = res.V
    if R is None:
        R = np.zeros((len(idx), len(b)))
        for i, j in enumerate(idx): R[i, j] = 1
        r = np.zeros(len(idx))
    d = R @ b - r; W = d @ np.linalg.inv(R @ V @ R.T) @ d; q = R.shape[0]
    F = W / q
    return F, stats.f.sf(F, q, res.df), q

def ame_logit(res, X, names, var, w=None):
    """Average marginal effect of a binary/continuous regressor in a logit (discrete change for 0/1 variables) + delta-method SE."""
    j = names.index(var); b = res.b; X = np.asarray(X, float)
    w = np.ones(len(X)) if w is None else np.asarray(w, float)
    def ame(bb):
        if set(np.unique(X[:, j])) <= {0.0, 1.0}:
            X1 = X.copy(); X0 = X.copy(); X1[:, j] = 1; X0[:, j] = 0
            return np.average(1 / (1 + np.exp(-X1 @ bb)) - 1 / (1 + np.exp(-X0 @ bb)), weights=w)
        p = 1 / (1 + np.exp(-X @ bb)); return np.average(p * (1 - p) * bb[j], weights=w)
    a = ame(b); eps = 1e-6; g = np.zeros(len(b))
    for i in range(len(b)):
        bp = b.copy(); bp[i] += eps; bm = b.copy(); bm[i] -= eps; g[i] = (ame(bp) - ame(bm)) / (2 * eps)
    se = float(np.sqrt(g @ res.V @ g)); t = a / se
    return dict(ame=a, se=se, p=2 * stats.t.sf(abs(t), res.df), ci_low=a - stats.t.ppf(.975, res.df) * se, ci_high=a + stats.t.ppf(.975, res.df) * se)


def firth(y, X, names=None, maxit=200, tol=1e-9):
    """Firth (1993) bias-reduced logit; UNWEIGHTED; model-based covariance; normal inference.  Used only as a sensitivity
    check for sparse cells / quasi-separation, where ordinary ML logit estimates are unreliable."""
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape
    b = np.zeros(k)
    for _ in range(maxit):
        eta = X @ b; p = 1 / (1 + np.exp(-eta)); W = p * (1 - p)
        I = (X * W[:, None]).T @ X; Ii = np.linalg.inv(I)
        h = np.einsum("ij,jk,ik->i", X * np.sqrt(W)[:, None], Ii, X * np.sqrt(W)[:, None])
        U = X.T @ (y - p + h * (0.5 - p)); step = Ii @ U
        mx = np.abs(step).max()
        if mx > 5: step = step * 5 / mx
        b = b + step
        if mx < tol: break
    p = 1 / (1 + np.exp(-X @ b)); W = p * (1 - p); V = np.linalg.inv((X * W[:, None]).T @ X)
    return Res(names or [f"x{i}" for i in range(k)], b, V, n, 10 ** 6)
