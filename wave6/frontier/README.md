# OPEN-1: the h-branch frontier, with the named-but-unrun engine

## The flag that was left up

`campaign/moduli_phase2/FRAMEWORK.md` states its own boundary and names the fix:

>  "The real boundary is now **memory, not time**: the unresolved cases are
>   killed by the OOM killer inside the time budget (verified directly —
>   `k=5, h=t, deg≤4` died at 2m46s of a 900 s budget on a 16 GB machine).
>   More RAM, or an **F4/FGLM engine such as msolve**, moves the line further."

msolve is installed in this container and **was never pointed at these cases**.
That is a Rosetta-Stone flag: the resolving step is named, and simply undone.

By the endgame-tablebase ranking these are also the right target — they sit on
**OPEN-1**, which the campaign calls "the campaign's real frontier": the
`deg_y = 3` slice, equivalently the h-branch at `k ≥ 4`.

## What is here

- `gen_hbranch.py` — regenerates the *campaign's own* h-branch system for any
  `(K, h, D, p)` by importing `hbranch_code` out of
  `session35_singular_modular_push.py`, so the system is theirs, not a
  re-derivation of mine. It swaps the terminal `slimgb` call for a dump of the
  ideal generators (construction is cheap; it was the Gröbner step that OOMed).
- `dump2ms.py` — converts a generator dump to msolve format, renaming `c(i)` to
  `c_i` since msolve will not parse parentheses.
- `hbranch_k5_ht_D4_p1000003.ms` — the first unresolved case, **46 variables,
  64 equations**.

## Status

| case | campaign's result | here |
|---|---|---|
| `k=5, h=t, D=4` | OOM-killed at 2m46s (Singular `slimgb`, 16 GB) | msolve at 6 GB: SIGSEGV → **NO VERDICT**; at 10 GB alone: **running** |
| `k=6, h=t, D=4` | Singular "no more memory", halt 14, at 3m40s | not yet attempted |

The 6 GB segfault was checked for the silent-failure mode first (Deepwater
Horizon): the input validates — 46 variables declared, 46 used, no undeclared
symbols, no coefficient ≥ p — so it was genuine memory exhaustion, not a
malformed file returning a false verdict.

**A SIGSEGV is NO VERDICT.** Never EMPTY, never a hit.
