# Astra 7 — both first live global-potential systems closed

Date: 2026-09-05. Branch: `astra/jc2-missed-routes-2026-09-05`.
Continues directly from Astra 6, commit `080661cc2fa7`.

**Verdict: BOTH LIVE SYSTEMS CLOSED.** There is no collision Keller pair
with coordinate v-degrees (4,10) or (6,8), in either order, and with
arbitrary polynomial degrees in c. The full collision subalgebra remains
open. No counterexample or arbitrary-degree subalgebra obstruction is claimed.

The proofs use the saved complete polynomial-part reductions and a single
forced simple zero of h at c=0. They do not reopen the degree<=13 proof,
extend a conductor lift, perform a generic coefficient sweep, or infer
impossibility from a numerical search.

## (4,10): cubic elimination followed by a pole contradiction

The three residual rows reduce exactly to

    y^2+64Z^3+A Z=B,
    kappa=u*(10y Z'+15Z y')/16,
    y=u^2/h,

with A,B constant, h having a simple zero, and u regular. The source
polynomiality conditions allow y,Z poles of order at most one. A pole
of Z gives a unique cubic pole of order three, so Z must be regular.
Then y is regular, u vanishes, and the displayed Jacobian vanishes at
c=0. The separately handled u=0 case also has zero Jacobian. This covers
all parameter degeneracies and both leading roots.

Full proof: [OBSTRUCTION_410](astra7/OBSTRUCTION_410.md).
Exact certificate: [certificate_410.json](astra7/certificate_410.json).

## (6,8): four first integrals force the Jacobian to vanish

After a rational coordinate change and parameter shifts, the five rows
become four algebraic first-integral conditions and one Jacobian identity.
Two integrals vanish by Galois anti-invariance; the other two are constants.
This Galois symmetry concerns sqrt(h), not the collision involution r->-r.
In particular even collision trace of the approximate root is **not** assumed.

The resulting pole constraints first remove the deepest poles. The next
two leading equations have exact resultant

    -73728 A0^3 B0^9,

with A0 nonzero. They force B0=0 and the next coefficient to vanish.
The remaining pole constraints then leave the exact Jacobian in the form

    kappa=(4/9){B(abu)'+U(bu)'-B t w'+U t t'},

where B,U vanish at c=0 and abu,bu,t,w are regular there. Again kappa
must vanish, a contradiction.

No unknown function is divided out in this proof. It covers the non-even
root-trace component in full, both v(cv-2/3) and v(cv-4/3), auxiliary
roots with poles elsewhere, and identically-zero parameter cases.

Full proof: [OBSTRUCTION_68](astra7/OBSTRUCTION_68.md).
Exact identities, resultant and polynomial Bezout witness:
[certificate_68.json](astra7/certificate_68.json).

## Exact verification and scope

Run from the repository root:

```sh
python astra7/verify_410_obstruction.py
python astra7/verify_68_obstruction.py
python astra7/verify_inputs_and_controls.py
```

The checks independently expand the finite polynomial-part formulas,
verify all residual-row identities before imposing constraints, verify
the elimination and its Bezout witness, check the strict valuation
comparisons, and verify both source-coordinate conversions. Ordinary
polynomial Keller maps remain positive controls for the exact global
gate; the nonterminating family remains a global negative control.

Combining these two new arbitrary-c-degree proofs with Astra 6's existing
obstruction gives **no admissible potential with deg_v H<=14**. The next
unexcluded degree range is **deg_v H=15**, with coordinate v-degrees
**(6,9)** up to exchange and the already justified target reductions.
That next system has not been attacked or declared empty in this strike.

These are written algebraic proofs supported by exact symbolic
certificates, not machine-formalized proofs or an external review.
