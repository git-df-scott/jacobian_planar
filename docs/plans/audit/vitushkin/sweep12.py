import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
from mkcurves import cubic_with_rational_cusps_and_pair, b_with_conditions
R = sp.Rational
lib = []
seen = set()
for p, q, t2, r1, r2 in cubic_with_rational_cusps_and_pair():
    a = t**3 + p*t**2 + q*t
    if (p, q) in seen: continue
    seen.add((p, q))
    for beta in (6, 7):
        b = b_with_conditions(a, beta, [r1, r2], [(1, t2)])
        if b is None: continue
        lib.append(('tac3%d_p%d_q%s' % (beta, p, str(q).replace('/', 'o').replace('-', 'm')), [(a, b)]))
        break
    if len(lib) >= 5: break
print('curves:', [n for n, c in lib]); sys.stdout.flush()
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
