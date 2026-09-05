# The Le-Weber canonical-divisor sieve (Kodai Math. J. 17 (1994) 374-381)

Source: Le Dung Trang & Claude Weber, "A geometrical approach to the
Jacobian conjecture for n = 2", Kodai Math. J. 17 (1994) 374-381.
New to this campaign: our existing topology work (sieve_d6.py) used knot
monodromy and cover homology; this is a different invariant entirely.

## What they prove

Setting: f with no critical points, phi = F/T^d o pi the minimal
compactification, D_infinity the divisor at infinity, a component
"dicritical" when phi is non-constant on it.

MAIN THEOREM. If C(f) = C(g) = empty and I(f) != empty, then (f,g) is NOT
a Jacobian pair when either
  1. some strongly non-equisingular component of phi is not dicritical for
     psi, or
  2. some strongly non-equisingular dicritical D0 has phi|D0 or psi|D0 of
     degree one.
So a counterexample requires a COMMON dicritical component with both
restrictions of degree >= 2.

PROPOSITION (the computational engine). For a Jacobian pair, the divisor of
dphi ^ dpsi is a canonical divisor of Z confined to infinity, and "the
multiplicities ... can be computed from the sequence of blowing-ups. They
do not depend on phi and psi."

COROLLARY (p. 379). f is not a Jacobian polynomial if some dicritical
component D0 is strongly non-equisingular and its multiplicity in that
canonical divisor is strictly negative -- then psi has a pole along D0, so
D0 cannot be a common dicritical component.

## Why this is useful to us

It converts a hard analytic question into ARITHMETIC ON A RESOLUTION TREE,
and the campaign already holds the resolution data: the 34 published corner
chains (trackD_chain_map) are exactly the blow-up/Puiseux data at infinity
for the candidate shapes.

## The calculus (leweber.py, controls PASS)

  K_{P^2} = -3L, so the line at infinity starts at -3.
  free blow-up (point on one component of multiplicity m)      -> m + 1
  satellite blow-up (intersection of m1, m2)                   -> m1+m2+1

Controls: C1 line = -3; C2 free chain gives -2,-1,0,+1,+2; C3
satellite(L,E1) = -4, i.e. satellites make things worse, never better.

## The immediate consequence

A dicritical component reached by L free blow-ups off the line at infinity
has multiplicity -3 + L. Therefore:

  free-depth 1 or 2  ->  multiplicity < 0  ->  KILLED outright
  free-depth >= 3    ->  multiplicity >= 0 ->  survives this criterion

and satellite blow-ups only push multiplicities down. So ANY hypothetical
counterexample must have its common dicritical component at free-depth at
least three from the line at infinity. That is a cheap, purely
combinatorial necessary condition that can be checked per chain.

## Next step (recorded, not yet run)

Feed each of the 34 published chains' corner data through the calculus,
compute the multiplicity of each dicritical component, and discard every
chain whose dicritical components all come out negative. This is a sieve
over the SAME catalogue the algebraic lane is grinding on, but at
combinatorial cost rather than Groebner cost -- and it is independent
evidence, so agreement between the two lanes is a real cross-check.

Caveat stated up front: mapping a GGHV corner chain to its free/satellite
blow-up sequence is a translation step that must itself be controlled
(against a worked example whose resolution is known) before any chain is
declared dead on this basis alone.
