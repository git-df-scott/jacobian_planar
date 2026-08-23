#!/usr/bin/env python3
"""The pentagon on the witness: no symbolic division, no branch choices.

Every earlier run solved each level with sp.solve, which divides by whatever
pivot it likes.  Two things go wrong.  Loudly: if that pivot is later forced to
zero, stored values become zoo and the run dies (levels 13 and 8 both did).
Quietly, and far worse: dividing by a quantity DELETES that quantity's
vanishing locus from the chart.  That is how the g9_8 = 0 chart stayed hidden,
and on it 47 of 51 endgame conditions died at once.  Any verdict obtained that
way is conditional on assumptions nobody wrote down.

This removes the problem instead of managing it.  At each level, eliminate new
unknowns by Gaussian elimination using ONLY pivots that are nonzero RATIONAL
numbers.  Those divisions are unconditional and delete nothing.  Any row with no
rational pivot is not solved at all -- it is simply carried out as a condition.
Levels 7 down to -2 contribute all their coefficients as conditions too.

The result is ONE polynomial system whose variety is exactly the pentagon on
this witness: no charts, no branch choices, no saturation, no inherited
assumptions such as g8_6 = g8_7 = 0.  It is larger than any single chart, which
is the price of not assuming anything.
"""
import sympy as sp, pickle, sys
PRIME = 1073741827
def redp(e):
    """Reduce an expanded expression's coefficients into F_PRIME.

    Characteristic 0 is where this descent dies: the rational coefficients grow
    without bound and by level 12 a single pivot costs an entire slice.  Mod a
    large prime they stay in one machine word, so the same algebra runs orders
    of magnitude faster and in bounded memory.

    A mod-p EMPTY is evidence, NOT a verdict -- a bad prime can manufacture a
    false EMPTY (p*x - 1 is a unit mod p but has the root 1/p over Q).  A mod-p
    NONEMPTY is the useful direction: it hands back an explicit candidate to
    lift, and a candidate is what a counterexample hunt actually needs.
    """
    e = sp.expand(e)
    if e == 0: return e
    gens = sorted(e.free_symbols, key=str)
    if not gens:
        q = sp.Rational(e)
        return sp.Integer((int(q.p) * pow(int(q.q), PRIME-2, PRIME)) % PRIME)
    P = sp.Poly(e, *gens)
    d = {}
    for mon, co in P.terms():
        q = sp.Rational(co)
        v = (int(q.p) * pow(int(q.q), PRIME-2, PRIME)) % PRIME
        if v: d[mon] = sp.Integer(v)
    if not d: return sp.Integer(0)
    return sp.Poly(d, *gens).as_expr()
def invp(c):
    """modular inverse of a nonzero rational constant"""
    q = sp.Rational(c)
    return sp.Integer((int(q.p) * pow(int(q.q), PRIME-2, PRIME)) % PRIME)

z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
# Only h_8 = c0 (s-tau)^8 is theorem-backed (eighth-power theorem); c0 and tau
# are normalisations, so h_8 = z^8 is WLOG.  h_7 = 2z^8, h_6 = z^8, g_12 = z^12
# were a CHOICE of witness -- one point of branch 1 -- so here they are FREE.
# This decides the whole Newton-polygon pair, not one witness.
# h_8 = c0 (s-tau)^8 : eighth-power theorem, c0 and tau are normalisations.
# g_12 = c1 (s-tau)^12 : UPPER-EDGE theorem.  A = c0 G^2 and Qh = c1 G^3 with
#   deg G = 4, and the eighth-power theorem forces G = (t-tau)^4; c1 is absorbed
#   by scaling Q.  So g_12 is FORCED, not chosen -- nodivide3 freed it for
#   nothing, spending 13 parameters to rediscover a theorem.
# h_7 and h_6 ARE genuine choices in the witness, so here they are FREE.
H = {8: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 8): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return redp(e - (s**2 if L == -2 else 0))
def newsyms(L):
    out = []
    if 0 <= L-12 <= 7: out += [sp.Symbol(f'h{L-12}_{i}') for i in hsup(L-12)]
    if 0 <= L-8 <= 11: out += [sp.Symbol(f'g{L-8}_{k}') for k in gsup(L-8)]
    return out
sub, conds = {}, []
USES = {}          # symbol -> set of sub keys whose stored value mentions it
def setsub(x, val):
    """record x = val and push it into ONLY the stored values that mention x.

    The naive version re-expanded every entry of sub after every pivot; sub
    reaches ~150 entries with large values, so that is quadratic and the run
    produced no output at all in nine minutes.  A reverse index makes each
    update touch only what actually changes."""
    for k in list(USES.get(x, ())):
        if k not in sub: continue
        nv = redp(sub[k].subs(x, val))
        sub[k] = nv
        for y in nv.free_symbols: USES.setdefault(y, set()).add(k)
    USES.pop(x, None)
    sub[x] = val
    for y in val.free_symbols: USES.setdefault(y, set()).add(x)
def norm(): pass
def res(e):
    """One substitution pass, not a fixed-point loop.

    setsub keeps sub self-consistent -- no key ever appears inside any stored
    value -- so a single simultaneous subs is already the fixed point.  The old
    26-pass loop re-substituted into ever-larger expressions up to 26 times per
    call, on the single most expensive operation in the descent.  The assert
    keeps the invariant honest rather than assumed."""
    e2 = redp(e.subs(sub))
    assert not (e2.free_symbols & set(sub)), "sub is not self-consistent"
    return e2
import os
CK = 'nodivide5.ckpt'
START = 19
MID = None
if os.path.exists(CK + '.mid'):
    _L, sub, USES, conds, _eqs, _new, _solved = pickle.load(open(CK + '.mid', 'rb'))
    MID = (_L, _eqs, _new, _solved); START = _L
    print(f"RESUMED INSIDE level {_L}: {_solved} already solved, "
          f"{len(_eqs)} equations left, {len(conds)} conditions so far", flush=True)
elif os.path.exists(CK):
    START, sub, USES, conds = pickle.load(open(CK, 'rb'))
    START -= 1
    print(f"RESUMED at level {START}: {len(sub)} substitutions, "
          f"{len(conds)} conditions so far", flush=True)
DEADLINE = __import__('time').time() + float(os.environ.get('SLICE', '440'))
for L in range(START, -3, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if redp(c) != 0]
    if not eqs:
        print(f"L={L:3d}: satisfied", flush=True); continue
    new = [u for u in newsyms(L) if u not in sub]
    solved = 0
    if MID is not None and MID[0] == L:
        _, eqs, new, solved = MID; MID = None
    changed = True
    while changed and new:
        changed = False
        for idx, c in enumerate(eqs):
            P = {x: sp.Poly(c, x) for x in new if x in c.free_symbols}
            for x, Px in P.items():
                if Px.degree() != 1: continue
                c1 = Px.coeff_monomial(x)
                if not (c1.is_number and c1 != 0): continue     # RATIONAL PIVOTS ONLY
                val = redp(-Px.coeff_monomial(1) * invp(c1))   # modular inverse, not a rational quotient
                assert not val.has(sp.zoo) and not val.has(sp.nan), f"L={L} degenerate"
                setsub(x, val)
                new.remove(x); solved += 1
                eqs = [q for k, q in enumerate(eqs) if k != idx]
                eqs = [redp(q.subs(sub)) for q in eqs]
                eqs = [q for q in eqs if redp(q) != 0]
                # MID-LEVEL checkpoint.  Between-level checkpoints are not
                # enough once a single level costs more than a whole slice,
                # which level 14 does with the top data free.
                pickle.dump((L, sub, USES, conds, eqs, new, solved),
                            open(CK + '.mid', 'wb'))
                if __import__('time').time() > DEADLINE:
                    print(f"--- slice deadline INSIDE level {L} "
                          f"({solved} solved so far); rerun to continue ---", flush=True)
                    sys.exit(3)
                changed = True; break
            if changed: break
    # Leftover rows have no rational pivot among the NEW unknowns, but may
    # still be UNCONDITIONALLY solvable for a CARRIED parameter.  Two cases are
    # forced, with one component and no branch choice, so imposing them assumes
    # nothing while cutting the free-parameter count that made the fully
    # assumption-free run OOM at level 10:
    #   * linear in one variable with a nonzero RATIONAL coefficient
    #   * a pure power  const * u^k  with u linear in one variable, rationally
    # Anything else -- in particular anything REDUCIBLE, which is a union of
    # components -- is carried out as a condition, never chosen between.
    left = [redp(q) for q in eqs if redp(q) != 0]
    progress = True
    while progress:
        progress = False
        for q in list(left):
            fl = [b for b, _e in sp.factor_list(q)[1] if b.free_symbols]
            targets = [q] if len(fl) != 1 else [fl[0]]   # pure power -> its base
            for u in targets:
                for x in sorted(u.free_symbols, key=str):
                    Px = sp.Poly(u, x)
                    if Px.degree() != 1: continue
                    c1 = Px.coeff_monomial(x)
                    if not (c1.is_number and c1 != 0): continue
                    val = redp(-Px.coeff_monomial(1) * invp(c1))   # modular inverse, not a rational quotient
                    assert not val.has(sp.zoo) and not val.has(sp.nan)
                    setsub(x, val)
                    left = [redp(w.subs(x, val)) for w in left if w is not q]
                    left = [w for w in left if redp(w) != 0]
                    print(f"        unconditional gate: {x}", flush=True)
                    progress = True; break
                if progress: break
            if progress: break
    conds += left
    print(f"L={L:3d}: {solved} solved on rational pivots, {len(left)} condition(s) carried out, "
          f"{len(new)} new unknown(s) left free", flush=True)
    pickle.dump((L, sub, USES, conds), open(CK, 'wb'))
    if os.path.exists(CK + '.mid'): os.remove(CK + '.mid')
    if __import__('time').time() > DEADLINE:
        print(f"--- slice deadline; checkpointed after level {L}, rerun to continue ---",
              flush=True)
        sys.exit(3)
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str) if conds else []
print(f"\nTOTAL {len(conds)} conditions in {len(V)} variables")
pickle.dump((conds, sub), open('nodivide5.pkl','wb'))
print("saved nodivide5.pkl", flush=True)
