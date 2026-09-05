import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
lib = [
 ('c25cusp_line',    [(t**2, t**5), (t, t/2)]),
 ('c25cusp_tanline', [(t**2, t**5), (t, 0*t)]),
 ('c25cusp_cc2',     [(t**2, t**5), (t**2 + 1, t**3)]),
 ('c25cusp_par',     [(t**2, t**5), (t, t**2 - 1)]),
 ('cc_tanpar_A2',    [(t**2, t**3), (t, 2*(t - 1)**2 + R(3,2)*(t - 1) + 1)]),
 ('c25cusp_line_gen', [(t**2, t**5), (t, t + 1)]),
 ('c25cusp_2lines', [(t**2, t**5), (t, t/2), (t, -t/3)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
