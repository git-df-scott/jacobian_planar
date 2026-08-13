# Track C — master identity + Phase-4 realization

Status: IN PROGRESS (skeleton created; sections fill incrementally).
Standard: exact arithmetic over Q (sympy Rational / Fraction). No floats anywhere.
Certified inputs trusted per Track F regression: Session 7 Belyi data
(h0 = (1664 - 832 i sqrt3)/3), Session 10 cubic coefficient
n3 = (-128 + 64 i sqrt3)/3, and h0 = -13 n3. Sessions 9, 11-18 prose claims are
UNCERTIFIED inputs; the C1 re-derivation below is their independent test.

## C1 — the endgame master identity (Session 19 claim), re-derived from scratch

Claim under test: in the (q,v) chart with boundary valuation vector -k(b,a) for
cusp type (a,b) ((a,b)=(2,3), k=3, D=13 in Borisov's First Framework), the
[q^D] block of the Keller condition equals

    g0^(a+b) * ( k R' + D R (log g0)' ),

with the chart slope rho provably absent, and with g0 = alpha (v+1)^m v^sigma
the order-matching relations

    D = (a+b) k + 1 - rho        and        (a+b) sigma = 1 + rho - rho^2.

Sub-claims to verify:
- [ ] C1a chart factor det d(q,v)/d(x1,x2) = -x2^3/v^3 (Sessions 16-18), and its
      generic-(rho,s) form
- [ ] C1b in-chart Keller form J_(q,v) = -c q^-3 v^-6 (and generic form)
- [ ] C1c the master identity, fully symbolic (generic a,b,k,D, generic g0, R,
      generic subleading tower), rho-absence
- [ ] C1d order-matching relations derived, sigma = -1 DERIVED for rho = 3
- [ ] C1e (99,66) specialization alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c
- [ ] C1f cross-epoch reproduction of h0 = -13 n3 from the identity + certified
      near-miss data

Verdict: PENDING

## C2 — the ten forced R's at (72,108)

- [ ] Derive actual D(k) from C1 relations (test the handoff guess D = 3k+4)
- [ ] Pole order p = (a+b)m - 1 forced (derive from ODE local analysis at U=0)
- [ ] Solve the ODE for S (deg-4 polynomial) for k = 3..12; uniqueness up to scalar
- [ ] Check handoff k=3: S = 243v^4 - 81v^3 + 54v^2 - 42v + 35, c = -455

Table: PENDING

## C3 — k=3, D=13 realization layer at (72,108)

Method: impose the Sessions 10-13 chain/boundary structure (chain <=> W-block
vanishings; sqrt-reduction; divisibility ladder; boundary rigidity g0 = alpha U^m v^sigma)
and decide whether the forced R (pole order 4 at U=0, certified via S(-1) = c != 0)
extends to a boundary-compatible jet or hits an obstruction. Exact certificate either way.

Verdict: PENDING

## C4 — admissible (rho, m) lattice beyond (3,1)

Constraints: sigma = (1 + rho - rho^2)/(a+b) integral; positivity; D = (a+b)k + 1 - rho >= 1.
List of unexamined slices: PENDING

## Discrepancy log

(every mismatch vs the handoff gets a line here)

## Final verdicts

PENDING
