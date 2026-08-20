# Tooling contract (Session 36, WP-0)

## Engines

| tool | version | role |
|---|---|---|
| Singular | 4.3.2 (4330, 64-bit) | primary. **`slimgb` first, `std` second** — three orders of magnitude on sparse quadratic systems |
| msolve | 0.10.1 (built from source, `/usr/local/bin/msolve`) | independent F4/FGLM confirmation |
| sympy | 1.14.0 | symbolic identities only. **Never** for Gröbner work |
| python-flint, PARI/GP | — | available, unused |

Not installed: Macaulay2, Magma, Sage.

### msolve build

```
git clone --depth 1 https://github.com/algebraic-solving/msolve.git
cd msolve && ./autogen.sh && ./configure && make -j4 && make install
```
Build deps: `libgmp-dev libmpfr-dev libflint-dev build-essential`.
**Do not copy `./msolve` from the build tree** — it is a libtool wrapper that
fails with `'.libs/msolve' does not exist`. Use `make install`.

Verified controls: empty ideal `⟨xy−1, x, y⟩` → `[-1]`; zero-dimensional
`⟨x²−1, y−2⟩` → dimension-0 output with 2 solutions.

## Run classification contract

Every Singular invocation must classify into exactly one of
`EMPTY | NONEMPTY | TIMEOUT | OOM`. Memory exhaustion arrives **two ways** and
both must be caught, or a memory failure is silently reported as an
unexplained "no verdict":

- Linux OOM killer → returncode `-9` / `137`
- Singular's own guard → `Singular error: no more memory`, `halt 14`

```python
if p.returncode in (-9, 137, 14) or 'no more memory' in p.stderr:
    return 'oom'
```

## Modular protocol

Every emptiness claim must agree at `p = 32003` **and** `p = 1000003`.
Disagreement means the characteristic is interfering — escalate, do not pick a
winner. Emptiness mod `p` implies emptiness over `Q` for integer systems (a
rational solution with denominators prime to `p` reduces); the converse fails.

## Watchdogs

Never `pgrep -f` / `pkill -f` on your own script name — the pattern matches the
watching shell's own command line. `until ! pgrep -f session35; do ...` never
exits. Use PID files, or match the interpreter plus path.

**This trap has now fired four times across the campaign (three of them in a
single session, 2026-08-19, each time killing the invoking shell mid-command —
once mid-commit, losing an uncommitted document).** A trap that survives being
documented, and that recurs within one session after being corrected twice, is a
**tooling problem, not a discipline problem**. Recommendation for future
sessions: put `pkill`/`pgrep -f` out of reach rather than relying on remembering
the rule —

```bash
# in the session's shell init
pkill()  { echo "pkill is disabled in this repo: use 'pgrep -x <name>' + kill by PID" >&2; return 1; }
```

or strip the binaries from PATH for the session. The safe idiom is
`for pid in $(pgrep -x msolve); do kill $pid; done` — `-x` matches the exact
process *name*, which a shell running a command line that merely mentions that
name cannot satisfy.

## Silent-lie table

Each returns a plausible wrong answer rather than an error.

| tool | the lie |
|---|---|
| `elim.lib`'s `sat()` (4.3.2) | wrong saturation: `⟨xz⁵, x+yz⁵⟩` → `⟨y⟩` instead of `⟨x,y⟩`. Use iterated `quotient` |
| `continue` in a Singular `for` loop | skips the increment — infinite loop. Use if/else |
| `res` in Singular | reserved identifier |
| `deg()` on a **number** in a parameter ring | always 0 regardless of parameter degree. Use `pardeg()` |
| `eliminate(I, y)` as a geometric-degree test | returns the eliminant in `x` alone; `(x, y²)` gives degree 1 while the fibre has 2 points. Use `vdim` |
| **sympy standard-monomial counting** | `Poly(g, x, y, z).monoms()[0]` is the **lex**-largest monomial, not the grevlex leading monomial. Agreed with Singular in 2 variables by coincidence through Sessions 33–34; in 3 variables it reported generic fibres of Alpöge's map as 12 instead of 3. **Found in Session 36 WP-1.** Use Singular `vdim` |
| sympy `subs(h, 0)` as "reduction mod `h`" | zeroes `h'` too |
| sympy `Integer.__format__` | `TypeError` on f-string specs; wrap in `int()` |

## PDF extraction

`poppler-utils` (`pdftotext -layout`) is the reliable path; `pypdf` fails on
this image with a `cryptography` binding panic, and WebFetch returns raw
FlateDecode streams for arXiv PDFs.
