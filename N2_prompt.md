
Read the MD file first for full context, then run exactly the task in the prompt below
Task: Test the transfer conjecture from Sessions 16-18 against Borisov's
Second Framework (D=23, target degree pair (435,290)).
CRITICAL SCOPE NOTE (confirmed via arXiv:1901.04073, full text):
Unlike the First Framework, Borisov's paper does NOT publish explicit
Belyi polynomials p(w), r(w) for the Second Framework's (-2)-curve map.
It gives only the ramification data:
- Degree 23 map, ramified above {0}, {1}, {infinity}
- Above {0}: 1 point order 1, 4 points order 3, 2 points order 5
- Above {1}: 1 point order 7, 16 points order 1
- {infinity} is the unique preimage sent there
This means Session 7's work (deriving explicit p, r from a dessin
d'enfant, then certifying via the miracle cancellation deg(p^2-w*r^3))
must be REDONE for this new dessin before any later-session machinery
applies. This is NOT a parameter substitution into the existing
pipeline — treat it as a fresh sub-campaign that reuses the D=13
machinery as a METHOD template, not as a quick numerical check. Budget
your time accordingly across a full session.
Context: Load, in order:
1. D23_transfer_check_context.md (reporting discipline, why this
matters, the two-outcomes distinction)
2. The attached file "sessions_1-18_full.py" (D=13 method template —
Belyi rederivation, chart factor, boundary rigidity, chain layer,
endgame) — treat the D=13 RESULT as ground truth, do not re-derive
it; treat the METHOD as the template to reapply for D=23
3. arXiv:1901.04073 Section 4 ("Second Framework") for the D=23
ramification data and target degree pair (435,290)
PHASE 0 — Belyi rederivation (required before anything else):
1. Report a plan: how to construct the dessin d'enfant for the
degree-23 (-2)-curve map from the stated ramification profile,
and derive explicit p(w), r(w) analogs (or the appropriate
structure — note the D=23 (-2)-curve Belyi map is NOT necessarily
of the same p^2/(w*r^3) form as D=13, since the ramification
profile differs — verify the correct functional form first).
2. Stop and wait for go-ahead.
3. Derive and certify in exact arithmetic, same rigor as Session 7's
ledger (squarefree checks, gcd checks, ramification profile match).
4. Report clearly whether this succeeded, partially succeeded (e.g.
ramification data alone doesn't pin a unique dessin), or requires
assumptions beyond what's stated in the paper.
PHASE 1 — D=23 tower (only if Phase 0 produces certified data):
Rebuild the chart factor, boundary rigidity, chain layer, and
endgame operator for D=23, following the SAME method as Sessions
8-18, using Phase 0's Belyi data as the new foundation. Full
plan-then-checkpoint discipline. Report outcome as DIES / DOES NOT
DIE per the context file's discipline — applies with full force.
PHASE 2 — Isotope series (only if Phase 1 result is DIES cleanly):
Check the isotope series flagged "to be checked" in the Session
16-18 notes. Same discipline: plan, checkpoint, certify, report.
HARD STOP — usage limit:
If the session hits either the 5-hour session limit or the weekly
usage cap at any point:
- Do NOT attempt to continue on a fallback/different model.
- Commit and save all progress exactly as-is, with a clear note
on exactly which phase/step was in progress and what the next
action would have been.
- Report clearly which limit was hit and what checkpoint to
resume from.
This is not a failure state — it's an expected pause point.
Standard discipline: no scope creep beyond Phase 0 → 1 → 2, commit
meaningful progress as you go, be explicit about "mechanism doesn't
apply here" vs. "mechanism applies and doesn't produce a contradiction"
vs. "proved it dies" — a clean DIES result at any phase is a complete,
valuable, publishable finding on its own, not a lesser outcome.


