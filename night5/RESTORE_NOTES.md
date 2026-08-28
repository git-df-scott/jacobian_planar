# night5 RESTORE_NOTES — campaign archive restore (TASK A)

Executor record. What was verified, what was found, what was not.

## Bundle verification

| step | result |
|---|---|
| md5 of `campaign_55commits.bundle` | `2fabb2392c0143f42fef7d0ff0efaa0e` |
| expected md5 | `2fabb2392c0143f42fef7d0ff0efaa0e` |
| **match** | **YES** — task A proceeded |

`git bundle verify campaign_55commits.bundle`:

```
campaign_55commits.bundle is okay
The bundle contains this ref:
894333cb15e9bb7b2eae954a8834b175838ccff5 HEAD
The bundle requires this ref:
82a683523aefb4f7d4706f2add422a9f25e77d82
The bundle uses this hash algorithm: sha1
```

Exit status 0. The required prerequisite `82a6835` is present in this repo
(`git cat-file -t` returns `commit`), which is why verification succeeded.

Fetched to a **local ref only**:

```
git fetch campaign_55commits.bundle HEAD:refs/heads/campaign-archive
 * [new ref]         HEAD       -> campaign-archive
```

`campaign-archive` contains 140 commits, tip `894333c "watch: enforcer ticks"`.
It was **not** pushed anywhere. The working branch stayed `claude/fable-6o0nqe`
throughout.

## Finding: the bundle does not contain session44

**The requested session-44 material is not in `campaign_55commits.bundle` at all.**
Checked two independent ways:

1. Walking all 140 commits of `campaign-archive` and testing `git cat-file -e
   <commit>:session44` — no commit has a `session44` tree entry.
2. `git log campaign-archive --name-only --diff-filter=A` over the full history,
   filtered for paths beginning `session44/` — **0 paths**. No `session4*` path of
   any kind appears.

The top-level directories that ever exist anywhere in the bundle's history are:
`campaign`, `certifiers`, `gao`, `gghv_audit`, `h2`, `h4`, `jacobian`, `lift`,
`logs`, `papers`, `pent`, `reruns2`, `samesign`, `symslice`, `wave0`–`wave6`,
`audit_parallel`, `audit_queue`, plus loose top-level files. There is no
`session43`, `session44`, or `lead4` anywhere in it.

The handoff's expectation that the session-44 core is reachable from the bundle
does not match the bundle's contents.

## Where the files actually are

The named files exist in this repository on a **different, pre-existing ref**:

| item | value |
|---|---|
| ref | `refs/remotes/origin/claude/past-code-session-8mdjqn` |
| tip commit | `a301e16606ffba8c074a337135322d9895d3dd26` |
| tip date / subject | 2026-08-28 02:26:49 +0000 — "The obstruction has a short, explicit certificate" |

This ref was already present in the local repository before this task; it did not
come from the bundle.

**Recorded deviation.** The instruction was to copy from `campaign-archive`. That
is not possible, because the files are not there. Rather than return nothing, the
restore was taken from the ref above, which is the only place in this repository
where the named artifacts exist. This is a read-only use of an existing local ref;
nothing was pushed to it or to any branch other than `claude/fable-6o0nqe`. Every
restored file's provenance is `a301e16`, **not** the bundle. Flagging this rather
than presenting bundle-sourced provenance that would be false.

One further caution for whoever reads the restored code: an earlier commit on that
same ref, `2b1eb22`, is the last commit that *touched* `lead4/cascade.py`, and its
tree holds a much smaller subset (5 `uz_*.py`, 10 `case1_*.py`, no `verify/`
directory at all). The restore below is from the **tip**, which has the complete
set.

## What was restored

Into `night5/campaign_restore/`. Every requested item was found at `a301e16`;
nothing on the request list was missing there.

| requested | found | restored to | count |
|---|---|---|---|
| `session44/lead4/cascade.py` | yes | `campaign_restore/lead4/` | 1 |
| `session44/lead4/uz_*.py` | yes | `campaign_restore/lead4/` | 13 |
| `session44/lead4/case1_*.py` | yes | `campaign_restore/lead4/` | 21 |
| `session44/lead4/face_eq.py` | yes | `campaign_restore/lead4/` | 1 |
| `session44/lead4/dk_eliminate.py` | yes | `campaign_restore/lead4/` | 1 |
| `session44/verify/` | yes | `campaign_restore/verify/` | 90 |
| `session44/*.md` (status/finding) | yes | `campaign_restore/session44_md/` | 26 |

Total 153 files restored, about 1.1 MB.

The 13 `uz_*.py`: `uz_cascade`, `uz_cascade_run`, `uz_eliminate`, `uz_export`,
`uz_ext`, `uz_ext_branch`, `uz_ext_run`, `uz_final`, `uz_final_sing`, `uz_lowq`,
`uz_qsolve`, `uz_system`, `uz_tests`.

The 21 `case1_*.py`: `allcovers`, `cascade`, `descend`, `envcheck`, `face_derive`,
`hurwitz`, `ladder`, `minlevel`, `msolve`, `nondeg`, `obstruction`, `orbits`,
`point`, `points`, `ranks`, `rational`, `reduce`, `symmetry`, `validate`,
`verdict`, `vertexpolys`.

The 26 `session44/*.md`: `B16_ABEL_LADDER`, `B17_MEMO`, `CANDIDATE_MAP`,
`CASCADE_STATUS`, `EDGE_GAP_FINDING`, `ESSENTIAL_FACE`, `FACE_STRUCTURE_CENSUS`,
`JELONEK_ASSESS`, `LEAD_C_PARAM`, `LEWEBER_SIEVE`, `LITERATURE_CHECK`,
`LIT_BATCH3`, `LIT_MONDELLO_AUG2026`, `MCKAY_WANG_CERTIFICATE`, `MULTIFACE`,
`NORMALIZATION_108`, `OPERATION_108`, `PREDICTION_AND_SUBCASE1`, `RETRACTION`,
`SOL_TASKS`, `SOURCE_GGHV2204`, `STRATEGY_RIGID`, `SWEEP_FRAMEWORKS`,
`U0_VERDICT`, `UNCOVERED_TIER`, `WGRADE_FINDING`.

### Items copied beyond the literal request

- `session44/lead4/CASE1_ESSENTIAL_FACE.md` — a finding document living inside
  `lead4/`. The request named `case1_*.py`, so this `.md` is outside the literal
  glob; copied because it is part of the same lead-4 finding set, and listed here
  so the addition is visible rather than silent.

### Items deliberately dropped

- `session44/verify/__pycache__/` — compiled Python bytecode, no source value.
  This is why the `verify/` count is 90 rather than the 91 blobs at `a301e16`.

### A trap worth recording

`session44/verify/.gitignore` was itself restored, and its patterns
(`own_sw_*.sing`, `sw_*.sing`, `_mp.sing`, `probe.sing`) match **16 files that are
tracked in the source ref**. Git ignores such patterns only for untracked files, so
those 16 were committed upstream but would have been silently skipped by a plain
`git add` here, making the restore quietly incomplete. They were force-added
(`git add -f`) so the restore matches the source. The 16: `probe.sing`,
`sw_7523.sing`, `sw_8053.sing`, `sw_11827.sing`, `own_sw_ctrl_7523.sing`,
`own_sw_ctrl_8053.sing`, and `own_sw_main_{7523,8053}_{0,1,2,3,4}.sing`.

## Integrity check

Every restored file was compared byte-for-byte against `git show a301e16:<path>`;
see the verification run recorded at commit time. No file was edited, reformatted,
or reconstructed — all content is verbatim from the source ref.
