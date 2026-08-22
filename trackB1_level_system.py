#!/usr/bin/env python3
"""Interpolate a cascade level as an EXACT polynomial system and solve it.

Each level m of the ladder, restricted to the live parameters (the level-4
parametrization of P_6 plus the free slices P_5, P_4, ... introduced so far),
is a polynomial system of low degree.  Measured: level 5 has degree 2 in the
parameters, and ALL 12 coefficients of rem(N_m, S^3) are live (P_5 reaches
digits 0 and 1 through the F-terms F_10 F_9, not only digit 2).

So the level is 12 quadratic equations in 15 unknowns at level 5, growing by
about 12 equations and 7 unknowns per level.  Slicing to 4 variables (as a
naive search does) is hopelessly overdetermined and finds nothing even when
solutions exist -- so the system is interpolated exactly and handed to Singular.

Interpolation is exact: with the degree bound d verified by finite differences
along random lines, the monomial basis is complete and the fitted coefficients
are the true ones (the sample matrix is checked for full rank).
"""
import random, sys, itertools, subprocess, os, json
from trackB1_sqrt import pmul, padd, pscal, ptrim, prange
from trackB1_cascade_general import component1_S, component2_S, half_radical
from trackB1_joint import make_P, cond_at, layout_for

p = 65521

def measure_degree(fn, nvars, rng, samples=3, cap=8):
    """Max degree of fn's coefficients along random lines."""
    best = 0
    for _ in range(samples):
        base = [rng.randrange(p) for _ in range(nvars)]
        d = [rng.randrange(p) for _ in range(nvars)]
        vals = []
        for t in range(cap + 3):
            q = [(base[i] + t * d[i]) % p for i in range(nvars)]
            c = fn(q)
            if c is None:
                return None
            vals.append(c)
        L = max((len(v) for v in vals), default=0)
        for r in range(L):
            y = [(v[r] if r < len(v) else 0) for v in vals]
            cur, deg = y[:], 0
            while len(cur) > 1 and any(cur):
                cur = [(cur[i + 1] - cur[i]) % p for i in range(len(cur) - 1)]
                deg += 1
            best = max(best, deg - 1 if not any(cur) else cap)
    return best

def interpolate(fn, nvars, deg, rng, extra=25):
    """Return list of polynomials (dicts monomial->coeff) for each coefficient."""
    monos = [m for dd in range(deg + 1)
             for m in itertools.combinations_with_replacement(range(nvars), dd)]
    npts = len(monos) + extra
    pts, vals = [], []
    for _ in range(npts):
        v = [rng.randrange(p) for _ in range(nvars)]
        c = fn(v)
        if c is None:
            return None, None
        pts.append(v)
        vals.append(c)
    L = max((len(v) for v in vals), default=0)
    A = []
    for v in pts:
        row = []
        for m in monos:
            t = 1
            for i in m:
                t = t * v[i] % p
            row.append(t)
        A.append(row)
    # rank check: the monomial basis must be identifiable
    rank = _rank(A)
    if rank < len(monos):
        return None, f"interpolation rank {rank} < {len(monos)}"
    polys = []
    for r in range(L):
        rhs = [(v[r] if r < len(v) else 0) for v in vals]
        coef = _lstsq(A, rhs)
        if coef is None:
            return None, "inconsistent interpolation (degree bound too low)"
        if any(coef):
            polys.append({m: c for m, c in zip(monos, coef) if c})
    return polys, monos

def _rank(A):
    M = [row[:] for row in A]
    n = len(M[0])
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(n)]
        r += 1
    return r

def _lstsq(A, rhs):
    n = len(A[0])
    M = [A[i][:] + [rhs[i]] for i in range(len(A))]
    r = 0
    piv = {}
    for c in range(n):
        pr = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(n + 1)]
        piv[c] = r
        r += 1
    for i in range(len(M)):
        if all(M[i][c] % p == 0 for c in range(n)) and M[i][n] % p:
            return None
    out = [0] * n
    for c, rr in piv.items():
        out[c] = M[rr][n] % p
    return out

def to_singular(polys, nvars, name="I"):
    terms = []
    for pol in polys:
        parts = []
        for m, c in pol.items():
            s = str(c)
            for i in sorted(set(m)):
                e = m.count(i)
                s += f"*x({i})" + (f"^{e}" if e > 1 else "")
            parts.append(s)
        terms.append("+".join(parts) if parts else "0")
    return terms

def singular_analyze(polys, nvars, timeout=900):
    eqs = to_singular(polys, nvars)
    src = f"""
option(redSB);
ring R = {p}, x(0..{nvars-1}), dp;
ideal I = {','.join(eqs)};
ideal G = std(I);
if (size(G) == 1 && G[1] == 1) {{ "VERDICT: EMPTY (1 in ideal)"; }}
else {{
  "VERDICT: NONEMPTY over the algebraic closure";
  "dim = " + string(dim(G));
  "deg-of-ideal codim = " + string({nvars} - dim(G));
}}
quit;
"""
    fn = "/tmp/claude-0/-home-user-jacobian-planar/19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad/lvl.sing"
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w") as f:
        f.write(src)
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

if __name__ == "__main__":
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    tag = sys.argv[3] if len(sys.argv) > 3 else "I"
    rng = random.Random(seed)
    if tag == "I":
        A = [1, rng.randrange(p), rng.randrange(1, p)]
        S = component1_S(A, 1, p)
    else:
        S = None
        while S is None:
            u, v = rng.randrange(1, p), rng.randrange(1, p)
            S = component2_S(u, v, 1, p)
    M = [rng.randrange(p) for _ in range(5)]
    lay = layout_for(S)
    wl = []
    for m in range(4, mmax + 1):
        w = 10 - m
        if w <= 6:
            wl.append(w)
    nvars = sum(lay[w] for w in wl)
    print(f"component {tag}, level {mmax}: live slices {wl}, {nvars} parameters")

    def fn(q):
        return cond_at(S, make_P(S, M, wl, q, lay), mmax)

    deg = measure_degree(fn, nvars, rng)
    print(f"  measured degree in the parameters: {deg}")
    polys, info = interpolate(fn, nvars, deg, rng)
    if polys is None:
        print(f"  INTERPOLATION FAILED: {info}")
        sys.exit(1)
    print(f"  interpolated {len(polys)} equations "
          f"(monomial basis verified full rank)")
    out = singular_analyze(polys, nvars)
    print("  Singular:")
    for line in out.splitlines():
        print("    " + line)
