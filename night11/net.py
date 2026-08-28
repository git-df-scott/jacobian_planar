"""night11 -- the numeric net (v0).

Continuous optimization of E(c) = E_K + lambda_T * E_T over real coefficient
vectors for pairs (P, Q) of degrees (84, 126) on the torus-graded
triangular supports described in supports.py.  Many random restarts, run in
parallel over the machine's cores.  v0 maps the landscape only: every seed is
run, classified and recorded, and nothing is lifted or certified.

Usage:  python3 net.py [n_seeds] [maxiter]
"""

import json
import os
import sys
import time
import multiprocessing as mp

import numpy as np

from polykit import keller_residual, top_form, sylvester_sigma
from supports import Support, Objective

try:
    from scipy.optimize import minimize
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

DP, DQ = 84, 126
HERE = os.path.dirname(os.path.abspath(__file__))
STALLDIR = os.path.join(HERE, 'stalls')

# initialisation families: sigma_{ij} = decay^(i+j), then a global rescale
FAMILIES = [
    ('flat', 1.00),
    ('mild', 0.96),
    ('steep', 0.90),
    ('vsteep', 0.82),
]

# (name, t, aP, aQ, lambda_T).  See supports.py for why t=5 and t=15 are the
# two gradings worth running: t=5 is the only nontrivial one compatible with
# BOTH the Keller constant and the (H^2,H^3) leading-form shape; t=15 keeps the
# Keller constant, drops the leading-form shape, and lands inside the requested
# 300-800 parameter band.
ARMS = [
    ('G5_lamT0',    5, 1, 4,  0.0),
    ('G5_lamT1e-3', 5, 1, 4,  1e-3),
    ('G15_lamT0',  15, 1, 14, 0.0),
]


def make_seed(sup, seed, decay):
    rng = np.random.default_rng(seed)
    P = np.zeros((sup.dP + 1, sup.dP + 1))
    Q = np.zeros((sup.dQ + 1, sup.dQ + 1))
    I, J = np.meshgrid(np.arange(sup.dP + 1), np.arange(sup.dP + 1),
                       indexing='ij')
    P[sup.maskP] = (rng.normal(size=int(sup.maskP.sum()))
                    * decay ** (I + J)[sup.maskP])
    I, J = np.meshgrid(np.arange(sup.dQ + 1), np.arange(sup.dQ + 1),
                       indexing='ij')
    Q[sup.maskQ] = (rng.normal(size=int(sup.maskQ.sum()))
                    * decay ** (I + J)[sup.maskQ])
    # global rescale P -> sP, Q -> sQ so that ||P_x Q_y - P_y Q_x|| ~ 1
    Rj = keller_residual(P, Q)
    Rj[0, 0] += 1.0
    nrm = float(np.sqrt(np.sum(Rj * Rj)))
    if nrm > 0 and np.isfinite(nrm):
        s = nrm ** -0.25
        P *= s
        Q *= s
    return sup.pack(P, Q)


def adam(obj, c0, iters, lr=3e-3):
    c = c0.copy(); m = np.zeros_like(c); v = np.zeros_like(c)
    for t in range(1, iters + 1):
        E, g = obj(c)
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        c = c - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-12)
    return c, iters, 'adam'


def run_one(task):
    arm, t, aP, aQ, lamT, seed, fam, decay, maxiter = task
    sup = Support(DP, DQ, t, aP, aQ)
    obj = Objective(sup, lambda_T=lamT)
    t0 = time.time()
    c0 = make_seed(sup, seed, decay)
    EK0 = obj.parts(c0)[0]
    status = 'ok'
    try:
        if HAVE_SCIPY:
            r = minimize(obj, c0, jac=True, method='L-BFGS-B',
                         options=dict(maxiter=maxiter, maxfun=3 * maxiter,
                                      ftol=1e-18, gtol=1e-16, maxcor=15))
            c1, nit, status = r.x, int(r.nit), str(r.message)[:60]
        else:
            c1, nit, status = adam(obj, c0, maxiter)
    except Exception as exc:  # pragma: no cover
        return dict(arm=arm, seed=seed, family=fam, cls='DIVERGED',
                    error=repr(exc)[:120], secs=time.time() - t0)

    EK, ET, ETp, ETn, g = obj.parts(c1)
    # gradient of E_K alone (lambda_T = 0) at the end point
    gK = Objective(sup, lambda_T=0.0).parts(c1)[4]
    gn = float(np.linalg.norm(g))
    gKn = float(np.linalg.norm(gK))
    cn = float(np.linalg.norm(c1))

    if not np.isfinite(EK) or EK > 1e6 or not np.isfinite(cn):
        cls = 'DIVERGED'
    elif EK < 1e-18:
        cls = 'CONVERGED-AUTOMORPHISM-LIKE'
    else:
        cls = 'STALLED'

    rec = dict(arm=arm, t=t, aP=aP, aQ=aQ, lambda_T=lamT, seed=seed,
               family=fam, decay=decay,
               EK0=float(EK0), EK=float(EK), ET=float(ET), ETprop=float(ETp),
               ETnd=float(ETn), gnorm=gn, gnorm_EK=gKn, cnorm=cn,
               nit=nit, status=status, cls=cls, secs=time.time() - t0)
    if cls == 'STALLED':
        rec['_c'] = c1
    return rec


def profile(sup, c):
    """Post-hoc profile of one stalled point (not part of the objective)."""
    P, Q = sup.unpack(c)
    R = keller_residual(P, Q)
    d = sup.dP + sup.dQ - 2
    by_deg = {}
    I, J = np.meshgrid(np.arange(R.shape[0]), np.arange(R.shape[1]),
                       indexing='ij')
    S = I + J
    for k in range(d + 1):
        m = (S == k)
        v = float(np.sum(R[m] ** 2))
        if v > 0:
            by_deg[k] = v
    top5 = sorted(by_deg.items(), key=lambda kv: -kv[1])[:5]
    tP, tQ = top_form(P, sup.dP), top_form(Q, sup.dQ)
    sv = sylvester_sigma(tP, tQ)
    out = dict(EK=float(np.sum(R * R)),
               resid_const=float(R[0, 0]),
               resid_mass_top5_by_total_degree=[[int(k), v] for k, v in top5],
               topform_norm_P=float(np.linalg.norm(tP)),
               topform_norm_Q=float(np.linalg.norm(tQ)),
               coeff_absmax=float(np.max(np.abs(c))))
    if sv is not None:
        out['sylvester_sigma_min'] = float(sv[-1])
        out['sylvester_sigma_max'] = float(sv[0])
        out['sylvester_cond_log10'] = float(np.log10(sv[0] / max(sv[-1], 1e-300)))
    return out


def main():
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    maxiter = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    os.makedirs(STALLDIR, exist_ok=True)

    tasks = []
    for arm, t, aP, aQ, lamT in ARMS:
        for k in range(n_seeds):
            fam, decay = FAMILIES[k % len(FAMILIES)]
            tasks.append((arm, t, aP, aQ, lamT, 110000 + k, fam, decay,
                          maxiter))

    t0 = time.time()
    ncpu = min(4, os.cpu_count() or 1)
    for arm, t, aP, aQ, lamT in ARMS:
        s = Support(DP, DQ, t, aP, aQ)
        print("  arm %-12s t=%2d (aP=%d,aQ=%d) lambda_T=%g: %d params,"
              " %d residual cells" % (arm, t, aP, aQ, lamT, s.n,
                                      s.n_residual_cells()), flush=True)
    print("night11 net: %d tasks on %d cores" % (len(tasks), ncpu), flush=True)
    recs = []
    with mp.Pool(ncpu) as pool:
        for i, rec in enumerate(pool.imap_unordered(run_one, tasks, chunksize=1)):
            recs.append(rec)
            if (i + 1) % 10 == 0:
                print("  %d/%d  (%.0f s)" % (i + 1, len(tasks), time.time() - t0),
                      flush=True)
    wall = time.time() - t0

    # deepest stalls -> stalls/
    stalls = [r for r in recs if r['cls'] == 'STALLED']
    stalls.sort(key=lambda r: r['EK'])
    deepest = []
    for rank, r in enumerate(stalls[:10]):
        c = r['_c']
        sup = Support(DP, DQ, r['t'], r['aP'], r['aQ'])
        fn = os.path.join(STALLDIR, 'stall_%02d_%s_seed%d.npz'
                          % (rank + 1, r['arm'], r['seed']))
        np.savez_compressed(fn, c=c, dP=DP, dQ=DQ, t=r['t'], aP=r['aP'],
                            aQ=r['aQ'], EK=r['EK'], ET=r['ET'],
                            arm=r['arm'], seed=r['seed'])
        p = profile(sup, c)
        p.update(rank=rank + 1, file=os.path.basename(fn), arm=r['arm'],
                 seed=r['seed'], family=r['family'], EK_recorded=r['EK'],
                 ET=r['ET'], gnorm_EK=r['gnorm_EK'], nit=r['nit'],
                 status=r['status'])
        deepest.append(p)

    for r in recs:
        r.pop('_c', None)

    out = dict(config=dict(dP=DP, dQ=DQ,
                           n_seeds_per_arm=n_seeds, maxiter=maxiter,
                           arms=[list(a) for a in ARMS],
                           families=[list(f) for f in FAMILIES],
                           scipy=HAVE_SCIPY),
               wall_seconds=wall, records=recs, deepest_stalls=deepest)
    with open(os.path.join(HERE, 'net_results.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print("done in %.1f s; %d records" % (wall, len(recs)))


if __name__ == '__main__':
    main()
