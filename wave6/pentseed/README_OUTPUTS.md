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
