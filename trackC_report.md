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

STATUS: COMPLETE (OPUS_PLAN P4, mechanical part). Executable:
`python3 trackC_phase4.py c2` — 5 PASS, 0 FAIL, exact over Q.
Artifact: trackC_c2_tenR.json.

- [x] D(k) DERIVED from the C1 q-order matching, not guessed:
      D = (a+b)k + 1 - s = **5k - 2** in the handoff frame (a+b = 5, s = 3).
      **The handoff guess D = 3k+4 is WRONG.** It coincides at k = 3
      (13 = 13) and diverges from k = 4 on (18 vs 16). See the discrepancy
      log — this one is not cosmetic: under the guessed D, the k = 4 slice
      comes back DEAD_resonance, i.e. the wrong relation manufactures a
      spurious death. Under the derived D it is alive with a forced R.
- [x] Pole order p = (a+b)m - 1 = 4 confirmed EXACT, not just an upper bound:
      S(-1) != 0 for all ten instances, verified via the consistency identity
      E(-1) = -(D*m - k*p)*S(-1) = -c.
- [x] ODE solved for k = 3..12: every one of the ten carries a forced R with
      deg S = 4, each passing the exact block check.
- [x] Uniqueness up to scalar for all ten (k never divides D on this range, and
      no pole resonance D*m = k*p occurs), so the scalar is absorbed by
      alpha^(a+b) and the R's are genuinely forced.
- [x] Handoff k = 3 cross-check: our forced S is **identical** to the handoff's
      S = 243v^4 - 81v^3 + 54v^2 - 42v + 35. |c| = 455 agrees; the sign does
      not (ours +455 in the C1e-verified convention, handoff -455) — logged
      below as a convention discrepancy, not a mathematical one.

| k | D = 5k-2 | S (primitive, leading coeff > 0) | c (alpha = 1) |
|---|---|---|---|
| 3 | 13 | 243v^4 - 81v^3 + 54v^2 - 42v + 35 | 455 |
| 4 | 18 | 128v^4 - 64v^3 + 48v^2 - 40v + 35 | 630 |
| 5 | 23 | 625v^4 - 375v^3 + 300v^2 - 260v + 234 | 5382 |
| 6 | 28 | 243v^4 - 162v^3 + 135v^2 - 120v + 110 | 3080 |
| 7 | 33 | 2401v^4 - 1715v^3 + 1470v^2 - 1330v + 1235 | 40755 |
| 8 | 38 | 2048v^4 - 1536v^3 + 1344v^2 - 1232v + 1155 | 43890 |
| 9 | 43 | 19683v^4 - 15309v^3 + 13608v^2 - 12600v + 11900 | 511700 |
| 10 | 48 | 625v^4 - 500v^3 + 450v^2 - 420v + 399 | 19152 |
| 11 | 53 | 14641v^4 - 11979v^3 + 10890v^2 - 10230v + 9765 | 517545 |
| 12 | 58 | 31104v^4 - 25920v^3 + 23760v^2 - 22440v + 21505 | 1247290 |

SCOPE NOTE (not a conclusion — input for C4/Fable). The D-relation
D = (a+b)k + 1 - s carries two unknowns; the table above fixes s = 3, the
handoff frame. Which (rho, s, m, sigma) slices are admissible at all is the
C4 lattice question, which OPUS_PLAN P4 marks Fable-grade and which is
therefore NOT decided here. Every number above is conditional on s = 3.

## C3 — k=3, D=13 realization layer at (72,108)

Method: impose the Sessions 10-13 chain/boundary structure (chain <=> W-block
vanishings; sqrt-reduction; divisibility ladder; boundary rigidity g0 = alpha U^m v^sigma)
and decide whether the forced R (pole order 4 at U=0, certified via S(-1) = c != 0)
extends to a boundary-compatible jet or hits an obstruction. Exact certificate either way.

Verdict: PENDING

## C4 — admissible (rho, m) lattice beyond (3,1)

Constraints: sigma = (1 + rho - rho^2)/(a+b) integral; positivity; D = (a+b)k + 1 - rho >= 1.

STATUS: **INPUTS PREPARED, CONCLUSIONS DEFERRED.** OPUS_PLAN P4 marks C4
Fable-grade ("do NOT attempt conclusions there; prepare clean inputs and
escalate"), so this session ran the enumeration and stopped there. It draws no
verdict about which slices matter.

`python3 trackC_phase4.py c4` — 4 PASS, 0 FAIL, artifact trackC_c4_lattice.json.
What the run produced, as data:

- the admissible (rho, m) slices in the window with, per slice, the k values
  admitting a forced R (e.g. (28,7) admits k in {6, 8, 12});
- 12 slices in the window that are dead for every k = 1..14 — (3,2), (8,4),
  (13,2), (13,8), (18,2), (18,3), (18,4), (18,8), (23,4), (23,7), (28,2), (28,6);
- explicit forced R's (S primitive, c/alpha^5) for the first unexamined
  instances (3,1,k), k = 4..11 — these coincide with the C2 table, which is a
  consistency check between the two code paths, not new information;
- an independent sympy cross-check of a novel instance
  (k, D, m, sigma) = (4, 18, 1, -1): block == const * v^(5 sigma - 1), const = -630;
- the REFINED frame with rho != s allowed (the C1d generalization): the
  integrality condition becomes rho*(s-1) = 1 (mod 5); in the window
  rho, s <= 12 that is 23 slices, 22 of them unexamined. sigma = 0 occurs only
  at (rho, s) = (1, 2), where k*t + D*sigma = 0 at t = 0 forces c = 0.

For Fable: the open question this data poses — which of the 22 unexamined
refined slices are geometrically realizable at (72,108), and whether the
t != 0 branch at (1,2) is live — is exactly the C4 judgment call, untouched
here.

## Discrepancy log

(every mismatch vs the handoff gets a line here)

- **C1d, rho vs s**: the handoff's order-matching relations are the special
  case rho = s. The D-relation involves only s; rho enters only through sigma.
- **C2, D(k)**: handoff guess D = 3k+4 vs derived D = 5k-2. Agree at k = 3
  only. Consequence: the guess makes k = 4 look DEAD (resonance) when the
  derived relation gives it a forced R. Any handoff statement about k >= 4
  slices that leaned on D = 3k+4 must be re-read.
- **C2, sign of c**: handoff c = -455 at k = 3; our C1e-verified convention
  gives c = +455. |c| agrees and S agrees exactly. Convention, not
  mathematics — but it must be pinned before any statement compares a c
  across the two epochs.

## Final verdicts

PENDING
