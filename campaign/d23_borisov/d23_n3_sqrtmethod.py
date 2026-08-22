"""
Plane Jacobian campaign - Session N2, stretch (start of Session N3 work):
the SQRT-SERIES REDUCTION for (-5)-curve Belyi maps of p^2/(w r^3) form,
VALIDATED by re-deriving the certified Session-7 First-Framework (p, r)
from scratch.

REDUCTION (the constructive face of the Sessions-12 sqrt-reduction).
For a degree-n map B = P^2/(w R^3) with deg P = m, deg R = d (2m = 3d+1),
and miracle cancellation deg(P^2 - w R^3) = 2m - D (chain degree D):
put u = 1/w and Rt(u) = u^d R(1/u)  (so Rt(0) = 1 for monic R).  Then

    sqrt(w R^3) = u^{-m} Rt(u)^{3/2},   Rt^{3/2} = sum h_k u^k,

and  P := [sqrt(w R^3)]_+  (polynomial part, i.e. p_k = h_{m-k})  gives
deg(P^2 - w R^3) <= 2m - D  if and only if

    h_{m+1} = h_{m+2} = ... = h_{2m-D} = 0.

FF (m, d, D) = (8, 5, 13): 4 conditions h_9..h_12 on the 5 coefficients
of R -- one scale freedom.  SF (m, d, D) = (14, 9, 23): 8 conditions
h_15..h_22 on 9 coefficients.  Slice: R(0) = 1 (valid maps have
gcd(R, w) = 1).  The h_k are computed by the ODE recurrence
2 Rt H' = 3 Rt' H:   2n h_n = sum_{i>=1} (5i - 2n) a_i h_{n-i}.

VALIDATION RUN (this file): Levenberg-Marquardt multistart on the FF
system recovers EXACTLY the two First-Framework dessins -- the certified
Session-7 (p, r) over Q(i sqrt 3) and its complex conjugate -- and
nothing else that passes the genericity filters.  This certifies the
method; the SF hunt (8-dim, h_15..h_22) is the companion run.
"""
import numpy as np

rng = np.random.default_rng(99)

def series_H(c, M, deg):
    """h_0..h_{M-1} of (1 + c1 u + ... + c_deg u^deg)^{3/2}."""
    a = np.zeros(deg + 1, dtype=complex); a[0] = 1; a[1:] = c
    h = np.zeros(M, dtype=complex); h[0] = 1
    for n in range(1, M):
        s = 0j
        for i in range(1, min(deg, n) + 1):
            s += (5*i - 2*n)*a[i]*h[n-i]
        h[n] = s/(2*n)
    return h

def lm(resid, x, nres, nvar, itmax=250):
    mu = 1e-3
    f = resid(x); nf = np.linalg.norm(f)
    for it in range(itmax):
        if not np.isfinite(nf):
            return None
        J = np.zeros((nres, nvar), dtype=complex)
        for j in range(nvar):
            xp = x.copy(); xp[j] += 1e-7
            J[:, j] = (resid(xp) - f)/1e-7
        A = J.conj().T@J
        g = J.conj().T@f
        moved = False
        for _ in range(60):
            try:
                step = np.linalg.solve(A + mu*np.eye(nvar), -g)
            except np.linalg.LinAlgError:
                return None
            xn = x + step
            fn = resid(xn); nfn = np.linalg.norm(fn)
            if nfn < nf:
                x, f, nf = xn, fn, nfn
                mu = max(mu*0.4, 1e-14)
                moved = True
                break
            mu *= 3
            if mu > 1e12:
                break
        if not moved:
            return x if nf < 1e-7 else None
        if nf < 1e-11:
            return x
    return x if nf < 1e-7 else None

def newton_polish(resid, x, nres, nvar, iters=6):
    """quadratic-convergence polish to the float floor after LM."""
    for _ in range(iters):
        f = resid(x)
        J = np.zeros((nres, nvar), dtype=complex)
        for j in range(nvar):
            xp = x.copy(); xp[j] += 1e-8
            J[:, j] = (resid(xp) - f)/1e-8
        try:
            step = (np.linalg.solve(J, -f) if nres == nvar
                    else np.linalg.lstsq(J, -f, rcond=None)[0])
        except np.linalg.LinAlgError:
            return x
        if not np.all(np.isfinite(step)):
            return x
        x = x + step
    return x

def resid_ff(x):
    c = np.concatenate([x, [1.0+0j]])
    return series_H(c, 13, 5)[9:13]

def invs5(r):
    return np.array([r[5-j]**5/r[5]**(5-j) for j in range(1, 5)])

if __name__ == "__main__":
    s3 = 1j*np.sqrt(3)
    r_cert = np.array([1, 4/3 + 16/3*s3, -278/9 + 68/9*s3, -140/3 - 24*s3,
                       35/3 - 112/3*s3, 68/3 - 20/3*s3], dtype=complex)
    t_cert = invs5(r_cert)
    found = []
    for trial in range(6000):
        rad = np.exp(rng.uniform(np.log(0.5), np.log(25.0), size=4))
        x0 = (rad*(rng.normal(size=4) + 1j*rng.normal(size=4))).astype(complex)
        x = lm(resid_ff, x0, 4, 4)
        if x is None:
            continue
        x = newton_polish(resid_ff, x, 4, 4)
        r = np.concatenate([[1.0+0j], x, [1.0+0j]])
        h = series_H(np.concatenate([x, [1.0+0j]]), 14, 5)
        p = h[:9]     # descending: p_desc[i] = p_{8-i} = h_i (NO reversal)
        wr3 = np.polymul([1, 0], np.polymul(np.polymul(r, r), r))
        D = np.polysub(np.polymul(p, p), wr3)
        if np.max(np.abs(D[:-4])) > 1e-6*np.max(np.abs(wr3)):
            continue
        if abs(D[-4]) < 1e-8*np.max(np.abs(D[-4:])):
            continue
        rs = np.roots(r)
        if min(abs(rs[i]-rs[j]) for i in range(5) for j in range(i+1, 5)) < 1e-5:
            continue
        t = invs5(r)
        if not any(np.all(np.abs(t - tt) <= 1e-4*(1 + np.abs(tt)))
                   for tt in found):
            found.append(t)
    print(f"distinct valid FF solutions: {len(found)} (expect 2)")
    def close(a, b):
        return np.all(np.abs(a - b) <= 1e-4*(1 + np.abs(b)))
    print("certified Session-7 (p,r) recovered:",
          any(close(t, t_cert) for t in found))
    print("conjugate dessin recovered:",
          any(close(t, np.conj(t_cert)) for t in found))
