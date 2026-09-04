# Graded frontier

## Current characteristic-zero results

**Both polygons in GGHV Proposition 4.3 are excluded.** Astra 3 closes the
pentagon in part (1), so the original case called (8,28) in that proposition
is excluded as well. This is a scoped computer-assisted result, not a
resolution of JC2 or a closure of the separate above-125 (3,4) chain.

Read `ASTRA_3_PENTAGON_PROJECTIVE.md` for the complete support reconstruction,
right-edge normalization, five-parameter descent and weighted-projective
valuation proof. Run `python astra/verify_pentagon_projective.py` to verify
the homogeneous equations, affine unit certificate, five boundary power
certificates and exact good reduction. The written normalization,
completeness and valuation arguments are not proof-assistant formalized.

**Case (2) is excluded in characteristic zero.** See
`ASTRA_2_CASE2_EXACT_DESCENT.md` for the five-dessin completeness proof,
universal two-parameter level-four solution, and independently verified
26-generator lower certificate. Run `python astra/verify_case2_certificate.py`.

The five exact leading solutions use `C_1=C_2=1`; the older `C_1=C_8=1`
normalization has seven representatives per scaling orbit, hence 35 points.
The separate degree-1144 object's provenance remains unresolved and is not
used. The modular archive audit below describes historical evidence only.

## Correct instrument for case (2)

For the GGHV Proposition 4.3 case-(2) reduced polygon `p108_525122`, grade by

```
rho=2i-j,  T=xy^2,
P_rho=y^-rho f_rho(T),  Q_sigma=y^-sigma g_sigma(T).
```

Then

```
{P_rho,Q_sigma}
=y^(1-rho-sigma)(rho f_rho g_sigma' - sigma f_rho' g_sigma),
```

and the two-variable system becomes five triangular one-variable levels.  The
top equation is

```
2 f2 g3' - 3 f2' g3 = T^2,
```

an exactness condition on `y^2=f2(T)`.  This is the right representation.  The
depth-6 y-adic Groebner timeout is not evidence.

## Mandatory positive controls

`astra/graded_control.py` independently verifies the grading identity and five
explicit witnesses over Q.  Every witness satisfies `{P,Q}=x^2` exactly;
degrees range from (2,4) through (12,12).  This also protects against the
archived `general.py` bug that imposed one common top degree and falsely
excluded witness W3.

## Case-(2) archive adjudication

`astra/audit_graded_case2.py` pins graded head
`10469087a97ca4143ce8a278f3ce0211143ced19`, verifies SHA-256 hashes of the
input and certificate logs, and independently factors the leading orbit
eliminant at p=32003.

Exact modular facts:

| item | result |
|---|---|
| m | 8 |
| reduced degrees | `(24,36)`; original pair `(72,108)` |
| E1 slice | dimension 0, vector-space dimension 35 |
| residual-scaling orbit polynomial | quintic |
| factor degrees over F_32003 | `1+1+3` |
| lower stages | both linear factors and the cubic factor give `GB=[1]` |
| verdict | `EMPTY-mod-p` at p=32003 |

At p=1000003 the leading slice again has 35 geometric points, but the checked
standalone lower-stage log kills only one rational orbit.  The automated
pipeline log contains generated Singular syntax errors on later factors, so it
is not a full second-prime certificate.

Before the new exact descent, characteristic-zero status was `UNKNOWN`:

- a claimed degree-35 field calculation is not identified with canon's
  degree-1144 residual object;
- no exact-Q lower-level `[1]` certificate was found; and
- modular emptiness at one prime cannot be promoted.

## Highest-ranked untouched published case

The primary table in arXiv:1708.07936 Section 6 was checked directly.  The
first high-value entry is

```
A0=(8,28), A1=(7/4,3), (m,n)=(3,4), max degree 144,
```

corresponding to the `(108,144)` campaign target.

It did not pass the translation gate.  The paper's table does not print the
last lower corner A'_t that the above-125 compiler sets to `(1,0)`, and the
compiler's c' ladder predates the cmax correction.  Therefore the archived
c'=0 monomial certificate is an exact kill of that generated stratum under its
assumptions, not a closure of the published case.  ASTRA did not feed this
unverified translation to a solver.

This is a provenance `WALL`, not a computational timeout.  The next work is:

1. derive A'_t and the complete c' range from the primary definitions;
2. independently reconstruct both epsilon orientations and verify
   `eps_P+eps_Q=(r+1,1)`;
3. run the exact Poisson grading on the resulting supports;
4. solve the leading one-variable period system by Galois orbit; and
5. descend level by level, producing exact-Q certificates or an explicit
   surviving branch.

No above-125 published case is claimed closed here. The new exclusions cover
both parts of Proposition 4.3 of the degree-108 reduction, with the precise
scope stated in the Astra 2 and Astra 3 reports.

## Tooling wall

The second Astra run provisioned Singular 4.3.1 locally and generated an exact
lower certificate. Its independent FLINT verifier requires no Singular.
The third run used Singular for finite-field pentagon certificates and
PARI/GP 2.15.2 for an optional smaller field model, independently checked
with FLINT. Three direct exact pentagon eliminations timed out; their
generated inputs and logs are preserved and prove no emptiness. The successful
projective verifier requires Python and python-flint, not either solver.
GAP and msolve remain unprovisioned. Missing binaries are not evidence.
