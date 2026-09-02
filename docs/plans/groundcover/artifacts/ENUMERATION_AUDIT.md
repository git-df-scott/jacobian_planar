# ENUMERATION_AUDIT — ground cover on the GGHV/[5] degree-pair enumeration

Independent re-run and instrumentation of the campaign's own re-implementation
`gghv_audit/ggv_algorithms.py` ([5] = arXiv:1708.07936 Algorithms 1–9, the
enumeration GGHV arXiv:2204.14178 Theorem 2.1 imports its ten-case table from).
Worktree read-only; everything below ran from a copy in `groundcover/run/`.
Pure Python 3.11, no solvers.

## 1. What was run (exact commands)

```
WT=.../scratchpad/wt/canon ; OUT=.../scratchpad/groundcover
cp -r $WT/gghv_audit $OUT/run
cd $OUT/run           && python3 w5_gghv_certifier.py          # 4.8 s
cd $OUT               && python3 gc_enum_audit.py > gc_enum_audit.log   # 1.0 s
cd $OUT               && python3 gc_run300.py 125 100          # 23.3 s
```

`gc_run300.py <xmax> <M>` — `xmax` is Algorithm 1's corner bound, `M` the
Algorithm 8 bound on v11(A0). There is no CLI in `ggv_algorithms.py` itself: it
is a library, driven by `w5_gghv_certifier.py` (fixed at xmax=60, M=50, i.e.
max ≤ 150) and by `build_case_tree.py`. The "default bound" is therefore
xmax=60 / M=50.

## 2. Counts at each bound

| bound | PLLC (Alg. 1) | distinct admissible complete chains (Alg. 8) | cases, one orientation |
|---|---|---|---|
| M=15 | 1266 @ xmax=60 | 0 | — (control P4: [5]'s B ≥ 16) |
| M=35 ([5] §5's bound) | 1266 | 27 (16 length-1, 11 length-2) | — |
| **M=50, xmax=60 (default)** | 1266 | 260 | **34 with max ≤ 150** |
| **M=100, xmax=125** | 5905 | 5706 | **474 with max ≤ 300** |

* `w5_gghv_certifier.py` reproduces **19/19 checks, 34/34 published cases at
  max ≤ 150 and 10/10 GGHV rows** — re-run here, not quoted. Its regenerated
  `all_cases_max_le_150.json` and `rerun_105_124.json` are **byte-identical** to
  the committed files.
* The max ≤ 300 run gives **474**, matching `extend300.log`; my
  `gc_all_cases_max_le_300.json` is set-identical to the committed
  `all_cases_max_le_300.json` (474/474, exact match after sorting), and its
  by-max histogram matches row for row. Note the archive used a smaller xmax
  (PLLC 5416); at xmax=125 PLLC is 5905 and the chain/case counts are unchanged,
  i.e. PLLC is saturated for this bound.
* Cases with max < 125 at **both** M=50 and M=100: exactly **10**, degree pairs
  {(48,64),(50,75),(75,50),(56,84),(64,96),(66,99),(72,108),(108,72),(80,112),
  (120,80)} — GGHV's ten-row table, nothing more.

## 3. Divergence table — every chain the code generates that the printed tables omit

"Printed" = [5] §5's 14 length-1 chains + 7 length-2 chains (F18–F24), compared
at [5] §5's own bound M=35, plus [5] §6's three case tables projected to
(A0, mid corners, final).

| # | chain (A_i, A'_i, μ_i) → final | len | in §5? | (m,n) it emits | min max deg | verdict |
|---|---|---|---|---|---|---|
| D1a | (8,24),(2,0),μ=3 → (14⁄4,6) | 1 | no | **none** | — | dies |
| D1b | (9,24),(1,0),μ=2 → (9⁄3,6) | 1 | no | **none** | — | dies |
| D2a | (6,18),(6,0),μ=1; (6,15),(1,0),μ=2 → (7⁄3,4) | 2 | no | (2,7),(3,11),… | **168** | survives, > 125 |
| D2b | (6,18),(6,0),μ=1; (6,15),(1,0),μ=2 → (8⁄3,5) | 2 | no | (3,7),(5,12),… | **168** | survives, > 125 |
| D2c | (6,24),(6,0),μ=1; (6,15),(1,0),μ=2 → (7⁄3,4) | 2 | no | (2,7),(3,11),… | **210** | survives, > 125 |
| D2d | (6,24),(6,0),μ=1; (6,15),(1,0),μ=2 → (8⁄3,5) | 2 | no | (3,7),(5,12),… | **210** | survives, > 125 |

**Exact step where each dies / diverges.**

* **D1a** final A=(14⁄4,6): Definition 3.3's index set I(A) is empty. bl−a =
  6·4−14 = 10; k must satisfy 1 ≤ k < l − a/b = 4 − 7/3 = 5/3, so k = 1 only;
  e_k = gcd(1,10) = 1 and gcd(b,(bl−a)/e_k) = gcd(6,10) = **2 ≠ 1**. So
  MN(A) = ∅ and **Algorithm 9 emits no degree pair**. Everything upstream
  (Definition 2.19 completeness, Definition 2.25 admissibility — vacuous at
  j = 0) passes as printed.
* **D1b** final A=(9⁄3,6): same step. bl−a = 9, k = 1 only (kmax = 3 − 3/2 =
  3/2), e_k = 1, gcd(6,9) = **3 ≠ 1** ⇒ I(A) = ∅.
* **D2a–D2d** do **not** die. They diverge at **Algorithm 2 line 7**, which
  accepts A'_0 = (6,0) because v_{1,−1}(6,0) = 6 > 0 and (6,0) ∈ PLLC;
  Algorithm 3's non-simple branch then generates A1 = (6,15) from it, reaching
  the same A1/A2 as the printed F18–F21 route through A'_0 = (6,15). They are
  genuine outputs of Algorithm 8 as printed, and they do emit (m,n)-families —
  but their smallest degree pair is (48,168) / (63,168) at v11(A0) = 24 and
  (60,210) / (90,210) at v11(A0) = 30. **All ≥ 168 > 125**, so they are outside
  [5] §5/§6's printed ranges and outside GGHV's window. They do appear inside
  the max ≤ 300 list (both routes give the same (A1,A2,MN), so the extra A'_0
  adds no new *degree pair* at any bound).

**The decisive negative results.**

* Cases with max ≤ 150 whose (A0, mid, final) shape is **not** in a printed
  [5] §5/§6 table: **0**.
* Chains at M=50 that yield a max ≤ 150 case with an unprinted shape: **0**.
* Degree pairs with max < 125 at M=50 and at M=100: **exactly GGHV's ten**.

**⇒ NO NEW SUB-125 CASE. The search space is not larger.** Every unprinted chain
either has I(A) = ∅ (D1) or first surfaces at max ≥ 168 (D2).

## 4. A'_t for the (10,40) chain — the unprinted assumption, re-derived

Context: [5] §6's tables print (A0, intermediate corners, final) but **not** the
lower corners A'_i. The campaign's shape compiler
`campaign/audit_tracks/trackD_chain_map.py:105,229` therefore defaults to
`A'_t = (1,0)` and flags it ("A'_t not printed in Sec.6; assumed (1,0)");
`AUDIT_EOD.md` §4.3 and `CATCHES.md:32` record the (10,40) case as resting on it.
`ggv_algorithms.py` contains **no** such assumption — it enumerates A'_0 in
Algorithm 2 — so the assumption can be replaced by the algorithm's own filters.

Enumerating `get_starting_edges(10, 40, PLLC)`: Algorithm 2 admits **58**
starting edges (A'_0, μ) for A0 = (10,1,40). Of these, exactly **one** carries
any admissible complete chain:

| A'_0 | μ | dir(ρ,σ) | complete chains | admissible complete |
|---|---|---|---|---|
| **(2,1,0)** | 4 | (5,−1) | 41 | **25** |
| (10,1,b') for 34 values of b' | 1 | (1,0) | 0–6 | 0 |
| 23 further (A'_0, μ) | 2,3,4,5,6,7,8,9 | various | 0 | 0 |

* **(1,0) is not even an admissible A'_0 for A0 = (10,40).** It never appears
  among the 58 starting edges: for μ=1 the edge direction is (1,0) and A'_0 must
  be (10, b'), while for the μ=4 direction (5,−1) the lattice points on the edge
  are (10−i, 40−5i), giving (2,0) at i=8 and never (1,0).
* **A'_t is forced, not assumed: A'_0 = (2,0), μ = 4.** Both published (10,40)
  rows come out of it — mid=(16⁄5,6), final=(23⁄10,3), (m,n)=(3,2), max=150; and
  mid=(18⁄5,8), final=(8⁄5,3), (m,n)=(3,2), max=150.
* **No alternative survives**, so nothing new is opened. Over all 25 admissible
  complete chains from A0=(10,40) (v11 = 50), the minimum degree-pair max is
  **150**, attained only by the two published rows; the next values are 200
  ((4,3) on final (11⁄5,4) and (3,4) on (7⁄10,1)), 250, 350, 400, 550.
  **Nothing below 150, hence nothing below 125.**
* **Action for the campaign:** the compiled polygon for the (10,40) shapes should
  use A'_t = (2,0), not (1,0). The default is wrong for this case; it changes the
  Newton polygon B = conv{(0,0), A'_t, A_t, …, A_0, (0,c)} and the slope
  q = b_t/(a_t − a') the compiler derives from it. This does not add a degree
  pair, but any shape already built for (10,40) under (1,0) is built on the
  wrong lower corner.

## 5. F6 / the seventh discrepancy — still holds

Checked in the code, not quoted:

* Over all 24 printed families F1–F24 and j = 0..7, **F6 is the only** family
  whose printed formula ever gives gcd(m,n) > 1: F6 = (m,n) = (3j+4, 8j+10) has
  gcd 2 at j = 0,2,4,6 → (4,10), (10,26), (16,42), (22,58).
* Definition 3.3's own MN(A) for F6's final corner A = (9⁄5, 4) at k = 2 is
  {(7,18),(13,34),(19,50),(25,66),…} — exactly the **odd**-j members. **(4,10) is
  absent** from MN(A) as the re-implementation computes it, although it does
  satisfy the Diophantine (8m − 3n = 2; 8·4 − 3·10 = 2): it is excluded by the
  coprimality clause alone.
* So the D7 finding stands unchanged: `campaign/audit_tracks/trackD_targets.json`'s
  entry `F6(j=0; m,n=4,10)` at max = 250 is not a possible counterexample shape
  under [5]'s own Definition 3.3. Smallest coprime F6 member is j = 1, (7,18),
  max = 18·25 = 450.

## 6. Caveats

* This audits the **enumeration** only (which degree pairs can occur), never the
  per-case kills. GGHV's §3/§5 kills and the external "[4, §3.5]" kill of
  (80,112) are unchanged and still not re-derived.
* The re-implementation is the campaign's own; this run is an independent
  *execution and instrumentation* of it, not a second independent transcription
  from the PDF. A shared misreading of [5]'s pseudocode would not be caught here.
  It is, however, checked against the printed tables (34/34, 10/10) and against
  four negative controls that must break.
* `mn_pairs` is capped at max_mn = 200 throughout; for v11(A0) ≥ 16 that covers
  every degree pair with max ≤ 3200, far beyond any bound used.
* The M=100 run used xmax = 125 for Algorithm 1 (the archive used a smaller
  value giving PLLC = 5416). Counts are identical, so PLLC is saturated at this
  bound; no claim is made about M > 100.

## 7. Cross-check against the source PDF text

A concurrent ground-cover agent left an extracted text layout of
arXiv:1708.07936 in `groundcover/1708_layout.txt` / `sec56.txt`. Spot-checks
against it (not against `ggv_reference_tables.py`):

* line 1385 — `F6 (5, 20) (1, 0) (9 ≀ 5, 4) 2 3j + 4 8j + 10` — the F6 row is
  transcribed faithfully, so §5 of D7 rests on the paper's own printed formula.
* lines 1521–1522 — the two (10,40) rows read
  `(10,40) (16/5,6) (23/10,3) (3,2) 150` and `(10,40) (18/5,8) (8/5,3) (3,2) 150`.
  **§6's table has no A′ column at all** (contrast §5's header at `sec56.txt:41`,
  `Family A0 A′0 A1 k m n`), and (10,40) appears nowhere in §5. This confirms
  directly that A'_t is unprinted for the (10,40) case — and §4 above shows the
  algorithm forces it to (2,0), not the (1,0) the compiler defaults to.
* line 1369 — `complete chains of length 1 and 2 admissible complete chains of
  length 2` — [5] §5's sentence, verbatim; D3 stands.
