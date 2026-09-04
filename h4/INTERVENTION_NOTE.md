# Intervention note for h4/h4_escalate.log

At 03:37 UTC the cell `k=5 h=t deg<=4` at p = 65539 was **killed by hand** to
free 8.9 GB while several solvers shared the same 15 GB box. The log therefore
records `UNKNOWN 672.8s` for that prime, and the combined line reads
`k=5 deg<=4: OOM {65521: 'OOM', 65539: 'UNKNOWN'}`.

`UNKNOWN` there means *this session terminated the run*, not that msolve failed
or that the cell is undecidable. The p = 65521 run of the same cell reached a
genuine kernel OOM (373.9 s) on its own, and that is the number to quote. The
p = 65539 run should be repeated on a quiet box before anything is said about it.

Every other row in that log ended on its own.
