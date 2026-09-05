import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t; a4 = t**4 - 2*t**2
I = lambda e: sp.integrate(e, t)
lib = [
 ('c45_2cusp', [(a4, I(t*(t-1)*(t-R(1,3))*(t+R(5,2))))]),
 ('c46_a',     [(a4, I(t*(t**2-1)*(t**2+t/2+R(1,3))))]),
 ('c37',       [(t**3, t**7 + t**5 + t**4)]),
 ('c27',       [(t**2, t**3*(t**2-1)*(t**2-4))]),
 ('c27_tac',   [(t**2, t**3*(t**2-1)**2)]),
 ('c27_25',    [(t**2, t**5*(t**2-1))]),
 ('cc_line_gen',  [(t**2, t**3), (t, t + 1)]),
 ('cc_line_cusp', [(t**2, t**3), (t, R(1,2)*t)]),
 ('cc_line_tan1', [(t**2, t**3), (1 + 2*t, 1 + 3*t)]),
 ('cc_line_line_cusp', [(t**2, t**3), (t, t/2), (t, -t/3)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
