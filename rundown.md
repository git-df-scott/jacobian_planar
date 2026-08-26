# JC2 Counterexample Campaign Rundown

This document preserves the campaign history, its main findings, and the verification rules that must govern future work.

## Sol 1 — Battlefield and Newton–Laurent campaign

Sol 1 built the main infrastructure: Newton polygons, Laurent chains, valuation recurrences, pentagon and quadrilateral configurations, finite-field algebra, reduced systems such as `{P,Q}=x^2`, reverse-lift machinery, modular searches, msolve/Singular calculations, and saturation tests.

Its most important legacy is the binding verification gate:

> A solution of a reduced equation is not a counterexample.

Any claimed CE must reverse-lift to actual polynomial coordinates, retain the required Newton vertices, have genuinely constant nonzero original Jacobian, satisfy every saturation and nondegeneracy condition, and exhibit an explicit collision. Numerical and finite-field points remain candidates until they lift and replay exactly.

Many apparent CEs died when truncated exporters or reduced recurrences omitted kernel-bearing rungs. Never trust a truncated exporter or recurrence without replaying the full equations.

The pentagon became a major target. Its y-adic recursion was built, the large export was independently cross-validated, and important pentagon seed systems received exact finite-field emptiness certificates. Those certificates do not eliminate every pentagon branch: some exceptional or resource-heavy branches remain unresolved.

**Result:** excellent machinery, many exclusions, no CE, and a strict verification standard.

## Sol 2 — Search the missed territory

Sol 2 was tasked with leaving the currently fashionable lane and auditing unexplored territory: new Newton configurations, alternative pentagon/quadrilateral branches, valuation structures, bottom-edge systems, exceptional components, and generic assumptions that might have silently discarded solutions.

The key methodological correction was distinguishing rational reconstruction failure from nonexistence over `C`. A modular solution may use algebraic coefficients and need not reconstruct rationally. The stronger target is a smooth finite-field point of the complete saturated system, with a nonzero Jacobian minor, so that Hensel lifting proves a characteristic-zero solution over `Qbar subset C`.

Sol 2 also pushed the campaign toward exceptional strata: zero divisors, rank-drop loci, saturation boundaries, and extension-field points.

**Result:** no CE, but several major blind spots were identified and the lifting philosophy was strengthened.

## Sol 3 — Five-target assault, F17, and degree 144

Sol 3 identified missed angles and attacked them directly, including F17 and the degree-144 reduced component.

### F17

F17 initially looked like a genuine algebraic solution. An exporter audit found that its tail had been truncated. Restoring the missing equations destroyed the apparent solution, and F17 was subsequently closed exactly over characteristic zero.

**F17 is dead. Do not reopen it without a genuinely new mathematical reason.**

### Degree 144

The degree-144 reduced hit was genuine as a reduced solution: residual approximately `10^-14`, with the required reduced vertices nonzero. It was not another fake numerical solve. However, reverse-lifting it to actual polynomial Keller coordinates failed badly.

This led to the simultaneous-shear program: free the shear parameters and test whether the genuine degree-144 reduced component intersects the polynomiality locus elsewhere. That problem continued into Sol 4 and Sol 5.

Sol 3 also contributed to the pentagon descent and the rebuilt level-16/15 branch analysis.

**Result:** F17 closed; degree-144 reduced component real but not a CE; its polynomial reverse-lift intersection remained open.

## Sol 4 — Audit, repair, and exact descent

Sol 4 inherited many seductive numerical signals and focused on preventing false positives. It audited Sol 3's state, preserved closed lanes, continued the degree-144 reverse-lift problem, descended the pentagon, studied exceptional branches, and investigated higher-dimensional mechanisms.

In pentagon branch 2, level 15 was descended exactly. Important conditions were

\[
F_2=2a_0a_2+a_1^2-4c_0b_2,
\qquad
F_3=a_0a_3+a_1a_2-2c_0b_3.
\]

On the generic chart `a_0 F_3 != 0`, level 15 survived after imposing `F_2=0`; the remaining constants could be solved. The strata `a_0=0` and `F_3=0` therefore required separate decomposition.

**Status:** no verdict—not a CE and not an emptiness proof.

Higher-dimensional Keller constructions were explored as a possible source of planar CEs by restricting a known noninjective 3D map to an invariant `A^2` surface. This produced useful geometry, including source surfaces containing colliding fibres, but the mechanism appeared dimension-specific. Low-degree target projections and graph constructions were ruled out in the tested ranges.

The `x=1` / non-separating-subalgebra direction also received exact low-degree exclusions; degree 3 was the first open boundary in that formulation.

The literature audit found no safe resolution of JC2. Higher-dimensional announcements and disputed proof claims do not resolve the planar case.

## Sol 5 — Degree-144 autopsy and the collision-first campaign

Sol 5 returned to degree 144 and asked whether the genuine reduced point intersects the simultaneous-shear polynomial-lift locus. The reduced point reproduced with residual near `10^-14`, but its reverse-lift defect was enormous. Continuation reduced the defect only by leaving the exact support variety. It was not a CE.

The next formulation parameterized the exact kernels of the polynomiality matrices instead of penalizing Laurent poles numerically. This reduced the problem substantially. A gauge-rank bug was found: three supposed driver gauges were not independent. The exact edge identity gives gauge rank 2, not 3, so the old 17-variable search was withdrawn.

The corrected formulation has 18 complex variables. Complex searches returned toward the already-empty zero-shear fibre rather than revealing a CE.

The new route is collision-first Hamiltonian incidence: normalize a hypothetical collision by affine source and target changes to

\[
a=(0,0),\qquad b=(1,0),\qquad P(a)=P(b)=Q(a)=Q(b)=0.
\]

For fixed `P`, solve the linear equation

\[
P_xQ_y-P_yQ_x=1
\]

with the two additional collision rows for `Q`. Every reported CE must still pass the full binding gate: explicit original polynomials, coefficient-by-coefficient Jacobian identity, and two distinct source points with the same image.

**Current status:** no counterexample. The collision-first incidence search is the active Sol 5 route. Reduced hits, numerical points, and finite-field points are only candidates until they lift and replay exactly.

## Standing rules

1. Never call a reduced solution a CE.
2. Never trust a truncated exporter or recurrence.
3. Rational reconstruction failure is not complex nonexistence.
4. Test complete saturated systems, including exceptional strata and extension-field points.
5. Preserve closed lanes unless a genuinely new mathematical reason reopens them.
6. A final CE requires explicit original `P,Q`, exact `[P,Q]=1`, and an explicit collision.
