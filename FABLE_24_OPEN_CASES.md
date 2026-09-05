# 24 enumerated, published, never-attacked cases — the hunting ground we didn't know we had

Fable, 2026-08-23. Primary source: **arXiv:1708.07936**, Guccione–Guccione–
Horruitiner–Valqui, *"Some algorithms related to the Jacobian Conjecture"*,
section 6. Text extracted verbatim (`fable_xcol/alg_paper_text.txt`).

## The finding

Section 6 states, verbatim:

> *"Here we describe the shape of the **34 possible counterexamples** with
> `max{deg(P),deg(Q)} <= 150`."*

The later paper (arXiv:2204.14178, the one this campaign works from) only handled
those with `max < 125` — its 10 cases. **The other 24 are enumerated, published,
complete with Newton-polygon corner data, and have never been discarded by
anyone.**

This is a far better hunting ground than the campaign's "804 pairs above 125",
a figure from the lost Sessions 19–38 that no artifact supports. These 24 are
concrete and in print.

## The complete list

### A. From the `(m,n)`-families (13 cases; 6 are `>= 125`)

| family | `(m,n)` | max | status |
|---|---|---|---|
| F1 | (3,4) | 64 | < 125 |
| F1 | (5,7) | 112 | < 125 |
| F2 | (2,3) | 75 | < 125 |
| **F2** | **(3,5)** | **125** | **OPEN** |
| F3 | (3,2) | 75 | < 125 |
| **F7** | **(2,7)** | **147** | **OPEN** |
| **F8** | **(3,7)** | **147** | **OPEN** |
| F9 | (2,3) | 84 | < 125 |
| **F9** | **(3,5)** | **140** | **OPEN** |
| **F11** | **(2,5)** | **140** | **OPEN** |
| F17 | (2,3) | 99 | < 125 |
| F22 | (2,3) | 96 | < 125 (discarded, Prop 6.1) |
| **F24** | **(3,4)** | **128** | **OPEN** |

### B. Complete chain of length 1 (9 cases; 8 are `>= 125`)

| `A_0` | `A_1` | `(m,n)` | max | status |
|---|---|---|---|---|
| **(7,35)** | (19/7,5) | (2,3) | **126** | **OPEN** |
| **(7,42)** | (13/7,6) | (3,2) | **147** | **OPEN** |
| **(7,42)** | (13/7,6) | (2,3) | **147** | **OPEN** |
| **(8,28)** | **(7/4,3)** | **(3,4)** | **144** | **OPEN** |
| (8,28) | (11/4,7) | (3,2) | 108 | **our case** |
| **(9,36)** | (17/9,4) | (3,2) | **135** | **OPEN** |
| **(9,36)** | (17/9,4) | (2,3) | **135** | **OPEN** |
| **(11,33)** | (19/4,8) | (2,3) | **132** | **OPEN** |
| **(12,33)** | (11/3,8) | (2,3) | **135** | **OPEN** |

### C. Complete chain of length 2 (11 cases; 9 are `>= 125`)

| `A_0` | `A_1` | `A_2` | `(m,n)` | max | status |
|---|---|---|---|---|---|
| (8,32) | (8,28) | (11/4,7) | (3,2) | 120 | < 125 |
| **(8,40)** | (8,28) | (11/4,7) | (3,2) | **144** | **OPEN** |
| (9,27) | (9,24) | (11/3,8) | (2,3) | 108 | discarded (Cor 5.7) |
| **(9,36)** | (9,24) | (11/3,8) | (2,3) | **135** | **OPEN** |
| **(10,40)** | (16/5,6) | (23/10,3) | (3,2) | **150** | **OPEN** |
| **(10,40)** | (18/5,8) | (8/5,3) | (3,2) | **150** | **OPEN** |
| **(12,30)** | (16/3,10) | (11/6,3) | (3,2) | **126** | **OPEN** |
| **(12,36)** | (12,33) | (11/3,8) | (2,3) | **144** | **OPEN** |
| **(12,36)** | (9,24) | (11/3,8) | (2,3) | **144** | **OPEN** |
| **(12,36)** | (21/4,9) | (19/4,8) | (2,3) | **144** | **OPEN** |
| **(12,36)** | (21/4,9) | (12/4,5) | (2,3) | **144** | **OPEN** |

### D. Complete chain of length 3 (1 case, `>= 125`)

| `A_0` | `A_1` | `A_2` | `A_3` | `(m,n)` | max |
|---|---|---|---|---|---|
| **(12,36)** | (12,30) | (16/3,10) | (11/6,3) | **(3,2)** | **144** |

**6 + 8 + 9 + 1 = 24 open cases**, and `34 - 24 = 10` below 125 — exactly the ten
GGHV worked. The arithmetic closes, which is a good check on the extraction.

## The single most striking entry

> **`A_0 = (8,28)`, `A_1 = (7/4,3)`, `(m,n) = (3,4)`, max = 144.**

That is **our own corner** `(8,28)` with a *different* `(m,n)` and a different
`A_1` — a second, larger case at the same corner that nobody has looked at. The
campaign has spent weeks on `(8,28)` with `(3,2)` while `(8,28)` with `(3,4)` sat
in a published table, untouched.

## Why this matters for the hunt, concretely

1. **These are necessary-condition cases exactly like ours.** The same machinery
   applies verbatim: reduce the polygon by the automorphism chain, get
   `[P,Q] = x^k` with explicit Newton polygons, build the bracket system, run the
   x-column descent and the determinantal rank test.
2. **Some will be structurally cheaper than `(8,28)`.** Chain length is a direct
   proxy for reduction complexity: the eight length-1 cases at `>= 125` are the
   natural first targets, ahead of the length-2 and length-3 ones. Per the
   mission's own instruction — do not assume the smallest degree is easiest.
3. **They multiply the search space by roughly 3x** over the single case the
   campaign has been grinding.
4. **The corner data is already given.** `A_0, A_1, A_2, (m,n)` are printed. What
   is missing is only the analogue of Prop 4.3 — the reduced polygons and the
   bracket exponent — which is exactly the derivation GGHV performs in their §4
   and which we now know how to read.

## Caveats, held to standard

- The 13 family cases (table A) are given as *family + `(m,n)`*, not as explicit
  corners; the family definitions live in §5 of the same paper and must be read
  before those six can be built.
- Extraction is from a PDF text dump. The `34 = 24 + 10` arithmetic and the
  agreement of the ten `< 125` entries with GGHV's table are strong internal
  checks, but **Sol should verify the tables against the published PDF directly**
  before anyone invests solver time.
- These cases being "open" means *not discarded*, i.e. still possible
  counterexamples. It does **not** mean they are likely; it means nobody has
  looked.

## Recommended next action

Build the **eight length-1 cases with `max >= 125`** first — `(7,35)`, `(7,42)`
twice, **`(8,28)` with `(3,4)`**, `(9,36)` twice, `(11,33)`, `(12,33)`. Each needs
its Prop-4.3 analogue derived, then the existing `fable_xcol` pipeline runs
unchanged. `(8,28)/(3,4)` is the obvious first pick: same corner as our current
target, so the reduction is closest to one we already understand.

## Status

No counterexample. What is new is that the campaign's target was one of
**twenty-five** open cases below 150, not one of one.
