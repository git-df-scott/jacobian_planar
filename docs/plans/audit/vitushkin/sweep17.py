import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
from mkcusp import build
from mkcurves import cubic_with_rational_cusps_and_pair, b_with_conditions
R = sp.Rational
a3 = t**3 - 3*t
lib = []
for i, vals in enumerate([(1, 2, 3, 1), (2, -1, R(1,2), -2), (-3, 1, 5, R(1,3))]):
    b = build(a3, 7, [(1, 7), (-1, 3)], vals)
    if b is not None: lib.append(('c37_27_%d' % i, [(a3, b)]))
for i, vals in enumerate([(1, 2, 3, 1, 2), (2, -1, R(1,2), -2, 3)]):
    b = build(a3, 8, [(1, 7), (-1, 5)], vals)
    if b is not None: lib.append(('c38_75_%d' % i, [(a3, b)]))
seen = set()
for p, q, t2, r1, r2 in cubic_with_rational_cusps_and_pair():
    a = t**3 + p*t**2 + q*t
    if (p, q) in seen: continue
    seen.add((p, q))
    b = b_with_conditions(a, 7, [r1, r2], [(1, t2)])
    if b is None: continue
    lib.append(('tac37_p%d_q%s' % (p, str(q).replace('/', 'o').replace('-', 'm')), [(a, b)]))
    if len([n for n, c in lib if n.startswith('tac')]) >= 3: break
print('curves:', [n for n, c in lib]); sys.stdout.flush()
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
