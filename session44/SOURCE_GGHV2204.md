# Source anchors: arXiv:2204.14178 (GGHV 2022)

"Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108" -- Guccione, Guccione, Horruitiner, Valqui.
PDF: https://arxiv.org/pdf/2204.14178

Extracted text lives only in the session scratchpad (wiped on container
restart), so the passages this campaign depends on are anchored here.

## Theorem 2.1 -- why the search space collapses
"If (P,Q) is a counterexample to the Jacobian Conjecture, then we have
either max{deg(P), deg(Q)} >= 125, or (deg(P), deg(Q)) in
{(72,108), (108,72)}."

## The open case -- their own words
"For the other case with (deg(P), deg(Q)) = (72,108) we couldn't solve the
corresponding system of polynomial equations, thus it is left open."
"With enough computing power we would be able to raise it up from 108 to
125, since there is only one case left."

## Proposition 4.3 -- the two open subcases (our targets)
If there is a counterexample in the case (8,28), then there exist
P, Q in L^(1) with [P,Q] = x^2 and one of:
 (1) N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)}
     N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}
 (2) N(P) = {(0,0),(1,0),(8,14),(8,16)}
     N(Q) = {(0,0),(2,1),(12,21),(12,24)}
Stored as trackD_targets_108.json.

## Section 5 -- the approximate-root method
P = C^2 and Q = C^3 + alpha2 C^2 + alpha1 C + alpha0 + alpha_-1 C^-1 + F.
Prop 5.5: D_k := C_k * C3^(5-2k) is a polynomial.
Conditions: P_-k = 0 for k = 1..8 and Q_-k = 0 for k = 1..5.
Final eliminant (5.9), after eliminating eight d's:
    18 C3^23 d1 (d_-1)^6 F_-4 + 8 C3^69 F_-4^3 + 27 d0 (d_-1)^9 = 0
REPRODUCED EXACTLY by dk_eliminate.py (with G := F_-4 * C3^23):
    8 G^3 + 18 G d1 dm1^6 + 27 d0 dm1^9
Our derivation is independent -- series coefficients derived, their printed
equations used only as checks (CHK1 PASS).

## Theorem 5.1 / Corollary 5.7 -- the control
They prove there is NO pair with [P,Q] = x and
    N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}
    N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)}
This is trackB1_shapes.SHAPES[2] and is the control our branching descent
must reproduce as EMPTY (trackD_targets_ctrl927.json). A verdict on the
open case is not trustworthy unless this control passes.
