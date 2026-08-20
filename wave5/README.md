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
  d=6+ running; char-0 d=5 running.
