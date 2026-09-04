# Compact restart package

## Do not reopen

- Briançon `g,g'`: `PERIOD-NONZERO / EXACT-ALL-DEGREES` (`night23`).
- Maximal single-cusp preserving family: `EXACT-ALL-DEGREES` (`night24`).
- Primitive models `(R)_inf=2O` and `O1+O2`: degree-two/Galois obstruction
  (`night25`).
- Cubic primitive `v^2=u^3+u+t, R=v`: independent topological-degree
  theorem excludes every faithful degree-3 Keller realization (`night26`).
- All intended degrees 4 and 5: Żołądek's degree-`<=5` theorem (`night26`).
- Degree-six monomial Darboux charts and regular polynomial birational
  intermediate maps: parity and exceptional-divisor obstructions (`night26`).
- Split-quartic affine-modification control `P=2y+x^4y^2`: nonzero
  holomorphic Gelfand–Leray form (`night26`).

## Live frontier

Use exactly

```
t=r^2+2u^2r,  R=r^3,  C_t: w^2=2tr-2r^3.
```

Solve the four-condition rational affine-modification equation in
`CLOSING_STRIKE.md`.  Start with non-toric boundary configurations whose
valuation matrix has determinant one and whose union contains `u=0` and
`r=0`.  Pole cancellation must make both fixed functions `t,R` regular in
the new affine chart.  Do not perform an unrestricted coefficient census.

## Reopen conditions

Reopen JC2 work only if at least one of the following is available:

1. a classification/construction theorem for rational log-symplectic plane
   charts with prescribed Jacobian divisor `u*r^3`;
2. a concrete non-toric affine modification that simultaneously removes the
   axes and keeps `t,R` polynomial;
3. a new obstruction proving no such modification can exist, which identifies
   a structurally different degree-6 divisor configuration;
4. a verified correction or strengthening of the low-degree/nonproper-value
   theorems that changes the live degree or rules out the cusp mechanism.

Merely increasing supports, mate degrees, or primitive degrees is not a
reopen condition.

## Binding CE gate

Require explicit rational-coefficient polynomials, coefficientwise bracket
`1`, original-coordinate polynomiality and faithfulness, a rigorous
nonautomorphism certificate, and a second independent replay.  Anything less
is CEC at most.

