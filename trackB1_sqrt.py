#!/usr/bin/env python3
"""Case-(1) pentagons via SQRT-REDUCTION: eliminate Q entirely.

STRUCTURE (derived 2026-08-14, Fable/Opus-5 block; same mechanism as the
Track-C C3 ladder, which is certified 13/13).

Grade by w = j - i.  P = sum_{w=-1}^{8} P_w, Q = sum_{w=-1}^{12} Q_w, and the
top edges are the B1a parametrization P_8 = a S^2, Q_12 = b S^3 (cusp (2,3)).

Let F be the formal weight-graded series with

        F^2 = gamma * P^3,     gamma = b^2/a^3,     F_12 = b S^3,

i.e. F = c P^{3/2}.  Then [P, F] = 0 identically (2F[P,F] = [P,F^2] =
gamma[P,P^3] = 0).  Hence with Delta := Q - F,

        [P, Q] = [P, Delta].

Because P, Q have weights >= -1, [P,Q] is a polynomial of weight >= -2, so the
whole system is equivalent to:

  (C1) LADDER: at every level the recursion 2 F_12 F_{12-m} = N_m divides
       exactly by S^3 (this is the divisibility ladder);
  (C2) SUPPORT: F_w lies in N(Q)'s weight-w slice for w = 12..-1  (then
       Q := sum_{w>=-1} F_w is a legitimate polynomial);
  (C3) VANISHING: F_w = 0 for w = -2..-9;
  (C4) INHOMOGENEITY: [P_8, F_{-10}] = -x^2.

So **Q is not an unknown at all** — it is determined by P.  The unknowns are
P's coefficients (52 free, weights <= 7) plus S (5) and a, b: ~59 instead of
the 186 of the raw case-(1) system.

KEY SIMPLIFICATION.  Every weight-w slice f = sum_i f_i x^i y^{i+w} is
isomorphic to the UNIVARIATE polynomial f^(z) = sum_i f_i z^i; slice products
are univariate products (weights add), and for slices of weights w1, w2

        [f, g]^ = w2 * f^' * g^  -  w1 * f^ * g^' .

So the entire pentagon problem is univariate polynomial arithmetic over the
base field.  Per sample: ~23 levels of a few multiplications and one exact
division each — microseconds, no Groebner, no symbolic carry.  This is the
numeric tower FABLE_DECISIONS.md Decision 2 asked for, with the kernels
resolved rather than sampled: the level kernels reported by the old symbolic
tower, direction (T, (3b/2a) S T), are exactly d/dP of the 3/2-power
(3 gamma a^2 / (2b) = 3b/(2a)), i.e. they are the reparametrization of P's own
lower components — not extra freedom.

Validation anchor: the exact witness P = Stilde^2, Q = Stilde^3 must pass
C1-C3 with F reproducing Q exactly, and must FAIL exactly C4 (its bracket is
0, not x^2).
"""
import sys
from fractions import Fraction

# ---------------------------------------------------------------- univariate
def pmul(f, g, p):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    out[i + j] = (out[i + j] + a * b) % p
    return ptrim(out)

def padd(f, g, p):
    n = max(len(f), len(g))
    out = [0] * n
    for i in range(n):
        out[i] = ((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0)) % p
    return ptrim(out)

def pscal(f, c, p):
    c %= p
    return ptrim([(x * c) % p for x in f]) if c else []

def ptrim(f):
    while f and f[-1] == 0:
        f.pop() if isinstance(f, list) else None
        if isinstance(f, list):
            continue
        break
    return f

def pdiv_exact(f, g, p):
    """Exact division f/g over F_p; returns None if not exact."""
    f = list(f)
    if not g:
        return None
    if not f:
        return []
    if len(f) < len(g):
        return None
    inv = pow(g[-1], p - 2, p)
    q = [0] * (len(f) - len(g) + 1)
    for k in range(len(f) - len(g), -1, -1):
        c = (f[k + len(g) - 1] * inv) % p
        q[k] = c
        if c:
            for i, gi in enumerate(g):
                f[k + i] = (f[k + i] - c * gi) % p
    if any(f):
        return None
    return ptrim(q)

def pderiv(f, p):
    return ptrim([(i * f[i]) % p for i in range(1, len(f))]) if len(f) > 1 else []

def slice_bracket(f, w1, g, w2, p):
    """[f,g]^ = w2 f^' g^ - w1 f^ g^'  (result has weight w1 + w2)."""
    return padd(pscal(pmul(pderiv(f, p), g, p), w2, p),
                pscal(pmul(f, pderiv(g, p), p), -w1, p), p)

# ------------------------------------------------------------------ supports
def prange(w):
    """i-range of N(P) = hull{(0,0),(1,0),(8,14),(8,16),(0,8)} at weight w."""
    lo, hi = max(0, -w), min(8, w + 2)
    return (lo, hi) if lo <= hi and w <= 8 else None

def qrange(w):
    """i-range of N(Q) = hull{(0,0),(2,1),(12,21),(12,24),(0,12)} at weight w."""
    lo, hi = max(0, -2 * w), min(12, w + 3)
    return (lo, hi) if lo <= hi and w <= 12 else None

# ------------------------------------------------------------------- cascade
def cascade(s, a, b, plow, p, wmin=-10, verbose=False):
    """s: univariate S (deg<=4). plow: {w: coeff-list} for w = 7..-1.
    Returns dict with verdict and data."""
    ginv = pow(a, p - 2, p)
    gamma = (b * b % p) * pow(ginv, 3, p) % p
    P = {8: pscal(pmul(s, s, p), a, p)}
    for w in range(7, -2, -1):
        P[w] = ptrim(list(plow.get(w, [])))
    # P^3 slices, weights 24 down to -3
    P2 = {}
    for w1 in P:
        for w2 in P:
            W = w1 + w2
            P2[W] = padd(P2.get(W, []), pmul(P[w1], P[w2], p), p)
    P3 = {}
    for W2 in P2:
        for w3 in P:
            W = W2 + w3
            P3[W] = padd(P3.get(W, []), pmul(P2[W2], P[w3], p), p)
    s3 = pmul(pmul(s, s, p), s, p)
    F = {12: pscal(s3, b, p)}
    twoF12 = pscal(s3, 2 * b, p)
    ladder = []
    for m in range(1, 12 - wmin + 1):
        W = 24 - m
        N = pscal(P3.get(W, []), gamma, p)
        for q_ in list(F):
            pq = W - q_
            if pq in F and pq <= 11 and q_ <= 11:
                N = padd(N, pscal(pmul(F[pq], F[q_], p), -1, p), p)
        Fw = pdiv_exact(N, twoF12, p)
        if Fw is None:
            return {"verdict": "LADDER_FAIL", "level": 12 - m, "F": F,
                    "ladder": ladder}
        ladder.append((12 - m, len(Fw)))
        F[12 - m] = Fw
        if verbose:
            print(f"  F_{12-m:>3} = {Fw}")
    # (C2) support of F_w inside N(Q) for w = 12..-1
    for w in range(12, -2, -1):
        r = qrange(w)
        fw = F.get(w, [])
        if not fw:
            continue
        if r is None:
            return {"verdict": "SUPPORT_FAIL", "level": w, "F": F}
        lo, hi = r
        for i, c in enumerate(fw):
            if c and not (lo <= i <= hi):
                return {"verdict": "SUPPORT_FAIL", "level": w, "i": i, "F": F}
    # (C3) vanishing F_w = 0 for w = -2..-9
    for w in range(-2, -10, -1):
        if F.get(w, []):
            return {"verdict": "VANISH_FAIL", "level": w, "F": F}
    # (C4) [P_8, F_-10] PROPORTIONAL to z^2 with a NONZERO constant.
    # Scale-invariant on purpose: [P,Q] = kappa x^2 with kappa != 0 is an
    # equally good Keller pair (replace Q by Q/kappa; N(Q) is unchanged), so
    # testing equality with -z^2 would reject genuine solutions.  Audited in
    # trackB1_bracket_audit.py: no campaign verdict changes, but this is the
    # correct test.  The witness still fails here, with bracket exactly 0.
    br = ptrim(list(slice_bracket(P[8], 8, F.get(-10, []), -10, p)))
    if len(br) == 3 and br[0] == 0 and br[1] == 0 and br[2] != 0:
        return {"verdict": "SURVIVOR", "F": F, "bracket": br, "kappa": br[2]}
    return {"verdict": "INHOM_FAIL", "bracket": br, "F": F}

# ---------------------------------------------------------------- validation
def validate(p=65521):
    """Witness P = Stilde^2, Q = Stilde^3, Stilde = y^4 + x^4y^8 + t x^4y^7."""
    t = 1
    s = [1, 0, 0, 0, 1]                       # S = 1 + z^4  (y^4 + x^4y^8)
    a = b = 1
    plow = {7: [0, 0, 0, 0, 2 * t % p, 0, 0, 0, 2 * t % p],   # 2AB
            6: [0] * 8 + [t * t % p]}                          # B^2
    res = cascade(s, a, b, plow, p)
    print("witness verdict:", res["verdict"])
    F = res["F"]
    # expected: F = Stilde^3, weights 12..9 only
    St = {4: [1, 0, 0, 0, 1], 3: [0, 0, 0, 0, t % p]}
    S2 = {}
    for w1 in St:
        for w2 in St:
            S2[w1 + w2] = padd(S2.get(w1 + w2, []), pmul(St[w1], St[w2], p), p)
    S3 = {}
    for W in S2:
        for w in St:
            S3[W + w] = padd(S3.get(W + w, []), pmul(S2[W], St[w], p), p)
    ok = True
    for w in range(12, -11, -1):
        want = ptrim(list(S3.get(w, [])))
        got = ptrim(list(F.get(w, [])))
        if want != got:
            ok = False
            print(f"  MISMATCH at w={w}: want {want} got {got}")
    print("F reproduces Stilde^3 exactly on all weights 12..-10:", ok)
    print("witness fails exactly the inhomogeneous condition:",
          res["verdict"] == "INHOM_FAIL")
    return ok and res["verdict"] == "INHOM_FAIL"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        sys.exit(0 if validate() else 1)
    print(__doc__)
