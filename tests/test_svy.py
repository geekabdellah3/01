"""Validation of scripts/svy.py against statsmodels (cases where results must coincide)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import numpy as np, statsmodels.api as sm, svy
rng = np.random.default_rng(1)
n = 400
X = np.column_stack([np.ones(n), rng.normal(size=n), rng.binomial(1, .4, n)])
y = X @ [1, .5, -.3] + rng.normal(size=n) * (1 + .5 * np.abs(X[:, 1]))
w = rng.uniform(.5, 3, n)
# 1) unweighted OLS, no strata: coefficients identical to OLS; V = n/(n-1) * HC0
r = svy.ols(y, X); m = sm.OLS(y, X).fit(cov_type="HC0")
assert np.allclose(r.b, m.params); assert np.allclose(r.V, m.cov_params() * n / (n - 1)), "OLS unweighted sandwich"
# 2) weighted OLS, every firm its own stratum (lonely-PSU centred): equals WLS HC0
st = np.arange(n)
r = svy.ols(y, X, w=w, strata=st); m = sm.WLS(y, X, weights=w).fit(cov_type="HC0")
assert np.allclose(r.b, m.params); assert np.allclose(r.V, m.cov_params(), rtol=1e-6), "WLS singleton strata"
# 3) logit unweighted vs statsmodels HC0 (x n/(n-1))
yb = rng.binomial(1, 1 / (1 + np.exp(-(X @ [-.5, .8, .4]))))
r = svy.logit(yb, X); m = sm.Logit(yb, X).fit(disp=0, cov_type="HC0")
assert np.allclose(r.b, m.params, atol=1e-6); assert np.allclose(r.V, m.cov_params() * n / (n - 1), rtol=1e-4), "logit sandwich"
# 4) fractional logit on 0/1 equals logit
f = svy.fracit(yb, X); assert np.allclose(f.b, r.b, atol=1e-6) and np.allclose(f.V, r.V, rtol=1e-6)
# 5) stratified variance: with 2 strata, identical weights, V differs from no-strata only through centering; check positivity + symmetric
st2 = rng.integers(0, 20, n); r2 = svy.ols(y, X, w=w, strata=st2)
assert np.all(np.linalg.eigvalsh(r2.V) > 0) and np.allclose(r2.V, r2.V.T)
# 6) Wald and AME consistency: AME of binary regressor in logit vs finite difference
a = svy.ame_logit(r, X, ["c", "x", "d"], "d")
p1 = 1 / (1 + np.exp(-(np.column_stack([X[:, :2], np.ones(n)]) @ r.b))); p0 = 1 / (1 + np.exp(-(np.column_stack([X[:, :2], np.zeros(n)]) @ r.b)))
assert abs(a["ame"] - (p1 - p0).mean()) < 1e-10
F, p, q = svy.wald(r, [1, 2]); assert q == 2 and 0 <= p <= 1
print("svy.py validation: all checks passed")
