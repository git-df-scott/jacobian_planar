# Handoff — plane Jacobian Conjecture campaign, session 44

Branch `claude/past-code-session-8mdjqn`.  Everything below is committed and
pushed.  Read this file first; it is written to be self-contained.

---

## 0. One-paragraph state

**No counterexample was found, and none is close.**  What this session
produced instead is the closure — *modulo a prime* — of the last open case
below degree 125 in the Guccione–Guccione–Horruitiner–Valqui classification.
If that closure survives to characteristic zero, the standing degree bound
for a plane Jacobian counterexample becomes a clean `max(deg P, deg Q) >= 125`
with no exceptional case.  That is the concrete deliverable on the table.
The counterexample hunt itself moved *backwards* this session: every result
eliminated territory.

---

## 1. The problem

JC2: if `P, Q` in `C[x,y]` and the Jacobian `[P,Q] = P_x Q_y - P_y Q_x` is a
nonzero constant, then `(x,y) -> (P,Q)` is a polynomial automorphism.  Open
since 1939.  A counterexample ("CE") is a Keller pair that is not invertible.

**Guccione–Guccione–Horruitiner–Valqui, arXiv:2204.14178, Thm 2.1.**  Any
counterexample has

        max(deg P, deg Q) >= 125     OR     degrees exactly (72,108).

The `(72,108)` clause is an escape hatch they could not close; their Prop 4.3
narrows it to **two subcases**, given in reduced Laurent coordinates with
`[P,Q] = x^2`:

    subcase 1 (pentagons)
        N(P) = conv{(0,0),(1,0),(8,14),(8,16),(0,8)}
        N(Q) = conv{(0,0),(2,1),(12,21),(12,24),(0,12)}

    subcase 2 (quadrilaterals)   -- the same without the (0,8)/(0,12) corners
        N(P) = conv{(0,0),(1,0),(8,14),(8,16)}
        N(Q) = conv{(0,0),(2,1),(12,21),(12,24)}

Note subcase 2's polygons are *contained* in subcase 1's, so the two are
linked: killing the vertex (8,16) inside the pentagon kills it inside the
quadrilateral too.

**Critical caveat, do not lose it.**  Prop 4.3 is a ONE-WAY implication.  A
pair surviving these constraints would *not* be a counterexample.  A CE claim
requires lifting to honest polynomials in ORIGINAL coordinates, with no
denominators, and the Jacobian verified to be a nonzero constant exactly.
This is the Vitushkin trap and it has eaten past sessions.

---

## 2. The key structural discovery: the essential face

Grade monomials by `w(i,j) = j - 2i`.  The monomial bracket rule

        [x^a y^b, x^c y^d] = (ad - bc) x^(a+c-1) y^(b+d-1)

gives `w(result) = w1 + w2 + 1`.  On subcase 2, `w` takes values `{0,-1,-2}`
on `N(P)` and `{0,-1,-2,-3}` on `N(Q)`, so bracket weights run `-4 .. 0`.
The target `x^2` has `w = -4`, which is the DEEPEST level.

That is the "essential face": a face where the bracket's top component
**equals** the target rather than vanishing.  It is shared outright by BOTH
subcases (verified independently by two codebases on the two polygon sets).

Substituting `u = x y^2`, `z = 1/y` (Jacobian of the substitution is `-1`,
so `[P,Q]_{x,y} = -[P,Q]_{u,z}`, and `x^2 = u^2 z^4`) gives

        P = f(u) + p(u) z + q(u) z^2
        Q = g(u) + r(u) z + s(u) z^2 + t(u) z^3

with supports (from exact lattice-point enumeration):

        f: u^0..u^8   p: u^1..u^8   q: u^1..u^8
        g: u^0..u^12  r: u^1..u^12  s: u^2..u^12  t: u^2..u^12
        (72 coefficients; the two constant terms never appear in the bracket)

and the five identities, collected by power of `z`:

        z^0:  f'r - p g'                          = 0
        z^1:  2f's + p'r - p r' - 2q g'           = 0
        z^2:  3f't + 2p's + q'r - p s' - 2q r'    = 0
        z^3:  3p't + 2q's - p t' - 2q s'          = 0
        z^4:  3q't - 2q t'                        = -u^2      <-- ESSENTIAL FACE

General rule, if you need to re-derive: writing `P = sum a_i z^i`,
`Q = sum b_j z^j`, the `z^k` coefficient of `[P,Q]_{u,z}` is
`sum_{i+j-1=k} (j a_i' b_j - i a_i b_j')`.

### Facts about the face equation `2 q t' - 3 q' t = u^2`

* **Degrees are forced.**  With `deg q = D`, `deg t = E`, `val q = d`,
  `val t = e`, the extreme coefficients are `(3D-2E) q_D t_E` and
  `(3d-2e) q_d t_e`.  Subcase 2 requires `q_1, q_8, t_2, t_12` nonzero (they
  are the polygon vertices), so `d + e = 3` puts the target at the bottom and
  `3D = 2E` forces **`(deg q, deg t) = (8,12)` exactly**.
* **Exactly 35 solutions** with the two gauges `q_1 = q_8 = 1`
  (17 equations, 17 unknowns, dim 0, vdim 35).  Confirmed by SIX independent
  instruments: Singular char 0 and mod 32003, msolve at multiple primes,
  sympy, a Frobenius / Murnaghan–Nakayama count of genus-0 covers with
  ramification `[3^7], [2^10,1], [17,1^4]`, and my own from-scratch rebuild.
* **35 = 5 covers x mu_7.**  Once `q_1 = q_8 = 1` the residual gauge group is
  `q_k -> L^(k-8) q_k` with `L^7 = 1`.  The mu_7 action was VERIFIED to be a
  genuine symmetry, induced by `(x,y) -> (tx,y)` with `P -> t^-1 P`,
  `Q -> t^-2 Q`, checked at `t = 2,3,5,7,11,-1`.  This matters: mod a prime
  with `7 | p-1` false, only one point per orbit is `F_p`-rational, so 5
  tested points cover 35 only because of this symmetry.
* Over **Q**, msolve gives an exact irreducible quintic in `T^7`: the five
  covers form a single Galois orbit over a quintic field.
* `W = 1` at a multiple root of `f` is impossible, so the face form can never
  be a power of a linear form — the multiplicity mechanism earlier sessions
  hoped for is unavailable here.

---

## 3. Results of this session

### 3a. Subcase 2 — EMPTY mod p

Cascade run over `GF(p)[T]/(h)` for every irreducible factor `h` of the
degree-35 eliminant, so all 35 face solutions are covered at once.  Result:
`f_1..f_8 = 0` and `p_1..p_8 = 0` forced, at **p = 999983 (128/128)** and
**p = 1000003 (144/144)**, complete coverage.  Since `f_8 = a_16_8` is the
vertex `(8,16)`, the polygon collapses to a triangle and the subcase is
empty.  The only surviving solutions are `P = a00 + q(u)z^2`,
`Q = b00 + t(u)z^3` — reconstructed and verified end-to-end (`[P,Q] = x^2`
exactly), with triangular Newton polygons.  Consistent with McKay–Wang
Cor 14 (isomorphism => triangle), which is a good sign.

### 3b. Subcase 1 — EMPTY mod p

Weight-graded cascade (`w = 2i - j` in that agent's convention) with the
vertex non-degeneracy imposed via a Rabinowitsch inverse of the product
`P(0,8) * P(8,16) * Q(0,12) * Q(12,24)`.  Down to level `W = -11` the ideal
is the **unit ideal**, for every one of the five covers, at
**p = 5189, 5441, 7523, 8053, 11827** — 25/25.  Each of the four vertex
coefficients is individually forced to zero.

**The subtlety that makes this non-trivial:** the all-parameters-zero point is
ALWAYS a solution (it is `P = face(P)`, `Q = face(Q)`, which genuinely
satisfies `[P,Q] = x^2`).  So "the ideal is proper" proves nothing whatever.
The vertex non-degeneracy conditions are what make the question real.  Any
future work must impose them.

Controls that passed before the verdict was trusted: positive (cascade
solutions reassembled into honest polynomials, `P_x Q_y - P_y Q_x = x^2`
verified by direct polynomial arithmetic, supports inside the polygons);
negative (without vertex conditions the same engine reports a live
2-dimensional component, not EMPTY); environment (pipeline reproduces EMPTY
on `trackD_targets_validate.json`); face vdim 35 mod each prime used.

### 3c. Independent verification (mine, from scratch)

`session44/verify/` rebuilds subcase 2 in ORIGINAL `(x,y)` coordinates with
its own polygon enumeration (exact half-plane test) and its own monomial
bracket, reusing none of the agents' builders.  It independently reproduces
25 + 47 lattice points, 92 bracket equations splitting **17/18/19/19/19** by
weight, the target at the deepest level, and face **dim 0, vdim 35**.  The
five `(u,z)` identities were re-derived by hand and CROSS-CHECKED against the
direct bracket at three random seeds — they agree exactly, up to the `-1`
that is the substitution's Jacobian.  `CROSSCHECK: PASS`.

### 3d. A characteristic-zero step that needs no computer

If `p = s = 0` the remaining identities read `-2 q g' = 0`, `3 f' t + q' r = 0`,
`f' r = 0`.  `q` and `t` are nonzero and `deg q = 8` gives `q' != 0`.  From
`f'r = 0`, either `f' = 0` or `r = 0`; if `r = 0` then `3f't = 0` forces
`f' = 0`; if `f' = 0` then `q'r = 0` forces `r = 0`.  Either way
`f' = r = g' = 0`, so **`f` and `g` are constants**, hence `f_8 = 0` (vertex
(8,16)) and `g_12 = 0` (vertex (12,24)) and neither polygon is the claimed
quadrilateral.  QED, characteristic zero.

**So the entire subcase-2 verdict reduces to one question: can `(p,s)` be
nonzero?**  That is the smallest remaining target and the best entry point
for a characteristic-zero proof.  Note `p = 0 => s = 0` already follows by
hand: `E3` becomes `2q's - 2qs' = 0`, i.e. `(s/q)' = 0`, i.e. `s = c*q`, and
`val s >= 2 > 1 = val q` forces `c = 0`.

Valuation/degree analysis of `E3` (done, no contradiction yet): with
`a = val p`, `b = val s`, the extreme coefficients force `b = a + 1` and
`(3a-2) p_a t_2 = 2a q_1 s_{a+1}`; at the top, either `deg p = 4`, or
`deg s = 8`, or `deg s = deg p + 4`.  None of these is empty on its own, so
the question is genuinely computational.

### 3e. An exact characteristic-zero witness (NOT a counterexample)

On the `deg q = 1` branch there is an exact solution over `Q(alpha)`,
`7 alpha^4 - 60 alpha^2 + 150 = 0` (irreducible over Q):

    P = a00 + x + alpha x^3 y^5 + x^5 y^10
    Q = b00 + x^2 y + (7 alpha/6) x^4 y^6 + (7 alpha^2/33 + 15/11) x^6 y^11
              + alpha(250 - 21 alpha^2)/528 x^8 y^16

`[P,Q] = x^2` identically — I re-verified this independently, residual
exactly 0.  It is NOT a counterexample: `N(P) = conv{(0,0),(1,0),(5,10)}` is a
triangle, the vertices (8,14) and (8,16) are absent, and `[P,Q] = x^2` is not
a constant in original coordinates.  Its value is as a *control*: it proves
the machinery produces genuine exact solutions when they exist, so an EMPTY
verdict elsewhere is not an artifact of the machinery.

---

## 4. Retractions — read before trusting any older memo

### 4a. The edge-gap analysis (RETRACTED, my error)

I claimed the face forms must commute on the `w`-maximal face of subcase 2
and inferred `face(P) = R^2`, `face(Q) = R^3`, `deg R = 4`.

The commuting step is **true but vacuous**.  That face lies on `j = 2i`,
a line THROUGH THE ORIGIN, so every monomial on it is a power of `t = x y^2`;
both face forms are polynomials in that single quantity and `[A(t),B(t)] = 0`
identically, for all coefficient values.  I had verified an implication whose
hypothesis was empty.

Explicit counterexample to the conclusion: `F = 1 + t^8`, `G = 1 + t^12`
commute (`8*24 - 16*12 = 0` on the only cross term) yet `F` has eight distinct
roots, so `F` is not the square of a quartic.

Second defect: `a_0_0` is the constant term of `P` and NEVER appears in
`[P,Q]`, so "`c_0 != 0` because (0,0) is a vertex" is a free normalisation,
not a constraint.

**Retracted:** `EDGE_GAP_FINDING.md` Claim 3, the `a_10_5` prediction's
reasoning, subcase 1's twin-face claim, the 1506-face census counts, the
MULTIFACE elimination figures.  Recorded in `RETRACTION.md` and
`session44/WGRADE_FINDING.md`.  **Imposing this premise would have cut the
solution set illegitimately and could have produced a spurious EMPTY** — the
worst failure mode available here.

Still standing: `PREDICTION_AND_SUBCASE1.md` sections 3-4.  For subcase 1's
`(-1,1)` face the weight is `w' = j - i`, the face forms are `y^8 F(xy)` and
`y^12 G(xy)`, and `[.,.] = 4 y^20 (3F'G - 2FG')`, whose vanishing IS a genuine
condition giving `F = R^2`, `G = R^3` with `deg R = 4`.  The `R^2/R^3`
machinery is legitimate there and only there.

### 4b. Other corrections made this session

* **Face census filter bug.**  `if tgt >= top: continue` discarded exactly the
  faces where the bracket top EQUALS the target — i.e. the essential face.
  This is why the decisive structure was missed for so long.
* **msolve linear form.**  msolve returns the eliminant with respect to a
  linear form of ITS OWN choosing, reported in its output.  I had assumed it
  was always the last variable, so after one substitution I was substituting
  roots of the wrong polynomial — which made the system look EMPTY at every
  prime.  Always read and check the reported form.
* **ODE identity.**  First attempt `h = u f^-3 g^2` returned check False;
  correct is `h = f^-3 g^2`, which verifies True.  With that,
  `W = f g (u h)'/h`.
* **Prop 3.12 route VOID.**  The face normal `(-2,1)` sits at 153.43 degrees,
  outside the required 270-315 degree arc.  No emptiness conclusion follows.
* **`case1_minlevel.py` off-by-one.**  It printed depth as `stopW + 1` but the
  descent breaks AFTER processing level `W`, so `stopW` is the deepest level
  included.  Fixed.  Real data points are depths `W = 0` (2 conditions) and
  `W = -1` (4 conditions), with a live component at both — the obstruction is
  genuinely not shallow, which is why the full verdict needs depth `W = -11`.
* **`walk_ideal.py`** failed validation (timed out at 540s on a target
  Singular decided EMPTY in 3s) and was killed rather than trusted.
* **Singular has no ternary operator** `? :` — it silently produces no output.
* **`pkill` self-match** (exit 144): the shell's own cmdline matches the
  pattern.  Use `ps -o pid=,cmd= | awk` and kill by explicit PID.

---

## 5. Verification standards in force

These were adopted after earlier losses and should not be relaxed:

1. Two primes must agree before any modular claim is stated.
2. Modular results are REPORTED AS MODULAR, always.
3. A solver's output is never trusted on its own — a candidate solution counts
   only when substituted back and checked to satisfy the identity exactly.
4. Every instrument is validated on a control with a KNOWN answer before it is
   pointed at an open question.  Positive AND negative controls.
5. A candidate is not a counterexample until lifted to honest polynomials in
   ORIGINAL coordinates (no denominators) with the Jacobian verified to be a
   nonzero constant exactly.

Controls that exist and pass, reusable:
`session44/mckay_wang.py` (McKay–Wang JPAA 40 (1986) Cor 14 certificate;
detects the Mondello char-2 CE, does not flag a tame automorphism),
`session44/leweber.py` (Le–Weber Kodai 17 (1994) canonical-divisor sieve,
C1/C2/C3 pass), `session44/lead4/dk_eliminate.py` (reproduces GGHV's published
eliminant (5.9) `8G^3 + 18 G d1 dm1^6 + 27 d0 dm1^9` EXACTLY — this validates
the whole elimination pipeline against the literature).

---

## 6. Where the files are

    session44/verify/            my from-scratch independent rebuild
        indep2.py                (x,y) polygon + bracket, own enumeration
        uz_indep.py              hand-derived (u,z) identities + CROSSCHECK
        face_solve_indep.py      face system + the char-0 hand proof in its docstring
        facepts.py               rational face points, self-verifying
        README.md                what was confirmed and how
    session44/lead4/uz_*.py      subcase 2: (u,z) system, cascade, extension runs
    session44/lead4/case1_*.py   subcase 1: face derivation, cascade, verdicts, symmetry
    session44/lead4/cascade.py   the weight-graded linear cascade
    session44/lead4/face_eq.py   the face equation W(u) = 1 in the f,g gauge
    session44/lead4/dk_eliminate.py   GGHV (5.9) reproduction — the pipeline control
    session44/CASCADE_STATUS.md  status at the point the quotient-ring step was identified
    session44/WGRADE_FINDING.md  independent retraction + the 1+t^8 counterexample
    session44/RETRACTION.md      the retraction record
    session44/SOURCE_GGHV2204.md, MCKAY_WANG_CERTIFICATE.md, LEWEBER_SIEVE.md,
    session44/LIT_BATCH3.md, JELONEK_ASSESS.md, ESSENTIAL_FACE.md

---

## 7. Next steps, ranked

**1. Upgrade the verdicts to characteristic zero.**  This is the highest-value
work and it is well-defined.  Two routes:

   * *Subcase 2, cheap route.*  Prove `(p,s) = 0` on the `deg q = 8` branch.
     Section 3d then finishes the subcase in characteristic zero with no
     further computation.  This is a question about the linear operator
     `E3(p,s) = 3p't + 2q's - pt' - 2qs'` over the quintic field carrying the
     five covers.  Known kernel element: `(0, c*q)`, excluded by the support
     constraint `val s >= 2 > 1 = val q`.  The reported kernel dimension was
     2 — IDENTIFY THE SECOND ELEMENT.  That is the crux and it is small.
   * *Subcase 1, heavy route.*  Redo the cascade over the quintic number field
     down to depth `W = -11`.  Mechanical but expensive; the minlevel probe
     says shallow depths do not suffice.

**2. Finish the two verification runs that were stopped.**  A 71-variable
direct Gröbner (`session44/verify/indep2_v816_p65521.sing`, asks whether
`<92 bracket equations> + <W * A8_16 - 1>` is the unit ideal — a fully
independent brute-force confirmation) and a characteristic-zero face
computation (`faceg2_p0.sing`).  Both were killed mid-run at the user's
instruction, not because they failed.

**3. Write it up.**  If the closure survives, this is a paper-shaped result:
the degree bound for plane Jacobian counterexamples becomes 125 with no
exceptional case.

**4. If continuing the counterexample hunt.**  Be clear-eyed: searching above
degree 125 is unstructured.  What made `(72,108)` decidable was the Newton
polygon being pinned to two specific shapes — 72 unknowns instead of ~16,000.
No comparable classification exists above 125.  The honest prerequisite for a
CE search up there is extending the polygon classification first.  Older
pending leads, unaffected by this session, are tracked in the task list:
the B=16 Abel ladder past `deg(q1) = 12`, Gröbner on the dim-3 loose charts
(F17 r=1, (9,27)-chain r=1), the `mu3 = 0` stratum audit, and the 732-chart
superset tier.

---

## 8. Honest assessment

Every computation this session came back empty, by independent routes, with
controls passing.  The parameter budget said it would: after the face is
fixed there are 16 free parameters against 38 conditions, overdetermined by
22.  I do not think there is a counterexample in this case, and nothing found
here suggests one is nearby.

The result worth having is the degree bound.  It is real, it is the exact
computation GGHV said needed more power than they had, and it is currently
modular — one clearly-defined step away from being a theorem.
