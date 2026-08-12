"""
Plane Jacobian campaign - Session 20
THE (8,28) OPEN CASE OVER GF(p): triangular reduction with no rational overhead.

The sympy reduction works but is slow, because every substitution builds
rational functions and every round calls together/fraction/factor_list.  Over
GF(p) none of that exists: coefficients are single machine ints and never grow.
This file reimplements the same triangular elimination on plain dicts.

WHAT A GF(p) VERDICT MEANS -- stated up front so it is never overclaimed:

  * A characteristic-zero solution reduces mod p for all but finitely many p.
    So "no solution mod p", for several independent p, is strong evidence of no
    solution over Qbar -- but it is NOT a proof, because the excluded primes are
    not identified.  A genuine closure of (8,28) must be redone over Q.
  * Conversely a mod-p solution is only a CANDIDATE.  It must be lifted to
    characteristic zero and then pass jc2_bulletproof.py.  It is never, by
    itself, a counterexample -- the Jacobian conjecture is FALSE in
    characteristic p, so a mod-p Keller pair proves nothing at all.
  * FROBENIUS GUARD: every prime used exceeds every degree in the system, so no
    p-th-power artifact can appear in range.  Asserted, not assumed.

The elimination rules are the same two that the exact run uses:
  R1  a single-monomial equation forces one of its variables to zero; if every
      variable in it is a required-nonzero vertex coefficient, that is a
      CONTRADICTION and the case closes;
  R2  an equation linear in some variable, with an invertible coefficient
      (nonzero constant, or a monomial in the known-nonzero coefficients),
      solves for that variable, which is then substituted everywhere.
"""

import sys
import time
from itertools import combinations

sys.path.insert(0, '/home/user/jacobian_planar')
import sympy as sp
import jc2_gghv_system as G

SCRATCH = ('/tmp/claude-0/-home-user-jacobian-planar/'
           '8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad')


# --------------------------------------------------------------- poly over GF(p)
# monomial: tuple of (var_index, exponent) sorted by var_index
# poly    : dict monomial -> coeff (int mod p), never storing zero coeffs

def pnorm(d, p):
    return {m: c % p for m, c in d.items() if c % p}


def padd(a, b, p):
    out = dict(a)
    for m, c in b.items():
        out[m] = (out.get(m, 0) + c) % p
    return {m: c for m, c in out.items() if c}


def pscal(a, k, p):
    k %= p
    if k == 0:
        return {}
    return {m: (c*k) % p for m, c in a.items()}


def mmul(m1, m2):
    d = dict(m1)
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted(d.items()))


def pmul(a, b, p):
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = mmul(m1, m2)
            out[m] = (out.get(m, 0) + c1*c2) % p
    return {m: c for m, c in out.items() if c}


def ppow(a, n, p):
    r = {(): 1}
    for _ in range(n):
        r = pmul(r, a, p)
    return r


def psubs(a, var, val, p):
    """Substitute variable index `var` by polynomial `val`."""
    out = {}
    cache = {0: {(): 1}}
    for m, c in a.items():
        e = dict(m).get(var, 0)
        rest = tuple((v, x) for v, x in m if v != var)
        if e not in cache:
            cache[e] = ppow(val, e, p)
        term = pscal(cache[e], c, p)
        term = pmul(term, {rest: 1}, p) if rest else term
        out = padd(out, term, p)
    return out


def pvars(a):
    s = set()
    for m in a:
        for v, _e in m:
            s.add(v)
    return s


def pdeg_in(a, var):
    return max((dict(m).get(var, 0) for m in a), default=0)


# --------------------------------------------------------------- reduction
def reduce_modp(eqs, nz_idx, p, names, verbose=True, report_every=10):
    """eqs: list of polys. nz_idx: set of variable indices required nonzero."""
    eqs = [pnorm(e, p) for e in eqs]
    eqs = [e for e in eqs if e]
    zeroed, solved = set(), {}
    t0 = time.time()
    rnd = 0
    while True:
        rnd += 1
        changed = False

        # R1: single-monomial equations
        for e in list(eqs):
            if len(e) != 1:
                continue
            (m, _c), = e.items()
            vs = [v for v, _x in m]
            if not vs:
                return eqs, solved, zeroed, "nonzero constant equation: CONTRADICTION"
            live = [v for v in vs if v not in nz_idx]
            if not live:
                return (eqs, solved, zeroed,
                        "monomial in only required-nonzero coefficients: CONTRADICTION "
                        f"({'*'.join(names[v] for v in vs)} = 0)")
            v = live[0]
            zeroed.add(v)
            eqs = [pnorm(psubs(x, v, {}, p), p) for x in eqs]
            eqs = [x for x in eqs if x]
            changed = True
            if verbose:
                print(f"    r{rnd}: kill {names[v]} = 0   (eqs {len(eqs)})", flush=True)
            break
        if changed:
            continue

        # R2: linear-with-invertible-coefficient
        best = None
        for e in eqs:
            vs = pvars(e)
            for v in vs:
                if pdeg_in(e, v) != 1:
                    continue
                # split e = A*v + B with A free of v
                A, B = {}, {}
                for m, c in e.items():
                    d = dict(m)
                    if d.get(v, 0) == 1:
                        del d[v]
                        A[tuple(sorted(d.items()))] = c
                    else:
                        B[m] = c
                if len(A) != 1:
                    continue
                (am, ac), = A.items()
                if any(w not in nz_idx for w, _x in am):
                    continue          # coefficient not known invertible
                score = len(B)
                if best is None or score < best[0]:
                    best = (score, v, A, B, e, am, ac)
        if best is None:
            break
        _s, v, A, B, src, am, ac = best
        # v = -B / (ac * am);  multiply through: represent as poly by dividing
        inv = pow(ac, p - 2, p)
        val = pscal(B, -inv, p)
        # divide by the monomial am (all its variables are invertible)
        if am:
            val = {tuple(sorted((dict(m) | {}).items())): c for m, c in val.items()}
            newval = {}
            ok = True
            for m, c in val.items():
                d = dict(m)
                for w, x in am:
                    d[w] = d.get(w, 0) - x
                if any(x < 0 for x in d.values()):
                    ok = False
                    break
                newval[tuple(sorted((w, x) for w, x in d.items() if x))] = c
            if not ok:
                # cannot divide cleanly; skip this pivot by dropping it
                eqs = [x for x in eqs if x is not src] + [src]
                continue
            val = newval
        solved[v] = val
        eqs = [pnorm(psubs(x, v, val, p), p) for x in eqs if x is not src]
        eqs = [x for x in eqs if x]
        if verbose and (rnd <= 20 or rnd % report_every == 0):
            print(f"    r{rnd}: solve {names[v]}   (eqs {len(eqs)}, "
                  f"{time.time()-t0:.0f}s)", flush=True)
    return eqs, solved, zeroed, None


def main(p=32003):
    case = G.OPEN_CASE_2
    pp, _ = G.lattice_points(case["P"])
    qq, _ = G.lattice_points(case["Q"])
    ps = G.build_symbols("c", pp)
    qs = G.build_symbols("d", qq)
    seqs = G.bracket_system(pp, ps, qq, qs, case["rhs"])
    nz = set(G.nonzero_side_conditions(case["P"], ps)) | \
         set(G.nonzero_side_conditions(case["Q"], qs))
    allsym = list(ps.values()) + list(qs.values())

    maxdeg = max(max(a, b) for a, b in list(pp) + list(qq))
    assert p > maxdeg + 10, "Frobenius guard: prime must exceed all degrees"

    idx = {s: i for i, s in enumerate(allsym)}
    names = {i: str(s) for s, i in idx.items()}
    nz_idx = {idx[s] for s in nz}

    # normalize d_2_1 = 1 (proved WLOG in jc2_gghv_normalize.py)
    norm = [s for s in allsym if str(s) == 'd_2_1'][0]

    def to_poly(expr):
        e = sp.expand(expr.subs(norm, 1))
        out = {}
        for term in sp.Add.make_args(e):
            c, mon = term.as_coeff_Mul()
            d = {}
            for f in sp.Mul.make_args(mon):
                b, ex = f.as_base_exp()
                if b in idx:
                    d[idx[b]] = int(ex)
            out[tuple(sorted(d.items()))] = int(sp.Rational(c)) % p
        return {m: c for m, c in out.items() if c}

    eqs = [to_poly(e) for e in seqs.values()]
    eqs = [e for e in eqs if e]
    nz_idx.discard(idx[norm])

    print(f"GF({p}) triangular reduction of the GGHV (8,28) open case")
    print(f"Frobenius guard: p = {p} > max degree {maxdeg}.  OK")
    print(f"start: {len(allsym)-1} unknowns (d_2_1 normalized to 1), "
          f"{len(eqs)} equations, {len(nz_idx)} required-nonzero\n")

    eqs2, solved, zeroed, contra = reduce_modp(eqs, nz_idx, p, names)
    rem = set()
    for e in eqs2:
        rem |= pvars(e)
    print(f"\nRESULT over GF({p}):")
    print(f"  forced to zero  : {len(zeroed)}")
    print(f"  solved & removed: {len(solved)}")
    print(f"  equations left  : {len(eqs2)}")
    print(f"  variables left  : {len(rem)}")
    if contra:
        print(f"\n  *** {contra}")
        print("  *** => no (P,Q) of the Prop 4.3 (8,28) shape over GF(p).")
        print("  *** This is EVIDENCE, not proof: must be redone over Q, and the")
        print("  *** divisions by assumed-invertible coefficients re-justified.")
        return
    if not eqs2:
        print("\n  *** ALL EQUATIONS ELIMINATED over GF(p): solution set nonempty.")
        print("  *** CANDIDATE ONLY. Must be lifted to characteristic zero and")
        print("  *** then pass jc2_bulletproof.py. A mod-p Keller pair proves")
        print("  *** nothing -- JC is false in characteristic p.")
        return
    print(f"\n  residual system: {len(eqs2)} equations in {len(rem)} variables")
    rl = sorted(rem)
    def to_sing(e):
        parts = []
        for m, c in e.items():
            s = str(c)
            for v, x in m:
                s += "*" + names[v] + ("^" + str(x) if x > 1 else "")
            parts.append(s)
        return "+".join(parts)
    body = ",\n  ".join(to_sing(e) for e in eqs2)
    path = f"{SCRATCH}/gghv_modp_residual.sing"
    open(path, "w").write(
        f"ring R = {p}, ({','.join(names[v] for v in rl)}), dp;\n"
        f"ideal I = {body};\n"
        f'"residual: {len(rl)} vars, {len(eqs2)} eqs";\n'
        f"ideal Gb = std(I);\n\"basis size:\"; size(Gb);\n"
        f'"TRIVIAL (=> (8,28) closed mod p):"; (size(Gb)==1 && Gb[1]==1);\nquit;\n')
    print(f"  emitted -> {path}")


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 32003)
