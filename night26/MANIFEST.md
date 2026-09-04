# NIGHT26 manifest

| artifact | contents | verification |
|---|---|---|
| `PRIME_DEGREE_AUDIT.md` | primary-source audit; Moskowicz gap; valid degree `<=5` gate | inspect linked theorem statements and hypothesis ledger |
| `CLOSING_STRIKE.md` | degree-six primitive, divisors, field degree, obstructions, remaining equation | run both commands below |
| `closing_strike26.py` | exact polynomial identities, cusp, toric parity, split-quartic control | `python3 night26/closing_strike26.py` |
| `closing_strike26.json` | machine-readable frontier and verdict | read by independent verifier |
| `verify_closing_strike26.py` | independent Jacobian, discriminant, divisor, determinant, degree-witness replay | `python3 night26/verify_closing_strike26.py` |
| `RESTART_PACKAGE.md` | closures, live frontier, CE gate, reopening conditions | documentary |

One-command replay from the repository root:

```bash
python3 night26/closing_strike26.py && \
python3 night26/verify_closing_strike26.py
```

The checkers use exact integer/rational arithmetic only.  No numerical,
modular, residual, or truncated result appears.  No polynomial Keller pair or
counterexample is claimed.

