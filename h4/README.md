# h4/ — the H4 deg_y = 3 slice, msolve escalation continued

`w5_h4_escalate.py` is a copy of `wave2/w2_msolve_escalate.py` with two changes,
so the original file is untouched:

* the cell list is extended past the four Session-35 out-of-memory cells to the
  next rungs of the same ladder — (k, deg) = (4,7), (5,6), (6,5), (7,4);
* every cell is run at **two** compliant primes (65521 and 65539, both ≡ 1 mod 3)
  and the two verdicts are combined without averaging: EMPTY needs both,
  one-EMPTY-one-NONEMPTY is reported as DISAGREE.

Run as:

    W2_SCRATCH=/tmp/h4scr W2_MSTMO=1800 python3 h4/w5_h4_escalate.py

Its parser controls (a unit ideal must read EMPTY, a solvable system must read
NONEMPTY) and its cross-engine control (msolve must agree with Singular's EMPTY
on a cell Singular decided) are the originals' and are re-run each time.
