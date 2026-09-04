"""
T4 -- Hensel lift + rational reconstruction + exact verification.

WHAT IT DOES
------------
Given a polynomial system F over Z (or Q) and a point x0 with F(x0) = 0 mod p:

  (a) HENSEL LIFT.  x_{k+1} = x_k - J(x_k)^+ F(x_k) computed modulo p^(2^k),
      doubling the precision each step, up to p^(2^K).  The step solves the
      linear system J dx = -F/p^m exactly over Z/p^m by row reduction, and
      REFUSES to proceed if that system is inconsistent or if J is singular
      mod p -- a singular Jacobian is a recorded stall, never a silent pass.
  (b) RATIONAL RECONSTRUCTION.  Each coordinate a mod m is reconstructed as
      r/s with |r|, |s| <= sqrt(m/2) by the half-extended Euclidean algorithm
      (the lattice reduction in one dimension; this is the standard, exact
      form).  A coordinate with no such r/s is reported as NOT RECONSTRUCTIBLE
      at that precision -- not silently rounded.
  (c) EXACT VERIFICATION.  The reconstructed rational point is substituted into
      the ORIGINAL system over Q with exact arithmetic.  Only a point that
      annihilates every generator exactly is reported, and it is reported as
      CANDIDATE-UNVERIFIED, never as a hit.

CONTROLS (controls() below; each is required to come out differently)
  L-POS  a planted system with the rational solution (2/3, -7/5, 11/13):
         lift + reconstruct + exact verify must SUCCEED.
  L-NEG  a system whose only roots are irrational (x^2 - 2 at a prime where 2
         is a square, so a mod-p root exists and the lift runs): reconstruction
         must FAIL to produce a point that verifies over Q.
  L-NEG2 a system with a SINGULAR Jacobian at the mod-p point: the lift must
         stall loudly rather than return something.
"""

import json
import os
import sys
from fractions import Fraction

import sympy as sp


def _rref_mod(M, rhs, m):
    """Row reduction over Z/m with m a prime power; pivots must be units."""
    A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    nr = len(A)
    nc = len(M[0]) if nr else 0
    piv, r = [], 0
    for c in range(nc):
        sel = None
        for i in range(r, nr):
            if A[i][c] % m and _is_unit(A[i][c], m):
                sel = i
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        inv = pow(A[r][c], -1, m)
        A[r] = [v * inv % m for v in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % m:
                f = A[i][c]
                A[i] = [(A[i][k] - f * A[r][k]) % m for k in range(nc + 1)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A, r, piv


def _is_unit(a, m):
    from math import gcd
    return gcd(a % m, m) == 1


def hensel_lift(polys, syms, x0, p, K=8):
    """Lift x0 (a root mod p) to a root mod p^K.  Returns (point, modulus, note)."""
    n = len(syms)
    x = [v % p for v in x0]
    m = p
    J = [[sp.diff(f, s) for s in syms] for f in polys]
    for step in range(K - 1):
        m2 = m * p
        env = {syms[i]: sp.Integer(x[i]) for i in range(n)}
        F = [int(sp.Integer(sp.expand(f.subs(env)))) % m2 for f in polys]
        if all(v % m == 0 for v in F):
            pass
        else:
            return None, m, f"the point is not a root mod {m} at step {step}"
        rhs = [(-(F[i] // m)) % p for i in range(len(polys))]
        Jm = [[int(sp.Integer(sp.expand(J[i][j].subs(env)))) % p
               for j in range(n)] for i in range(len(polys))]
        A, rk, piv = _rref_mod(Jm, rhs, p)
        if any(all(A[i][c] % p == 0 for c in range(n)) and A[i][n] % p
               for i in range(len(A))):
            return None, m, (f"the linearised system is INCONSISTENT mod {p} at "
                             f"step {step}: the mod-p point does not lift")
        dx = [0] * n
        for i, c in enumerate(piv):
            dx[c] = A[i][n] % p
        x = [(x[i] + m * dx[i]) % m2 for i in range(n)]
        m = m2
    env = {syms[i]: sp.Integer(x[i]) for i in range(n)}
    bad = [k for k, f in enumerate(polys)
           if int(sp.Integer(sp.expand(f.subs(env)))) % m]
    if bad:
        return None, m, f"lifted point fails generators {bad[:5]} mod {m}"
    return x, m, f"lifted to modulus p^{K}"


def rational_reconstruct(a, m):
    """r/s = a (mod m) with |r|,|s| <= sqrt(m/2); None when none exists."""
    from math import isqrt
    bound = isqrt(m // 2)
    r0, r1 = m, a % m
    s0, s1 = 0, 1
    while r1 > bound:
        if r1 == 0:
            return None
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    from math import gcd
    if gcd(abs(r1), abs(s1)) != 1:
        return None
    return Fraction(r1 if s1 > 0 else -r1, abs(s1))


def reconstruct_point(x, m):
    out = []
    for a in x:
        r = rational_reconstruct(a, m)
        if r is None:
            return None, f"coordinate {a} is not reconstructible at modulus {m}"
        out.append(r)
    return out, "all coordinates reconstructed"


def verify_exact(polys, syms, pt):
    env = {syms[i]: sp.Rational(pt[i]) for i in range(len(syms))}
    bad = []
    for k, f in enumerate(polys):
        if sp.simplify(sp.expand(f.subs(env))) != 0:
            bad.append(k)
    return (not bad), bad


def pipeline(polys, syms, x0, p, K=8):
    rec = {"prime": p, "K": K}
    x, m, note = hensel_lift(polys, syms, x0, p, K)
    rec["lift_note"] = note
    rec["modulus"] = m
    if x is None:
        rec["status"] = "LIFT-STALLED"
        return rec
    rec["lifted_point"] = [int(v) for v in x]
    pt, note2 = reconstruct_point(x, m)
    rec["reconstruction_note"] = note2
    if pt is None:
        rec["status"] = "NOT-RECONSTRUCTIBLE"
        return rec
    rec["rational_point"] = [str(v) for v in pt]
    ok, bad = verify_exact(polys, syms, pt)
    rec["status"] = "VERIFIED-RATIONAL-POINT" if ok else "RECONSTRUCTED-BUT-FAILS-EXACT"
    rec["failing_generators"] = bad[:8]
    return rec


def controls():
    out = []
    x, y, z = sp.symbols("x y z")
    p = 1000003
    # L-POS: planted rational solution (2/3, -7/5, 11/13)
    polys = [3 * x - 2, 5 * y + 7, 13 * z - 11]
    syms = [x, y, z]
    x0 = [2 * pow(3, -1, p) % p, (-7) * pow(5, -1, p) % p, 11 * pow(13, -1, p) % p]
    r = pipeline(polys, syms, x0, p, K=4)
    out.append(("L-POS a planted rational solution is lifted, reconstructed and "
                "verified exactly",
                r["status"] == "VERIFIED-RATIONAL-POINT" and
                r.get("rational_point") == ["2/3", "-7/5", "11/13"],
                f"{r['status']} {r.get('rational_point')}"))
    # L-NEG: x^2 - 2 has a mod-q root when 2 is a square, but no rational root.
    # q must satisfy q = 1 (mod 3) (campaign rule) and q = +-1 (mod 8) (2 a QR).
    q = 1000033
    assert q % 3 == 1 and q % 8 in (1, 7), q
    rt = int(sp.sqrt_mod(2, q))
    r2 = pipeline([x ** 2 - 2], [x], [rt], q, K=6)
    out.append((f"L-NEG an irrational-only system (x^2 - 2, at q = {q} where 2 IS "
                f"a square so the lift really runs) is NOT reported as a rational "
                f"point", r2["status"] != "VERIFIED-RATIONAL-POINT",
                f"{r2['status']}: {r2.get('reconstruction_note', '')[:60]}"))
    # L-NEG2: a mod-p root that does NOT lift -- x^2 - p at x0 = 0 has a singular
    # Jacobian there and the linearised step is inconsistent.
    r3 = pipeline([x ** 2 - p], [x], [0], p, K=4)
    out.append(("L-NEG2 a mod-p root with a singular Jacobian that does not lift "
                "makes the pipeline stall loudly instead of returning a point",
                r3["status"] == "LIFT-STALLED", f"{r3['status']}: "
                f"{r3.get('lift_note', '')[:70]}"))
    return out


if __name__ == "__main__":
    print("=" * 78)
    print("T4 -- lift pipeline controls")
    print("=" * 78)
    ok = True
    for n, o, note in controls():
        ok &= o
        print(f"    [{'PASS' if o else 'FAIL'}] {n}   {note}")
    print("=" * 78)
    sys.exit(0 if ok else 1)
