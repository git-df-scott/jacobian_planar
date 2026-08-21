# jacobian_planar

Computational campaign on the **two-dimensional Jacobian Conjecture** — the case
left open after the conjecture fell in dimension ≥ 3 in July 2026.

## → Read [`STATUS.md`](STATUS.md)

`STATUS.md` is the single source of truth: every result, every verdict with its
proof standard, every correction, every open item, and an index of all
certifiers and data.

**Current bottom line:** no counterexample found; no non-EMPTY verdict on any
real system; nothing promoted from mod-p to ℚ. The one degree pair below 125 not
eliminated in the literature, **(72,108)**, remains undecided.

## Layout

| path | contents |
|---|---|
| `STATUS.md` | **start here** — the consolidated log |
| `MANIFEST.md` | claim → certifier → verdict ledger |
| `wave0/`, `wave1/` | certifiers and data from the Plan 43 session |
| `campaign/` | the inherited campaign, five PR branches consolidated |

Every certifier is runnable and self-documenting: it prints `PASS`/`FAIL` per
claim, each labelled with its proof standard (`PROVED-exact`, `CERTIFIED`,
`LIT-READ`, `CONDITIONAL`, `UNCHECKED`).

## Parallel adjudication
A second (Opus) session independently adjudicated the three reports on this branch name; its ledger is preserved verbatim at wave3/ADJUDICATION_PARALLEL_OPUS.md. Its claims are NOT yet verified by the auditor; see the note at the end of ADJUDICATION.md.
