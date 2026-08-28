"""night11 -- post-hoc diagnostics on the deepest stalls.

Two labelled experiments per stall, run AFTER the net, never inside it:

  D1  Sylvester singular-value diagnostic on the two leading forms
      (polykit.sylvester_sigma), reported in full: sigma_max, sigma_min,
      log10 condition number, and the tail of the spectrum.

  D2  RATIONAL-RECONSTRUCTION EXPERIMENT (labelled as such).  The k dominant
      coefficients of the stall vector (largest |c|) are passed through
      sympy.nsimplify with a bounded rational tolerance; every other
      coefficient is taken as the exact dyadic rational the float already is.
      The resulting vector is EXACTLY rational, so the bracket
          B = P_x Q_y - P_y Q_x
      can be formed exactly over Q by integer/Fraction convolution, and the
      exact residual  B - 1  is reported as an exact object: its number of
      nonzero coefficients, its exact constant term, and the exact rational
      with the largest absolute value.  A nonzero exact residual is the
      expected outcome and carries no information beyond "this float point is
      not an exact solution".  An identically zero exact residual would be a
      separate matter and is flagged for halt.

Usage:  python3 diag.py [n_stalls] [n_dominant]
"""

import json
import os
import sys
import time
from fractions import Fraction

import numpy as np

from polykit import sylvester_sigma, top_form
from supports import Support

HERE = os.path.dirname(os.path.abspath(__file__))
STALLDIR = os.path.join(HERE, 'stalls')


# --------------------------------------------------------------- exact layer

def to_dict(A):
    """Dense float/Fraction array -> {(i,j): Fraction} with zeros dropped."""
    out = {}
    n0, n1 = A.shape
    for i in range(n0):
        row = A[i]
        for j in range(n1):
            v = row[j]
            if v:
                out[(i, j)] = v if isinstance(v, Fraction) else Fraction(v)
    return out


def d_dx(D):
    return {(i - 1, j): i * v for (i, j), v in D.items() if i}


def d_dy(D):
    return {(i, j - 1): j * v for (i, j), v in D.items() if j}


def mul(A, B):
    out = {}
    for (i, j), a in A.items():
        for (k, l), b in B.items():
            key = (i + k, j + l)
            p = a * b
            if key in out:
                out[key] += p
            else:
                out[key] = p
    return out


def sub(A, B):
    out = dict(A)
    for k, v in B.items():
        if k in out:
            out[k] -= v
        else:
            out[k] = -v
    return out


def exact_bracket_residual(Pd, Qd):
    """B - 1 with B = P_x Q_y - P_y Q_x, all exact.  Returns dict of nonzeros."""
    R = sub(mul(d_dx(Pd), d_dy(Qd)), mul(d_dy(Pd), d_dx(Qd)))
    R[(0, 0)] = R.get((0, 0), Fraction(0)) - 1
    return {k: v for k, v in R.items() if v}


# ------------------------------------------------------------- reconstruction

def rationalise(c, n_dominant, rational_tol=1e-6, max_denom=10 ** 6):
    """Return (list of Fractions, list of reconstruction records)."""
    import sympy as sp

    vals = [Fraction(float(x)) for x in c]           # exact dyadic by default
    order = np.argsort(-np.abs(c))[:n_dominant]
    recs = []
    for idx in order:
        x = float(c[idx])
        rec = dict(index=int(idx), float_value=x)
        try:
            r = sp.nsimplify(sp.Float(x, 17), rational=True, tolerance=rational_tol)
            r = sp.Rational(r)
            if abs(r.q) <= max_denom:
                fr = Fraction(int(r.p), int(r.q))
                vals[idx] = fr
                rec.update(reconstructed='%d/%d' % (fr.numerator, fr.denominator),
                           abs_error=abs(float(fr) - x), substituted=True)
            else:
                rec.update(reconstructed='%s' % r,
                           abs_error=abs(float(r) - x), substituted=False,
                           note='denominator above bound')
        except Exception as exc:
            rec.update(reconstructed=None, substituted=False,
                       note=repr(exc)[:100])
        recs.append(rec)
    return vals, recs


# ------------------------------------------------------------------- per-file

def run_one(fn, n_dominant):
    z = np.load(fn)
    c = z['c']
    dP, dQ = int(z['dP']), int(z['dQ'])
    sup = Support(dP, dQ, int(z['t']), int(z['aP']), int(z['aQ']))
    P, Q = sup.unpack(c)

    out = dict(file=os.path.basename(fn), arm=str(z['arm']), seed=int(z['seed']),
               EK_recorded=float(z['EK']), ET_recorded=float(z['ET']),
               n_params=int(sup.n))

    # -------- D1 Sylvester
    tP, tQ = top_form(P, dP), top_form(Q, dQ)
    sv = sylvester_sigma(tP, tQ)
    if sv is None:
        out['D1_sylvester'] = None
    else:
        out['D1_sylvester'] = dict(
            dim=int(len(sv)),
            sigma_max=float(sv[0]), sigma_min=float(sv[-1]),
            log10_cond=float(np.log10(sv[0] / max(sv[-1], 1e-300))),
            smallest_five=[float(v) for v in sv[-5:]],
            topform_deg_P=int(np.count_nonzero(tP)),
            topform_deg_Q=int(np.count_nonzero(tQ)))

    # -------- D2 rational reconstruction (labelled experiment)
    t0 = time.time()
    vals, recs = rationalise(c, n_dominant)
    Pf = np.empty(P.shape, dtype=object); Pf[:] = Fraction(0)
    Qf = np.empty(Q.shape, dtype=object); Qf[:] = Fraction(0)
    Pf.ravel()[sup.iP] = vals[:sup.nP]
    Qf.ravel()[sup.iQ] = vals[sup.nP:]
    R = exact_bracket_residual(to_dict(Pf), to_dict(Qf))
    biggest = max(R.items(), key=lambda kv: abs(kv[1])) if R else None
    const = R.get((0, 0), Fraction(0))
    out['D2_rational_reconstruction'] = dict(
        n_dominant_attempted=len(recs),
        n_substituted=sum(1 for r in recs if r.get('substituted')),
        reconstructions=recs,
        exact_residual_nonzero_cells=len(R),
        exact_residual_identically_zero=(len(R) == 0),
        exact_residual_constant_term=str(const),
        exact_residual_max_abs_float=(float(abs(biggest[1])) if biggest else 0.0),
        exact_residual_max_abs_cell=(list(biggest[0]) if biggest else None),
        exact_seconds=time.time() - t0)
    return out


def main():
    n_stalls = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    n_dom = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    files = sorted(f for f in os.listdir(STALLDIR) if f.endswith('.npz'))[:n_stalls]
    res = []
    for f in files:
        print('diag %s ...' % f, flush=True)
        r = run_one(os.path.join(STALLDIR, f), n_dom)
        print('   exact residual nonzero cells: %d' %
              r['D2_rational_reconstruction']['exact_residual_nonzero_cells'],
              flush=True)
        res.append(r)
    with open(os.path.join(HERE, 'diag_results.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    hits = [r for r in res
            if r['D2_rational_reconstruction']['exact_residual_identically_zero']]
    print('done; %d files, %d with identically-zero exact residual'
          % (len(res), len(hits)))


if __name__ == '__main__':
    main()
