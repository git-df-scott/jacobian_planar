"""night18 -- THE SYMBOLIC OBSTRUCTION over the whole deg g = 1 family.

Stage 2: build M(params) q = e_{(0,0)} with the parameters kept symbolic and
solve for a certificate lambda(params) over Q(params).
Stage 3: read off the DEGENERATION LOCUS -- the vanishing of the denominators
of lambda (and of the pivots that produced it) -- decompose it, and decide the
mate system EXACTLY over Q at rational points of every component.
"""
import json, os, random, sys, time
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk, fam18, mate18, members18
import pk17, mate17, certs17, res17

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}


def stage2(H, Ds):
    Fm = fam18.family(H)
    gens = Fm['free']
    rec = {"deg_h": H, "n_params": len(gens), "params": [str(s) for s in gens],
           "deg_P": spk.tdeg(Fm['P']), "P": spk.to_str(Fm['P']), "carriers": []}
    for D in Ds:
        t0 = time.time()
        S = mate18.carrier(D)
        cols, rows = mate18.build(Fm['P'], S)
        rk, _ = mate18.rank_symbolic(cols, rows, gens)
        lam, info = mate18.solve_lambda(cols, rows, gens)
        row = {"deg_Q_bound": D, "n_unknowns": len(S), "n_equations": len(rows),
               "rank_symbolic": rk, "cokernel_dim": len(rows) - rk,
               "kernel_dim": len(S) - rk}
        if lam is None:
            q, qi = mate18.solve_mate(cols, rows, S, gens)
            row["verdict"] = "MATE_over_Q(params)" if q is not None else "NOT_CERTIFIED"
            if q is not None:
                res = spk.psub(spk.bracket(Fm['P'], q), {(0, 0): sp.Integer(1)})
                row["bracket_minus_one_terms"] = len(res)
                row["Q"] = spk.to_str(q)
        else:
            good, msg = mate18.verify_lambda(lam, cols)
            dens = mate18.denominators(lam)
            row.update(verdict="EMPTY_over_Q(params)" if good else "NOT_CERTIFIED",
                       lambda_verified=bool(good), verification=msg,
                       lambda_support=len(lam),
                       lam={"%d,%d" % k: sp.sstr(v) for k, v in sorted(lam.items())},
                       denominator_factors=[[sp.sstr(f), int(m)] for f, m in dens])
            row["_lam"] = lam
            row["_dens"] = [f for f, m in dens]
        row["secs"] = round(time.time() - t0, 1)
        rec["carriers"].append(row)
        print("  deg h=%d  D=%-3d n=%-4d rows=%-4d rank=%-4d  %-22s |supp lambda|=%s  "
              "denominators=%s  (%.1fs)"
              % (H, D, len(S), len(rows), rk, row["verdict"],
                 row.get("lambda_support"),
                 [d[0] for d in row.get("denominator_factors", [])], row["secs"]))
        sys.stdout.flush()
    return Fm, rec


def rational_points_on(f, gens, Fm, n=4, seed=7):
    """rational points of V(f) inside the parameter space."""
    rnd = random.Random(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 4000:
        tries += 1
        v = {g: sp.Rational(rnd.randint(-4, 4)) for g in gens}
        # solve f = 0 for one variable, cycling through them
        var = gens[tries % len(gens)]
        if var not in f.free_symbols:
            continue
        sub = {g: v[g] for g in gens if g is not var}
        try:
            sols = sp.solve(sp.Eq(f.subs(sub), 0), var)
        except Exception:
            continue
        for s in sols:
            s = sp.nsimplify(s)
            if not s.is_rational:
                continue
            w = dict(sub); w[var] = sp.Rational(s)
            if sp.expand(f.subs(w)) != 0:
                continue
            if w in [p for p, _ in pts]:
                continue
            gam = w[Fm['gam']]
            ha = sp.expand(Fm['ha'].subs(w))
            pts.append((w, {"gamma_nonzero": bool(gam != 0), "h_at_a_nonzero": bool(ha != 0),
                            "in_family": bool(gam != 0 and ha != 0)}))
            break
    return pts


def decide_exact(Ps, Ds):
    """decide the mate system EXACTLY over Q at a specialised P."""
    Ppk = spk.to_pk(Ps)
    out = []
    for D in Ds:
        o, cols, rows, q = mate17.stage(Ppk, D, verbose=False)
        o.pop('lambda', None)
        r = {"deg_Q_bound": D, "verdict": o['verdict'], "n_unknowns": o.get('n_unknowns'),
             "n_equations": o.get('n_equations'), "rank": o.get('rank_mod_p')}
        if o['verdict'] == 'EMPTY_over_Q':
            # re-solve and re-verify the certificate in THIS lane, symbolically
            c2, r2 = mate18.build(Ps, mate18.carrier(D))
            lam, _i = mate18.solve_lambda(c2, r2, [])
            ok = lam is not None and mate18.verify_lambda(lam, c2)[0]
            r["night18_lambda_verified"] = bool(ok)
            r["night18_lambda_support"] = len(lam) if lam else 0
            r["night18_lambda"] = {"%d,%d" % k: sp.sstr(v)
                                   for k, v in sorted(lam.items())} if lam else None
        elif o['verdict'] == 'MATE_over_Q':
            r["Q"] = pk17.to_str(q)
            r["bracket_minus_one_terms"] = len(pk17.psub(pk17.bracket(Ppk, q), {(0, 0): F(1)}))
        out.append(r)
    return out


def stage3(Fm, rec, Ds):
    gens = Fm['free']
    comps = {}
    for row in rec['carriers']:
        for f in row.get('_dens', []):
            comps.setdefault(sp.sstr(f), f)
    rec['degeneration_locus'] = {
        "ideal_generators": sorted(comps.keys()),
        "note": ("the certificate lambda(params) is a rational object; it is valid "
                 "at every parameter point where none of its denominators vanishes. "
                 "The listed generators are the irreducible factors of those "
                 "denominators, over all carriers tested."),
        "components": []}
    extra = {sp.sstr(sp.expand(Fm['ha'])): sp.expand(Fm['ha'])}
    for key, f in sorted(list(comps.items()) + list(extra.items())):
        comp = {"polynomial": key, "irreducible": True,
                "role": ("denominator of the symbolic certificate"
                         if key in comps else
                         "the family's own unimodularity wall h(a) = 0 (probed, not a"
                         " degeneration of the certificate)"),
                "dimension": len(gens) - 1, "ambient_dimension": len(gens),
                "points": []}
        # is the component inside a family wall?
        comp["inside_wall_gamma_eq_0"] = bool(sp.simplify(f / Fm['gam']).is_polynomial()
                                              and sp.rem(sp.Poly(f, Fm['gam']),
                                                         sp.Poly(Fm['gam'], Fm['gam'])).is_zero) \
            if Fm['gam'] in f.free_symbols else False
        pts = rational_points_on(f, gens, Fm, n=4, seed=11 + len(key))
        for w, flags in pts:
            Ps = spk.subs(Fm['P'], w)
            entry = {"params": {str(g): sp.sstr(w[g]) for g in gens},
                     "gamma_nonzero": flags["gamma_nonzero"],
                     "h_at_a_nonzero": flags["h_at_a_nonzero"],
                     "in_family": flags["in_family"],
                     "P": spk.to_str(Ps), "deg_P": spk.tdeg(Ps)}
            if not flags["gamma_nonzero"]:
                entry["mate"] = [{"verdict": "NOT_A_POINT_OF_THE_FAMILY",
                                  "note": "gamma = 0: k = (h^2 - alpha x - beta)/(4 gamma (x-a))"
                                          " is not defined, and deg g = 1 fails; the component"
                                          " lies outside the parametrisation's domain"}]
                comp["points"].append(entry)
                print("     %-12s %-58s OUTSIDE THE FAMILY (gamma = 0)"
                      % (key[:12], str(entry['params'])[:58]))
                continue
            if flags["in_family"]:
                Ppk = spk.to_pk(Ps)
                u = certs17.unimodular(Ppk)
                entry["bezout"] = u['verdict']
                entry["bezout_residual_terms"] = u['residual_terms']
                entry["sy"] = certs17.sy(Ppk)[0]
                g, h, k = members18.decompose(spk.to_expr(Ps))
                rs = res17.he17(g, h, k)
                entry["residues_all_zero"] = bool(rs['residues_all_zero'])
                entry["genus"] = int(rs['genus'])
            entry["mate"] = decide_exact(Ps, Ds)
            comp["points"].append(entry)
            print("     %-12s %-58s in_family=%s  %s"
                  % (key[:12], str(entry['params'])[:58], entry['in_family'],
                     ";".join("D=%d:%s" % (m['deg_Q_bound'], m['verdict'])
                              for m in entry['mate'])))
            sys.stdout.flush()
        rec['degeneration_locus']['components'].append(comp)
    return rec


if __name__ == "__main__":
    Ds = {1: [3, 6], 2: [3, 6]}
    res = {}
    for H in (1, 2):
        print("=" * 78)
        print("STAGE 2 -- symbolic mate system and certificate, deg h = %d" % H)
        print("=" * 78)
        Fm, rec = stage2(H, Ds[H])
        print("STAGE 3 -- degeneration locus, deg h = %d" % H)
        rec = stage3(Fm, rec, Ds[H])
        for row in rec['carriers']:
            row.pop('_lam', None); row.pop('_dens', None)
        res[str(H)] = rec
        json.dump(res, open(os.path.join(HERE, 'obstruction18.json'), 'w'), indent=1)
    print("done")
