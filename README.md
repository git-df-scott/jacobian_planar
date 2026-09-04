# jacobian_planar

This repository is a research archive for the plane Jacobian-conjecture campaign. It contains exact algebra, computational experiments, audits, retractions, and handoff material. **No counterexample has been found.** The repository is deliberately conservative: a timeout is not an EMPTY result, a modular result is not a characteristic-zero proof, and a numerical miss is not evidence of emptiness.

## Start here

1. **Current campaign state:** [`STATUS.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/STATUS.md)
2. **Complete re-walk and open queue:** [`STATE_FULL.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/STATE_FULL.md), [`OPEN_ITEMS.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/OPEN_ITEMS.md)
3. **What is closed, live, or retired:** [`LIVE_MAP.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/LIVE_MAP.md), [`TRUST_MAP.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/TRUST_MAP.md)
4. **Corrections and failed-proof ledger:** [`CATCHES.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/CATCHES.md)
5. **Branch audit:** [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md) — full inventory of every branch, confirms nothing pushed to GitHub has been lost, and checks each branch against what this README claims about it.
6. **Latest handoff (not yet merged):** [`docs/plans/HANDOFF_CE_HUNT.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/jc2-handoff-audit-hartnc/docs/plans/HANDOFF_CE_HUNT.md) on `claude/jc2-handoff-audit-hartnc` (PR [#22](https://github.com/git-df-scott/jacobian_planar/pull/22)) is the most recent self-contained "read this first" for a fresh session — where every verified artifact lives, how to rebuild the worktrees/engines, and the ordered direct attempts with gates and stop rules. See [Open pull requests](#open-pull-requests) below for the night-run logs that continue past it.
7. **Session narrative:** [`docs/history/sessions-01-18-status.md`](docs/history/sessions-01-18-status.md), [`docs/sessions/active/`](docs/sessions/active/), [`docs/sessions/archive/`](docs/sessions/archive/)

The full scripts, certifiers, logs, and generated data are on the campaign branch. The `main` branch is the lightweight map and archive index.

**For a new Claude or Codex session:** read this README top to bottom before touching any branch. It is the map; `STATUS.md` on the canonical branch is the verdict; `CATCHES.md` is the list of mistakes not to repeat.

## Cross-chat JC2 handoff audit

The archived Codex/Claude conversations were checked against the live branches. The older handoff is useful provenance, but its verdicts remain subordinate to the current campaign files.

- The strongest inherited asset is the reconstructed characteristic-zero bottom-seed target over `Q(alpha)`, degree five: 164 variables, 288 quadratic equations, 6,821 terms. It has **NO VERDICT** in characteristic zero.
- The specialized reduction at `p=1000003` has an independently reproduced unit Gröbner basis and is **EMPTY mod-p** only; that does not prove characteristic-zero emptiness.
- The corrected level-16 pentagon calculation is a joint condition (`F0 = F1 = a0^3 lambda = 0`), not the previously suggested `sigma^6 | h7` ladder. The quick level-16/15/14 kill path is therefore closed.
- The bottom quintic orbit does not pin six independent pentagon vertices. It leaves a nonzero residual torus parameter `t`; the transfer audit and exact coefficient formulas are recorded on `codex/pentagon-p11-zero-search`.
- The exact formal order-two gate and tested structured families are empty only in their stated restricted systems. The unsaturated polynomial core is nonempty, and the full CE-bearing root remains **NO VERDICT**.
- The above-125 tail census found new exact system families, but 189 records did not close because the unprinted `A'_t` provenance assumption is load-bearing. This is an open audit, not a CE result.
- The six proposed follow-up leads (exclusion audit, non-injectivity transport, Weyl/Dixmier route, tail saturation, the `k=0` cover transition, and beyond-bound search) are research directions, not established results.
- The archived mailbox handoff reached `OPUS43-012` (remote mailbox snapshot `7db7ff2`); the corresponding Codex reply `e4dc2fc` was local-only and must not be presented as delivered. The next assigned checks were the rank-five Corollary 5.7 slices, a bounded characteristic-zero attack, and provenance auditing for the 184 new tail hashes / 189 nonclosing cases.

Operationally: read the canonical campaign branch first, then the relevant Codex branch and mailbox artifacts. Do not treat stale transfer archives, timeouts, OOMs, modular results, or solver output without certificates as a JC2 verdict. No archived chat supplied a verified Jacobian-conjecture counterexample.

## Bottom line (latest audited state)

- **No plane Jacobian counterexample has been produced.** Nothing has passed the HIT protocol.
- The Borisov framework route is closed by an exact endgame obstruction for the reachable admissible charts. This is a result about that constructive family, not a disproof of the Jacobian conjecture.
- The corrected B=16 ladder is exact EMPTY in characteristic zero for `d = 3..7`. The corrected `d = 8..12` chart-N cells, the resonant `d = 27` cell, and the unsaturated family remain open or require uninterrupted exact runs; earlier claims based on the printed system were retracted.
- The surviving degree territory `(72,108)/(108,72)` remains open. The pentagon (case 1) bottom edge has been classified computationally and has admissible seeds modulo tested primes, but full extension runs timed out. Case (2) is EMPTY at several primes, while its characteristic-zero residual system remains open. The literature-only `(9,27)` kill was found to contain an unproved step and is being treated as live until independently settled.
- Above degree 125 is the largest unsearched region: many targets still need the chain-compiler extension. Forty-one timeout shapes and several small-cell/VR routes are also open.

## Branch map

Use the branch that matches the question. Do not search every branch by default.

### Canonical / campaign branches

| Branch | Use it for |
| --- | --- |
| [`main`](https://github.com/git-df-scott/jacobian_planar/tree/main) | This index, organized session notes, and transfer archives. |
| [`claude/opus-5-counterexample-plan-sep6yk`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-5-counterexample-plan-sep6yk) | **Canonical full campaign state**: `STATUS.md`, `STATE_FULL.md`, `LIVE_MAP.md`, `OPEN_ITEMS.md`, `CATCHES.md`, `wave0/`, `wave1/`, `wave5/`, `wave6/`, and all certifiers. Head `b233c70` (prime-sweep continuation, plus the 2026-09-04 stale-file cleanup). |
| [`claude/plane-counterexample-endgame-az3geq`](https://github.com/git-df-scott/jacobian_planar/tree/claude/plane-counterexample-endgame-az3geq) | Endgame/framework work and the earlier full campaign snapshot. |
| [`claude/fable-ce-backup`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-ce-backup) | Backup branch for the corrected ladder and overnight queue. |
| [`claude/opus-errors-false-proofs-820rmd`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-errors-false-proofs-820rmd) | Error analysis, retractions, and false-proof audit material. |
| [`claude/opus-hunt-territories`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-hunt-territories) | Territory ranking and candidate-hunt planning. |
| [`claude/opus-plan-priority-queue-0pultj`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-plan-priority-queue-0pultj) | Priority queue and next-run planning. |
| [`claude/opus-support-compute`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-compute) | Compute support and run artifacts. |
| [`claude/opus-support-toolchain-62st0d`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-toolchain-62st0d) | Toolchain/build support. |
| [`claude/opus-worker-resisters`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-worker-resisters) | Resister/timeout worker outputs. |

### Claude workstreams

These are focused or historical worktrees; their names are the routing key.

`ce-acquisition-strategy`, `counter-example-audit`, `d23-borisov-transfer-test`, `fable-6o0nqe`, `fable-counterexample-sweep`, `ggv-conjecture-evidence`, `github-push-issue`, `jacobian-collision-counterexample`, `jacobian-conjecture-campaign`, `jacobian-conjecture-search`, `jacobian-planar-sweep`, `mod-3-keller-pair-obstruction`, `moduli-deformation-exceptions`, `past-code-session`, `poisson-bracket-counterexample`.

Three more recent workstreams continue past the canonical branch's `24a06fc`-era campaign work and are not yet folded in:

| Branch | Use it for |
| --- | --- |
| [`claude/jc2-handoff-audit-hartnc`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-handoff-audit-hartnc) | The unified fleet plan, the 2026-09-02 ground-cover audit (455 exported systems by content hash), and `docs/plans/HANDOFF_CE_HUNT.md` — read this one first. |
| [`claude/jc2-counterexample-hunt-handoff-w369mc`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-counterexample-hunt-handoff-w369mc) | The 2026-09-03 overnight run log against the handoff's direct attempts: strata killed by exact monomial certificates, the case (2) depth-6 timeout, and the next session's priority order. |
| [`claude/jc2-counterexample-hunt-handoff-x40ahz`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-counterexample-hunt-handoff-x40ahz) | The Vitushkin-search sweep logs (dicritical test, cusp families, group-first screen) — a parallel line of attack, not yet reconciled with the ground-cover register. |

Use the canonical campaign branch for the latest adjudicated verdict; use these branches only when tracing the named subproblem or its provenance.

### Codex workstreams

| Branch family | Use it for |
| --- | --- |
| `codex/claude-opus5-mailbox` | Mailbox/handoff coordination. |
| `codex/pentagon-level14-rational-obstruction`, `codex/pentagon-level16-exact`, `codex/pentagon-p11-zero-search` | Pentagon exact levels and obstruction searches. |
| `codex/sol-session3-pole`, `codex/sol3-all-five` | Session-3/pole and Sol-3 explorations. |
| `codex/sol5-collision-first`, `codex/sol5-counterexample-hunt` | Sol-5 collision and candidate hunts. |
| `codex/sol6-collision-first` | Sol-6 collision-first work. |

These branches are parallel investigations, not independent final verdicts. Reconcile claims against `STATUS.md` and `CATCHES.md` before quoting them.

The [`work`](https://github.com/git-df-scott/jacobian_planar/tree/work) branch is an additional audit/work area; it is not the canonical state.

### Exact branch heads (2026-09-04)

This compact ref list is the handoff index. The short commit ID makes it possible to verify that an agent opened the intended snapshot without scanning unrelated history. Refreshed 2026-09-04 after a repo-wide cleanup pass removed four stale root-level files (`39`, `40.md`, `41.md`, `42.md`) from every branch that still had them, which moved almost every head below past its previous value; see [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md) for the full accounting of that pass and confirmation that nothing was lost.

| Family | Branch | Head |
| --- | --- | --- |
| Main | [`main`](https://github.com/git-df-scott/jacobian_planar/tree/main) | `b9f5cb8` |
| Other | [`work`](https://github.com/git-df-scott/jacobian_planar/tree/work) | `5627f34` |
| Claude | [`claude/opus-5-counterexample-plan-sep6yk`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-5-counterexample-plan-sep6yk) | `b233c70` |
| Claude | [`claude/plane-counterexample-endgame-az3geq`](https://github.com/git-df-scott/jacobian_planar/tree/claude/plane-counterexample-endgame-az3geq) | `72e6ce5` |
| Claude | [`claude/fable-ce-backup`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-ce-backup) | `0d6dee1` |
| Claude | [`claude/opus-errors-false-proofs-820rmd`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-errors-false-proofs-820rmd) | `1ebeece` |
| Claude | [`claude/opus-hunt-territories`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-hunt-territories) | `99b3650` |
| Claude | [`claude/opus-plan-priority-queue-0pultj`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-plan-priority-queue-0pultj) | `784eacf` |
| Claude | [`claude/opus-support-compute`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-compute) | `b6bf58c` |
| Claude | [`claude/opus-support-toolchain-62st0d`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-toolchain-62st0d) | `83e0f80` |
| Claude | [`claude/opus-worker-resisters`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-worker-resisters) | `215a040` |
| Claude | [`claude/ce-acquisition-strategy-uyqftb`](https://github.com/git-df-scott/jacobian_planar/tree/claude/ce-acquisition-strategy-uyqftb) | `2a9fb4c` |
| Claude | [`claude/counter-example-audit-dnu9l9`](https://github.com/git-df-scott/jacobian_planar/tree/claude/counter-example-audit-dnu9l9) | `b0bd0ad` |
| Claude | [`claude/d23-borisov-transfer-test-vpr3m6`](https://github.com/git-df-scott/jacobian_planar/tree/claude/d23-borisov-transfer-test-vpr3m6) | `7296164` |
| Claude | [`claude/fable-6o0nqe`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-6o0nqe) | `a105bc9` |
| Claude | [`claude/fable-counterexample-sweep-yyj5vf`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-counterexample-sweep-yyj5vf) | `35c7281` |
| Claude | [`claude/ggv-conjecture-evidence-r9almu`](https://github.com/git-df-scott/jacobian_planar/tree/claude/ggv-conjecture-evidence-r9almu) | `f5e5397` |
| Claude | [`claude/github-push-issue-oftsm3`](https://github.com/git-df-scott/jacobian_planar/tree/claude/github-push-issue-oftsm3) | `f738744` |
| Claude | [`claude/jacobian-collision-counterexample-nsc6ul`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-collision-counterexample-nsc6ul) | `8b5adec` |
| Claude | [`claude/jacobian-conjecture-campaign-xcw9p4`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-conjecture-campaign-xcw9p4) | `fbd2864` |
| Claude | [`claude/jacobian-conjecture-search-om7slv`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-conjecture-search-om7slv) | `df9f911` |
| Claude | [`claude/jacobian-planar-sweep-iajyma`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-planar-sweep-iajyma) | `f307232` |
| Claude | [`claude/jc2-handoff-audit-hartnc`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-handoff-audit-hartnc) | `ae58bd3` |
| Claude | [`claude/jc2-counterexample-hunt-handoff-w369mc`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-counterexample-hunt-handoff-w369mc) | `e0086a7` |
| Claude | [`claude/jc2-counterexample-hunt-handoff-x40ahz`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jc2-counterexample-hunt-handoff-x40ahz) | `387d28e` |
| Claude | [`claude/mod-3-keller-pair-obstruction-oceq9z`](https://github.com/git-df-scott/jacobian_planar/tree/claude/mod-3-keller-pair-obstruction-oceq9z) | `70025d3` |
| Claude | [`claude/moduli-deformation-exceptions-2f4ey2`](https://github.com/git-df-scott/jacobian_planar/tree/claude/moduli-deformation-exceptions-2f4ey2) | `2ea44d8` |
| Claude | [`claude/past-code-session-8mdjqn`](https://github.com/git-df-scott/jacobian_planar/tree/claude/past-code-session-8mdjqn) | `37d2ebe` |
| Claude | [`claude/poisson-bracket-counterexample-9esk1r`](https://github.com/git-df-scott/jacobian_planar/tree/claude/poisson-bracket-counterexample-9esk1r) | `1046908` |
| Codex | [`codex/claude-opus5-mailbox`](https://github.com/git-df-scott/jacobian_planar/tree/codex/claude-opus5-mailbox) | `2875093` |
| Codex | [`codex/pentagon-level14-rational-obstruction`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-level14-rational-obstruction) | `b57cd27` |
| Codex | [`codex/pentagon-level16-exact`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-level16-exact) | `ae717ed` |
| Codex | [`codex/pentagon-p11-zero-search`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-p11-zero-search) | `1aed0b4` |
| Codex | [`codex/sol-session3-pole`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol-session3-pole) | `df7471d` |
| Codex | [`codex/sol3-all-five`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol3-all-five) | `e43947e` |
| Codex | [`codex/sol5-collision-first`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol5-collision-first) | `1d814dd` |
| Codex | [`codex/sol5-counterexample-hunt`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol5-counterexample-hunt) | `a5a8327` |
| Codex | [`codex/sol6-collision-first`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol6-collision-first) | `fd113a5` |

## Open pull requests

Every workstream branch above has a corresponding **draft** PR against `main` (a few chain against another workstream branch instead — see their base in the list below); none has been merged. That is deliberate: `main` stays a lightweight index, and a PR here is a labelled, reviewable unit of work rather than a merge candidate. Do not merge one of these without checking its claims against `STATUS.md` and `CATCHES.md` on the canonical branch first — several were superseded or partially retracted by later sessions. Newest first:

| PR | Base | Title |
| --- | --- | --- |
| [#24](https://github.com/git-df-scott/jacobian_planar/pull/24) | `main` | Clues audit across all branches, 2026-09-03 |
| [#23](https://github.com/git-df-scott/jacobian_planar/pull/23) | `main` | JC2 counterexample hunt: night run log and direct attempts |
| [#22](https://github.com/git-df-scott/jacobian_planar/pull/22) | `main` | Add unified JC2 counterexample-hunt fleet plan with audit appendix |
| [#21](https://github.com/git-df-scott/jacobian_planar/pull/21) | `main` | night1: deformation depth-map engine for the JC2 campaign |
| [#20](https://github.com/git-df-scott/jacobian_planar/pull/20) | `main` | Session 44 — full audit plan + four calibrated new-angle instruments |
| [#19](https://github.com/git-df-scott/jacobian_planar/pull/19) | `main` | Session 43 — the C* lane closed, the Keller condition collapsed, and three lanes run to verdict |
| [#18](https://github.com/git-df-scott/jacobian_planar/pull/18) | `main` | Graded reduction for {P,Q}=x^2, and a verdict on the live (72,108) resister |
| [#17](https://github.com/git-df-scott/jacobian_planar/pull/17) | `main` | Fable sweep: findings and game plan for the counterexample hunt |
| [#16](https://github.com/git-df-scott/jacobian_planar/pull/16) | `main` | Solve pentagon cascade level 17 and add controlled residual-edge checks (`work`, not draft) |
| [#15](https://github.com/git-df-scott/jacobian_planar/pull/15) | `claude/jacobian-planar-sweep-iajyma` | **[MAILBOX — DO NOT MERGE]** Codex ↔ Claude Opus 5 handshake |
| [#14](https://github.com/git-df-scott/jacobian_planar/pull/14) | `main` | Session 43: the pentagon target was mis-specified — pent_L23.ms is NONEMPTY in every chart |
| [#13](https://github.com/git-df-scott/jacobian_planar/pull/13) | `claude/opus-5-counterexample-plan-sep6yk` | Bottom-edge orbit structure settled; A1 answered; pentagon reduced 283/165 → 212/95 |
| [#12](https://github.com/git-df-scott/jacobian_planar/pull/12) | `main` | wave6/ms_opus: resister worker results (16 systems + control) |
| [#11](https://github.com/git-df-scott/jacobian_planar/pull/11) | `claude/opus-5-counterexample-plan-sep6yk` | ggv: computational evidence and structure data for the GGV B=16 conjecture (G1-G5) |
| [#10](https://github.com/git-df-scott/jacobian_planar/pull/10) | `claude/plane-counterexample-endgame-az3geq` | Hunt: five-territory sweep (GGHV audit, same-sign sector, symmetry slices, lift pipeline, Gao audit) |
| [#9](https://github.com/git-df-scott/jacobian_planar/pull/9) | `main` | Adjudicated record + Wave 5: the B=16 door closed past the 2013 stall |
| [#8](https://github.com/git-df-scott/jacobian_planar/pull/8) | `main` | Solve the endgame residue equation; repair the (99,66) emptiness proof |
| [#7](https://github.com/git-df-scott/jacobian_planar/pull/7) | `main` | Waves 2–3: refute H1c, repair the framework proof, refute the Session 38 collapse, answer Path A's A1 |
| [#6](https://github.com/git-df-scott/jacobian_planar/pull/6) | `main` | Plan 43 Waves 0–1: THEOREM 2/3 discharged, the (108,72) framework kill made unconditional |
| [#5](https://github.com/git-df-scott/jacobian_planar/pull/5) | `main` | Sessions 19–38: framework closure, the tangent sweep, and the GGHV (8,28) relation |
| [#3](https://github.com/git-df-scott/jacobian_planar/pull/3) | `main` | Counterexample audit campaign: night plan + Sessions 19–20 verification run |
| [#2](https://github.com/git-df-scott/jacobian_planar/pull/2) | `main` | Sessions 19–20: mod-3 wall re-derived (verdict (c)); (66,99) closed since 2022; retarget to (72,108) |
| [#1](https://github.com/git-df-scott/jacobian_planar/pull/1) | `main` | D=23 transfer test: Borisov Second Framework (Phase 0 → 1 → 2) |

None of these PRs claims a counterexample; several were later narrowed or retracted (see `CATCHES.md`). #4 does not exist (skipped/never opened).

## Evidence rules

1. Read the verdict file and its stderr/log before trusting an output file.
2. `[-1]` after a parser error, an empty output after timeout/OOM, and an unverified modular contradiction are **failures or evidence**, not proofs.
3. Exact characteristic-zero results are labelled `[PROVED-exact]` or `[CERTIFIED]`; modular results stay labelled mod-p; numerical hits require exact lifting and the HIT protocol.
4. Keep retractions in the record. They are part of the campaign’s results and prevent repeating silent-lie, gauge, and truncation errors.

## Archive layout on `main`

- `CLAUDE.md`, `AGENTS.md` — thin pointers so a fresh Claude Code or Codex session reads this README on its first turn, instead of guessing.
- `docs/BRANCH_AUDIT.md` — full per-branch audit: confirms nothing is lost, checks every branch against this README's claims.
- `docs/sessions/active/` — sessions 39–40 (current paths).
- `docs/sessions/archive/` — stale sessions 41–42, retained rather than deleted.
- `docs/history/` — sessions 1–18 status report.
- `archives/transfer/` — the campaign bundle, state-transfer archive, and restoration instructions.

Sessions 43–44 are not merged into `main` itself; their material lives on PR [#19](https://github.com/git-df-scott/jacobian_planar/pull/19) (Session 43) and PR [#20](https://github.com/git-df-scott/jacobian_planar/pull/20) (Session 44) — see [Open pull requests](#open-pull-requests). No files were deleted to create this organization; the moves preserve their contents.

## Reproduction entry points

On the canonical campaign branch, start with `MANIFEST.md` and `ARTIFACT_INDEX.md`, then use the certifiers named by `STATUS.md`. The large `.ms`, `.out`, `.gens`, and archive files are data products; do not infer a verdict from their presence alone.
