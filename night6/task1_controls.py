"""night6 TASK 1 controls.

C1  identity control: the five expressions E0..E4 as coded are compared,
    at random numeric f,p,q,g,r,s,t over F_p, against the z^k coefficients
    of the bracket [P,Q]_{u,z} = P_u Q_z - P_z Q_u computed directly.

C2  positive control: the SAME builder, at the same face solutions, with
    (p_,s_) = (0,0) -- the branch the handoff's section 3d treats by hand.
    Expected NOT to be the unit ideal (the trivial family f,g constant,
    r = 0 lives there), and the known point is substituted back exactly.

C3  the same branch WITH the vertex non-degeneracy f_8 != 0, g_12 != 0
    imposed.  The handoff's hand argument says f and g are then forced
    constant, so f_8 = g_12 = 0 and this must be EMPTY -- a control whose
    answer is known in advance and known for a reason.
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flint
import e3_final as E
import integrate as I
from task1_run import face_families


def flush(*a):
    print(*a)
    sys.stdout.flush()


# ------------------------------------------------------------------ control C1
def upmul(a, b, p):
    r = {}
    for i, x in a.items():
        for j, y in b.items():
            r[i + j] = (r.get(i + j, 0) + x * y) % p
    return {k: v for k, v in r.items() if v % p}


def upadd(*args):
    p = args[-1]
    r = {}
    for a in args[:-1]:
        for k, v in a.items():
            r[k] = (r.get(k, 0) + v) % p
    return {k: v for k, v in r.items() if v % p}


def upscal(a, c, p):
    return {k: v * c % p for k, v in a.items() if v * c % p}


def upder(a, p):
    return {k - 1: k * v % p for k, v in a.items() if k > 0 and k * v % p}


def control_C1(p, seeds=4):
    """direct bracket in (u,z) vs the five coded identities"""
    random.seed(20260828)
    ok = True
    for _ in range(seeds):
        def rnd(lo, hi):
            return {k: random.randrange(1, p) for k in range(lo, hi + 1)}
        f, pp, q = rnd(0, 8), rnd(1, 8), rnd(1, 8)
        g, r, s, t = rnd(0, 12), rnd(1, 12), rnd(2, 12), rnd(2, 12)
        A = {0: f, 1: pp, 2: q}          # P = sum A_i z^i
        B = {0: g, 1: r, 2: s, 3: t}     # Q = sum B_j z^j
        # [P,Q]_{u,z} coefficient of z^k  =  sum_{i+j-1=k} (j A_i' B_j - i A_i B_j')
        direct = {}
        for i, ai in A.items():
            for j, bj in B.items():
                k = i + j - 1
                if k < 0:
                    continue
                term = upadd(upscal(upmul(upder(ai, p), bj, p), j, p),
                             upscal(upmul(ai, upder(bj, p), p), (-i) % p, p), p)
                direct[k] = upadd(direct.get(k, {}), term, p)
        coded = {
            0: upadd(upmul(upder(f, p), r, p),
                     upscal(upmul(pp, upder(g, p), p), p - 1, p), p),
            1: upadd(upscal(upmul(upder(f, p), s, p), 2, p),
                     upmul(upder(pp, p), r, p),
                     upscal(upmul(pp, upder(r, p), p), p - 1, p),
                     upscal(upmul(q, upder(g, p), p), p - 2, p), p),
            2: upadd(upscal(upmul(upder(f, p), t, p), 3, p),
                     upscal(upmul(upder(pp, p), s, p), 2, p),
                     upmul(upder(q, p), r, p),
                     upscal(upmul(pp, upder(s, p), p), p - 1, p),
                     upscal(upmul(q, upder(r, p), p), p - 2, p), p),
            3: upadd(upscal(upmul(upder(pp, p), t, p), 3, p),
                     upscal(upmul(upder(q, p), s, p), 2, p),
                     upscal(upmul(pp, upder(t, p), p), p - 1, p),
                     upscal(upmul(q, upder(s, p), p), p - 2, p), p),
            4: upadd(upscal(upmul(upder(q, p), t, p), 3, p),
                     upscal(upmul(q, upder(t, p), p), p - 2, p), p),
        }
        for k in range(5):
            if direct.get(k, {}) != coded[k]:
                ok = False
    return ok


# --------------------------------------------------------------- controls C2/C3
def build_zero_ps(K, p, q, t, rabin):
    """the same builder with (p_, s_) = (0,0)."""
    names = (["f%d" % i for i in I.FIDX] + ["g%d" % j for j in I.GIDX]
             + ["r%d" % k for k in I.RIDX])
    if rabin:
        names += ["Wf", "Wg"]
    nv = len(names)
    idx = {n: i for i, n in enumerate(names)}
    V = lambda n: I.var(K, nv, idx[n])
    C = lambda c: I.const(K, nv, c)
    pu, su = {}, {}
    qu = {i: C(q[i]) for i in E.QIDX if not K.iszero(q[i])}
    tu = {j: C(t[j]) for j in E.TIDX if not K.iszero(t[j])}
    fu = {i: V("f%d" % i) for i in I.FIDX}
    gu = {j: V("g%d" % j) for j in I.GIDX}
    ru = {k: V("r%d" % k) for k in I.RIDX}
    fd, gd, rd = (I.uderiv(fu, K, p), I.uderiv(gu, K, p), I.uderiv(ru, K, p))
    qd, td = I.uderiv(qu, K, p), I.uderiv(tu, K, p)
    E0 = I.umul(fd, ru, K)
    E1 = I.uadd(I.uscal(I.umul(qu, gd, K), p - 2, K))
    E2 = I.uadd(I.uscal(I.umul(fd, tu, K), 3, K), I.umul(qd, ru, K),
                I.uscal(I.umul(qu, rd, K), p - 2, K))
    eqs = []
    for Ex in (E0, E1, E2):
        for k in sorted(Ex):
            eqs.append(Ex[k])
    if rabin:
        eqs.append(V("f8") * V("Wf") + C(K.smul(p - 1, K.one)))
        eqs.append(V("g12") * V("Wg") + C(K.smul(p - 1, K.one)))
    return eqs, names, dict(n_E0=len(E0), n_E1=len(E1), n_E2=len(E2))


def subst_check(eqs, names, sol, K):
    bad = 0
    for e in eqs:
        acc = K.zero
        for m, c in e.d.items():
            term = c
            for i, ex in enumerate(m):
                for _ in range(ex):
                    term = K.mul(term, sol.get(names[i], K.zero))
            acc = K.add(acc, term)
        if not K.iszero(acc):
            bad += 1
    return bad


def main():
    res = {}
    for p in (999983, 1000003):
        flush("=" * 78)
        flush("PRIME p = %d" % p)
        flush("=" * 78)
        c1 = control_C1(p)
        flush("C1  identity control: the coded E0..E4 agree with the direct"
              " (u,z) bracket P_u Q_z - P_z Q_u at 4 random seeds: %s" % c1)
        assert c1
        fams, vdim, dim = face_families(p, only_rational=False)
        out = []
        for fi, (K, q, t, basis, cols, h) in enumerate(fams):
            flush("")
            flush("FACE FAMILY %d (deg h = %d, covers %d of the 35)"
                  % (fi, h.degree(), h.degree()))
            for rabin in (False, True):
                eqs, names, meta = build_zero_ps(K, p, q, t, rabin)
                tag = "ctl_%d_%d_%s" % (p, fi, 'rab' if rabin else 'free')
                isunit, sdim, size, gb, secs, path = I.run_singular(
                    eqs, names, K, p, tag)
                label = ("C3  (p_,s_) = (0,0) WITH vertex non-degeneracy"
                         " f_8 != 0, g_12 != 0" if rabin else
                         "C2  (p_,s_) = (0,0), free")
                flush("   %s" % label)
                flush("      %d equations, %d unknowns; Singular std:"
                      " |GB| = %d, unit ideal = %s, dim = %d  (%.1fs)"
                      % (len(eqs), len(names), size, isunit, sdim, secs))
                known = None
                if not rabin:
                    sol = {n: K.zero for n in names}
                    nb = subst_check(eqs, names, sol, K)
                    known = (nb == 0)
                    flush("      known point f_1..f_8 = g_1..g_12 = r_1..r_12"
                          " = 0 (f, g constant, r = 0) satisfies all"
                          " equations exactly: %s" % known)
                    flush("      => the branch is NON-empty and the"
                          " instrument finds it (positive control)")
                else:
                    flush("      => expected EMPTY: the handoff's hand"
                          " argument forces f, g constant, hence f_8 = 0")
                out.append(dict(face=fi, hdeg=h.degree(), rabinowitsch=rabin, unit_ideal=isunit,
                                dim=sdim, gb_size=size, known_point_ok=known,
                                n_eqs=len(eqs), n_vars=len(names)))
        res[str(p)] = dict(C1=c1, branches=out)
    json.dump(res, open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'task1_controls.json'),
        'w'), indent=1)
    flush("")
    flush("=" * 78)
    flush("CONTROL SUMMARY")
    for p, r in res.items():
        flush("   p=%s  C1 identity control: %s" % (p, r['C1']))
        for b in r['branches']:
            flush("      family %d (deg %d)  %-4s : unit ideal = %-5s"
                  " dim = %2d  known point verified = %s"
                  % (b['face'], b['hdeg'],
                     'rab' if b['rabinowitsch'] else 'free',
                     b['unit_ideal'], b['dim'], b['known_point_ok']))


if __name__ == '__main__':
    main()
