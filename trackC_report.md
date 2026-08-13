# Track C — master identity + Phase-4 realization

Status: IN PROGRESS (skeleton created; sections fill incrementally).
Standard: exact arithmetic over Q (sympy Rational / Fraction). No floats anywhere.
Certified inputs trusted per Track F regression: Session 7 Belyi data
(h0 = (1664 - 832 i sqrt3)/3), Session 10 cubic coefficient
n3 = (-128 + 64 i sqrt3)/3, and h0 = -13 n3. Sessions 9, 11-18 prose claims are
UNCERTIFIED inputs; the C1 re-derivation below is their independent test.

## C1 — the endgame master identity (Session 19 claim), re-derived from scratch

STATUS: COMPLETE. Executable: trackC_master_identity.py — 29 PASS, 0 FAIL,
all exact (sympy symbolic / Q(i sqrt 3)).

Claim under test: in the (q,v) chart with boundary valuation vector -k(b,a) for
cusp type (a,b) ((a,b)=(2,3), k=3, D=13 in Borisov's First Framework), the
[q^D] block of the Keller condition equals

    g0^(a+b) * ( k R' + D R (log g0)' ),

with the chart slope rho provably absent, and with g0 = alpha (v+1)^m v^sigma
the order-matching relations

    D = (a+b) k + 1 - rho        and        (a+b) sigma = 1 + rho - rho^2.

Derivation re-built from scratch (not copied): with v = x1 x2^s - 1,
q = x2/v^rho, write y2 = F = q^{-ka}(g0^a + q G1 + ...) and
y1 = F^{b/a} + Delta, Delta = q^{-kb+D}(g0^b R/a + q u1 + ...) (D = chain
degree, R DEFINED by the deviation's first block). J(F^{b/a}, F) = 0
(root part Jacobian-silent, certified), so J(y1,y2) = J(Delta, F), whose
leading block is (D-kb) u0 G0' + ka u0' G0 = g0^{a+b}(k R' + D R (log g0)').

Sub-claims verified:
- [x] C1a chart factor det d(q,v)/d(x1,x2) = -x2^s v^-rho for GENERIC (rho,s);
      rho=s=3 gives the Sessions 16-18 -x2^3/v^3. PASS.
- [x] C1b J_(q,v) = -c q^-s v^{rho(1-s)} (generic; via certified chain-rule
      multiplicativity); rho=s=3 gives -c q^-3 v^-6. PASS.
- [x] C1c the master identity, FULLY SYMBOLIC a, b, k, D, generic g0, R,
      generic subleading tower: block == g0^(a+b)(k R' + D R (log g0)').
      Subleading tower provably absent from the block; chart slopes rho, s
      provably absent from the identity (they enter only the order matching).
      Cross-checked at concrete (a,b) = (2,3),(3,5),(2,5),(4,7). PASS.
- [x] C1d order matching DERIVED:  q-side  D = (a+b)k + 1 - s ;
      v-side (g0 = alpha (v+1)^m v^sigma)  (a+b) sigma = 1 + rho - rho*s.
      REFINEMENT vs the handoff: the handoff's relations are the special case
      rho = s (both chart slopes equal); the D-relation involves ONLY s, and
      rho enters ONLY through sigma. For rho = s = 3, a+b = 5: sigma = -1
      DERIVED. Pole forcing: exact (v+1)-order of the block is
      (a+b)m - p - 1 off resonance, so c != 0 forces the exact pole order
      p = (a+b)m - 1 of R at v = -1 (resonance Dm = kp impossible when
      k does not divide Dm — true for every case used below). PASS.
- [x] C1e specialization (2,3,3,13), g0 = alpha(v+1)/v:
      block = alpha^5 (v+1)^4 (3v(v+1)R' - 13R) / v^6, so Keller <=>
      alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c. Reproduces Sessions 16-18
      exactly (their identity + their chart factor + their J_qv form). PASS.
- [x] C1f cross-epoch: (i) h0 and n3 recomputed from the Session-7 Belyi
      p, r: 2p'rw - p(r+3wr') == h0 constant, N = p^2 - w r^3 cubic,
      n3 = (-128+64 i sqrt3)/3, and h0 == -13 n3 EXACTLY. (ii) the
      near-miss in-chart is y1 = (v+1)^3 q^-1 v^-3 p(1/q),
      y2 = (v+1)^2 q^-1 v^-2 r(1/q) (composition verified), its DIRECT
      (q,v)-Jacobian is h0 (v+1)^4 q^-3 v^-6 (single block), its cusp
      function is W = (v+1)^6 v^-6 (n3 q^-5 + n2 q^-4 + n1 q^-3 + n0 q^-2)
      — the 13 chain blocks q^-18..q^-6 vanish identically and R = n3.
      (iii) the identity applied to R = n3 predicts block -13 n3 (v+1)^4 v^-6;
      the direct block is h0 (v+1)^4 v^-6: the identity EXPLAINS h0 = -13 n3.
      Track-F-certified anchors reproduced end-to-end. PASS.

Verdict: C1 VERIFIED (with the rho-vs-s refinement noted above).

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
