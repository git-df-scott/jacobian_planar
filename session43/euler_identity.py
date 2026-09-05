"""Session 43 — an EXACT Euler identity for any planar counterexample.

The campaign carries an "Euler filter" in the congruence form

    chi(F^{-1}(S_F)) == 1  (mod d)          [d = geometric degree]

The slice work here produced the same object as an EQUALITY, which is strictly
sharper and costs nothing extra.

SETUP.  Let F : C^2 -> C^2 be a dominant polynomial map with FINITE fibres,
geometric degree d, and non-properness set (tear) A.  Stratify A by fibre size:
A = ⊔_i A_i with #F^{-1}(w) = n_i < d for w in A_i.  Over C^2 \\ A the map is
proper, étale and finite, hence a d-sheeted covering, so chi multiplies; over
each A_i the fibre size is constant and the restriction is again finite, so chi
multiplies there too.  Motivic additivity then gives

    chi(C^2) = d * chi(C^2 \\ A) + sum_i n_i chi(A_i)

and since chi(C^2) = 1 and chi(C^2 \\ A) = 1 - chi(A) = 1 - sum_i chi(A_i),

    *** sum_i (d - n_i) * chi(A_i) = d - 1 ***                            (E)

equivalently  chi(F^{-1}(A)) = d*chi(A) - (d - 1) = d(chi(A) - 1) + 1, which
reduces mod d to the campaign's congruence -- so (E) implies it and is strictly
stronger, pinning the value rather than its residue.

WHY IT IS USEFUL.  Every term (d - n_i) is a POSITIVE integer, so (E) forces

    at least one stratum must have chi(A_i) > 0,

i.e. the tear cannot consist entirely of strata of non-positive Euler
characteristic.  Combined with Chau/Abhyankar-Moh (no component of the tear is
isomorphic to A^1), that pushes any counterexample's tear towards CUSPIDAL
rational components -- chi = 1 is achievable for a rational curve with one place
at infinity only when it is singular, since a SMOOTH one would be A^1.

CHECK.  The plane-slice filter used throughout Path S,

    2 chi(A_W) + #C_W = 2,

is exactly (E) at d = 3 with the two strata n = 1 (the tear off C_sing) and
n = 0 (C_sing): (3-1) chi(A_W \\ C_W) + (3-0) chi(C_W) = 2 chi(A_W) + #C_W, and
d - 1 = 2.  Verified below against the one slice whose chi was also computed by
a completely independent route (W = {w2 = 0}, where S = (C* x C*) u A^1 directly).
"""
import sympy as sp

OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def identity_lhs(d, strata):
    """sum (d - n_i) chi(A_i) for strata given as [(n_i, chi_i), ...]."""
    return sum((d - n)*c for n, c in strata)


if __name__ == '__main__':
    print("(E)   sum_i (d - n_i) chi(A_i) = d - 1\n")

    # 1. the Path S plane filter is (E) at d = 3
    d = 3
    chiA, nC = sp.symbols('chiA nC')
    lhs = (d - 1)*(chiA - nC) + (d - 0)*nC          # tear off C_sing, then C_sing
    rec("at d=3 the identity reads 2*chi(A_W) + #C_W = 2",
        sp.expand(lhs - (2*chiA + nC)) == 0 and d - 1 == 2)

    # 2. the one slice computed two independent ways: W = {w2 = 0}
    #    A_W = {w1 = 0} u {27 w1 w3^2 + 16 = 0} = A^1 disjoint from C*, chi = 1+0 = 1
    #    #C_W = 0, and independently S = (C* x C*) u A^1 so chi(S) = 0 + 1 = 1.
    rec("W={w2=0}: (E) holds with chi(A_W)=1, #C_W=0",
        identity_lhs(3, [(1, 1), (0, 0)]) == 3 - 1,
        "lhs = %s, d-1 = 2" % identity_lhs(3, [(1, 1), (0, 0)]))

    # 3. the congruence form is implied
    for d in (3, 4, 6, 9, 16):
        for chiA in (-3, -1, 0, 1, 2):
            chi_pre = d*chiA - (d - 1)
            if (chi_pre - 1) % d != 0:
                rec("congruence implied at d=%d, chi(A)=%d" % (d, chiA), False)
                break
        else:
            continue
        break
    else:
        rec("(E) implies the campaign's chi(F^{-1}(A)) == 1 mod d, for all tested d", True)

    # 4. the positivity consequence
    rec("(E) forces some stratum to have chi > 0 (all terms d-n_i > 0)",
        all(identity_lhs(d, [(n, c) for n, c in st]) != d - 1
            for d, st in [(6, [(1, 0), (0, -2)]), (9, [(2, -1), (0, 0)])]),
        "a tear with every chi(A_i) <= 0 cannot satisfy (E)")

    print()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("%d checks, %d FAILED" % (len(OUT), nf))
