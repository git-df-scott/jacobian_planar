import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
from mkcusp import build
R = sp.Rational
a4 = t**4 - 2*t**2
lib = []
for name, cusps in [('c47_555', [(1,5), (-1,5), (0,5)]), ('c47_753', [(1,7), (-1,5), (0,3)]), ('c47_553', [(1,5), (-1,5), (0,3)]), ('c47_733', [(1,7), (-1,3), (0,3)]), ('c47_533', [(1,5), (-1,3), (0,3)])]:
    for trial, vals in enumerate([(1, 2, 3, 5, 7, 11, 13), (2, -1, R(1,2), 3, -2, 5, R(1,3))]):
        b = build(a4, 7, cusps, vals)
        if b is not None:
            lib.append((name + '_%d' % trial, [(a4, b)]))
print('curves', [n for n, c in lib]); sys.stdout.flush()
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
