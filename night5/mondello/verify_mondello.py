#!/usr/bin/env python3
"""
night5/mondello/verify_mondello.py -- independent verification of the
characteristic-two plane map extracted from arXiv 2608.02634, Theorem 1.2
(source label \\label{thm:main}).

Standard library only for everything it computes itself.  The one import
beyond the standard library is night4/tail.py, whose formal-inverse
recursion this task explicitly asks to run on the pair; that module is
itself pure standard library.  Nothing else is imported.

THE OBJECT, transcribed from the paper and not reconstructed:

    P(x,y) = x + x^2 y + x^4 + x^6 y^2
    Q(x,y) = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3        over k = closure(F_2)

CHECKS
  (1) F_2 arithmetic is sound (ring axioms and Frobenius on this
      implementation, plus a brute-force cross-check of the polynomial
      product against pointwise evaluation over F_4)
  (2) the Jacobian of the extracted pair is exactly 1 in F_2[x,y]
  (3) the stated collision: the three printed points are pairwise distinct
      and have equal images
  (4) the night4/tail.py recursion mod 2 on the pair to D = 24, reporting
      the tail profile.  The linear part must be invertible mod 2; if it is
      not, that is recorded and the run stops.  No coordinate change is
      applied to the source object under any circumstances.

Nothing here adjusts the object to make a check pass.  A failing check is
reported as a failure.
"""
import os
import sys

P_MONOMIALS = [(1, 0), (2, 1), (4, 0), (6, 2)]
Q_MONOMIALS = [(0, 1), (5, 0), (6, 1), (7, 2), (8, 3)]
COLLISION_POINTS = [(0, 1), (1, 0), (1, 1)]
COMMON_IMAGE = (0, 1)
D_TAIL = 24

P = {m: 1 for m in P_MONOMIALS}
Q = {m: 1 for m in Q_MONOMIALS}


# --------------------------------------------------------------------------
# polynomials over F_2: dict {(i, j): 1}; a coefficient is present iff it is 1
# --------------------------------------------------------------------------

def add2(a, b):
    r = dict(a)
    for k in b:
        if k in r:
            del r[k]          # 1 + 1 = 0
        else:
            r[k] = 1
    return r


def mul2(a, b):
    r = {}
    for (i1, j1) in a:
        for (i2, j2) in b:
            k = (i1 + i2, j1 + j2)
            if k in r:
                del r[k]
            else:
                r[k] = 1
    return r


def ddx2(a):
    """d/dx over F_2: the exponent i survives only when i is odd."""
    return {(i - 1, j): 1 for (i, j) in a if i % 2 == 1}


def ddy2(a):
    return {(i, j - 1): 1 for (i, j) in a if j % 2 == 1}


def pstr(a):
    if not a:
        return "0"
    out = []
    for (i, j) in sorted(a, key=lambda t: (t[0] + t[1], t[0], t[1])):
        if (i, j) == (0, 0):
            out.append("1")
        else:
            s = ""
            if i:
                s += "x" + ("^%d" % i if i > 1 else "")
            if j:
                s += "y" + ("^%d" % j if j > 1 else "")
            out.append(s)
    return " + ".join(out)


def evaluate_f2(a, x, y):
    t = 0
    for (i, j) in a:
        t ^= (pow(x, i) * pow(y, j)) & 1 if True else 0
    return t & 1


# --- F_4 = F_2[t]/(t^2+t+1), elements as 2-bit ints, for the cross-check ---

def f4_mul(a, b):
    # carryless multiply then reduce by t^2 = t + 1
    r = 0
    for k in range(2):
        if (b >> k) & 1:
            r ^= a << k
    for k in (3, 2):
        if (r >> k) & 1:
            r ^= (1 << k)
            r ^= (1 << (k - 1)) | (1 << (k - 2))
    return r & 3


def f4_pow(a, n):
    r = 1
    for _ in range(n):
        r = f4_mul(r, a)
    return r


def f4_eval(a, x, y):
    t = 0
    for (i, j) in a:
        t ^= f4_mul(f4_pow(x, i), f4_pow(y, j))
    return t & 3


def report(name, ok, extra=""):
    print("  %s %s%s" % ("PASS" if ok else "FAIL", name,
                         ("  " + extra) if extra else ""))
    return ok


# --------------------------------------------------------------------------
# (1) arithmetic
# --------------------------------------------------------------------------

def check1():
    print("(1) F_2 arithmetic")
    ok = True
    A = {(1, 0): 1, (0, 1): 1, (2, 3): 1}
    B = {(0, 1): 1, (3, 1): 1}
    C = {(1, 1): 1, (0, 0): 1}

    ok &= report("1 + 1 = 0", add2({(0, 0): 1}, {(0, 0): 1}) == {})
    ok &= report("A + A = 0", add2(A, A) == {})
    ok &= report("commutativity of +", add2(A, B) == add2(B, A))
    ok &= report("commutativity of *", mul2(A, B) == mul2(B, A))
    ok &= report("associativity of *", mul2(mul2(A, B), C) == mul2(A, mul2(B, C)))
    ok &= report("distributivity", mul2(A, add2(B, C)) == add2(mul2(A, B), mul2(A, C)))
    ok &= report("Frobenius (A+B)^2 = A^2 + B^2",
                 mul2(add2(A, B), add2(A, B)) == add2(mul2(A, A), mul2(B, B)))
    # Leibniz, and the char-2 fact that d/dx kills even exponents
    ok &= report("Leibniz d/dx(A*B) = A_x*B + A*B_x",
                 ddx2(mul2(A, B)) == add2(mul2(ddx2(A), B), mul2(A, ddx2(B))))
    ok &= report("d/dx(x^2) = 0 in char 2", ddx2({(2, 0): 1}) == {})

    # brute-force cross-check of mul2 against pointwise evaluation over F_4
    bad = 0
    prod = mul2(A, B)
    for x in range(4):
        for y in range(4):
            if f4_eval(prod, x, y) != f4_mul(f4_eval(A, x, y), f4_eval(B, x, y)):
                bad += 1
    ok &= report("product agrees with pointwise evaluation over all 16 F_4 points",
                 bad == 0, "mismatches=%d" % bad)
    return bool(ok)


# --------------------------------------------------------------------------
# (2) Jacobian
# --------------------------------------------------------------------------

def check2():
    print("(2) Jacobian of the extracted pair, in F_2[x,y]")
    Px, Py = ddx2(P), ddy2(P)
    Qx, Qy = ddx2(Q), ddy2(Q)
    print("      P   = %s" % pstr(P))
    print("      Q   = %s" % pstr(Q))
    print("      P_x = %s        (paper prints: 1)" % pstr(Px))
    print("      P_y = %s        (paper prints: x^2)" % pstr(Py))
    print("      Q_x = %s   (paper prints: x^4+x^6y^2)" % pstr(Qx))
    print("      Q_y = %s   (paper prints: 1+x^6+x^8y^2)" % pstr(Qy))
    ok = True
    ok &= report("P_x matches the paper", Px == {(0, 0): 1})
    ok &= report("P_y matches the paper", Py == {(2, 0): 1})
    ok &= report("Q_x matches the paper", Qx == {(4, 0): 1, (6, 2): 1})
    ok &= report("Q_y matches the paper", Qy == {(0, 0): 1, (6, 0): 1, (8, 2): 1})
    # in characteristic 2 subtraction is addition
    det = add2(mul2(Px, Qy), mul2(Py, Qx))
    print("      det JF = %s" % pstr(det))
    ok &= report("det JF is exactly 1 in F_2[x,y]", det == {(0, 0): 1})
    return bool(ok)


# --------------------------------------------------------------------------
# (3) collision
# --------------------------------------------------------------------------

def check3():
    print("(3) stated collision F(0,1) = F(1,0) = F(1,1) = (0,1)")
    ok = True
    n = len(COLLISION_POINTS)
    distinct = len(set(COLLISION_POINTS)) == n
    ok &= report("the %d printed points are pairwise distinct" % n, distinct)
    images = []
    for (a, b) in COLLISION_POINTS:
        im = (evaluate_f2(P, a, b), evaluate_f2(Q, a, b))
        images.append(im)
        print("      F(%d,%d) = (%d,%d)" % (a, b, im[0], im[1]))
    ok &= report("all images are equal", len(set(images)) == 1)
    ok &= report("the common image is the printed (0,1)",
                 all(im == COMMON_IMAGE for im in images))
    # the paper also states F(0,0) = (0,0)
    z = (evaluate_f2(P, 0, 0), evaluate_f2(Q, 0, 0))
    ok &= report("F(0,0) = (0,0) as the paper states", z == (0, 0))
    return bool(ok)


# --------------------------------------------------------------------------
# (4) the night4/tail.py recursion mod 2
# --------------------------------------------------------------------------

def check4():
    print("(4) night4/tail.py formal-inverse recursion mod 2, D = %d" % D_TAIL)
    here = os.path.dirname(os.path.abspath(__file__))
    night4 = os.path.abspath(os.path.join(here, "..", "..", "night4"))
    if night4 not in sys.path:
        sys.path.insert(0, night4)
    try:
        import tail as T
    except ImportError as exc:
        print("  FAIL could not import night4/tail.py: %s" % exc)
        return False
    print("      imported %s" % os.path.join(night4, "tail.py"))

    L = T.linear_part(P, Q, 2)
    d = T.det2(L, 2)
    print("      linear part mod 2 = [[%d, %d], [%d, %d]], det = %d"
          % (L[0][0], L[0][1], L[1][0], L[1][1], d))
    if d == 0:
        print("  RECORDED: the linear part is NOT invertible mod 2 "
              "(det = 0), so the recursion does not apply to the pair as "
              "printed.  A source coordinate change is not ours to make; "
              "stopping here as instructed.")
        return None
    report("linear part is invertible mod 2", True, "det = %d" % d)

    r = T.tail(P, Q, 2, D_TAIL)
    print("      deg F = %d, D = %d" % (r["deg_F"], r["D"]))
    print("      composition self-check: %s"
          % ("PASS" if r["selfcheck"]["pass"] else "FAIL"))
    if not r["selfcheck"]["pass"]:
        print("      self-check mismatches: %s" % r["selfcheck"]["mismatches"])
    print("      TAIL profile (m = %d..%d):" % (r["deg_F"] + 1, D_TAIL))
    for i, v in enumerate(r["tail"]):
        print("        m=%2d : %d" % (r["deg_F"] + 1 + i, v))
    nonzero = any(r["tail"])
    first = next((r["deg_F"] + 1 + i for i, v in enumerate(r["tail"]) if v), None)
    print("      tail vector = %s" % r["tail"])
    print("      tail NONZERO somewhere: %s (first nonzero degree: %s)"
          % (nonzero, first))
    ok = r["selfcheck"]["pass"]
    report("composition self-check", ok)
    return bool(ok), nonzero, r["tail"], first, r["deg_F"]


# --------------------------------------------------------------------------

def main():
    print("verify_mondello -- arXiv 2608.02634 Theorem 1.2, characteristic two")
    print("object transcribed from the paper; never adjusted by this script")
    print("=" * 70)
    r1 = check1()
    print()
    r2 = check2()
    print()
    r3 = check3()
    print()
    r4 = check4()
    print()
    print("=" * 70)
    print("SUMMARY")
    print("  (1) F_2 arithmetic          : %s" % ("PASS" if r1 else "FAIL"))
    print("  (2) Jacobian is exactly 1   : %s" % ("PASS" if r2 else "FAIL"))
    print("  (3) stated collision        : %s" % ("PASS" if r3 else "FAIL"))
    if r4 is None:
        print("  (4) tail recursion mod 2    : NOT APPLICABLE "
              "(linear part singular mod 2; recorded, not worked around)")
        allok = False
    else:
        ok4, nonzero, prof, first, degF = r4
        print("  (4) tail recursion mod 2    : self-check %s, tail %s"
              % ("PASS" if ok4 else "FAIL",
                 "NONZERO from m=%d" % first if nonzero else "ALL ZERO"))
        print("      tail profile m=%d..%d : %s" % (degF + 1, D_TAIL, prof))
        allok = r1 and r2 and r3 and ok4
    print("=" * 70)
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
