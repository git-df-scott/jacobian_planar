# night3 TOOLING — solver and environment audit

Audit record only. No searches, no new mathematics, no existing file modified.
Nothing was installed.

Run date (UTC): 2026-08-28. Repo root: `/home/user/jacobian_planar`, branch `claude/fable-6o0nqe`.

---

## 1. Solver inventory

| tool | status | version |
|---|---|---|
| msolve | NOT FOUND | — |
| Singular | NOT FOUND | — |
| Macaulay2 (`M2`, `macaulay2`) | NOT FOUND | — |
| sage | NOT FOUND | — |
| gp / PARI | FOUND (`/usr/bin/gp`) | GP/PARI CALCULATOR 2.15.4 (released), x86-64/GMP-6.3.0 kernel, 64-bit, threading engine pthread |
| flint command-line tools | NOT FOUND | — |
| flint library | FOUND (shared lib only) | 3.0.1 via pkg-config; `/lib/x86_64-linux-gnu/libflint.so.18` |
| python-flint | FOUND (python module) | 0.9.0 |
| sympy | FOUND | 1.14.0 |
| cypari2 | NOT FOUND | — |

Supporting: Python 3.11.15, numpy 2.4.6.

Best available Groebner engine: **sympy 1.14.0** (`sympy.groebner`, Buchberger, with
`modulus=` for GF(p)). No dedicated Groebner system (msolve / Singular / Macaulay2 /
sage) is present. gp/PARI is present but is not a general Groebner engine; the flint
library and python-flint are present but expose no Groebner basis routine. The
benchmark in section 3 therefore uses the sympy fallback.

---

## 2. Machine profile

| item | value |
|---|---|
| cores (`nproc`) | 4 |
| RAM total | 15 Gi |
| RAM available | 15 Gi (584 Mi used, 589 Mi buff/cache, at time of audit) |
| swap | 0 B |
| disk available in working directory | 29 G available of 252 G on `/dev/vda` (24% used) |

---

## 3. Groebner benchmark — CONTROLS ONLY

Engine: sympy 1.14.0, `groebner(..., order='grevlex', modulus=999983)`. Field GF(999983).
Each case run in its own process. Cases (a) and (b) are known-answer controls.

| case | system | expected | result | wall time |
|---|---|---|---|---|
| a | `<x^2+y, x^2+y+1>` | unit ideal / empty | GB = `[1]` — unit ideal confirmed, variety empty | 0.0022 s |
| b | `<x^2-1, y-x>` | 2 solutions / dim 0 | GB = `[y^2 - 1, x - y]`, `is_zero_dimensional = True` | 0.0023 s |
| c | scaling probe, n=6 | — | completed, GB length 39, zero-dimensional | 13.27 s |
| c | scaling probe, n=10 | — | **TIMEOUT at 120 s** | >120 s |
| c | scaling probe, n=14 | — | **TIMEOUT at 120 s** | >120 s |
| c | scaling probe, n=18 | — | **TIMEOUT at 120 s** | >120 s |

Case (c) construction: `n` random dense quadratic equations in `n` variables over
GF(999983) — every monomial of total degree <= 2 given an independent uniform random
coefficient — fixed seed 77, per-case wall limit 120 s enforced externally.

**Label, as required: case (c) is a generic dense-random benchmark.** It measures this
container's practical Groebner ceiling with the available fallback engine and nothing
else. It is not a statement about any specific problem, system, or support family in
this campaign.

Recorded ceiling on this box with this engine: n=6 dense quadratic completes in ~13 s;
n=10 and above do not complete within 120 s.

---

## 4. Reproducibility spot-check

Re-ran `night2/sol/verify_deliverables.py` once on today's container. Exit status 0.
Output identical to the night2 record:

```
PASS V1 Python syntax
PASS V2 CSV shape, controls, rank-nullity, and cross-prime agreement
PASS V3 exact d=3 certificate checker
PASS V4 report/theory required conclusions
PASS DELIVERABLES all fast integrity checks completed
```

Final line: `PASS DELIVERABLES all fast integrity checks completed`.
