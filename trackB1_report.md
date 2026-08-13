# Track B1 report — case (1) pentagons of GGHV Prop 4.3 (the second virgin territory)

STATUS: IN PROGRESS (2026-08-13). Skeleton created at start per checkpoint discipline;
sections fill in as steps complete. If this file looks truncated, the container died —
resume from the last completed section.

Input (hash-pinned): trackA_system_case1.json, 186 unknowns / 302 equations,
sha256 49d28a2fd7ca72eb4064564d02084b2fab1612222d0c2c86b22ee1fe4702be9a.
Nobody — paper, lost sessions, tonight's Track B — has ever attacked this system.

## Plan of record

- B1a: derive (not assume) the top-edge structure: equations on the bracket line
  beta - alpha = 20 are exactly the coefficients of [L_P, L_Q] = 0; prove
  L_P = a*S^2, L_Q = b*S^3 for a single slope-1 form S (5 coeffs), machine-checking
  every identity that can be machine-checked and writing out the one UFD step.
- B1b: substitute the parametrization into the 186/302 system (exact Fractions),
  quotient the 4-dim gauge (A2 torus + S-rescaling mu), run the sound eliminator.
- B1c: mod-p scout (65521 first) of the reduced core via Singular, Rabinowitsch
  ties for every nonzero side condition (incl. transferred ones).
- B1d: per-branch verdicts DEAD / alive-with-structure, with certificates.

## B1a. Derivation of the pentagon top-edge parametrization

(pending — filled by trackB1_pentagon.py --derive)

## B1b. Substituted system + gauge quotient + elimination

(pending)

## B1c. mod-p scout

(pending)

## B1d. Verdicts

(pending)

## Artifacts

- trackB1_pentagon.py — all derivation/build/scout code (subcommands)
- trackB1_param_system.json — substituted, normalized system (built in B1b)
- trackB1_reduced.json — eliminator output tree (B1b)
- trackB1_*.sing / *.out — Singular scout scripts and outputs (B1c)
