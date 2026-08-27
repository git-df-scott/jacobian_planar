# Lead: parameterize the open case by C, not by (P, Q)

## The structural fact (verified here)

For the open (72,108) subcases of GGHV Prop 4.3 the two Newton polygons'
upper corners are exactly proportional with ratio 3/2:

    (12,24) = 1.5 * (8,16)      (12,21) = 1.5 * (8,14)

and the bracket of the two leading corner terms vanishes identically:

    [a x^8 y^16 , b x^12 y^24] = (8*24 - 16*12) ab x^19 y^39 = 0.

So the leading forms commute: l(Q)^2 is proportional to l(P)^3. This is the
(m,n) = (2,3) structure, and it is why GGHV write

    P = C^2 ,    Q = C^3 + alpha C^2 + ... + lambda C^-1 + F

for an approximate root C (a Laurent series in x with coefficients in a
ring of y). It is also, concretely, why the direct (P,Q)-coefficient system
resists solvers: the top-degree equations are identically zero, so the
system is highly degenerate near its leading stratum and the basis
computation spends its memory there. Three memory failures (Singular at
4.2GB, msolve at 4.9GB and 6.5GB) all occurred on the direct formulation,
including after orbit normalization.

## Why the C-parameterization is the right instrument

Unknowns drop sharply: instead of one coefficient per lattice point of
N(P) (25) plus one per lattice point of N(Q) (47), the free data is the
coefficient sequence of a single object C plus a small number of
correction terms. GGHV's own closed cases used exactly this: their D_k
transformation (D_k := C_k * C_3^(5-2k), or C_k y^(2-k) in the (7,21)
case) keeps everything polynomial, and their systems came out at 9
equations, which they then eliminated down to a single relation by hand.

For the case they could not finish, the same reduction applies -- they
simply ran out of computing power at the elimination step in 2022. That
step is a Groebner/elimination problem of a size worth attempting with
current tools, and it is far smaller than the direct system.

## Next steps (in order)

1. Derive the C-recursion for subcase 2 mechanically from P = C^2:
   C_3-k determined from P_6-k and lower C's; verify against GGHV's
   printed D_k formulas as the control (same discipline as f_system.py,
   which derived rather than transcribed and caught a transcription error
   that way).
2. Impose Q = C^3 + lambda C^-1 + F with F's leading data fixed by the
   bracket normalization ([l(P), l(F)] = x^2 fixes F's top coefficient).
3. The resulting system in the D_k coefficients is the target; solve mod
   two primes, then in characteristic zero.
4. Control: run the SAME derivation on the (9,24)/(9,27) case, which GGHV
   closed (their Thm 5.1 / Cor 5.7). Our pipeline must reproduce their
   contradiction. Only then does a verdict on the open case carry weight.
