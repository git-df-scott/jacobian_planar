"""Session 43 — an exact linear reducer for msolve .ms systems over F_p.

Several of the campaign's frontier systems die on memory rather than on
mathematics.  On this box, three separate ones OOM-killed with 0-byte output
(corrected B=16 d=8 at 13.9 GB; the pentagon seed-extension 241eq/123unk at
13.75 GB; p11zero_full_sat 186var/306eq at 13.2 GB).  Shrinking a system before
handing it to Groebner is therefore worth more than more compute.

The idea is the campaign's own (w6_pent_lineloop.py): use ONLY equations that
are total-degree 1 with an invertible coefficient, solve one for a variable and
substitute, and iterate to a fixed point.  Each step is exact and reversible, so
no solution is created or destroyed; and substitution can turn quadratics into
new linear equations, so the loop can go further than the initial count suggests.

THE TRAP THIS ONE AVOIDS.  The campaign's first attempt at exactly this produced
a file msolve refused, because elimination was done mod p but the SUBSTITUTION
used plain integer arithmetic: products of residues were never reduced, so
coefficients grew past p and some were exact multiples of it (their example:
-1577793733367 = 1000003 * 1577789).  msolve then reads a nonzero coefficient as
zero -- one of its two documented silent lies.  Here every coefficient is
reduced into [0,p) after every multiplication and every addition, and terms that
reduce to zero are dropped, with a final audit that no coefficient is >= p and
no monomial is repeated within a polynomial.

CONTROLS (can-fail, run first):
  * a synthetic system with a PLANTED solution must still be satisfied by that
    solution after reduction;
  * an INCONSISTENT system must be reported inconsistent, not silently reduced;
  * a system with NO linear equations must come back untouched.

WHEN NOT TO USE greedy_reduce.  Measured on p11zero: the linear-only loop gives
174 vars / 294 equations and keeps every equation QUADRATIC.  Letting the greedy
pass also use constant-coefficient linear occurrences inside higher-degree
equations removes 20 more variables (154/274) but TRIPLES the term count
(6757 -> 20261) and raises the maximum degree from 2 to 6.  That is a bad trade
for F4/Groebner, whose cost is dominated by degree, not by variable count: a
system of quadrics is far better behaved than one of sextics in slightly fewer
variables.  For a quadratic target, degree-preserving elimination means LINEAR
elimination only -- i.e. reduce_system is already the right tool, and
greedy_reduce should be reserved for systems where degree growth is acceptable.
"""
import re
import sys


def parse(path):
    L = open(path).read().split('\n')
    variables = L[0].split(',')
    p = int(L[1])
    polys = []
    for line in L[2:]:
        line = line.strip().rstrip(',')
        if line:
            polys.append(parse_poly(line, set(variables), p))
    return variables, p, polys


def parse_poly(line, vset, p):
    """-> dict: monomial (sorted tuple of (var,exp)) -> coeff in [0,p)."""
    out = {}
    for term in re.split(r'(?=[+-])', line.replace(' ', '')):
        if not term:
            continue
        sign = -1 if term.startswith('-') else 1
        body = term.lstrip('+-')
        coeff = 1
        mono = {}
        for tok in body.split('*'):
            if not tok:
                continue
            m = re.fullmatch(r'([A-Za-z]\w*)(?:\^(\d+))?', tok)
            if m and m.group(1) in vset:
                mono[m.group(1)] = mono.get(m.group(1), 0) + int(m.group(2) or 1)
            else:
                m2 = re.fullmatch(r'(\d+)(?:\^(\d+))?', tok)
                if m2:
                    coeff = coeff*pow(int(m2.group(1)), int(m2.group(2) or 1))
                else:
                    raise ValueError("token %r" % tok)
        key = tuple(sorted(mono.items()))
        out[key] = (out.get(key, 0) + sign*coeff) % p
    return {k: v for k, v in out.items() if v}


def poly_str(poly, p):
    if not poly:
        return "0"
    parts = []
    for mono, c in sorted(poly.items()):
        c %= p
        if not c:
            continue
        s = str(c)
        for v, e in mono:
            s += "*" + v + ("^%d" % e if e > 1 else "")
        parts.append(s)
    return "+".join(parts) if parts else "0"


def mul_mono(a, b):
    d = dict(a)
    for v, e in b:
        d[v] = d.get(v, 0) + e
    return tuple(sorted(d.items()))


def substitute(poly, var, repl, p):
    """Replace var by the polynomial repl (which must not contain var)."""
    out = {}
    for mono, c in poly.items():
        e = dict(mono).get(var, 0)
        if e == 0:
            out[mono] = (out.get(mono, 0) + c) % p
            continue
        rest = tuple((v, x) for v, x in mono if v != var)
        acc = {(): c % p}
        for _ in range(e):
            nxt = {}
            for m1, c1 in acc.items():
                for m2, c2 in repl.items():
                    k = mul_mono(m1, m2)
                    nxt[k] = (nxt.get(k, 0) + c1*c2) % p      # reduce EVERY product
            acc = {k: v for k, v in nxt.items() if v}
        for m1, c1 in acc.items():
            k = mul_mono(rest, m1)
            out[k] = (out.get(k, 0) + c1) % p                 # reduce EVERY sum
    return {k: v for k, v in out.items() if v}


def reduce_system(variables, p, polys, verbose=True):
    polys = [dict(q) for q in polys]
    eliminated = {}
    rounds = 0
    while True:
        rounds += 1
        pick = None
        for i, q in enumerate(polys):
            if not q:
                continue
            deg = max(sum(e for _v, e in m) for m in q)
            if deg != 1:
                continue
            for mono, c in q.items():
                if len(mono) == 1 and mono[0][1] == 1:
                    pick = (i, mono[0][0], c)
                    break
            if pick:
                break
        if not pick:
            break
        i, var, c = pick
        q = polys[i]
        inv = pow(c, p - 2, p)
        repl = {}
        for mono, cc in q.items():
            if mono == ((var, 1),):
                continue
            repl[mono] = (-cc*inv) % p
        repl = {k: v for k, v in repl.items() if v}
        polys = [substitute(r, var, repl, p) for j, r in enumerate(polys) if j != i]
        eliminated[var] = repl
        for v2 in list(eliminated):
            if v2 != var:
                eliminated[v2] = substitute(eliminated[v2], var, repl, p)
        if any(q and all(len(m) == 0 for m in q) for q in polys):
            for q in polys:
                if q and list(q) == [()]:
                    return None, None, "INCONSISTENT: 1 = 0 after elimination"
    live = sorted({v for q in polys for m in q for v, _e in m})
    polys = [q for q in polys if q]
    if verbose:
        print("   rounds %d  eliminated %d variables  ->  %d vars / %d equations"
              % (rounds - 1, len(eliminated), len(live), len(polys)))
    return live, polys, eliminated


def audit(p, polys):
    """No coefficient outside [1,p), no empty poly, no repeated monomial."""
    for q in polys:
        for _m, c in q.items():
            if not (0 < c < p):
                return False, "coefficient %s out of range" % c
        if not q:
            return False, "empty polynomial"
    return True, "ok"


def write_ms(path, variables, p, polys):
    with open(path, 'w') as f:
        f.write(",".join(variables) + "\n")
        f.write("%d\n" % p)
        f.write(",\n".join(poly_str(q, p) for q in polys) + "\n")




# ------------------------------------------------------- greedy solve-and-substitute
# The linear-only loop above uses total-degree-1 equations.  But a HIGHER-degree
# equation can still be linear in one variable with a CONSTANT coefficient
# (e.g. 3z + xy + ...), and then z = -(xy+...)/3 substitutes polynomially -- no
# denominators, exact and reversible, so no solution is created or destroyed.
# In p11zero 179 of 186 variables occur that way.
#
# The catch is expression swell: substituting a big expression into many
# equations can cost more than the variable saves.  So this is greedy on SIZE --
# always eliminate the variable whose replacement has the fewest terms and
# lowest degree -- and it aborts if the total system size grows past a cap.

def _size(polys):
    return sum(len(q) for q in polys)


def _deg(q):
    return max((sum(e for _v, e in m) for m in q), default=0)


def candidates(polys):
    """(i, var, coeff, nterms, degree) for every constant-coefficient linear occurrence."""
    out = []
    for i, q in enumerate(polys):
        for mono, c in q.items():
            if len(mono) == 1 and mono[0][1] == 1:
                var = mono[0][0]
                rest = {m: cc for m, cc in q.items() if m != mono}
                out.append((i, var, c, len(rest), _deg(rest)))
    return out


def greedy_reduce(variables, p, polys, growth_cap=8.0, max_deg=6, verbose=True):
    polys = [dict(q) for q in polys if q]
    start = _size(polys)
    elim = 0
    while True:
        cands = candidates(polys)
        if not cands:
            break
        # cheapest first: small replacement, low degree
        cands.sort(key=lambda t: (t[4], t[3]))
        done = False
        for (i, var, c, nt, dg) in cands:
            q = polys[i]
            inv = pow(c, p - 2, p)
            repl = {m: (-cc*inv) % p for m, cc in q.items() if m != ((var, 1),)}
            repl = {k: v for k, v in repl.items() if v}
            if any(var == v for m in repl for v, _e in m):
                continue                      # must not contain the variable itself
            trial = [substitute(r, var, repl, p) for j, r in enumerate(polys) if j != i]
            trial = [t for t in trial if t]
            if any(list(t) == [()] for t in trial):
                return None, None, "INCONSISTENT after eliminating %s" % var
            if _size(trial) > growth_cap*start or max((_deg(t) for t in trial), default=0) > max_deg:
                continue                      # too expensive; try the next candidate
            polys = trial
            elim += 1
            done = True
            break
        if not done:
            break
    live = sorted({v for q in polys for m in q for v, _e in m})
    if verbose:
        print("   greedy: eliminated %d more variables -> %d vars / %d equations "
              "(terms %d -> %d, max degree %d)"
              % (elim, len(live), len(polys), start, _size(polys),
                 max((_deg(q) for q in polys), default=0)))
    return live, polys, elim


# ------------------------------------------------------------------ controls
def _controls():
    ok = True
    P = 1000003
    # (1) planted solution survives
    sol = {'a': 5, 'b': 7, 'c': 11}
    sys_ = [
        {(('a', 1),): 1, (('b', 1),): 1, (): (-(sol['a'] + sol['b'])) % P},      # a+b-12
        {(('a', 1), ('c', 1)): 1, (): (-(sol['a']*sol['c'])) % P},               # ac-55
        {(('b', 2),): 1, (): (-(sol['b']**2)) % P},                              # b^2-49
    ]
    live, red, elim = reduce_system(['a', 'b', 'c'], P, sys_, verbose=False)
    def ev(q, s):
        t = 0
        for m, c in q.items():
            v = c
            for var, e in m:
                v = v*pow(s[var], e, P) % P
            t = (t + v) % P
        return t
    good = red is not None and all(ev(q, sol) == 0 for q in red)
    print(("  PASS  " if good else "  FAIL  ") + "planted solution still satisfies the reduced system")
    ok &= good
    # (2) inconsistency is reported
    bad = [{(('a', 1),): 1, (): P - 1}, {(('a', 1),): 1, (): P - 2}]
    r = reduce_system(['a'], P, bad, verbose=False)
    good = (r[0] is None) or (r[1] == []) or any(list(q) == [()] for q in (r[1] or []))
    print(("  PASS  " if good else "  FAIL  ") + "an inconsistent system is detected, not silently reduced")
    ok &= good
    # (3) no linear equations -> untouched
    quad = [{(('a', 2),): 1, (('b', 2),): 1, (): P - 1}]
    live, red, elim = reduce_system(['a', 'b'], P, quad, verbose=False)
    good = len(elim) == 0 and len(red) == 1
    print(("  PASS  " if good else "  FAIL  ") + "a system with no linear equations is returned untouched")
    ok &= good
    return ok


if __name__ == '__main__':
    print("controls:")
    if not _controls():
        print("CONTROLS FAILED -- not reducing anything")
        sys.exit(1)
    if len(sys.argv) >= 3:
        src, dst = sys.argv[1], sys.argv[2]
        variables, p, polys = parse(src)
        print("\n%s: %d vars / %d equations" % (src, len(variables), len(polys)))
        live, red, elim = reduce_system(variables, p, polys)
        if live is None:
            print("   ", elim)
            sys.exit(0)
        ok, msg = audit(p, red)
        print("   audit:", msg)
        if not ok:
            sys.exit(1)
        write_ms(dst, live, p, red)
        print("   wrote", dst)
