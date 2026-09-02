# **Path D — The Classification Door and the `L = 5` Wall**

**Session 41\. Two blockers that must fall together — neither is worth anything alone.**

---

## **What Session 38 established**

The pipeline is genuinely generic in `L` and the cost model is analytic:

ρ − ρ' \= (2·degC − 1\) − (2·degC − 2 − L) \= L \+ 1        independent of deg C  
U(L) \= (L+1)·\[(L+1)(L+2)/2 − 1\] \+ L                     U(3)=39, U(4)=74, both measured

And two blockers were found, both real:

**Blocker 1 — `L` is not a function of the degree pair.** `(72,108)` gives `L = 3`; `(108,72)` gives `L = 4`. Identical degree arithmetic. `L` is the first coordinate of the base point `B` with `en(P) = 2B`, `en(Q) = 3B`, and `B` comes from `A₀` — the Newton-polygon family produced by GGV's shape analysis, **whose enumeration stops below 125 by construction.** 804 admissible pairs were enumerated with `max ∈ [125,300]`; not one can be assigned an `L`. They can be listed, not ranked.

**Blocker 2 — the constraints stop being quadratic at `L = 5`.**

| `L` | constraint degrees |  |
| ----- | ----- | ----- |
| 3 | 2,2,2 | quadratic |
| 4 | 2,2,2,2 | quadratic |
| 5 | 2,2,2,2,**3** | the `F`\-carrying constraint is cubic |

Gröbner timed out at 1200 s; iterated resultants cleared `d₋₅` and `d₋₄` in 4 s each then stalled on `d₋₃` for 16+ minutes. **Both routes died in the same place because it is a change in shape, not a compute limit.** `L = 4` is the last quadratic case, which retrospectively explains why (8,28) was solvable at all.

**Together these mean the ranking programme has at most two rungs and both are occupied.** Fixing only one blocker buys nothing: polygons above 125 with `L ≥ 5` are unrunnable, and a working `L = 5` engine has no polygons to run.

---

## **D1 — The classification `[the real work, and it is a paper]`**

**Objective.** Extend GGV's shape analysis past `max = 125`, producing `A₀` families and hence `B`, hence `L`, for degree pairs above the current ceiling.

**First, diagnose the termination.** Read `arXiv:1401.1784` and `arXiv:1605.09430` and identify **exactly which step bounds the enumeration.** Three possibilities, with very different consequences:

* a **genuine finiteness theorem** — the families are finite and 125 is where they run out. Then Path D is dead and should be recorded as such.  
* a **computational cutoff** — the method extends but the case analysis was truncated where it stopped being humanly tractable. Then it is mechanisable, and mechanising it is the entire contribution.  
* an **artefact of the bound being proved** — they only needed enough families to reach 125\. Then extension is routine and possibly quick.

**Do this diagnosis before anything else.** It is a reading task of maybe two days and it determines whether Path D is a week or a year.

**Then, if mechanisable:** implement the shape analysis as a program rather than a case analysis. GGV's Cor 7.4, Prop 8.2, and the `ℓ_{ρ,σ}` / `en` / `st` apparatus are already understood well enough in this repo to have reproduced two of their published results from scratch. That is a strong position from which to automate their classification.

### **D1b — Write to Valqui**

The blocker is precisely specified and sits squarely inside GGV's own specialty. What this repo holds and they would want:

* the `L = 4` relation for the case their paper explicitly leaves open — principal, degree 31, 102 terms, uniquely quasi-homogeneous with weights `(2,3,4,5,17)`, total 125  
* the correction `v([P,Q]) = 2v(C) + v(F) − 1`, which reproduces their published Prop 5.2 value at `v(C)=3, [P,Q]=x` and gives `v(F) = −5` at (8,28)  
* a bounds derivation reproducing both (5.10) and Prop 5.6  
* `U(L)` in closed form, and `w(F·W) = 5L − 1 − m`, matching the residual symmetry orders `μ₁₃`, `μ₁₇` computed independently from the chain rule  
* the `L = 5` cubic transition

Thirty-nine sessions solo against a wall one classification result thick, where that result is a paper someone else is better positioned to write. The trade is obvious in both directions.

---

## **D2 — Break the cubic wall `[co-requisite, 3–5 days]`**

**Objective.** Decide `L = 5`. Without this, D1 opens a door onto a room nobody can enter.

The system is **one cubic constraint against four quadratics** in `U(5) = 125` unknowns. That is a much better-posed problem than "Gröbner timed out."

**Attacks, in order:**

1. **Exploit quasi-homogeneity.** The `L = 4` relation had a **1-dimensional weight nullspace**, uniquely pinning the weights from the case's own monomials. Compute the `L = 5` weight vector the same way — from the constraint system before elimination — and use a **matching weighted ordering** rather than `dp`. The Session 36 mitigation list names this and it was never tried, because `L = 4` did not need it.  
2. **Eliminate the cubic last.** Both failed attempts hit the cubic mid-sequence. Clear all four quadratics first (they went in 4 s each), then bring in the cubic against the reduced system.  
3. **`msolve` F4/FGLM.** Installed and verified in Session 36's WP-0, never used in anger. Its advantage over Buchberger-family engines is largest exactly on systems that stall mid-elimination.  
4. **Split by the `y`\-grading** into homogeneous pieces, per the standing mitigation list.  
5. **Predict rather than compute.** `U(L)` was derived analytically, not fitted. Do the same for the relation's degree and order, and get `E(L)` and the ratio `r(L)` **without computing the `L = 5` relation at all.** Session 38 correctly refused to fit `W_tot` on two points; the fix is to derive it. This is hours, not days, and it may make D2's brute-force attacks unnecessary.

**Attack 5 first.** It is cheapest and it is the one that respects the campaign's own rule about fits versus arguments.

---

## **Success / abort**

**Success.** D1 diagnoses the termination and either extends the classification or proves it cannot be extended; D2 decides `L = 5` or derives `r(L)` in closed form. **Both are required for the ranking programme to exist.**

**Abort.** If D1's diagnosis returns "genuine finiteness theorem," record Path D as closed, notify the other paths that the region above 125 is permanently out of reach by this method, and reallocate to Paths A and C.

**Deliverable.** `certifiers/session41_pathD.py`; a note stating the termination diagnosis with the exact citation; `r(L)` in closed form if attack 5 lands.

---

## **Honest odds**

A counterexample from Path D **this session: effectively zero.** This path builds the road; it does not walk it.

But it is the only route to territory nobody has searched, and 804 admissible degree pairs above 125 currently sit unrankable and unrunnable. If both blockers fall, Path D becomes the largest search space in the campaign's history. If either survives, that region is closed by proof rather than by exhaustion — which is itself worth knowing and worth writing down.

