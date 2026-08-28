"""night6 TASK 1 driver -- integration test of the E3 kernel."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flint
import e3_final as E
import integrate as I


def flush(*a):
    print(*a)
    sys.stdout.flush()


def face_families(p, only_rational=True):
    res = E.build_residuals(p)
    vdim, dim, gb, gbs, secs = E.singular_lexgb(res, p, 'task1_%d' % p)
    uni = [g for g in gb if all(m[i] == 0 for m in g for i in range(5))]
    U = uni[0]
    deg = max(m[5] for m in U)
    uc = [0] * (deg + 1)
    for m, c in U.items():
        uc[m[5]] = c % p
    f = flint.nmod_poly([c % p for c in uc], p)
    shape = {}
    for g in gb:
        if g is U:
            continue
        lin = [i for i in range(5) if any(m[i] for m in g)]
        k = lin[0] + 1
        num, den = {}, {}
        for m, c in g.items():
            (den if m[k - 1] else num)[m[5]] = c % p
        nl = [0] * (max(num or [0]) + 1)
        for e, c in num.items():
            nl[e] = c
        dl = [0] * (max(den or [0]) + 1)
        for e, c in den.items():
            dl[e] = c
        shape[k] = (nl, dl)
    out = []
    for h, mult in sorted(f.factor()[1], key=lambda x: x[0].degree()):
        if only_rational and h.degree() != 1:
            continue
        K = E.Ext(h, p)
        q, t = E.face_point(K, K.gen(), shape, p)
        assert not E.face_residual(q, t, K, p)
        M, cols, ns = E.e3_matrix(q, t, K, p)
        rank, basis = E.nullspace_ext(M, K)
        assert len(basis) == 2, ("kernel dim != 2", len(basis))
        for b in basis:
            pv, sv = E.split(b, cols)
            assert not E.apply_e3(pv, sv, q, t, K, p)
        out.append((K, q, t, basis, cols, h))
    return out, vdim, dim


def verify_solution(sol, names, eqs, K):
    """substitute a numeric solution (dict name->K elt) into eqs; exact check"""
    idx = {n: i for i, n in enumerate(names)}
    bad = 0
    for e in eqs:
        acc = K.zero
        for m, c in e.d.items():
            term = c
            for i, ex in enumerate(m):
                for _ in range(ex):
                    term = K.mul(term, sol[names[i]])
            acc = K.add(acc, term)
        if not K.iszero(acc):
            bad += 1
    return bad


def main(p, out):
    flush("=" * 78)
    flush("PRIME p = %d" % p)
    flush("=" * 78)
    fams, vdim, dim = face_families(p)
    flush("face system: dim=%d vdim=%d ; F_p-rational face solutions: %d"
          % (dim, vdim, len(fams)))
    recs = []
    for fi, (K, q, t, basis, cols, h) in enumerate(fams):
        flush("")
        flush("#" * 74)
        flush("FACE POINT %d   (h = %s)" % (fi, h.str().replace(' ', '')))
        flush("   q_1..q_8  = %s" % [K.show(q[i]) for i in E.QIDX])
        flush("   t_2..t_12 = %s" % [K.show(t[j]) for j in E.TIDX])
        # E4 check
        e4 = E.face_residual(q, t, K, p)
        flush("   E4 (3q't - 2qt' = -u^2) verified exactly: %s" % (not e4))
        rec = dict(h=h.str(), q=[K.show(q[i]) for i in E.QIDX],
                   t=[K.show(t[j]) for j in E.TIDX], E4=not e4, variants=[])
        for chart in ('A', 'B'):
            for rabin in (False, True):
                eqs, names, meta = I.build_system(K, p, q, t, basis[0],
                                                  basis[1], cols, chart, rabin)
                tag = "%d_f%d_%s_%s" % (p, fi, chart, 'rab' if rabin else 'free')
                flush("   " + "-" * 68)
                flush("   chart %s (%s), variant %s"
                      % (chart,
                         "alpha=1, beta free" if chart == 'A' else
                         "alpha=0, beta=1",
                         "vertex non-degeneracy f_8 != 0, g_12 != 0 imposed"
                         " (Rabinowitsch)" if rabin else "free"))
                flush("      E3 vanishes identically in the unknowns"
                      " (kernel property, symbolic): %s"
                      % meta['E3_identically_zero'])
                flush("      equations: E0 %d rows, E1 %d rows, E2 %d rows"
                      " (+%d Rabinowitsch) = %d ; unknowns %d"
                      % (meta['n_E0'], meta['n_E1'], meta['n_E2'],
                         2 if rabin else 0, meta['n_eqs'], meta['n_vars']))
                isunit, sdim, size, gb, secs, path = I.run_singular(
                    eqs, names, K, p, tag)
                flush("      Singular std: |GB| = %d, unit ideal = %s,"
                      " dim = %d   (%.1fs)" % (size, isunit, sdim, secs))
                claimed = None
                if isunit:
                    flush("      => NO solution in this chart: with alpha,beta"
                          " scaled to this chart the identities E0,E1,E2 have"
                          " no common zero at all.")
                else:
                    flush("      => solutions exist in this chart; GB (first"
                          " 40 elements):")
                    for g in gb[:40]:
                        flush("         " + (g if len(g) < 200
                                             else g[:197] + "..."))
                    # try to read off a point when the GB is linear/diagonal
                    claimed = gb
                rec['variants'].append(dict(
                    chart=chart, rabinowitsch=rabin, unit_ideal=isunit,
                    dim=sdim, gb_size=size, seconds=secs,
                    n_eqs=meta['n_eqs'], n_vars=meta['n_vars'],
                    E3_identically_zero=meta['E3_identically_zero'],
                    gb=gb if not isunit else []))
        recs.append(rec)
    json.dump(recs, open(out, 'w'), indent=1)
    return recs


if __name__ == '__main__':
    allr = {}
    for p in (999983, 1000003):
        allr[str(p)] = main(p, os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'task1_p%d.json' % p))
    flush("")
    flush("=" * 78)
    flush("SUMMARY  (unit ideal = no solution in that chart)")
    for p, recs in allr.items():
        for fi, r in enumerate(recs):
            for v in r['variants']:
                flush("   p=%s face %d chart %s %-4s : unit ideal = %s"
                      % (p, fi, v['chart'],
                         'rab' if v['rabinowitsch'] else 'free',
                         v['unit_ideal']))
    flush("")
    for p, recs in allr.items():
        forced = all(v['unit_ideal'] for r in recs for v in r['variants']
                     if not v['rabinowitsch'])
        flush("   p=%s : (alpha,beta) = (0,0) forced at every F_p-rational"
              " face solution, free variant: %s" % (p, forced))
