# night5 ENGINE_VALIDATION — restored control instruments

Executor record. Each instrument was run **as-is** from the restored tree. No
code was edited. The only accommodations were path-level: running each script
from its own directory, and, for the bonus, importing `mckay_wang` as a module to
reach its public functions. Raw console output for every run is in
`night5/validation_out/`.

Environment: Python 3.11.15, sympy 1.14.0 (both instruments that need sympy found
it). Provenance of all three files is the ref `origin/claude/past-code-session-8mdjqn`
at `a301e16`, as recorded in `night5/RESTORE_NOTES.md`.

## Restore gap closed first

`dk_eliminate.py` was already present from TASK A (`campaign_restore/lead4/`).
The other two were **not**: TASK A's request scope for the `session44/` top level
was `*.md` only, so `mckay_wang.py` and `leweber.py` had not been restored. They
were fetched from the same commit `a301e16` into
`night5/campaign_restore/session44/` before this validation, and are included in
this commit. Recording the addition rather than letting the tree quietly change
shape between tasks.

## Summary

| instrument | runs? | control outcome | vs handoff expectation | wall |
|---|---|---|---|---|
| `lead4/dk_eliminate.py` | **RUNS** | CONTROL PASS — GGHV (5.9) reproduced exactly | **MET** | 1.55 s |
| `session44/mckay_wang.py` | **RUNS** | A PASS, B PASS → VALIDATED | **MET** | 0.45 s |
| `session44/leweber.py` | **RUNS** | C1 PASS, C2 PASS, C3 PASS → VALIDATED | **MET** | 0.02 s |

All three run, exit 0, clean stderr. No missing dependencies, no import errors.

---

## 1. `dk_eliminate.py` — RUNS, CONTROL PASS

Run from `night5/campaign_restore/lead4/`. Exit 0, wall **1.55 s**.

The handoff's stated expectation is that it reproduce the published GGHV eliminant
(5.9), `8G^3 + 18 G d1 dm1^6 + 27 d0 dm1^9`, exactly. It did:

```
*** CONTROL PASS: GGHV equation (5.9) reproduced exactly ***
    8*G**3 + 18*G*d1*dm1**6 + 27*d0*dm1**9   (multiplicity 1)
```

Term-by-term against the expected form: `8*G**3` ↔ `8G^3`, `18*G*d1*dm1**6` ↔
`18 G d1 dm1^6`, `27*d0*dm1**9` ↔ `27 d0 dm1^9`. **Exact match, all three terms,
same coefficients.**

The script's own internal control also passed on the way there:

```
CHK1 derived series coefficients vs GGHV printed equations: PASS
cascade solved by substitution: ['dm10', 'dm4', 'dm5', 'dm6', 'dm7', 'dm8']
remaining: 3 equations in ['G', 'd0', 'd1', 'dm1', 'dm2', 'dm3']
R1 done: deg dm2 = 3
R2 done: deg dm2 = 3
final eliminant: 2 irreducible factors
```

So the elimination pipeline is validated against the literature end to end: its
derived series coefficients match GGHV's printed equations (CHK1), and the final
resultant reproduces their published (5.9) as an irreducible factor of
multiplicity 1.

## 2. `mckay_wang.py` — RUNS, both controls PASS

Run from `night5/campaign_restore/session44/`. Exit 0, wall **0.45 s**.

Handoff expectation: detect the Mondello-type char-2 object, and not flag a tame
automorphism. Both held.

**Control A — tame automorphism `f = x + y^2, g = y`:** `det J = 1`, Keller True,
both Newton polygons triangular → verdict `INCONCLUSIVE`, i.e. **not** certified
as a counterexample. **A PASS** — the instrument does not flag a tame automorphism.

**Control B — Mondello char-2 pair:** both polygons non-triangular:

```
N(P) triangular: False  {'k': 4, 'n': 0, 'outside_triangle': [(6, 2), (2, 1)]}
N(Q) triangular: False  {'k': 5, 'n': 1, 'outside_triangle': [(8, 3), (7, 2), (6, 1)]}
```

**B PASS** — the known object is detected as a non-automorphism.
Script's own verdict line: `McKay-Wang certificate instrument: VALIDATED`.

Incidental cross-check: the pair hardcoded in this script's Control B is
character-for-character the pair independently extracted in
`night5/mondello/mondello_map.json` (verified by symbolic difference = 0 in the
bonus run below). That is now a third independent path to the same map — the
arXiv LaTeX, the restored `LIT_MONDELLO_AUG2026.md`, and this instrument.

### Bonus — feeding it the extracted `night5/mondello` pair

`mckay_wang.py` has no CLI for arbitrary input, but exposes `certificate(f, g)`,
`is_automorphism_triangle(f)` and `keller(f, g)`. The pair was rebuilt **from
`night5/mondello/mondello_map.json`** (not retyped, not taken from the script) and
passed to those functions. Wall 0.53 s. Full output:
`validation_out/mckay_wang_bonus_mondello.out`.

The result splits, and the split is worth recording precisely:

- **The polygon test flags it.** `is_automorphism_triangle` returns False for both
  components, with the same off-triangle monomials as Control B →
  "flagged as non-automorphism by the polygon test: **True**". This is the
  expected outcome, and it is what the script's own Control B exercises.
- **The full `certificate()` entry point does not.** It returns **`NOT-KELLER`**,
  because its `keller()` helper computes `det J` **over the integers**:

  ```
  det J = 2*x**13*y**4 - 2*x**12*y**3 + 6*x**11*y**2 - 2*x**10*y - 2*x**9*y**3
          + 4*x**9 - 2*x**7*y - 4*x**6 + 6*x**5*y**2 + 4*x**3 + 2*x*y + 1
  Keller: False
  ```

  a 12-term polynomial, so the constancy test fails and Corollary 14 is reported
  as not applying.

This is a scope limitation of the instrument, not a fault in the object and not
something to repair: `certificate()` is a characteristic-zero entry point, while
the Corollary 14 polygon test it wraps depends only on supports and so is
characteristic-independent. The script's authors evidently knew this — Control B
calls the triangle test directly and never routes the char-2 pair through
`certificate()`.

Recorded as an independent confirmation, from this instrument's own arithmetic:
that same integer `det J`, reduced mod 2, is exactly **1**, matching the
night5/mondello verification.

**Bonus verdict as asked:** the instrument flags the extracted pair via the
Corollary 14 polygon test; its `certificate()` wrapper returns `NOT-KELLER` for
characteristic reasons rather than flagging it.

## 3. `leweber.py` — RUNS, C1/C2/C3 all PASS

Run from `night5/campaign_restore/session44/`. Exit 0, wall **0.02 s**. No
dependencies beyond `sys`.

```
C1 line at infinity has K-multiplicity -3: PASS
C2 free chain multiplicities [-2, -1, 0, 1, 2] (expect [-2,-1,0,1,2]): PASS
C3 satellite(L,E1) multiplicity -4 (expect -4): PASS
multiplicity calculus: VALIDATED
```

All three controls pass, matching the handoff expectation exactly.

The script then prints its sieve applied to free-chain depths (depths 1–2 KILLED,
depths 3–5 SURVIVE). That output is downstream of the controls and is reproduced
verbatim in `validation_out/leweber.out`; no reading of it is offered here.

## Scope

This records that three restored instruments execute and that their own built-in
controls return the values the handoff said to expect. It is a statement about the
instruments, not about any mathematical object they may later be pointed at. The
`dk_eliminate.py` result is an exact symbolic reproduction of one published
equation; the other two are self-consistency controls internal to their scripts.
Nothing here was interpreted beyond comparing outcome to stated expectation.
