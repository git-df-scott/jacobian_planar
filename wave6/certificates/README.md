# Nullstellensatz certificates for pentagon case (1)

Each file is the raw output of Singular's `lift`: the nonzero multipliers
`lambda_i` such that `sum_i lambda_i * F_i = 1` for the corresponding reduced
system. Existence of such an identity is **equivalent** to the variety being
empty over the algebraic closure — so these files *are* the emptiness argument,
and they can be checked without re-running any solver.

| file | prime | system | multipliers | terms | max deg |
|---|---|---|---|---|---|
| `cert_p1000003_92v.txt` | 1000003 | `pentseed/reduced_91v.ms` (92 vars, 209 eq) | 9 | 53 | 5 |
| `cert_p1000039_89v.txt` | 1000039 | `pentseed/reduced_sp1000039_0_88v.ms` (89 vars, 188 eq) | 9 | 53 | 5 |

## How to check one WITHOUT trusting Singular

    python3 wave6/w6_verify_cert.py <system.ms> <certificate.txt>

`w6_verify_cert.py` parses both files with its own parser and re-expands the sum
with its own modular arithmetic — no Singular, no msolve, no sympy. Both
certificates above PASS that check: the expansion collapses to the single
term `1`.

This matters because the certificate was *produced* by Singular; letting
Singular also be the thing that validates it would be one process checking
itself.

## Scope — read this before quoting them

These certificates are **modulo p**. They prove the reduced systems are empty
over the algebraic closure of F_p, at two independent primes. They are **not**
a characteristic-zero proof: that requires the same identity with **rational**
coefficients, expanded exactly over Q. That reconstruction (`w6_cert_lift.py`,
CRT across primes on one fixed Q-system) is the remaining step.

Status: **announced, not closed.**
