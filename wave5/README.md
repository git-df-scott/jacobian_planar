# Wave 5 — the B=16 door (GGV Pro Mathematica 27 (2013), Theorem 1.2)

Chain of custody for tonight's main hunt:
- GGHV 2022's discard of the gcd-16 degree pairs cites [4, Sec 3.5], which
  solved only deg(q1) = 2,3,4 and STALLED at deg(q1)=5 (2013 PC, one hour).
- GGV's refereed 2017 paper says Heitmann's B>16 is gapped: "B >= 16 remains
  ... the best lower limit"; "the possible counterexample at B=16 is still
  within reach".
- A solution of (1.2)+(1.3) with mu0 != 0 at ANY deg(q1) is constructively a
  counterexample to JC2 (GGV Thm 1.2 + their Sec 2 construction).

Files: w5_b16_abel.py (exact transcription + 6 controls, incl. the mu0-typo
finding in their Sec 3.1), w5_b16_export.py (msolve exports, mu0 saturated,
p = 1 mod 3), ms/ (systems + outputs + timings).

Ladder verdicts so far (mod p at 1000003/1000033/1000039):
  d=2 EMPTY (reproduces GGV)   d=3 EMPTY (reproduces GGV)
  d=4 EMPTY (reproduces GGV)   d=5 EMPTY at 3 primes, ~3.3s each  <- NEW, past the 2013 stall
  d=6 EMPTY over Q (char-0, 135s) + 3 primes.  d=5 EMPTY over Q (char-0, 22s).
  d=7 (3 primes) and d=8 (p=1000003): OOM at the 13.9 GB machine ceiling,
  0-byte outputs -- STALLED, not verdicts. Single-threaded retry OOMed identically (13.96 GB):
  the F4 matrix itself exceeds this machine. Next rung needs more RAM, full stop.

## Wave 5b (the RAM-wall hour)
- w5_b16_reduce.py: linear eliminations + quasi-homogeneity (VERIFIED
  computationally) + exhaustive gauge charts {mu2=1} u {mu2=0, mu3=1};
  regression: reduced d=5, d=6 EMPTY both charts (matches unreduced char-0).
  Reduced d=7: 28 eqs, 21/20 vars per chart (from 35 eqs/28 vars).
- w5_pent_grading.py: THE PENTAGON SYSTEM HAS A 2-DIMENSIONAL TORUS SYMMETRY
  in its exported form (integer grading ~ 3i-7j + one more): positive-
  dimensional orbits explain every Groebner OOM. ms2/pent_L18_g4.ms pins both
  scalings (charts p_1_0=1, p_1_1=1; vanishing charts still owed).
- reruns2/: every previously-unaudited certifier re-run, all exit 0 (W3-2..5,
  HIT gate, ledger linter, lift controls, parallel-session wave3 files).
- 20G swapfile enabled; unreduced d=7 re-running under swap in parallel.
