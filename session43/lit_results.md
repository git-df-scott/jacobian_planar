# Literature check results (2026-08-22)

## TASK 1: arXiv:2608.00222 (Path E abort-check E1)

**Paper EXISTS and is fetchable.**
Title: "Counterexamples to the Jacobian conjecture in dimensions greater than two"
Author: Shuhong Gao. arXiv:2608.00222.

Abstract (as returned by fetch, verbatim): "The Jacobian conjecture, open since 1939, asks whether every polynomial map of C^n whose Jacobian determinant is a nonzero constant must have a polynomial inverse. It was refuted in dimension three by Alpöge on July 19, 2026, with an infinite family by Gallagher (July 20) and a geometric explanation by Speyer (July 23): the counterexample sweeps the tangent lines of a plane curve --- a map that classical duality forces to hit most points several times. We give a self-contained account of this tangent-sweep mechanism and generalize it from plane curves to direction fields on hypersurfaces. The resulting construction produces counterexamples in every dimension greater than two and, in each dimension, of arbitrarily large geometric degree (the number of preimages of a typical point). We work it out in five new explicit maps: one three-dimensional of degree four, two four-dimensional of degrees five and ten, and two five-dimensional of degrees six and twelve. The counterexamples provide explicit examples of etale coverings C^n -> C^n that are not proper: they are everywhere unramified, and fail to be injective only through points escaping to infinity. All identities were verified in exact rational arithmetic; an appendix determines exact fiber structures through Gröbner bases."

### (a) Mechanism
VERDICT: YES — it is explicitly the tangent-sweep mechanism, generalized. The paper self-describes as "a self-contained account of this tangent-sweep mechanism," generalized "from plane curves to direction fields on hypersurfaces." Core form (per HTML fetch of v1): a "padded sweep"
  F0(x, gamma, w) = (gamma*x, X(w) + gamma*Delta(w))
with tangency criterion det(Delta, J(X)) = 0, then det J(F0) = gamma * det(Delta, J(X) + gamma J(Delta)) = sum_k L_k gamma^{k+1}; after monomial conjugation + twisting by divisibility, constant Jacobian is achieved. So: same family as "Phi = sum s^i C_i(t)" tangent-sweep generalization — NOT a different mechanism.

### (b) Arbitrary geometric degree; d=2?
Geometric degree = number of roots of a "tangency polynomial" W_{X,Y}(w) = q(w) + (w/2)(X - p(w)) - Y; sweeping a plane curve of degree d gives tangency polynomial of degree d+1, hence generic fiber d+1. Degree grows by taking higher-degree base curves / direction fields. d=2 does NOT occur: the fetch reports the paper notes degree-2 (geometric degree 2) is impossible — consistent with the classical fact that a Keller map of geometric degree 2 would be invertible (and Wang's deg<=2 theorem is cited in this connection). [CAVEAT: the "no d=2" reasoning was paraphrased by the fetch model; the cited reason (Wang) concerns algebraic degree <=2 of the map, not geometric degree — treat the precise exclusion argument as UNVERIFIED wording, but the paper's explicit examples start at geometric degree 3 (Alpöge) / 4 (this paper's 3D example).]

### (c) C*-equivariance
The paper's construction carries an explicit weighted/graded discrete-data structure (weights d_j on parameters w_j, twist exponents e_i on outputs, monomial degrees m_j on source variables, with sum_j m_j = sum_i e_i and sum_j d_j + (k+1) = sum_i e_i). Fetch reports "explicit weighted structure, though not global homogeneity." I could NOT verify a verbatim claim of C*-equivariance of the final maps; treat as LIKELY graded/quasi-equivariant by construction but UNVERIFIED as a stated theorem.

### Explicit small member (3D, geometric degree 4, Theorem 3.5 per fetch)
G = (gamma*x, (p(w) + 2*gamma)/(gamma*x)? ...) — as reported by the fetch:
  G = ( gamma*x,  (p(w)+2gamma)/(gamma x),  (q(w)+gamma w)/(gamma x)^2 )^T
with
  p(w) = w^3 - 6w^2 + 6w
  q(w) = (3/8)w^4 - 2w^3 + (3/2)w^2
  gamma = 2 - 4xy - x^2 z
  w = gamma*(1 + xy)
and det J(G) = 2 identically, geometric degree 4.
**VERIFIED SYMBOLICALLY (sympy, this session): G2 and G3 are genuinely polynomial in (x,y,z) after cancellation, and det J(G) = 2 identically.** This member is safe to feed to the quotient-descent computation. (Expand G2 = cancel((p(w)+2*gamma)/(gamma*x)), G3 = cancel((q(w)+gamma*w)/(gamma*x)^2) with the substitutions above.)

### Alpöge's original map (recounted in Sec. 3.4 of 2608.00222; Theorem 3.3)
  f1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
  f2 = y + 3x(1+xy)^2 z + 3x y^2 (4+3xy)
  f3 = 2x - 3x^2 y - x^3 z
det J = -2 identically. **VERIFIED SYMBOLICALLY (sympy, this session): det J(f) = -2.**
(Announced informally July 19 2026, not as a traditional arXiv paper; Alpöge credited Akhil Mathew with suggesting the problem and Claude with assisting. Gallagher gave an infinite family July 20; Speyer's geometric explanation July 23: "one sweeps the tangent lines of a plane curve — a map that is unavoidably many-to-one, by projective duality." Terry Tao's digestion post exists at terrytao.wordpress.com 2026/07/21 but returned HTTP 403 to this agent's proxy.)

Paper also states (per fetch): "In dimension two, Moh verified the conjecture for maps of degree at most 100; the two-dimensional case remains open."

### TASK 1 VERDICT
(a) YES — arXiv:2608.00222 is explicitly the tangent-sweep mechanism (Alpöge/Speyer), generalized from plane curves to direction fields on hypersurfaces; not a different mechanism. (b) Arbitrarily large geometric degree via higher-degree base curves (tangency polynomial of degree d+1 for a degree-d curve); geometric degree 2 excluded — smallest members have geometric degree 3 (Alpöge) and 4 (Gao's 3D example). (c) Alpöge's map IS C*-equivariant — per arXiv:2607.20210 (Shaska), "equivariant for the grading wt(x,y,z)=(1,-1,-2)" (mixed-sign weights). Gao's family carries explicit weighted discrete data (weights/twist exponents); full C*-equivariance of every member NOT verbatim-verified. One explicit small member extracted and SYMBOLICALLY VERIFIED above (Gao 3D degree-4 map, det J = 2) — ready for quotient-descent.

---

## TASK 2: Is the plane weighted-homogeneous / quasi-homogeneous Keller case a theorem?

**VERDICT: YES for fully graded (C*-equivariant) plane Keller maps — brand new (July 2026); NO theorem found covering the graded-lifting case (top weighted-homogeneous part + free lower terms).**

Decisive citation: **arXiv:2607.20210, T. Shaska, "Graded Keller maps and the Jacobian Conjecture" (July 2026).** Per fetch of the abstract/paper:
- Any dimension, all-positive weights: "an equivariant Keller map is always an automorphism, so no counterexample can be graded that way."
- Dimension two: "In dimension two the same holds for every sign pattern" — i.e., EVERY nontrivially C*-equivariant plane Keller map is an automorphism, for all weight sign patterns. This is exactly the fully quasi-homogeneous plane case: **Path B1's fully-graded case is already a theorem.**
- The paper explicitly notes Alpöge's dim-3 counterexample is equivariant for wt = (1,-1,-2) (mixed signs, dim 3 — consistent with both theorems).
- **NOT covered (per fetch): the graded-lifting case** — top part weighted-homogeneous with unconstrained lower-order terms. No discussion found there, and no theorem found elsewhere in this session covering it. That case remains the open target.

Classical landmarks (context, all about ordinary degrees / Newton polygons, none giving the graded-lifting theorem):
- Magnus (1955): plane JC holds when gcd(deg f, deg g) = 1.
- Nakai–Baba: gcd a prime (and small cases). Applegate–Onishi (1985): gcd = 2p. Combined known set per Moskowicz arXiv:1810.08202 ("A variation on Magnus' theorem and its generalizations"): gcd in {1, 8} ∪ P ∪ 2P implies automorphism (under mild conditions in her generalization). Nagata, "Some remarks on the two-dimensional Jacobian conjecture," Chinese J. Math. 17 (1989) 1–7 (leading-form/Newton-polygon analysis).
- Moh (1983): plane JC for deg ≤ 100. Wang (1980): Keller maps of degree ≤ 2 invertible (any dimension).
- Makar-Limanov, "On the shape of a counterexample to the two-dimensional Jacobian conjecture" (Serdica): further Newton-polygon shape constraints on any counterexample (exact constraints not extracted this session).
- Standard Newton-polygon fact (implicit in the above literature): the top (weighted-)homogeneous parts of a plane counterexample must be algebraically dependent (J(f+, g+) = 0), so "independent weighted-homogeneous tops" cannot occur in a counterexample — but that is a constraint on counterexamples, not an invertibility theorem for graded-lift maps.

CAVEAT / UNVERIFIED: All 2607.20210 statements are from a WebFetch summary of the arXiv page; I could not read the full proofs. Before relying on Path B1 closure, pull the PDF and check the dimension-two every-sign-pattern theorem's exact hypotheses (e.g., whether "equivariant" requires the whole map graded, which weights are allowed to be zero, and whether the base field/constants matter).

---

## TASK 3: Orevkov, "Counterexamples to the 'Jacobian Conjecture at Infinity'", Trudy Mat. Inst. Steklova 235 (2001) 181–210; Proc. Steklov Inst. Math. 235 (2001) 173–201.

From the Math-Net.Ru abstract page: Orevkov constructs "an open complex surface U, a smooth compact rational curve L ⊂ U with self-intersection index +1, and a holomorphic immersion f: U \ L → C^2" which is "meromorphic on U but is not an embedding." Interpretation for Path C: the "Jacobian conjecture at infinity" is the local-analytic strengthening that no such non-injective immersed at-infinity germ configuration (a (+1)-rational curve playing the role of the line at infinity, with a locally-unramified meromorphic extension) can exist; Orevkov shows it CAN — the at-infinity data that a plane JC counterexample would have to realize (resolution/divisor configuration at the line at infinity with an unramified map germ) IS realizable in the holomorphic category. BOUND ON PATH C: purely local/at-infinity obstruction arguments cannot prove the plane JC — any proof (or counterexample-exclusion) must use global polynomiality/algebraicity, not just the structure at infinity. (Exact list of which splice/resolution data he realizes was NOT extractable this session — abstract-level only; the full paper would be needed for the precise realized dual graphs.)


### Dimension-two remark
The paper (per fetch) does not give a 2D obstruction theorem; the mechanism needs the extra "padding" dimension (sweep of a curve family lives naturally in >=3 variables); no analogous construction is claimed in the plane.

