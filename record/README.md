# JC2 complete-record archive

Start with [JC2_COMPLETE_RECORD.md](../JC2_COMPLETE_RECORD.md). This directory
is the exhaustive source index accompanying that readable campaign history.
The frozen cutoff precedes the closing record commit on 2026-09-04.

| Record | Coverage |
|---|---|
| [BRANCHES.md](BRANCHES.md) / [BRANCHES.json](BRANCHES.json) | All 44 remote branches, exact heads, counts and numeric branch IDs |
| [CHRONOLOGY.md](CHRONOLOGY.md) / [COMMITS.jsonl](COMMITS.jsonl) | All 1,287 commits reachable from those heads, plus the two recovered local commits; full messages, parents, tree IDs and changed paths in JSONL |
| [REPORT_INDEX.md](REPORT_INDEX.md) / [REPORTS.jsonl](REPORTS.jsonl) | All 581 distinct report path/blob versions at those branch heads, with pinned source links |
| [FILES.jsonl](FILES.jsonl) | All 35,078 branch/file occurrences, deduplicated into 10,062 path/blob records across 9,952 paths |
| [PULL_REQUESTS.md](PULL_REQUESTS.md) | All 26 original PR descriptions and four retrieved discussion entries |
| [SNAPSHOT.json](SNAPSHOT.json) / [PR_DISCUSSIONS.json](PR_DISCUSSIONS.json) | Frozen GitHub metadata underlying the archive; no tags existed at the cutoff |
| [RECOVERY.json](RECOVERY.json) | Original SHAs and checksums for the 12 recovered night25/night26 files |
| [RECOVERED_NIGHTS_25_26.patch](RECOVERED_NIGHTS_25_26.patch) | Both recovered commits as an original Git mail patch, retaining author and message provenance |
| [RECOVERED_NIGHTS_25_26.bundle](RECOVERED_NIGHTS_25_26.bundle) | The two original commit objects and their new trees/blobs; prerequisite commit is recorded in RECOVERY.json |
| [INVENTORY_VERIFICATION.json](INVENTORY_VERIFICATION.json) | Object-integrity checks, complete coverage counts and SHA-256 checksums |
| [build_record.py](build_record.py) | Rebuild the inventory from the frozen inputs and Git objects |

The original campaign files remain on their pinned branches. They are not
silently merged into a single mathematical state. The record branch contains
all three Astra runs and additionally restores the previously unpublished
night25/night26 files at their original relative paths. Their old conclusions
remain unchanged in the source copies; see
[RECORD_CORRECTIONS.md](../RECORD_CORRECTIONS.md), especially the new night26
pure-power obstruction.

Original recovered source whitespace and Git mail-patch signature separators
are preserved byte-for-byte. The closing documents and generated indexes
are checked separately from those original-source whitespace differences.

`FILES.jsonl` has one JSON object per distinct `(path, sha, mode, type)`.
Its `branch_ids` list indexes `BRANCHES.json`. For an entry and a listed branch,
the original is available at
`https://github.com/git-df-scott/jacobian_planar/blob/<branch-sha>/<path>`.
Git object IDs identify exact bytes. `COMMITS.jsonl` also indexes deleted and
superseded history through each commit's tree and changed paths; the file
catalog itself describes the frozen branch heads, not every historical tree.

## What “complete” means here

The inventory is exhaustive for the fetched repository refs at the stated
cutoff, all PRs then visible, and the two additional local commits found during
this closeout. It is a complete repository-backed record, not a reconstruction
of every private chat, every lost inline executable, or uncommitted work in
unavailable environments. Git author names are not reliable model labels;
the narrative uses branch and report provenance to distinguish Claude,
earlier Codex/Sol work, and the three Astra runs. Historical solver claims
were not all rerun during this archival task.

## Rebuild

In a clone with all remote branches fetched, restore the original local
commits if needed:

```bash
git fetch origin
git fetch record/RECOVERED_NIGHTS_25_26.bundle refs/archive/recovered-night26:refs/heads/recovered-night26
python record/build_record.py
```

The published `COUNTS.json` is fixed to the pre-closeout snapshot. Subsequent
commits do not alter that snapshot. Restore a missing pinned branch SHA before
rebuilding; do not substitute a newer branch tip.
