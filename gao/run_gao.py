import json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from w5_gao_audit import (x, y, z, u, v, V, RESULTS, check, detJ3, F_ALP, G_GAO,
                          gao_recipe, find_weights, invariant_generators,
                          build_descent, mono)

print("=" * 78)
print("T5  GAO FAMILY MECHANISM AUDIT  (arXiv:2608.00222v1)")
print("=" * 78)

w = sp.Symbol('w')
MEMBERS = []

# ---- rebuild G from the recipe, independently of the printed components ----
p3 = w**3 - 6*w**2 + 6*w
q3 = sp.Rational(3,8)*w**4 - 2*w**3 + sp.Rational(3,2)*w**2
gam3 = 2 - 4*x*y - x**2*z
G_rebuilt = gao_recipe(p3, q3, gam3)
same = all(sp.expand(a - b) == 0 for a, b in zip(G_rebuilt, G_GAO))
check("section 3.5: the printed components of G equal the recipe of section 3.3 "
      "run with deg p = 3", same,
      "printed vs rebuilt differ" if not same else "exact match, all 3 components")

p2 = -3*w**2 + 4*w
q2 = -w**3 + w**2
gam2 = 2 - 3*x*y - x**2*z
F_rebuilt = gao_recipe(p2, q2, gam2)     # sweep order: (C, .., ..)
# Alpoge order reverses the outer components
F_rebuilt_alp = [F_rebuilt[2], F_rebuilt[1], F_rebuilt[0]]
same2 = all(sp.expand(a - b) == 0 for a, b in zip(F_rebuilt_alp, F_ALP))
check("section 3.4: the printed components of F equal the recipe run with "
      "deg p = 2, after the stated component reversal", same2)

for name, F, ref, printed_det, printed_deg, printed_gd in [
        ("F_sec3.4_Alpoge", F_ALP, "2608.00222 section 3.4, p.6, Theorem 3.3",
         -2, (7, 6, 4), 3),
        ("G_sec3.5", G_GAO, "2608.00222 section 3.5, p.7, Theorem 3.5",
         2, (4, 11, 12), 4)]:
    print(f"\n  --- {name}  [{ref}] ---")
    J = detJ3(F)
    isconst = not (J.free_symbols & {x, y, z})
    check(f"{name}: det J is a nonzero constant", isconst and J != 0, f"det J = {J}")
    check(f"{name}: det J equals the printed value {printed_det}",
          sp.simplify(J - printed_det) == 0, f"computed {J}")
    degs = tuple(sp.Poly(f, x, y, z).total_degree() for f in F)
    check(f"{name}: component degrees equal the printed {printed_deg}",
          sorted(degs) == sorted(printed_deg), f"computed {degs}")

    wts = find_weights(F)
    check(f"{name}: a C*-weight structure exists and is found", len(wts) > 0,
          f"{wts}")
    entry = {"name": name, "reference": ref, "dimension": 3,
             "components": [sp.sstr(f) for f in F],
             "component_degrees": list(degs), "detJ": sp.sstr(J),
             "printed_detJ": printed_det,
             "printed_geometric_degree": printed_gd,
             "weight_systems": [[list(wv), list(d)] for wv, d in wts],
             "k_from_W3_4a": None, "k_from_detJG": None,
             "descent": None, "noninjectivity_witness": None,
             "flag": None}
    for wv, d in wts:
        gens = invariant_generators(wv)
        if len(gens) != 2:
            continue
        p1e, p2e = gens
        k_formula = (sum(p1e) + sum(p2e)) - 3
        res = build_descent(F, wv, gens)
        if res is None:
            continue
        G, JG, P1, P2 = res
        fac = sp.factor(JG)
        # read the exponent of the non-constant factor
        k_direct, hfac = 0, None
        ff = sp.factor_list(sp.expand(JG))
        for base, e in ff[1]:
            if base.free_symbols & {u, v}:
                k_direct += e
                hfac = base
        entry["weights_used"] = list(wv)
        entry["invariant_generators"] = [sp.sstr(mono(p1e)), sp.sstr(mono(p2e))]
        entry["k_from_W3_4a"] = int(k_formula)
        entry["k_from_detJG"] = int(k_direct)
        entry["descent"] = [sp.sstr(g) for g in G]
        entry["detJG"] = sp.sstr(fac)
        entry["h"] = sp.sstr(hfac)
        print(f"      weights {wv}: pi = ({sp.sstr(mono(p1e))}, {sp.sstr(mono(p2e))}), "
              f"descent det J = {fac}")
        check(f"{name}: k from LEMMA W3-4a equals k from det J(descent) "
              f"(weights {wv})", k_formula == k_direct,
              f"formula {k_formula} vs direct {k_direct}")
        break
    MEMBERS.append(entry)

# ---- non-injectivity witnesses -------------------------------------------
print("\n  NON-INJECTIVITY WITNESSES")
pts = [(sp.Integer(0), sp.Integer(0), sp.Rational(-1, 4)),
       (sp.Integer(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
       (sp.Integer(-1), sp.Rational(3, 2), sp.Rational(13, 2))]
imgs = [tuple(sp.simplify(f.subs({x: a, y: b, z: c})) for f in F_ALP) for a, b, c in pts]
check("section 3.4's printed witness: three distinct points with one image",
      len(set(pts)) == 3 and imgs[0] == imgs[1] == imgs[2]
      and imgs[0] == (sp.Rational(-1, 4), sp.Integer(0), sp.Integer(0)),
      f"images {imgs}")
MEMBERS[0]["noninjectivity_witness"] = {
    "points": [[sp.sstr(c) for c in p] for p in pts],
    "common_image": [sp.sstr(c) for c in imgs[0]], "verified": True}

# a witness for G is SEARCHED for exactly, in exact rational arithmetic
from fractions import Fraction as Fr
GP = [sp.Poly(f, x, y, z) for f in G_GAO]
GT = [[(m, Fr(int(sp.Rational(c).p), int(sp.Rational(c).q))) for m, c in
       zip(pp.monoms(), pp.coeffs())] for pp in GP]
def evalG(a, b, c):
    out = []
    for terms in GT:
        acc = Fr(0)
        for (i, j, k), co in terms:
            acc += co * a ** i * b ** j * c ** k
        out.append(acc)
    return tuple(out)

grid = [Fr(n, d) for d in (1, 2, 3, 4) for n in range(-8, 9)]
grid = sorted(set(grid))
found = None
seen = {}
for a in grid:
    for b in grid:
        for c in grid:
            key = evalG(a, b, c)
            if key in seen and seen[key] != (a, b, c):
                found = (seen[key], (a, b, c), key)
                break
            seen[key] = (a, b, c)
        if found:
            break
    if found:
        break
if found:
    p_, q_, img = found
    subs1 = {x: sp.Rational(p_[0]), y: sp.Rational(p_[1]), z: sp.Rational(p_[2])}
    subs2 = {x: sp.Rational(q_[0]), y: sp.Rational(q_[1]), z: sp.Rational(q_[2])}
    ok = all(sp.simplify(f.subs(subs1) - f.subs(subs2)) == 0 for f in G_GAO)
    check("section 3.5's G: an exact non-injectivity witness was FOUND and "
          "verified by substitution", ok and p_ != q_,
          f"{p_} and {q_} -> {img}")
    MEMBERS[1]["noninjectivity_witness"] = {
        "points": [[str(c) for c in p_], [str(c) for c in q_]],
        "common_image": [str(c) for c in img], "verified": bool(ok)}
else:
    check("section 3.5's G: an exact non-injectivity witness was found in the "
          "probed rational box", False,
          "none in the box; recorded as DONE-NO-VERDICT for this leg")
    MEMBERS[1]["noninjectivity_witness"] = {"searched_box": "n/d, |n|<=8, d<=4",
                                            "found": False}

# ---- NEGATIVE CONTROLS ----------------------------------------------------
print("\n  NEGATIVE CONTROLS")
Fbad = list(F_ALP)
Fbad[2] = sp.expand(Fbad[2] + x ** 2 * y)          # one coefficient changed
Jbad = detJ3(Fbad)
check("NEGATIVE: one corrupted coefficient makes det J non-constant",
      bool(Jbad.free_symbols & {x, y, z}), f"det J = {sp.factor(Jbad)}")

# k = 0 class: weights (1,-1,0), invariants xy and z -> k = 2 + 1 - 3 = 0.
# The direct route reads the exponent of the non-constant factor of det J of the
# DESCENT, which is only meaningful when the map upstairs is itself Keller, so
# a Keller representative of the class is used: F0 = (x, y, z + x^2 y^2), whose
# descent is the plane automorphism (u, v + u^2).
F0 = [x, y, sp.expand(z + x ** 2 * y ** 2)]
JF0 = detJ3(F0)
wts0 = find_weights(F0)
has = any(tuple(wv) == (1, -1, 0) for wv, _ in wts0)
gens0 = invariant_generators((1, -1, 0))
kf0 = sum(gens0[0]) + sum(gens0[1]) - 3 if len(gens0) == 2 else None
res0 = build_descent(F0, (1, -1, 0), gens0)
kd0 = None
if res0:
    _, JG0, _, _ = res0
    kd0 = sum(e for base, e in sp.factor_list(sp.expand(JG0))[1]
              if base.free_symbols & {u, v})
check("NEGATIVE: in the k=0 weight class (1,-1,0) BOTH routes give k = 0, i.e. "
      "the exponent is not hard-wired to 2",
      has and kf0 == 0 and kd0 == 0 and JF0 == 1,
      f"weights found {has}, det J upstairs = {JF0}, formula k = {kf0}, "
      f"direct k = {kd0}")

badpts = ((sp.Integer(0), sp.Integer(0), sp.Integer(0)),
          (sp.Integer(1), sp.Integer(1), sp.Integer(1)))
same_img = all(sp.simplify(f.subs({x: badpts[0][0], y: badpts[0][1], z: badpts[0][2]})
                           - f.subs({x: badpts[1][0], y: badpts[1][1], z: badpts[1][2]})) == 0
               for f in F_ALP)
check("NEGATIVE: the witness verifier REJECTS a non-witness", not same_img,
      "(0,0,0) and (1,1,1) do not share an image")

# ---- dimension > 3: record and skip --------------------------------------
HIGHER = [
 {"name": "F4", "dimension": 4, "reference": "section 4.4.1, p.13-14, Theorem 4.3",
  "component_degrees": [4, 11, 12, 21], "detJ": "-44/9", "geometric_degree": 5,
  "direction_field": "(1, w1, w1^2)^T", "computed": False,
  "note": "recorded and skipped per brief (dimension > 3)"},
 {"name": "F5", "dimension": 4, "reference": "section 4.4.2",
  "component_degrees": None, "detJ": None, "geometric_degree": 10,
  "direction_field": "(1, w1, w2)^T", "computed": False,
  "note": "recorded and skipped per brief (dimension > 3)"},
 {"name": "F6", "dimension": 5, "reference": "section 4.5",
  "component_degrees": None, "detJ": "-290", "geometric_degree": 6,
  "direction_field": "(1, w1, w1^2, w2)^T, bottom (L1-)branch", "computed": False,
  "note": "recorded and skipped per brief (dimension > 3)"},
 {"name": "F7", "dimension": 5, "reference": "section 4.6 and the table on p.15",
  "component_degrees": None, "detJ": "det J(F0) = gamma^2; table entry 119377",
  "geometric_degree": 12, "direction_field": "(1, w1, ..., w1^{n-2})^T",
  "computed": False, "note": "recorded and skipped per brief (dimension > 3)"},
]

for m in MEMBERS:
    if m["k_from_W3_4a"] == 0:
        m["flag"] = "PORT-CANDIDATE (k = 0)"
    elif m["k_from_W3_4a"] != 2:
        m["flag"] = f"PORT-CANDIDATE (k = {m['k_from_W3_4a']}, not the Alpoge pattern)"
    else:
        m["flag"] = None

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump({"paper": "arXiv:2608.00222v1 (papers/2608.00222.pdf)",
           "dimension_3_members": MEMBERS, "higher_dimension_members": HIGHER,
           "controls": [[n, o, note] for n, o, note in RESULTS]},
          open(os.path.join(HERE, "family.json"), "w"), indent=1)

print("\n  PORT-CANDIDATE flags: "
      + str([(m["name"], m["flag"]) for m in MEMBERS if m["flag"]] or "none"))
print("\n" + "=" * 78)
npass = sum(1 for _, o, _ in RESULTS if o)
print(f"    {npass}/{len(RESULTS)} checks passed")
print("=" * 78)
sys.exit(0 if npass == len(RESULTS) else 1)
