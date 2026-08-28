"""night6 -- characteristic-zero integration test, driver.

Stage 1 (night6/char0_face.py) computes the lex Groebner basis of the face
system over Q and factors the eliminant.  This driver reads that output and,
for each irreducible factor h of the eliminant:

  * rebuilds the face solution (q,t) in K = Q[T]/(h) and verifies the face
    equation 2*q*t' - 3*q'*t = u^2 by exact substitution;
  * builds the support-restricted E3 matrix over K, computes its rank and
    kernel, verifies every kernel basis vector by exact substitution;
  * runs the four ideals -- chart A (alpha=1, beta unknown) and chart B
    (alpha=0, beta=1), each free and with the Rabinowitsch vertex
    non-degeneracy f_8*Wf = 1, g_12*Wg = 1 -- over Q;
  * runs the controls C2 ((p_,s_)=(0,0), free; must be NOT unit, with the
    all-zero point verified by exact substitution) and C3 (the same with the
    vertex non-degeneracy; expected unit).

All characteristic zero.  Nothing is reduced modulo anything.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import flint
import char0_lib as C
import char0_integrate as CI
import char0_controls as CC

SCRATCH = os.environ.get('N6SCRATCH', '/tmp')
FACEOUT = os.path.join(SCRATCH, 'char0_face.out')


def flush(*a):
    print(*a)
    sys.stdout.flush()


def read_face_out(path=FACEOUT):
    lines = [l.strip() for l in open(path).read().splitlines() if l.strip()
             and not l.startswith('// **')]
    dim = int(lines[lines.index('DIM:') + 1])
    vdim = int(lines[lines.index('VDIM:') + 1])
    gbs = lines[lines.index('LEXGB:') + 1:lines.index('ELIMFACTORS:')]
    fl = lines[lines.index('ELIMFACTORS:') + 1:lines.index('END')]
    facs = []
    i = 0
    while i < len(fl):
        assert fl[i] == 'FACTOR', fl[i]
        poly = fl[i + 1]
        assert fl[i + 2] == 'MULT'
        mult = int(fl[i + 3])
        facs.append((poly, mult))
        i += 4
    return dim, vdim, gbs, facs


def to_fmpq_poly(coeffs):
    """coeffs: list of Fractions low->high -> monic flint.fmpq_poly"""
    num = [c.numerator for c in coeffs]
    den = [c.denominator for c in coeffs]
    P = flint.fmpq_poly([flint.fmpq(n, d) for n, d in zip(num, den)])
    return P / P.leading_coefficient()


def main(only_factor=None, skip_singular=False, timeout=36000):
    t_all = time.time()
    dim, vdim, gbs, sfacs = read_face_out()
    flush("=" * 78)
    flush("CHARACTERISTIC ZERO -- face system over Q")
    flush("=" * 78)
    flush("   residual ideal: dim = %d, vdim = %d" % (dim, vdim))
    gb = [C.parse_poly_A(g) for g in gbs]
    uc, shape = C.split_shape(gb)
    flush("   lex GB in shape position; eliminant degree %d" % (len(uc) - 1))
    U = to_fmpq_poly(uc)
    fac = U.factor()
    flush("   eliminant factorisation over Q (flint):")
    facs = []
    for h, mult in sorted(fac[1], key=lambda x: x[0].degree()):
        hm = h / h.leading_coefficient()
        facs.append((hm, mult))
        flush("      degree %d, multiplicity %d : %s"
              % (hm.degree(), mult, hm.str().replace(' ', '')))
    flush("   Singular's own factorize() reported %d factor(s), degrees %s"
          % (len(sfacs), [s.count('A6^') and 0 or 0 for s in []] or
             "(see log)"))
    for poly, mult in sfacs:
        flush("      [Singular] mult %d : %s" % (mult, poly[:200]))

    out = dict(dim=dim, vdim=vdim, elim_degree=len(uc) - 1,
               factors=[], lexgb=gbs)
    covered = 0
    for fi, (h, mult) in enumerate(facs):
        if only_factor is not None and fi != only_factor:
            continue
        d = h.degree()
        flush("")
        flush("#" * 78)
        flush("FACTOR %d : degree %d, multiplicity %d  (covers %d of the 35"
              " face solutions)" % (fi, d, mult, d * mult))
        flush("   h(T) = %s" % h.str().replace(' ', ''))
        K = C.Ext0(h)
        x = K.gen()
        t0 = time.time()
        q, t, badrows = C.face_point0(K, x, shape)
        assert not badrows, ("face system residual rows nonzero", badrows)
        res = C.face_residual0(q, t, K)
        face_ok = not res
        flush("   face solution rebuilt in K = Q[T]/(h)  (%.1fs)"
              % (time.time() - t0))
        flush("   2*q*t' - 3*q'*t - u^2 identically zero in K (exact"
              " substitution): %s" % face_ok)
        assert face_ok
        flush("   q_1 = %s, q_8 = %s ; t_2 != 0: %s ; t_12 != 0: %s"
              % (K.show(q[1]), K.show(q[8]),
                 not K.iszero(t[2]), not K.iszero(t[12])))
        assert K.show(q[1]) == "1" and K.show(q[8]) == "1"
        assert not K.iszero(t[2]) and not K.iszero(t[12])

        M, cols, ns = C.e3_matrix0(q, t, K)
        rank, basis, piv, free = C.nullspace(M, K)
        Mx, colsx, nsx = C.e3_matrix0(q, t, K, s_min=1)
        rankx, basisx, pivx, freex = C.nullspace(Mx, K)
        flush("   support-restricted E3 matrix over K: %d x %d, rank = %d,"
              " KERNEL DIMENSION = %d"
              % (len(M), len(M[0]), rank, len(basis)))
        if len(basis) != 2:
            flush("   *** FLAG: char-0 kernel dimension is %d, NOT 2 ***"
                  % len(basis))
        flush("   free columns: %s"
              % [("%s%d" % cols[c]) for c in free])
        kok = []
        for b in basis:
            pv, sv = C.split(b, cols)
            r3 = C.apply_e30(pv, sv, q, t, K)
            kok.append(not r3)
            nzp = [k for k, v in pv.items() if not K.iszero(v)]
            nzs = [k for k, v in sv.items() if not K.iszero(v)]
            flush("      kernel vector: val p_=%s deg p_=%s val s_=%s"
                  " deg s_=%s ; E3(p_,s_) identically zero in K: %s"
                  % (min(nzp, default=None), max(nzp, default=None),
                     min(nzs, default=None), max(nzs, default=None),
                     not r3))
        assert all(kok), "a kernel basis vector fails E3"
        flush("   relaxed matrix (s_ from u^1): %d x %d, rank = %d,"
              " kernel dim = %d" % (len(Mx), len(Mx[0]), rankx, len(basisx)))
        covered += d * mult

        rec = dict(index=fi, hdeg=d, mult=mult, h=h.str(),
                   face_verified=face_ok, e3_shape=[len(M), len(M[0])],
                   rank=rank, kerdim=len(basis),
                   free_cols=[("%s%d" % cols[c]) for c in free],
                   relaxed=dict(shape=[len(Mx), len(Mx[0])], rank=rankx,
                                kerdim=len(basisx)),
                   runs=[], controls=[])
        if skip_singular:
            out['factors'].append(rec)
            continue

        # ---- controls first (hard gate) -------------------------------
        for rabin in (False, True):
            eqs, names, meta = CI.build_system0(
                K, q, t, None, None, cols, 'B', rabin, zero_ps=True)
            label = ("C3  (p_,s_)=(0,0) WITH vertex non-degeneracy"
                     if rabin else "C2  (p_,s_)=(0,0), free")
            sol = {n: K.zero for n in names}
            nb = CC.subst_check(eqs, names, sol, K)
            isunit, sdim, size, gbo, secs, path = CI.run_singular0(
                eqs, names, K, "f%d_c%s" % (fi, 'rab' if rabin else 'free'),
                timeout=timeout)
            flush("   %s : %d eqs, %d vars -> |GB| = %d, unit ideal = %s,"
                  " dim = %d  (%.1fs)"
                  % (label, len(eqs), len(names), size, isunit, sdim, secs))
            if not rabin:
                flush("      all-zero point (f, g constant, r = 0) satisfies"
                      " every equation exactly: %s" % (nb == 0))
            rec['controls'].append(dict(
                control='C3' if rabin else 'C2', unit_ideal=isunit, dim=sdim,
                gb_size=size, seconds=secs,
                known_point_ok=(nb == 0) if not rabin else None))
        c2 = [c for c in rec['controls'] if c['control'] == 'C2'][0]
        assert c2['unit_ideal'] is False and c2['known_point_ok'], \
            "C2 positive control FAILED over char 0"

        # ---- the four main ideals -------------------------------------
        for chart in ('A', 'B'):
            for rabin in (False, True):
                eqs, names, meta = CI.build_system0(
                    K, q, t, basis[0], basis[1], cols, chart, rabin)
                flush("   " + "-" * 68)
                flush("   chart %s (%s), %s"
                      % (chart, "alpha=1, beta free" if chart == 'A'
                         else "alpha=0, beta=1",
                         "vertex non-degeneracy f_8*Wf=1, g_12*Wg=1"
                         if rabin else "free"))
                flush("      E3 vanishes identically in the unknowns"
                      " (symbolic kernel property): %s"
                      % meta['E3_identically_zero'])
                assert meta['E3_identically_zero']
                flush("      E0 %d rows, E1 %d rows, E2 %d rows (+%d"
                      " Rabinowitsch) = %d equations; %d unknowns (incl. T)"
                      % (meta['n_E0'], meta['n_E1'], meta['n_E2'],
                         2 if rabin else 0, meta['n_eqs'], meta['n_vars']))
                isunit, sdim, size, gbo, secs, path = CI.run_singular0(
                    eqs, names, K,
                    "f%d_%s_%s" % (fi, chart, 'rab' if rabin else 'free'),
                    timeout=timeout)
                flush("      Singular std over Q: |GB| = %d, unit ideal = %s,"
                      " dim = %d  (%.1fs)" % (size, isunit, sdim, secs))
                rec['runs'].append(dict(
                    chart=chart, rabinowitsch=rabin, unit_ideal=isunit,
                    dim=sdim, gb_size=size, seconds=secs,
                    n_eqs=meta['n_eqs'], n_vars=meta['n_vars'],
                    E3_identically_zero=meta['E3_identically_zero'],
                    gb=gbo if not isunit else []))
                if not isunit:
                    flush("      *** NON-UNIT IDEAL -- STOP RULE ***")
        out['factors'].append(rec)
        json.dump(out, open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'char0_results.json'), 'w'), indent=1)
    out['covered'] = covered
    flush("")
    flush("face solutions covered: %d of 35" % covered)
    flush("total wall %.1fs" % (time.time() - t_all))
    json.dump(out, open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'char0_results.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--factor', type=int, default=None)
    ap.add_argument('--no-singular', action='store_true')
    ap.add_argument('--timeout', type=int, default=36000)
    a = ap.parse_args()
    main(a.factor, a.no_singular, a.timeout)
