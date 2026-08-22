# H2 — the 866 / 804 / 180 / 167 counts, reconciled

These four numbers appear across `41.md`, `STATUS.md`, `ABOVE_125_STATUS.md`
and the `trackD_*.json` state files, and they have been quoted as if they
measured the same thing. They do not. Traced against the actual JSON:

| number | what it actually counts | source |
|---:|---|---|
| **866** | reduced-polygon **shapes** emitted by the chain→polygon map and put through the vertex probe, at **all** max degrees | `trackD_vertex.json`: `388` dead + `478` live |
| **478** | of those, the shapes that **survived** the vertex probe (a required vertex is not identically zero) | `trackD_vertex.json["live"]` |
| **167** | of the 478, those in the §6 catalogue with **max ≥ 125** — tier `sec6>=125` | `trackD_targets.json` |
| **13** | family chains continued **past** [C] §6's horizon of 150 — tier `gen>150` | `trackD_targets.json` |
| **180** | the elimination queue = `167 + 13` | `len(trackD_targets.json)` |
| **804** | a **different object**: admissible **degree pairs** with `max ∈ [125,300]` from the Path-D Newton-polygon enumeration. Not shapes, not chains. Blocked because none can be assigned an `L` | `41.md` |

Verified programmatically, not by reading prose:

```
targets inside vertex-live : 167      (every sec6>=125 target is a live shape)
targets inside vertex-dead : 0        (no dead shape leaked into the queue)
targets in neither         : 13       (exactly the gen>150 tier, which post-dates
                                       the vertex probe and was never probed)
```

**So the funnel is:** `866 shapes → 478 vertex-live → 167 at max ≥ 125 (+13
extended) = 180 queued`. And **804 is not in this funnel at all** — it counts
degree pairs in a separate, still-blocked enumeration. Quoting "804 unsearched"
and "167 targets" in the same breath compares a pair count with a shape count.

## Queue state as found

| state | count | source |
|---|---:|---|
| certified EMPTY (one prime, 65521) | 20 | `trackD_certified.json` |
| timeout, no verdict | 9 | `trackD_solve.json` (`3` carried into `trackD_certified.json`) |
| terminal in the resume state | 49 entries | `trackD_state.json` |
| **never run** | **160** | `180 − 20` |

## Two defects found in the machinery, both fixed

1. **`trackD_extract.py` pointed at a dead scratch directory** — the absolute
   path of a previous session's scratchpad (`…/19771ba8-…/scratchpad`). Any new
   container ENOENTs on the first write. Now resolved at import time, with a
   `TRACKD_SCRATCH` override.
2. **The characteristic was hardcoded** (`P = 65521`), so the whole certified
   table rests on a single prime. Now `TRACKD_PRIME`, and
   `trackD_twoprime.py` drives every target at two primes, both `≡ 1 (mod 3)`.

`trackD_twoprime.py` records **both** verdicts per target and never averages
them: `EMPTY` requires both primes, and one-EMPTY-one-LIVE is reported as
`DISAGREE`, loudly. Its `combine()` is unit-tested against an explicit truth
table rather than assumed.

## Chain→polygon map: already hardened, and re-verified here

`ABOVE_125_STATUS.md` recorded the map as the blocker; `TRACKD_CHAIN_MAP.md`
records it as resolved. Re-run from scratch this session:

```
validation: 6/6 published reduced pairs reproduced exactly
  Prop 4.1 (9,27), Prop 4.2(1)(2)(3) (9,24), Prop 4.3(1)(2) (8,28)
total chains: 34      total eps-passing candidate shapes: 134
```

The validation is a real comparison — it matches computed `NP`, `NQ` and the
bracket exponent `r` against the vertex lists transcribed from [G] §4, and
reports `[MISSED]` on failure. It is not a hardcoded pass.

**Cusp-type enumeration is complete and self-checking:** the map's degree pair
`(m·v₁₁(A₀), n·v₁₁(A₀))` agrees with [C] §6's own max column on all 34 rows.
Seven chains emit **no** engine-compatible shape, each for a stated structural
reason rather than silently — five because `c_t = (a+b_t)/a_t` is not an integer
(the monomial twist does not close), one because `A'_t` is not printed in §6,
one because no shape passes the ε filter. That is a named out-of-scope set, not
a gap.
