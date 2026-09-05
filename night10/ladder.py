"""night10 -- the ramified pi-ladder over O_e = Z[pi]/(pi^e - 2).

Everything is checked against exact arithmetic in O_e at every accepted level:
after choosing d_m the truncated point is substituted into r and every
component must have w-valuation > m.
"""

import ram
import system as S

CEILING = 12
NODE_BUDGET = 400000


class Ladder:
    def __init__(self, R, n, reval, jeval, x0, ceiling=CEILING):
        self.R = R
        self.n = n
        self.reval = reval
        self.jeval = jeval
        self.x0 = list(x0)
        self.ceiling = ceiling
        # J mod 2 at x0 (constant along the ladder: x_trunc = x0 mod pi)
        J = jeval(x0)
        self.J2 = [[c % 2 for c in row] for row in J]
        self.m_rows = len(self.J2)
        self.rank = ram_rank(self.J2, n)
        self.kernel_basis = ker(self.J2, n)
        self.kernel = span(self.kernel_basis, n)

    def trunc(self, ds):
        R = self.R
        v = [R.from_int(t) for t in self.x0]
        for k, d in ds.items():
            t = [R.from_int(c) for c in d]
            for _ in range(k):
                t = [R.mul_pi(u) for u in t]
            v = [R.add(a, b) for a, b in zip(v, t)]
        return v

    def resid(self, ds):
        return self.reval(self.trunc(ds), self.R)

    def level_data(self, ds, m):
        """Returns (wmin, rho, solvable, solutions) for level m given d_1..d_{m-1}."""
        R = self.R
        res = self.resid(ds)
        ws = [R.w(u) for u in res]
        wm = min(ws)
        assert wm >= m, "invariant broken at level %d: wmin=%d" % (m, wm)
        shifted = [R.div_pi_pow(u, m) for u in res]
        rho = [R.residue(u) for u in shifted]
        ok, part = solve(self.J2, rho, self.n)
        sols = []
        if ok:
            sols = [tuple((a ^ b) for a, b in zip(part, k)) for k in self.kernel]
        return wm, rho, ok, sols

    def run(self, verbose_deaths=1):
        """DFS.  Returns dict with survivor (if any) and death records."""
        deaths = []
        nodes = [0]
        survivor = [None]
        levels_reached = [0]

        def dfs(ds, m):
            if survivor[0] is not None:
                return
            nodes[0] += 1
            if nodes[0] > NODE_BUDGET:
                raise RuntimeError("node budget exceeded")
            wm, rho, ok, sols = self.level_data(ds, m)
            if not ok:
                deaths.append(dict(level=m, ds={k: list(v) for k, v in ds.items()},
                                   rho=rho, wmin=wm,
                                   nonzero_rho_rows=[S.LABELS[i] for i, b in enumerate(rho) if b],
                                   rank_J=self.rank,
                                   rank_aug=ram_rank([r + [rho[i]] for i, r in
                                                      enumerate([list(x) for x in self.J2])],
                                                     self.n + 1)))
                return
            for d in sols:
                ds2 = dict(ds)
                ds2[m] = list(d)
                # independent exact check: residual valuation must exceed m
                res = self.resid(ds2)
                wnew = min(self.R.w(u) for u in res)
                assert wnew > m, "accepted level %d but wmin=%d" % (m, wnew)
                levels_reached[0] = max(levels_reached[0], m)
                if m >= self.ceiling:
                    survivor[0] = dict(level=m, ds={k: list(v) for k, v in ds2.items()},
                                       trunc=[list(u) for u in self.trunc(ds2)],
                                       residual=[list(u) for u in res],
                                       residual_w=[self.R.w(u) if self.R.w(u) < 10**6
                                                   else None for u in res])
                    return
                dfs(ds2, m + 1)
                if survivor[0] is not None:
                    return

        dfs({}, 1)
        return dict(nodes=nodes[0], deaths=deaths, survivor=survivor[0],
                    max_level_reached=levels_reached[0],
                    rank_J_mod2=self.rank, nullity=self.n - self.rank)


# --- small F_2 helpers, dimension-generic (ram.py's are hard-wired to N=9) ---

def rref(rows, ncols):
    rows = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(rows)):
            if rows[i][c] & 1:
                p = i
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] & 1:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], piv


def ram_rank(rows, ncols):
    return len(rref(rows, ncols)[1])


def ker(J, n):
    R, piv = rref(J, n)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = R[i][f] & 1
        basis.append(v)
    return basis


def span(basis, n):
    out = []
    for mask in range(1 << len(basis)):
        v = [0] * n
        for i in range(len(basis)):
            if mask >> i & 1:
                v = [a ^ b for a, b in zip(v, basis[i])]
        out.append(tuple(v))
    return out


def solve(J, b, n):
    aug = [list(J[k]) + [b[k] & 1] for k in range(len(J))]
    R, piv = rref(aug, n + 1)
    if n in piv:
        return False, None
    sol = [0] * n
    for i, c in enumerate(piv):
        sol[c] = R[i][n] & 1
    return True, sol
