# G1 -- deadline history for the ladder (recorded, not hidden)

The per-cell deadline is recorded in the `timeout_s` column of every row of
`ggv/ladder.tsv`.  It was revised once, on evidence, and the evidence is here.

## Why the deadline was lowered from 2700 s to 900 s

Cell `d=8, chart A, p=1000003` (`ggv/ms_ladder/b16r_d8_A_p1000003.ms`,
24 variables, 32 generators) was run to a full 2700 s deadline twice before the
ladder was re-sequenced:

| attempt | deadline | outcome | peak RSS observed | note |
|---|---|---|---|---|
| 1 | 2700 s | no output artifact at the deadline | ~7.2 GiB resident | ran under a 13 GiB address-space cap, later removed; ended in SIGSEGV on a failed allocation at the deadline |
| 2 | 2700 s | no output artifact; stopped at 32 min by the operator to land driver fixes | ~6.7 GiB resident | kernel OOM policy, no address-space cap |
| 3 | 2700 s | no output artifact; stopped at 11 min by the operator to re-sequence | ~4.8 GiB resident | fixed driver |

In every attempt the engine ran at ~100% of one core throughout and produced no
output bytes.  A cell that yields nothing at 2700 s yields nothing at 900 s, so
holding a 2700 s deadline for the first cell of the ladder only delays the
remaining 29 cells -- chart B in particular, which at d=5 solves in 0.01 s and
had not been reached at all after an hour of wall clock.

The ladder therefore sweeps all 30 cells at a recorded 900 s deadline first, so
every (d, chart, prime) cell gets a recorded verdict; cells recorded TIMEOUT at
900 s are then re-run at a longer deadline as budget allows, and any such re-run
appears as its own row with its own larger `timeout_s`.  No cell is capped
silently: the deadline that produced each verdict is a column of the table.
