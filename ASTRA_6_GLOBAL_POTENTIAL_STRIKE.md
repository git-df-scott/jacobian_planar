# Astra 6 — global polynomial-potential strike

Subsequent result: [Astra 7](ASTRA_7_LIVE_SYSTEMS_CLOSED.md) closes both
degree-14 systems left open below. This file preserves the Astra 6 record.

Date: 2026-09-05. Working branch: `astra/jc2-missed-routes-2026-09-05`.

**Verdict: OPEN.** No polynomial counterexample was found. There is no
arbitrary-degree obstruction for the full collision subalgebra in this
report. Formal conductor lifting is not used or extended.

The exact criterion is now a single differential identity plus two
membership conditions. For a finite polynomial H, put

    g=gcd(H_v,H_c+v).

It yields a collision Keller pair if and only if

    H+2(3cv-2)/3 in B,  g in B,
    (H_c+v)g_v-H_v g_c=g.

The reconstructed second coordinate automatically belongs to B. The
proof, equivalences, low-degree classification and positive/negative
controls are in [GLOBAL_POTENTIAL_THEOREM](astra6/GLOBAL_POTENTIAL_THEOREM.md).

The degree analysis proves structural obstructions with unbounded degree
in c, rather than reporting a finite coefficient box:

- Coprime v-degrees are excluded at once by Newton homothety and even trace.
- Divisible degrees reduce by exact polynomial target shears.
- The remaining (4,6) case is excluded. Its nonsquare-leading-factor branch
  reduces to a rational differential equation and an uncancelled pole;
  its square branch becomes linear on a source line.
- Consequently no passing potential has v-degree at most 13.

The proofs are in [DEGREE_COLLAPSE](astra6/DEGREE_COLLAPSE.md). This is a
partial-degree theorem; it is not a classification of arbitrary potentials.

The first remaining degree range is potential v-degree 14, containing
coordinate v-degrees (4,10) and (6,8). The component attacked further here
is (6,8). Its highest weighted pieces have common root
v(cv-rho), with **rho=2/3 or 4/3**. Both branches must be retained.
The polynomial quadratic-root branch inside B is excluded by a
half-integer valuation contradiction. The same proof excludes rational
roots with even trace, including roots with poles elsewhere. What remains
in (6,8) is a quadratic approximate root with non-even collision trace.

Precisely, normalize P=h^3 v^6+sum_(i<6)p_i v^i, with h having a simple
zero at c=0, and put

    Q=[P^(4/3)]_+ + k4[P^(2/3)]_+ + k2[P^(1/3)]_+.

The unresolved system is

    [v^4]J=[v^3]J=[v^2]J=[v]J=0, [1]J=kappa != 0,

with all coefficients of P,Q polynomial and both trace-parity equations
zero. Every higher Jacobian coefficient cancels identically. The complete
necessary-and-sufficient component reduction, its two leading branches,
the subfamily obstruction and the exact remaining gap are in
[EXCEPTIONAL_68](astra6/EXCEPTIONAL_68.md).

The other component in that degree range is also retained, not silently
excluded: [EXCEPTIONAL_410](astra6/EXCEPTIONAL_410.md) isolates its three
remaining differential equations with the same global regularity and
parity requirements.

Reproduce the exact checks with:

```sh
python astra6/verify_global_potential.py
python astra6/derive_exceptional_system.py
python astra6/derive_quartic10_system.py
python astra6/verify_polynomial_root.py
```

The JSON outputs distinguish symbolic identities from unresolved equations.
The written arbitrary-degree arguments use the cited Newton-polygon and
injectivity-on-a-line theorems. They have not been formally mechanized or
externally reviewed. No computational degree exhaustion is promoted to a
proof, and no remaining equation is reported as solved.
