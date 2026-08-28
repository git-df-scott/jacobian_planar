"""night11 -- shared descent driver.

L-BFGS-B with its relative tolerances switched OFF (ftol = gtol = 0) so that a
run stops only on the iteration budget or on a genuine line-search failure --
otherwise scipy's default relative tests halt the descent at ~1e-11 and a
"plateau" would just be a tolerance artefact rather than a feature of the
landscape.  On an early stop the descent is re-launched from the end point
with a fresh curvature history, up to `restarts` times or until a whole pass
buys less than `rel_gain` relative improvement.  Falls back to Adam when scipy
is absent.
"""

import numpy as np

try:
    from scipy.optimize import minimize
    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    HAVE_SCIPY = False


def adam(obj, c0, iters, lr=3e-3):
    c = c0.copy()
    m = np.zeros_like(c)
    v = np.zeros_like(c)
    E = np.inf
    for t in range(1, iters + 1):
        E, g = obj(c)
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        c = c - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-12)
    return c, float(E), iters, 1, 'adam'


def descend(obj, c0, maxiter, restarts=4, rel_gain=1e-6):
    """Return (c, E, total_iters, n_passes, last_message)."""
    if not HAVE_SCIPY:
        return adam(obj, c0, maxiter)
    c = np.asarray(c0, dtype=float)
    E = float(obj(c)[0])
    total = 0
    passes = 0
    msg = ''
    while total < maxiter and passes < restarts:
        budget = maxiter - total
        r = minimize(obj, c, jac=True, method='L-BFGS-B',
                     options=dict(maxiter=budget, maxfun=3 * budget,
                                  ftol=0.0, gtol=0.0, maxcor=20))
        passes += 1
        total += int(r.nit)
        msg = str(r.message)[:70]
        Enew = float(r.fun)
        gain = (E - Enew) / max(abs(E), 1e-300)
        c, E = np.asarray(r.x, dtype=float), Enew
        if int(r.nit) >= budget:
            break
        if gain < rel_gain:
            break
    return c, E, total, passes, msg
