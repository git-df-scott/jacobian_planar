# L1 executed: the exclusions audited

Full report: `exclusion_audit.md`.  Primary source fetched and text-extracted,
not summarised from abstracts.  Headline results.

## 1. The 125 bound — VERIFIED, exactly

The load-bearing paper is **arXiv:2204.14178**, Guccione–Guccione–Horruitiner–
Valqui, *"Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108"*.  Its Theorem 2.1, quoted from the extracted text:

> If (P,Q) is a counterexample to the Jacobian Conjecture, then we have either
> max{deg(P),deg(Q)} >= 125, or (deg(P),deg(Q)) ∈ {(72,108),(108,72)}.

So "125" is the **larger** of the two degrees, and `(72,108)` genuinely is the
sole numeric survivor below it.  The campaign's targeting is correct on this
point.

## 2. The finding that changes the reading — one orientation is OPEN, by the authors' own admission

Within the numeric pair `(72,108)` there are two Newton-polygon orientations.
The paper eliminates **one** of them, via Corollary 5.7.  Of the other, its own
text says:

> For the other case ... we couldn't solve the corresponding system of
> polynomial equations, thus it is left open.

Two consequences, and they pull in opposite directions:

- **Reassuring for targeting.**  The campaign has been attacking the orientation
  the original authors explicitly could not solve.  It is working on a genuinely
  open problem, not re-deriving something already closed.
- **Sobering about difficulty.**  The four authors who built the entire
  classification apparatus could not solve this system either.  Forty sessions
  of EMPTY here is not evidence of incompetence; it is the expected difficulty.

It also means the phrase "sole surviving admissible pair" is doing two different
jobs: the *numeric* pair is closed by Theorem 2.1, but one of its two
orientations rests on an **unproven gap** rather than a completed exclusion.

## 3. Corollary 5.7 — statement verified, correctness only partially

Statement and proof architecture read.  It reduces to Theorem 5.1 of the same
paper (proof read) **plus an imported Corollary 7.2** from the earlier GGV paper
(arXiv:1401.1784, J. Algebra 471 (2017)), which was **not** independently
re-checked.  **No third-party replication and no erratum found anywhere.**

This is exactly the claim my two sliced `p108` systems test independently — and
those systems turn out to be **torus rank 5**, i.e. positive-dimensional, so the
1800 s TIMEOUTs recorded against them were structural and not resource-bound.

## 4. Nguyen 104 — identified, and a cross-lineage gap

**arXiv:1902.05923**, Thuy Nguyen, *"Some classes satisfying the 2-dimensional
Jacobian conjecture and a proof of the complex conjecture until degree 104"*,
published in *Quaestiones Mathematicae* 48(2), 2025 — so "trusted refereed" is
confirmed.  Two flags:

- possible identity confusion: this Thuy Nguyen may **not** be Nguyen Van Chau,
  whose name attaches to much of the at-infinity literature the campaign uses;
- **GGHV's 2022 paper never cites it**, despite postdating the 2019 preprint.
  The two exclusion lineages appear never to have cross-validated each other.

**Concrete open check, worth doing:** what does "degree" mean in Nguyen's
theorem?  If it is `max(deg P, deg Q)`, then `108 > 104` and `(72,108)` survives
both lineages consistently.  If it is any other reading under which `(72,108)`
falls inside the bound, the two lineages **disagree**, and one of them is wrong —
which would be worth far more than another EMPTY.

## 5. Errata

None found — but with no MathSciNet or zbMATH access in this environment, that
is **"none found", not "none exist"**.

## Net assessment of L1

The `(72,108)` narrowing is structurally sound: the numeric bound is real and
correctly quoted.  But it leans on three layers nobody here — and as far as the
audit could establish, nobody anywhere — has independently re-derived: the
classification paper arXiv:1708.07936, the imported Corollary 7.2 from GGV 2017,
and the raw algebra inside Theorem 5.1.

The campaign is in the right place.  The remaining audit value is concentrated
in (a) the Nguyen cross-check above, and (b) the live independent test of
Cor 5.7 now running.
