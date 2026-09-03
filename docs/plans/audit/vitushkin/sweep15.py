import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
lib = [
 ('cc_cc_a',   [(t**2, t**3), (t**2 + 1, t**3)]),
 ('cc_cc_b',   [(t**2, t**3), (t**2, t**3 + 1)]),
 ('cc_cc_c',   [(t**2, t**3), (-t**2 + 1, t**3)]),
 ('cc_cc_d',   [(t**2, t**3), ((t+1)**2, t**3)]),
 ('c33cusp_a', [(t**3, t**4 + t**2/2)]),
 ('c35_34cusp',[(t**3, t**5 + t**4)]),
]
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
