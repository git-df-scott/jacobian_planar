import sys, subprocess, json, time; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
def integ(expr):  # antiderivative in t with zero constant
    return sp.integrate(expr, t)
a3 = t**3 - 3*t
a4 = t**4 - 2*t**2
a5 = t**5 - R(25,3)*t**3 + 20*t
lib = [
 ('c34_s2',    [(a3, integ((t**2-1)*(t-2)))]),
 ('c34_s5',    [(a3, integ((t**2-1)*(t-5)))]),
 ('c35_a',     [(a3, integ((t**2-1)*(t**2+t/2+R(1,3))))]),
 ('c35_b',     [(a3, integ((t**2-1)*(t**2+2)))]),
 ('c35_c',     [(a3, integ((t**2-1)*(t**2-2)))]),
 ('c35_d',     [(a3, integ((t**2-1)*(t**2+t-1)))]),
 ('c35_dbl',   [(a3, integ((t-1)**2*(t+1)*(t-R(1,3))))]),
 ('c35_25cusp',[(a3, integ((t-1)**3*(t-R(1,3))))]),
 ('c36_a',     [(a3, integ((t**2-1)*(t**3+t/2+R(1,3))))]),
 ('c36_b',     [(a3, integ((t**2-1)*(t-2)*(t**2+1)))]),
 ('c34_1cusp', [(a3, integ((t-1)*(t**2+t/2+R(1,3))))]),
 ('c45_a',     [(a4, integ(t*(t**2-1)*(t-R(1,3))))]),
 ('c45_b',     [(a4, integ(t*(t**2-1)*(t-2)))]),
 ('c45_2cusp', [(a4, integ(t*(t-1)*(t-R(1,3))*(t+R(5,2))))]),
 ('c46_a',     [(a4, integ(t*(t**2-1)*(t**2+t/2+R(1,3))))]),
 ('c33cusp_a', [(t**3, t**4 + t**2/2)]),
 ('c35_34cusp',[(t**3, t**5 + t**4)]),
 ('c37',       [(t**3, t**7 + t**5 + t**4)]),
 ('c27',       [(t**2, t**3*(t**2-1)*(t**2-4))]),
 ('c27_tac',   [(t**2, t**3*(t**2-1)**2)]),
 ('c27_25',    [(t**2, t**5*(t**2-1))]),
 ('cc_line_gen',  [(t**2, t**3), (t, t + 1)]),
 ('cc_line_cusp', [(t**2, t**3), (t, R(1,2)*t)]),
 ('cc_line_tan0', [(t**2, t**3), (t, 0*t + 0)]),
 ('cc_line_tan1', [(t**2, t**3), (1 + 2*t, 1 + 3*t)]),
 ('cc_cc_a',   [(t**2, t**3), (t**2 + 1, t**3)]),
 ('cc_cc_b',   [(t**2, t**3), (t**2, t**3 + 1)]),
 ('cc_cc_c',   [(t**2, t**3), (-t**2 + 1, t**3)]),
 ('cc_cc_d',   [(t**2, t**3), ((t+1)**2, t**3)]),
 ('cc_cc_T',   [(t**2, t**3), (t**3, t**2)]),
 ('cc_cc_T2',  [(t**2, t**3), (t**3 + 1, t**2)]),
 ('cc_par_a',  [(t**2, t**3), (t, t**2 + 1)]),
 ('cc_par_b',  [(t**2, t**3), (t, t**2 - R(1,2))]),
 ('cc_par_c',  [(t**2, t**3), (t + 1, t**2)]),
 ('c34_line',  [(a3, integ((t**2-1)*(t-2))), (t, t/3 + 1)]),
 ('cc_2lines', [(t**2, t**3), (t, t + 1), (t, -t + 2)]),
 ('cc_line_line_cusp', [(t**2, t**3), (t, t/2), (t, -t/3)]),
]
names = sys.argv[1:] 
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
