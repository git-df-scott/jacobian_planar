"""Same as _w0.py but with ONE Gaussian elimination for all right-hand sides.
The previous version re-solved the identical 370x350 system once per condition
(~28 times), which is a 28x waste."""
import sys, random, time
import trackB1_case2_extend as M
import _w0 as W
p, DEG = M.p, M.DEG

def solve_multi(rows, rhss):
    """rows: m x n over K; rhss: list of m-vectors. One RREF, all RHS."""
    m, n = len(rows), len(rows[0])
    nr = len(rhss)
    A = [list(rows[i]) + [rhss[j][i] for j in range(nr)] for i in range(m)]
    piv = {}
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, m) if not M.kis0(A[i][c])), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = M.kinv(A[r][c])
        A[r] = [M.kmul(x, iv) for x in A[r]]
        for i in range(m):
            if i != r and not M.kis0(A[i][c]):
                f = A[i][c]
                A[i] = [M.ksub(A[i][k], M.kmul(f, A[r][k]))
                        for k in range(n + nr)]
        piv[c] = r
        r += 1
    out = []
    for j in range(nr):
        col = n + j
        bad = any(all(M.kis0(A[i][c]) for c in range(n)) and not M.kis0(A[i][col])
                  for i in range(m))
        if bad:
            out.append(None)
            continue
        sol = [M.kzero()] * n
        for c, rr in piv.items():
            sol[c] = A[rr][col]
        out.append(sol)
    return out, len(piv)

if __name__ == "__main__":
    const = int(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
    C, G, BF0, BFb, Kb = W.setup(const)
    t0 = time.time()
    rows, vals = [], []
    need = len(W.MON) + 20
    while len(rows) < need:
        beta = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r = W.w0_resid(C, G, BF0, BFb, Kb, beta, alpha)
        if r is None:
            continue
        rows.append([W.monval(mm, beta, alpha) for mm in W.MON])
        vals.append(r)
    NEQ = max(len(v) for v in vals)
    print(f"evaluations: {len(rows)} pts, {len(W.MON)} monomials, "
          f"{NEQ} conditions [{time.time()-t0:.0f}s]", flush=True)
    rhss = [[(v[w] if w < len(v) else M.kzero()) for v in vals]
            for w in range(NEQ)]
    sols, rank = solve_multi(rows, rhss)
    print(f"one elimination done, rank {rank}/{len(W.MON)} "
          f"[{time.time()-t0:.0f}s]", flush=True)
    if rank < len(W.MON):
        print("  UNDERDETERMINED -- need more points"); sys.exit(1)
    if any(s is None for s in sols):
        print("  INCONSISTENT -- degree bound too low"); sys.exit(1)
    def kstr(e):
        ts = [(f"{e[i]}*a^{i}" if i > 1 else (f"{e[i]}*a" if i == 1 else f"{e[i]}"))
              for i in range(DEG) if e[i]]
        return "(" + "+".join(ts) + ")" if ts else "0"
    out = []
    for cf in sols:
        terms = []
        for c, (b, a) in zip(cf, W.MON):
            if M.kis0(c):
                continue
            s = kstr(c)
            for i in b:
                s += f"*b({i+1})"
            for i in a:
                s += f"*al({i+1})"
            terms.append(s)
        out.append("+".join(terms) if terms else "0")
    out = [o for o in out if o != "0"]
    open(f"_w0_{const}.txt", "w").write(",\n".join(out))
    print(f"[wrote _w0_{const}.txt : {len(out)} nonzero conditions "
          f"[{time.time()-t0:.0f}s]]")
