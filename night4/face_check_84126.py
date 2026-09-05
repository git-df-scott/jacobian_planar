#!/usr/bin/env python3
"""
night4/face_check_84126.py -- mechanical face-check for the (84,126) claim.

Self-contained: standard library only.  It imports nothing from night2/ or
night3/, and nothing from any third-party package, so it stands on its own
as an independent check.

Everything is exact integer arithmetic.  Nothing is evaluated numerically
and no floating point appears anywhere.

FIRST PRINCIPLES.  The single rule this file is built on is the monomial
bracket rule

    [x^a y^b, x^c y^d] = (a*d - b*c) * x^(a+c-1) * y^(b+d-1),

extended bilinearly.  Item 0 below re-derives that rule from explicit
partial differentiation, so the rule itself is checked rather than assumed.

Signs are DERIVED here, not copied from any statement of the claim: each
item prints the coefficients it computed, and the comparisons are made
against those computed values.

Items:
  0. bracket rule self-check against explicit differentiation
  1. weight w(i,j) = 10i - 13j, u = x^13 y^10:
         P_w = x*(a0 + a1*u),  Q_w = b*x^4*y
     compare [P_w, Q_w] against x^4*(a0*b - 26*a1*b*u), coefficient by
     coefficient over Z
  2. weight w(i,j) = 3i - 4j, v = x^4 y^3:
         P_w = a*x^4*y,  Q_w = x * sum_{j=0..5} b_j * v^j
     derive the coefficient of each v^j in [P_w, Q_w] and print it
  3. the kill: over Z, mod 999983 and mod 1000003, with target x^4,
     orientation A forces a1 = 0 (or b = 0), orientation B forces b_5 = 0
"""

PRIMES = (999983, 1000003)

# ---------------------------------------------------------------------------
# exact polynomials in x, y whose coefficients are integer polynomials in the
# unknown symbols.  A coefficient is a dict {sorted tuple of symbol names: int},
# e.g. a0*b is {('a0','b'): 1} and the integer -26 is {(): -26}.
# ---------------------------------------------------------------------------

def cmul(c1, c2):
    out = {}
    for m1, k1 in c1.items():
        for m2, k2 in c2.items():
            m = tuple(sorted(m1 + m2))
            out[m] = out.get(m, 0) + k1 * k2
    return {m: k for m, k in out.items() if k}


def cadd(c1, c2):
    out = dict(c1)
    for m, k in c2.items():
        out[m] = out.get(m, 0) + k
    return {m: k for m, k in out.items() if k}


def cscale(c, n):
    return {m: k * n for m, k in c.items() if k * n}


def padd(p1, p2):
    out = dict(p1)
    for mon, c in p2.items():
        merged = cadd(out.get(mon, {}), c)
        if merged:
            out[mon] = merged
        else:
            out.pop(mon, None)
    return out


def term(i, j, coeff):
    """single term coeff * x^i * y^j."""
    return {(i, j): dict(coeff)} if coeff else {}


def sym(name):
    return {(name,): 1}


def const(n):
    return {(): n} if n else {}


def pmul_monomial(p, i, j, coeff):
    """multiply a polynomial by a single term coeff * x^i * y^j."""
    out = {}
    for (a, b), c in p.items():
        m = (a + i, b + j)
        merged = cadd(out.get(m, {}), cmul(c, coeff))
        if merged:
            out[m] = merged
    return out


# ---------------------------------------------------------------------------
# the bracket
# ---------------------------------------------------------------------------

def bracket_by_rule(p, q):
    """[p, q] using ONLY the monomial rule
       [x^a y^b, x^c y^d] = (a*d - b*c) x^(a+c-1) y^(b+d-1)."""
    out = {}
    for (a, b), cp in p.items():
        for (c, d), cq in q.items():
            factor = a * d - b * c
            if factor == 0:
                continue
            mon = (a + c - 1, b + d - 1)
            contrib = cscale(cmul(cp, cq), factor)
            merged = cadd(out.get(mon, {}), contrib)
            if merged:
                out[mon] = merged
            else:
                out.pop(mon, None)
    return out


def d_dx(p):
    out = {}
    for (i, j), c in p.items():
        if i > 0:
            out[(i - 1, j)] = cadd(out.get((i - 1, j), {}), cscale(c, i))
    return {m: c for m, c in out.items() if c}


def d_dy(p):
    out = {}
    for (i, j), c in p.items():
        if j > 0:
            out[(i, j - 1)] = cadd(out.get((i, j - 1), {}), cscale(c, j))
    return {m: c for m, c in out.items() if c}


def pmul(p, q):
    out = {}
    for (a, b), cp in p.items():
        for (c, d), cq in q.items():
            m = (a + c, b + d)
            merged = cadd(out.get(m, {}), cmul(cp, cq))
            if merged:
                out[m] = merged
    return out


def psub(p, q):
    return padd(p, {m: cscale(c, -1) for m, c in q.items()})


def bracket_by_derivatives(p, q):
    """[p, q] = p_x*q_y - p_y*q_x, computed by explicit differentiation."""
    return psub(pmul(d_dx(p), d_dy(q)), pmul(d_dy(p), d_dx(q)))


# ---------------------------------------------------------------------------
# display
# ---------------------------------------------------------------------------

def cstr(c):
    if not c:
        return "0"
    parts = []
    for m in sorted(c):
        k = c[m]
        body = "*".join(m) if m else ""
        if body:
            parts.append(("%+d*%s" % (k, body)) if abs(k) != 1
                         else ("%s%s" % ("+" if k > 0 else "-", body)))
        else:
            parts.append("%+d" % k)
    return "".join(parts).lstrip("+")


def pstr(p):
    if not p:
        return "0"
    bits = []
    for (i, j) in sorted(p):
        bits.append("(%s)*x^%d*y^%d" % (cstr(p[(i, j)]), i, j))
    return " + ".join(bits)


def report(name, ok):
    print("%s %s" % ("PASS" if ok else "FAIL", name))
    return ok


# ---------------------------------------------------------------------------
# item 0 -- the rule itself
# ---------------------------------------------------------------------------

def item0():
    print("=" * 72)
    print("ITEM 0  bracket rule vs explicit differentiation")
    print("=" * 72)
    ok = True
    checked = 0
    for a in range(0, 8):
        for b in range(0, 8):
            for c in range(0, 8):
                for d in range(0, 8):
                    p = term(a, b, sym("s"))
                    q = term(c, d, sym("t"))
                    lhs = bracket_by_rule(p, q)
                    rhs = bracket_by_derivatives(p, q)
                    checked += 1
                    if lhs != rhs:
                        ok = False
                        print("  mismatch at (a,b,c,d)=(%d,%d,%d,%d): %s vs %s"
                              % (a, b, c, d, pstr(lhs), pstr(rhs)))
    print("  compared %d monomial pairs, exponents 0..7" % checked)
    print("  rule used: [x^a y^b, x^c y^d] = (a*d - b*c) x^(a+c-1) y^(b+d-1)")
    return report("item 0: monomial bracket rule agrees with p_x q_y - p_y q_x", ok)


# ---------------------------------------------------------------------------
# item 1 -- orientation A, weight w(i,j) = 10i - 13j, u = x^13 y^10
# ---------------------------------------------------------------------------

def item1():
    print()
    print("=" * 72)
    print("ITEM 1  w(i,j) = 10i - 13j,  u = x^13*y^10")
    print("=" * 72)
    U = (13, 10)
    # P_w = x*(a0 + a1*u) = a0*x + a1*x^14*y^10
    P = padd(term(1, 0, sym("a0")), term(1 + U[0], U[1], sym("a1")))
    # Q_w = b*x^4*y
    Q = term(4, 1, sym("b"))
    print("  P_w = %s" % pstr(P))
    print("  Q_w = %s" % pstr(Q))

    got = bracket_by_rule(P, Q)
    print("  [P_w, Q_w] = %s" % pstr(got))

    # weight check: every monomial of P_w has the same w, likewise Q_w
    wP = {10 * i - 13 * j for (i, j) in P}
    wQ = {10 * i - 13 * j for (i, j) in Q}
    print("  w-values on P_w: %s ; on Q_w: %s" % (sorted(wP), sorted(wQ)))

    # claimed RHS: x^4*(a0*b - 26*a1*b*u), built here term by term
    claimed = padd(term(4, 0, cmul(sym("a0"), sym("b"))),
                   term(4 + U[0], U[1], cscale(cmul(sym("a1"), sym("b")), -26)))
    print("  claimed    = %s" % pstr(claimed))

    ok = (got == claimed)
    if not ok:
        for m in sorted(set(got) | set(claimed)):
            g, c = got.get(m, {}), claimed.get(m, {})
            if g != c:
                print("    x^%d*y^%d : computed %s , claimed %s"
                      % (m[0], m[1], cstr(g), cstr(c)))

    # the derived number in the u-slot, printed rather than assumed
    slot = got.get((4 + U[0], U[1]), {})
    derived = slot.get(tuple(sorted(("a1", "b"))), 0)
    print("  DERIVED coefficient of x^4*u (i.e. x^17*y^10) : %d * a1*b" % derived)
    print("    from the rule with (a,b,c,d) = (14,10,4,1): a*d - b*c = %d"
          % (14 * 1 - 10 * 4))
    return report("item 1: [P_w,Q_w] == x^4*(a0*b - 26*a1*b*u) coefficient by "
                  "coefficient over Z", ok), derived


# ---------------------------------------------------------------------------
# item 2 -- orientation B, weight w(i,j) = 3i - 4j, v = x^4 y^3
# ---------------------------------------------------------------------------

def item2():
    print()
    print("=" * 72)
    print("ITEM 2  w(i,j) = 3i - 4j,  v = x^4*y^3")
    print("=" * 72)
    V = (4, 3)
    # P_w = a*x^4*y
    P = term(4, 1, sym("a"))
    # Q_w = x * sum_{j=0..5} b_j * v^j
    Q = {}
    for j in range(6):
        Q = padd(Q, term(1 + V[0] * j, V[1] * j, sym("b%d" % j)))
    print("  P_w = %s" % pstr(P))
    print("  Q_w = %s" % pstr(Q))
    wP = {3 * i - 4 * j for (i, j) in P}
    wQ = {3 * i - 4 * j for (i, j) in Q}
    print("  w-values on P_w: %s ; on Q_w: %s" % (sorted(wP), sorted(wQ)))

    got = bracket_by_rule(P, Q)
    print("  [P_w, Q_w] = %s" % pstr(got))

    # derive, for each j, the integer multiplying a*b_j in the x^4*v^j slot
    print()
    print("  DERIVED coefficients (nothing copied; each read off the rule):")
    derived = {}
    all_match_8j_minus_1 = True
    for j in range(6):
        mon = (4 + V[0] * j, V[1] * j)
        c = got.get(mon, {})
        key = tuple(sorted(("a", "b%d" % j)))
        n = c.get(key, 0)
        derived[j] = n
        # what the rule gives directly, for the record
        a_, b_, c_, d_ = 4, 1, 1 + V[0] * j, V[1] * j
        direct = a_ * d_ - b_ * c_
        flag = "" if n == 8 * j - 1 else "   <-- NOT 8j-1"
        if n != 8 * j - 1:
            all_match_8j_minus_1 = False
        print("    j=%d : x^%d*y^%d  coefficient of a*b%d = %+d   "
              "(rule: a*d-b*c = %d*%d - %d*%d = %+d)   8j-1 = %+d%s"
              % (j, mon[0], mon[1], j, n, a_, d_, b_, c_, direct, 8 * j - 1, flag))
        if n != direct:
            print("      INTERNAL INCONSISTENCY: expansion %d vs direct rule %d"
                  % (n, direct))

    print()
    print("  So [P_w,Q_w] = a*x^4 * sum_j (%s) * b_j * v^j"
          % ", ".join("%+d" % derived[j] for j in range(6)))
    print("  The derived sign pattern is (8j - 1), i.e. NEGATIVE at j=0 (-1) and")
    print("  positive for j >= 1.  This was computed, not assumed.")

    # rebuild from the derived numbers and confirm it reproduces the expansion
    rebuilt = {}
    for j in range(6):
        rebuilt = padd(rebuilt, term(4 + V[0] * j, V[1] * j,
                                     cscale(cmul(sym("a"), sym("b%d" % j)),
                                            derived[j])))
    ok = (rebuilt == got)
    report("item 2: expansion is exactly a*x^4*sum_j c_j*b_j*v^j with the "
           "derived c_j", ok)
    report("item 2: derived c_j equal (8j - 1) for j = 0..5", all_match_8j_minus_1)
    return ok and all_match_8j_minus_1, derived


# ---------------------------------------------------------------------------
# item 3 -- the kill, over Z and mod each prime
# ---------------------------------------------------------------------------

def nonzero_everywhere(n, label):
    """n != 0 over Z and n != 0 mod each prime."""
    good = True
    bits = ["Z: %s" % ("nonzero" if n != 0 else "ZERO")]
    if n == 0:
        good = False
    for p in PRIMES:
        r = n % p
        bits.append("mod %d: %s" % (p, "nonzero" if r else "ZERO"))
        if r == 0:
            good = False
    print("    %s = %+d  ->  %s" % (label, n, ", ".join(bits)))
    return good


def item3(coef_A, coef_B):
    print()
    print("=" * 72)
    print("ITEM 3  the kill, with target x^4")
    print("=" * 72)
    print("  Target x^4 means: in the bracket, every monomial OTHER than x^4*y^0")
    print("  must have zero coefficient, and the x^4 coefficient must be nonzero.")
    print()

    print("  Orientation A  (item 1):")
    print("    [P_w,Q_w] = (a0*b)*x^4 + (%d*a1*b)*x^17*y^10" % coef_A)
    print("    off-target slot x^17*y^10 must vanish:")
    okA = nonzero_everywhere(coef_A, "coefficient of a1*b")
    print("    => %d*a1*b = 0 with %d invertible  =>  a1*b = 0  =>  a1 = 0 or b = 0."
          % (coef_A, coef_A))
    print("    and the target slot needs a0*b != 0, which forces b != 0,")
    print("    hence a1 = 0.")
    okA = report("item 3A: a1 = 0 (or b = 0) forced over Z and mod both primes", okA)

    print()
    print("  Orientation B  (item 2):")
    print("    [P_w,Q_w] = a*x^4 * sum_j c_j*b_j*v^j,  c_j as derived above.")
    print("    target x^4 is the j=0 slot, so every j >= 1 slot must vanish:")
    okB = True
    for j in range(1, 6):
        okB &= nonzero_everywhere(coef_B[j], "c_%d (coefficient of a*b_%d)" % (j, j))
    print("    each c_j (j>=1) is invertible over Z and mod both primes, and the")
    print("    target slot needs c_0*a*b_0 != 0, which forces a != 0;")
    print("    hence a*b_j = 0 with a != 0 gives b_j = 0 for every j = 1..5,")
    print("    in particular b_5 = 0.")
    okB = report("item 3B: b_5 = 0 forced over Z and mod both primes "
                 "(and likewise b_1..b_4)", okB)
    return okA and okB


# ---------------------------------------------------------------------------

def main():
    print("face_check_84126 -- exact integer face check, stdlib only")
    print("primes used for the modular statements: %s" % (PRIMES,))
    print()
    r0 = item0()
    r1, coef_A = item1()
    r2, coef_B = item2()
    r3 = item3(coef_A, coef_B)
    print()
    print("=" * 72)
    allok = r0 and r1 and r2 and r3
    print("%s OVERALL: all items" % ("PASS" if allok else "FAIL"))
    print("=" * 72)
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
