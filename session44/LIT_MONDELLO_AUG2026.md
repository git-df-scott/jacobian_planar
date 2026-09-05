# New literature surfaced (Aug 2026) — Mondello char-2 CE, and what it means for us

## The paper: arXiv:2608.02634 (Mondello, 29 Jul 2026)

**A Dimension-Two Counterexample to the SEPARABLE Jacobian Conjecture in
Characteristic Two.** Explicit, over k = F2:

    P = x + x^2 y + x^4 + x^6 y^2
    Q = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3

det J = 1; the three points (0,1),(1,0),(1,1) share an image;
[k(x,y):k(P,Q)] = 3, SEPARABLE (so generic degree 3 is prime to
char 2 — not an Artin-Schreier/Frobenius artifact). F is etale but not
an automorphism.

Mechanism (read from the PDF, not the abstract):
- **Hidden cubic**: substituting w = 1 + xQ into a cubic H(w)=0 yields the
  exact identity  Q^2 x^3 + (P^3 + P Q + 1) x + P = 0  — x satisfies a
  degree-3 equation over k(P,Q), capping the generic degree at 3.
- **Descent**: it is a coordinate-permuted plane reduction of Irit
  Huq-Kuruvilla's 3-variable char-2 map G = (x+x^2y, y+xz+x^2yz, z+x^2z^2)
  [HK26], via Phi = tau o G o sigma with sigma=tau=(swap last two coords).

## Why this does NOT give us a characteristic-zero CE (the honest read)

The construction is char-2 to the core: it uses (a+b)^2 = a^2+b^2
(Frobenius additivity) in every simplification, and the source paper's own
Remark 5.2 says the 3-variable construction "does not address dimension
two" in char 0. The separable-JC it refutes is a POSITIVE-CHARACTERISTIC
strengthening; the classical plane JC (char 0) is untouched, as Mondello,
Tao's digestion, and the dim>2 papers all state.

## What we already did about exactly this — and it still holds

session44/mondello_sweep.py was built for precisely this question: does a
Mondello-like separable Keller pair (generic degree g >= 2, p NOT dividing
g) exist at a Newton shape STABLE across two primes? A cross-prime shape =
a bounded-degree family = the certified road to char 0 (an emptiness
certificate has finitely many bad primes; a hit alive at 2+ primes escapes
them).

Result on record (scanlogs/mondello_235.log): p=2 positive control finds
Mondello's g=3 pair; at p=3, 369 Keller pairs / 143 "prime-to-p" fibre
hits; **at p=5, zero prime-to-p hits; CROSS-PRIME SHAPES alive at >=2
primes: [] (empty).**

New this session — exact recheck of a representative p=3 hit
(shape (1,0,6,3,0,2,3), C=2,D=1):
    P = x + 2x^6 + 2x^9 y^3,  Q = y + x^2 + x^5 y^3   over F3
    det J = 1 exactly (Keller, verified by exact bracket)
    fibre histogram over F_27^2: sizes {1,2,3,4,6}, max 6
All non-trivial fibre sizes are DIVISIBLE BY 3 -> generic degree is a
multiple of p -> Frobenius artifact, NOT a separable (prime-to-p) CE.
This is exactly the failure mode the sweep's "prime-to-p" filter and the
cross-prime requirement are designed to reject, and it confirms the
p=3 hits are char-specific noise, not char-0 leads.

## Net

Mondello is a real, important char-2 result and the FIRST plane CE of any
kind — but to a positive-characteristic variant. Our cross-prime sieve
already tested whether its mechanism transfers toward char 0 and found it
does not (no shape survives two primes; the survivors are all p | g). So:
no new char-0 lead here, but a clean external confirmation that the
Mondello route is closed for us, and a new primary source (HK26 +
2608.02634) for the eventual writeup. The char-0 attack stays where it is:
Operation 108 and the F-system/µ-rigidity lane.
