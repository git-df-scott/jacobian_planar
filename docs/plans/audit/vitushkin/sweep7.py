import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t
I = lambda e: sp.integrate(e, t)
def nm(x): return str(x).replace('/','o').replace('-','m')
lib = [
 ('c25cusp_line',    [(t**2, t**5), (t, t/2)]),
 ('c25cusp_tanline', [(t**2, t**5), (t, 0*t)]),
 ('c25cusp_cc',      [(t**2, t**5), (t**2, t**3)]),
 ('c25cusp_cc2',     [(t**2, t**5), (t**2 + 1, t**3)]),
 ('c25cusp_par',     [(t**2, t**5), (t, t**2 - 1)]),
 ('cc_cc_samecusp_b', [(t**2, t**3), (t**2, 2*t**3)]),
 ('c36_25_2nodes_a', [(a3, I((t-1)**2*(t-R(1,2))*(t**2+t+2)))]),   # (2,5)-cusp at 1 only? h=(t-1)(...) not needed: b' = (t-1)^2 k with k'(1)... recompute below
]
# (2,5)-cusp at 1 without a cusp at -1: need b'(1)=0 and beta_3 = beta_2/3, i.e. with b' = (t-1) h: condition derived: h'(1) = h(1)/... do it generally
def b25_only(beta, vals):
    cs = sp.symbols('c1:%d' % (beta + 1))
    b = sum(c * t**(i+1) for i, c in enumerate(cs))
    s_ = sp.symbols('s_')
    bs = sp.expand(b.subs(t, 1 + s_) - b.subs(t, 1))
    be = [bs.coeff(s_, i) for i in range(beta + 1)]
    eqs = [be[1], be[3] - be[2]/3]
    sol = list(sp.linsolve(eqs, cs))[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    return sp.expand(b.subs(dict(zip(cs, sol))).subs(dict(zip(free, vals))))
lib = lib[:-1]
for i, vals in enumerate([(1, 2, 3, -1), (2, -1, R(1,2), 3), (-3, 1, 5, R(1,3))]):
    lib.append(('c35_25only_%d' % i, [(a3, b25_only(5, vals))]))
for i, vals in enumerate([(1, 2, 3, -1, 2), (2, -1, R(1,2), 3, -1)]):
    lib.append(('c36_25only_%d' % i, [(a3, b25_only(6, vals))]))
names = sys.argv[1:]
for name, comps in lib:
    if names and name not in names: continue
    try:
        run(name, comps, Dmin=4, Dmax=10)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
