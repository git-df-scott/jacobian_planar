"""night18 -- COVERING the family by certificates.

The certificate produced by an rref over Q(params) is valid off the vanishing
locus of its denominators.  That locus is an artefact of the elimination, not
of the mathematics, so this module walks it: on each component it RESTRICTS the
parameters to the component and solves for a NEW symbolic certificate there.
Recursing until every branch either closes (denominators only on the family's
own excluded walls gamma = 0 / h(a) = 0) or hits the depth limit gives a FINITE
COVER of the whole family by symbolic certificates.
"""
import json, os, sys, time
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk, fam18, mate18

HERE = os.path.dirname(os.path.abspath(__file__))


def cert(Fm, sub, D):
    """symbolic certificate for the family restricted by `sub`."""
    P = spk.subs(Fm['P'], sub) if sub else Fm['P']
    gens = sorted({s for v in P.values() for s in sp.sympify(v).free_symbols},
                  key=lambda s: str(s))
    S = mate18.carrier(D)
    cols, rows = mate18.build(P, S)
    lam, info = mate18.solve_lambda(cols, rows, gens)
    if lam is None:
        q, qi = mate18.solve_mate(cols, rows, S, gens)
        if q is None:
            return {"verdict": "NOT_CERTIFIED", "gens": [str(g) for g in gens]}
        res = spk.psub(spk.bracket(P, q), {(0, 0): sp.Integer(1)})
        return {"verdict": "MATE_over_Q(params)", "Q": spk.to_str(q),
                "bracket_minus_one_terms": len(res), "gens": [str(g) for g in gens]}
    good, msg = mate18.verify_lambda(lam, cols)
    dens = mate18.denominators(lam)
    return {"verdict": "EMPTY_over_Q(params)" if good else "NOT_CERTIFIED",
            "lambda_verified": bool(good), "verification": msg,
            "gens": [str(g) for g in gens], "lambda_support": len(lam),
            "lambda": {"%d,%d" % k: sp.sstr(v) for k, v in sorted(lam.items())},
            "denominator_factors": [[sp.sstr(f), int(m)] for f, m in dens],
            "_dens": [f for f, m in dens], "_lamraw": lam,
            "n_unknowns": len(S), "n_equations": len(rows)}


def walk(H, D, maxdepth=4):
    Fm = fam18.family(H)
    walls = {str(Fm['gam'])}
    ha = sp.expand(Fm['ha'])
    charts, queue = [], [({}, 0, "generic")]
    seen = set()
    while queue:
        sub, depth, label = queue.pop(0)
        key = sp.sstr(sorted(((str(k), sp.sstr(v)) for k, v in sub.items())))
        if key in seen:
            continue
        seen.add(key)
        t0 = time.time()
        c = cert(Fm, sub, D)
        c.update(chart=label, depth=depth,
                 restriction={str(k): sp.sstr(v) for k, v in sub.items()},
                 _restr=dict(sub),
                 secs=round(time.time() - t0, 1))
        charts.append(c)
        print("  [d=%d] %-34s %-22s denominators=%s  (%.1fs)"
              % (depth, label, c['verdict'],
                 [d[0] for d in c.get('denominator_factors', [])], c['secs']))
        sys.stdout.flush()
        if c['verdict'] != "EMPTY_over_Q(params)" or depth >= maxdepth:
            continue
        for f in c.get('_dens', []):
            fs = sp.sstr(f)
            if str(f) in walls:
                c.setdefault('closed_on_wall', []).append(fs)
                continue                     # gamma = 0 leaves the stratum
            if sp.simplify(f - ha) == 0 or sp.simplify(f + ha) == 0:
                c.setdefault('closed_on_wall', []).append(fs)
                continue                     # h(a) = 0 is the non-unimodular wall
            done = False
            for v in sorted(f.free_symbols, key=lambda s: str(s)):
                if sp.degree(sp.Poly(f, v)) == 1:
                    sol = sp.solve(sp.Eq(f, 0), v)
                    if not sol:
                        continue
                    nsub = {k: sp.expand(w.subs({v: sol[0]})) for k, w in sub.items()}
                    nsub[v] = sp.expand(sol[0])
                    queue.append((nsub, depth + 1, label + " & {%s=0}" % fs))
                    done = True
                    break
            if not done:
                c.setdefault('unresolved_components', []).append(fs)
    return charts


if __name__ == "__main__":
    out = {}
    for H in (1, 2):
        for D in (3, 6):
            print("=" * 78)
            print("COVER  deg h = %d,  carrier deg Q <= %d" % (H, D))
            print("=" * 78)
            ch = walk(H, D)
            for c in ch:
                c.pop('_dens', None); c.pop('_lamraw', None); c.pop('_restr', None)
            out["H%d_D%d" % (H, D)] = ch
            json.dump(out, open(os.path.join(HERE, 'cover18.json'), 'w'), indent=1)
    print("done")
