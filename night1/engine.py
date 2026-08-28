#!/usr/bin/env python3
"""
night1/engine.py -- deformation depth-map engine for JC2 (plane Jacobian
conjecture), session "night1".

METHOD
At a polynomial automorphism F=(P,Q) with [P,Q]=1, every first-order Keller
deformation is X_g(F) for a Hamiltonian g(u,v):
    a1 = g_v(P,Q),  b1 = -g_u(P,Q)
(the identity: writing a=A(P,Q), b=B(P,Q), the linearization
L(a,b) = [a,Q]+[P,b] equals (A_u+B_v)(P,Q), so ker L = divergence-free
directions = Hamiltonian fields composed with F).

Under a hard degree cap d, continue order by order in t:
    L(a_k,b_k) = -sum_{i+j=k, 0<i,j<k} [a_i,b_j]
Each step is a linear solve in the space of pairs of degree <= d.  The DEPTH
of a cell (F,g,d) is the highest k reached before the system obstructs.

CALIBRATION ROWS (not data -- controls): g depending on one variable only
(shears) and quadratic g (linear symplectic flows) have flows polynomial in t
with bounded degree, so their towers MUST survive to K_MAX.  Any obstruction
there is an engine bug, and the run aborts.

DETERMINISM: basis columns ordered by ascending total degree; particular
solutions take free variables = 0, so towers are reproducible bit-for-bit.

All arithmetic over F_p (report results as modular, always).
"""
import argparse, csv, itertools, json, os, sys
import numpy as np

# ---------- polynomial arithmetic: dict {(i,j): int mod p} ----------

def pnorm(a, p):
    return {k: v % p for k, v in a.items() if v % p}

def padd(a, b, p):
    r = dict(a)
    for k, v in b.items():
        r[k] = (r.get(k, 0) + v) % p
    return {k: v for k, v in r.items() if v}

def pmul(a, b, p):
    r = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            k = (i1 + i2, j1 + j2)
            r[k] = (r.get(k, 0) + v1 * v2) % p
    return {k: v for k, v in r.items() if v}

def pscale(a, c, p):
    c %= p
    return {k: (v * c) % p for k, v in a.items() if (v * c) % p}

def pdiff(a, var, p):
    r = {}
    for (i, j), v in a.items():
        if var == 0 and i > 0:
            r[(i - 1, j)] = (v * i) % p
        elif var == 1 and j > 0:
            r[(i, j - 1)] = (v * j) % p
    return {k: v for k, v in r.items() if v}

def bracket(a, b, p):
    """[a,b] = a_x b_y - a_y b_x"""
    t1 = pmul(pdiff(a, 0, p), pdiff(b, 1, p), p)
    t2 = pmul(pdiff(a, 1, p), pdiff(b, 0, p), p)
    return padd(t1, pscale(t2, -1, p), p)

def pdeg(a):
    return max((i + j for i, j in a), default=-1)

def ppow(a, n, p, cache):
    if n == 0:
        return {(0, 0): 1}
    if n in cache:
        return cache[n]
    r = pmul(ppow(a, n - 1, p, cache), a, p)
    cache[n] = r
    return r

def subst(g, P, Q, p, cp, cq):
    """evaluate g(u,v) at u=P, v=Q; cp/cq are power caches for P/Q."""
    r = {}
    for (m, n), c in g.items():
        term = pscale(pmul(ppow(P, m, p, cp), ppow(Q, n, p, cq), p), c, p)
        r = padd(r, term, p)
    return r

# ---------- automorphism library (compositions of elementary maps) ----------
# spec: list of ("U", phi) meaning (x, y+phi(x)) or ("L", psi) meaning
# (x+psi(y), y); phi/psi given as {exponent: coeff}.  Composition applied
# left-to-right.  Jacobian of every elementary map is 1, so [P,Q]=1.

def build_auto(spec, p):
    P, Q = {(1, 0): 1}, {(0, 1): 1}
    for kind, phi in spec:
        if kind == "U":          # post-compose with (u, v + phi(u))
            add = {}
            cp = {}
            for e, c in phi.items():
                add = padd(add, pscale(ppow(P, e, p, cp), c, p), p)
            Q = padd(Q, add, p)
        elif kind == "L":        # post-compose with (u + psi(v), v)
            add = {}
            cq = {}
            for e, c in phi.items():
                add = padd(add, pscale(ppow(Q, e, p, cq), c, p), p)
            P = padd(P, add, p)
        else:
            raise ValueError(kind)
    return P, Q

AUTOS = {
    # name: spec.  degrees noted for orientation.
    "Fa": [("U", {2: 1}), ("L", {2: 1})],                 # P deg 4, Q deg 2
    "Fb": [("U", {2: 1}), ("L", {2: 1}), ("U", {3: 1})],  # longer composition
    "Fc": [("U", {3: 1}), ("L", {2: 1})],                 # P deg 6, Q deg 3
    "Fid": [],                                            # identity baseline
}

def check_keller(P, Q, p):
    br = bracket(P, Q, p)
    return br == {(0, 0): 1}

# ---------- linear algebra mod p (numpy int64; p^2 < 2^63) ----------

def monomials(d):
    """total degree <= d, sorted by (degree, i) -- ascending degree ordering
    makes free-vars-zero particular solutions low-degree-preferring."""
    return sorted(((i, j) for i in range(d + 1) for j in range(d + 1 - i)),
                  key=lambda m: (m[0] + m[1], m[0]))

class LSystem:
    """The operator L(a,b) = [a,Q]+[P,b] on pairs of degree <= d, with RREF
    and transform for repeated solves."""

    def __init__(self, P, Q, d, p):
        self.P, self.Q, self.d, self.p = P, Q, d, p
        self.dout = d + max(pdeg(P), pdeg(Q)) - 2
        self.cols_basis = [("a", m) for m in monomials(d)] + \
                          [("b", m) for m in monomials(d)]
        self.rows_basis = monomials(max(self.dout, 0))
        self.row_index = {m: i for i, m in enumerate(self.rows_basis)}
        nr, nc = len(self.rows_basis), len(self.cols_basis)
        A = np.zeros((nr, nc), dtype=np.int64)
        for ci, (which, m) in enumerate(self.cols_basis):
            e = {m: 1}
            img = bracket(e, Q, p) if which == "a" else bracket(P, e, p)
            for mm, v in img.items():
                A[self.row_index[mm], ci] = v
        self.A = A
        self._rref()

    def _rref(self):
        p = self.p
        R = self.A.copy()
        nr, nc = R.shape
        T = np.eye(nr, dtype=np.int64)
        pivots = []
        r = 0
        for c in range(nc):
            if r >= nr:
                break
            nz = np.nonzero(R[r:, c])[0]
            if len(nz) == 0:
                continue
            i = r + nz[0]
            if i != r:
                R[[r, i]] = R[[i, r]]
                T[[r, i]] = T[[i, r]]
            inv = pow(int(R[r, c]), p - 2, p)
            R[r] = (R[r] * inv) % p
            T[r] = (T[r] * inv) % p
            col = R[:, c].copy()
            col[r] = 0
            mask = col != 0
            if mask.any():
                R[mask] = (R[mask] - np.outer(col[mask], R[r])) % p
                T[mask] = (T[mask] - np.outer(col[mask], T[r])) % p
            pivots.append((r, c))
            r += 1
        self.R, self.T, self.pivots = R, T, pivots
        self.rank = len(pivots)
        self.zero_rows = list(range(self.rank, nr))
        self.kernel_dim = nc - self.rank

    def pair_to_vec(self, a, b):
        v = np.zeros(len(self.cols_basis), dtype=np.int64)
        idx = {cb: i for i, cb in enumerate(self.cols_basis)}
        for m, c in a.items():
            v[idx[("a", m)]] = c
        for m, c in b.items():
            v[idx[("b", m)]] = c
        return v

    def poly_to_rhs(self, poly):
        """None if poly has monomials outside the target space (automatic
        obstruction by degree overflow)."""
        v = np.zeros(len(self.rows_basis), dtype=np.int64)
        for m, c in poly.items():
            if m not in self.row_index:
                return None
            v[self.row_index[m]] = c
        return v

    def apply(self, a, b):
        v = self.pair_to_vec(a, b)
        return (self.A @ v) % self.p

    def solve(self, rhs):
        """particular solution with free vars = 0, or None if inconsistent."""
        p = self.p
        y = (self.T @ rhs) % p
        if any(int(y[r]) for r in self.zero_rows):
            return None
        x = np.zeros(self.A.shape[1], dtype=np.int64)
        for r, c in self.pivots:
            x[c] = y[r]
        return x

    def vec_to_pair(self, x):
        a, b = {}, {}
        for ci, (which, m) in enumerate(self.cols_basis):
            v = int(x[ci]) % self.p
            if v:
                (a if which == "a" else b)[m] = v
        return a, b

# ---------- the tower ----------

def direction(g, P, Q, p):
    """(a1,b1) = X_g(P,Q) for Hamiltonian g(u,v) = dict {(m,n): c}."""
    cp, cq = {}, {}
    gv = {(m, n - 1): (c * n) % p for (m, n), c in g.items() if n > 0}
    gu = {(m - 1, n): (c * m) % p for (m, n), c in g.items() if m > 0}
    a1 = subst(gv, P, Q, p, cp, cq)
    b1 = pscale(subst(gu, P, Q, p, cp, cq), -1, p)
    return a1, b1

def run_tower(sys_, g, kmax, record=False):
    """returns dict: depth (highest k solved), status, and optionally tower."""
    P, Q, p, d = sys_.P, sys_.Q, sys_.p, sys_.d
    a1, b1 = direction(g, P, Q, p)
    if not a1 and not b1:
        return {"depth": 0, "status": "zero-direction"}
    if pdeg(a1) > d or pdeg(b1) > d:
        return {"depth": 0, "status": "direction-exceeds-cap"}
    # sanity: first order must be in the kernel (the structural identity)
    if int((sys_.apply(a1, b1) % p).any()):
        return {"depth": 0, "status": "IDENTITY-VIOLATED"}  # engine bug trap
    A = {1: a1}
    B = {1: b1}
    tower = {"1": {"a": list(map(list, a1.keys())), }} if record else None
    for k in range(2, kmax + 1):
        rhs_poly = {}
        for i in range(1, k):
            j = k - i
            rhs_poly = padd(rhs_poly, pscale(bracket(A[i], B[j], p), -1, p), p)
        if not rhs_poly:
            A[k], B[k] = {}, {}
            continue
        rhs = sys_.poly_to_rhs(rhs_poly)
        if rhs is None:
            return {"depth": k - 1, "status": f"obstructed@{k}:degree-overflow",
                    "tower": _dump_tower(A, B) if record else None}
        x = sys_.solve(rhs)
        if x is None:
            return {"depth": k - 1, "status": f"obstructed@{k}:inconsistent",
                    "tower": _dump_tower(A, B) if record else None}
        A[k], B[k] = sys_.vec_to_pair(x)
    return {"depth": kmax, "status": "survived",
            "tower": _dump_tower(A, B) if record else None}

def _dump_tower(A, B):
    enc = lambda poly: {f"{i},{j}": v for (i, j), v in poly.items()}
    return {str(k): {"a": enc(A[k]), "b": enc(B[k])} for k in A}

def verify_tower_independent(P, Q, A, B, kmax, p):
    """Independent check reusing NO linear algebra: multiply out
    [P + sum t^k a_k, Q + sum t^k b_k] directly and confirm t^1..t^kmax
    coefficients all vanish.  Used on any surviving/deep tower."""
    terms = {0: (P, Q)}
    for k in A:
        terms[k] = (A[k], B[k])
    for k in range(1, kmax + 1):
        coef = {}
        for i, (ai, _) in terms.items():
            j = k - i
            if j in terms:
                coef = padd(coef, bracket(terms[i][0], terms[j][1], p), p)
        if coef:
            return False
    return True

# ---------- calibration / controls ----------

def hamiltonian_grid(gmax):
    """monomial Hamiltonians u^m v^n, 1 <= m+n <= gmax.
    Calibrated (provably-polynomial flow => must survive):
      - single-variable g (shear flows), any degree
      - all quadratics (linear symplectic flows)
    Everything else is a live probe."""
    out = []
    for m in range(gmax + 1):
        for n in range(gmax + 1 - m):
            if m + n < 1:
                continue
            calibrated = (m == 0 or n == 0 or m + n <= 2)
            out.append(((m, n), calibrated))
    return out

def run_controls(p, verbose=True):
    ok = True
    msgs = []
    # Control K: every X_g(F) fitting the cap must lie in ker L, and
    # kernel_dim must be >= the count of such independent directions.
    P, Q = build_auto(AUTOS["Fa"], p)
    assert check_keller(P, Q, p)
    d = 10
    sys_ = LSystem(P, Q, d, p)
    count = 0
    for (m, n), _cal in hamiltonian_grid(4):
        a1, b1 = direction({(m, n): 1}, P, Q, p)
        if (a1 or b1) and pdeg(a1) <= d and pdeg(b1) <= d:
            count += 1
            if int((sys_.apply(a1, b1)).any()):
                ok = False
                msgs.append(f"CONTROL-K FAIL: X_g not in kernel, g=u^{m}v^{n}")
    if sys_.kernel_dim < count:
        ok = False
        msgs.append(f"CONTROL-K FAIL: kernel_dim {sys_.kernel_dim} < {count}")
    else:
        msgs.append(f"CONTROL-K PASS: {count} directions in kernel, "
                    f"kernel_dim={sys_.kernel_dim}")
    # Control P: quadratic g (linear flow) and shear g must survive.
    for gname, g in [("uv", {(1, 1): 1}), ("u^3", {(3, 0): 1})]:
        r = run_tower(sys_, g, kmax=10)
        if r["status"] != "survived":
            ok = False
            msgs.append(f"CONTROL-P FAIL: calibrated g={gname} -> {r}")
        else:
            msgs.append(f"CONTROL-P PASS: g={gname} survived to 10")
    # Control N: an engineered provable obstruction.  Choose g so that
    # deg X_g(F) == d exactly; then deg[a1,b1] can exceed dout, and if its
    # top form is nonzero the obstruction at order 2 is a theorem
    # (degree count), not an opinion.  Engine must report exactly that.
    found = False
    for (m, n), _cal in hamiltonian_grid(5):
        if m == 0 or n == 0 or m + n <= 2:
            continue
        a1, b1 = direction({(m, n): 1}, P, Q, p)
        dd = max(pdeg(a1), pdeg(b1))
        if dd < 4:
            continue
        s2 = LSystem(P, Q, dd, p)
        br = bracket(a1, b1, p)
        if br and pdeg(br) > s2.dout:
            found = True
            r = run_tower(s2, {(m, n): 1}, kmax=6)
            if r["depth"] == 1 and "degree-overflow" in r["status"]:
                msgs.append(f"CONTROL-N PASS: g=u^{m}v^{n}, cap={dd}: provable "
                            f"obstruction at 2 reported ({r['status']})")
            else:
                ok = False
                msgs.append(f"CONTROL-N FAIL: expected obstruction@2, got {r}")
            break
    if not found:
        msgs.append("CONTROL-N SKIP: no engineered overflow found in scan "
                    "(weakens the suite; widen the scan)")
    if verbose:
        for m_ in msgs:
            print(m_)
    return ok, msgs

# ---------- grid runner ----------

def run_grid(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, spec["name"] + ".csv")
    deep_dir = os.path.join(outdir, spec["name"] + "_towers")
    kmax = spec.get("kmax", 12)
    deep_threshold = spec.get("deep_threshold", 6)
    rows_written = 0
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["F", "g", "calibrated", "d", "p", "kernel_dim",
                    "depth", "status", "indep_check"])
        for p in spec["primes"]:
            ok, _ = run_controls(p, verbose=False)
            if not ok:
                print(f"ABORT: controls failed at p={p}; no data written")
                sys.exit(1)
            for Fname in spec["autos"]:
                P, Q = build_auto(AUTOS[Fname], p)
                if not check_keller(P, Q, p):
                    print(f"ABORT: {Fname} not Keller at p={p}")
                    sys.exit(1)
                for d in spec["caps"]:
                    if d < max(pdeg(P), pdeg(Q)):
                        continue
                    sys_ = LSystem(P, Q, d, p)
                    for (m, n), cal in hamiltonian_grid(spec["gmax"]):
                        g = {(m, n): 1}
                        rec = run_tower(sys_, g, kmax,
                                        record=True)
                        indep = ""
                        if rec.get("tower") and (rec["status"] == "survived"
                                                 or rec["depth"] >= deep_threshold):
                            Adec, Bdec = _decode_tower(rec["tower"], p)
                            indep = "PASS" if verify_tower_independent(
                                P, Q, Adec, Bdec, rec["depth"], p) else "FAIL"
                            os.makedirs(deep_dir, exist_ok=True)
                            fn = f"{Fname}_g{m}-{n}_d{d}_p{p}.json"
                            with open(os.path.join(deep_dir, fn), "w") as tf:
                                json.dump(rec["tower"], tf)
                        if cal and rec["status"] != "survived" \
                                and rec["status"] != "direction-exceeds-cap" \
                                and rec["status"] != "zero-direction":
                            print(f"ABORT: calibrated cell died: {Fname} "
                                  f"g=u^{m}v^{n} d={d} p={p}: {rec['status']}")
                            sys.exit(1)
                        w.writerow([Fname, f"u^{m}v^{n}", int(cal), d, p,
                                    sys_.kernel_dim, rec["depth"],
                                    rec["status"], indep])
                        rows_written += 1
                    fh.flush()
                print(f"done: {Fname} p={p} ({rows_written} rows so far)")
    print(f"GRID COMPLETE: {rows_written} rows -> {csv_path}")

def _decode_tower(tw, p):
    dec = lambda enc: {tuple(map(int, k.split(","))): v
                       for k, v in enc.items()}
    A = {int(k): dec(v["a"]) for k, v in tw.items()}
    B = {int(k): dec(v["b"]) for k, v in tw.items()}
    return A, B

# ---------- cli ----------

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["controls", "grid"])
    ap.add_argument("--spec", help="path to grid spec json")
    ap.add_argument("--out", default="night1/results")
    ap.add_argument("--prime", type=int, default=999983)
    args = ap.parse_args()
    if args.cmd == "controls":
        ok, _ = run_controls(args.prime)
        print("CONTROLS:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    else:
        with open(args.spec) as fh:
            spec = json.load(fh)
        run_grid(spec, args.out)
