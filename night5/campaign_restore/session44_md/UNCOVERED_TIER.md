# Audit sweep 2 — what was actually missed (Session 44)

Three suspicions were checked mechanically. Two were real.

## 1. The µ3=0 stratum of the B=16 ladder  (REAL GAP — being closed now)

Every trusted F-system verdict (j=2,3, µ0 and µ1 saturations) was run in
the gauge µ3=1. The scaling (x,y) → (λ^a x, λ^b y) rescales µ3 by
λ^(a+b), so the gauge covers exactly the µ3 ≠ 0 locus — **the µ3=0
stratum is fixed by the action and was never queried on the
derivation-grade instrument** (only the superseded Abel transcription ran
a free-µ3 chart). Consequences:

- j=2,3 EMPTY claims are, as of this audit, claims about µ3 ≠ 0 only.
- Sol's T1 crack files (deg q1 = 8) are also gauged µ3=1; the µ3=0
  companions `lead4/j7mu1_mu3zero_*.ms` were generated (T1b in
  SOL_TASKS.md) and are SMALLER than T1's systems.
- Running here: `mu3zero_batch.sh` = j=2,3 (both saturations) at µ3=0
  exactly, plus a direct mod-p shot at the j=7 µ3=0 companion.

## 2. The superset tier: 732 charts, 7 legitimate chains, never swept
   (THE BIG ONE)

`build_all()` contains 866 eps-passing charts: 134 **derived** + 732
**superset**. CANDIDATE_MAP.md's "all 134 charts" ranked only the derived
tier. The superset tier belongs to the 8 chains where the derived
reduction does not close ("c_t not an integer" etc.), and of those:

| chain | max | superset charts | ever run |
|---|---|---|---|
| (10,40)/16/5,6/23/10,3 (3,2) | **150** | 54 | 0 |
| (10,40)/18/5,8/8/5,3 (3,2)   | **150** | 72 | 0 |
| (12,36)/21/4,9/19/4,8 (2,3)  | **144** | 160 | 0 |
| (12,36)/21/4,9/12/4,5 (2,3)  | **144** | 112 | 0 |
| (11,33)/19/4,8 (2,3)         | 132 | 160 | 0 |
| F24 (3,4) — paper-flagged OPEN | 128 | 62 | 5 (EMPTY) |
| F11 (2,5)                    | 140 | 62 | 8 (TIMEOUT/UNKNOWN) |
| F22 (2,3) — excluded, Prop 6.1 | 96 | 50 | 0 (paper's own exclusion) |

Five published chains of the ≤150 catalog — including both max-150 rows —
have ZERO verdicts from any instrument, ever. They were recorded as
"honestly out of scope" when the derived reduction failed, and the
superset fallback that exists precisely for them was queued for only 13
of their 732 charts.

Soundness caveats, stated now so nobody over-claims later:
- superset mode is a bounded enumeration (template from terminal corner
  data, r ≤ 8, both orientations). EMPTY across a chain's whole superset
  family is a kill OF THAT FAMILY; the enumeration's completeness for the
  chain is an assumption inherited from the original track-D design.
- any witness is a reduced/modular object: replay + lift per the standing
  standards before any claim.

Plan: the full-866 rank+vertex sweep is running (make_loose_targets on
build_all); loose vertex-alive superset charts go to the constructive
walker, tight ones to the two-prime queue, chain by chain, smallest
params first.

## 3. eps-filter silent drops  (CLEAN — audited, no gap)

check_eps mixes the paper's vertex condition with the engine's row-0
shape requirement, so a mathematically-valid chart could in principle be
rejected invisibly. Counted over all derived candidates of the 34 chains:
134 pass, 0 fail the eps arithmetic, 0 fail the row-0 shape. The filter
never dropped anything; the derived tier is complete as claimed.
