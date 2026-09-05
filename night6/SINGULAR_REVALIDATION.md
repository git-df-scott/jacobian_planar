# night6 — Singular revalidation (TASK 2): PARTIAL, stopped at handoff

Status: **incomplete**. Work stopped on coordinator instruction mid-task.
What follows is only what was actually established, by reading `night5/`
(read-only) and by import-probing a scratch copy of it. `night5/` was not
modified: the probe ran against a copy at
`<scratch>/lead4_copy/`, made with `cp`, so no `__pycache__` or other
artefact was written into the other executor's lane.

Singular 4.x is now installed (`/usr/bin/Singular`, via `apt-get install
singular`) and is working — it was used successfully for the night6 face
system and the Task 1 integration test.

## 1. The named scripts do not exist

The task named `run_val.py`, `run_val2.py`, `run_ref_val.py`. None of these
is present. `night5/campaign_restore/lead4/` contains exactly one validation
driver:

        night5/campaign_restore/lead4/run_validate.py
        night5/campaign_restore/lead4/trackD_targets_validate.json

## 2. `run_validate.py` is not Singular-backed

Read in full: it imports `walk_ideal` and calls `WI.analyse(...)` on the
single target in `trackD_targets_validate.json`. `walk_ideal.py` is pure
Python/sympy — it invokes no Singular. The string "Singular" appears in
`run_validate.py` only as the *expected* reference verdict printed for
comparison. So running it does not exercise Singular and is not the
environment control the handoff describes.

Its recorded prior outcome is already in the repository at
`night5/validation_out/run_validate.out`:

        VALIDATION: F24(m,n)=3,4 | a=8 b=4 c'=0 r=4 eps=((1, 0),(4, 1))
          Singular (independent instrument) verdict: EMPTY
          level 9: 1 conds, 1 solved, ideal still trivial
          level 12: 2 conds, 0 solved, ideal has 2 relation(s)
        walk_ideal verdict: OPEN   (1202s, 2 relations)
        *** DISAGREES ***

which matches the handoff's own note (section 4b) that `walk_ideal` failed
validation and was killed rather than trusted. **This run was not repeated
by me**; the line above is quoted from the existing file, not measured here.

## 3. The Singular-backed environment control cannot be run — missing module

The handoff's environment control ("pipeline reproduces EMPTY on
`trackD_targets_validate.json`") is implemented by

        night5/campaign_restore/lead4/case1_envcheck.py

whose docstring is exactly "Environment check: re-run the campaign's own
Singular pipeline on the target that an independent run of it decided
EMPTY." It does `import trackD_extract as TE` and calls `TE.run(NP, NQ, r,
...)`.

**`trackD_extract.py` is absent.** A filesystem-wide search
(`find / -name "trackD_extract*"`) returns nothing. It is not in the restored
`lead4/` tree and not anywhere else on this machine.

Import probe of the copied tree (result per module):

        IMPORT-FAIL  case1_envcheck    ModuleNotFoundError: No module named 'trackD_extract'
        IMPORT-FAIL  case1_rational    FileNotFoundError: 'msolve'   (msolve binary absent)
        IMPORT-FAIL  case1_minlevel    IndexError (expects argv)
        IMPORT-FAIL  case1_obstruction IndexError (expects argv)
        IMPORT-FAIL  case1_verdict     IndexError (expects argv)
        IMPORT-FAIL  case1_vertexpolys IndexError (expects argv)
        IMPORT-OK    cascade, case1_allcovers, case1_cascade, case1_descend,
                     case1_face_derive, case1_hurwitz, case1_ladder,
                     case1_msolve, case1_nondeg, case1_orbits, case1_point,
                     case1_points, case1_ranks, case1_reduce, case1_symmetry,
                     case1_validate, dk_eliminate, face_eq, face_param
        (the probe was cut off by a time limit before reaching the
        remaining modules: run_validate, trackB1_polygon, uz_*, walk_ideal,
        walk_sym — their import status was NOT measured)

**Conclusion actually established:** the handoff's Singular-backed
environment control is not runnable from the restored tree as it stands,
because `trackD_extract` is missing. Per the standing rule, this is recorded
rather than improvised around — no substitute driver was written.

## 4. Not done

* `run_validate.py` was not re-run here (no fresh wall time measured).
* `dk_eliminate.py` (the documented literature control that reproduces GGHV
  equation (5.9)) was identified as the other available control with a
  known published answer, but **was not run**.
* No EMPTY/non-EMPTY verdict was reproduced by me in this task. The expected
  EMPTY is therefore **neither confirmed nor contradicted** by this session.

## 5. What a successor needs

To run the real environment control, `trackD_extract.py` must be recovered
from the campaign history (it is referenced by `case1_envcheck.py` and is the
module that builds and dispatches the Singular ideal for a trackD target).
Without it, the only executable route in the restored tree is the pure-sympy
`walk_ideal` path, which the handoff already records as failing validation.
