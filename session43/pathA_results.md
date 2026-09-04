# Path A results: is the square in det JG forced?

All items marked VERIFIED were checked symbolically in sympy 1.14 (exact polynomial identities,
not numerics). Scripts: step1.py plus inline runs (this directory).

## VERDICT

**FORCED — in the following refined, verified sense.**

- The **h-factor** in det JG is forced: for every C*-equivariant polynomial map whose source and
  target weight quotients are polynomial planes, the verified identity
      det JG ∘ π_src · x^e = det JF · p^{k},   k = m + l' - 1 ≥ 1,   e = n - k
  holds, where f3 = x·p(u,v) (p = the descended equation of h, forced to exist by weights) and the
  target weights are (-m, -l', +1). Since m, l' ≥ 1 for any nontrivial action, **k = 0 is
  unachievable by ANY weight system** unless p is constant.
- The **square** (k even) is an *accident of Alpöge's target weights* (-2,-1,1): k = 2+1-1 = 2.
  Odd exponents occur for other weight systems (k=1 and k=3 exhibited and VERIFIED below). So
  "det JG is c·(square)" is not the invariant statement; "det JG = c·p^k with k ≥ 1" is.
- For a **Keller** F the exponent is pinned: det JF is C*-homogeneous of weight Σw_tgt − Σw_src,
  so det JF = const ≠ 0 forces Σw_tgt = Σw_src, i.e. e = 0, i.e. **k = n = |weight of z|**.
  (Alpöge: n = 2, hence the square.) k=0 would need n=0, a degenerate action.
- The only escape hatch is **p ≡ const**, i.e. f3 = c·x exactly. Then det JG = c^k·D(u,v) with D
  the descent of det JF, so G is Keller iff F is Keller (VERIFIED on a toy). But then x = f3/c and
  expanding det JF along the row (c,0,0) gives det JF = c·det ∂(f1,f2)/∂(y,z): F is a Keller family
  of plane maps over the x-line, and (proof sketch, unverified formally) G is invertible iff F is:
  F invertible ⇒ its equivariant inverse descends to G^{-1}; G invertible ⇒ from T3 = cx recover x,
  then π_src(p) = G^{-1}(T1T3^2-slot, T2T3-slot) recovers (xy, x^n z), hence (y,z) off x=0, so F is
  injective on a dense open set, hence an automorphism. **So the k=0 route yields a plane
  counterexample only if one already has a non-invertible Keller family of plane maps — the
  construction is circular and cannot break the plane case on its own.**

Conclusion for the campaign: the holy-grail "weight system with k=0" does not exist. The correct
statement is not "the square is forced" but "k = n ≥ 1 is forced for Keller F"; parity of k is a
choice of weights, and k=0 degenerates to (parametrized) 2-variable JC.

## 1. Verified identities (Alpöge, weights src (1,-1,-2), tgt (-2,-1,1))

- det JF = -2, det JG = -2(3u+v-2)^2. VERIFIED.
- Descent pairing: **G1∘π_src = f1·f3^2, G2∘π_src = f2·f3** (i.e. π_tgt = (X1X3^2, X2X3) in this
  order; the other order does NOT reproduce the stated G). VERIFIED as exact polynomial identities.
- f3 = x·p(π_src) with p = -(3u+v-2) = -h. Structural reason (rigorous): any monomial of source
  weight +1 under (1,-1,-n) has x-exponent ≥ 1 and quotient invariant. VERIFIED.
- Cauchy–Binet chain rule, VERIFIED for all three column pairs I ⊂ {x,y,z}:
      det JG(π(p)) · minor_I(Jπ_src)(p) = Σ_{|K|=2} minor_K(Jπ_tgt)(F(p)) · minor_{K,I}(JF)(p).
  Minors of Jπ_src = (xy, x^2z): (-2x^2z, x^2y, x^3), gcd x^2.
  Minors of Jπ_tgt = (X1X3^2, X2X3): (X3^3, X2X3^2, -2X1X3^2), gcd X3^2. The target gcd exponent
  m+l'-1 = 2 is the source of the square; substituting f3 = x·p makes the RHS divisible by p^2, and
  dominance of π_src pushes the divisibility down to det JG itself.
- Clean form, VERIFIED symbolically: **det JG ∘ π_src = det JF · p^2** ( = -2·h^2 ).

## 2. Exponent k vs weight systems — five data points (all VERIFIED)

Family: source (1,-1,-n), π_src = (xy, x^n z); target (-m,-l',1), π_tgt = (X1X3^m, X2X3^{l'}).
Generic equivariant toys: f3 = x·p, f1 = y^m r1 + z·x^{n-m} r2 (or z y^{m-n} r2), similarly f2,
with random affine p, q_i, r_i ∈ C[u,v]. In every case descent was exact and

    det JG ∘ π_src · x^{e} = det JF · p^{m+l'-1}   (ratio ≡ 1 symbolically),  e = n-m-l'+1
    (for e<0 the x^{-e} sits on the RHS).

| n | m | l' | k measured | k = m+l'-1 | note              |
|---|---|----|-----------|------------|-------------------|
| 2 | 2 | 1  | 2         | 2          | Alpöge weights    |
| 1 | 1 | 1  | 1         | 1          | **k odd**         |
| 3 | 3 | 1  | 3         | 3          | **k odd**         |
| 2 | 1 | 2  | 2         | 2          |                   |
| 2 | 2 | 2  | 3         | 3          | e = -1 case       |

Degenerate p ≡ const toy (f3 = 2x, src (1,-1,-2), tgt (-2,-1,1)): det JF = 2(2u^3-2uv+2u-1)∘π,
det JG = 8(2u^3-2uv+2u-1) = 2^2·(descended det JF). VERIFIED — confirms k=0 ⟺ p const, and that
then G is Keller iff F is.

Caveats / not verified: only positive source weight w1 = 1 and positive target weight +1 treated;
general (w, -l, -n) with w>1 (fractional-looking exponents k = (m+l'-w')/w') is conjectured
analogous but unchecked. The divisibility-descent step (p^k | det JG∘π ⇒ p^k | det JG, via
dominance of π_src and gcd(p∘π, x)=1) is a standard argument, stated but not machine-checked;
the identity itself, which implies it, IS machine-checked in each case.

## 3. A2: factorization of G — explicit answer (VERIFIED)

**G does factor, but the h^2 splits as h·h, not as Keller∘(h^2-carrier).** Explicitly, with
h = 3u+v-2:

    σ = (A, B) = ( h·(u+1),  h·(2u+3) ),      det Jσ = h            (VERIFIED)
    G'(a,b) = ( a^3 + ab - a^2,  -3a^2 - 2b ),  det JG' = 2(2a-b)    (VERIFIED)
    G = G' ∘ σ                                                        (VERIFIED, exact)
    and h = B - 2A, i.e. (2a-b)∘σ = -h: the second h lives in G'.     (VERIFIED)

- σ is birational: off {b = 2a}, invert via h = B-2A, u+1 = A/h. σ contracts the line {h=0} to
  (0,0) — consistent with the VERIFIED fact that G itself contracts {h=0} to the point (0,0)
  (substituting v = 2-3u gives G1 = G2 = 0 identically), so the critical-value "curve" is a point.
- G' is generically 3:1: eliminating b, its fiber over (P,Q) is a(a^2+2a+Q) = -2P, a cubic in a.
  Hence G is generically 3:1 (σ birational). G is a threefold cover degenerating along one line.
- No factorization G = K∘τ with K Keller was found; the tried candidates σ = (u, h^3)
  (det = 3h^2) fail membership (G1 has H-degrees {2,3}, G2 has {1,2} in H, not multiples of 3),
  and a leading-order obstruction analysis for τ = (c1+h s1, c2+h^2 t2) is *consistent* (the
  needed identity (u+1)(u+2) = ((2u+3)^2-1)/4 happens to hold) but was not pushed to higher order
  — so "no Keller-cofactor factorization" is CONJECTURED, not proven. What IS proven is that a
  natural nontrivial factorization exists and distributes h evenly between the factors.
- Implication of the contraction: G factors set-theoretically through the non-separated quotient
  crushing {h=0}; any right factor τ in a Keller factorization would have to perform the same
  contraction (a Keller left factor is a local iso and cannot contract a curve).

## Files
- /tmp/claude-0/-home-user-jacobian-planar/211fa372-1945-5d1c-89a5-22497f8a4ea2/scratchpad/step1.py — Alpöge verification.
- This file: pathA_results.md.
