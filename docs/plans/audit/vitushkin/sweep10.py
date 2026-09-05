import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t
I = lambda e: sp.integrate(e, t)
def nm(x): return str(x).replace('/','o').replace('-','m')
lib = []
for r, c in ((2, 1), (R(1,2), -1), (3, R(1,3)), (-2, 2)):
    h = I((t**2-1)*(t-r)) + c
    lib.append(('c37_2525_r%s_c%s' % (nm(r), nm(c)), [(a3, I((t**2-1)*h))]))
names = sys.argv[1:]
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
