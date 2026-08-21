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
