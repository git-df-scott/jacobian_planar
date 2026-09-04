# ASTRA reconciliation — 2026-09-04

## Verdict first

No explicit Keller pair, CEC, or CE was found.  The routed repository state is
consistent after the stale and over-strong statements listed below are
downgraded.  The strongest new result is an `EXACT-Q`, six-blowup
target/source exclusion for the H3 blueprint; see
`TARGET_SOURCE_COMPATIBILITY.md`.

## Routed heads

The audit used the requested order and pinned every workstream before comparing
claims.

| role | ref | audited head |
|---|---|---|
| public entry point | `main` | `b9f5cb89676286c2a3ec8ea43562f0abbba91b5d` |
| branch map / PR #25 | `claude/github-repo-organization-wdr8n7` | `5c41b3afbbc2927560c3c193ac3cd39b2571786b` |
| target audit / PR #24 | `claude/jc2-counterexample-hunt-handoff-x40ahz` | `0aab6fb4036a4c4bff7e375a2bf9454a22a60790` |
| night run / PR #23 | `claude/jc2-counterexample-hunt-handoff-w369mc` | `e0086a78682a1b91fe483f16e5698b8eda48b6eb` |
| CE plan / PR #22 | `claude/jc2-handoff-audit-hartnc` | `ae58bd33dc6a037e9d421a8a0b102c1ad7a2d6f3` |
| historical canon | `claude/opus-5-counterexample-plan-sep6yk` | `b233c708e9b43c597f6f2fa2e82a9b04fb5dd55a` |
| graded case-(2) lane | `claude/poisson-bracket-counterexample-9esk1r` | `10469087a97ca4143ce8a278f3ce0211143ced19` |
| mate lane | `codex/sol-session3-pole` | `df7471deb9207422b2a5f0b8661f3a7f05f7fee6` |

`main` is therefore an entry point, not a merge of the current research
state.

## Reconciliation decisions

1. **B=16 ladder.**  `STATE_FULL.md` still displays rows later voided in
   `CATCHES.md` after the GGV row-3 transcription error was found.  In
   particular, the stale d=6 through d=12 `EMPTY` display is not evidence.
   Only rows explicitly re-established on the corrected equations may be used.

2. **Case-(2) quadrilateral.**  `p108_525122` is the GGHV Proposition 4.3
   case-(2) reduced polygon.  The graded archive proves a full
   `EMPTY-mod-p` result at p=32003.  Its p=1000003 archive kills only one
   rational orbit.  No exact-Q lower-level certificate was located.

3. **Conflicting characteristic-zero descriptions.**  One handoff describes
   a degree-35 field calculation; historical canon describes a residual object
   over a degree-1144 eliminant.  No checked map between those objects was
   found.  The characteristic-zero status of case (2) is therefore `UNKNOWN`.

4. **Wrong instrument.**  PR #23's proposed depth-6 y-adic continuation on
   case (2) is superseded by the grading rho=2i-j.  The y-adic timeout is a
   `WALL`, not evidence about the variety.

5. **Above 125.**  The 12 exact-Q monomial certificates above the old bound
   certify the compiler strata that produced them.  They do not close their
   published cases because the compiler's A'_t default and c' ladder are still
   unverified there.

6. **Target audit.**  PR #24 is a bounded enumeration for the curves and
   degrees explicitly listed.  Its timeouts and missing runs stay `UNKNOWN`.
   The H3 and A8 near-misses are not candidates.

7. **Source audit.**  The archived 11,465-tree count replays, but the old
   search restricts each coordinate to at most two horizontal components of
   degree at most two.  It does not directly test the H3 target degrees
   (3,5)/(3,6).  The new ASTRA H3-specific search removes that degree/support
   cap by solving the complete complementarity problem on the same tree list.

## Replays and controls

| check | result | label |
|---|---|---|
| graded Poisson identity plus five `{P,Q}=x^2` witnesses | pass, coefficientwise over Q | `EXACT-Q` |
| Briançon chart identities and gradient ideals for `g,g'` | both Groebner bases are `[1]` over Q | `EXACT-Q` |
| Briançon infinity valuations | `(0,0,0)` for each t=1 fibre | `EXACT-Q` plus stated genus theorem |
| abstract target pre-screen | 5,261 rows, 635 basic signatures | `ADMISSIBLE-SHAPE` |
| independent H3 permutation enumeration | one simultaneous-conjugacy orbit, order 60, Euler 1, coarse chi(R)=0 | `EXACT-Q` / `BLUEPRINT` |
| archived boundary generator | 11,465 records through six blowups | exact replay of generator |
| H3 target/source complementarity | zero P-coordinate solutions for both (3,5) and (3,6) on those records | `EXACT-Q`, bounded |
| graded case-(2) archive hashes and F_32003 factorization | hashes pass; factor degrees 1+1+3; all five orbits have `[1]` logs | `EMPTY-mod-p` |

The curve-by-curve braid/GAP enumeration could not be independently executed
in this runtime because GAP is absent.  This is a tooling wall only.  The pure
Python abstract count and H3 group computation above were independently
replayed.

The source/target comparison also yields an adjunction bridge not present in
the inherited screens: `chi(P fibre)=sum_E(k_E-1)dP_E`.  After subtracting the
escape contribution, all remaining P-horizontal components have weighted sum
D, and likewise for Q.  For H3 both non-escape budgets equal +6, recovering
the target fibre values `-6` and `-14/-18` exactly.

## Machine-readable evidence

All new scripts are under `astra/`; exact outputs are under
`astra/artifacts/`.  Run `python3 astra/run_controls.py` from the repository
root to refresh them.
