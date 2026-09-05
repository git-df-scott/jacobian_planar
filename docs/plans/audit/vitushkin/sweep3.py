import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
from mkcurves import cubic_with_rational_cusps_and_pair, b_with_conditions
R = sp.Rational
lib = []
seen = set()
for p, q, t2, r1, r2 in cubic_with_rational_cusps_and_pair():
    a = t**3 + p*t**2 + q*t
    key = (p, q)
    if key in seen: continue
    seen.add(key)
    b = b_with_conditions(a, 7, [r1, r2], [(1, t2)])
    if b is None: continue
    lib.append(('tac37_p%d_q%s' % (p, str(q).replace('/', 'o')), [(a, b)]))
    if len(lib) >= 6: break
# cuspidal cubic + tangent parabola (contact 2) and osculating parabola (contact 3) at t0
t0 = R(1)
u0, v0 = t0**2, t0**3
slope = R(3,2)*t0
for A in (R(1,2), R(2), R(-1)):
    lib.append(('cc_tanpar_A%s' % str(A).replace('/', 'o').replace('-', 'm'), [(t**2, t**3), (t, A*(t - u0)**2 + slope*(t - u0) + v0)]))
# osculating: v = t0^3 + (3t0/2)(u-u0) + (3/(8 t0))(u-u0)^2 for v = u^{3/2}: second derivative of u^{3/2} is (3/4) u^{-1/2}; /2 -> 3/(8 t0)
lib.append(('cc_oscpar', [(t**2, t**3), (t, R(3,8)*(t - u0)**2 + slope*(t - u0) + v0)]))
# two cuspidal cubics meeting only at the shared cusp
lib.append(('cc_cc_samecusp_a', [(t**2, t**3), (2*t**2, t**3)]))
lib.append(('cc_cc_samecusp_b', [(t**2, t**3), (t**2, 2*t**3)]))
lib.append(('cc_cc_samecusp_c', [(t**2, t**3), (t**2 + t**3, t**3)]))
# (2,5)-cusp curve with a line through the cusp and tangent line
lib.append(('c25cusp_line', [(t**2, t**5), (t, t/2)]))
lib.append(('c25cusp_tanline', [(t**2, t**5), (t, 0*t)]))
lib.append(('c25cusp_cc', [(t**2, t**5), (t**2, t**3)]))
lib.append(('cc_line_tan1_line', [(t**2, t**3), (1 + 2*t, 1 + 3*t), (t, -t/2 + 3)]))
names = sys.argv[1:] or [n for n, c in lib if n.startswith('tac37')]
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=8)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
