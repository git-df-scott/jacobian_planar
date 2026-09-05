# Session 44 — new-angle CE plan (post-Session-43 context sweep)

Date: 2026-08-26. Branch: `claude/past-code-session-8mdjqn`.
Full context absorbed from: PR #19 (Session 43), `codex/sol3-all-five`
(campaign rundown + FABLE_* corpus), `codex/sol5-collision-first`,
`codex/sol5-counterexample-hunt`, `codex/sol6-collision-first`,
`claude/claude-opus5-mailbox` ledgers (STATE_FULL / LIVE_MAP / OPEN_ITEMS /
TRUST_MAP), session reports 39–42 (treated as done per user), and the
state-transfer tree.

Binding gate (unchanged, from the campaign rundown): a CE exists only when
explicit `P,Q` over a char-0 field verify `[P,Q]=1` coefficientwise and two
distinct points share an image. Everything else is a candidate.

## Where the frontier actually is (one paragraph)

Geometric degree 2–5 excluded, **6 open**. `(72,108)` is the last pair below
125 (case (2) is 3-prime modular only; pentagons no verdict). `B=16` alive
(Żołądek 4.10 gap), frontier cells OOM on 14 GB boxes. 24 published shapes in
`[125,150]` never attacked (FABLE_24). The one *live, reduced, currently
walkable* object is sol6's `(4,6)` collision ribbon at degree 126: a
three-parameter formal branch `(u,v,w)` survives the kernel-retaining
recurrence exactly through `x^2`; one planted rational point survived to
`x^21` and died only at the forced nonzero `p3[22]` (degree boundary). Nobody
has searched the `(u,v,w)` space itself.

## The leads (new ways, ranked)

### Lead 1 — Hunt the (u,v,w) obstruction variety of the (4,6) ribbon  ★ ACTIVE
Kepler/Neptune: treat the degree-boundary obstruction as *data*, not verdict.
The recurrence makes every later coefficient a function of `(u,v,w)`; the
forced `p3[22]`, `p3[23]`, … are polynomials `O_1, O_2, …` in three variables.
A CE on this chart must satisfy all of them; conversely `{O_1=O_2=O_3=0}` is
expected 0-dimensional, so it can be *solved*, not sampled: interpolate the
`O_i` mod p by running the recurrence on grids, eliminate (resultants /
3-var Gröbner mod p — small), verify candidate points at a second prime,
Hensel-lift, then run the untested gates (second collision row `q0(1)=0`,
vertex nonvanishing, exact replay). Positive control: the planted seed's
exact `p3[22] = 421966423176051225964907643652535431/885443715538058477568`.
Exceptional charts `u=0` (kernel coefficient `3u/4` dies) and the widened
slice (free low coefficients of `p0..p3`) queued behind the generic chart.
Either outcome is decisive for the campaign's only live reduced frontier:
candidate points, or the generic chart of the (4,6) ribbon dies at two primes.

### Lead 2 — The (4,6) collapse invariant (Einstein compression)
The (2,3) ribbon died by an exact mechanism: the surviving rows assemble into
`dH/dx = 1` with `H` a polynomial in `w = v^2−4u` — impossible degrees. Find
the analogous composite invariant for `(4,6)` at a *small model degree*
(same ribbon structure, tiny triangle) where full symbolic work is cheap. If
the collapse generalizes: all-degree kill of the lane (frees the campaign).
If it breaks: the breaking term is exactly where a CE can live — feed Lead 1.

### Lead 3 — d = 6 topological sieve (Blue LED: change the representation)
Session 43's tear theorem forces an irreducible tear to be a singular rational
curve with one place at infinity, fibre count 1, plus the exact Euler identity
`Σ(d−n_i)χ(A_i) = d−1` and an 83-entry admissible-configuration catalogue at
d=6. New representation never used by the campaign: over the target complement
of the tear, a CE *is* a 6-sheeted étale covering, i.e. a transitive
representation `π₁(C²∖C) → S₆` with constrained meridian data (cusp-type
groups `⟨a,b | a^p = b^q⟩` for one-place-at-infinity cuspidal `C`), and
escape/χ bookkeeping from the Euler identity. Enumerate exactly (pure
combinatorial group theory, no RAM wall). Output: the finite list of
admissible topological types at the open floor — construction targets with
cusp data pinned — or emptiness, which raises the floor for irreducible tears
above 6. Control: the formalism must kill d=2 instantly (a permutation in S₂
with exactly one fixed point does not exist) and must *not* kill d=3 by group
theory alone (Alpöge's 3D map's stratification is the model; d=3 dies only by
Orevkov, which is invisible to the sieve).

### Lead 4 — 144 = 144 (Penicillin: the anomaly as the object)
Three artifacts sit at the same number and nobody has connected them: the
genuine degree-144 reduced component (residual 1e-14, reverse-lift defect
~2.5e3), the B=16 resonant cell d=12 (12d = 144 = 12², rational roots −1/12,
1/20), and the d=12 *unsaturated* cell — the campaign's self-described
biggest anomaly ("degenerate family?", undecided after 2 kills while the d=3
analogue is instant). Test whether these are the same object; run the
unsaturated d=12 system to a verdict treating the degenerate family as the
find, not the noise. If the reduced component is the resonance kernel, the
lift defect becomes an inverse problem: which missing support component
generates exactly that defect pattern.

### Lead 5 — Cross-prime Mondello transfer (H. pylori: attack "char p is noise")
Mondello's char-2 CE has geometric degree 3 — *coprime to p*, so it is not an
Artin–Schreier/Frobenius artefact. Session 43's `charp_ladder` measured the
wrong invariant (minimal total degree, which Artin–Schreier trivially makes
p). The right question: do *prime-to-p geometric degree* planar Keller CEs
exist at p = 3, 5, 7 with a p-stable shape? Sweep the unit-monomial families
(`u = 1+x^k y`, `P = x^a u^b + x^m u^n`, `Q = y + x^r u^s`, plus small
perturbations — Keller is linear in Q, noninjectivity brute-forced over F_p,
F_{p^2}, F_{p^3}) with Mondello@p=2 as the positive control. Any shape alive
at two primes is a bounded-degree family across primes — the certified road
to char 0 (an emptiness certificate has finitely many bad primes).

### Lead 6 — Audit the canon's discard steps (O-rings: the background variable)
The campaign found a misprint in GGV (1.2) and a gap in Żołądek 4.10 — but
never audited the discard steps it builds on: GGHV Cor 5.7 (kills (9,27),
"never re-derived by anyone"; the campaign's independent test was queued,
outcome unrecorded) and Prop 6.1 (kills F22). Also: four independent routes
found `[P,Q]=x` solvable *only with Newton vertices vanishing* — the vertex
condition is the recurring obstruction, and the vertex-nonvanishing discards
in the shape theory are exactly where a mistake would hide a live case.
Re-derive one discard independently; a gap means an uncounted open case.

### Standing inherited targets (not new, kept visible)
The 24 published untouched shapes (first: (8,28) with (m,n)=(3,4), max 144);
B=16 d=8 chart N (30 eq/23 unk — needs >14 GB or a staged eliminator);
pentagon seed-extension 241/123 (same wall); case (2) char-0 confirmation.

## Session 44 execution order
1 (hunter running) → 5 (background sweep on spare cores) → 2 → 3 → 4/6 as
time allows. Every instrument calibrated on a known value before use; every
negative stated with its strength; no reduced point called a CE.
