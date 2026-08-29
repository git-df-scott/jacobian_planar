# NIGHT23 MANIFEST

| artifact | claim | strength | one-command verification |
|---|---|---|---|
| `BRIANCON_STRIKE.md` | exact period verdicts, family degeneration theorem, next target | exact proof plus primary-source geometry | read report and run commands below |
| `briancon_period23.py`, `briancon_period23.json` | \(g,g'\) have a nonzero holomorphic Gelfand--Leray form on the compact genus-one fibre \(t=1\) | `EXACT-ALL-DEGREES` over \(\mathbb Q\) | `python3 night23/briancon_period23.py` |
| `verify_briancon_period23.py` | independent reconstruction of both function-field identities and all three infinity valuations | exact independent checker over \(\mathbb Q\) | `python3 night23/verify_briancon_period23.py` |
| `family_boundary23.py`, `family_boundary23.json` | \(b\ne0\) retains the holomorphic obstruction; \(b=0\) has reducible zero fibre; exceptional \((-1,0)\) is exactly unimodular/non-coordinate | exact algebra and exact Bezout/SY certificates | `python3 night23/family_boundary23.py` |

Combined verification:

```bash
python3 night23/briancon_period23.py && \
python3 night23/verify_briancon_period23.py && \
python3 night23/family_boundary23.py
```

No numerical or modular verdict is promoted.  No counterexample is claimed.
