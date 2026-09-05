import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t
I = lambda e: sp.integrate(e, t)
def nm(x): return str(x).replace('/','o').replace('-','m')
lib = [('c36_b_D10', [(a3, I((t**2-1)*(t-2)*(t**2+1)))])]
# (3,5): b' = (t^2-1)((t-1)^2 + c): (2,5)-cusp at 1, cusp at -1, one node
for c in (1, -1, R(1,2), 3, -R(1,4)):
    lib.append(('c35_25_c%s' % nm(c), [(a3, I((t**2-1)*((t-1)**2 + c)))]))
# (3,6): h = (t-s)(t^2 + 2s - 3)
for s_ in (3, R(5,2), R(3,2), 4, -1, R(1,2)):
    lib.append(('c36_25_s%s' % nm(s_), [(a3, I((t**2-1)*(t-s_)*(t**2 + 2*s_ - 3)))]))
# (3,6): h = ((t-1)^2 + c)(t - r)
for c, r in ((1, 3), (-1, 3), (2, -2), (R(1,2), R(1,3))):
    lib.append(('c36_25b_c%s_r%s' % (nm(c), nm(r)), [(a3, I((t**2-1)*((t-1)**2 + c)*(t - r)))]))
# both cusps of type (2,5): h'(1) = h'(-1) = 0: h = t^3 - 3t + c  (h' = 3(t^2-1))
for c in (1, 5, -2, R(1,2)):
    lib.append(('c37_2525_c%s' % nm(c), [(a3, I((t**2-1)*(t**3 - 3*t + c)))]))
names = sys.argv[1:]
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
