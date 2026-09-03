import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t
I = lambda e: sp.integrate(e, t)
lib = []
for s_ in (2, 3, R(1,2), -2, 5):
    for q in (1, 2, R(1,3), -R(1,2)):
        lib.append(('c36_s%s_q%s' % (str(s_).replace('/','o').replace('-','m'), str(q).replace('/','o').replace('-','m')), [(a3, I((t**2-1)*(t-s_)*(t**2+q)))]))
lib.append(('c36_3lin_a', [(a3, I((t**2-1)*(t-2)*(t-3)*(t+4)))]))
lib.append(('c36_3lin_b', [(a3, I((t**2-1)*(t-2)*(t-R(1,2))*(t+R(3,2))))]))
lib.append(('c37_a', [(a3, I((t**2-1)*(t-2)*(t**2+1)*(t+3)))]))
lib.append(('c37_b', [(a3, I((t**2-1)*(t**2+1)*(t**2+2)))]))
lib.append(('c38_a', [(a3, I((t**2-1)*(t-2)*(t**2+1)*(t**2+3)))]))
names = sys.argv[1:]
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
