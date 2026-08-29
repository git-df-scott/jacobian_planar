# NIGHT21 MANIFEST

| artifact | claim | status | verification |
|---|---|---|---|
| `POLE_THEOREM.md` | finite poles of a rational mate are fibre components; all irreducible fibres force polynomialization; full mixed-isobaric no-mate theorem | exact proof over an algebraically closed characteristic-zero field | read proof; run checker below |
| `pole21.py` | checks night19 rational mates, whole-fibre cancellation, the mixed-weight operator, top-term obstruction, and the squarefree criterion | exact rational/symbolic arithmetic | `python3 night21/pole21.py` |
| `eigensearch21.py` / `eigensearch21.json` | direct construction search via `[P,A]=P`: 6,065 sparse `A`, 188 with eigenvectors, 2,898 exact unimodular eigenpolynomials | exact rational linear algebra; the recorded zero-fibre checks are explicitly unavailable in this environment | `python3 night21/eigensearch21.py` |
| `make_eigenfactor21.py` | generates factor/coordinate certificates for every unique `P` in the construction sweep | exact factorization over Q using SymPy; certificate generation only | `python3 night21/make_eigenfactor21.py` (requires SymPy 1.14) |
| `eigenfactor21.json` / `verify_eigenfactor21.py` | all 2,835 unique hits are either explicitly reducible (2,755) or triangular coordinates with an explicit mate (80); no CE survives | exact rational certificate verification independent of SymPy | `python3 night21/verify_eigenfactor21.py` |

No numerical or modular calculation is promoted to an exact theorem.  No
counterexample is claimed.
