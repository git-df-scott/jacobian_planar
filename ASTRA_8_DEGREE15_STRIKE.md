# Astra 8 — degree-15 strike: a noncube obstruction and a live resonance

Date: 2026-09-05. Branch: `astra/jc2-missed-routes-2026-09-05`.
Continues directly from Astra 7, commit `c983d81d55d9`.

**Outcome: OPEN. The requested decisive outcome was not achieved.**
There is no counterexample, no arbitrary-degree collision-route closure,
and no proved reduction of the entire route to one irreducible component.
Degree 15 itself remains open. The verified progress below must not be
relabelled as any of those stronger conclusions.

## What is proved in this strike

Normalize a (6,9) pair by lc_v(P)=h^2 and lc_v(Q)=h^3.

1. **Every noncube h is excluded**, with unrestricted polynomial coefficient
   degrees in c. This ambient theorem does not even need collision membership.
   Four exact first integrals and Galois characters reduce the Jacobian to

       h=-32768*kappa^3*(C+3W^2/2)
           /(27*(2C+7W^2)^3*(W')^3), W in C(c).

   If C!=0, two distinct rational target values force a finite pole of h.
   If C=0, h and W become monomials. Polynomial reconstruction then requires
   two pole polynomials to have a common root, but their exact resultant is
   **567/32768**, with a separate Bezout identity for 1.

2. **An arbitrary-degree necessary leading-coefficient invariant:** if a
   component of v-degree m>1 has leading coefficient f(c)^m with f polynomial
   and nonconstant, then

       f=gamma*(c-c0)^N, N>=2.

   The Jacobian forces a rational primitive of 1/f. A rational-function pole
   count proves the statement. This is a necessary condition, not a complete
   Keller-map criterion or a collision-route obstruction.

3. Consequently **every surviving (6,9) collision pair has**, after constant
   target scalings, h=c^(3N), N>=2. Its exact normalization removes k_6,k_0
   by target shear and k_3 by a target translation. Six fractional-power
   constants remain: k_1,k_2,k_4,k_5,k_7,k_8.

4. Polynomiality and collision parity force both possible leading branches
   into the same singular cubic behavior:

       P_top=[A*v*(cv-rho)]^2, rho=2/3 or 4/3,
       ord_0(p5)=3N+1,
       leading(p5^2/(c^(6N)*p4))=4,
       ord_0(a)=2-4N, ord_0(b)=3-6N,
       leading(4a^3+27b^2)=0.

   The leading cubic has a double root. Its quadratic first-integral equations
   have a nonzero tangent direction; the earlier noncube vanishing argument
   does not eliminate that direction in the resonant field.

## The exact remaining equations

Set x=c^N(v+eta), with a,b,u,w,z,eta Laurent polynomials in c, and

    p=(x^3+a*x+b)^2+u*x^2+w*x+z,
    q=[p^(3/2)]_+ + sum_(j in {1,2,4,5,7,8}) k_j[p^(j/6)]_+,
    mu_i=-(1/i)[x^(-1)](q_x*p^(i/6)), i=1,...,5.

The residual Jacobian equations are equivalent to the five algebraic identities

    mu_1=C1, mu_2=C2, mu_3=C3, mu_4=C4,
    mu_5=C5+kappa*c^(1-N)/(6*(1-N)), N>=2, kappa!=0.

In addition, the reconstructed P,Q must be polynomials in c,v and their two
full collision-parity polynomials must vanish. These conditions are necessary
and sufficient for this normalized degree-15 system. The expanded mu_i and
the finite reconstruction formulas are in `astra8/resonant_69_system.json`.

I have not proved this system empty or produced a solution. I have not proved
its fibers irreducible. The new leading-coefficient invariant also supplies
no reduction of larger coordinate degrees to (6,9). Those missing steps
prevent the requested FULL COLLISION-ROUTE CLOSURE or SINGLE IRREDUCIBLE GAP
verdict. It would be incorrect to claim that a full-route theorem follows
from recurring low-degree pole calculations.

## Proofs and exact certificates

- [Noncube obstruction](astra8/OBSTRUCTION_69_NONCUBE.md), with all zero branches
  retained and rational auxiliary coefficients allowed.
- [Arbitrary-degree leading-coefficient invariant](astra8/LEADING_COEFFICIENT_INVARIANT.md).
- [Complete resonant system and local leading proof](astra8/RESONANT_69_SYSTEM.md).
- [Noncube algebra certificate](astra8/certificate_69_noncube.json), including
  the polynomial-part identities, all four first-integral rows, the eliminated
  rational Jacobian, resultant and Bezout identity.
- [Expanded resonant equations](astra8/resonant_69_system.json), including an
  unconstrained identity for the full Jacobian in terms of the five mu_i'.
- [Inputs and controls](astra8/inputs_and_controls.json), including removal of
  the redundant k_3, both parity polynomials, both leading alternatives, and
  ordinary polynomial Keller controls.

Replay with Python and SymPy:

```bash
python astra8/run_certificates.py
```

The saved global negative control remains rejected: c*(Q+v)^2=1 has no
rational solution by valuation at c. Ordinary polynomial Keller controls
still pass the ambient potential test and are correctly excluded from the
collision subalgebra. The leading-coefficient residue identity is also checked
on the ordinary pair P=v^6+c, Q=v, whose Jacobian is -1.

No new conductor-adic orders, coefficient-degree sweeps, numerical point
searches or unsupported modular inferences were used. The degree<=14 result
was used as saved, not reopened. The new proofs are written mathematical
arguments supported by exact symbolic identities, not externally reviewed
or proof-assistant formalized proofs.
