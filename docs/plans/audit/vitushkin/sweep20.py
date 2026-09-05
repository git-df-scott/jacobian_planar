import sys, resource; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
resource.setrlimit(resource.RLIMIT_AS, (6_000_000_000, 6_000_000_000))
from bm import *
from runcurve import run
from mkcusp import build
R = sp.Rational
a = t**3 - 3*t; b = sp.integrate((t**2-1)*((t-1)**2 + 1), t)
P25 = (a.subs(t, 1), b.subs(t, 1))
lib = [
 ('c3525_line25_tan_D6', [(a, b), (t, P25[1] + R(1,3)*(t - P25[0]))]),
 ('c38_75_0_D6', [(a, build(a, 8, [(1, 7), (-1, 5)], (1, 2, 3, 1, 2)))]),
 ('cc_cc_samecusp_c_D6', [(t**2, t**3), (t**2 + t**3, t**3)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=6)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
