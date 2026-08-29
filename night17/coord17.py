"""night17 -- coordinate pairs with a verified mate, for the controls.

(F, G) starts at (x, y) with [F, G] = F_x G_y - F_y G_x = 1 and is moved by two
bracket-preserving operations:

    T_p : (F, G) -> (F, G + p(F))       (triangular)
    S   : (F, G) -> (G, -F)             (swap)

[T_p F, T_p G] = F_x (G_y + p'(F) F_y) - F_y (G_x + p'(F) F_x) = [F, G] and
[G, -F] = G_x (-F_y) - G_y (-F_x) = [F, G], so every word in T and S produces a
pair with [F, G] = 1 -- verified coefficientwise over Q by pk17.bracket.
"""
from fractions import Fraction as F
import pk17 as pk

Xp = {(1, 0): F(1)}
Yp = {(0, 1): F(1)}


def poly1(coeffs):
    """univariate p(t) = sum coeffs[i] t^i as a polynomial in a placeholder."""
    return {(i, 0): F(c) for i, c in enumerate(coeffs) if F(c) != 0}


def apply_T(FG, p):
    Fp, Gp = FG
    # p(F): substitute F into the univariate p (given in the x-slot)
    pF = pk.compose(p, Fp, {})
    return (Fp, pk.padd(Gp, pF))


def apply_S(FG):
    Fp, Gp = FG
    return (Gp, pk.pscal(-1, Fp))


def build(word):
    """word: list of ('T', coeffs) / ('S',).  Returns (P, Q) with [P,Q] = 1."""
    FG = (Xp, Yp)
    for w in word:
        FG = apply_T(FG, poly1(w[1])) if w[0] == "T" else apply_S(FG)
    Pp, Qp = FG
    assert pk.bracket(Pp, Qp) == {(0, 0): F(1)}, "bracket check failed"
    return Pp, Qp


def deg_y2_coordinate(pdeg, seed=1):
    """P = -x + q(y + p(x)) with deg q = 2: deg_y P = 2, deg P = 2*pdeg."""
    pc = [F(0)] + [F((seed * (i + 3)) % 7 + 1, (i % 3) + 1) for i in range(pdeg)]
    qc = [F(1), F(2), F(3, 2)]
    return build([("T", pc), ("S",), ("T", qc), ("S",)])
