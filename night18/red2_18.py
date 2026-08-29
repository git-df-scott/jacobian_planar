"""night18 -- deg h = 2 at the carrier deg Q <= 12 = 4 deg P.

Only the translation TAU_a is carrier-preserving for deg h = 2, so the family is
reduced to the slice a = 0; alpha is set to 0 as well, which only removes an
additive constant from P and leaves [P, Q] untouched.  Free parameters that
remain: gamma, h0, h1, h2.
"""
import json, os, sys
import sympy as sp
import fam18, cover18
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for D in (6, 12):
    Fm = fam18.family(2)
    sub = {Fm['a']: sp.Integer(0), Fm['al']: sp.Integer(0)}
    c = cover18.cert(Fm, sub, D)
    c.pop('_dens', None); c.pop('_lamraw', None)
    out[str(D)] = c
    print("  deg h=2  slice {a=0, alpha=0}  D=%-3d n=%-4d rows=%-4d %-22s |supp|=%s dens=%s"
          % (D, c.get('n_unknowns'), c.get('n_equations'), c['verdict'],
             c.get('lambda_support'), [d[0] for d in c.get('denominator_factors', [])]))
    sys.stdout.flush()
    json.dump(out, open(os.path.join(HERE, 'red2_18.json'), 'w'), indent=1)
print("done")
