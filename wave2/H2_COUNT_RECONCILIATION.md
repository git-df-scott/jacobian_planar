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

---

# Two-prime sweep — results as of 127/180

Both primes `≡ 1 (mod 3)`: **65521** and **65539**. `EMPTY` requires *both*;
one-EMPTY-one-LIVE would be reported as `DISAGREE`, never averaged.

| outcome | count |
|---|---:|
| **EMPTY at both compliant primes** | **31** |
| TIMEOUT (90 s / prime budget) | 96 |
| **DISAGREE** | **0** |
| **LIVE** | **0** |
| not yet run | 53 |

**The old table is fully reproduced.** All **20/20** shapes certified EMPTY in
the previous single-prime (65521) run come back EMPTY at both compliant primes —
no disagreement anywhere — and the sweep adds **11 EMPTYs the old table did not
have**.

## The real stall point, named by parameter count

The sweep does not fail uniformly; it fails by size, and the boundary is sharp
enough to state:

```
EMPTY   verdicts:  params 20 .. 82
TIMEOUT verdicts:  params 38 .. 152
never run        :  params 152 .. 779
```

Parameter count is not a clean threshold — 50, 55 and 82 decide while 48, 51,
53 and 56 time out — so shape matters too. But the direction is unambiguous, and
the **53 unrun targets carry 152–779 parameters**, an order of magnitude beyond
anything this engine has decided. They are not "unrun for want of time"; they
are out of reach of the y-adic + Singular route at any plausible budget.

That replaces the old framing. *"~150 of 167 targets unrun"* suggested a queue
that just needed more hours. The accurate statement is:

> The above-125 sweep decides shapes up to roughly 80 parameters and stalls
> above that. 31 shapes are EMPTY at two compliant primes. The remainder is
> blocked on engine capacity, not on schedule.

A retry pass at 300 s/prime is chained behind pass 1 (`chain_retry.sh`), taking
the cheapest 60 timeouts first; it can only move the boundary, not remove it.

---

# A third defect: the engine could not report OOM

Pass 1 finished all 180 targets and returned **31 EMPTY, 141 TIMEOUT, 8
UNKNOWN**. `UNKNOWN` is not in the campaign's engine contract — that contract is
`EMPTY | NONEMPTY | TIMEOUT | OOM` — so the 8 needed explaining rather than
tallying.

All eight are the same chain (`F11(m,n)=2,5` at `c'=2` and `c'=3`), each running
350–500 s and then returning with **empty stdout and no timeout**. Diagnosed
directly on `F11(m,n)=2,5 | a=7 b=4 c'=2 r=5`:

```
returncode : -9          elapsed : 281s
stdout len : 0           stderr len : 0
'no more memory' present : False
=> OOM
```

**Cause.** `trackD_extract.run()` ignored the subprocess returncode entirely and
reported every non-timeout run as `"RAN"`. An OOM-killed Singular therefore
looked like a successful run that happened to print nothing, and the caller
filed it as `UNKNOWN`. Note that Singular's own *"no more memory"* message is
**absent** here — the process is killed by the OS before it can print anything —
so the returncode check is the only thing that catches this case.

**Fixed.** `run()` now returns `OOM` on a kill signal (`-9`/`137`/`14`) or the
memory message, and `CRASH` on any other nonzero exit with empty output, and
carries the returncode through. `trackD_twoprime.py` propagates both as
first-class verdicts, treats them as **terminal** — a bigger *time* budget does
not buy *memory*, so they are never re-queued — and skips the second prime once
the first has OOM'd. `combine()` was re-tested against an explicit 12-case truth
table.

**No EMPTY verdict changes.** What changes is how 8 undecided targets are
*labelled*: from an uninformative `UNKNOWN` to a named stall reason. That is the
difference between "we don't know why" and "the box ran out of memory" — and the
second is a stall point Plan 43 §6.4 can actually record.

The re-label runs each of the 8 through the repaired engine fresh
(`relabel_oom.py`); none is converted on the strength of the old run.

---

# FINAL — H2 above-125 sweep, complete

All 180 targets carry a verdict from the engine contract. No target is left
labelled `UNKNOWN`.

| verdict | count | meaning |
|---|---:|---|
| **EMPTY** (both compliant primes) | **31** | no non-degenerate realization at 65521 **and** 65539 |
| TIMEOUT | 141 | undecided; wall-clock |
| **OOM** | **8** | undecided; Singular killed by the OS (`rc = -9`) |
| **LIVE** | **0** | — |
| **DISAGREE** | **0** | the two primes never disagreed, anywhere |
| PARTIAL / CRASH / UNKNOWN | 0 | — |

The 8 OOMs are one chain, `F11(m,n)=2,5` at `c'=2` (params 51) and `c'=3`
(params 66), each killed after 204–308 s on a fresh run through the repaired
engine. The timings reproduce the standalone diagnosis (281 s), so the OOM is a
property of these systems at 15 GB rather than an artefact of two engines
competing for memory.

## What this sweep did and did not establish

**Did.** All **20/20** shapes from the earlier single-prime (65521) table
reproduce as EMPTY at both compliant primes, and **11 further shapes** are newly
EMPTY. Nothing anywhere returned LIVE, and the two primes never disagreed on any
target — so the single-prime table was not a characteristic artefact.

**Did not.** `EMPTY` here is still emptiness **mod p**, at two primes. Plan 43
§6.2 forbids promoting that to ℚ. 149 of 180 targets remain undecided.

## The stall point, stated as a size boundary

```
EMPTY   : params  20 ..  82
TIMEOUT : params  38 .. 779
OOM     : params  51, 66      (one chain, memory-bound rather than time-bound)
```

The sweep decides shapes up to roughly 80 parameters and stalls above that.
A retry at 300 s/prime — 3.3× the original budget — converted **zero** of the 46
targets it reached before a worker restart ended it, which is what the boundary
predicts. Its remaining 14 targets sit in the same `params ≥ 74` class and were
deliberately not resumed.

So the honest close-out is not *"149 targets unrun"* but:

> The above-125 sweep decides shapes up to roughly 80 parameters, where it
> returns 31 EMPTYs at two compliant primes and no LIVE. Above that it is
> blocked on engine capacity — wall-clock for most, memory for one chain — and
> more time does not move it.

## Three defects found and fixed in the machinery

1. **Dead scratch path.** `trackD_extract.py` wrote to a previous session's
   absolute scratchpad; any new container ENOENTs on the first write.
2. **Hardcoded characteristic.** The entire certified table rested on one prime.
   Now `TRACKD_PRIME`, with a two-prime driver that reports one-EMPTY-one-LIVE
   as `DISAGREE` rather than averaging.
3. **OOM invisible.** `run()` ignored the subprocess returncode, so an
   OOM-killed Singular looked like a successful run printing nothing and was
   filed `UNKNOWN`. Singular's own *"no more memory"* message never appears —
   the OS kills it first — so the returncode is the only signal.
