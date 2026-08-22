#!/usr/bin/env python3
"""Export the w-cascade's level-18 block as a small standalone solver target.

The descent: level 20 = the eighth-power family (3 parameters tau, c0, c1);
level 19 consistent with a 10-dimensional kernel; level 18 then imposes explicit
conditions on those 10 carried parameters.

Those conditions are NECESSARY for the pentagon, so a verdict on them is a
verdict on the pentagon in one direction:  **EMPTY here => pentagon EMPTY**.
NONEMPTY here is not a counterexample -- it hands back a reduced family.

Saturation: tau, c0, c1 are all nonzero (p_16_8 = c0 != 0, p_8_0 = c0 tau^8 != 0,
q_24_12 = c1 != 0), so each gets a Rabinowitsch row.
"""
import io, contextlib, sympy as sp
src = open('session43/pentagon/wcascade.py').read(); g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, g)
x, y, level = g['x'], g['y'], g['level']
t, tau, c0, c1 = sp.symbols('t tau c0 c1')

sub = {}
A  = sp.Poly(sp.expand(c0*(t-tau)**8), t)
Qh = sp.Poly(sp.expand(c1*(t-tau)**12), t)
for i in range(9):  sub[sp.Symbol(f'p_{i+8}_{i}')]  = A.coeff_monomial(t**i)
for k in range(13): sub[sp.Symbol(f'q_{12+k}_{k}')] = Qh.coeff_monomial(t**k)
assert sp.expand(level(20).subs(sub)) == 0, "level 20 control FAILED"
print("level 20 control: PASS", flush=True)

e19 = sp.expand(level(19).subs(sub))
eqs19 = sp.Poly(e19, x, y).coeffs()
new19 = sorted(set().union(*[c.free_symbols for c in eqs19]) - {tau, c0, c1}, key=str)
M, v = sp.linear_eq_to_matrix(eqs19, new19)
assert M.rank() == M.row_join(v).rank(), "level 19 inconsistent"
s19 = sp.solve(eqs19, new19, dict=True)[0]
sub.update({k: sp.expand(val) for k, val in s19.items()})
free = sorted(set(new19) - set(s19), key=str)
print(f"level 19: solved {len(s19)} of {len(new19)}, carried free: {len(free)}", flush=True)
assert sp.expand(level(19).subs(sub)) == 0, "level 19 re-check FAILED"
print("level 19 re-check: PASS", flush=True)

e18 = sp.expand(level(18).subs(sub))
eqs18 = sp.Poly(e18, x, y).coeffs()
new18 = sorted(set().union(*[c.free_symbols for c in eqs18]) - {tau, c0, c1} - set(free), key=str)
M, v = sp.linear_eq_to_matrix(eqs18, new18)
conds = []
for n in M.T.nullspace():
    val = sp.simplify(sp.expand((n.T*v)[0, 0]))
    if val != 0:
        num, _ = sp.fraction(sp.together(val))
        num = sp.expand(num)
        for f, m in sp.factor_list(num)[1]:
            f = sp.expand(f)
            if not f.is_number and f not in (tau, c0, c1) and f not in conds:
                conds.append(f)
print(f"level 18: {len(eqs18)} eqs, {len(new18)} new, rank {M.rank()}, "
      f"{len(conds)} residual conditions on {len(free)} carried params", flush=True)

vars_ = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
print("unknowns:", [str(v_) for v_ in vars_], flush=True)
p = 1000003
def to_ms(e):
    e = sp.expand(e)
    out = []
    for mono, co in sp.Poly(e, *vars_).terms():
        s = str(int(co) % p)
        for vv, ee in zip(vars_, mono):
            if ee: s += f'*{vv}' + (f'^{ee}' if ee > 1 else '')
        out.append(s)
    return '+'.join(out) if out else '0'
sat = ['sz_tau', 'sz_c0', 'sz_c1']
allv = [str(v_) for v_ in vars_] + sat
lines = [to_ms(c) for c in conds]
lines += [f'sz_tau*tau-1', f'sz_c0*c0-1', f'sz_c1*c1-1']
body = ',\n'.join(lines)
open('/tmp/red/level18.ms', 'w').write(','.join(allv) + f'\n{p}\n' + body + '\n')
print(f"/tmp/red/level18.ms: {len(allv)} vars, {len(lines)} eqs, "
      f"parens: {'(' in body}", flush=True)
