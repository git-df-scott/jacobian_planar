# The bifurcation program — attack the GGV ladder without Groebner

Novel-method thread started 2026-08-20 22:05Z at user request ("think of a
way no one has thought of").  Core: (1.3) is linear in A', hence a
first-order rational ODE; import center-focus / Abel-moment technology
(Briskin-Francoise-Yomdin, Pakovich composition theorems) and do LOCAL
bifurcation analysis (Lyapunov-Schmidt, mu0-direction) at the mu0=0
degenerate families instead of global Groebner per cell.  Scales to
d=27,48,75 where no Groebner will ever reach.  Either outcome is a prize:
unobstructed direction -> mu0!=0 power-series branch -> GGV Sec 2 -> CE;
uniformly obstructed pattern -> the induction step toward proving the GGV
conjecture (closing B=16 forever).

## Result 1 — d=3 degenerate locus in closed form (NEW, exact, char 0)

minAssGTZ over Q of the reduced d=3 system with mu0=0 (11 eqs, 8 vars,
instant).  EXACTLY two components:

- dim 0 (non-resonant root a6=1/12): the isolated point
  mu3=mu2=b2=0, a5=a4=a3=a2=0, a6=1/12.
- dim 1 (resonant root a6=-1/4): THE FAMILY
  mu2=0, b2=0, a5=a4=a2=0, a3=-mu3/2, mu3 free, i.e.
      q1 = y^3 + mu3,     A = -(1/4)(y^3 + mu3)^2 = -q1^2/4.
  Everything factors through w = y^3: pure composition structure, and
  mu1 = -mu3(a2+2b2)/3 = 0 on it, so ALL standalone-y terms (mu2 y,
  mu1 y^2, mu0 y^3) vanish along the family.

Consistency: the family sits at the RESONANT root (-1/4), the isolated
point at the non-resonant one (1/12) — matching the resonance law's
prediction of where degeneration lives.

## Result 2 — the naive composition lift to d=12 is REFUTED

Ansatz A = -q1^2/4 in (1.3) with mu0=mu1=mu2=0 forces
    y * q1' = 3 (q1 - mu3),
whose only polynomial solutions are q1 = mu3 + c y^3.  So the d=3 family
does NOT lift to d=12 by composition with A = -q1^2/4 kept exact.  If a
d=12 degenerate family exists (the d12-unsaturated OOM anomaly suggests
it), it deviates from -q1^2/4 at some order.  The d=3k^2 resonance pattern
must operate through the descent-level mechanism (level 36 at d=12), not
through naive inner composition.

## Result 3 — where a d=12 family MUST sit (probe running)

row0 is mu-free, so even on mu0=0 the top coefficient obeys
a24 in {-1/12, 1/20}; a degenerate family (positive-dimensional, resonant
by the law) must have a24 = -1/12.  Probe launched: dim of the
d=12 slice {mu0=0, a24=-1/12} mod 65521 (46 eqs, 34 vars, dp), Singular
std, hard-capped at 2.5GB / 900s so it cannot threaten the twin.
- dim >= 1 -> the family EXISTS: extract it, then Lyapunov-Schmidt in the
  mu0-direction at a smooth family point (the CE gate).
- dim = 0 or empty -> the anomaly is NOT a family at the resonant root;
  d12-unsat solo re-run stays queued, and the L-S base moves to d=27's
  slice (which this method can reach cheaply, unlike Groebner).

## Controls for the program
- d=3 L-S warm-up MUST return OBSTRUCTED (GGV proved d<=4 empty; an
  unobstructed verdict there means the code is wrong).
- d=12 conclusions must agree with the twin + 1/20-N verdicts
  (cross-method replication).

## Alternates logged (ranked below, not pursued tonight)
- Weyl-algebra route: JC2 => DC1, so a non-surjective endomorphism of A_1
  ([X,Y]=1 pair generating a proper subalgebra) refutes JC2; smaller
  search space, no polygon-style steering known.
- Lagrangian-graph route: enumerate the graph as an abstract Lagrangian
  surface in C^4 with pi_1 iso, pi_2 quasi-finite non-injective.
- mod-p^k lifting of degenerate families: same L-S obstruction in p-adic
  form (Hensel), usable as a fast pre-filter at higher resonant levels.

## Result 4 — the obstruction is EXACT and rank-one at d=3 (new, 01:40Z)

Substituting the d=3 degenerate family (q1 = y^3 + mu3, A = -q1^2/4, with
mu1 = mu2 = 0, a3 = -mu3/2, a6 = -1/4, rest zero) into the FULL GGV system
with mu0 left symbolic: every equation vanishes identically EXCEPT one row,
which equals exactly

        R  =  6*mu0

-- a nonzero constant multiple of mu0, with NO dependence on mu3 or any
family parameter.  So the family solves the system iff mu0 = 0, and the
obstruction never degenerates anywhere along the family.  That is precisely
why GGV's d=3 cell is empty, and it is the exact mechanism behind the
numerical walk's behaviour (below).

## Result 5 — the numerical mu0-walk works, both controls pass

wave6/w6_mu0walk.py implements homotopy continuation: find a mu0=0 point,
then track it while mu0 is increased.  Newton correction per step; fixed
memory; no Groebner basis anywhere.
  W0 (tracker, synthetic path that must be tracked): PASS.  It also caught a
     real bug first -- scipy LM needs #residuals >= #unknowns, so the
     original underdetermined control failed; fixed by squaring the system.
  W1 (mathematical negative control, d=3): 12 family points located at
     residual ~1e-35, and EVERY walk breaks at the FIRST step with end
     residual exactly 2.25e-8 = (6*s)^2 for step s = 2.5e-5 -- i.e. the
     numerics reproduce R = 6*mu0 to full precision.  d=3 is proven empty,
     so this is the required failure.

## THE BIFURCATION CRITERION (what the hunt is now actually testing)

For cell d let F_d be the mu0 = 0 degenerate family and let R_d(params, mu0)
be the residual left by substituting F_d into the full system.  A
counterexample bifurcates off F_d iff R_d can be driven to zero with
mu0 != 0 -- i.e. iff the mu0-direction lies in the image of the
linearisation at some family point (Lyapunov-Schmidt).
  * d=3: R_3 = 6*mu0, a nonzero constant  ->  NO bifurcation, cell empty.
  * general d: the -6*mu0*y^3 term of (1.3) lands in ONE coefficient row,
    but at larger d that row also carries many family-dependent terms which
    could cancel it.  Where such a cancellation is possible, a counterexample
    exists -- and that is a LOCAL, linear-algebra question, not a Groebner
    one, so it is computable at d = 12, 27, 48, ... where elimination is
    hopeless.
Hunt consequence: the target is no longer "solve cell d" but "find a family
point where the mu0 obstruction degenerates".

## Result 6 — the rank pattern is EXACT and unbroken (d = 3..9 so far)

At the quasi-homogeneous point of cell d the exact rank criterion gives,
with no exception and for BOTH roots of the row-0 quadratic:

        #equations = 4d + 6      #unknowns  = 3d - 1
        rank J     = 2d + 1      rank[J|G]  = 2d + 2   ->  ALWAYS obstructed

so no counterexample bifurcates off the quasi-homogeneous stratum at any d
tested (sweep continuing to d = 30, including the resonant cell d = 27).
The kernel has dimension (3d-1) - (2d+1) = d - 2: the degenerate locus grows
with d (dim 1 at d=3, dim 10 at d=12), which is why bigger cells feel
"roomier" -- but see the count below.

## Result 7 — the dimension count, and where a counterexample can still live

For a fixed vector G to enter the column span of J as the point moves, the
generic codimension of that condition is (#equations - rank) = 2d + 5, while
the degenerate locus offers only d - 2 directions to move in.  Since
d - 2 < 2d + 5 for every d >= 0, a bifurcation off the mu0 = 0 locus is
NON-GENERIC at every d -- it can only happen through an exact coincidence,
which is precisely what the resonance law hunts for but never guarantees.

Two consequences, both acted on:

 (a) The GGV system is heavily OVERDETERMINED, with excess
     (4d + 6) - (3d - 1) = d + 7 growing linearly in d.  The usual intuition
     "higher d gives more room" is therefore BACKWARDS for this system: the
     larger the cell, the more overdetermined it is, and the less likely a
     solution.  The best remaining odds are at the SMALLEST undecided cells.

 (b) Smallest undecided cells (the ladder's true frontier) are therefore the
     priority target, not d = 20+:
        d = 8  chart N   -- exported but NEVER RUN (MISS-2)   <== smallest
        d = 9, 10, 11 chart N -- never run
        d = 12 chart N   -- undecided (twin OOM-killed twice)
     and a counterexample not connected to the degenerate locus (an isolated
     solution) remains possible at any of them -- which is exactly what the
     global multi-start numerical hunt searches for, and why that lane is
     resumed and broadened rather than retired.

## Result 8 — the factored form, and why the ladder is rigid (derived 02:00Z)

Write D := A - q1^2/4 (the "defect") and C := (mu3/4)q1 - (mu2/6)y.  Then
(1.3) factors:

        6 D (D + 2C)  =  y * (4 A A' - mu2 q1^2 + 3 mu1 y q1 - 6 mu0 y^2)

At y = 0 the second factor vanishes identically under GGV's normalisations
(D(0) = -mu3^2/2, C(0) = mu3^2/4), so D + 2C = y E and the whole system
reduces one degree to

        6 D E  =  4 A A' - mu2 q1^2 + 3 mu1 y q1 - 6 mu0 y^2 .

CHECKS (both exact, both pass):
 * leading coefficients: 6(a_2d - 1/4)^2 = 8d a_2d^2  <=>  (8d-6)a^2 + 3a - 3/8 = 0
   -- the row-0 quadratic and hence the entire resonance law fall straight
   out of this balance, confirming the framework end to end.
 * at the d=3 family (D = -q1^2/2, E = -q1 y^2/2) both sides give
   (3/2) q1^3 y^2 identically, leaving exactly  0 = -6 mu0 y^2  -- the
   obstruction R = 6*mu0 re-derived in one line.
 * the branch D == 0 (A = q1^2/4) is impossible for d >= 1 by degree count
   (LHS degree 4d-1 vs RHS degree <= 2d), so it needs no computation.

RIGIDITY.  A counterexample requires the polynomial
        P := 6DE - 4AA' + mu2 q1^2 - 3 mu1 y q1
to collapse to the single monomial -6*mu0*y^2 with mu0 != 0: 4d-1 vanishing
conditions on 3d-1 unknowns, an excess of ~d that GROWS with d.  This is the
same verdict the rank sweep and the numerical floors give, now from pure
structure: the B=16 ladder is rigid, and rigid in a way that gets worse, not
better, as d increases.

## STRATEGIC SYNTHESIS — where a counterexample must be, if the ladder closes

GGV prove: B = 16 **or B > 20**.  Every independent line of evidence tonight
(exact rank pattern d=3..13, the excess count, the numerical empty-floors at
d=8 and d=12, this rigidity argument) points to B = 16 being EMPTY.  If that
is right then B > 20, and a counterexample's degrees are multiples of some
B >= 21 -- necessarily in the ABOVE-125 territory, where GGHV's elimination
does not reach and where no reduction machinery exists at all.

Consequence for the campaign: the above-125 frontier is not a side-quest, it
is the ONLY remaining home for a counterexample, and the tail-closure
predictor (last-2-segments + shape index -> system hash, zero violations on
every system ever generated here) is the tool that makes that frontier
finite.  The (72,108) resisters now running on the worker are the nearest
live instance of it, and GGHV Cor 5.7 -- the only thing killing the (9,27)
branch anywhere in the literature -- has still never been independently
checked by anyone.
