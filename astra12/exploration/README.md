# Recorded exploratory calculations

These scripts preserve intermediate exact work. They do not certify a full
Keller pair or a complete global-component classification. The authoritative
result and hypotheses are in [Astra 12](../../ASTRA_12_GLOBAL_DIFFERENTIAL_DESCENT.md).

- `cohomology.py`: an early linear differential calculation; its second
  problem imposes additional approximate-root integrality assumptions.
  It is not used to claim an obstruction for all coefficient choices.
- `next_exact.py`: the next meromorphic linear problem, with `L=tau^2`.
  It has 11 free parameters and an admissible particular row with zero
  forcing numerator. That row has not been extended to a finite pair.
- `ansatz.py`: exact universal bracket identity and the divisibility
  rejection for the explicitly restricted polynomial ansatz.

Saved text outputs record these calculations. The principal verifier in
`../verify.py` independently checks the identities used in the final report.
