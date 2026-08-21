# Artifact index for this branch

Everything below is new; no file that existed on
`claude/plane-counterexample-endgame-az3geq` is modified or deleted
(`git diff --name-status base...HEAD` is 100% `A`). `STATUS.md`, `MANIFEST.md`
and PR #6 are untouched.

## Certifiers (each prints PASS/FAIL and carries negative controls)

| file | what it certifies | score |
|---|---|---|
| `gghv_audit/w5_gghv_certifier.py` | the GGV enumeration behind GGHV Theorem 2.1, against all three published tables | 19/19 |
| `gghv_audit/w5_pairs_105_124.py` | every ordered degree pair with 105 ≤ max ≤ 124, decided | 4/4 |
| `samesign/run_sweep.py` | the same-sign weighted-homogeneous sector, exactly | 9/9 |
| `symslice/run_symslice.py` | the μ_n-equivariant slices of case (2) | see log |
| `gao/run_gao.py` | Gao's dimension-3 members, both k-routes, witnesses | 17/17 |
| `lift/lift_pipeline.py` | Hensel lift + rational reconstruction + exact verify | 3/3 |
| `wave4/w4_case2_selftest.py` | the case-(2) weight grading, gauge, charts, elimination | 13/13 |
| `wave4/w4_edge_reconciliation.py` | why the edge count is 5 here and 1144 in wave1/ | 7/7 |
| `wave4/w4_gf.py` | exact linear algebra over F_p[w]/(g) | 6/6 |
| `wave4/w4_msformat.py` | the msolve-input sanitiser and validator | 7/7 |
| `h2/w5_h2_controls.py` | the H2 engine, with a correction to its shipped control | 5/5 |
| `pent/run_pent_v3.py` | the pentagon hit detector v3 and the slice search | 9/9 |
| `pent/run_pent_v3b.py` | the same with exact (dual-number) Jacobians | 3/3 |

## Data and logs

| path | contents |
|---|---|
| `gghv_audit/case_tree.json` | GGHV's case tree, 11 nodes, each with page reference, hypotheses, what it kills, and whether this audit reproduced it |
| `gghv_audit/pairs_105_124.json` | all 4560 ordered pairs in the window, each decided with its reason |
| `gghv_audit/all_cases_max_le_150.json` | the 34 cases, reproduced |
| `gghv_audit/all_cases_max_le_300.json` | the 474 cases at max ≤ 300 — new, beyond the published horizon |
| `gghv_audit/DISCREPANCIES.md` | six recorded divergences, none affecting a degree pair |
| `gghv_audit/controls.log`, `pairs.log`, `extend300.log` | run logs |
| `samesign/sweep_results.json`, `TABLE.md`, `sweep.log` | 230 cells, 378 branches, 0 non-automorphisms |
| `symslice/symslice_results.json`, `symslice.log`, `artifacts/*.ms/.out` | 1140 cells, solver confirmation on the largest per n |
| `gao/family.json`, `mechanism_table.md`, `gao_audit.log` | the Gao members |
| `lift/lift_results.json` | controls plus the lifted case-(2) points |
| `wave4/artifacts/item1_cascade_results.json` | Item 1: every w=−4 run, every RUR, every residual cell, with controls |
| `wave4/artifacts/c2_full_*` | the direct 71-variable attempt (OOM) |
| `wave4/artifacts/edge_eliminant_Q_one.json` | the exact eliminant over ℚ, if reconstruction succeeded |
| `pent/RUNLOG.tsv` | the pentagon msolve ladder: generators, gauges, exit code, seconds, **peak RSS**, output bytes, verdict |
| `pent/pent_v3_results.json`, `pent_v3b_results.json` | every Newton start and every slice |
| `h2/h2_state.json`, `h2_sweep_900.log`, `h2_controls.log` | the above-125 queue at a 900 s cap |
| `h4/h4_escalate.log` | the deg_y = 3 msolve escalation, two primes per cell |
| `papers/` | the six PDFs with `SHA256SUMS` (verified), plus `1708.07936.pdf` and `1406.0886.pdf` fetched this session, and `figures_ggv_alg/` page renders |

## Reproduction

```
# toolchain (BUILD.md on claude/opus-support-toolchain-62st0d)
msolve 0.10.1, Singular 4.3.2p16

python3 wave4/w4_msformat.py            # msolve-input sanitiser self-test
python3 wave4/w4_case2_selftest.py      # case-(2) structure
python3 wave4/w4_gf.py                  # exact linear algebra over F_p[w]/(g)
python3 wave4/run_item1_cascade.py      # Item 1 (needs msolve)
python3 wave4/w4_edge_reconciliation.py # the 5-vs-1144 reconciliation
python3 gghv_audit/w5_gghv_certifier.py # T1
python3 gghv_audit/w5_pairs_105_124.py  # T1(b), the full window
python3 samesign/run_sweep.py           # T2 (needs Singular)
python3 symslice/run_symslice.py        # T3 (needs msolve)
python3 lift/run_lift.py                # T4
python3 gao/run_gao.py                  # T5
python3 pent/run_pent_v3.py 8           # Item 2a
python3 pent/run_pent_msolve.py         # Item 2b (writes pent/RUNLOG.tsv)
cd h2 && PYTHONPATH=../campaign/audit_tracks python3 w5_h2_controls.py   # Item 3 controls
W2_SCRATCH=/tmp/h4scr python3 h4/w5_h4_escalate.py                        # Item 4
```
