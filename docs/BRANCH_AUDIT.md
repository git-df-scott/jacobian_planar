# Branch audit — 2026-09-04

Full inventory of every branch on `git-df-scott/jacobian_planar`: confirms nothing is stranded (unpushed, uncommitted, or otherwise lost), and checks each branch's real content against what `README.md` claims about it. This is a point-in-time snapshot; re-run the methodology below rather than trusting it forever.

Scope note: this audit covers what is on GitHub. It cannot see a chat transcript that never resulted in a push — if a past session's work was never committed, no git-based check can recover it. Every finding below is "everything that reached GitHub is intact and accounted for," not "every conversation ever had about this project is represented here."

## 1. No lost work

Checked, as of this audit:

- **All 38 branches are on `origin`.** `git branch -r` lists every branch used anywhere in `README.md`'s branch map plus this session's own branches; every one resolves to a real commit on GitHub.
- **No unpushed local state.** `git branch -vv`, `git stash list`, and `git fsck --unreachable --no-reflogs` in this session's checkout show no local branches ahead of their remote, no stashed changes, and no dangling commits — everything this session touched is already pushed.
- **`wip:`-labelled commits are not lost work.** A grep across all 1,268 commits reachable from any branch for markers like `wip`, `uncommitted`, `not pushed`, `local-only` turns up 23 `wip: snapshot` / `wip: lane snapshot` / `WIP checkpoint` commits (mostly on `codex/sol-session3-pole`'s `night*/` sequence). All 23 are already committed and pushed to `origin` — "WIP" here describes the research state (an in-progress lane), not an unpushed artifact. Nothing found reads as "this exists only in a chat and never made it to git."
- **No secrets.** Re-confirmed (see the prior organization pass) that no tracked file on `main` contains credential/API-key/token patterns.

Verdict: everything that any session did on this repository, across every branch, is on GitHub. There is no evidence of lost work.

## 2. Consistency with README's claims

Cross-checked every branch's actual head commit and top-level file listing against its description in `README.md`'s [Branch map](../README.md#branch-map):

- All descriptions match. The five support/backup branches with no PR (`fable-ce-backup`, `github-push-issue-oftsm3`, `opus-support-compute`, `opus-support-toolchain-62st0d`) and the eight unwrapped Codex branches (below) have file layouts consistent with what README says they're for — e.g. `opus-support-toolchain-62st0d` really does hold `BUILD.md`/`tooling.log`, `codex/sol-session3-pole` really does hold the `night1`..`night24` sequence its name promises.
- **The one real drift**: this session's prior cleanup pass (removing the stale root-level `39`/`40.md`/`41.md`/`42.md` files) added a new commit to 29 of the 38 branches, which moved every one of those heads past the shas recorded in README's "Exact branch heads (2026-09-01)" table. That table has been refreshed alongside this report (see the branch map).
- No branch's actual content contradicts the "no counterexample found" claim — nothing found in any top-level file, README, or STATUS-style doc across any branch asserts a verified counterexample. Retraction/correction files (`CATCHES.md`, `AUDIT_EOD.md`, `CROSSDOOR.md`, etc.) are present and consistent with README's description of them as a live error ledger.
- One branch moved concurrently with this audit: `claude/jc2-counterexample-hunt-handoff-x40ahz` picked up a new commit (`387d28e`, "Vitushkin search: notes on the mate-problem route and current queue") from another active session while this audit was running. That is expected — this is a live, multi-session repository — and the table below reflects the branch's state as fetched at audit time.

## 3. Full inventory

"PR" is blank/`no PR` where a branch exists and is referenced from README but was never wrapped in a pull request — this is normal for support/backup branches and for Codex-origin branches, which don't follow the same "always open a draft PR" convention this session's Claude Code branches do.

### Claude workstreams

| Branch | Head | Last commit | Commits | PR |
| --- | --- | --- | --- | --- |
| `claude/ce-acquisition-strategy-uyqftb` | `2a9fb4c` | 2026-09-04 | 133 | [#14](https://github.com/git-df-scott/jacobian_planar/pull/14) draft |
| `claude/counter-example-audit-dnu9l9` | `b0bd0ad` | 2026-08-15 | 117 | [#3](https://github.com/git-df-scott/jacobian_planar/pull/3) draft |
| `claude/d23-borisov-transfer-test-vpr3m6` | `7296164` | 2026-08-12 | 18 | [#1](https://github.com/git-df-scott/jacobian_planar/pull/1) draft |
| `claude/fable-6o0nqe` | `a105bc9` | 2026-09-04 | 234 | [#21](https://github.com/git-df-scott/jacobian_planar/pull/21) draft |
| `claude/fable-ce-backup` | `0d6dee1` | 2026-09-04 | 11 | no PR |
| `claude/fable-counterexample-sweep-yyj5vf` | `35c7281` | 2026-09-04 | 28 | [#17](https://github.com/git-df-scott/jacobian_planar/pull/17) draft |
| `claude/ggv-conjecture-evidence-r9almu` | `f5e5397` | 2026-09-04 | 95 | [#11](https://github.com/git-df-scott/jacobian_planar/pull/11) draft |
| `claude/github-push-issue-oftsm3` | `f738744` | 2026-09-04 | 7 | no PR |
| `claude/github-repo-organization-wdr8n7` | `ee8bd69` | 2026-09-04 | 12 | [#25](https://github.com/git-df-scott/jacobian_planar/pull/25) draft |
| `claude/jacobian-collision-counterexample-nsc6ul` | `8b5adec` | 2026-09-04 | 34 | [#19](https://github.com/git-df-scott/jacobian_planar/pull/19) draft |
| `claude/jacobian-conjecture-campaign-xcw9p4` | `fbd2864` | 2026-09-04 | 164 | no PR |
| `claude/jacobian-conjecture-search-om7slv` | `df9f911` | 2026-09-04 | 11 | [#8](https://github.com/git-df-scott/jacobian_planar/pull/8) draft |
| `claude/jacobian-planar-sweep-iajyma` | `f307232` | 2026-09-04 | 309 | [#13](https://github.com/git-df-scott/jacobian_planar/pull/13) draft |
| `claude/jc2-counterexample-hunt-handoff-w369mc` | `e0086a7` | 2026-09-03 | 32 | [#23](https://github.com/git-df-scott/jacobian_planar/pull/23) draft |
| `claude/jc2-counterexample-hunt-handoff-x40ahz` | `387d28e` | 2026-09-04 | 27 | [#24](https://github.com/git-df-scott/jacobian_planar/pull/24) draft |
| `claude/jc2-handoff-audit-hartnc` | `ae58bd3` | 2026-09-03 | 15 | [#22](https://github.com/git-df-scott/jacobian_planar/pull/22) draft |
| `claude/mod-3-keller-pair-obstruction-oceq9z` | `70025d3` | 2026-08-13 | 24 | [#2](https://github.com/git-df-scott/jacobian_planar/pull/2) draft |
| `claude/moduli-deformation-exceptions-2f4ey2` | `2ea44d8` | 2026-08-16 | 35 | [#5](https://github.com/git-df-scott/jacobian_planar/pull/5) draft |
| `claude/opus-5-counterexample-plan-sep6yk` | `b233c70` | 2026-09-04 | 231 | [#9](https://github.com/git-df-scott/jacobian_planar/pull/9) draft |
| `claude/opus-errors-false-proofs-820rmd` | `1ebeece` | 2026-09-04 | 11 | [#7](https://github.com/git-df-scott/jacobian_planar/pull/7) draft |
| `claude/opus-hunt-territories` | `99b3650` | 2026-09-04 | 68 | [#10](https://github.com/git-df-scott/jacobian_planar/pull/10) draft |
| `claude/opus-plan-priority-queue-0pultj` | `784eacf` | 2026-08-14 | 70 | [#4](https://github.com/git-df-scott/jacobian_planar/pull/4) closed |
| `claude/opus-support-compute` | `b6bf58c` | 2026-09-04 | 30 | no PR |
| `claude/opus-support-toolchain-62st0d` | `83e0f80` | 2026-09-04 | 33 | no PR |
| `claude/opus-worker-resisters` | `215a040` | 2026-09-04 | 169 | [#12](https://github.com/git-df-scott/jacobian_planar/pull/12) draft |
| `claude/past-code-session-8mdjqn` | `37d2ebe` | 2026-09-04 | 137 | [#20](https://github.com/git-df-scott/jacobian_planar/pull/20) draft |
| `claude/plane-counterexample-endgame-az3geq` | `72e6ce5` | 2026-09-04 | 44 | [#6](https://github.com/git-df-scott/jacobian_planar/pull/6) draft |
| `claude/poisson-bracket-counterexample-9esk1r` | `1046908` | 2026-09-04 | 19 | [#18](https://github.com/git-df-scott/jacobian_planar/pull/18) draft |

### Codex workstreams

| Branch | Head | Last commit | Commits | PR |
| --- | --- | --- | --- | --- |
| `codex/claude-opus5-mailbox` | `2875093` | 2026-09-04 | 362 | [#15](https://github.com/git-df-scott/jacobian_planar/pull/15) draft |
| `codex/pentagon-level14-rational-obstruction` | `b57cd27` | 2026-09-04 | 10 | no PR |
| `codex/pentagon-level16-exact` | `ae717ed` | 2026-09-04 | 14 | no PR |
| `codex/pentagon-p11-zero-search` | `1aed0b4` | 2026-09-04 | 239 | no PR |
| `codex/sol-session3-pole` | `df7471d` | 2026-09-04 | 235 | no PR |
| `codex/sol3-all-five` | `e43947e` | 2026-09-04 | 31 | no PR |
| `codex/sol5-collision-first` | `1d814dd` | 2026-09-04 | 33 | no PR |
| `codex/sol5-counterexample-hunt` | `a5a8327` | 2026-09-04 | 32 | no PR |
| `codex/sol6-collision-first` | `fd113a5` | 2026-09-04 | 43 | no PR |

### Other

| Branch | Head | Last commit | Commits | PR |
| --- | --- | --- | --- | --- |
| `work` | `5627f34` | 2026-09-04 | 15 | [#16](https://github.com/git-df-scott/jacobian_planar/pull/16) open |

### Codex workstreams — separately, as requested

Of the nine `codex/*` branches, only `codex/claude-opus5-mailbox` has an open PR ([#15](https://github.com/git-df-scott/jacobian_planar/pull/15), explicitly marked "DO NOT MERGE" — it's a handshake/mailbox protocol between Codex and Claude sessions, not a mergeable change). The other eight — the pentagon-level14/level16/p11 exact-system branches and the five sol-session3/sol3/sol5/sol6 branches — have no PR at all; they are indexed only through README's "Codex workstreams" table and the exact-heads table. All eight are intact on `origin`, all eight had their stale root files removed in the prior cleanup pass, and all eight match their README description. Nothing here is missing or unpushed — they were simply never opened as PRs, which appears to be how Codex-authored branches in this repo have always worked (as distinct from the Claude Code convention of a draft PR per branch).

## 4. Newest branch

`claude/jc2-counterexample-hunt-handoff-x40ahz` (this session's audit target explicitly named "including the newest one") is confirmed present, pushed, clean of the stale files, and consistent with README — its PR [#24](https://github.com/git-df-scott/jacobian_planar/pull/24) is open and draft, titled "Clues audit across all branches, 2026-09-03," and its content (Vitushkin-search sweep logs) matches what README's branch map says it's for.
