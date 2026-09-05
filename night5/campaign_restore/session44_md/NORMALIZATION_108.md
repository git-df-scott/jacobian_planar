# The (0,0) normalization — why the open case is now decidable

Full-depth rank showed both (72,108) subcases have dim = 1. Diagnosis
(via the walk_t control failure) located that one free dimension exactly:
the driver's (0,0) constant coefficient, c(1) in the Singular system.

This is a genuine invariance, not slack: for any constant c,

    [P + c, Q] = d(P+c)/dx * dQ/dy - d(P+c)/dy * dQ/dx = [P, Q],

since the derivatives of a constant vanish. So the (0,0) coefficient of P
is free and can be normalized to 0 with no loss: a solution with that
coefficient equal to a maps to one with it equal to 0 by replacing P with
P - a.

Setting c(1) = 0 removes the one free dimension. Verified numerically:
after fixing it, dim = 0 for case 2 (quadrilaterals, 25 params). A
0-dimensional ideal has a finite solution count (vdim), which Groebner
bases compute directly -- this is why the un-normalized (positive-
dimensional) systems timed out and the normalized ones should not.

run_108_norm.py runs both subcases at two primes with c(1)=0 injected.
Verdict reading:
  EMPTY at both primes  -> no counterexample at (72,108) mod those primes;
     combined with the char-0 facstd, evidence toward max-degree >= 125.
  a live 0-dim component -> finite explicit candidate points; each is
     replayed through the exact bracket check and then a characteristic-0
     lift before any claim. A modular survivor is never itself a claim.
