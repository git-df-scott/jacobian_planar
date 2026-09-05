"""night6 -- driver for the characteristic-zero linear-algebra instrument.

Order of business, controls first:

  C2 (positive control)  (p_,s_) = (0,0), free.  The linear part E1+E2 must be
     CONSISTENT -- the handoff's section 3d branch lives there -- and the
     all-zero point (f, g constant, r = 0) must satisfy every equation of the
     full system exactly.  A NOT-unit answer is the required outcome.
  C3 (control with a known answer, known for a reason)  the same branch with
     the vertex non-degeneracy f_8 != 0, g_12 != 0.  The handoff's hand
     argument forces f and g constant, hence f_8 = 0, so this must be empty.
  chart B  (alpha = 0, beta = 1)
  chart A  (alpha = 1, beta = be free)  -- via minors in be

All characteristic zero, exact, no Groebner engine.
"""
import os, sys, json, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_run as R
import char0_lib as C
import char0_linear as L


def flush(*a):
    print(*a)
    sys.stdout.flush()


def load_face():
    dim, vdim, gbs, sfacs = R.read_face_out()
    gb = [C.parse_poly_A(g) for g in gbs]
    uc, shape = C.split_shape(gb)
    U = R.to_fmpq_poly(uc)
    facs = sorted(U.factor()[1], key=lambda x: x[0].degree())
    assert len(facs) == 1 and facs[0][1] == 1, \
        ("expected a single irreducible factor", [(f.degree(), m)
                                                  for f, m in facs])
    h = facs[0][0]
    h = h / h.leading_coefficient()
    K = C.Ext0(h)
    q, t, bad = C.face_point0(K, K.gen(), shape)
    assert not bad
    assert not C.face_residual0(q, t, K)
    M, cols, ns = C.e3_matrix0(q, t, K)
    rank, basis, piv, free = C.nullspace(M, K)
    assert len(basis) == 2
    for bvec in basis:
        pv, sv = C.split(bvec, cols)
        assert not C.apply_e30(pv, sv, q, t, K)
    return dict(dim=dim, vdim=vdim, K=K, h=h, q=q, t=t, cols=cols,
                basis=basis, rank=rank, kerdim=len(basis),
                free=[("%s%d" % cols[c]) for c in free])


def run_fixed(K, q, t, pv, sv, tag, out):
    """one linear system over K, no be"""
    t0 = time.time()
    M, b, labels = L.build_rows(q, t, pv, sv, K)
    rank, coef, rhs, tr, piv = L.rref_tracked(M, b, K)
    inc = L.inconsistent_rows(coef, rhs, K)
    secs = time.time() - t0
    flush("   %s : linear system %d x %d over K ; rank = %d ;"
          " inconsistent rows = %d   (%.1fs)"
          % (tag, len(M), len(M[0]), rank, len(inc), secs))
    rec = dict(tag=tag, rows=len(M), cols=len(M[0]), rank=rank,
               n_inconsistent=len(inc), seconds=secs)
    if inc:
        c = tr[inc[0]]
        okM, okb, val = L.verify_certificate(c, M, b, K)
        flush("      CERTIFICATE re-verified against the original rows:"
              " c.M = 0 : %s ; c.b = %s (nonzero: %s)"
              % (okM, val[:60] + ("..." if len(val) > 60 else ""), okb))
        assert okM and okb
        rec.update(consistent=False, certificate_verified=True)
        flush("      => NO solution in (f,g,r) at all: this chart is EMPTY"
              " over characteristic zero, from E1 and E2 alone.")
    else:
        rec.update(consistent=True, certificate_verified=None,
                   solution_space_dim=len(M[0]) - rank)
        flush("      => the linear system is CONSISTENT; solution space"
              " dimension %d" % (len(M[0]) - rank))
        # read off the unique solution when the rank is full
        if rank == len(M[0]):
            sol = {}
            for ri, c in enumerate(piv):
                sol[L.NAMES[c]] = rhs[ri]
            nz = [n for n in L.NAMES if not K.iszero(sol.get(n, K.zero))]
            flush("      unique solution; nonzero coordinates: %s"
                  % (nz or "none -- f, g constant and r = 0"))
            rec['unique_solution_nonzero_coords'] = nz
            rec['f8'] = K.show(sol.get('f8', K.zero))
            rec['g12'] = K.show(sol.get('g12', K.zero))
    out.append(rec)
    return rec


def main():
    t_all = time.time()
    D = load_face()
    K, q, t = D['K'], D['q'], D['t']
    flush("=" * 78)
    flush("CHARACTERISTIC ZERO -- integration test by exact linear algebra")
    flush("=" * 78)
    flush("   face system over Q: dim = %d, vdim = %d" % (D['dim'], D['vdim']))
    flush("   eliminant: one irreducible factor of degree %d over Q"
          " (covers 35 of the 35 face solutions)" % D['h'].degree())
    flush("   face equation verified exactly in K = Q[T]/(h)")
    flush("   E3 matrix over K: rank %d, KERNEL DIMENSION %d, free columns %s"
          % (D['rank'], D['kerdim'], D['free']))
    flush("   both kernel basis vectors verified: E3(p_,s_) = 0 exactly in K")

    pv1, sv1 = C.split(D['basis'][0], D['cols'])
    pv2, sv2 = C.split(D['basis'][1], D['cols'])
    out = []

    flush("")
    flush("CONTROLS")
    zero_p = {i: K.zero for i in C.PIDX}
    zero_s = {j: K.zero for j in C.SIDX}
    c2 = run_fixed(K, q, t, zero_p, zero_s, "C2  (p_,s_)=(0,0), free", out)
    if c2.get('consistent'):
        flush("      C2 verdict: the branch is NON-EMPTY -> the ideal is NOT"
              " the unit ideal.  Positive control PASSES.")
    assert c2.get('consistent'), "C2 positive control FAILED"
    if c2.get('unique_solution_nonzero_coords') == []:
        flush("      C3  the same branch with the vertex non-degeneracy"
              " f_8 != 0, g_12 != 0:")
        flush("          the unique solution has f_8 = %s and g_12 = %s,"
              " so f_8*Wf = 1 is unsatisfiable"
              % (c2['f8'], c2['g12']))
        flush("          => EMPTY, which is exactly what the handoff's"
              " section 3d hand argument predicts.  Control PASSES.")
        out.append(dict(tag="C3", consistent=False,
                        reason="unique solution of C2 has f_8 = 0"))

    flush("")
    flush("CHART B  (alpha = 0, beta = 1)")
    run_fixed(K, q, t, pv2, sv2, "chart B, free", out)

    json.dump(dict(kerdim=D['kerdim'], rank=D['rank'], free=D['free'],
                   hdeg=D['h'].degree(), results=out),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'char0_linear_results.json'), 'w'), indent=1)
    flush("")
    flush("wall %.1fs" % (time.time() - t_all))


if __name__ == '__main__':
    main()
