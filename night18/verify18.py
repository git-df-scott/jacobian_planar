"""night18 -- the symbolic certificate, SPECIALISED and re-verified over Q.

One certificate is supposed to cover infinitely many P at once.  This checks it
literally: draw random rational parameter points of the family, substitute them
into the symbolic lambda of the relevant chart, and verify lambda^T M = 0 on
every column and lambda^T e = 1 EXACTLY over Q at that point.
"""
import json, os, random, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk, fam18, mate18, cover18

HERE = os.path.dirname(os.path.abspath(__file__))


def run(H, D, npts=60, seed=99):
    Fm = fam18.family(H)
    charts = []          # (name, restriction dict, lambda) from the full cover walk
    for c in cover18.walk(H, D):
        if c['verdict'] != "EMPTY_over_Q(params)":
            continue
        sub = {}
        for k, w in c.get('_restr', {}).items():
            sub[k] = w
        charts.append((c['chart'], sub, c.get('_lamraw')))
    rnd = random.Random(seed)
    rows, ok = [], True
    for _ in range(npts):
        v = {Fm['gam']: sp.Rational(rnd.randint(-6, 6) or 1),
             Fm['a']: sp.Rational(rnd.choice([0, 0] + list(range(-5, 6)))),
             Fm['al']: sp.Rational(rnd.randint(-6, 6))}
        for s in Fm['hs']:
            v[s] = sp.Rational(rnd.randint(-5, 5))
        Ps = spk.subs(Fm['P'], v)
        cols, rws = mate18.build(Ps, mate18.carrier(D))
        lam, name = None, None
        for cname, sub, cl in charts:
            if any(sp.expand(v[k] - sp.sympify(w).subs(v)) != 0 for k, w in sub.items()):
                continue
            trial, bad = {}, False
            for m, e in cl.items():
                z = sp.cancel(sp.sympify(e).subs(v))
                if z.has(sp.zoo) or z.has(sp.nan):
                    bad = True; break
                trial[m] = sp.Rational(z)
            if not bad:
                lam, name = trial, cname
                break
        if lam is None:
            rows.append({"chart": None, "params": {str(k): sp.sstr(w) for k, w in v.items()},
                         "specialises": False}); ok = False; continue
        good, msg = mate18.verify_lambda(lam, cols)
        ha = sp.expand(Fm['ha'].subs(v))
        rows.append({"chart": name, "params": {str(k): sp.sstr(w) for k, w in v.items()},
                     "h_at_a": sp.sstr(ha), "unimodular_member": bool(ha != 0),
                     "specialises": True, "lambda_verified_over_Q": bool(good)})
        ok &= good
    n_gen = sum(1 for r in rows if r['chart'] == 'generic')
    from collections import Counter
    used = Counter(r['chart'] for r in rows)
    print("  deg h=%d  D=%-3d  %d points; charts used %s; certificate specialises and "
          "verifies over Q at %d / %d"
          % (H, D, len(rows), dict(used),
             sum(1 for r in rows if r.get('lambda_verified_over_Q')), len(rows)))
    return {"deg_h": H, "deg_Q_bound": D, "n_points": len(rows),
            "charts_used": {str(k): n for k, n in used.items()},
            "all_verified": bool(ok), "points": rows}


if __name__ == "__main__":
    out = {}
    print("SPECIALISATION SWEEP -- one symbolic certificate, many P")
    for H in (1, 2):
        for D in (3, 6):
            out["H%d_D%d" % (H, D)] = run(H, D)
            json.dump(out, open(os.path.join(HERE, 'verify18.json'), 'w'), indent=1)
    print("ALL VERIFIED" if all(v['all_verified'] for v in out.values()) else "*** FAILED ***")
