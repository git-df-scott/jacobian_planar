import sys; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
from runcurve import run
R = sp.Rational
a3 = t**3 - 3*t
I = lambda e: sp.integrate(e, t)
def nm(x): return str(x).replace('/','o').replace('-','m')
def b_cusp_conditions(beta, kind, extra_vals):
    """b of degree beta with cusp at -1 (b'(-1)=0) and a (2,5) or (2,7) cusp at 1 for a = t^3-3t."""
    cs = sp.symbols('c1:%d' % (beta + 1))
    b = sum(c * t**(i+1) for i, c in enumerate(cs))
    s_ = sp.symbols('s_')
    bs = sp.expand(b.subs(t, 1 + s_) - b.subs(t, 1))
    beta_ = [bs.coeff(s_, i) for i in range(beta + 1)]
    eqs = [sp.diff(b, t).subs(t, -1), beta_[1], beta_[3] - beta_[2]/3]
    if kind == 27:
        eqs.append(beta_[5] - 2*beta_[4]/3)
    sol = list(sp.linsolve(eqs, cs))[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    vals = dict(zip(free, extra_vals))
    bb = sp.expand(b.subs(dict(zip(cs, sol))).subs(vals))
    return bb
lib = []
for i, vals in enumerate([(1, 2, 3), (2, -1, R(1,2)), (-3, 1, 5), (R(1,3), R(2,7), -2)]):
    bb = b_cusp_conditions(6, 27, vals)
    lib.append(('c36_27_%d' % i, [(a3, bb)]))
for i, vals in enumerate([(1, 2, 3, 1), (2, -1, R(1,2), -2), (-3, 1, 5, R(1,3))]):
    bb = b_cusp_conditions(7, 27, vals)
    lib.append(('c37_27_%d' % i, [(a3, bb)]))
lib.append(('c36_b_D12', [(a3, I((t**2-1)*(t-2)*(t**2+1)))]))
names = sys.argv[1:]
for name, comps in lib:
    if names and name not in names: continue
    Dmax = 12 if name.endswith("D12") else 10
    try:
        run(name, comps, Dmin=4, Dmax=Dmax)
    except Exception as ex:
        print(name, 'ERROR', repr(ex)[:300])
    sys.stdout.flush()
