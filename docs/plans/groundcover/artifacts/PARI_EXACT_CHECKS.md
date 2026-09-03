# PARI/GP exact characteristic-zero checks — three items

Engines found: `/usr/bin/Singular` (4.3.2), `/usr/bin/msolve`, `/usr/bin/gp` (PARI/GP 2.15.4,
amd64/GMP-6.3.0). `galdata` is **not** installed (`/usr/share/pari/` holds only `PARI`,
`pari.desc`), so `polgalois` is usable natively only up to degree 7. `/usr/bin/time` is absent;
timings are wall-clock via `date +%s`, plus PARI's own `gettime()` in ms.

Every external computation ran under a hard `timeout 300`.

---

## CHECK 1 — degree-9 bottom-edge eliminant, pentagon case (1)

### 1.1 The archive file does NOT contain an eliminant

`$WT/canon/wave6/bottomedge/be_c2is1_q.out` (3386 bytes) is **not** a rational parametrization.
It is msolve's default **real-root-isolation** output: `[0, [1, [ <3 boxes of 18 coordinate
intervals each, written as bignum/2^k> ]]]`. There is no univariate polynomial anywhere in it.
So the degree-9 eliminant had to be regenerated.

Corroborating archive data (mod p only): `elim_roots.json` records `deg: 9` at
p = 1000003, 1000033, 1000039, 999983 with 5, 4, 5, 4 rational roots; `orbit_data.txt` records
`elim_deg=9` at eight further primes with rational-root counts 5, 4, 5, 3, 3, 2, 5, 6.

### 1.2 Direct char-0 regeneration — BOTH ENGINES TIMED OUT

```
timeout 300 msolve -P 1 -f be_c2is1_q.ms -o be_c2is1_q_P1.out
  -> exit=124 elapsed=300s, output file 0 bytes           [TIMEOUT]

timeout 300 Singular -q check1_sing.sing        (std + vdim + eliminate over Q, dp)
  -> exit=124 elapsed=300s                                 [TIMEOUT]
```

### 1.3 Exact triangular reduction, then msolve — SUCCEEDED

`be_c2is1_q.ms` has 18 variables and 18 polynomials, of which two are the gauge `c1-1`, `c2-1`.
After substituting `c1 = c2 = 1`, sixteen equations remain. Ten of them are linear in a fresh
`d`-variable **with a nonzero integer constant as the leading coefficient**:

```
3*d3 - 2            -> d3      (lead 3)      13*d8 + ... - 17*c7  -> d8   (lead 13)
5*d4 - 5*c3         -> d4      (lead 5)      15*d9 + ... - 20*c8  -> d9   (lead 15)
7*d5 + ... - 8*c4   -> d5      (lead 7)      17*d10 + ...         -> d10  (lead 17)
9*d6 + ... - 11*c5  -> d6      (lead 9)      19*d11 + ...         -> d11  (lead 19)
11*d7 + ... - 14*c6 -> d7      (lead 11)     21*d12 + ...         -> d12  (lead 21)
```

Because every pivot is a nonzero **rational constant** (never a polynomial in the unknowns),
solving for `d3..d12` and back-substituting is an **invertible change of variables over Q**:
no denominators vanish, no component is created or lost, and the variety of the original system
is in graph-bijection with that of the residual system. Clearing the remaining purely-numeric
denominators and taking primitive parts leaves

```
6 equations in c3,c4,c5,c6,c7,c8  — total degrees 5,6,6,6,6,6; 47..73 terms each
                                    (file: resid6.ms, 6276 bytes)
```

A lex Groebner basis of this in sympy timed out at 300 s. msolve did it immediately:

```
timeout 300 msolve -P 1 -f resid6.ms -o resid6_P1.out
  -> exit=0  elapsed=30s          [SUCCESS]
```

The RUR eliminant in `resid6_P1.out` has **degree 9** — matching the mod-p degree recorded at all
twelve archive primes — with coefficients of up to 108 digits.

### 1.4 Exact factorization over Q  (gp, elapsed < 1 s)

```
DEG = 9
content = 1
nfactors = 4
factor_degrees   = [1, 1, 2, 5]
multiplicities   = [1, 1, 1, 1]
deg gcd(f, f') = 0                              -> squarefree
n_rational_roots = 2
  factor 1 deg=1  poly = x
  factor 2 deg=1  poly = 4100*x - 771
  factor 3 deg=2  poly = 12777897437829*x^2 - 5099242904970*x + 513561091708
  factor 4 deg=5
--- Galois groups ---
  factor 3 deg 2 : polgalois = [2, -1, 1, "S2"]
  factor 4 deg 5 : polgalois = [120, -1, 1, "S5"]
--- NEGATIVE control ---
  polgalois(x^5 - 5*x + 12) = [10, 1, 1, "D(5) = 5:2"]   (correctly D5, not S5)
```

### 1.5 Verdict — the retracted claim is refuted, and replaced

**[PROVED-exact]** The degree-9 bottom-edge eliminant splits over Q as

```
        1 + 1 + 2 + 5
```

i.e. **2 rational roots, one quadratic Galois orbit (S2), one quintic Galois orbit (S5)**.
It is squarefree. There is no repeated factor.

The retracted claim — "4 degenerate rational seeds + one degree-5 Galois orbit" — is **false**:
there are **2** rational roots, not 4, and there is an extra quadratic orbit.

This is independently consistent with the mod-p rational-root counts, which is a real check and
not a restatement. Under the correct pattern `1+1+2+5`, the expected number of roots mod p is
`2 + 2*(1/2) + 1 = 4` (a degree-5 S5 quintic has on average exactly one root mod p, by Burnside:
the number of orbits of S5 on 5 points is 1), and the **minimum** is 2. Observed across the twelve
archive primes: 5, 4, 5, 4, 5, 4, 5, 3, 3, 2, 5, 6 — mean 4.25, minimum 2, maximum 6 = 2+2+2.
The retracted pattern `1+1+1+1+5` would force **at least 4** rational roots at every prime; the
observed 2 and 3 are impossible under it. That is exactly the contradiction the archive recorded.

Caveat: the eliminant is msolve's RUR eliminant for a random separating linear form on
(c3..c8), so it is a minimal polynomial of a generic coordinate, not of a named variable.
Its degree, squarefreeness and factor-degree multiset are intrinsic to the point set.

---

## CHECK 2 — case (2), w = -4 block, degree-5 eliminant

### 2.1 Provenance

Located at `$WT/canon/wave4/artifacts/edge_eliminant_Q_one.json`
(keys: chart="one", degree=5, coefficients (6 rationals, monic, ascending), build_primes_used=41,
held_out_primes=[1002361, 1002403, 1002427, 1002433, 1002451, 1002457], factorisation, checks).
Structure summary at `$WT/canon/wave4/artifacts/edge_eliminant_structure.json`.
Clearing denominators from `coefficients` reproduces the integer polynomial stored in
`factorisation` exactly; content = 1. Integer-coefficient digit lengths: 80, 89, 97, 106, 114, 121.

### 2.2 PARI verification (gp, elapsed 0 s)

```
deg = 5
content = 1
lead digits = 80
deg gcd(f,f') = 0                       -> SQUAREFREE
polisirreducible = 1                    -> IRREDUCIBLE over Q
factor degrees = [5] ; nfactors = 1     -> hence NO rational root (deg 5 > 1, irreducible)
disc digits = 806 ; disc sign = 1 ; disc issquare = 0
polredbest(f) = w^5 - w^4 - 9*w^3 + w^2 + 24*w - 18
polgalois(f) = [120, -1, 1, "S5"]
--- NEGATIVE controls ---
polgalois(w^5 - 5*w + 12)        = [10, 1, 1, "D(5) = 5:2"]   (a different group: call is live)
polisirreducible((w^2+1)*(w^3-2)) = 0                          (reducible detected)
```

`disc issquare = 0` is the independent cross-check on S5: a quintic has Galois group inside A5
iff its discriminant is a square. It is not, so the group is not in A5 — consistent with S5 and
inconsistent with A5, F20 (in A5 only when disc is square), D5 or C5.

### 2.3 Label

**[PROVED-exact] for the polynomial as given**: the specific degree-5 integer polynomial in
`edge_eliminant_Q_one.json` is squarefree, irreducible over Q, has no rational root, and has
Galois group S5. These are exact PARI computations on exact integers, with live negative controls.

**Provenance is NOT proved.** The polynomial was obtained by CRT + rational reconstruction from
41 of 96 primes and checked at 6 held-out primes. Its **identity with the true w = -4 eliminant
is only as strong as that held-out-prime check** — it is not a char-0 Groebner result. Everything
above is a theorem about a written-down polynomial, not about the edge variety, until the
reconstruction is confirmed by an exact char-0 solve. Standing label:
**PROVED-exact (polynomial) / modularly-reconstructed (identity)**.

---

## CHECK 3 — degree-1144 case (2) edge eliminant

File: `$WT/canon/wave1/edgeQ_eliminant.txt`, 5,759,664 bytes, a single line, variable `x`.
Loaded into gp with `extern("cat <file>")`.

```
deg = 1144
lc digits = 4666
tc digits = 5192
content == 1      -> primitive
```

### 3.1 Squarefreeness — EXACT, over Q

```
gp: g = gcd(f, deriv(f));
    EXACT deg_gcd_over_Q = 0    ms = 72      [timeout 300 not approached]
```

**[PROVED-exact] f is squarefree over Q.** The full char-0 gcd was cheap (72 ms), so the modular
fallback was not needed. It was run anyway as a corroborating check (p not dividing lc):

```
SQF p=100169  lc_nonzero=1  deg_gcd=0   ms=4
SQF p=100183  lc_nonzero=1  deg_gcd=0   ms=4
SQF p=100207  lc_nonzero=1  deg_gcd=0   ms=4
```

Each of these on its own already implies squarefreeness over Q (deg gcd = 0 mod p with
p not dividing lc(f) forces disc(f) nonzero), so squarefreeness is established four times over.

### 3.2 Dedekind-style factor patterns at NEW primes

Excluded (already in the record): 100003, 100019, 100043, 100057, 100069, 100103, 100109,
100129, 100153. All primes below are strictly larger than every excluded one, hence all NEW.
Every factorization is multiplicity-free (`maxmult = 1`) and every degree multiset sums to 1144.

```
DED p=100169  nfac=4   ms=457  degs=[1, 26, 66, 1051]
DED p=100183  nfac=10  ms=471  degs=[1, 2, 3, 4, 8, 37, 88, 128, 153, 720]
DED p=100189  nfac=9   ms=457  degs=[8, 10, 10, 10, 23, 85, 102, 104, 792]
DED p=100193  nfac=6   ms=466  degs=[1, 3, 4, 21, 60, 1055]
DED p=100207  nfac=6   ms=482  degs=[4, 9, 16, 49, 430, 636]
DED p=100213  nfac=7   ms=465  degs=[1, 1, 3, 4, 4, 75, 1056]
DED p=100237  nfac=5   ms=466  degs=[16, 116, 147, 355, 510]
```

The task asked for 2 new primes; 7 were done because each costs ~0.5 s.

### 3.3 Subset-sum (Dedekind) sieve

Any proper factor of f over Q must have degree that is a subset sum of the mod-p degree multiset,
at every p not dividing lc(f). Intersecting the achievable proper degrees, incrementally, over the
NEW primes only:

```
after p=100169 : 14 candidate degrees survive
after p=100183 :  6 survive  -> [1, 92, 93, 1051, 1052, 1143]
after p=100189 :  2 survive  -> [93, 1051]
after p=100193 :  0 survive  -> []
(remaining primes keep it empty)
```

So the sieve **closes to zero on the fresh primes alone**, by p = 100193. Separately, three of the
new patterns (p = 100189, 100207, 100237) contain no degree-1 factor at all, which excludes a
rational root on its own.

The archive's own 8-prime table (`$WT/canon/wave1/pari/eliminant_modp_degrees.txt`) was re-sieved
independently and also closes to zero, so the two prime sets agree without sharing a prime.

### 3.4 Label

**Squarefreeness: [PROVED-exact]** — `gcd(f, f') = 1` computed over Q in 72 ms, plus three
independent mod-p certificates.

**Irreducibility: strengthened modular evidence, NOT claimed as proved here.** The subset-sum
sieve above is the standard Dedekind argument and it does close, but per the task's instruction it
is reported as evidence and not as a claim: a direct char-0 `polisirreducible`/`factor` on the
degree-1144, 4666-digit-leading-coefficient polynomial was **not** run to completion in this pass,
and the sieve's force depends on the mod-p degree tables being correct (they are exact PARI
`factormod` outputs, computed here for the 7 new primes and taken from the archive for the 8 old).
The honest statement is: **no proper factor degree survives 7 fresh primes**, which is
inconsistent with any nontrivial factorization; independent confirmation by an exact
char-0 factorization remains outstanding.

---

## Timing / status summary

| computation | command | result | wall |
|---|---|---|---|
| char-0 RUR, 18-var bottom edge | `msolve -P 1 -f be_c2is1_q.ms` | TIMEOUT exit 124 | 300 s |
| char-0 elimination, 18-var | `Singular -q check1_sing.sing` | TIMEOUT exit 124 | 300 s |
| lex GB of residual, sympy | `sp.groebner(res, c3..c8, lex)` | TIMEOUT | 300 s |
| char-0 RUR, 6-var residual | `msolve -P 1 -f resid6.ms` | SUCCESS, deg 9 | 30 s |
| factor deg-9 eliminant | `gp -q -f check1_elim.gp` | 1+1+2+5 | < 1 s |
| verify deg-5 quintic | `gp -q -f check2.gp` | irred, S5 | < 1 s |
| exact gcd(f,f') deg 1144 | `gp -q -f check3_exactgcd.gp` | deg 0 | 72 ms |
| mod-p squarefree x3 | `gp -q -f check3c.gp` | deg 0 each | 4 ms each |
| factormod deg 1144 x7 | `gp -q -f check3c.gp`, `check3d.gp` | see table | ~465 ms each |

## Gotchas recorded for reruns

* `gp -q -f script.gp` parsed my multi-line `for(...)` bodies line-by-line and threw
  "syntax error, unexpected end of file"; the loop variable then stayed an unbound t_POL and the
  body silently executed at top level with a **symbolic** `p`, producing plausible-looking but
  meaningless output (`p=p ... deg_gcd=0`). Fixed by putting each loop and function body on a
  single line. Anyone rerunning this must not trust a `deg_gcd` line that prints `p=p`.
* `polrootsQ` does not exist in PARI 2.15.4; use `factor()` and count degree-1 factors.
* `/usr/bin/time` is not installed in this image.
