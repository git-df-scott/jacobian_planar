# jacobian_planar

This repository is a research archive for the plane Jacobian-conjecture campaign. It contains exact algebra, computational experiments, audits, retractions, and handoff material. **No counterexample has been found.** The repository is deliberately conservative: a timeout is not an EMPTY result, a modular result is not a characteristic-zero proof, and a numerical miss is not evidence of emptiness.

## Start here

1. **Current campaign state:** [`STATUS.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/STATUS.md)
2. **Complete re-walk and open queue:** [`STATE_FULL.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/STATE_FULL.md), [`OPEN_ITEMS.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/OPEN_ITEMS.md)
3. **What is closed, live, or retired:** [`LIVE_MAP.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/LIVE_MAP.md), [`TRUST_MAP.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/TRUST_MAP.md)
4. **Corrections and failed-proof ledger:** [`CATCHES.md`](https://github.com/git-df-scott/jacobian_planar/blob/claude/opus-5-counterexample-plan-sep6yk/CATCHES.md)
5. **Fleet plan for the next counterexample hunt:** [`docs/plans/CE_HUNT_PLAN.md`](docs/plans/CE_HUNT_PLAN.md) (audit gates, ordered leads, fleet design, two-week schedule; reader reports, planner outputs and adversarial reviews in [`docs/plans/appendix/`](docs/plans/appendix/))
6. **Session narrative:** [`docs/history/sessions-01-18-status.md`](docs/history/sessions-01-18-status.md), [`docs/sessions/active/`](docs/sessions/active/), [`docs/sessions/archive/`](docs/sessions/archive/)

The full scripts, certifiers, logs, and generated data are on the campaign branch. The `main` branch is the lightweight map and archive index.

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
| [`claude/opus-5-counterexample-plan-sep6yk`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-5-counterexample-plan-sep6yk) | **Canonical full campaign state**: `STATUS.md`, `STATE_FULL.md`, `LIVE_MAP.md`, `OPEN_ITEMS.md`, `CATCHES.md`, `wave0/`, `wave1/`, `wave5/`, `wave6/`, and all certifiers. Head `24a06fc` (prime-sweep continuation). |
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

`ce-acquisition-strategy`, `counter-example-audit`, `d23-borisov-transfer-test`, `fable-counterexample-sweep`, `ggv-conjecture-evidence`, `github-push-issue`, `jacobian-collision-counterexample`, `jacobian-conjecture-campaign`, `jacobian-conjecture-search`, `jacobian-planar-sweep`, `mod-3-keller-pair-obstruction`, `moduli-deformation-exceptions`, `past-code-session`, `poisson-bracket-counterexample`.

Use the canonical campaign branch for the latest verdict; use these branches only when tracing the named subproblem or its provenance.

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

### Exact branch heads (2026-09-01)

This compact ref list is the handoff index. The short commit ID makes it possible to verify that an agent opened the intended snapshot without scanning unrelated history.

| Family | Branch | Head |
| --- | --- | --- |
| Main | [`main`](https://github.com/git-df-scott/jacobian_planar/tree/main) | `74bbe4e` |
| Other | [`work`](https://github.com/git-df-scott/jacobian_planar/tree/work) | `cc04dad` |
| Claude | [`claude/opus-5-counterexample-plan-sep6yk`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-5-counterexample-plan-sep6yk) | `24a06fc` |
| Claude | [`claude/plane-counterexample-endgame-az3geq`](https://github.com/git-df-scott/jacobian_planar/tree/claude/plane-counterexample-endgame-az3geq) | `658960a` |
| Claude | [`claude/fable-ce-backup`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-ce-backup) | `c630696` |
| Claude | [`claude/opus-errors-false-proofs-820rmd`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-errors-false-proofs-820rmd) | `55417d0` |
| Claude | [`claude/opus-hunt-territories`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-hunt-territories) | `26d610d` |
| Claude | [`claude/opus-plan-priority-queue-0pultj`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-plan-priority-queue-0pultj) | `784eacf` |
| Claude | [`claude/opus-support-compute`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-compute) | `6ed1d53` |
| Claude | [`claude/opus-support-toolchain-62st0d`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-support-toolchain-62st0d) | `1978a0c` |
| Claude | [`claude/opus-worker-resisters`](https://github.com/git-df-scott/jacobian_planar/tree/claude/opus-worker-resisters) | `5e51b09` |
| Claude | [`claude/ce-acquisition-strategy-uyqftb`](https://github.com/git-df-scott/jacobian_planar/tree/claude/ce-acquisition-strategy-uyqftb) | `873021b` |
| Claude | [`claude/counter-example-audit-dnu9l9`](https://github.com/git-df-scott/jacobian_planar/tree/claude/counter-example-audit-dnu9l9) | `b0bd0ad` |
| Claude | [`claude/d23-borisov-transfer-test-vpr3m6`](https://github.com/git-df-scott/jacobian_planar/tree/claude/d23-borisov-transfer-test-vpr3m6) | `7296164` |
| Claude | [`claude/fable-6o0nqe`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-6o0nqe) | `b6648e4` |
| Claude | [`claude/fable-counterexample-sweep-yyj5vf`](https://github.com/git-df-scott/jacobian_planar/tree/claude/fable-counterexample-sweep-yyj5vf) | `e9a65be` |
| Claude | [`claude/ggv-conjecture-evidence-r9almu`](https://github.com/git-df-scott/jacobian_planar/tree/claude/ggv-conjecture-evidence-r9almu) | `66899d1` |
| Claude | [`claude/github-push-issue-oftsm3`](https://github.com/git-df-scott/jacobian_planar/tree/claude/github-push-issue-oftsm3) | `c72e7e4` |
| Claude | [`claude/jacobian-collision-counterexample-nsc6ul`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-collision-counterexample-nsc6ul) | `2f97e2f` |
| Claude | [`claude/jacobian-conjecture-campaign-xcw9p4`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-conjecture-campaign-xcw9p4) | `66341b0` |
| Claude | [`claude/jacobian-conjecture-search-om7slv`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-conjecture-search-om7slv) | `2c4b511` |
| Claude | [`claude/jacobian-planar-sweep-iajyma`](https://github.com/git-df-scott/jacobian_planar/tree/claude/jacobian-planar-sweep-iajyma) | `e4d1de3` |
| Claude | [`claude/mod-3-keller-pair-obstruction-oceq9z`](https://github.com/git-df-scott/jacobian_planar/tree/claude/mod-3-keller-pair-obstruction-oceq9z) | `70025d3` |
| Claude | [`claude/moduli-deformation-exceptions-2f4ey2`](https://github.com/git-df-scott/jacobian_planar/tree/claude/moduli-deformation-exceptions-2f4ey2) | `2ea44d8` |
| Claude | [`claude/past-code-session-8mdjqn`](https://github.com/git-df-scott/jacobian_planar/tree/claude/past-code-session-8mdjqn) | `a301e16` |
| Claude | [`claude/poisson-bracket-counterexample-9esk1r`](https://github.com/git-df-scott/jacobian_planar/tree/claude/poisson-bracket-counterexample-9esk1r) | `b08ad5a` |
| Codex | [`codex/claude-opus5-mailbox`](https://github.com/git-df-scott/jacobian_planar/tree/codex/claude-opus5-mailbox) | `156ba7a` |
| Codex | [`codex/pentagon-level14-rational-obstruction`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-level14-rational-obstruction) | `338eca4` |
| Codex | [`codex/pentagon-level16-exact`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-level16-exact) | `1e3ac1f` |
| Codex | [`codex/pentagon-p11-zero-search`](https://github.com/git-df-scott/jacobian_planar/tree/codex/pentagon-p11-zero-search) | `e4fa5ce` |
| Codex | [`codex/sol-session3-pole`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol-session3-pole) | `7095528` |
| Codex | [`codex/sol3-all-five`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol3-all-five) | `55a962c` |
| Codex | [`codex/sol5-collision-first`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol5-collision-first) | `2fe8ab2` |
| Codex | [`codex/sol5-counterexample-hunt`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol5-counterexample-hunt) | `e26ec86` |
| Codex | [`codex/sol6-collision-first`](https://github.com/git-df-scott/jacobian_planar/tree/codex/sol6-collision-first) | `4fbdccb` |

## Evidence rules

1. Read the verdict file and its stderr/log before trusting an output file.
2. `[-1]` after a parser error, an empty output after timeout/OOM, and an unverified modular contradiction are **failures or evidence**, not proofs.
3. Exact characteristic-zero results are labelled `[PROVED-exact]` or `[CERTIFIED]`; modular results stay labelled mod-p; numerical hits require exact lifting and the HIT protocol.
4. Keep retractions in the record. They are part of the campaign’s results and prevent repeating silent-lie, gauge, and truncation errors.

## Archive layout on `main`

- `docs/sessions/active/` — sessions 39–40 (current paths).
- `docs/sessions/archive/` — stale sessions 41–42, retained rather than deleted.
- `docs/history/` — sessions 1–18 status report.
- `archives/transfer/` — the campaign bundle, state-transfer archive, and restoration instructions.

Sessions 43–44 are not present in the repository. No files were deleted to create this organization; the moves preserve their contents.

## Reproduction entry points

On the canonical campaign branch, start with `MANIFEST.md` and `ARTIFACT_INDEX.md`, then use the certifiers named by `STATUS.md`. The large `.ms`, `.out`, `.gens`, and archive files are data products; do not infer a verdict from their presence alone.
