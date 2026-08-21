# Reading the .out files in this directory — the standing rule

msolve exits 0 on timeout, on crash, and on a parse error. So:

>  **An EMPTY (0-byte) `.out` file is NOT a verdict.** It is not `EMPTY`, it is
>  not a hit. It means the run did not finish, or died.

Only a non-empty file carries a verdict:

| content | meaning |
|---|---|
| `[-1]:` | no solution over the algebraic closure — EMPTY |
| `[0, [...]]` | solutions exist; the parametrization follows |
| 0 bytes | **NO VERDICT** (timeout / crash / rejected input) |
| anything else | UNRECOGNISED — report verbatim, do not interpret |

Files currently in flight when committed (0 bytes, no verdict):
`char0_118v.out` — the characteristic-zero run, still computing.

## And a second rule, learned the hard way tonight

A `.ms` file whose equations use a variable **not declared in its header** is
malformed, and msolve will return `[-1]` on it — a *false* EMPTY. This
happened, and the verdict was retracted (`../RETRACTION_msolve.md`). Both
exporters now assert against it, but if you find a stray `.ms` here, check it
before trusting any verdict derived from it:

    header=$(head -1 F.ms | tr ',' '\n' | sort -u)
    used=$(tail -n +3 F.ms | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | sort -u)
    comm -13 <(echo "$header") <(echo "$used")     # must be empty

## Recorded non-verdict: prime 2, first attempt

`P2=1000033 94vars exit=139 bytes=0` — exit 139 is **SIGSEGV** (128+11) with an
empty output file. That is the memory-cap failure mode: msolve hits a failed
allocation and segfaults, exiting without writing. **NO VERDICT.** It is not
EMPTY and it is not a hit, and it must never be quoted as either.

Cause: the run was capped at ~7 GB while three msolve processes competed for a
15 GB machine (one alone held 4.9 GB). Fix applied, and it is the campaign's own
standing lesson from the identical failure in the pentagon runs: **sequence, do
not race.** Competing runs were stopped, and the chain was pushed deeper first
so that Gröbner sees fewer variables, rather than simply granting more memory.
