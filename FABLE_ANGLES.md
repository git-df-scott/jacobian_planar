# Fable: 15 new angles on the pentagon — 2026-08-22

Companion to `FABLE_SWEEP_REPORT.md`. These are attack directions the campaign
has NOT tried (Gröbner-centric to date). Angles 1 and 2 are **verified with
passing controls in this session** (`check_angle1.py`, `check_angle5.py` at
repo root); the rest are ranked leads with concrete first steps. Notation as in
the mailbox: `p_j_i` = coeff of `x^i y^j` in P (x-deg 8), `q_j_k` in Q
(x-deg 12); ladder pieces `h_a(s)`, `g_b(s)`; gauges `h_{-1} = s`,
`g_{-1} = s^2`.

---

## VERIFIED RESULT 1 (angle 1). The descent's ladder IS a Jacobian pair on the torus — the problem renormalizes into itself

Let `H(s,w) = sum_a h_a(s) w^a`, `G(s,w) = sum_b g_b(s) w^b` (Laurent in `w`,
supports `a in [-1,8]`, `b in [-1,12]`). Then the ENTIRE ladder
`sum_{a+b=L} [b h_a' g_b - a h_a g_b'] = delta_{L,-2} s^2` is exactly

    H_s (w G_w) - (w H_w) G_s = s^2 w^{-2}

and with `u = s^3/3`, `v = -1/(2w^2)`:  **dH ∧ dG = du ∧ dv.**

Checked symbolically (random truncations, all L; gauge pieces alone give the
`s^2` RHS on the nose; the `(s, log w)` Jacobian equals the bracket).
`check_angle1.py` — three PASS lines.

Consequences, in order of ambition:

- The pentagon interior is a **Keller pair on a (3,2)-branched cover of the
  torus** — the same (2,3) exponents as the original `{P,Q} = x^2 =
  d(x^3/3) ∧ dy` reduction. The problem is SELF-SIMILAR: a (72,108)
  counterexample contains a smaller Laurent–Keller pair of bidegree ~(8,12)
  inside it.
- **Descent route to EMPTY:** apply the classical polygon-shrinking theory
  (Abhyankar "going down", Joseph/Makar-Limanov for Laurent pairs: Newton
  polygons of a torus Jacobian pair are similar and reducible by elementary
  moves) to (H,G). If every admissible (H,G)-polygon reduces to a case in the
  campaign's already-CLOSED small-cell territory, the pentagon dies by
  infinite descent — a *proof*, no Gröbner.
- **Construction route:** if the renormalization has a fixed point (the (H,G)
  pair itself pentagon-shaped), that fixed-point equation is a much smaller
  system than 59-in-19 and is where a CE would concentrate.
- Practical: all torus-pair literature (Laurent Jacobian conjecture is
  *settled*; commuting-pair polygon theory) now applies to the descent. Nobody
  has opened that toolbox on this campaign.

## VERIFIED RESULT 2 (angle 2). `q_21_12 != 0` is automatic, and rung 19 falls out of one Wronskian

The top x-column of `{P,Q} = x^2` is `x^19`, fed only by `(i,k) = (8,12)`:
`8 a_8 b_12' - 12 a_8' b_12 = 0`, i.e. `b_12^2 = c a_8^3` on the right
vertical edges. Since `b_12` is a polynomial, `a_8^3` must be a square, so the
edge quadratic of `a_8 = y^14(p_14_8 + p_15_8 y + p_16_8 y^2)` has
**disc = 0** — rung 19 re-derived from one line, independent of the lower-edge
sub-ladder (cross-validates OPUS43-014). Writing `a_8 = p_16_8 y^14 (y-r0)^2`:

    b_12 = c' y^21 (y - r0)^3,   q_24_12 = c',   q_21_12 = -c' r0^3,
    p_14_8 = p_16_8 r0^2.

So given the vertex conditions `p_16_8 != 0, q_24_12 != 0` **already imposed**:

    q_21_12 != 0  <=>  r0 != 0  <=>  p_14_8 != 0.

`p_14_8 != 0` is itself one of the six mutable vertices. **The "one vertex
that is not automatic" (OPUS43-029 soundness check 2) is automatic after
all** — no separate endgame check needed, and any chart that kills `p_14_8`
or `r0` (note `tau` vs `r0` are different objects: `tau = -p_15_7/(8 p_16_8)`)
is dead on arrival. `check_angle5.py` — all PASS, including the converse
(Gröbner over the edge coefficients forces disc when `q_24_12 != 0`).

---

## The other 13 angles, ranked

**3. Period-integral / moment-problem reformulation.** `{P,Q} = x^2` says
`X_P(Q) = x^2` — a linear PDE in Q. Polynomial solvability of `dP ∧ dQ =
x^2 dx ∧ dy` is a cohomological condition on P alone: `x^2 dx∧dy` must die in
P's Brieskorn module, i.e. the Abelian integrals `∮_{γ(c)} x^2 dx∧dy / dP`
vanish for every vanishing cycle of every fiber. This is the
tangential-center / polynomial-moment problem (Pakovich–Muzychuk toolset),
where vanishing forces **composition structure** on P. Either that structure
contradicts the six nonzero vertices (⇒ pentagon EMPTY, structurally), or it
*names the ansatz* for P. Eliminates Q from the hunt entirely: search is over
P's ~45 coefficients with a functional-analytic filter.

**4. Discriminant-curve + BKK/Riemann–Hurwitz bookkeeping (cheap, decisive
flavor).** The map Φ = (P,Q) is critical exactly on x = 0 (since Jac = x^2);
its discriminant curve is the parametrized `(P(0,y), Q(0,y))`, degrees (8,12).
Compute: (a) topological degree of Φ = mixed volume of the two pentagons
(BKK); (b) Euler characteristic of the generic fiber P = c from N(P) lattice
count (Khovanskii) with punctures from a toric resolution at infinity; (c)
Riemann–Hurwitz for Q restricted to that fiber — ramification only over the 8
double points on x = 0 plus infinity. These three must reconcile in one
integer identity. If they don't: **pentagon EMPTY, all charts, no solver.** If
they do: we learn the fibration's genus/punctures, which constrains
construction. A day of careful arithmetic, zero compute.

**5. Orevkov audit.** Orevkov's work on dicritical configurations, bad field
generators, and near-counterexamples is the deepest existing theory of exactly
this object (small-polygon JC candidates) and postdates/exceeds GGV in the
directions the campaign needs. Check (72,108)-pentagon against his constraint
lists. Either it violates one (dead) or it matches a configuration he leaves
open (we inherit his machinery + know we're on the true frontier). Pure
literature work — assign to whoever has library access; zero compute.

**6. Abhyankar–Moh semigroup constraints at infinity.** The pentagon fixes the
branches at infinity of the fibers P = c. The AM semigroup / characteristic-
pair inequalities on a (72,108) Keller-candidate's points at infinity are
severe Diophantine conditions never checked here. Complements angle 4: same
geometry, arithmetic side.

**7. Deformation lift from the degenerate families (CODEX-004's dropped
thread).** Families A/B/C are known NONEMPTY unsaturated points, and
CODEX-004 found the tangent space at the p_1_1 = 0 chart has directions that
turn on `p_8_0, p_14_8` — i.e. toward saturation. Nobody followed them. Do
obstruction calculus order-by-order in a deformation parameter ε: either the
lift extends (CE constructed from a known solution — this is the single most
*constructive* angle on the board) or it obstructs at a computable finite
order, uniformly across charts. Reuses existing family code; sympy-cheap.

**8. Grading of the 59-in-19 endgame + cone test.** The raw pentagon had torus
rank 2. Check whether a residual Z-grading survives on the 19 endgame
parameters (run `torus_scan.py` on the endgame system — two minutes, never
done). If a positive grading exists, the variety is a cone: test the origin
instantly, and decompose the 59 conditions by weight — pure-power gates then
have a *predicted* location (see angle 9).

**9. The pure-cube conjecture (structural form of `g8_6 = g8_7 = 0`).** Two
cube gates at one level is not an accident. Conjecture: at every
pure-condition level, the gate ideal contains `(resonant parameter)^3` for
each parameter pairing with ker D_k. If Sol proves this from the operator's
Jordan structure, we get closed-form necessary conditions at EVERY level
solver-free — a skeleton of the whole endgame, and it de-inherits the
`g8_6 = g8_7 = 0` assumption behind all six EMPTYs (S2 upgraded with a target
theorem).

**10. G-centric change of variables.** Both upper edges are powers of ONE
quartic: `A = c0 G^2`, `Qh = c1 G^3`, and (new, angle 2) both right edges are
powers of `(y - r0)`. The fundamental objects are G and r0, not P and Q.
Re-coordinate the interior corrections in a G-adapted basis; the bilinear
system should block-triangularize further. Mechanical, and it shrinks the
symbolic descent Sol and Opus are both running.

**11. Alpha-certified Newton on near-dead charts + PSLQ.** Where "47 of 51
conditions die," hunt the remaining few numerically at 200 digits, certify any
root by Smale alpha-theory (a certified root IS a NONEMPTY verdict — this
meets the campaign's proof standard, unlike the retracted P15 numerics), and
PSLQ/LLL the coordinates back to exact algebraic numbers. Target: the
surviving conditions on deleted-divisor charts of the GENERIC branch, as they
emerge from sweep-plan O1/O2.

**12. Dixon/sparse resultants with symbolic `a4`.** For the generic-branch
endgames (parameters kept symbolic), interpolation-based Dixon resultants
handle parametric elimination where Gröbner degenerates. This is the right
engine for the "51-in-16 with 47 sharing a factor" shapes.

**13. Char-p Cartier operator obstructions.** In char p, `{P,Q} = x^2`
interacts with the Cartier operator: necessary congruences on the endgame
parameters can be derived without solving, for many p at once. Any p-uniform
contradiction on a chart is a char-0 EMPTY for free; conversely the p-adic
pattern of near-solutions guides the height guesses in angle 11.

**14. Fiber-count identity on the cover.** From Verified Result 1, (H,G) is a
Keller pair on the (u,v)-chart with cusp branching. Run angle 4's bookkeeping
*upstairs* on (H,G) (smaller polygons, easier arithmetic) — the two counts
(upstairs/downstairs) must agree through the 3:1 and 2:1 branchings. Two
identities instead of one; twice the chance of an integer contradiction.

**15. Infinite descent wiring into closed territory.** Combine angles 1 + 5 +
6: if each pentagon solution induces a strictly smaller admissible torus pair
(elementary moves shrink the (H,G) polygon), and everything below is the
B=16/small-cell land the campaign has already CLOSED with certified EMPTYs,
then the closed ground becomes the base case of an induction and the pentagon
closes by descent. This is the only angle that converts the campaign's
enormous pile of EMPTYs from "losses" into load-bearing lemmas.

---

## Assignment deltas (on top of the sweep-plan lanes)

- **Opus 5:** angle 8 (2-minute torus scan of the endgame) immediately; then
  angle 7 (deformation lift — constructive) alongside O1/O2; angle 11/12 as
  the solver back-end for generic-branch charts. Use Verified Result 2 to
  delete the `q_21_12` check from every endgame and kill any chart with
  `p_14_8 = 0` or `r0 = 0` on sight.
- **Sol:** angle 9 (target theorem for S2), angle 4's arithmetic (it is pure
  derivation, Sol's lane), angle 3's composition-condition analysis, angle 5's
  literature audit. Verified Result 1 gives Sol a second independent
  formulation of the whole descent for the S1 recount: expand
  `H_s(wG_w) - (wH_w)G_s - s^2 w^{-2}` directly and count conditions per
  `w`-level — if that count is not 59, we've found the discrepancy from the
  53-vs-59 sum in one shot.
- **Fable:** stays on adjudication; the two results above cost ~zero budget
  (two sympy runs) and are committed with their controls.

Breakthrough honesty: Results 1 and 2 are real but small-to-medium — Result 1
is a reframing with a plausible path to a *proof-level* outcome (descent) and
a concentrated CE target (fixed point); Result 2 removes an endgame check and
adds a chart-killer. Nothing here is a counterexample. The 99% bar is not met;
the fastest route to it remains O1/O2 (deleted-divisor charts, generic branch)
now augmented by angles 8, 7, and 11.
