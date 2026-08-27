# Lead 2 memo — what "B ≥ 17" actually means, and where the theory stops

**B** = minimal gcd(deg P, deg Q) over counterexamples (∞ if JC2 true).
Heitmann gives B ≥ 16 [cited as Thm 2.23 in Pro Mathematica 27]. What exists
at B=16 and stops there:

1. **The GGV Thm 8.10 normal form** (P = x³y + x²p₂ + xp₁ + p₀,
   Q = x²y + xq₁ + q₀, [P,Q] = x⁴y + µ₃x³ + ... + µ₀) is derived
   *specifically for a B=16 minimal counterexample*. The Abel-equation
   reduction and our direct/F-system ladders live downstream of it. No
   analogue exists in the literature for B=17.

2. **The shape enumeration is already B-agnostic.** The mechanized
   enumerator (`gghv_audit/ggv_algorithms.py`, 19/19 controls, 34/34
   row-for-row match with the published table, extended to max ≤ 300 in
   `all_cases_max_le_300.json`: 474 cases, 440 above 150) enumerates ALL
   possible-counterexample shapes regardless of gcd. The (72,108) pair has
   gcd 36, not 16 — B=16 is about the *minimal* pair, not these shapes.

**Consequence for strategy:** deriving a B=17 normal form means redoing GGV
§8's corner analysis from scratch — days of delicate work with high
transcription risk, for a case that only matters after B=16 is closed. The
efficient path to the same territory is: (a) close B=16 via the ladder +
a degree-uniform µ-rigidity argument (in progress, transcription-free), and
(b) attack the enumerated shapes directly through the trackD pipeline (in
progress tonight: 70 never-decided published-case targets). B≥17 as a
separate program is deferred with reasons, not abandoned.
