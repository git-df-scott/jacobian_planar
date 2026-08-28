"""night11 -- support design and the (swappable) objective.

SUPPORT DESIGN
==============
Target degree shape: deg P = 2m, deg Q = 3m, with m = 42, i.e. (84, 126).

1) Newton-triangle similarity.  Both supports sit in triangles
      supp(P) subset Delta(2m) = conv{(0,0), (2m,0), (0,2m)}
      supp(Q) subset Delta(3m) = (3/2) * Delta(2m),
   one Newton triangle and a scaled copy of it.  Taken alone that is
   3655 + 8128 = 11783 real parameters -- too many for a many-restart net.

2) Torus grading.  Let zeta be a primitive t-th root of unity and act by
      sigma_zeta : (x, y) --> (zeta * x, zeta^{-1} * y).
   A monomial x^i y^j has weight (i - j) mod t.  We take P and Q to be
   semi-invariant of weights aP and aQ:
      supp(P) subset { (i,j) : i - j = aP  (mod t) },
      supp(Q) subset { (i,j) : i - j = aQ  (mod t) }.
   These are cosets of the index-t sublattice L_t = {i - j = 0 (mod t)}, not
   L_t itself.  The Jacobian of a weight-aP and a weight-aQ polynomial has
   weight aP + aQ, so the residual P_x Q_y - P_y Q_x - 1 stays inside one
   coset provided aP + aQ = 0 (mod t).

3) Which gradings are admissible.  Two constraints pin the weights down.

   (a) Keller normalisation.  The (0,0) coefficient of P_x Q_y - P_y Q_x is
       P[1,0] Q[0,1] - P[0,1] Q[1,0], and nothing else -- it is the only way
       to reach total degree 0.  So the constant 1 is reachable ONLY if
       (1,0) is in supp(P) and (0,1) is in supp(Q) (or the mirror), i.e.
            aP = 1,  aQ = -1  (mod t).
       Any other choice forces E_K >= 1 identically, with equality exactly on
       the degenerate locus P_x Q_y - P_y Q_x = 0.  (This was measured, not
       assumed: an earlier run with aP = aQ = 0 drove every seed to
       E_K = 1.0000000 with ||Jacobian|| ~ 2e-4.)

   (b) Leading-form shape.  The (H^2, H^3) shape wanted by the tear proxy
       needs a form H of some weight w with 2w = aP and 3w = aQ (mod t).
       With aP = 1, aQ = -1 this gives 2w = 1 and 3w = -1, hence w = -2 and
       then -4 = 1 (mod t), i.e.  t divides 5.
       So t = 5 is the ONLY nontrivial torus grading compatible with both the
       Keller constant and the (H^2, H^3) leading-form shape;  w = 3 works
       (2*3 = 6 = 1, 3*3 = 9 = 4 = -1 mod 5).

   Consequence for the parameter budget: the requested 300-800 band is not
   reachable by a grading that keeps both constraints.  The net therefore runs
   two arms:
      GRADED-5   t = 5,  aP = 1, aQ = 4 -- both constraints hold; 2357 params
                 (above the 300-800 target band, and recorded as such);
      GRADED-15  t = 15, aP = 1, aQ = 14 -- Keller constant reachable, the
                 (H^2, H^3) shape NOT reachable (no valid w); 788 params,
                 inside the target band.  Its E_T can therefore not go to 0,
                 which is itself the measurement.
   A third small arm FULL (t = 1, 11783 params) is used only by the controls.

4) Over-determination.  The residual lives on
      { (i,j) : i + j <= 2m + 3m - 2 = 208, i - j = aP + aQ = 0 (mod t) },
   so the count of equations and the count of unknowns both scale like 1/t and
   the ratio (unknowns / equations) ~ 0.537 is independent of t.  t is a
   resolution knob, not a knob on how over-determined the Keller system is.

OBJECTIVE
=========
    E(c) = E_K + lambda_T * E_T
E_K is the exact sum of squares of the coefficients of P_x Q_y - P_y Q_x - 1
(FFT convolution, checked against sympy and against a direct product in N1).
E_T is documented in polykit.tear_energy_grad.  The objective is a small
object so a refined E_T can be dropped in without touching the net.
"""

import numpy as np

from polykit import (keller_energy_grad, tear_energy_grad, top_form,
                     scatter_top)


class Support:
    def __init__(self, dP, dQ, t, aP=1, aQ=-1):
        self.dP, self.dQ, self.t = dP, dQ, t
        self.aP, self.aQ = aP % t if t > 1 else 0, aQ % t if t > 1 else 0
        self.maskP = self._mask(dP, t, aP)
        self.maskQ = self._mask(dQ, t, aQ)
        self.iP = np.flatnonzero(self.maskP.ravel())
        self.iQ = np.flatnonzero(self.maskQ.ravel())
        self.nP = self.iP.size
        self.nQ = self.iQ.size
        self.n = self.nP + self.nQ

    @staticmethod
    def _mask(d, t, a):
        I, J = np.meshgrid(np.arange(d + 1), np.arange(d + 1), indexing='ij')
        m = (I + J <= d)
        if t > 1:
            m &= ((I - J - a) % t == 0)
        return m

    def n_residual_cells(self):
        d = self.dP + self.dQ - 2
        I, J = np.meshgrid(np.arange(d + 1), np.arange(d + 1), indexing='ij')
        m = (I + J <= d)
        if self.t > 1:
            m &= ((I - J - (self.aP + self.aQ)) % self.t == 0)
        return int(m.sum())

    def n_topform(self):
        return int(self.maskP[np.arange(self.dP + 1),
                              self.dP - np.arange(self.dP + 1)].sum()), \
               int(self.maskQ[np.arange(self.dQ + 1),
                              self.dQ - np.arange(self.dQ + 1)].sum())

    def unpack(self, c):
        P = np.zeros((self.dP + 1, self.dP + 1))
        Q = np.zeros((self.dQ + 1, self.dQ + 1))
        P.ravel()[self.iP] = c[:self.nP]
        Q.ravel()[self.iQ] = c[self.nP:]
        return P, Q

    def pack(self, P, Q):
        return np.concatenate([P.ravel()[self.iP], Q.ravel()[self.iQ]])

    def pack_grad(self, gP, gQ):
        return np.concatenate([gP.ravel()[self.iP], gQ.ravel()[self.iQ]])


class Objective:
    """E = E_K + lambda_T * E_T.  Swap `tear` for a refined proxy later."""

    def __init__(self, sup, lambda_T=0.0, tear=tear_energy_grad, tau=1e-2):
        self.sup = sup
        self.lambda_T = lambda_T
        self.tear = tear
        self.tau = tau

    def parts(self, c):
        sup = self.sup
        P, Q = sup.unpack(c)
        EK, gP, gQ, R = keller_energy_grad(P, Q)
        ET = ETp = ETn = 0.0
        if self.lambda_T != 0.0:
            tP = top_form(P, sup.dP)
            tQ = top_form(Q, sup.dQ)
            ET, gtP, gtQ, ETp, ETn = self.tear(tP, tQ, tau=self.tau)
            gP = gP + self.lambda_T * scatter_top(gtP, sup.dP, P.shape)
            gQ = gQ + self.lambda_T * scatter_top(gtQ, sup.dQ, Q.shape)
        g = sup.pack_grad(gP, gQ)
        return EK, ET, ETp, ETn, g

    def __call__(self, c):
        EK, ET, _, _, g = self.parts(c)
        E = EK + self.lambda_T * ET
        if not np.isfinite(E):
            return 1e300, np.zeros_like(c)
        return E, g

    def tear_only(self, c):
        sup = self.sup
        P, Q = sup.unpack(c)
        tP = top_form(P, sup.dP)
        tQ = top_form(Q, sup.dQ)
        ET, _, _, ETp, ETn = self.tear(tP, tQ, tau=self.tau)
        return ET, ETp, ETn
