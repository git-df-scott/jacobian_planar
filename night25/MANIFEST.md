# NIGHT25 MANIFEST

| artifact | claim | strength | one-command verification |
|---|---|---|---|
| `PRIMITIVE_FIRST.md` | Models A/B impossible by degree-two Galois obstruction; minimal live cubic primitive | exact proof + classical theorem | read report; run combined command below |
| `primitive_first25.py`, `primitive_first25.json` | exact curve, differential, symplectic quotient, bracket and degree data | exact rational arithmetic | `python3 night25/primitive_first25.py` |
| `verify_primitive_first25.py` | independent resultants/discriminants and quotient bracket checks | exact independent checker | `python3 night25/verify_primitive_first25.py` |

Combined verification:

```bash
python3 night25/primitive_first25.py && \
python3 night25/verify_primitive_first25.py
```

No numerical or modular claim appears.  The displayed Keller pairs are
explicitly labelled nonfaithful triangular quotient controls.  No
counterexample candidate is claimed.
