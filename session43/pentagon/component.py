#!/usr/bin/env python3
"""Run ONE component of the descent to its endgame conditions.

Both explored charts made exactly one multi-component branch choice, and each
time the run silently took sol[0].  Those siblings are the difference between
"this component is empty" and "the witness is dead", so they get run too.

  CHART=A : g9_8 free (the chart where solves divide by it) -- branches at L9
  CHART=B : g9_8 = 0 imposed up front                       -- branches at L8
  PICK=k  : take component k at the (single) multi-component decision

Everything else is identical to the runs that produced the two EMPTY verdicts.
"""
import sympy as sp, sys, os, pickle
CHART = os.environ.get('CHART', 'A'); PICK = int(os.environ.get('PICK', '0'))
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 6): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (s**2 if L == -2 else 0))
def newsyms(L):
    out = []
    if -1 <= L-12 <= 5: out += [sp.Symbol(f'h{L-12}_{i}') for i in hsup(L-12)]
    if 0 <= L-8 <= 11:  out += [sp.Symbol(f'g{L-8}_{k}') for k in gsup(L-8)]
    return out
S = sp.Symbol
sub = {S('g11_11'):0, S('g9_4'):0, S('g9_5'):0, S('g9_11'):0, S('g10_10'):0,
       S('g9_9'):sp.Rational(3,2)*S('h5_5'), S('g8_4'):0, S('g8_5'):0,
       S('g8_10'):2*S('g9_10'), S('g7_4'):0, S('g7_5'):0,
       S('g9_6'):0, S('g9_7'):0, S('g7_7'):S('g8_7')+sp.Rational(3,2)*S('h3_3'),
       S('g8_6'):0, S('g8_7'):0}
if CHART == 'F': sub = {}
if CHART in ('D','E'):
    # Discharge the inherited g8_6 = g8_7 = 0 by covering its complement.
    # D: g8_6 free, saturated at g8_6 afterwards  -> the g8_6 != 0 region
    # E: g8_6 = 0, g8_7 free, saturated at g8_7   -> g8_6 = 0, g8_7 != 0
    # Together with charts B and C (which cover g8_6 = g8_7 = 0) these leave
    # nothing out.
    del sub[S('g8_6')], sub[S('g8_7')]
    if CHART == 'E': sub[S('g8_6')] = sp.Integer(0)
if CHART == 'F':
    # NOTHING pre-imposed at all.  Only the witness (h_8, h_7, h_6, g_12, tau)
    # and the two gauges are fixed; every condition at every level from 19 down
    # to 8 is extracted by the gate machinery in this run.  This subsumes
    # charts A, B and C and removes the last inherited assumption, namely
    # g8_6 = g8_7 = 0, which had been carried in from a run that made its own
    # branch choices at level 9.
    sub = {}
if   CHART == 'A': sub[S('g7_6')] = sp.Integer(0)   # forced on this chart, imposed early
elif CHART == 'B': sub[S('g9_8')] = sp.Integer(0)
# CHART == 'C': NOTHING extra imposed.  g7_6 and g9_8 both left free, and the
# result is saturated at g9_8 afterwards.  This is the assumption-free form of
# the g9_8 != 0 chart, so that {g9_8 = 0} (chart B) and {g9_8 != 0} (chart C)
# genuinely COVER the g8_6 = g8_7 = 0 component with nothing excluded.
sub = {k: sp.sympify(v) for k, v in sub.items()}
def norm():
    global sub
    for _ in range(12):
        nxt = {k:(sp.cancel(sp.expand(vv.subs(sub))) if hasattr(vv,'subs') else vv)
               for k,vv in sub.items()}
        if nxt == sub: return
        sub = nxt
    raise RuntimeError("sub did not stabilise")
def res(e):
    for _ in range(26):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")
def analyse(L):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    new = [u for u in newsyms(L) if u not in sub]
    if not eqs: return 'sat', [], [], [0,len(new),0]
    if not new: return 'pure', eqs, [], [len(eqs),0,0]
    M, v = sp.linear_eq_to_matrix(eqs, new)
    r = M.rank()
    if r == M.row_join(v).rank(): return 'ok', eqs, [], [len(eqs), len(new), r]
    cs = []
    for n in M.T.nullspace():
        val = sp.cancel(sp.expand((n.T*v)[0,0]))
        if val != 0: cs.append(sp.expand(sp.numer(sp.together(val))))
    return 'gate', eqs, cs, [len(eqs), len(new), r]
NBR = [0]
def close(L):
    st, eqs, cs, info = analyse(L)
    for _r in range(8):
        if st != 'gate': break
        cv = sorted(set().union(*[c_.free_symbols for c_ in cs]), key=str)
        lin = [x for x in cv if all(sp.degree(sp.Poly(c_, x), x) <= 1 for c_ in cs)]
        sol = sp.solve(cs, lin or cv, dict=True)
        if not sol and lin:            # sp.solve([]) on a subset means only
            sol = sp.solve(cs, cv, dict=True)   # 'no solution in THOSE vars'
        if not sol:
            print(f"\nL={L}: sp.solve found no solution; the {len(cs)} gate(s) are:",
                  flush=True)
            for c_ in cs:
                print("   ", sp.factor(c_), flush=True)
                print("      free:", sorted(map(str, c_.free_symbols)), flush=True)
            sys.exit(7)
        k = 0
        if len(sol) > 1:
            NBR[0] += 1
            k = PICK if PICK < len(sol) else None
            print(f"L={L:3d}: {len(sol)} components; taking #{k}", flush=True)
            if k is None:
                print(f"*** PICK={PICK} out of range ({len(sol)} components) ***"); sys.exit(4)
        sub.update({k2: sp.cancel(sp.expand(v)) for k2, v in sol[k].items()}); norm()
        bad = {str(a): str(b) for a, b in sub.items()
               if b.has(sp.nan) or b.has(sp.zoo) or b.has(sp.oo)}
        if bad:
            print(f"\n*** L={L}: substitution produced a degenerate value ***", flush=True)
            for a, b in bad.items(): print(f"    {a} = {b}", flush=True)
            sys.exit(8)
        print(f"L={L:3d}: {len(cs)} gate(s) -> imposed {sorted(map(str,sol[k]))}", flush=True)
        st, eqs, cs, info = analyse(L)
    assert st == 'ok', (L, st, [str(sp.factor(c)) for c in cs])
    new = [u for u in newsyms(L) if u not in sub]
    solx = sp.solve(eqs, new, dict=True)[0]
    sub.update({k2: sp.cancel(sp.expand(vv)) for k2, vv in solx.items()}); norm()
    assert res(lev(L)) == 0, f"L={L} residual not identically zero"
    print(f"L={L:3d}: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, "
          f"kernel {info[1]-info[2]}), residual 0", flush=True)
for L in range(19, 7, -1): close(L)
conds = []
for L in range(7, -3, -1):
    st, eqs, cs, info = analyse(L)
    nz = [sp.expand(sp.numer(sp.together(c))) for c in eqs]
    nz = [c for c in nz if sp.simplify(c) != 0]
    conds += nz
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str) if conds else []
print(f"\nCHART={CHART} PICK={PICK}: {NBR[0]} multi-component decision(s); "
      f"{len(conds)} conditions in {len(V)} parameters")
pickle.dump((conds, sub), open(f'comp_{CHART}{PICK}.pkl','wb'))
print(f"saved comp_{CHART}{PICK}.pkl", flush=True)
