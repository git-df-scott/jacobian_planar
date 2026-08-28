"""night6 -- control C4: the linear-algebra instrument, run MOD P.

The same build_rows / rref_tracked code that produces the characteristic-zero
verdict is run at the mod-p face solutions of night6/E3_KERNEL.md, where the
answer is already on record (night6/INTEGRATION_TEST.md: unit ideal in both
charts, at all 35 face solutions, both primes).  If the instrument is sound it
must reproduce that: chart B and chart A inconsistent, and the (p_,s_)=(0,0)
branch consistent.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e3_final as E
import char0_linear as L
from task1_run import face_families


def main():
    for p in (999983, 1000003):
        fams, vdim, dim = face_families(p, only_rational=False)
        print("p = %d : face system dim %d vdim %d, %d families covering %d"
              " of the 35 face solutions"
              % (p, dim, vdim, len(fams), sum(f[5].degree() for f in fams)),
              flush=True)
        tally = {}
        for fi, (K, q, t, basis, cols, h) in enumerate(fams):
            pv1, sv1 = E.split(basis[0], cols)
            pv2, sv2 = E.split(basis[1], cols)
            cases = [("chart B", pv2, sv2),
                     ("chart A be=0", pv1, sv1)]
            for x in (1, 2, 3):
                pv = {i: K.add(pv1[i], K.smul(x, pv2[i])) for i in pv1}
                sv = {j: K.add(sv1[j], K.smul(x, sv2[j])) for j in sv1}
                cases.append(("chart A be=%d" % x, pv, sv))
            cases.append(("(p_,s_)=(0,0)",
                          {i: K.zero for i in E.PIDX},
                          {j: K.zero for j in E.SIDX}))
            for name, pv, sv in cases:
                M, b, lab = L.build_rows(q, t, pv, sv, K)
                rank, coef, rhs, tr, piv = L.rref_tracked(M, b, K)
                inc = L.inconsistent_rows(coef, rhs, K)
                ok = True
                if inc:
                    okM, okb, val = L.verify_certificate(tr[inc[0]], M, b, K)
                    ok = okM and okb
                key = (name, bool(inc), rank, ok)
                tally[key] = tally.get(key, 0) + 1
        for (name, incons, rank, ok), n in sorted(tally.items()):
            print("   %-16s : inconsistent = %-5s rank = %d,"
                  " certificate verified = %-5s  [%d of %d families]"
                  % (name, incons, rank, ok if incons else "n/a",
                     n, len(fams)), flush=True)


if __name__ == '__main__':
    main()
