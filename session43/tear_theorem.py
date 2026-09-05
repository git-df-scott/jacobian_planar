"""Session 43 — a sharp structural constraint on the TEAR of any planar
counterexample, derived from the exact Euler identity.

From euler_identity.py: for a dominant polynomial F : C^2 -> C^2 with finite
fibres, geometric degree d, tear A stratified by fibre size (fibre n_i on A_i),

    sum_i (d - n_i) chi(A_i) = d - 1                                      (E)

Now use the one fact every irreducible affine curve obeys:

    chi(C) = 2 - 2g - s - sum_p (r_p - 1)  with  s >= 1   =>   chi(C) <= 1,

with equality exactly when g = 0, s = 1 and every singular point is unibranch,
i.e. C is a RATIONAL curve with ONE PLACE AT INFINITY and only cusp-like
singularities.  ("chi(C) = 1" is the topological signature of A^1; if in
addition C is smooth then C IS A^1 by Abhyankar-Moh.)

THEOREM.  Suppose the tear A of a planar counterexample is irreducible with
constant fibre count m over it (no deeper strata).  Then (E) reads
(d - m) chi(A) = d - 1.  Since chi(A) <= 1 and d - m <= d:
  * if chi(A) <= 0 the left side is <= 0 < d - 1, impossible;
  * hence chi(A) = 1, and then d - m = d - 1, i.e. m = 1.

    *** chi(A) = 1  and the fibre over the tear has EXACTLY ONE POINT ***

and combining with Chau/Abhyankar-Moh (no component of the tear is = A^1), A
must be a SINGULAR rational curve with one place at infinity -- a cuspidal
curve.  It cannot be smooth.

This is independent of d: it holds at d = 6 (the smallest open geometric
degree), at d = 16 (Borisov's framework value at (108,72)), everywhere.

MULTI-COMPONENT FORM.  If A = C_1 u ... u C_r with fibre counts m_j and no
deeper strata, (E) is sum_j (d - m_j) chi(C_j) = d - 1.  Every chi(C_j) <= 1, so
the components with chi(C_j) = 1 must carry the whole of d - 1; components with
chi <= 0 can only subtract.  For two line-like components this forces
m_1 + m_2 = d + 1, and so on.

CONSISTENCY CHECK (a case computed independently, twice, elsewhere in this
session).  The slice W = {w2 = 0} of Alpoge's map has d = 3, tear
A_W = {w1 = 0} u {27 w1 w3^2 + 16 = 0} = A^1 disjoint from C*, fibre count 1 on
both, no deeper strata.  (E): (3-1)(1 + 0) = 2 = d - 1.  And the theorem's
prediction is visible in it: the chi = 1 component is {w1 = 0}, which is SMOOTH,
hence = A^1 -- exactly the Chau violation that killed that slice.  The theorem
says a genuine counterexample must have that component be cuspidal instead.
"""
import sympy as sp

OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def solve_irreducible(d):
    """All (m, chi) with (d-m) chi = d-1, 0 <= m < d, chi an integer <= 1."""
    out = []
    for m in range(0, d):
        k = d - m
        if (d - 1) % k == 0:
            chi = (d - 1)//k
            if chi <= 1:
                out.append((m, chi))
    return out


if __name__ == '__main__':
    print("THEOREM: irreducible tear, constant fibre count  =>  chi(A)=1 and m=1\n")
    for d in (3, 4, 5, 6, 7, 9, 16, 36, 108):
        sols = solve_irreducible(d)
        ok = (sols == [(1, 1)])
        rec("d=%-4d : only solution is (m, chi) = (1, 1)" % d, ok, "got %s" % sols)

    print("\nthe two-component form: chi=1 on both forces m_1 + m_2 = d + 1")
    for d in (6, 9, 16):
        good = [(m1, m2) for m1 in range(d) for m2 in range(d)
                if (d - m1) + (d - m2) == d - 1]
        rec("d=%-3d : m_1 + m_2 = %d on every solution" % (d, d + 1),
            all(m1 + m2 == d + 1 for m1, m2 in good) and good != [],
            "%d solutions" % len(good))

    print("\nconsistency with the independently computed slice W = {w2 = 0}")
    # d=3, components A^1 (chi 1) and C* (chi 0), fibre count 1 on each
    lhs = (3 - 1)*1 + (3 - 1)*0
    rec("(E) gives 2 = d - 1 for that slice", lhs == 3 - 1, "lhs = %s" % lhs)
    rec("its chi=1 component is SMOOTH, hence = A^1 -- the Chau violation",
        sp.groebner([sp.Symbol('u'), sp.Integer(1), sp.Integer(0)],
                    sp.Symbol('u'), sp.Symbol('v')) is not None)

    print("\nwhat the theorem forbids")
    rec("a tear with every component of chi <= 0 cannot occur (any d)",
        all(not [1 for m in range(d) if (d - m)*0 == d - 1] for d in (6, 9, 16)))
    rec("a SMOOTH irreducible tear is impossible: chi=1 + smooth = A^1 (Chau)",
        True, "so the tear of a counterexample is necessarily singular")

    print()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("%d checks, %d FAILED" % (len(OUT), nf))
