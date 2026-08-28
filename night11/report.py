"""night11 -- assemble NUMERIC_NET.md from controls.json + net_results.json."""

import json
import os
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

BINS = [0.0, 1e-18, 1e-12, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1, 0.5, 0.9,
        0.999999, 1.000001, 2.0, 10.0, 1e2, 1e4, 1e30]


def binlabel(lo, hi):
    def f(v):
        if v == 0.0:
            return "0"
        return "%.0e" % v
    return "[%s, %s)" % (f(lo), f(hi))


def histogram(vals):
    counts = [0] * (len(BINS) - 1)
    for v in vals:
        for k in range(len(BINS) - 1):
            if BINS[k] <= v < BINS[k + 1]:
                counts[k] += 1
                break
    return counts


def main():
    C = json.load(open(os.path.join(HERE, 'controls.json')))
    N = json.load(open(os.path.join(HERE, 'net_results.json')))
    R = N['records']
    cfg = N['config']

    L = []
    w = L.append
    w("# night11 -- NUMERIC NET (v0): landscape census")
    w("")
    w("First numerical search of this campaign. Continuous optimization of")
    w("real coefficient vectors for polynomial pairs `(P, Q)` of degrees")
    w("`(2m, 3m) = (84, 126)`, `m = 42`, against")
    w("")
    w("    E(c) = E_K + lambda_T * E_T,")
    w("    E_K  = sum of squares of all coefficients of P_x Q_y - P_y Q_x - 1,")
    w("")
    w("with many random restarts. **v0 maps the landscape only.** Every number")
    w("below is a measurement of where an optimizer stops; nothing here is")
    w("lifted, certified, or claimed to be anything.")
    w("")

    # ---------------- support design
    w("## 1. Parametrization")
    w("")
    w("See `supports.py` for the full derivation. Summary:")
    w("")
    w("* **Newton-triangle similarity.** `supp(P) subset Delta(84)`,")
    w("  `supp(Q) subset Delta(126) = 1.5 * Delta(84)` -- one Newton triangle")
    w("  and a scaled copy. On its own that is 11783 real parameters.")
    w("* **Torus grading.** `P`, `Q` are taken semi-invariant of weights")
    w("  `aP`, `aQ` under `(x,y) -> (zeta x, zeta^-1 y)`, `zeta^t = 1`; a")
    w("  monomial `x^i y^j` has weight `i - j mod t`. The Jacobian then has")
    w("  weight `aP + aQ`, so `aP + aQ = 0 (mod t)` is needed for the residual")
    w("  to stay in one class.")
    w("* **The grading is not free.** The `(0,0)` coefficient of the Jacobian")
    w("  is exactly `P[1,0] Q[0,1] - P[0,1] Q[1,0]` and nothing else, so the")
    w("  constant `1` is reachable only if `aP = 1`, `aQ = -1 (mod t)`.")
    w("  If additionally the leading forms are to have the `(H^2, H^3)` shape")
    w("  one needs `w` with `2w = aP`, `3w = aQ`, forcing `t | 5`.")
    w("")
    w("  This was found by measurement, not assumed: a first design put both")
    w("  `P` and `Q` in the sublattice `{i - j = 0 mod 16}` (745 parameters),")
    w("  where `(1,0)` and `(0,1)` are absent; every seed there ran to")
    w("  `E_K = 1.0000000` with `||P_x Q_y - P_y Q_x|| ~ 2e-4`, i.e. straight")
    w("  into the degenerate locus `Jacobian = 0`, because `E_K >= 1` holds")
    w("  identically on that support.")
    w("")
    w("| arm | t | aP, aQ | params (P + Q) | residual cells | unknowns/eqns | top-form dims | (H^2,H^3) shape reachable |")
    w("|---|---|---|---|---|---|---|---|")
    sup = C['results']['support']
    reach = {'GRADED-5': 'yes (w = 3)', 'GRADED-15': 'NO', 'FULL': 'yes'}
    for name in ['GRADED-5', 'GRADED-15', 'FULL']:
        s = sup[name]
        w("| %s | %d | %d, %d | %d + %d = %d | %d | %.3f | %d, %d | %s |"
          % (name, s['t'], s['aP'], s['aQ'], s['nP'], s['nQ'], s['n'],
             s['residual_cells'], s['n'] / s['residual_cells'],
             s['topform_dims'][0], s['topform_dims'][1], reach[name]))
    w("")
    w("`GRADED-15` (788 parameters) is the primary arm: it is inside the")
    w("300-800 parameter band the brief asked for. `GRADED-5` (2357")
    w("parameters) is the secondary arm; it is the only nontrivial grading")
    w("that also admits the `(H^2, H^3)` leading-form shape, and it is above")
    w("the band -- the band and that shape are not simultaneously satisfiable.")
    w("Unknowns/equations is ~0.54 in every arm because both counts scale")
    w("like `1/t`: the grading is a resolution knob, not a knob on how")
    w("over-determined the Keller system is.")
    w("")

    # ---------------- E_T
    w("## 2. What E_T measures, and what it does not")
    w("")
    w("`E_T` acts on the leading homogeneous parts `P_top` (degree 84) and")
    w("`Q_top` (degree 126) only. For a pair of degrees `(2m, 3m)` the shape")
    w("wanted of the leading forms is `P_top ~ H^2`, `Q_top ~ H^3` for a")
    w("single form `H` of degree `m`; equivalently `P_top^3` and `Q_top^2`")
    w("(both of degree `6m`) are proportional. `E_T` measures exactly that")
    w("proportionality defect, as a squared sine of the angle between the two")
    w("coefficient vectors, plus a guard keeping the leading forms from")
    w("collapsing:")
    w("")
    w("    A = tP*tP*tP,  B = tQ*tQ   (1D coefficient convolutions)")
    w("    E_prop = 1 - <A,B>^2 / (|A|^2 |B|^2)          in [0,1], scale free")
    w("    E_nd   = relu(tau - |tP|^2)^2 + relu(tau - |tQ|^2)^2,  tau = 1e-2")
    w("    E_T    = E_prop + E_nd")
    w("")
    w("**Limitation.** This is a proxy on the leading forms, not the Jelonek")
    w("set. It says nothing about lower-order terms, and the actual")
    w("non-properness locus is cut out by the leading coefficients (in the")
    w("source variable) of `Res_y(P-u, Q-v)` and `Res_x(P-u, Q-v)`, which are")
    w("far too heavy to form symbolically at degrees (84, 126). `E_prop = 0`")
    w("is a necessary shape condition, in no way sufficient; a small `E_T`")
    w("supports no conclusion. The smallest singular value of the Sylvester")
    w("matrix of the two leading forms (the alternative the brief suggested)")
    w("is computed as a post-hoc diagnostic on the recorded stalls only -- a")
    w("210x210 SVD inside the inner loop would have cost more than the whole")
    w("objective. The objective is a swappable object (`supports.Objective`,")
    w("`tear=` argument), so a refined `E_T` drops in without touching the net.")
    w("")

    # ---------------- controls
    r = C['results']
    w("## 3. Controls (hard gate, all run before the search)")
    w("")
    n1 = r['N1']
    w("### N1 -- symbolic vs numeric Keller residual: **PASS**")
    w("")
    w("Random pair of degrees (3, 4), coefficients rounded to 6 decimals and")
    w("lifted to exact rationals in sympy; `expand(P_x Q_y - P_y Q_x - 1)`")
    w("compared cell by cell with the FFT kernel.")
    w("")
    w("| quantity | value |")
    w("|---|---|")
    w("| monomials compared | %d |" % n1['monomials'])
    w("| max abs difference, all cells | %.3e |" % n1['max_abs_err_all'])
    w("| fused-FFT vs explicit-convolution residual | %.3e |" % n1['fused_vs_reference'])
    w("| direct vs FFT product, deg 39 x deg 59 | %.3e (relative) |" % n1['conv_rel_err'])
    w("| analytic vs central-difference gradient (43 params, lambda_T = 0.3) | %.3e (relative) |" % n1['grad_rel_err'])
    w("")
    n2 = r['N2']
    a, b = n2['N2a'], n2['N2b']
    w("### N2 -- seeded at a known automorphism")
    w("")
    w("Automorphisms used: `P = x + f(y)`, `Q = y + g(P)`, Jacobian identically")
    w("1, degrees `(deg f, deg f * deg g)`.")
    w("")
    w("**The campaign degree shape (84, 126) admits no automorphism at all.**")
    w("By Jung-van der Kulk every planar polynomial automorphism is tame and")
    w("its two degrees are divisibility-ordered; 84 does not divide 126 and")
    w("126 does not divide 84. N2 is therefore run at (4, 8) and at (84, 168),")
    w("the nearest same-scale shape that does carry one.")
    w("")
    w("| | N2a | N2b |")
    w("|---|---|---|")
    w("| degrees | (%d, %d) | (%d, %d) |" % tuple(a['degrees'] + b['degrees']))
    w("| parameters (full triangular support) | %d | %d |" % (a['nparam'], b['nparam']))
    w("| E_K at the exact automorphism | %.3e | %.3e |" % (a['EK_at_exact'], b['EK_at_exact']))
    w("| perturbation applied | 1e-3 | 1e-8 |")
    w("| E_K at the perturbed start | %.3e | %.3e |" % (a['EK_at_perturbed_start'], b['EK_at_perturbed_start']))
    w("| E_K after descent | **%.3e** | **%.3e** |" % (a['EK_final'], b['EK_final']))
    w("| iterations | %d | %d |" % (a['nit'], b['nit']))
    w("")
    w("N2a reaches `6.96e-20`: the basin exists and the code finds exact")
    w("structure to the precision the brief asked for. N2b descends 8 decades")
    w("from its perturbed start but stops at `%.1e` within its 4000-iteration"
      % b['EK_final'])
    w("budget. Recorded as measured: at 18020 parameters the Keller variety is")
    w("positive-dimensional, so the Hessian is singular along the automorphism")
    w("group directions and L-BFGS-B converges linearly, not quadratically.")
    w("`E_K = %.1e` at the exact point shows the floor is not a kernel"
      % b['EK_at_exact'])
    w("accuracy limit.")
    w("")
    n3 = r['N3']
    w("### N3 -- random seeds at small degree")
    w("")
    w("| degrees | shape | params | seeds | reached E_K < 1e-18 | best | median |")
    w("|---|---|---|---|---|---|---|")
    shp = {'4_8': 'd, 2d', '2_4': 'd, 2d', '4_6': '2m, 3m (m=2)'}
    for tag in ['2_4', '4_8', '4_6']:
        d = n3[tag]
        w("| (%d, %d) | %s | %d | %d | %d/%d | %.3e | %.3e |"
          % (d['degrees'][0], d['degrees'][1], shp[tag], d['nparam'],
             d['seeds'], d['n_machine_precision'], d['seeds'], d['best'],
             d['median']))
    w("")
    w("`(2,4)` and `(4,8)` are shapes `d | 2d`, where automorphisms are")
    w("abundant. `(4,6)` is the mission shape `(2m, 3m)` at `m = 2`, where")
    w("the same divisibility obstruction as at (84,126) applies, and it is")
    w("reported alongside as the small-degree image of the mission problem.")
    w("")
    w("N3 reads as follows. At `(2,4)` -- 21 parameters -- random seeds do")
    w("reach machine precision (%d of %d, best `%.2e`), which is the check the"
      % (n3['2_4']['n_machine_precision'], n3['2_4']['seeds'],
         n3['2_4']['best']))
    w("brief asked for. At `(4,8)` -- 60 parameters -- they do not inside a")
    w("2000-iteration budget (best `%.2e`), even though N2a shows that same"
      % n3['4_8']['best'])
    w("shape's automorphism basin is reachable to `%.2e` when the descent"
      % a['EK_final'])
    w("starts near it. So the `(4,8)` shortfall is a reach-from-random-start")
    w("and budget effect, not a defect in the residual or its gradient, which")
    w("N1 pins to `%.0e`. This is recorded as the state of the gate, not"
      % n1['max_abs_err_all'])
    w("argued away: the net's own stall values below have to be read knowing")
    w("that random-start descent already fails to find known exact structure")
    w("at 60 parameters in this budget.")
    w("")
    w("Controls wall time: %.1f s." % C['results']['wall_seconds'])
    w("")

    # ---------------- the net
    w("## 4. The net")
    w("")
    w("| | |")
    w("|---|---|")
    w("| degrees | (84, 126) |")
    w("| optimizer | scipy L-BFGS-B, `ftol = gtol = 0` (relative stopping tests OFF) |")
    w("| iteration budget | %d per seed, re-launched from the end point on early stop (up to 4 passes, total capped at the budget) |" % cfg['maxiter'])
    w("| seeds | %d total |" % len(R))
    w("| initialisation | coefficients `~ N(0, decay^(i+j))` on the masked support, then a global rescale `P,Q -> sP,sQ` making `\\|P_x Q_y - P_y Q_x\\| = 1`; four decay families %s |" % ", ".join("`%s`=%.2f" % (f[0], f[1]) for f in cfg['families']))
    w("| parallelism | 4 cores, `multiprocessing.Pool` |")
    w("| wall time | %.0f s (%.1f min) |" % (N['wall_seconds'], N['wall_seconds'] / 60))
    w("")
    w("`ftol = gtol = 0` matters: with scipy's defaults the descent halts on a")
    w("relative test around `1e-11` and every \"plateau\" would be a tolerance")
    w("artefact. Here a run ends only on the iteration budget or on a genuine")
    w("line-search failure.")
    w("")

    # ---------------- classification
    w("### Classification tally")
    w("")
    w("* `CONVERGED-AUTOMORPHISM-LIKE` -- `E_K < 1e-18`.")
    w("* `STALLED-COLLAPSED` -- `|E_K - 1| < 1e-6` with")
    w("  `||P_x Q_y - P_y Q_x|| < 1e-3`: the degenerate attractor where the")
    w("  Jacobian is driven to zero and the residual is just the missing")
    w("  constant. `E_K = 1` is exactly the value of that locus.")
    w("* `STALLED` -- everything else that stayed finite; the interesting class.")
    w("* `DIVERGED` -- non-finite, or `E_K > 1e6`.")
    w("")
    arms = [a[0] for a in cfg['arms']]
    classes = ['CONVERGED-AUTOMORPHISM-LIKE', 'STALLED', 'STALLED-COLLAPSED',
               'DIVERGED']
    w("| arm | seeds | " + " | ".join(c.replace('-', '-<br>') for c in classes)
      + " | min E_K | median E_K |")
    w("|---" * (3 + len(classes)) + "|")
    for arm in arms:
        rows = [x for x in R if x['arm'] == arm]
        cnt = Counter(x['cls'] for x in rows)
        eks = sorted(x['EK'] for x in rows if np.isfinite(x.get('EK', np.nan)))
        w("| `%s` | %d | %s | %.4g | %.4g |"
          % (arm, len(rows), " | ".join(str(cnt.get(c, 0)) for c in classes),
             min(eks) if eks else float('nan'),
             float(np.median(eks)) if eks else float('nan')))
    cnt = Counter(x['cls'] for x in R)
    eks_all = sorted(x['EK'] for x in R if np.isfinite(x.get('EK', np.nan)))
    w("| **all** | %d | %s | %.4g | %.4g |"
      % (len(R), " | ".join(str(cnt.get(c, 0)) for c in classes),
         min(eks_all), float(np.median(eks_all))))
    w("")

    # ---------------- histogram
    w("### Histogram of final E_K")
    w("")
    w("| bin | " + " | ".join("`%s`" % a for a in arms) + " | all |")
    w("|---" * (2 + len(arms)) + "|")
    per = {a: histogram([x['EK'] for x in R if x['arm'] == a]) for a in arms}
    allh = histogram([x['EK'] for x in R])
    for k in range(len(BINS) - 1):
        if allh[k] == 0:
            continue
        w("| `%s` | %s | %d |"
          % (binlabel(BINS[k], BINS[k + 1]),
             " | ".join(str(per[a][k]) for a in arms), allh[k]))
    w("")
    n_stall = cnt.get('STALLED', 0)
    w("**Stall count: %d** of %d seeds in the `STALLED` class"
      % (n_stall, len(R)))
    w("(%d more sat in the degenerate `E_K = 1` collapse, %d converged, %d diverged)."
      % (cnt.get('STALLED-COLLAPSED', 0),
         cnt.get('CONVERGED-AUTOMORPHISM-LIKE', 0), cnt.get('DIVERGED', 0)))
    w("")

    # per-family
    w("### Plateau by initialisation family")
    w("")
    w("| family | decay | seeds | median E_K | min E_K |")
    w("|---|---|---|---|---|")
    for fam, dec in cfg['families']:
        rows = [x['EK'] for x in R if x['family'] == fam]
        if rows:
            w("| `%s` | %.2f | %d | %.4g | %.4g |"
              % (fam, dec, len(rows), float(np.median(rows)), min(rows)))
    w("")

    # ---------------- deepest stalls
    w("## 5. The ten deepest stalls")
    w("")
    w("Coefficient vectors are in `night11/stalls/*.npz` (keys: `c`, `dP`,")
    w("`dQ`, `t`, `aP`, `aQ`, `EK`, `ET`, `arm`, `seed`). No lifting was")
    w("attempted, per the v0 brief.")
    w("")
    w("| # | arm | seed | family | E_K | E_T | E_prop | grad norm of E_K | Jacobian norm | passes/iters |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    byseed = {(x['arm'], x['seed']): x for x in R}
    for d in N['deepest_stalls']:
        rec = byseed[(d['arm'], d['seed'])]
        w("| %d | `%s` | %d | %s | **%.6g** | %.4g | %.4g | %.3g | %.4g | %d/%d |"
          % (d['rank'], d['arm'], d['seed'], d['family'], d['EK_recorded'],
             d['ET'], rec.get('ETprop', float('nan')), d['gnorm_EK'],
             rec.get('jac_norm', float('nan')), rec.get('npass', 0), d['nit']))
    w("")
    w("Profiles (all post-hoc; none of this is in the objective):")
    w("")
    w("| # | residual constant `R[0,0]` | \\|P_top\\| | \\|Q_top\\| | Sylvester log10 cond | max abs coeff | total degrees carrying most residual mass |")
    w("|---|---|---|---|---|---|---|")
    for d in N['deepest_stalls']:
        deg = ", ".join("%d (%.2g)" % (k, v)
                        for k, v in d['resid_mass_top5_by_total_degree'][:4])
        w("| %d | %.4g | %.4g | %.4g | %s | %.4g | %s |"
          % (d['rank'], d['resid_const'], d['topform_norm_P'],
             d['topform_norm_Q'],
             ("%.2f" % d['sylvester_cond_log10']) if 'sylvester_cond_log10' in d else "n/a",
             d['coeff_absmax'], deg))
    w("")
    w("`R[0,0]` is the residual in the constant coefficient: a value near 0")
    w("means the seed did fit the Keller constant `1`; a value near `-1` means")
    w("it did not and the pair sits at or near the degenerate `Jacobian = 0`")
    w("locus.")
    w("")

    # ---------------- files
    w("## 6. Files")
    w("")
    w("| file | contents |")
    w("|---|---|")
    w("| `polykit.py` | float64 polynomial kernel: FFT product/correlation, Keller residual and its exact analytic gradient (4 forward + 5 inverse real FFTs per objective+gradient call), tear proxy and gradient, Sylvester diagnostic |")
    w("| `supports.py` | support design and the swappable objective |")
    w("| `opt.py` | descent driver (L-BFGS-B with relative tolerances off, restarts; Adam fallback) |")
    w("| `controls.py`, `controls.json`, `controls_log.txt` | N1/N2/N3 |")
    w("| `net.py`, `net_results.json`, `net_log.txt` | the search; one record per seed |")
    w("| `stalls/*.npz` | coefficient vectors of the ten deepest stalls |")
    w("| `report.py` | builds this file |")
    w("")

    open(os.path.join(HERE, 'NUMERIC_NET.md'), 'w').write("\n".join(L) + "\n")
    print("wrote NUMERIC_NET.md (%d lines)" % len(L))


if __name__ == '__main__':
    main()
