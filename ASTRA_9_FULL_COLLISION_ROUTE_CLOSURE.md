# Astra 9 — full collision-route closure

Date: 2026-09-05. Branch: `astra/jc2-missed-routes-2026-09-05`.
Continues directly from Astra 8, commit `05a36d66cd0a`.

**Verdict: FULL COLLISION-ROUTE CLOSURE.**

For the entire algebra

    B=C[b,c]+Delta*C[v,c],
    b=-3cv^2+4v+2, Delta=(3cv-2)^2-9c,

the following arbitrary-degree theorem holds:

    P,Q in B and J_(v,c)(P,Q) constant
        ==> J_(v,c)(P,Q)=0.

Thus this construction cannot produce a polynomial Keller pair, and no
polynomial potential satisfies the saved exact global criterion. The full
(6,9) resonance, both collision branches and all higher degrees are excluded.
There is no remaining degree frontier in this collision subalgebra.

## The missing global obstruction

The key ingredient omitted by the earlier strikes was the slope-one
Newton-edge obstruction. It has an independent published statement as
Corollary 1.6 of
[Guccione, Guccione and Valqui, *The two-dimensional Jacobian conjecture and
the lower side of the Newton polygon*](https://arxiv.org/html/1605.09430v2#S1).
The full proof for the present setting is supplied in
[astra9/FULL_COLLISION_OBSTRUCTION.md](astra9/FULL_COLLISION_OBSTRUCTION.md).

The argument is short and does not depend on the earlier degree exclusions:

1. Use weight(v)=1, weight(c)=-1. Every F in B has even trace at
   c=r^2/9, v=3(r+2)/r^2. If its positive-weight top form were a single
   monomial, that monomial would have an uncancellable nonzero odd trace
   coefficient. Therefore its top form is v^d L(vc), d>0, with L not a
   monomial. L has a nonzero root lambda.

2. That root gives an exact algebraic branch of F=0 with
   v=s^(-e), c=s^e z(s), z(0)=lambda!=0. If F had a polynomial mate G
   with Jacobian kappa!=0, a polynomial H would satisfy

       dH=F dG-kappa*v dc.

   On the branch, the right side has residue -kappa*e*lambda, which is
   nonzero. The derivative of the Laurent series H(v(s),c(s)) has residue
   zero. This contradiction excludes every positive-weight component.

3. Both components of a putative pair in B must consequently have
   nonpositive weight. Write P=F(c,cv), Q=G(c,cv). Then

       J_(v,c)(P,Q)=c*(F_t G_c-F_c G_t)|_(t=cv),

   which vanishes on c=0 and cannot be a nonzero constant.

Repeated roots and arbitrary ramification e are included. No irreducibility,
simple-root assumption, bound on c-degree, minimal-pair normalization, or
assumption about polynomial approximate roots is needed.

For degree 15 specifically, the previously surviving forms
[A*v*(cv-rho)]^2 already have the forbidden edge, with lambda=rho=2/3 or
4/3. The six retained fractional-power constants and the entire integer
family N>=2 cannot change this contradiction. There is no need to keep
eliminating their five first-integral equations.

## Verification and scope

Run:

```bash
python astra9/verify_full_obstruction.py
```

All seven checks pass. They verify the exact collision trace, the
arbitrary-degree odd coefficient and weight separation, the universal
ramified residue identity, an exact repeated-root control, the final
Jacobian factor c, both degree-15 branches, and ordinary Keller controls.
The saved global potential positive controls and nonterminating negative
control also pass their expected tests. No new conductor-adic order or
degree sweep was performed.

- [Full proof](astra9/FULL_COLLISION_OBSTRUCTION.md).
- [Boundary-case and scope audit](astra9/PROOF_AUDIT.md).
- [Exact symbolic certificate](astra9/full_obstruction_certificate.json).
- [Verifier](astra9/verify_full_obstruction.py).

This is a written proof with exact supporting identities and an independently
published match for its central obstruction. It has not been proof-assistant
formalized or externally peer reviewed as a campaign result.

The prior OPEN verdicts for this collision algebra are superseded. Their
degree-specific calculations remain archived, but this lane should not be
reopened merely by raising degree or deepening a conductor lift.

The theorem concerns this specified collision subalgebra. It does not
establish the general planar Jacobian conjecture, or claim a counterexample
outside this construction.
