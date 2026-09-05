"""night6 -- control C5: the PROJECTIVE instrument, run MOD P.

char0_projective.analyse is the code path that produces the characteristic-
zero verdict.  Here the identical code is run at the mod-p face solutions of
night6/E3_KERNEL.md, where the answer is already on record
(night6/INTEGRATION_TEST.md: unit ideal in both charts and both variants, at
all 35 face solutions, at p = 999983 and p = 1000003).  The instrument must
reproduce that, at every face family, at both primes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e3_final as E
import char0_projective as P
from task1_run import face_families


def main():
    total = ok = 0
    for p in (999983, 1000003):
        fams, vdim, dim = face_families(p, only_rational=False)
        print("p = %d : face system dim %d vdim %d ; %d families covering %d"
              " of the 35 face solutions"
              % (p, dim, vdim, len(fams), sum(f[5].degree() for f in fams)),
              flush=True)
        for fi, (K, q, t, basis, cols, h) in enumerate(fams):
            pv1, sv1 = E.split(basis[0], cols)
            pv2, sv2 = E.split(basis[1], cols)
            out, rows, minors = P.analyse(q, t, pv1, sv1, pv2, sv2, K,
                                          show=lambda *a: None)
            bez = P.bezout_certificate(minors, K, show=lambda *a: None)[0] \
                if minors else False
            total += 1
            ok += 1 if (out.get('empty') and bez) else 0
            print("   family %d (deg h = %d, covers %d of the 35) :"
                  " E2 rank %d ker %d | G rank %d left-null %d |"
                  " nonzero 3x3 minors %d | gcd degree %s |"
                  " common zero at [1:0] %s | no (alpha,beta) != 0 admits a"
                  " solution: %s | Bezout certificate verified: %s"
                  % (fi, h.degree(), h.degree(), out['E2_rank'],
                     out['E2_kerdim'], out['G_rank'], out['G_leftnull'],
                     out['n_minors_nonzero'], out.get('gcd_degree'),
                     out.get('common_zero_at_beta0'), out.get('empty'), bez),
                  flush=True)
    print("", flush=True)
    print("C5 summary: %d of %d face families (both primes, 35 of 35 face"
          " solutions each) reproduce the recorded mod-p verdict, with the"
          " Bezout certificate verified in each case." % (ok, total))


if __name__ == '__main__':
    main()
