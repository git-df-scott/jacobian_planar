# TABLE_VERIFY — GGHV "Some algorithms related to the Jacobian Conjecture" (arXiv:1708.07936) §5/§6 vs campaign reproduction

Verified 2026-09-02. Sources:
- PDF: `wt/canon/papers/1708.07936.pdf` (29 pp, A4, LaTeX/dvips). Extracted with `pdftotext -layout`. **Text layer is clean — no page renders were needed.**
- JSON: `wt/canon/gghv_audit/all_cases_max_le_150.json` (34 records).
- Mailbox: `wt/mailbox/AGENT_MAILBOX.md` lines 3907–3985 (FABLE-006).
- Cross-check: `wt/canon/papers/2204.14178.pdf` (GGHV 2022, "…from 100 to 108").

**Headline: 34 printed rows, 34 JSON records, 34/34 matched. 0 MISSING, 0 EXTRA, 0 value discrepancies.**

## Page map

| Content | PDF page |
|---|---|
| §5 heading "Admissible complete chains with v11(A0) ≤ 35" + preamble (14 chains len 1, 2 chains len 2 → 17 families len 1, 7 families len 2) | 24 |
| §5 Table 1: families **F1–F17** (length 1); §5 Table 2: families **F18–F24** (length 2); start of the F18–F21 impossibility argument | 25 |
| §5 conclusion of F18–F21 argument; Remark 5.1 (F13, j=1 = Orevkov) | 26 |
| §6 heading "Possible counterexamples with max(deg(P), deg(Q)) ≤ 150"; **Table A** (13 family rows); **Table B** (9 rows, chain length 1) | 27 |
| **Table C** (11 rows, chain length 2); **Table D** (1 row, chain length 3); statement + proof of Proposition 6.1 | 28 |
| End of Prop 6.1 proof; references | 29 |

13 + 9 + 11 + 1 = **34**, matching the paper's own "the 34 possible counterexamples".

## Notation

JSON encodes a corner `(a ≀ l, b)` (printed as `a/l, b`) as `[a, l, b]`. A bare printed `(a,b)` is `[a, 1, b]`.
`A0` = first corner, `mid` = list of intermediate corners, `final` = last corner. Chain length = `len(mid) + 1`.

Confirmed invariant across all 34 records: **`deg_P = m · v11(A0)`, `deg_Q = n · v11(A0)`, `max = max(m,n) · (a0+b0)`.** No record violates it.

## §5 family definitions (p25) as reproduced

F1 (4,12)/(1,0)/(7≀4,3) k=1 m=2j+3 n=3j+4 · F2 (5,20)/(1,0)/(7≀5,2) k=1 m=j+2 n=2j+3 · F3 (5,20)/(1,0)/(8≀5,3) k=1 m=4j+3 n=3j+2 · F4 (5,20)/(1,0)/(8≀5,3) k=2 m=2j+3 n=12j+16 · F5 (5,20)/(1,0)/(9≀5,4) k=1 m=7j+9 n=4j+5 · F6 (5,20)/(1,0)/(9≀5,4) k=2 m=3j+4 n=8j+10 · F7 (6,15)/(1,0)/(7≀3,4) k=1 m=j+2 n=4j+7 · F8 (6,15)/(1,0)/(8≀3,5) k=1 m=2j+3 n=5j+7 · F9 (7,21)/(1,0)/(11≀7,2) k=1 m=j+2 n=2j+3 · F10 (7,21)/(1,0)/(13≀7,3) k=1 m=5j+7 n=3j+4 · F11 (7,21)/(1,0)/(13≀7,3) k=2 m=j+2 n=3j+5 · F12 (8,24)/(2,0)/(13≀4,5) k=1 m=2j+3 n=5j+7 · F13 (9,21)/(2,0)/(13≀3,7) k=1 m=j+2 n=7j+13 · F14 (9,24)/(1,0)/(7≀3,4) k=1 m=j+2 n=4j+7 · F15 (9,24)/(1,0)/(8≀3,5) k=1 m=2j+3 n=5j+7 · F16 (9,24)/(1,0)/(10≀3,7) k=1 m=4j+3 n=7j+5 · F17 (9,24)/(1,0)/(11≀3,8) k=1 m=5j+2 n=8j+3
F18 (6,18)→(6,15)→(7≀3,4) m=j+2 n=4j+7 · F19 (6,18)→(6,15)→(8≀3,5) m=2j+3 n=5j+7 · F20 (6,24)→(6,15)→(7≀3,4) m=j+2 n=4j+7 · F21 (6,24)→(6,15)→(8≀3,5) m=2j+3 n=5j+7 · F22 (8,24)→(14≀4,6)→(5≀4,2) m=j+2 n=2j+3 · F23 (8,24)→(14≀4,6)→(11≀4,4) m=j+2 n=4j+7 · F24 (8,24)→(14≀4,6)→(19≀8,3) m=2j+3 n=3j+4

**Independent check performed:** every `(m,n)` used in §6 Table A is realizable at an integer `j ≥ 0` in its stated family. All 13 resolve (j=0 for eleven rows, j=1 for F1(5,7), F2(3,5), F9(3,5)). No §6 row cites an `(m,n)` outside its family's parametrization.

## Row-for-row comparison (all 34)

`pMax` = printed max; `jMax` = JSON `max`. `J[i]` = 0-indexed JSON record.

| # | pg | Printed row | Expanded (A0, mid, final) | (m,n) | pMax | JSON | degP | degQ | jMax | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 27 | F1 (3,4) | [4,1,12] / — / [7,4,3] | (3,4) | 64 | J[00] | 48 | 64 | 64 | MATCH |
| 2 | 27 | F1 (5,7) | [4,1,12] / — / [7,4,3] | (5,7) | 112 | J[08] | 80 | 112 | 112 | MATCH |
| 3 | 27 | F2 (2,3) | [5,1,20] / — / [7,5,2] | (2,3) | 75 | J[01] | 50 | 75 | 75 | MATCH |
| 4 | 27 | **F2 (3,5)** | [5,1,20] / — / [7,5,2] | (3,5) | **125** | **J[10]** | **75** | **125** | **125** | **MATCH (boundary)** |
| 5 | 27 | F3 (3,2) | [5,1,20] / — / [8,5,3] | (3,2) | 75 | J[02] | 75 | 50 | 75 | MATCH |
| 6 | 27 | F7 (2,7) | [6,1,15] / — / [7,3,4] | (2,7) | 147 | J[28] | 42 | 147 | 147 | MATCH |
| 7 | 27 | F8 (3,7) | [6,1,15] / — / [8,3,5] | (3,7) | 147 | J[29] | 63 | 147 | 147 | MATCH |
| 8 | 27 | F9 (2,3) | [7,1,21] / — / [11,7,2] | (2,3) | 84 | J[03] | 56 | 84 | 84 | MATCH |
| 9 | 27 | F9 (3,5) | [7,1,21] / — / [11,7,2] | (3,5) | 140 | J[19] | 84 | 140 | 140 | MATCH |
| 10 | 27 | F11 (2,5) | [7,1,21] / — / [13,7,3] | (2,5) | 140 | J[20] | 56 | 140 | 140 | MATCH |
| 11 | 27 | F17 (2,3) | [9,1,24] / — / [11,3,8] | (2,3) | 99 | J[05] | 66 | 99 | 99 | MATCH |
| 12 | 27 | F22 (2,3)\* | [8,1,24] / [14,4,6] / [5,4,2] | (2,3) | 96 | J[04] | 64 | 96 | 96 | MATCH |
| 13 | 27 | F24 (3,4) | [8,1,24] / [14,4,6] / [19,8,3] | (3,4) | 128 | J[13] | 96 | 128 | 128 | MATCH |
| 14 | 27 | (7,35) (19/7,5) | [7,1,35] / — / [19,7,5] | (2,3) | 126 | J[11] | 84 | 126 | 126 | MATCH |
| 15 | 27 | (7,42) (13/7,6) | [7,1,42] / — / [13,7,6] | (3,2) | 147 | J[31] | 147 | 98 | 147 | MATCH |
| 16 | 27 | (7,42) (13/7,6) | [7,1,42] / — / [13,7,6] | (2,3) | 147 | J[30] | 98 | 147 | 147 | MATCH |
| 17 | 27 | **(8,28) (7/4,3)** | **[8,1,28] / — / [7,4,3]** | **(3,4)** | **144** | **J[21]** | **108** | **144** | **144** | **MATCH (corner 8,28)** |
| 18 | 27 | **(8,28) (11/4,7)** | **[8,1,28] / — / [11,4,7]** | **(3,2)** | **108** | **J[06]** | **108** | **72** | **108** | **MATCH (corner 8,28)** |
| 19 | 27 | (9,36) (17/9,4) | [9,1,36] / — / [17,9,4] | (3,2) | 135 | J[16] | 135 | 90 | 135 | MATCH |
| 20 | 27 | (9,36) (17/9,4) | [9,1,36] / — / [17,9,4] | (2,3) | 135 | J[17] | 90 | 135 | 135 | MATCH |
| 21 | 27 | (11,33) (19/4,8) | [11,1,33] / — / [19,4,8] | (2,3) | 132 | J[14] | 88 | 132 | 132 | MATCH |
| 22 | 27 | (12,33) (11/3,8) | [12,1,33] / — / [11,3,8] | (2,3) | 135 | J[18] | 90 | 135 | 135 | MATCH |
| 23 | 28 | (8,32) (8,28) (11/4,7) | [8,1,32] / [8,1,28] / [11,4,7] | (3,2) | 120 | J[09] | 120 | 80 | 120 | MATCH |
| 24 | 28 | (8,40) (8,28) (11/4,7) | [8,1,40] / [8,1,28] / [11,4,7] | (3,2) | 144 | J[22] | 144 | 96 | 144 | MATCH |
| 25 | 28 | (9,27) (9,24) (11/3,8) | [9,1,27] / [9,1,24] / [11,3,8] | (2,3) | 108 | J[07] | 72 | 108 | 108 | MATCH |
| 26 | 28 | (9,36) (9,24) (11/3,8) | [9,1,36] / [9,1,24] / [11,3,8] | (2,3) | 135 | J[15] | 90 | 135 | 135 | MATCH |
| 27 | 28 | (10,40) (16/5,6) (23/10,3) | [10,1,40] / [16,5,6] / [23,10,3] | (3,2) | 150 | J[32] | 150 | 100 | 150 | MATCH |
| 28 | 28 | (10,40) (18/5,8) (8/5,3) | [10,1,40] / [18,5,8] / [8,5,3] | (3,2) | 150 | J[33] | 150 | 100 | 150 | MATCH |
| 29 | 28 | (12,30) (16/3,10) (11/6,3) | [12,1,30] / [16,3,10] / [11,6,3] | (3,2) | 126 | J[12] | 126 | 84 | 126 | MATCH |
| 30 | 28 | (12,36) (12,33) (11/3,8) | [12,1,36] / [12,1,33] / [11,3,8] | (2,3) | 144 | J[27] | 96 | 144 | 144 | MATCH |
| 31 | 28 | (12,36) (9,24) (11/3,8) | [12,1,36] / [9,1,24] / [11,3,8] | (2,3) | 144 | J[24] | 96 | 144 | 144 | MATCH |
| 32 | 28 | (12,36) (21/4,9) (19/4,8) | [12,1,36] / [21,4,9] / [19,4,8] | (2,3) | 144 | J[25] | 96 | 144 | 144 | MATCH |
| 33 | 28 | (12,36) (21/4,9) (12/4,5) | [12,1,36] / [21,4,9] / [12,4,5] | (2,3) | 144 | J[23] | 96 | 144 | 144 | MATCH |
| 34 | 28 | (12,36) (12,30) (16/3,10) (11/6,3) | [12,1,36] / [12,1,30],[16,3,10] / [11,6,3] | (3,2) | 144 | J[26] | 144 | 96 | 144 | MATCH |

**MISSING_FROM_JSON: none. EXTRA_IN_JSON: none. Value discrepancies: none.**

## Spotlight items requested

### Corner A0 = [8,1,28] — exactly two records, both confirmed
- **J[06] = printed row 18**: `A0=[8,1,28]`, `mid=[]`, `final=[11,4,7]`, `(m,n)=(3,2)`, `(deg_P, deg_Q) = (108, 72)`, max 108. Printed as `(8,28) (11/4,7) (3,2) 108`.
- **J[21] = printed row 17**: `A0=[8,1,28]`, `mid=[]`, `final=[7,4,3]`, `(m,n)=(3,4)`, `(deg_P, deg_Q) = (108, 144)`, max 144. Printed as `(8,28) (7/4,3) (3,4) 144`.

Both match the task's stated expectation exactly. Note `deg_P = 108` in both because `deg_P = m·v11(A0) = 3·36`.

`[8,1,28]` also appears as a **mid** corner (not `A0`) in two further records: J[09] (`A0=[8,1,32]`, max 120) and J[22] (`A0=[8,1,40]`, max 144). Anyone saying "the (8,28) case" should say which of the four.

### Boundary case max = 125
**J[10] = printed row 4**: `A0=[5,1,20]`, `mid=[]`, `final=[7,5,2]`, `(m,n)=(3,5)`, `(deg_P, deg_Q) = (75, 125)`, `max = 125`. Family **F2 with j=1**. Confirmed as stated. Exactly one record has `max == 125`.

Distribution: **10 records with max < 125**, **1 record with max == 125**, **23 records with max > 125**.

### The 10 rows with max < 125 (the GGHV-2022 set)
J[00]–J[09], in ascending max:

| J | Printed as | A0 | (m,n) | (degP,degQ) | max |
|---|---|---|---|---|---|
| J[00] | F1 (3,4) | (4,12) | (3,4) | (48,64) | 64 |
| J[01] | F2 (2,3) | (5,20) | (2,3) | (50,75) | 75 |
| J[02] | F3 (3,2) | (5,20) | (3,2) | (75,50) | 75 |
| J[03] | F9 (2,3) | (7,21) | (2,3) | (56,84) | 84 |
| J[04] | F22 (2,3)\* | (8,24) | (2,3) | (64,96) | 96 |
| J[05] | F17 (2,3) | (9,24) | (2,3) | (66,99) | 99 |
| J[06] | (8,28)(11/4,7) len-1 | (8,28) | (3,2) | (108,72) | 108 |
| J[07] | (9,27)(9,24)(11/3,8) len-2 | (9,27) | (2,3) | (72,108) | 108 |
| J[08] | F1 (5,7) | (4,12) | (5,7) | (80,112) | 112 |
| J[09] | (8,32)(8,28)(11/4,7) len-2 | (8,32) | (3,2) | (120,80) | 120 |

**Cross-verified against arXiv:2204.14178 §2 (p2–3), which prints its own 10-row table.** It matches this set row-for-row on (A0, (m,n), max):
`(4,12)(3,4)64 · (4,12)(5,7)112 · (5,20)(2,3)75 · (5,20)(3,2)75 · (7,21)(2,3)84 · (8,24)(2,3)96 · (8,28)*(3,2)108 · (8,32)(3,2)120 · (9,24)(2,3)99 · (9,27)(2,3)108`.
Its own accounting — "the smallest members of the families F1, F2, F3, F9, F17, F22 … and three additional cases in the tables of section 6" — reproduces exactly: 7 family rows (F1 contributes two) + 3 non-family rows (J[06], J[07], J[09]) = 10.

**Critical:** GGHV 2022's Theorem 2.1 discards all ten **except** `(deg P, deg Q) ∈ {(72,108),(108,72)}` — and its table marks that row `(8,28) *(3,2)`. That survivor is **J[06]**, the campaign's own case. Note the paper's abstract says it discards all but "(72,108)"; two of the ten have that degree pair (J[06] and J[07]), and §1 says one of the two was discarded in §5 and the other "we couldn't solve … thus it is left open". The starred `(8,28)(3,2)` row is the one left open.

## What 1708.07936 itself discards vs merely enumerates

The paper **discards nothing above max = 100**, let alone above 125. Everything it removes sits inside the ten `< 125` rows.

1. **§5, p25–26 (proved):** families **F18, F19, F20, F21** "can not be obtained from a standard (m,n)-pair (P,Q) as in Theorem 2.20". These four families **never appear in the §6 34-case table at all**, so they subtract nothing from the 34.
2. **§6, p27 (attributed to prior work):** "In [6] (Moh) there are listed four cases (which correspond to six cases in our terminology) of possible counterexamples with max(deg(P),deg(Q)) ≤ 100. They are discarded by hand." The paper colours these six **red** in Table A. The six red rows are exactly the six rows with max ≤ 100: F1(3,4) 64, F2(2,3) 75, F3(3,2) 75, F9(2,3) 84, F22(2,3)\* 96, F17(2,3) 99.
3. **§6, p27:** "Five of them correspond to the six cases found by Moh, one of the cases of Moh was discarded by the algorithm because it featured (A0,A′0) = ((7,21),(2,1)), and (2,1) ∉ PLLC. The sixth red case, marked with a star, corresponds to F22. This case was probably discarded … by Heitmann (with no mention to it) by symmetry reasons… In Proposition 6.1 we show that we can discard it."
4. **Proposition 6.1, p28–29 (the paper's only original §6 discard):** "The example corresponding to **F22 with (m,n) = (2,3)** can not be obtained from a standard (m,n)-pair (P,Q) as in Theorem 2.20." That is **J[04], max = 96**.

So the paper's own §6 verb for everything else is *describe / list*: "Here we describe the shape of the 34 possible counterexamples with max(deg(P), deg(Q)) ≤ 150." Tables B, C, D are introduced purely as "There are 9 other possible pairs… / There are also 11 other possible pairs… / Finally there is another possible pair…". **No discard claim is made for any row with max ≥ 108.** The 34 count *includes* rows the paper then discards (e.g. F22(2,3)), so "34 open" would be wrong; "34 enumerated" is right.

## FABLE-006 reconciliation (AGENT_MAILBOX.md, lines 3907–3985)

**Verdict: reconciled. Every checkable numeric and structural claim in FABLE-006 is correct.**

| FABLE-006 claim | Verified against | Result |
|---|---|---|
| Verbatim: "34 possible counterexamples with max ≤ 150" | p27 §6 line 3 | CORRECT (paper writes `max(deg (P ), deg (Q)) ≤ 150`; Fable's `max{…}` braces are cosmetic) |
| "2204.14178 handled only those with max < 125 — its ten cases" | 2204.14178 abstract + §2 | CORRECT, and the `<` is strict in the source too |
| "34 − 24 = 10 and the ten < 125 entries match GGHV's table exactly" | JSON + 2204.14178 §2 table | CORRECT, row-for-row |
| Headline: "A0 = (8,28), A1 = (7/4,3), (m,n) = (3,4), max = 144" | printed row 17 / J[21] | CORRECT |
| "Six from the (m,n)-families: F2(3,5) 125, F7(2,7) 147, F8(3,7) 147, F9(3,5) 140, F11(2,5) 140, F24(3,4) 128" | Table A minus the 7 rows < 125 | CORRECT (13 − 7 = 6) |
| "Seven more with a complete chain of length 1: (7,35) 126, (7,42) twice 147, (9,36) twice 135, (11,33) 132, (12,33) 135" | Table B minus J[06] (108) and minus the headline row | CORRECT (9 − 1 − 1 = 7) |
| "the eight length-1 cases at ≥ 125" | Table B minus J[06] | CORRECT (9 − 1 = 8) |
| "Nine with chain length 2: (8,40) 144, (9,36) 135, (10,40) twice 150, (12,30) 126, (12,36) four times 144" | Table C minus J[09] (120) and J[07] (108) | CORRECT (11 − 2 = 9) |
| "One with chain length 3: (12,36) at 144" | Table D / J[26] | CORRECT |
| Total of the untouched set = 24 | 6 + 7 + 9 + 1 + 1 headline | CORRECT |
| Caveat: "The 13 family cases are given as family + (m,n), not explicit corners; §5 must be read first" | p27 Table A | CORRECT and important — this reproduction had to expand them |
| Caveat: "'open' means *not discarded*, not likely" | §6 wording | CORRECT |

**FABLE-006 imprecisions worth flagging (none change a number):**

- **F-a (boundary fragility).** "max < 125" must be read strictly. F2(3,5) sits at exactly 125 and is on the *untouched* side. Read as "≤ 125" the split becomes 11/23 and the whole 24/10 arithmetic breaks. The strict reading is the correct one — 2204.14178's own abstract and Theorem 2.1 use `< 125` and `≥ 125` — but the memo never says "strictly".
- **F-b (the campaign's own case is one of the ten, not outside them).** FABLE-006 says "we have spent weeks on (8,28) with (3,2)". That case is **J[06], max 108**, which is inside the ten that 2204.14178 addressed — it is precisely the single case that paper could **not** discard (starred `(8,28) *(3,2)`, `(deg P, deg Q) = (108,72)`). So the memo's framing "1 of 25 open cases" is exactly right and its arithmetic is right, but a reader could mistakenly infer from "the ten < 125 [are] handled" that (8,28)(3,2) is closed. It is not: it is the one survivor, and discarding it is what raises the bound 108 → 125.
- **F-c (ambiguous corner reference).** "(8,28)" alone is ambiguous across four records: J[06] (A0, len-1, (3,2), 108), J[21] (A0, len-1, (3,4), 144), J[09] (mid, A0=(8,32), 120), J[22] (mid, A0=(8,40), 144). Only J[21] is Fable's headline target.
- **F-d (unverifiable here).** The artifact `FABLE_24_OPEN_CASES.md` and `fable_xcol/alg_paper_text.txt` on branch `claude/fable-counterexample-sweep-yyj5vf` are not present in these worktrees; not checked.
- **F-e.** Fable's ask — "verify these tables against the published PDF directly before anyone spends solver time" — is now discharged for the enumeration itself. The PDF text layer is clean and the reproduction is exact.

## Other observations / minor anomalies (not discrepancies)

- **O-1.** Printed Table C row 33 reads `(12,36) (21/4,9) (12/4,5)` — the corner `12/4` is not in lowest terms (= 3/1). The JSON faithfully stores `[12,4,5]`. In GGV's `(a ≀ l, b)` notation `l` is the level of the Laurent extension `L^(l)`, not merely a denominator, so an unreduced-looking `12 ≀ 4` may be intended; either way the reproduction copies the paper verbatim, so this is a question about the *paper*, not the JSON.
- **O-2.** §5's preamble (p24) says 14 admissible complete chains of length 1 and 2 of length 2, yielding **17** families of length 1 and **7** of length 2 = 24 families (F1–F24). Confirmed: p25 prints exactly 17 + 7 rows.
- **O-3.** Only 10 of the 24 families (F1, F2, F3, F7, F8, F9, F11, F17, F22, F24) contribute to §6 Table A. F4–F6, F10, F12–F16, F18–F21, F23 contribute nothing at ≤ 150 — for F18–F21 because they were proved impossible in §5; for the rest, presumably because their smallest member already exceeds 150 (not re-derived here).
- **O-4.** Both papers list only cases satisfying equality (3.17); the (3.18) cases are obtained by swapping m with n. So the 34 is a count of `(m,n)`-ordered representatives, not of unordered degree pairs.
- **O-5.** Remark 5.1 (p26): "The possible counterexample in F13 with j = 1 was analyzed extensively by Orevkov in [7]". F13 with j=1 is (m,n) = (3,20) at A0 = (9,21), v11 = 30 → max = 600, far above 150, hence absent from the 34.

## Files written
- `groundcover/TABLE_VERIFY.md` (this file)
- `groundcover/1708_layout.txt` — full `pdftotext -layout` of 1708.07936
- `groundcover/sec56.txt` — pages 24–29 only
- `groundcover/2204_layout.txt` — full `pdftotext -layout` of 2204.14178
- `groundcover/compare_raw.txt` — raw output of the matching script
