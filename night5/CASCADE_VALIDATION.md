# night5 CASCADE_VALIDATION — the cascade engine's environment control

Executor record. Outcome and interface only; no interpretation of what the
result means for any mathematical question.

Raw console output: `night5/validation_out/run_validate.out`.

## Provenance of files fetched for this task

`cascade.py` was already present from TASK A. The validation target, the runner,
and their import closure were **not** in the restored tree (TASK A's `lead4/`
scope was `cascade.py`, `uz_*.py`, `case1_*.py`, `face_eq.py`, `dk_eliminate.py`
only). Fetched from the same commit `a301e16` on
`origin/claude/past-code-session-8mdjqn`, as recorded in `night5/RESTORE_NOTES.md`:

| file | bytes | why |
|---|---|---|
| `run_validate.py` | 874 | the runner that drives the validation target |
| `walk_ideal.py` | 6965 | the pipeline it validates |
| `walk_sym.py` | 8895 | `walk_ideal` imports `hull_rows` from it |
| `trackB1_polygon.py` | 9414 | `walk_sym` imports `hull_rows` from it |
| `face_param.py` | 4752 | `cascade.py` imports `lattice_points` from it |
| `trackD_targets_validate.json` | 385 | the validation target |
| `trackD_targets_108.json` | 821 | the target `cascade.py` hardcodes |

## Which "pipeline" the control refers to

The handoff records: *"pipeline reproduces EMPTY on trackD_targets_validate.json"*.
Searching every `.py`/`.md`/`.sh` in `session44/` for `trackD_targets_validate`
gives seven referents: `run_validate.py`, `run_val.py`, `run_val2.py`,
`run_ref_val.py`, `chk2.py`, `case1_envcheck.py`, `CASE1_ESSENTIAL_FACE.md`.

Of the runners:

- **`run_validate.py`** drives `walk_ideal.analyse()` — pure Python + sympy, and
  the only one runnable in this container. This is what was run.
- `run_val.py`, `run_val2.py` drive `wgrade.Walk`, which shells out to
  `Singular` via `subprocess`.
- `run_ref_val.py` shells out to `Singular` directly.

**`Singular` is not installed** (confirmed again here; also recorded in
`night3/TOOLING.md`, where msolve, Singular, Macaulay2 and sage were all NOT
FOUND). The `shim/Singular` in `lead4/` is a two-line bash wrapper that sets
`ulimit -v` and `exec`s `/usr/bin/Singular` — it does not supply Singular. So the
three Singular-backed routes **cannot run here**. Recorded as an outcome, not
repaired.

Note on what the control can and cannot establish in this container: the line
`Singular (independent instrument) verdict: EMPTY` printed by `run_validate.py`
is a **hardcoded string literal in the script**, not a recomputation. The
instrument that originally produced EMPTY is unavailable here, so the EMPTY side
of the comparison is a recorded prior, not something this run re-derived.

## The validation target

`trackD_targets_validate.json` holds exactly one entry:

```
tag : F24(m,n)=3,4 | a=8 b=4 c'=0 r=4 eps=((1, 0),(4, 1))
r   : 4
NP  : [[0, 0], [1, 0], [24, 9], [24, 12]]
NQ  : [[0, 0], [4, 1], [32, 12], [32, 16]]
```

## Result: EMPTY was NOT reproduced

Exact command line, run from `night5/campaign_restore/lead4/` (cwd matters — the
script opens the target by bare relative filename):

```
cd night5/campaign_restore/lead4 && python3 run_validate.py
```

No arguments; `run_validate.py` takes none. Exit 0, no stderr.

**Wall time: 1213 s measured end-to-end (script's own timer: 1202 s).**

Full output:

```
VALIDATION: F24(m,n)=3,4 | a=8 b=4 c'=0 r=4 eps=((1, 0),(4, 1))
  Singular (independent instrument) verdict: EMPTY
  level 9: 1 conds, 1 solved, ideal still trivial
  level 12: 2 conds, 0 solved, ideal has 2 relation(s)

walk_ideal verdict: OPEN   (1202s, 2 relations)
*** DISAGREES: walk_ideal says OPEN where Singular says EMPTY.
    Either walk_ideal is incomplete (it only walks driver levels
    and may not reach the contradiction) or it is WRONG.
    Its verdicts on the open case cannot be trusted until this
    is understood. ***
```

| | |
|---|---|
| expected (handoff) | EMPTY |
| obtained | **OPEN** |
| **EMPTY reproduced?** | **NO** |
| ideal at termination | proper, 2 relations (did not contain 1) |
| levels reached | 9, then 12 |

The script's own failure branch fired. The wording of that branch —
"Either `walk_ideal` is incomplete (it only walks driver levels and may not reach
the contradiction) or it is WRONG" — is the script's, quoted here verbatim, not
an executor judgement. Which of those two it is was not determined here, and no
attempt was made to adjust the run to obtain EMPTY.

## `cascade.py` interface inventory

`cascade.py` **runs** once `face_param.py` and `trackD_targets_108.json` are
present. Command and result:

```
cd night5/campaign_restore/lead4 && python3 cascade.py 1
```

Exit 0, wall **10.29 s**:

```
cascade mod 65521, seed 1
  w=-3: 18 eqs, 19 unknowns -> solved (rank 18, 1 free)
  w=-2: 19 eqs, 21 unknowns -> solved (rank 19, 2 free)
  w=-1: 19 eqs, 13 unknowns -> INCONSISTENT
  -> this face point does NOT extend
```

Those ranks match the ones written into the script's own docstring and into the
session-44 commit message that introduced it (`w=-3` rank 18 with 1 free, `w=-2`
rank 19 with 2 free, `w=-1` inconsistent), so the file reproduces its documented
behaviour.

### Interface, read from the code

**Entry point.** `python3 cascade.py [seed]` — `sys.argv[1]`, an integer, default
`1`. That is the *only* command-line input. There is no `argparse`, no target
flag, no output flag.

**Inputs it actually consumes**, and where each comes from:

| input | source | changeable without editing code? |
|---|---|---|
| target polygons `NP`, `NQ` and RHS exponent `r` | `json.load(open("trackD_targets_108.json"))[1]` — **filename and index both hardcoded** (line 28) | **no** |
| prime `p = 65521` | module-level constant (line 26) | **no** |
| weight `w(i,j) = j - 2i` | module-level lambda (line 31) | **no** |
| face-level values | drawn at random, `rng.randrange(1, p)` over `LP[-2] + LQ[-3]` | only via the seed |
| RNG seed | `sys.argv[1]` | **yes** |

**Working directory.** Must be `lead4/` — the target is opened by bare relative
filename, and `from face_param import lattice_points` needs `face_param.py`
importable.

**Target-file schema** (`trackD_targets_*.json` is a JSON list of objects; keys
seen: `NP`, `NQ`, `r`, `tag`, `tier`, `size`, `max`, `params`). Only `NP`, `NQ`
and `r` are read. `NP`/`NQ` are lists of `[i, j]` polygon vertices; interior
lattice points are filled in by `face_param.lattice_points`.

**Output.** Human-readable text only: one line per weight level giving equation
count, unknown count, and either `solved (rank R, F free)` or `INCONSISTENT`;
then either "this face point does NOT extend" (and `sys.exit(0)`) or a count of
violated `w=0` consistency conditions. **It emits no EMPTY/NONEMPTY verdict and
writes no file** — so `cascade.py` is not itself the instrument the
"reproduces EMPTY" control refers to.

**Reusable internals**, if it is ever driven as a library:
`rank_modp(rows, ncol) -> (M, rank)` and
`solve_level(lev, newvars, assign, rng) -> (sol, rank, msg)`.

### Feeding radial-sieve survivors to it later — what stands in the way

Recorded plainly, since this was the stated purpose of the inventory:

1. **No input path for a new target.** The target file *and* the index `[1]` are
   literals on line 28. Supplying a different shape needs a code edit, or
   overwriting `trackD_targets_108.json` in place.
2. **Module-level execution.** Lines 26–43 — target load, symbol creation, the
   bracket expansion `br`, and the weight bucketing `byw` — all run **at import
   time**, keyed to that hardcoded target. Importing `cascade` as a module to
   reach `solve_level` therefore builds the *old* system first; `solve_level` and
   `rank_modp` both close over module globals (`p`, `byw`, `cP`, `cQ`, `LP`,
   `LQ`). There is no function that takes `(NP, NQ, r)` as arguments.
3. **The face level is randomised, not supplied.** Line 98 assigns the face
   coefficients from the RNG. The script's own note says this "does not yet use
   the 35 true face solutions". There is no parameter through which specific face
   solutions — or sieve survivors — can be injected.
4. **The prime is fixed** at 65521, so the two-prime agreement standard used
   elsewhere in this campaign is not available from this script as written.

So as restored, `cascade.py` exercises one hardcoded shape at one prime from a
random face point. Pointing it at externally supplied survivors is a code change,
which was out of scope for this task and was not made.

## Scope

This records that one runner executed and what verdict it returned against the
handoff's stated expectation, plus what `cascade.py`'s code accepts as input. The
disagreement is reported as measured. Nothing here says which of the two
instruments is correct, and nothing here bears on any underlying mathematical
question.

## Coordinator interpretation (Fable, added after the run)

The handoff (night6/SESSION44_HANDOFF.md, section 4b) already records:
"walk_ideal.py failed validation (timed out at 540s on a target Singular
decided EMPTY in 3s) and was KILLED RATHER THAN TRUSTED." The instrument
that reported OPEN here is that same walk_ideal — the one instrument
session 44 itself condemned. The session-44 EMPTY verdicts rest on the
Singular/msolve runs performed then, which this box cannot re-run
(no Singular, per night3/TOOLING.md). Consequence, stated at honest
strength: the session-44 modular closures are NOT re-validated on this
machine, and the restored pure-Python cascade tooling must NOT be used
for new verdicts. Any future cascade-type verdict on this box needs a
from-scratch solver with its own controls (as done for E3), or real
Singular/msolve. The restored engine is hereby demoted from "validated
instrument" to "reference code".
