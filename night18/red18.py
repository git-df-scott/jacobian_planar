"""night18 -- the carrier deg Q <= 4 deg P = 12 layer, via CARRIER-PRESERVING moves.

Two substitutions act on the family without changing the carrier
{ x^i y^j : i + j <= D } (both send monomials of degree <= D to polynomials of
degree <= D, and both have Jacobian 1):

    TAU_a : (x, y) -> (x + a, y)                      (translation)
    SIG_s : (x, y) -> (x, y - s),  s a CONSTANT       (degree-0 shear)

Adding a constant to P also leaves [P, Q] unchanged.  By FAMILY.md section 5,
for deg h = 1

    P( x + a,  y - h1/(2 gamma) )  =  gamma x y^2 + h(a) y  -  alpha/(4 gamma),

so EVERY member of the deg h = 1 family is carried, by carrier-preserving
Jacobian-1 moves and a constant shift, onto the TWO-parameter slice

    R(gamma, c) = gamma * x * y^2 + c * y .

Q -> Q o (TAU_a . SIG_s) is then a linear BIJECTION of the carrier space that
matches the two mate systems, so a certificate on R at carrier D is a
certificate for every member of the family at carrier D.  For deg h = 2 only
TAU_a is carrier-preserving, so the reduction there is to the slice a = 0
(and alpha = 0, which only removes an additive constant).
"""
import json, os, sys, time
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk, fam18, mate18

X, Y = spk.X, spk.Y
HERE = os.path.dirname(os.path.abspath(__file__))


def cert_on(P, gens, D):
    S = mate18.carrier(D)
    cols, rows = mate18.build(P, S)
    t0 = time.time()
    lam, info = mate18.solve_lambda(cols, rows, gens)
    if lam is None:
        q, qi = mate18.solve_mate(cols, rows, S, gens)
        return {"verdict": "MATE_over_Q(params)" if q is not None else "NOT_CERTIFIED",
                "Q": spk.to_str(q) if q else None,
                "n_unknowns": len(S), "n_equations": len(rows),
                "secs": round(time.time() - t0, 1)}, None
    good, msg = mate18.verify_lambda(lam, cols)
    dens = mate18.denominators(lam)
    return {"verdict": "EMPTY_over_Q(params)" if good else "NOT_CERTIFIED",
            "lambda_verified": bool(good), "verification": msg,
            "n_unknowns": len(S), "n_equations": len(rows),
            "lambda_support": len(lam),
            "lambda": {"%d,%d" % k: sp.sstr(v) for k, v in sorted(lam.items())},
            "denominator_factors": [[sp.sstr(f), int(m)] for f, m in dens],
            "secs": round(time.time() - t0, 1)}, lam


def transport_check(H, D, lam, npts=6, seed=5):
    """the certificate on the slice, pulled back to random members, over Q."""
    import random
    rnd = random.Random(seed)
    Fm = fam18.family(H)
    rows = []
    for _ in range(npts):
        v = {Fm['gam']: sp.Rational(rnd.choice([1, 2, 3, -1, -2, 5])),
             Fm['a']: sp.Rational(rnd.randint(-3, 3)),
             Fm['al']: sp.Rational(rnd.randint(-4, 4))}
        for s in Fm['hs']:
            v[s] = sp.Rational(rnd.randint(-3, 3))
        if Fm['ha'].subs(v) == 0:
            continue
        a = v[Fm['a']]
        s = sp.Rational(sp.cancel(v[Fm['hs'][1]] / (2 * v[Fm['gam']]))) if H == 1 else sp.Integer(0)
        Pe = spk.to_expr(spk.subs(Fm['P'], v))
        Pm = spk.from_expr(sp.expand(Pe.subs(X, X + a).subs(Y, Y - s)))
        # drop the additive constant; the bracket does not see it
        Pm.pop((0, 0), None)
        gam, c = sp.Symbol('gamma'), sp.Symbol('c')
        lam_s = {m: sp.Rational(sp.cancel(e.subs({gam: v[Fm['gam']],
                                                  c: sp.expand(Fm['ha'].subs(v))})))
                 for m, e in lam.items()}
        cols, rws = mate18.build(Pm, mate18.carrier(D))
        good, msg = mate18.verify_lambda(lam_s, cols)
        rows.append({"params": {str(k): sp.sstr(w) for k, w in v.items()},
                     "translation_a": sp.sstr(a), "shear_s": sp.sstr(s),
                     "moved_P": spk.to_str(Pm),
                     "slice_certificate_verifies_over_Q": bool(good)})
    return rows


if __name__ == "__main__":
    gam, c = sp.symbols('gamma c')
    R = spk.from_expr(gam * X * Y**2 + c * Y)
    out = {"slice": spk.to_str(R), "carriers": {}}
    print("SLICE  R(gamma, c) = gamma x y^2 + c y   (the deg h = 1 family, moved)")
    for D in (3, 6, 12, 18):
        rec, lam = cert_on(R, [gam, c], D)
        out["carriers"][str(D)] = rec
        print("  D=%-3d n=%-4d rows=%-4d %-22s |supp lambda|=%s  denominators=%s  (%.1fs)"
              % (D, rec['n_unknowns'], rec['n_equations'], rec['verdict'],
                 rec.get('lambda_support'), [d[0] for d in rec.get('denominator_factors', [])],
                 rec['secs']))
        sys.stdout.flush()
        if lam is not None and D in (6, 12):
            tr = transport_check(1, D, lam)
            rec['transport_to_family_members'] = tr
            print("     pulled back to %d random deg h = 1 members at D=%d: verified over Q at %d / %d"
                  % (len(tr), D, sum(1 for r in tr if r['slice_certificate_verifies_over_Q']), len(tr)))
        json.dump(out, open(os.path.join(HERE, 'red18.json'), 'w'), indent=1)
    print("done")
