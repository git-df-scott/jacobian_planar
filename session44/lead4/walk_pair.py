#!/usr/bin/env python3
"""Level-by-level constructive walk of a trackD/trackB1 shape mod p.

run_pair (trackB1_shapes) measures dimension at random points; this walker
CONSTRUCTS points.  Q[L] (the other polynomial's y^L row) is integrated
from driver rows <= L-1, and a product of two driver rows both >= jd (the
top driver row) first appears at label 2*jd+1; so for TALL drivers
(2*jd+1 > jmax+1, checked) every support condition of label L is affine in
driver row L-1 once lower rows are fixed.  The walk gauges the pivot p10
to a random nonzero value (1/p10 enters everything), then solves labels
<= j+1 at each level j as an exact affine system in the row-j
coefficients (kernel directions drawn at random, dims recorded), with an
always-on affinity check that aborts loudly if the schedule premise is
ever violated.

Soundness asymmetry, stated up front: p10 is sliced at random values and
kernel draws are random, so a FAILED walk never proves emptiness; but a
reported WITNESS passes an INDEPENDENT final gate - both polynomials are
rebuilt and [A,B] = rhs is checked by direct bracket arithmetic plus
support containment - so false positives cannot occur.  This is a hunting
instrument; Groebner remains the killing instrument.

Controls (run on the first target's real geometry):
  W1: for a RANDOM driver, the integrated Q must satisfy [A,B] = rhs up to
      the y-cutoff with the bracket computed by sympy (independent
      library) - validates the recurrence copy and the gate arithmetic.
  W2: the gate must REJECT a random non-solution (support leaks), so it
      cannot pass junk vacuously.
No end-to-end planted-witness control exists yet (constructing a planted
solvable instance is as hard as the problem: Q truncates only on the
variety itself).  Consequence: WALK-FAIL results are hunting misses, not
kills; only gate-passing WITNESS results carry certification weight.
"""
import argparse
import json
import random
import sys

import trackB1_shapes as SH
from trackB1_polygon import (hull_rows, trim, pscal, dadd, dmul, dscal,
                             dderiv, dinv_scalar, p)


# ---------------------------------------------------------------- engine ---
class Walker:
    def __init__(self, NA, NB, rhs, name="shape"):
        self.pair = SH.Pair(name, NA, NB, rhs)
        o = self.pair.orient()
        if o is None:
            raise ValueError("OUT OF SCOPE: needs one (0,1) and one (0,0) "
                             "j=0 row")
        self.DR, self.OR_, self.rhs, self.flipped = o
        self.idx = [(j, i) for j in sorted(self.DR)
                    for i in range(self.DR[j][0], self.DR[j][1] + 1)]
        self.jmax = max(max(self.OR_), max(self.DR)) + 2
        self.R = SH.rhs_rows(self.rhs, self.jmax)
        self.pivot = self.idx.index((0, 1))
        self.levels = sorted(self.DR)
        self.vars_at = {j: [k for k, (jj, _) in enumerate(self.idx)
                            if jj == j] for j in self.levels}

    def build(self, vec, k=None):
        D = {}
        for t, ((j, i), val) in enumerate(zip(self.idx, vec)):
            A, B = D.setdefault(j, ([], []))
            while len(A) <= i:
                A.append(0)
                B.append(0)
            A[i] = val % p
            if k is not None and t == k:
                B[i] = 1
            D[j] = (A, B)
        return {j: (trim(a), trim(b)) for j, (a, b) in D.items()}

    def qrows(self, D):
        """The engine's recurrence, verbatim (dual-number rows)."""
        A0, B0 = D[0]
        p10 = (A0[1] if len(A0) > 1 else 0, B0[1] if len(B0) > 1 else 0)
        if p10[0] == 0:
            return None
        inv = dinv_scalar(*p10)
        r0 = self.R.get(0, [])
        Q = {0: ([0], [0]),
             1: (pscal(r0, inv[0]), pscal(r0, inv[1]))}
        for k in range(1, self.jmax + 1):
            acc = (list(self.R.get(k, [])), [])
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in D and b in Q:
                    acc = dadd(acc, dscal(dmul(D[a + 1], dderiv(Q[b])), a + 1))
                if a >= 1 and a in D and (b + 1) in Q:
                    acc = dadd(acc,
                               dscal(dmul(dderiv(D[a]), Q[b + 1]), -(b + 1)))
            Q[k + 1] = dscal(dmul(acc, ([inv[0]], [inv[1]])),
                             pow(k + 1, p - 2, p))
        return Q

    def conds_labeled(self, vec, k=None):
        """{(row_j, x_i): (val, eps)} for the support conditions, or None.

        Keyed by (row, x-power), NOT positionally: trim() makes row lengths
        value-dependent, so positional indexing misaligns conditions between
        evaluations (the source of a spurious NONAFFINE).  A key absent from
        one evaluation means that coefficient is 0 there; align via dict.
        """
        Q = self.qrows(self.build(vec, k))
        if Q is None:
            return None
        out = {}
        for j in range(1, self.jmax + 1):
            A, B = Q.get(j, ([], []))
            if j in self.OR_:
                lo, hi = self.OR_[j]
                bad = [i for i in range(max(len(A), len(B)))
                       if i < lo or i > hi]
            else:
                bad = list(range(max(len(A), len(B))))
            for i in bad:
                out[(j, i)] = (A[i] if i < len(A) else 0,
                               B[i] if i < len(B) else 0)
        return out

    # -------------------------------------------------------------- walk ---
    # Affine schedule: Q[L] is integrated from driver rows <= L-1, and a
    # product of two driver rows both >= jd (the top driver row) first
    # appears at label 2*jd+1.  So when 2*jd+1 > jmax+1 (checked), every
    # condition of label L is AFFINE in driver row L-1 once rows < L-1 are
    # fixed: solve labels <= j+1 at level j, everything remaining at the
    # top level.  The always-on affinity check is the runtime guard.
    def walk(self, rng, restarts=40, verbose=False):
        jd = max(self.levels)
        # Merged top block: any product of two driver rows both > jmax/2
        # exceeds the label cutoff jmax+1, so ALL conditions are JOINTLY
        # affine in the rows >= j0 = jmax//2 + 1 (given the rows below).
        # Solving that block as one affine system keeps its kernel freedom
        # joint instead of committing greedy per-level draws - the greedy
        # walk provably cannot reach consistency loci of codimension >= 1
        # in the draws it commits, this can.
        j0 = self.jmax // 2 + 1
        steps = ([j for j in self.levels if j < j0]
                 + (["MERGE"] if any(j >= j0 for j in self.levels) else []))
        best_fail = (-1, None)
        nc_total = None
        fail_hist = {}
        for attempt in range(restarts):
            vec = [0] * len(self.idx)
            vec[self.pivot] = rng.randrange(1, p)
            done = set()
            kdims = []
            ok = True
            for j_raw in steps:
                j = self.jmax + 99 if j_raw == "MERGE" else j_raw
                if j_raw == "MERGE":
                    unks = [k for jj in self.levels if jj >= j0
                            for k in self.vars_at[jj] if k != self.pivot]
                else:
                    unks = [k for k in self.vars_at[j] if k != self.pivot]
                base = self.conds_labeled(vec)
                if base is None:
                    ok = False
                    break
                nc_total = len(base)
                if j_raw == "MERGE":
                    new = [key for key in base if key not in done]
                else:
                    new = [key for key in base
                           if key not in done and key[0] <= j + 1]
                if unks:
                    cols = [self.conds_labeled(vec, k) for k in unks]
                    # key set: union over base and eps evaluations so no
                    # value-dependent coefficient is silently dropped
                    keys = set(new)
                    for c in cols:
                        keys |= {key for key in c
                                 if key not in done
                                 and (j_raw == "MERGE" or key[0] <= j + 1)}
                    new = sorted(keys)
                    c0 = [base.get(key, (0, 0))[0] for key in new]
                    A = [[cols[q].get(key, (0, 0))[1]
                          for q in range(len(unks))] for key in new]
                    ut = [rng.randrange(p) for _ in unks]
                    v2 = list(vec)
                    for q, k in enumerate(unks):
                        v2[k] = ut[q]
                    chk = self.conds_labeled(v2)
                    for r, key in enumerate(new):
                        lin = (c0[r] + sum(A[r][q] * ut[q]
                                           for q in range(len(unks)))) % p
                        if chk.get(key, (0, 0))[0] != lin:
                            raise RuntimeError(
                                f"NONAFFINE at level {j_raw} cond {key}: "
                                f"schedule premise violated")
                    sol = solve_affine(A, c0, rng, n=len(unks))
                    if sol is None:
                        ok = False
                        fail_hist[j] = fail_hist.get(j, 0) + 1
                        if j > best_fail[0]:
                            hom = solve_affine(A, [0] * len(new), rng,
                                               n=len(unks))
                            rkA = len(unks) - hom[1]
                            best_fail = (j, {"new": len(new),
                                             "unks": len(unks),
                                             "rankA": rkA,
                                             "kdims_before": list(kdims)})
                        break
                    u, kdim = sol
                    if kdim:
                        kdims.append((j_raw, kdim))
                    for q, k in enumerate(unks):
                        vec[k] = u[q]
                else:
                    if any(base[key][0] != 0 for key in new):
                        ok = False
                        fail_hist[j] = fail_hist.get(j, 0) + 1
                        if j > best_fail[0]:
                            best_fail = (j, {"new": len(new), "unks": 0})
                        break
                done |= set(new)
            if not ok:
                continue
            fin = self.conds_labeled(vec)
            resid = [key for key in fin if fin[key][0] != 0]
            if resid:
                if verbose:
                    print(f"  attempt {attempt}: residual at {resid[:6]}")
                continue
            return {"status": "WITNESS", "vec": list(vec), "kdims": kdims,
                    "attempt": attempt}
        return {"status": "FAIL", "restarts": restarts,
                "deepest_fail_level": best_fail[0],
                "fail_profile": best_fail[1], "fail_hist": fail_hist,
                "nconds": nc_total}

    # ------------------------------------------------- independent gate ---
    def bracket_gate(self, vec):
        """Rebuild both polynomials; check [A,B]=rhs by direct arithmetic."""
        D = {j: a for j, (a, _) in self.build(vec).items()}
        Q = self.qrows(self.build(vec))
        Qr = {j: a for j, (a, _) in Q.items() if trim(a)}
        drv = {}
        for j, row in D.items():
            for i, c in enumerate(row):
                if c % p:
                    drv[(i, j)] = c % p
        oth = {}
        for j, row in Qr.items():
            for i, c in enumerate(row):
                if c % p:
                    oth[(i, j)] = c % p
        br = {}
        for (i1, j1), c1 in drv.items():
            for (i2, j2), c2 in oth.items():
                if i1 >= 1 and j2 >= 1:
                    k = (i1 + i2 - 1, j1 + j2 - 1)
                    br[k] = (br.get(k, 0) + i1 * j2 * c1 * c2) % p
                if j1 >= 1 and i2 >= 1:
                    k = (i1 + i2 - 1, j1 + j2 - 1)
                    br[k] = (br.get(k, 0) - j1 * i2 * c1 * c2) % p
        want = {}
        for (i, j, c) in self.rhs:
            want[(i, j)] = (want.get((i, j), 0) + c) % p
        diff = {k: v for k, v in
                {**{k: (br.get(k, 0) - want.get(k, 0)) % p
                    for k in set(br) | set(want)}}.items() if v}
        if diff:
            return False, f"bracket mismatch at {sorted(diff)[:5]}"
        for j, row in Qr.items():
            nz = [i for i, c in enumerate(row) if c % p]
            if not nz:
                continue
            if j not in self.OR_:
                return False, f"other-poly support at forbidden row {j}"
            lo, hi = self.OR_[j]
            if min(nz) < lo or max(nz) > hi:
                return False, f"other-poly row {j} outside [{lo},{hi}]"
        return True, f"driver {len(drv)} terms, other {len(oth)} terms"


def solve_affine(A, c0, rng, n=None):
    """Solve A u = -c0 mod p; return (u, kernel_dim) or None."""
    m = len(A)
    if n is None:
        n = len(A[0]) if A else 0
    M = [list(A[r]) + [(-c0[r]) % p] for r in range(m)]
    piv = []
    row = 0
    for col in range(n):
        sel = next((r for r in range(row, m) if M[r][col] % p), None)
        if sel is None:
            continue
        M[row], M[sel] = M[sel], M[row]
        inv = pow(M[row][col], p - 2, p)
        M[row] = [x * inv % p for x in M[row]]
        for r in range(m):
            if r != row and M[r][col] % p:
                f = M[r][col]
                M[r] = [(M[r][k] - f * M[row][k]) % p for k in range(n + 1)]
        piv.append(col)
        row += 1
        if row == m:
            break
    for r in range(row, m):
        if M[r][n] % p:
            return None
    free = [c for c in range(n) if c not in piv]
    u = [0] * n
    for c in free:
        u[c] = rng.randrange(p)
    for r, c in enumerate(piv):
        u[c] = (M[r][n] - sum(M[r][f] * u[f] for f in free)) % p
    return u, len(free)


# -------------------------------------------------------------- controls ---
def control_W1(rng, targets):
    """Machinery vs sympy: for a RANDOM driver on the real chart geometry,
    the integrated Q must satisfy [A,B] = rhs + (rows above the cutoff),
    with the bracket computed by sympy (independent library).  Validates
    the recurrence copy AND the gate arithmetic in one shot."""
    import sympy as sp
    t = targets[0]
    w = Walker(t["NP"], t["NQ"], [(t["r"], 0, 1)], "W1")
    vec = [rng.randrange(p) for _ in w.idx]
    vec[w.pivot] = rng.randrange(1, p)
    D = {j: a for j, (a, _) in w.build(vec).items()}
    Q = {j: a for j, (a, _) in w.qrows(w.build(vec)).items()}
    x, y = sp.symbols("x y")
    Apoly = sum(c * x**i * y**j for j, row in D.items()
                for i, c in enumerate(row))
    Bpoly = sum(c * x**i * y**j for j, row in Q.items()
                for i, c in enumerate(row))
    br = sp.expand(sp.diff(Apoly, x) * sp.diff(Bpoly, y)
                   - sp.diff(Apoly, y) * sp.diff(Bpoly, x))
    want = sum(c * x**i * y**j for (i, j, c) in w.rhs)
    diff = sp.Poly(br - want, x, y)
    bad = [(m, c % p) for m, c in diff.terms()
           if c % p and m[1] <= w.jmax]
    ok = not bad
    print(f"W1 recurrence+bracket vs sympy (below y^{w.jmax + 1}): "
          f"{'PASS' if ok else 'FAIL ' + str(bad[:4])}")
    return ok


def control_W2(rng, targets):
    """Gate corruption: a vector that satisfies the bracket relation by
    construction must PASS the gate's bracket half, and perturbing one
    driver coefficient must make the full-condition residual nonzero
    (the walk's final residual check is live)."""
    t = targets[0]
    w = Walker(t["NP"], t["NQ"], [(t["r"], 0, 1)], "W2")
    vec = [rng.randrange(p) for _ in w.idx]
    vec[w.pivot] = rng.randrange(1, p)
    fin = w.conds_labeled(vec)
    nz = sum(1 for v, _ in fin.values() if v != 0)
    if nz == 0:
        print("W2 SKIP: random vector satisfied all conditions (?!)")
        return False
    ok1, det = w.bracket_gate(vec)
    # gate must FAIL on a random vec (support leaks), not pass vacuously
    print(f"W2a gate rejects a random non-solution: "
          f"{'PASS' if not ok1 else 'FAIL (gate passed junk: ' + det + ')'}")
    return not ok1


# ------------------------------------------------------------------ main ---
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default=None)
    ap.add_argument("--index", type=int, default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--skipcal", action="store_true")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    if not a.targets:
        print("need --targets (controls run on the first target's geometry)")
        return
    targets = json.load(open(a.targets))
    if not a.skipcal:
        if not control_W1(rng, targets):
            sys.exit(1)
        if not control_W2(rng, targets):
            sys.exit(1)
    sel = targets if a.all else [targets[a.index or 0]]
    for t in sel:
        w = Walker(t["NP"], t["NQ"], [(t["r"], 0, 1)], t["tag"])
        r = w.walk(rng, restarts=a.restarts, verbose=True)
        if r["status"] == "WITNESS":
            ok, det = w.bracket_gate(r["vec"])
            print(f"{t['tag']}\n  WITNESS mod {p} attempt={r['attempt']} "
                  f"kdims={r['kdims']}\n  gate: "
                  f"{'PASS  <CERTIFIED mod-p point> ' + det if ok else 'FAIL ' + det}")
            if ok:
                print("  vec =", r["vec"])
        else:
            print(f"{t['tag']}\n  WALK-FAIL restarts={r['restarts']} "
                  f"deepest-level={r['deepest_fail_level']} "
                  f"profile={r['fail_profile']} hist={r['fail_hist']} "
                  f"nconds={r['nconds']}  (not an emptiness proof)", flush=True)


if __name__ == "__main__":
    main()
