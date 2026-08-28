"""Night 6 -- E3 kernel computation (main driver).

Face equation (brief's form):   2*q*t' - 3*q'*t = u^2
  q supported u^1..u^8, gauge q_1 = q_8 = 1;  t supported u^2..u^12.
  Coefficient of u^(n-1), n = i+j:  sum_{i+j=n} (2j-3i) q_i t_j = [n==3].
  n runs 3..20; the n=20 row vanishes identically  ->  17 equations,
  17 unknowns (q_2..q_7, t_2..t_12).

E3 operator:  E3(p_,s_) = 3*p_'*t + 2*q'*s_ - p_*t' - 2*q*s_'
  p_ supported u^1..u^8 (8 cols), s_ supported u^2..u^12 (11 cols).
  Coefficient of u^(n-1): sum_{i+j=n} (3i-j) p_i t_j + sum_{i+j=n} (2i-2j) q_i s_j
  n runs 3..20 -> 18 rows.  Matrix is 18 x 19.

Solving route: write q = u*A (deg A = 7), t = u^2*B (deg B = 10); the face
equation becomes  sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m==0], m = 0..17
(m=17 identically zero).  Gauge group: A->cA, B->B/c and u->lambda*u
(A_k->lambda^k A_k, B_k->lambda^k B_k).  The brief's gauge A_0=A_7=1 keeps
the residual mu_7 (lambda^7=1); the gauge A_0=A_1=1 kills it, so its
solution set is the mu_7 quotient.  Points are transported back to
A_0=A_7=1 by lambda^7 = 1/A_7 (a bijection on F_p^* since 7 does not
divide p-1 for either prime), and then RE-VERIFIED from scratch in the
brief's gauge.
"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import fpgb as gb

QIDX = list(range(1, 9))
TIDX = list(range(2, 13))
PIDX = list(range(1, 9))
SIDX = list(range(2, 13))


def flush(*a):
    print(*a)
    sys.stdout.flush()


# --------------------------------------------------- (A,B) system construction
def build_AB(nv, p, Avars):
    """Avars: dict k->poly (k=0..7).  Eliminate B_0..B_10, return residuals."""
    one = {(0,) * nv: 1}
    assert Avars[0] == one
    B = {}
    for m in range(0, 11):
        c0 = (1 + 2 * m) % p
        acc = dict(one) if m == 0 else {}
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = (1 + 2 * j - 3 * i) % p
            if c:
                term = gb.pmul(Avars[i], B[j], p)
                acc = gb.padd(acc, {k: (-c * v) % p for k, v in term.items()}, p)
        inv = pow(c0, p - 2, p)
        B[m] = {k: v * inv % p for k, v in acc.items()}
    res = []
    for m in range(11, 18):
        acc = {}
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = (1 + 2 * j - 3 * i) % p
                if c:
                    term = gb.pmul(Avars[i], B[j], p)
                    acc = gb.padd(acc, {k: c * v % p for k, v in term.items()}, p)
        res.append(acc)
    assert res[-1] == {}, "m=17 row is not identically zero"
    return B, res[:-1]


def face_residual_qt(qv, tv, p):
    res = {}
    for i, qi in qv.items():
        for j, tj in tv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (2 * j - 3 * i) * qi * tj) % p
    res[2] = (res.get(2, 0) - 1) % p
    return {k: v for k, v in res.items() if v % p}


def count_face_equations(p):
    """Independent count in the brief's own gauge: 17 equations / 17 unknowns."""
    eqs, unknowns = 0, set()
    for n in range(3, 21):
        terms = [(i, n - i) for i in QIDX if (n - i) in TIDX]
        terms = [(i, j) for i, j in terms if (2 * j - 3 * i) % p]
        if n == 20:
            assert all((2 * j - 3 * i) % p == 0 for i in QIDX
                       for j in [20 - i] if j in TIDX)
            continue
        eqs += 1
    unknowns = len(range(2, 8)) + len(TIDX)
    return eqs, unknowns


# -------------------------------------------------------------- E3 (as spec'd)
def e3_matrix(qv, tv, p, s_min=2):
    sidx = list(range(s_min, 13))
    cols = [('p', i) for i in PIDX] + [('s', j) for j in sidx]
    # n = i+j:  p_i t_j gives n in 3..20;  q_i s_j gives n in (1+s_min)..20
    ns = list(range(min(3, 1 + s_min), 21))
    M = [[0] * len(cols) for _ in ns]
    for ri, n in enumerate(ns):
        for ci, (kind, k) in enumerate(cols):
            if kind == 'p':
                i, j = k, n - k
                if j in TIDX:
                    M[ri][ci] = ((3 * i - j) * tv[j]) % p
            else:
                j, i = k, n - k
                if i in QIDX:
                    M[ri][ci] = ((2 * i - 2 * j) * qv[i]) % p
    keep = [ri for ri in range(len(ns)) if any(M[ri])] if False else list(range(len(ns)))
    return M, cols, ns


def nullspace_mod(M, p):
    return gb.nullspace(M, p)


def rank_mod(M, p):
    m, n = len(M), len(M[0])
    A = [row[:] for row in M]
    r = 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if A[rr][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for rr in range(r + 1, m):
            if A[rr][c] % p:
                f = A[rr][c]
                A[rr] = [(a - f * b) % p for a, b in zip(A[rr], A[r])]
        r += 1
        if r == m:
            break
    return r


def verify_e3(vec, cols, qv, tv, p):
    pv, sv = {}, {}
    for val, (kind, k) in zip(vec, cols):
        (pv if kind == 'p' else sv)[k] = val % p
    res = {}
    for i, pi in pv.items():
        for j, tj in tv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (3 * i - j) * pi * tj) % p
    for i, qi in qv.items():
        for j, sj in sv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (2 * i - 2 * j) * qi * sj) % p
    return {k: v for k, v in res.items() if v % p}, pv, sv


def polystr(d, name):
    ts = [("%d*u^%d" % (v, k)) for k, v in sorted(d.items()) if v % 1000003 or v]
    ts = [("%d*u^%d" % (v, k)) for k, v in sorted(d.items()) if v]
    return name + " = " + (" + ".join(ts) if ts else "0")


# ------------------------------------------------------------------- transport
def transport(A7vals, p):
    lamexp = pow(7, -1, p - 1)
    A7 = A7vals[7]
    lam = pow(pow(A7, p - 2, p), lamexp, p)
    assert pow(lam, 7, p) == pow(A7, p - 2, p)
    At = {k: pow(lam, k, p) * A7vals[k] % p for k in range(8)}
    assert At[0] == 1 and At[7] == 1
    Av = {k: ({(): At[k]} if At[k] % p else {}) for k in range(8)}
    Av[0] = {(): 1}
    B, res = build_AB(0, p, Av)
    for e in res:
        assert e == {}, ("transported point fails residual eq", e)
    qv = {i: At[i - 1] for i in QIDX}
    tv = {j: B[j - 2].get((), 0) % p for j in TIDX}
    return qv, tv


# ------------------------------------------------------------------------ main
def run_prime(p):
    flush("=" * 74)
    flush("PRIME p = %d      7 | p-1 ?  %s" % (p, (p - 1) % 7 == 0))
    flush("=" * 74)
    ne, nu = count_face_equations(p)
    flush("STEP 1  face system in the gauge q_1 = q_8 = 1:")
    flush("        %d equations (u^2..u^18 of 2qt'-3q't-u^2; the u^19 row is"
          " identically zero), %d unknowns (q_2..q_7, t_2..t_12)" % (ne, nu))
    assert (ne, nu) == (17, 17)

    # ---- solve on the mu_7 quotient (gauge A_0 = A_1 = 1)
    t0 = time.time()
    nv = 6
    Av = {0: {(0,) * nv: 1}, 1: {(0,) * nv: 1}}
    for k in range(2, 8):
        e = [0] * nv
        e[k - 2] = 1
        Av[k] = {tuple(e): 1}
    B, res = build_AB(nv, p, Av)
    flush("        mu_7-quotient gauge A_0=A_1=1 (A_k = q_{k+1}, B_k = t_{k+2}):"
          " %d residual equations in A_2..A_7, total degrees %s"
          % (len(res), [max(sum(m) for m in e) for e in res]))
    G = gb.buchberger(res, p)
    flush("        grevlex Groebner basis: %d elements, leading monomials %s"
          % (len(G), [gb.lm(g) for g in G]))
    qb = gb.quotient_basis(G, nv)
    flush("        quotient ring dimension over F_p: %d  (basis %s)"
          % (len(qb), qb))
    pts, n, cpdeg = gb.solve_zero_dim(G, nv, p, None)
    flush("        F_p-rational points of the quotient system: %d  (%.1fs)"
          % (len(pts), time.time() - t0))

    # ---- transport back and verify in the brief's gauge
    faces = []
    for pt in pts:
        A = {0: 1, 1: 1}
        for k in range(2, 8):
            A[k] = pt[k - 2]
        qv, tv = transport(A, p)
        bad = face_residual_qt(qv, tv, p)
        assert not bad, ("FACE VERIFICATION FAILED", qv, tv, bad)
        assert qv[1] == 1 and qv[8] == 1
        assert tv[2] % p and tv[12] % p, "t_2 or t_12 vanishes"
        faces.append((qv, tv))
    faces.sort(key=lambda ft: [ft[0][i] for i in QIDX])
    flush("        face solutions in the gauge q_1=q_8=1, each VERIFIED by exact"
          " substitution (2qt'-3q't-u^2 == 0 mod p) with t_2 != 0, t_12 != 0: %d"
          % len(faces))

    # ---- E3 kernels
    flush("")
    flush("STEP 2/3  E3 kernel per face solution")
    recs = []
    for si, (qv, tv) in enumerate(faces):
        M, cols, ns = e3_matrix(qv, tv, p)
        rank = rank_mod(M, p)
        basis = nullspace_mod(M, p)
        Mx, colsx, nsx = e3_matrix(qv, tv, p, s_min=1)
        rankx = rank_mod(Mx, p)
        basisx = nullspace_mod(Mx, p)
        flush("-" * 70)
        flush("face #%d" % si)
        flush("   q coefficients q_1..q_8   = %s" % [qv[i] for i in QIDX])
        flush("   t coefficients t_2..t_12  = %s" % [tv[j] for j in TIDX])
        flush("   support-restricted E3 (p_: u^1..u^8, s_: u^2..u^12)")
        flush("      matrix %d x %d (rows u^%d..u^%d)  rank = %d  kernel dim = %d"
              % (len(M), len(M[0]), ns[0] - 1, ns[-1] - 1, rank, len(basis)))
        kb = []
        for b in basis:
            bad, pvv, svv = verify_e3(b, cols, qv, tv, p)
            assert not bad, ("kernel vector fails E3", bad)
            flush("      kernel basis vector, VERIFIED E3 == 0 mod p:")
            flush("        %s" % polystr({k: v for k, v in pvv.items() if v}, "p_"))
            flush("        %s" % polystr({k: v for k, v in svv.items() if v}, "s_"))
            kb.append([int(x) for x in b])
        flush("   reference: same operator with s_ allowed from u^1 (20 cols)")
        flush("      matrix %d x %d  rank = %d  kernel dim = %d"
              % (len(Mx), len(Mx[0]), rankx, len(basisx)))
        # is (0, c*q) in the u^1-relaxed kernel?
        v0 = [0] * len(colsx)
        for ci, (kind, k) in enumerate(colsx):
            if kind == 's' and k in qv:
                v0[ci] = qv[k] % p
        bad0, _, _ = verify_e3(v0, colsx, qv, tv, p)
        flush("      (p_, s_) = (0, q) lies in that relaxed kernel: %s"
              % (not bad0))
        recs.append(dict(q=[qv[i] for i in QIDX], t=[tv[j] for j in TIDX],
                         shape=[len(M), len(M[0])], rank=rank,
                         kerdim=len(basis), kernel=kb,
                         cols=[k + str(i) for k, i in cols],
                         relaxed=dict(shape=[len(Mx), len(Mx[0])], rank=rankx,
                                      kerdim=len(basisx),
                                      kernel=[[int(x) for x in b] for b in basisx],
                                      zero_q_in_kernel=(not bad0))))
    return recs


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'night6/e3_kernel_results.json'
    results = {}
    for p in (999983, 1000003):
        results[str(p)] = run_prime(p)
        flush("")
    json.dump(results, open(out, 'w'), indent=1)
    flush("=" * 74)
    flush("STEP 4  cross-prime comparison")
    for p in results:
        flush("  p=%s : %d face solutions, restricted kernel dims %s,"
              " relaxed kernel dims %s"
              % (p, len(results[p]), [r['kerdim'] for r in results[p]],
                 [r['relaxed']['kerdim'] for r in results[p]]))
    a = sorted(r['kerdim'] for r in results['999983'])
    b = sorted(r['kerdim'] for r in results['1000003'])
    flush("  multisets of restricted kernel dimensions agree: %s" % (a == b))
    flush("wrote " + out)
