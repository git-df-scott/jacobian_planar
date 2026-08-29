"""night18 -- the family must REPRODUCE night17's recorded instances, and its
random members must pass night17's own certificates (read-only imports).
"""
import json, os, random, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk
import fam18
import pk17, certs17, res17

X, Y = spk.X, spk.Y


def decompose(Pexpr):
    """P -> (g, h, k) with P = g y^2 + h y + k."""
    p = sp.Poly(sp.expand(Pexpr), Y)
    d = {int(m[0]): c for m, c in zip(p.monoms(), p.coeffs())}
    return (sp.expand(d.get(2, 0)), sp.expand(d.get(1, 0)), sp.expand(d.get(0, 0)))


def recover_params(Pexpr):
    """recover (gamma, a, alpha, h coefficients) of a deg g = 1 member."""
    g, h, k = decompose(Pexpr)
    gp = sp.Poly(g, X)
    if gp.degree() != 1:
        return None
    gam = gp.coeff_monomial(X)
    a = sp.cancel(-gp.coeff_monomial(1) / gam)
    Delta = sp.expand(h**2 - 4 * g * k)
    dp = sp.Poly(Delta, X)
    if dp.degree() > 1:
        return None
    al = dp.coeff_monomial(X)
    beta = dp.coeff_monomial(1)
    hp = sp.Poly(h, X)
    H = hp.degree()
    hc = [hp.coeff_monomial(X**i) if i else hp.coeff_monomial(1) for i in range(H + 1)]
    ha = sum(hc[i] * a**i for i in range(H + 1))
    return dict(H=H, gam=gam, a=a, al=al, beta=beta, hs=hc,
                beta_ok=(sp.expand(beta - (ha**2 - al * a)) == 0), ha=sp.expand(ha))


def rebuild(pr):
    F = fam18.family(pr['H'])
    sub = {F['gam']: pr['gam'], F['a']: pr['a'], F['al']: pr['al']}
    for i, s in enumerate(F['hs']):
        sub[s] = pr['hs'][i]
    return spk.subs(F['P'], sub)


def main():
    rec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      '..', 'night17', 'records17.json')))['records']
    out = {"night17_instances": [], "random_members": []}
    print("=" * 78)
    print("FAMILY vs night17: every recorded HE deg g = 1 instance must be a member")
    print("=" * 78)
    for r in rec:
        if not r['support'].startswith('H'):
            continue
        Pe = sp.sympify(r['P'].replace('^', '**'))
        pr = recover_params(Pe)
        row = {"support": r['support'], "hash": r['hash'], "P": r['P']}
        if pr is None:
            row["member"] = False
            row["reason"] = "deg g != 1 (stratum deg g = 0 or >= 2)"
        else:
            Pb = rebuild(pr)
            same = (spk.psub(Pb, spk.from_expr(Pe)) == {})
            row.update(member=bool(same), deg_h=pr['H'],
                       gamma=sp.sstr(pr['gam']), a=sp.sstr(pr['a']),
                       alpha=sp.sstr(pr['al']), h=[sp.sstr(c) for c in pr['hs']],
                       h_at_a=sp.sstr(pr['ha']),
                       beta_equals_ha2_minus_alpha_a=bool(pr['beta_ok']))
        out["night17_instances"].append(row)
        print("  %-4s %-14s %s" % (r['support'], r['hash'],
              ("MEMBER   deg h=%d gamma=%s a=%s alpha=%s h(a)=%s" %
               (row.get('deg_h'), row.get('gamma'), row.get('a'), row.get('alpha'),
                row.get('h_at_a'))) if row.get('member') else
              ("not on this stratum: " + row.get('reason', 'rebuild mismatch'))))

    print()
    print("=" * 78)
    print("RANDOM MEMBERS: night17's own certificates on 5 random parameter points")
    print("=" * 78)
    random.seed(1807)
    pts = []
    for H in (1, 1, 2, 2, 3):
        F = fam18.family(H)
        while True:
            v = {F['gam']: sp.Rational(random.choice([1, 2, -1, 3, -2])),
                 F['a']: sp.Rational(random.randint(-3, 3)),
                 F['al']: sp.Rational(random.randint(-4, 4))}
            for s in F['hs']:
                v[s] = sp.Rational(random.randint(-3, 3))
            ha = F['ha'].subs(v)
            if ha != 0:
                break
        pts.append((H, F, v))
    for H, F, v in pts:
        Ps = spk.subs(F['P'], v)
        Ppk = spk.to_pk(Ps)
        uni = certs17.unimodular(Ppk)
        syv, _ = certs17.sy(Ppk)
        g, h, k = decompose(spk.to_expr(Ps))
        rs = res17.he17(g, h, k)
        row = {"deg_h": H, "params": {str(s): sp.sstr(v[s]) for s in F['free']},
               "P": spk.to_str(Ps), "deg_P": spk.tdeg(Ps),
               "bezout": uni['verdict'], "bezout_residual_terms": uni['residual_terms'],
               "bezout_method": uni['method'], "sy": syv,
               "deg_Delta_c": int(rs['deg_Delta_c']), "genus": int(rs['genus']),
               "residues_all_zero": bool(rs['residues_all_zero'])}
        out["random_members"].append(row)
        print("  deg h=%d %-46s uni=%-22s SY=%-15s res0=%s genus=%d"
              % (H, row['params'], row['bezout'], row['sy'],
                 row['residues_all_zero'], row['genus']))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'members18.json'), 'w'), indent=1)
    ok = all(r.get('member') for r in out['night17_instances']
             if r['support'] in ('H3', 'H4', 'H5', 'H6', 'H7', 'H8'))
    ok &= all(r['bezout'] == 'UNIMODULAR_CERTIFIED' and r['sy'] == 'NON_COORDINATE'
              and r['residues_all_zero'] for r in out['random_members'])
    print("\nCROSS-CHECK %s" % ("PASS" if ok else "*** FAILED ***"))


if __name__ == "__main__":
    main()
