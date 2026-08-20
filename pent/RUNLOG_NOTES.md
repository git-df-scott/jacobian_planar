# Notes on pent/RUNLOG.tsv

Columns: `timestamp system generators levels gauges bytes threads exit seconds
peak_rss_kb out_bytes verdict head`.

* `peak_rss_kb` is the child's maximum resident set size from `/usr/bin/time -v`,
  so it is msolve's own peak, not the box's.
* `exit = -9` is SIGKILL, i.e. the kernel's out-of-memory killer; the verdict
  column records it as `OOM`. `out_bytes = 0` alongside a nonzero exit is a
  FAILURE and is written down as one — never read as a result.
* `gauges = 2` is the file as exported (p_00 = 0, p_10 = 1). `gauges = 3` adds
  the generator `p_1_0 - 1`, which fixes the coordinate-scale gauge
  (x,y) -> (lam x, lam^-3 y). Without it the variety contains a one-dimensional
  gauge orbit through every point and cannot be zero-dimensional, which is what
  msolve's solve mode needs; with it the system is rigid. The two are different
  problems, not two runs of one.

## Concurrency caveat, stated rather than hidden

The rows produced in this session were run while other solvers (the H2 Singular
sweep, the H4 msolve escalation, the pentagon slice search, the exact-Q
reconstruction) were resident on the same 15 GB box. An `OOM` row therefore
records "did not fit in the memory available at that moment", which is a weaker
statement than "does not fit in 15 GB". Any row that matters should be re-run on
a quiet box before it is quoted as a hard memory bound. The campaign's own
recorded L23 OOM (`wave1/L23_VERDICT.txt`, exit 137 at 13.9 GB peak, from
`heavy/RUNLOG.tsv` on the support-compute branch) was measured with the box to
itself and is the better number for that system.
