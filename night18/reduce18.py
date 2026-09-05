"""night18 -- the structural reduction behind the two-chart cover.

Every member of the deg g = 1 stratum is the image, under the Jacobian-1
substitution  (x, y) -> (x + a,  y + p(x + a)),  p := (h - h(a)) / (2 gamma (x-a)),
followed by nothing else, of the THREE-parameter member

        Ptilde = gamma * x * y^2 + h(a) * y + const .

p is a polynomial identically in the parameters (h - h(a) vanishes at x = a),
of degree deg h - 1; for deg h = 1 it is a CONSTANT, so the substitution is a
degree-0 shear and preserves every carrier deg Q <= D exactly.
"""
import json, os, sys
import sympy as sp
import spk18 as spk, fam18

X, Y = spk.X, spk.Y
HERE = os.path.dirname(os.path.abspath(__file__))


def reduce_member(H):
    F = fam18.family(H)
    gam, a, ha, h = F['gam'], F['a'], F['ha'], F['h']
    p = sp.cancel(sp.together((h - ha) / (2 * gam * (X - a))))
    p = sp.simplify(sp.expand(p))
    Pe = spk.to_expr(F['P'])
    # translate x -> x + a, then shear y -> y + p(x + a)
    Pt = sp.expand(Pe.subs(X, X + a))
    ps = sp.expand(p.subs(X, X + a))
    Pt = sp.expand(Pt.subs(Y, Y - ps))
    Pt = sp.expand(sp.cancel(sp.together(Pt)))
    target = sp.expand(gam * X * Y**2 + ha * Y)
    const = sp.expand(sp.cancel(sp.together(Pt - target)))
    jac = sp.expand(sp.diff(X + a, X) * sp.diff(Y - ps, Y)
                    - sp.diff(X + a, Y) * sp.diff(Y - ps, X))
    return {"deg_h": H, "p": sp.sstr(p), "deg_p": int(sp.degree(sp.Poly(p, X))) if p.free_symbols & {X} else 0,
            "p_is_polynomial": bool(sp.denom(sp.cancel(p)).free_symbols <= set(F['free'])),
            "jacobian_of_substitution": sp.sstr(jac),
            "image": sp.sstr(Pt), "reduced_form": sp.sstr(target),
            "image_minus_reduced_form": sp.sstr(const),
            "difference_is_a_constant_in_x_y": bool(not (const.free_symbols & {X, Y})),
            "carrier_preserving": bool(int(sp.degree(sp.Poly(p, X))) <= 0
                                       if p.free_symbols & {X} else True)}


if __name__ == "__main__":
    out = {}
    for H in (1, 2, 3):
        r = reduce_member(H)
        out[str(H)] = r
        print("deg h=%d  p = %s  (deg_x p = %d, Jacobian = %s)"
              % (H, r['p'], r['deg_p'], r['jacobian_of_substitution']))
        print("   image - (gamma x y^2 + h(a) y) = %s" % r['image_minus_reduced_form'])
        print("   constant in x,y : %s   carrier-preserving shear : %s"
              % (r['difference_is_a_constant_in_x_y'], r['carrier_preserving']))
    json.dump(out, open(os.path.join(HERE, 'reduce18.json'), 'w'), indent=1)
