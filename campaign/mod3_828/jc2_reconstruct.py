"""
Plane Jacobian campaign - Session 20
RECONSTRUCT AND TEST A CANDIDATE SOLUTION OF THE (8,28) SYSTEM.

The reduction eliminated 49 of the 72 unknowns.  A point of the reduced variety
is therefore only a candidate: it must be pushed back UP the substitution chain
to recover all 72 coefficients, and then it must survive two independent tests:

  T1  every one of the 92 ORIGINAL equations must vanish at the full point;
  T2  every coefficient that Proposition 4.3 requires NONZERO -- the vertices of
      both Newton polygons -- must actually be nonzero there.

T2 is the one that matters here.  The reduction divides by, and saturates
against, exactly those vertex coefficients, so the reduced variety can perfectly
well contain degenerate points where a vertex coefficient vanishes.  Such a
point satisfies the equations but is NOT a configuration of the shape
Proposition 4.3 describes, and is therefore not a candidate for anything.

This file does the reconstruction and both tests, over GF(p).  A pass here is
still only a mod-p candidate: JC is false in characteristic p, so nothing found
here is a counterexample until it is lifted to characteristic zero and, beyond
that, until the automorphism chain relating Prop 4.3's pairs to a genuine Keller
pair is inverted (see jc2_gghv_system.md section 9).
"""

import sys
import sympy as sp
sys.path.insert(0, '/home/user/jacobian_planar')
import jc2_gghv_system as G
import jc2_gghv_modp as M

P_MOD = 65521          # 65521 = 1 (mod 3), so the sqrt(-3) branches are present


def main():
    case = G.OPEN_CASE_2
    pp, _ = G.lattice_points(case["P"])
    qq, _ = G.lattice_points(case["Q"])
    ps = G.build_symbols("c", pp)
    qs = G.build_symbols("d", qq)
    seqs = G.bracket_system(pp, ps, qq, qs, case["rhs"])
    nz = set(G.nonzero_side_conditions(case["P"], ps)) | \
         set(G.nonzero_side_conditions(case["Q"], qs))
    allsym = list(ps.values()) + list(qs.values())
    idx = {s: i for i, s in enumerate(allsym)}
    names = {i: str(s) for s, i in idx.items()}
    nz_idx = {idx[s] for s in nz}
    norm = [s for s in allsym if str(s) == 'd_2_1'][0]

    def to_poly(expr):
        e = sp.expand(expr.subs(norm, 1))
        out = {}
        for term in sp.Add.make_args(e):
            c, mon = term.as_coeff_Mul()
            d = {}
            for f in sp.Mul.make_args(mon):
                b, ex = f.as_base_exp()
                if b in idx:
                    d[idx[b]] = int(ex)
            out[tuple(sorted(d.items()))] = int(sp.Rational(c)) % P_MOD
        return {m: c for m, c in out.items() if c}

    eqs = [to_poly(e) for e in seqs.values()]
    eqs = [e for e in eqs if e]
    nz_idx.discard(idx[norm])

    print(f"reduction over GF({P_MOD}) ...")
    _res, solved, zeroed, contra = M.reduce_modp(eqs, nz_idx, P_MOD, names,
                                                 verbose=False)
    print(f"  {len(zeroed)} forced to zero, {len(solved)} solved and eliminated")
    assert contra is None

    # ---- the candidate point found for branch r1 -------------------------
    edge = {'d_3_3': 1, 'd_4_5': -2926, 'd_5_7': -5269, 'd_6_9': -14566,
            'd_7_11': 16056, 'd_8_13': 3283, 'd_9_15': 28232}
    rest = ['d_3_4', 'd_4_6', 'd_4_7', 'd_5_8', 'd_5_9', 'd_6_10', 'd_6_11',
            'd_7_12', 'd_7_13', 'd_8_14', 'd_8_15', 'd_9_16', 'd_9_17']
    val = {}
    for nm, v in edge.items():
        val[idx[[s for s in allsym if str(s) == nm][0]]] = v % P_MOD
    for nm in rest:                       # the lex basis forced every one to 0
        val[idx[[s for s in allsym if str(s) == nm][0]]] = 0
    val[idx[norm]] = 1
    for i in zeroed:
        val[i] = 0

    # ---- push back up the substitution chain -----------------------------
    def ev(poly):
        tot = 0
        for m, c in poly.items():
            t = c
            for v_, e_ in m:
                if v_ not in val:
                    return None            # not yet determined
                t = (t * pow(val[v_], e_, P_MOD)) % P_MOD
            tot = (tot + t) % P_MOD
        return tot % P_MOD

    order = list(solved.keys())
    for _ in range(len(order) + 5):
        progress = False
        for i in list(order):
            if i in val:
                continue
            got = ev(solved[i])
            if got is not None:
                val[i] = got
                progress = True
        if not progress:
            break
    undetermined = [names[i] for i in range(len(allsym)) if i not in val]
    print(f"  reconstructed {len(val)}/{len(allsym)} coefficients; "
          f"undetermined: {undetermined if undetermined else 'none'}")

    # ---- T1: all 92 original equations ----------------------------------
    bad = 0
    for e in eqs:
        r = ev(e)
        if r is None or r != 0:
            bad += 1
    print(f"\n  T1  original equations violated: {bad} of {len(eqs)}"
          f"   -> {'PASS' if bad == 0 else 'FAIL'}")

    # ---- T2: required-nonzero vertex coefficients ------------------------
    print("\n  T2  coefficients Proposition 4.3 requires NONZERO:")
    zero_vertices = []
    for s in sorted(nz | {norm}, key=str):
        i = idx[s]
        v = val.get(i, None)
        state = "undetermined" if v is None else ("ZERO  <-- violates Prop 4.3"
                                                  if v == 0 else f"= {v}")
        print(f"        {str(s):10s} {state}")
        if v == 0:
            zero_vertices.append(str(s))
    print(f"\n  T2 verdict: {'PASS' if not zero_vertices else 'FAIL'}"
          f"{'' if not zero_vertices else '  (vanishing: ' + ', '.join(zero_vertices) + ')'}")

    print("\n" + "=" * 68)
    if bad == 0 and not zero_vertices:
        print("CANDIDATE SURVIVES BOTH TESTS over GF(p).")
        print("Still NOT a counterexample: lift to characteristic zero, then")
        print("invert the automorphism chain, then run jc2_bulletproof.py.")
    else:
        print("CANDIDATE REJECTED.  This point of the reduced variety is")
        print("degenerate -- it satisfies the equations but is not a")
        print("configuration of the shape Proposition 4.3 describes.")
        print("It says nothing for or against the (8,28) case.")


if __name__ == '__main__':
    main()
