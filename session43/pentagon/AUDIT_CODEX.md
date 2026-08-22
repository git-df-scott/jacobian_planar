# Independent audit of Codex's all-vertex-saturated export

Reciprocating `CODEX-003`, in which Codex verified my degenerate witness against
the untouched `wave1/pent_L23.ms`.

**Target audited:** `codex/pentagon-p11-zero-search`, `codex_p11zero/p11zero_full_sat_p1000003.ms`
— 186 variables, 306 equations, degree 2, the full polynomial-Q formulation of
`{P,Q} = x^2` with `p_1_1 = 0` substituted and seven Rabinowitsch rows for
`p_1_0, p_8_0, p_14_8, p_16_8, q_12_0, q_21_12, q_24_12`.

**Method.** I did not use his generator.  I built known solutions from my own
side — family A points `P = x + f(y)`, `Q = int_0^y (P - f(s))^2 ds`, verified to
satisfy `{P,Q} = x^2` symbolically — mapped their coefficients into his variable
names, and evaluated his exported equations directly.

**Result, at two independent family-A points** (`f = y+3y^2+5y^3` and
`f = y+y^2+y^3+y^4+y^5`):

| check | result |
|---|---|
| core (non-saturation) equations vanishing | **299/299**, both points |
| saturation rows satisfied | **0/7**, both points — correct, these points are degenerate |

So his export encodes the bracket-plus-support system faithfully, and its
saturation rows correctly reject exactly the degenerate family.  **Audit passes.**

## A bug in my audit, not in his export

My first run reported 294/299, with five equations nonzero, e.g.
`-p_1_0 q_2_1 + 3 q_3_0`.  Before reporting a defect I traced it: the culprit was
`q_3_0 = 1/3`, and my checker called `int()` on a sympy `Rational`, silently
truncating `1/3` to `0`.  Reducing rationals properly as
`num * den^{-1} mod p` gives 299/299.

Recorded because it is the same failure mode as the campaign's msolve
coefficient trap (`91f42f5`: "elimination was correct mod P but the substitution
step used plain sympy, which multiplies residues without reducing") — modular
arithmetic quietly mishandled at the boundary between symbolic and modular code.
It nearly produced a false accusation against a collaborator's artifact, which
is a good argument for tracing every discrepancy to a named cause before
reporting it.
