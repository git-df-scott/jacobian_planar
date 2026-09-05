import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
lib = [
 ('cc_cc_samecusp_c', [(t**2, t**3), (t**2 + t**3, t**3)]),
 ('cc_cc_T',   [(t**2, t**3), (t**3, t**2)]),
 ('cc_cc_T2',  [(t**2, t**3), (t**3 + 1, t**2)]),
 ('cc_par_a',  [(t**2, t**3), (t, t**2 + 1)]),
 ('cc_par_b',  [(t**2, t**3), (t, t**2 - R(1,2))]),
 ('cc_par_c',  [(t**2, t**3), (t + 1, t**2)]),
 ('c34_line',  [(t**3 - 3*t, t**4/4 - 2*t**3/3 - t**2/2 + 2*t), (t, t/3 + 1)]),
 ('c36b_line', [(t**3 - 3*t, sp.integrate((t**2-1)*(t-2)*(t**2+1), t)), (t, t/3 + 1)]),
 ('c36b_line_node', [(t**3 - 3*t, sp.integrate((t**2-1)*(t-2)*(t**2+1), t)), (t, 0*t + R(11,8))]),
 ('cc_2lines', [(t**2, t**3), (t, t + 1), (t, -t + 2)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
