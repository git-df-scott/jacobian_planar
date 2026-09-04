import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a = t**3 - 3*t; b = sp.integrate((t**2-1)*((t-1)**2 + 1), t)   # (3,5): (2,5)-cusp at t=1, cusp at t=-1, node
P25 = (a.subs(t, 1), b.subs(t, 1)); P3 = (a.subs(t, -1), b.subs(t, -1))
lam25 = R(1,3)   # tangent slope at the (2,5)-cusp
lam3 = sp.limit(sp.diff(b, t)/sp.diff(a, t), t, -1)
def line(pt, lam): return (t, pt[1] + lam*(t - pt[0]))
lib = [
 ('c3525_line25_tan',  [(a, b), line(P25, lam25)]),
 ('c3525_line25_gen',  [(a, b), line(P25, 2)]),
 ('c3525_line3_tan',   [(a, b), line(P3, lam3)]),
 ('c3525_line3_gen',   [(a, b), line(P3, -1)]),
 ('c3525_line_gen',    [(a, b), (t, t + 5)]),
 ('c3525_2lines_cusps',[(a, b), line(P25, 2), line(P3, -1)]),
]
print('lines', [(n, str(c[1])) for n, c in lib]); sys.stdout.flush()
for name, comps in lib:
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
