"""night11 -- support design and the (swappable) objective.

SUPPORT DESIGN
==============
Target degree shape: deg P = 2m, deg Q = 3m, with m = 42, i.e. (84, 126).

1) Newton-triangle similarity.  Both supports sit in triangles
      supp(P) subset Delta(2m) = conv{(0,0), (2m,0), (0,2m)}
      supp(Q) subset Delta(3m) = (3/2) * Delta(2m),
   i.e. one Newton triangle and a scaled copy of it.  Taken alone this is
   3655 + 8128 = 11783 real parameters -- too many for a many-restart net.

2) Diagonal-congruence sublattice L_t.  We additionally restrict both supports
   to
      L_t = { (i, j) : i - j = 0  (mod t) },
   a rank-2 sublattice of Z^2 of index t.  L_t is exactly the set of
   exponents of monomials invariant under the torus action
      (x, y) --> (zeta * x, zeta^{-1} * y),   zeta^t = 1,
   so this is the ansatz "P and Q are Z/t-invariant".  The restriction is
   self-consistent for the Keller equation:
      * (1,1) in L_t, so d/dx and d/dy shift the class by an element of L_t;
      * L_t is closed under addition, so products stay in L_t;
      * (0,0) in L_t, so the target constant 1 is reachable.
   Hence for P, Q supported in L_t the whole residual P_x Q_y - P_y Q_x - 1
   is supported in L_t as well, and nothing is thrown away by construction.

   With t = 16 this gives 233 free coefficients for P and 512 for Q,
   745 real parameters in total (target band was 300-800).

3) Over-determination.  The residual lives on
      { (i,j) in L_t : i + j <= 2m + 3m - 2 = 208 },
   which has 1379 lattice points.  So the net always searches a 745-parameter
   space against 1379 equations; the ratio 745/1379 = 0.54 is independent of t
   (both counts scale like 1/t), so t is a resolution knob only, not a knob on
   how over-determined the Keller system is.

OBJECTIVE
=========
    E(c) = E_K + lambda_T * E_T
E_K is the exact sum of squares of the coefficients of P_x Q_y - P_y Q_x - 1
(FFT convolution, verified against a direct/symbolic product in control N1).
E_T is documented in polykit.tear_energy_grad.  The objective is passed around
as a small object so a refined E_T can be dropped in without touching the net.
"""

import numpy as np

from polykit import (keller_energy_grad, tear_energy_grad, top_form,
                     scatter_top)


class Support:
    def __init__(self, dP, dQ, t):
        self.dP, self.dQ, self.t = dP, dQ, t
        self.maskP = self._mask(dP, t)
        self.maskQ = self._mask(dQ, t)
        self.iP = np.flatnonzero(self.maskP.ravel())
        self.iQ = np.flatnonzero(self.maskQ.ravel())
        self.nP = self.iP.size
        self.nQ = self.iQ.size
        self.n = self.nP + self.nQ

    @staticmethod
    def _mask(d, t):
        I, J = np.meshgrid(np.arange(d + 1), np.arange(d + 1), indexing='ij')
        m = (I + J <= d)
        if t > 1:
            m &= ((I - J) % t == 0)
        return m

    def n_residual_cells(self):
        d = self.dP + self.dQ - 2
        I, J = np.meshgrid(np.arange(d + 1), np.arange(d + 1), indexing='ij')
        m = (I + J <= d)
        if self.t > 1:
            m &= ((I - J) % self.t == 0)
        return int(m.sum())

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
        """E_T at a point, with lambda_T ignored (for reporting)."""
        sup = self.sup
        P, Q = sup.unpack(c)
        tP = top_form(P, sup.dP)
        tQ = top_form(Q, sup.dQ)
        ET, _, _, ETp, ETn = self.tear(tP, tQ, tau=self.tau)
        return ET, ETp, ETn
