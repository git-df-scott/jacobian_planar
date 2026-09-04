import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a = t**3 - 3*t; b = sp.integrate((t**2-1)*((t-1)**2 + 1), t)   # (3,5) with (2,5)-cusp, cusp, node
lib = [
 ('c3525_cc_a', [(a, b), (t**2 - 1, t**3 + 1)]),
 ('c3525_cc_b', [(a, b), (t**2 + 2, t**3)]),
 ('c3525_c3525', [(a, b), (a.subs(t, t+2) + 5, b + 3)]),
 ('c34_cc', [(a, t**4/4 - t**3/9 - t**2/2 + t/3), (t**2 + 1, t**3)]),
 ('cc_c25', [(t**2, t**3), (t**2 + 1, t**5 + t**3)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
