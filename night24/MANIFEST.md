# NIGHT24 MANIFEST

| artifact | claim | strength | one-command verification |
|---|---|---|---|
| `CUSP_CLOSURE.md` | maximal practical family, empty elliptic de Rham-zero locus, complete submersion locus, rational pole mismatch, next divisor type | exact proof | read report and run both commands below |
| `cusp_family24.py`, `cusp_family24.json` | symbolic support/lift derivation; formal eigenprimitive and factorization identities; exact sample certificates | `EXACT-ALL-DEGREES` | `python3 night24/cusp_family24.py` |
| `verify_cusp_family24.py` | independent sample reconstruction, bracket/Bezout/factor checks, support enumeration, three pole constants | exact independent checker | `python3 night24/verify_cusp_family24.py` |

Combined verification:

```bash
python3 night24/cusp_family24.py && \
python3 night24/verify_cusp_family24.py
```

No numerical or modular claim appears.  No counterexample is claimed.
