import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
"""night11 -- mandatory controls N1, N2, N3 for the numeric net.

Run:  python3 controls.py     (writes controls.json, prints a log)
"""

import json
import time

import numpy as np

from polykit import (conv2, conv2_direct, keller_residual,
                     keller_residual_slow, keller_energy_grad, top_form,
                     tear_energy_grad)
from supports import Support, Objective

from opt import descend, HAVE_SCIPY

RES = {}
LOG = []


def say(s):
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ N1


def n1_symbolic():
    """Symbolic (sympy, exact rationals) vs numeric Keller residual, plus a
    direct-vs-FFT convolution check and an analytic-vs-finite-difference
    gradient check."""
    import sympy as sp
    rng = np.random.default_rng(11001)
    dP, dQ = 3, 4
    P = np.zeros((dP + 1, dP + 1))
    Q = np.zeros((dQ + 1, dQ + 1))
    for i in range(dP + 1):
        for j in range(dP + 1 - i):
            P[i, j] = np.round(rng.normal(), 6)
    for i in range(dQ + 1):
        for j in range(dQ + 1 - i):
            Q[i, j] = np.round(rng.normal(), 6)

    x, y = sp.symbols('x y')
    Ps = sum(sp.Rational(str(P[i, j])) * x**i * y**j
             for i in range(dP + 1) for j in range(dP + 1))
    Qs = sum(sp.Rational(str(Q[i, j])) * x**i * y**j
             for i in range(dQ + 1) for j in range(dQ + 1))
    Js = sp.expand(sp.diff(Ps, x) * sp.diff(Qs, y)
                   - sp.diff(Ps, y) * sp.diff(Qs, x) - 1)
    poly = sp.Poly(Js, x, y)

    R = keller_residual(P, Q)
    err = 0.0
    checked = 0
    for (i, j), co in zip(poly.monoms(), poly.coeffs()):
        err = max(err, abs(float(co) - R[i, j]))
        checked += 1
    # and every coefficient the symbolic side does not list must be ~0
    S = np.zeros_like(R)
    for (i, j), co in zip(poly.monoms(), poly.coeffs()):
        S[i, j] = float(co)
    err_all = float(np.max(np.abs(R - S)))

    # fused-FFT residual vs the explicit-convolution reference path
    fused_err = float(np.max(np.abs(keller_residual_slow(P, Q)
                                    - R[:dP + dQ + 1, :dP + dQ + 1])))

    # direct vs FFT convolution at a larger size
    A = rng.normal(size=(40, 40)) * np.tri(40)[::-1].T
    B = rng.normal(size=(60, 60)) * np.tri(60)[::-1].T
    cd = conv2_direct(A, B)
    cf = conv2(A, B)
    conv_err = float(np.max(np.abs(cd - cf)) / np.max(np.abs(cd)))

    # analytic gradient vs central finite differences (small support)
    sup = Support(4, 6, 1)
    obj = Objective(sup, lambda_T=0.3)
    c = rng.normal(size=sup.n) * 0.3
    E0, g = obj(c)
    gfd = np.zeros(sup.n)
    h = 1e-6
    for k in range(sup.n):
        cp = c.copy(); cp[k] += h
        cm = c.copy(); cm[k] -= h
        gfd[k] = (obj(cp)[0] - obj(cm)[0]) / (2 * h)
    grad_err = float(np.max(np.abs(g - gfd)) / max(1.0, np.max(np.abs(gfd))))

    say("N1  symbolic-vs-numeric Keller residual  (deg 3, deg 4)")
    say("      monomials compared              : %d" % checked)
    say("      max |sympy - numeric| (listed)  : %.3e" % err)
    say("      max |sympy - numeric| (all cells): %.3e" % err_all)
    say("      fused-vs-reference residual err : %.3e" % fused_err)
    say("      direct-vs-FFT conv rel error    : %.3e" % conv_err)
    say("      analytic-vs-FD gradient rel err : %.3e  (%d params)"
        % (grad_err, sup.n))
    RES['N1'] = dict(monomials=checked, max_abs_err=err, max_abs_err_all=err_all,
                     conv_rel_err=conv_err, grad_rel_err=grad_err,
                     fused_vs_reference=fused_err,
                     pass_=bool(err_all < 1e-10 and conv_err < 1e-10
                                and grad_err < 1e-6))
    say("      N1 PASS" if RES['N1']['pass_'] else "      N1 FAIL")


# ------------------------------------------------------------------ N2


def automorphism(dP_target, k, coeffs_f, coeffs_g):
    """P = x + f(y) with deg f = a; Q = y + g(P) with deg g = k.
    Jacobian is identically 1.  Degrees: (a, a*k)."""
    a = len(coeffs_f) - 1
    dP = a
    dQ = a * k
    P = np.zeros((dP + 1, dP + 1))
    P[1, 0] = 1.0
    for e, c in enumerate(coeffs_f):
        if c != 0.0:
            P[0, e] += c
    # Q = y + sum_r g_r P^r   (P^r by repeated convolution, truncated to dQ)
    Q = np.zeros((dQ + 1, dQ + 1))
    Q[0, 1] = 1.0
    Pw = np.zeros((dQ + 1, dQ + 1))
    Pw[0, 0] = 1.0
    Pbig = np.zeros((dQ + 1, dQ + 1))
    Pbig[:dP + 1, :dP + 1] = P
    for r in range(0, k + 1):
        if r > 0:
            C = conv2(Pw, Pbig)
            Pw = np.zeros((dQ + 1, dQ + 1))
            s0 = min(dQ + 1, C.shape[0]); s1 = min(dQ + 1, C.shape[1])
            Pw[:s0, :s1] = C[:s0, :s1]
        if r < len(coeffs_g) and coeffs_g[r] != 0.0:
            Q += coeffs_g[r] * Pw
    assert dP == dP_target, (dP, dP_target)
    return P, Q, dP, dQ


def _run(obj, c0, maxiter):
    c, E, nit, npass, msg = descend(obj, c0, maxiter)
    return c, E, nit


def n2_automorphism_basin():
    rng = np.random.default_rng(11002)
    out = {}

    # --- N2a: small automorphism, degrees (4, 8)
    f = np.zeros(5); f[4] = 1.0; f[2] = 0.31; f[1] = -0.7
    g = np.array([0.0, 0.0, 0.62])
    P, Q, dP, dQ = automorphism(4, 2, f, g)
    R0 = keller_residual(P, Q)
    sup = Support(dP, dQ, 1)
    obj = Objective(sup, lambda_T=0.0)
    c_star = sup.pack(P, Q)
    EK_star = obj(c_star)[0]
    c0 = c_star + rng.normal(size=sup.n) * 1e-3
    t0 = time.time()
    c1, E1, nit = _run(obj, c0, 6000)
    out['N2a'] = dict(degrees=[dP, dQ], nparam=sup.n,
                      EK_at_exact=float(EK_star),
                      EK_at_perturbed_start=float(obj(c0)[0]),
                      EK_final=float(E1), nit=nit, secs=time.time() - t0,
                      max_resid_exact=float(np.max(np.abs(R0))))
    say("N2a automorphism (deg 4, deg 8), %d params" % sup.n)
    say("      E_K at exact automorphism      : %.3e" % EK_star)
    say("      E_K at perturbed start (1e-3)  : %.3e" % out['N2a']['EK_at_perturbed_start'])
    say("      E_K after L-BFGS-B (%4d iters) : %.3e" % (nit, E1))

    # --- N2b: large automorphism at the campaign scale, degrees (84, 168)
    f = np.zeros(85)
    f[84] = 1.0
    f[40] = 0.4
    f[3] = -0.25
    f[1] = 0.9
    g = np.array([0.0, 0.0, 0.5])
    P, Q, dP, dQ = automorphism(84, 2, f, g)
    sup = Support(dP, dQ, 1)
    obj = Objective(sup, lambda_T=0.0)
    c_star = sup.pack(P, Q)
    EK_star = obj(c_star)[0]
    c0 = c_star.copy()
    pert = rng.normal(size=sup.n) * 1e-8
    c0 = c0 + pert
    t0 = time.time()
    c1, E1, nit = _run(obj, c0, 4000)
    out['N2b'] = dict(degrees=[dP, dQ], nparam=sup.n,
                      EK_at_exact=float(EK_star),
                      EK_at_perturbed_start=float(obj(c0)[0]),
                      EK_final=float(E1), nit=nit, secs=time.time() - t0)
    say("N2b automorphism (deg 84, deg 168), %d params" % sup.n)
    say("      E_K at exact automorphism      : %.3e" % EK_star)
    say("      E_K at perturbed start (1e-8)  : %.3e" % out['N2b']['EK_at_perturbed_start'])
    say("      E_K after L-BFGS-B (%4d iters) : %.3e  [%.1f s]"
        % (nit, E1, out['N2b']['secs']))

    say("      NOTE  the campaign degree shape (2m, 3m) = (84, 126) admits no")
    say("            automorphism at all: by Jung-van der Kulk every planar")
    say("            polynomial automorphism is tame and its two degrees are")
    say("            divisibility-ordered, while 84 does not divide 126 and")
    say("            126 does not divide 84.  N2 is therefore run at (84, 168),")
    say("            the nearest same-scale shape that does carry one.")
    RES['N2'] = out


# ------------------------------------------------------------------ N3


def n3_small_random():
    rng = np.random.default_rng(11003)
    out = {}
    for tag, (dP, dQ) in [('4_8', (4, 8)), ('2_4', (2, 4)), ('4_6', (4, 6))]:
        sup = Support(dP, dQ, 1)
        obj = Objective(sup, lambda_T=0.0)
        fin = []
        for s in range(12):
            c0 = rng.normal(size=sup.n) * 0.5
            c1, E1, nit = _run(obj, c0, 2000)
            fin.append(float(E1))
        fin = np.array(fin)
        out[tag] = dict(degrees=[dP, dQ], nparam=sup.n, seeds=len(fin),
                        n_machine_precision=int((fin < 1e-18).sum()),
                        median=float(np.median(fin)), best=float(fin.min()),
                        finals=[float(v) for v in fin])
        say("N3  degrees (%d, %d), %d params, %d random seeds: %d reached"
            " E_K < 1e-18, best %.3e, median %.3e"
            % (dP, dQ, sup.n, len(fin), out[tag]['n_machine_precision'],
               fin.min(), np.median(fin)))
    say("      (4,8) and (2,4) are shapes d | 2d where automorphisms are")
    say("      abundant; (4,6) is the mission shape (2m,3m) at m=2, where")
    say("      the same divisibility obstruction as at (84,126) applies.")
    RES['N3'] = out


def main():
    t0 = time.time()
    say("night11 numeric net -- controls   (scipy=%s)" % HAVE_SCIPY)
    RES['support'] = {}
    for name, t, aP, aQ in [('GRADED-5', 5, 1, 4), ('GRADED-15', 15, 1, 14),
                            ('FULL', 1, 0, 0)]:
        sup = Support(84, 126, t, aP, aQ)
        tp, tq = sup.n_topform()
        say("support %-10s deg(84,126) t=%2d (aP=%d,aQ=%d): %5d+%5d = %5d params,"
            " %5d residual cells, top-form dims (%d,%d)"
            % (name, t, aP, aQ, sup.nP, sup.nQ, sup.n,
               sup.n_residual_cells(), tp, tq))
        RES['support'][name] = dict(t=t, aP=aP, aQ=aQ, nP=sup.nP, nQ=sup.nQ,
                                    n=sup.n, residual_cells=sup.n_residual_cells(),
                                    topform_dims=[tp, tq])
    n1_symbolic()
    n2_automorphism_basin()
    n3_small_random()
    RES['wall_seconds'] = time.time() - t0
    say("total %.1f s" % RES['wall_seconds'])
    with open('controls.json', 'w') as fh:
        json.dump(dict(results=RES, log=LOG), fh, indent=1)


if __name__ == '__main__':
    main()
