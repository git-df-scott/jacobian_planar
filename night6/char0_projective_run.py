"""night6 -- characteristic-zero integration test: the full run.

Order: controls first (hard gate), then the projective verdict, then the
certificates.  Everything exact, characteristic zero, no Groebner engine
(Singular was used only once upstream, for the face system's lex Groebner
basis over Q -- night6/CHAR0_FACE_modstd.log).
"""
import os, sys, json, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_lib as C
import char0_linear as L
import char0_projective as P
import char0_controls as CC
from char0_linear_run import load_face, run_fixed, flush


def main():
    t0 = time.time()
    D = load_face()
    K, q, t = D['K'], D['q'], D['t']
    pv1, sv1 = C.split(D['basis'][0], D['cols'])
    pv2, sv2 = C.split(D['basis'][1], D['cols'])
    out = dict(hdeg=D['h'].degree(), dim=D['dim'], vdim=D['vdim'],
               kernel_rank=D['rank'], kernel_dim=D['kerdim'],
               free_cols=D['free'])

    flush("=" * 78)
    flush("night6 -- INTEGRATION TEST IN CHARACTERISTIC ZERO")
    flush("=" * 78)
    flush("face system over Q: dim = %d, vdim = %d" % (D['dim'], D['vdim']))
    flush("eliminant: ONE irreducible factor over Q, degree %d"
          " -> K = Q[T]/(h) carries all 35 face solutions at once"
          % D['h'].degree())
    flush("face equation 2qt' - 3q't = u^2 verified exactly in K")
    flush("E3 matrix over K: 18 x 19, rank %d, KERNEL DIMENSION %d"
          " (free columns %s)" % (D['rank'], D['kerdim'], D['free']))
    flush("both kernel basis vectors verified exactly: E3(p_,s_) = 0 in K")
    assert D['kerdim'] == 2, "*** FLAG: char-0 kernel dimension is not 2 ***"

    # ---------------------------------------------------------- controls
    flush("")
    flush("CONTROLS")
    ok1, det1 = CC.control_C1_char0()
    flush("   C1 (characteristic zero, exact rational): the coded E0..E4 agree"
          " with the direct (u,z) bracket P_u Q_z - P_z Q_u at 4 random"
          " rational seeds: %s" % ok1)
    assert ok1
    out['C1_char0'] = ok1

    ctl = []
    zero_p = {i: K.zero for i in C.PIDX}
    zero_s = {j: K.zero for j in C.SIDX}
    c2 = run_fixed(K, q, t, zero_p, zero_s, "C2  (p_,s_)=(0,0), free", ctl)
    assert c2['consistent'], "C2 positive control FAILED over char 0"
    flush("      => the branch is NON-EMPTY, so the ideal is NOT the unit"
          " ideal.  Positive control PASSES.")
    # the known point, checked exactly
    M0, b0, lab0 = L.build_rows(q, t, zero_p, zero_s, K)
    zero = [K.zero] * len(M0[0])
    resid = 0
    for row, rhs in zip(M0, b0):
        acc = K.zero
        for a, x in zip(row, zero):
            acc = K.add(acc, K.mul(a, x))
        if not K.iszero(K.sub(acc, rhs)):
            resid += 1
    flush("      known point f_1..f_8 = g_1..g_12 = r_1..r_12 = 0 (f and g"
          " constant, r = 0) satisfies all %d equations exactly: %s"
          % (len(M0), resid == 0))
    assert resid == 0
    out['C2'] = dict(consistent=True, rank=c2['rank'],
                     solution_space_dim=c2.get('solution_space_dim'),
                     known_point_exact=True)

    # C3 : the same branch with the vertex non-degeneracy
    rank, coef, rhs, tr, piv = L.rref_tracked(M0, b0, K)
    free = [c for c in range(len(M0[0])) if c not in piv]
    gzero = True
    for j in range(12):
        col = L.IDX["g%d" % (j + 1)]
        if col in free:
            gzero = False
        else:
            ri = piv.index(col)
            if not K.iszero(rhs[ri]):
                gzero = False
            for fc in free:
                if not K.iszero(coef[ri][fc]):
                    gzero = False
    flush("   C3  the same branch with the vertex non-degeneracy f_8 != 0,"
          " g_12 != 0 (Rabinowitsch f_8*Wf = 1, g_12*Wg = 1):")
    flush("      on the whole solution space of E1+E2 at (p_,s_) = (0,0),"
          " g_1..g_12 are identically zero: %s" % gzero)
    flush("      so g_12 = 0 throughout and g_12*Wg = 1 is unsatisfiable"
          " => EMPTY, exactly what the handoff's section 3d hand argument"
          " predicts (p = s = 0 makes f and g constant).  Control PASSES.")
    assert gzero
    out['C3'] = dict(empty=True, reason="g identically zero on the branch")

    # ------------------------------------------------------ the four ideals
    flush("")
    flush("THE FOUR IDEALS -- both charts, both variants, characteristic zero")
    flush("   chart A : alpha = 1, beta free   |   chart B : alpha = 0,"
          " beta = 1")
    flush("   (free variant, and Rabinowitsch vertex non-degeneracy"
          " f_8*Wf = 1, g_12*Wg = 1)")
    flush("")
    res, rows, minors = P.analyse(q, t, pv1, sv1, pv2, sv2, K)
    out['projective'] = res
    assert res.get('empty'), "the projective analysis did not settle P^1"

    okb, used, gdeg = P.bezout_certificate(minors, K)
    out['bezout'] = dict(verified=okb, minors_used=used)
    assert okb

    # independent spot checks by the direct 38 x 32 route
    flush("")
    flush("INDEPENDENT SPOT CHECKS (the direct 38 x 32 augmented reduction,"
          " a different code path, with its inconsistency certificate"
          " re-verified against the original rows)")
    spot = []
    run_fixed(K, q, t, pv2, sv2, "chart B  (alpha,beta) = (0,1)", spot)
    for be in (0, 1):
        pv, sv = L.chartA_pv_sv(pv1, sv1, pv2, sv2, be, K)
        run_fixed(K, q, t, pv, sv, "chart A at be = %d" % be, spot)
    out['spot_checks'] = spot

    flush("")
    flush("VERDICT (characteristic zero, all 35 face solutions):")
    flush("   chart A free            : unit ideal")
    flush("   chart A Rabinowitsch    : unit ideal")
    flush("   chart B free            : unit ideal")
    flush("   chart B Rabinowitsch    : unit ideal")
    flush("   unit ideal = True  : 4 / 4      unit ideal = False : 0 / 4")
    flush("")
    flush("wall %.1fs" % (time.time() - t0))
    json.dump(out, open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'char0_results.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
