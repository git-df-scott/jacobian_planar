#!/usr/bin/env python3
"""Session 44 — decide the u=0 exceptional chart of the (4,6) collision ribbon.

Chart (sol6 slice, everything exact):
    p0 = x^84 - x, c = 1, p1 = sum_{m>=2} a_m x^m, p2 = v x + sum b_m x^m,
    p3 = w x + sum_{m>=2} t_m x^m,  deg caps (63, 42, 21).
    A1=-1, A2=0, A3=-v/3, A5=-v^2/5, a2=(v w+3)/2, b2=(3/8)(v^3+w^2)  [rungs 0-1,
    unique — integer-constant pivots, no branching].
Rung n >= 2: E2[x^n], E1[x^n] determine b_{n+1}, a_{n+1} with INTEGER pivots
(-3 each; verified at rung 2 and asserted at every rung here); E0[x^n] is a
condition C_n.  C_2 = (2v^4 + 3v w^2 + 18w)/16 — the quartic.  Kernels t_m are
consumed only when some C_n actually depends on them; this solver:

  * carries kernels as ACTIVE SYMBOLS (polynomial coefficients mod p),
  * solves each condition for a kernel exactly when it is linear in it,
    BRANCHING separately on every vanishing leading coefficient and on every
    root when the dependence is quadratic,
  * never divides by anything non-constant without retaining the zero branch,
  * past the p3 cap (rung >= 22) conditions fall on (v,w) and remaining
    kernels — points die at their first unavoidable nonzero condition.

Mode `sweep p`: enumerate ALL points of the quartic over F_p (v=0 -> w=0
branch retained; v!=0 -> roots of 3v w^2 + 18w + 2v^4), walk each to the
horizon with full branch tracking, report per-point death rung or survival.
Survivors at two primes go to the exact characteristic-zero stage.
"""
import argparse
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from uvw_hunt import TERMS, USED_A  # noqa: E402  (term lists; A-usage check)

# ---------------- polynomial-in-active-kernels layer (mod p) ----------------
# elements: dict {exponent-tuple over active list: coeff mod p}; () = constant


def pz():
    return {}


def pconst(c, p):
    c %= p
    return {(): c} if c else {}


def padd_(A, B, p):
    out = dict(A)
    for k, v in B.items():
        nv = (out.get(k, 0) + v) % p
        if nv:
            out[k] = nv
        else:
            out.pop(k, None)
    return out


def pmul_(A, B, p, nact):
    if not A or not B:
        return {}
    out = {}
    for ka, va in A.items():
        ea = ka + (0,) * (nact - len(ka))
        for kb, vb in B.items():
            eb = kb + (0,) * (nact - len(kb))
            k = tuple(x + y for x, y in zip(ea, eb))
            while k and k[-1] == 0:
                k = k[:-1]
            nv = (out.get(k, 0) + va * vb) % p
            if nv:
                out[k] = nv
            else:
                out.pop(k, None)
    return out


def pscal(A, c, p):
    c %= p
    if not c:
        return {}
    return {k: (v * c) % p for k, v in A.items()}


class Branch:
    """One branch of the u=0 walk at a fixed quartic point."""

    def __init__(self, p, v, w, horizon):
        self.p, self.v, self.w, self.N = p, v, w, horizon
        self.active = []          # names of active kernel symbols, e.g. 't2'
        self.log = []
        inv2 = pow(2, p - 2, p)
        inv8 = pow(8, p - 2, p)
        a2 = (v * w + 3) * inv2 % p
        b2 = 3 * inv8 % p * (v**3 + w * w) % p
        self.s1 = {0: pz(), 1: pz(), 2: pconst(a2, p)}       # p1 coeffs
        self.s2 = {0: pz(), 1: pconst(v, p), 2: pconst(b2, p)}
        self.s3 = {0: pz(), 1: pconst(w, p), 2: None}        # t2 active below
        inv3 = pow(3, p - 2, p)
        inv5 = pow(5, p - 2, p)
        self.A = {1: pconst(p - 1, p), 2: pz(),
                  3: pconst((-v * inv3) % p, p),
                  5: pconst((-v * v * inv5) % p, p), 0: pz(), 4: pz()}
        self.new_kernel(3, 2)

    def clone(self):
        import copy
        b = object.__new__(Branch)
        b.p, b.v, b.w, b.N = self.p, self.v, self.w, self.N
        b.active = list(self.active)
        b.log = list(self.log)
        b.s1 = copy.deepcopy(self.s1)
        b.s2 = copy.deepcopy(self.s2)
        b.s3 = copy.deepcopy(self.s3)
        b.A = copy.deepcopy(self.A)
        return b

    def new_kernel(self, which, m):
        name = f"t{m}"
        self.active.append(name)
        idx = len(self.active) - 1
        mono = tuple([0] * idx + [1])
        {1: self.s1, 2: self.s2, 3: self.s3}[which][m] = {mono: 1}

    # series of each base symbol to order n (lists of poly-dicts)
    def series_for(self, idx, n):
        p = self.p
        zero = pz()
        if idx == 0:                                  # p0 = x^84 - x
            out = [zero] * (n + 1)
            if n >= 1:
                out[1] = pconst(-1, p)
            if n >= 84:
                out[84] = pconst(1, p)
            return out
        if idx < 4:
            src = {1: self.s1, 2: self.s2, 3: self.s3}[idx]
            return [src.get(k, zero) or zero for k in range(n + 1)]
        if idx == 4:                                  # dp0
            out = [pconst(-1, p)] + [zero] * n
            if n >= 83:
                out[83] = pconst(84, p)
            return out
        if idx < 8:
            src = {5: self.s1, 6: self.s2, 7: self.s3}[idx]
            return [pscal(src.get(k + 1, zero) or zero, k + 1, p)
                    for k in range(n + 1)]
        if idx < 14:
            out = [zero] * (n + 1)
            out[0] = self.A[idx - 8]
            return out
        out = [zero] * (n + 1)
        out[0] = pconst(1, p)                          # c = 1
        return out

    def row_coeff(self, row, n):
        """[x^n] of E-row as a poly-dict in the active kernels."""
        p, nact = self.p, len(self.active)
        cache = {}
        total = pz()
        for num, den, factors in TERMS[row]:
            c0 = num * pow(den, p - 2, p) % p
            acc = [pconst(c0, p)] + [pz()] * n
            for idx, power in factors:
                if idx not in cache:
                    cache[idx] = self.series_for(idx, n)
                fs = cache[idx]
                for _ in range(power):
                    new = [pz()] * (n + 1)
                    for i, av in enumerate(acc):
                        if not av:
                            continue
                        for j in range(n + 1 - i):
                            bv = fs[j]
                            if bv:
                                new[i + j] = padd_(new[i + j],
                                                   pmul_(av, bv, p, nact), p)
                    acc = new
            total = padd_(total, acc[n], p)
        return total

    def substitute(self, name, value):
        """Substitute active kernel := value (mod p) everywhere; drop it."""
        p = self.p
        pos = self.active.index(name)

        def sub(poly):
            out = {}
            for k, c in poly.items():
                e = k[pos] if pos < len(k) else 0
                nk = tuple(x for i, x in enumerate(k) if i != pos) \
                    if pos < len(k) else k
                # strip trailing zeros
                nk = tuple(nk)
                while nk and nk[-1] == 0:
                    nk = nk[:-1]
                nc = c * pow(value, e, p) % p if e else c
                if nc:
                    out[nk] = (out.get(nk, 0) + nc) % p
                    if not out[nk]:
                        del out[nk]
            return out
        for store in (self.s1, self.s2, self.s3):
            for k in store:
                if store[k]:
                    store[k] = sub(store[k])
        self.active.pop(pos)
        self.log.append(f"{name}={value}")


def univar(poly, active):
    """If poly involves at most one active kernel, return (idx, coeffs by
    degree); else None."""
    used = set()
    for k in poly:
        for i, e in enumerate(k):
            if e:
                used.add(i)
    if len(used) > 1:
        return None
    if not used:
        return (-1, {0: poly.get((), 0)})
    i = used.pop()
    out = {}
    for k, c in poly.items():
        e = k[i] if i < len(k) else 0
        out[e] = (out.get(e, 0) + c)
    return (i, out)


def walk(p, v, w, horizon, max_branches=64, trace=False):
    """Walk all branches at one quartic point.  Returns list of
    (status, depth, log) per branch; status 'SURVIVED' if horizon reached."""
    results = []
    stack = [(2, Branch(p, v, w, horizon))]
    while stack:
        n, br = stack.pop()
        died = None
        while n <= horizon:
            # TERMS rows: [0]=E2, [1]=E1, [2]=E0-1.
            # E2 -> b_{n+1}, E1 -> a_{n+1} (integer pivots; probed each rung)
            for row, store, cap in ((0, br.s2, 42), (1, br.s1, 63)):
                m = n + 1
                if m > cap:
                    continue
                # probe pivot: coefficient of the new unknown is constant;
                # evaluate row with unknown absent (0) then with 1
                store[m] = pz()
                base = br.row_coeff(row, n)
                store[m] = pconst(1, p)
                shift = br.row_coeff(row, n)
                store[m] = pz()
                piv = padd_(shift, pscal(base, -1, p), p)
                pv = univar(piv, br.active)
                assert pv is not None and pv[0] == -1, \
                    f"rung {n}: E{row} pivot not constant: {piv}"
                pivc = pv[1].get(0, 0)
                assert pivc, f"rung {n}: E{row} pivot vanished mod {p}"
                sol = pscal(base, -pow(pivc, p - 2, p) % p, p)
                store[m] = sol
            # E0 row (TERMS[2] = E0-1): condition / kernel consumption
            cond = br.row_coeff(2, n)
            uv = univar(cond, br.active)
            if uv is None:
                # multivariate in kernels: try to solve for the NEWEST kernel
                # linearly; coefficient may involve older kernels -> branch on
                # its vanishing is not decidable pointwise; report and stop
                results.append(("MULTIVAR", n, list(br.log)))
                died = True
                break
            i, coeffs = uv
            deg = max(coeffs) if coeffs else 0
            if i == -1 or deg == 0:
                val = coeffs.get(0, 0)
                if val % p:
                    results.append(("DEAD", n, list(br.log)))
                    died = True
                    break
            elif deg == 1:
                c1, c0 = coeffs.get(1, 0) % p, coeffs.get(0, 0) % p
                name = br.active[i]
                if c1:
                    br.substitute(name, (-c0 * pow(c1, p - 2, p)) % p)
                else:
                    if c0:
                        results.append(("DEAD", n, list(br.log)))
                        died = True
                        break
                    # 0 = 0: kernel stays free — record and continue
                    br.log.append(f"rung{n}:free({name})")
            else:
                # quadratic (or higher) in one kernel: branch on each root
                name = br.active[i]
                roots = [r for r in range(p)
                         if sum(coeffs.get(e, 0) * pow(r, e, p)
                                for e in coeffs) % p == 0]
                if not roots:
                    results.append(("DEAD-NOROOT", n, list(br.log)))
                    died = True
                    break
                if len(stack) + len(roots) > max_branches:
                    results.append(("BRANCH-CAP", n, list(br.log)))
                    died = True
                    break
                for r in roots[1:]:
                    nb = br.clone()
                    nb.substitute(name, r)
                    stack.append((n + 1, nb))
                br.substitute(name, roots[0])
            # introduce the next kernel p3[n+1] if within cap
            if n + 1 <= 21:
                br.new_kernel(3, n + 1)
            n += 1
        if not died:
            results.append(("SURVIVED", horizon, list(br.log)))
    return results


def quartic_points(p):
    pts = [(0, 0)]
    for v in range(1, p):
        # 3v w^2 + 18 w + 2v^4 = 0
        a, b, c = 3 * v % p, 18 % p, 2 * pow(v, 4, p) % p
        disc = (b * b - 4 * a * c) % p
        rs = [r for r in range(p) if (r * r - disc) % p == 0]
        for r in set(rs):
            w = (-b + r) * pow(2 * a, p - 2, p) % p
            if (a * w * w + b * w + c) % p == 0:
                pts.append((v, w))
    return sorted(set(pts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sweep", "point"])
    ap.add_argument("args", nargs="*", type=int)
    ap.add_argument("--horizon", type=int, default=45)
    a = ap.parse_args()
    if a.mode == "point":
        p, v, w = a.args
        for status, depth, log in walk(p, v, w, a.horizon, trace=True):
            print(f"({v},{w}) mod {p}: {status} at rung {depth}; {log}")
        return
    p = a.args[0]
    pts = quartic_points(p)
    print(f"p={p}: {len(pts)} quartic points")
    from collections import Counter
    deaths = Counter()
    for v, w in pts:
        res = walk(p, v, w, a.horizon)
        best = max(res, key=lambda r: (r[0] == "SURVIVED", r[1]))
        if best[0] == "SURVIVED":
            print(f"SURVIVOR ({v},{w}) mod {p} to rung {a.horizon}; "
                  f"branches={len(res)}; log={best[2]}", flush=True)
        else:
            deaths[best[1]] += 1
            if best[0] in ("MULTIVAR", "BRANCH-CAP"):
                print(f"NOTE ({v},{w}): {best[0]} at rung {best[1]}",
                      flush=True)
    print("death-depth histogram:", dict(sorted(deaths.items())))


if __name__ == "__main__":
    main()
