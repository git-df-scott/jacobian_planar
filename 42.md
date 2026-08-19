# **Path E — Is There a Second Mechanism?**

**Session 42\.** **The question nobody in the campaign has asked out loud.**

---

## **The gap in the strongest result**

Sessions 28–32 proved the tangent sweep is unavailable in the plane, at every osculating order, by a one-line argument:

det JΦ \= Σ\_{i,j} j·s^(i+j−1)·det\[C\_i', C\_j\]  
max(i+j−1) with i,j ≤ k  ⟺  i \= j \= k     (UNIQUE)  
⟹ coeff(s^(2k−1)) \= k·det\[C\_k', C\_k\] \= k·W(C\_k)   exactly, all k

Constant Jacobian forces `W(C_k) = 0`, hence constant direction, at every order. And the separation is proved both ways: for `v : C → C²`, `(p/q)' = W(C)/q²` makes degeneracy and constant direction coincide; for `v : C² → C³`, rank `≤ n−1` is strictly weaker, witnessed by `v = ((1+xy)³, 3x(1+xy)², −x³)` with `det[v_x,v_y,v] = 0` but `rank[v,v_x] = 2`.

**This is the campaign's best result. It is also strictly a theorem about sweeps.**

The inference "the mechanism that killed every higher dimension is unavailable in the plane" is only as strong as the claim that **the sweep is the only mechanism.** That claim comes from Speyer's geometric explanation of Alpöge's map, and it has never been checked against the rest of the family. `[GAP — DERIVED-S39]`

`arXiv:2608.00222` produces counterexamples in every dimension `> 2` with **arbitrarily large geometric degree**. Alpöge's has `d = 3`. Nobody has verified that the large-`d` members arise the same way.

---

## **Procedure**

### **E1 — Classify the known counterexamples by mechanism `[2 days]`**

For every member of Alpöge's map, Gallagher's family, and the `arXiv:2608.00222` family, determine whether it is a tangent sweep:

* Is it of the form `Φ = Σ_{i≤k} sⁱ C_i(t)` for some curve family, after a coordinate change?  
* Does the Session 29 top-coefficient identity hold — is `coeff(s^{2k−1}) = k·W(C_k)` recoverable?  
* If not literally a sweep, is it a **degeneration or limit** of one? Sweeps degenerate; the limits need not look like sweeps.

**Sort the family into sweep / non-sweep / undetermined.** This has never been done and it is the load-bearing check under the campaign's headline claim.

### **E2 — If a non-sweep member exists, test it against the plane `[3 days]`**

This is the payoff. A second mechanism is a **second thing to try to port down**, and the sweep proof says nothing about it.

For each non-sweep mechanism, run the two admissibility tests before spending time:

* **Entire-function test.** `F(x,y) = (eˣ, ye⁻ˣ)` has `det JF ≡ 1` and is not injective. If the mechanism would also produce it, the mechanism cannot work in the plane and must use polynomiality — finiteness at infinity.  
* **Dimension-separation test.** Does the mechanism have an argument that distinguishes `n = 2` from `n = 3`? If it does not, either it ports down (and there is a plane counterexample) or the campaign gains a new separator by finding out why it cannot.

**Either outcome is valuable.** A mechanism that ports is the counterexample. A mechanism that provably cannot port is separator number two or three.

### **E3 — The `d` ladder `[2 days]`**

`arXiv:2608.00222` gets arbitrarily large geometric degree. Ask **how**, and whether the construction has a `d`\-lowering direction.

The plane is constrained at low `d`: `d = 1` is an automorphism by Ax–Grothendieck; `d = 2` is nearly closed (Path C); `d = 3` is where Alpöge sits. **If the higher-dimensional family has a natural minimum `d`, and that minimum is above what the plane can support, that is a quantitative separator** rather than a structural one — a new kind, and the campaign has none.

Conversely, if the construction can be pushed to `d = 2` upstairs, ask what happens when the ambient dimension is pushed to 2 simultaneously. The two limits may not commute, and the obstruction to their commuting is the separator.

### **E4 — Cross-reference Path A `[half a day]`**

Path A found that Alpöge's map descends to a plane map with `det JG = −2h²`. **Run the same descent on every non-sweep member found in E1.** If sweeps give `k = 2` and non-sweeps give a different exponent, the descent exponent classifies the mechanism, and it becomes a cheap invariant to compute on any future example.

If any member gives `k = 0`, stop everything and run §7's HIT protocol.

---

## **Success / abort**

**Success.** Either the family is proved uniformly sweep-based — which closes the gap and upgrades the campaign's headline claim from "the mechanism" to "every known mechanism", correctly hedged — or a second mechanism is identified and tested against the plane.

**Abort.** If `arXiv:2608.00222`'s construction is explicitly a sweep generalisation and the paper says so in its first section, E1 is a one-hour reading task and Path E collapses to E3 alone. **Check this before committing the session.**

**Deliverable.** `certifiers/session42_pathE.py`; a table of every known counterexample with mechanism, `d`, descent exponent `k`, and whether the sweep proof covers it.

---

## **Honest odds**

A counterexample: **low**, and lower than Paths A and C.

But this path is the campaign's own **audit**. Every document since Session 32 has asserted that the higher-dimensional mechanism is structurally unavailable in the plane, and every strategic decision since — including the decision to concentrate everything on `(108,72)` — rests on it. That claim has been checked against **one** map.

The campaign's own second rule is to attack your own conclusions adversarially, especially the ones you like. This is the conclusion the campaign likes most, and it has never been attacked.

---

## **Path summary, sessions 39–42**

| Session | Path | Route | Counterexample odds | Other value |
| ----- | ----- | ----- | ----- | ----- |
| 39 | **A** | Quotient descent — the `h²` obstruction | Low, but the search space is objects known to exist | A second separator if the square is forced |
| 39 | **B** | Equivariant search generalized to `μ_n` and graded lifts | Low | Upgrades the Session 38 collapse to a theorem |
| 40 | **C** | Build the map from its tear | Low, no degree ceiling, only generative route | Closes `d = 2` outright |
| 41 | **D** | Classification above 125 \+ the `L = 5` wall | Zero this session | Opens 804 unsearched degree pairs, or closes them by proof |
| 42 | **E** | Is the sweep the only mechanism? | Low | Audits the claim every other decision rests on |

**If you run one: Path A.** It is the only place in the campaign where the object under study is a real counterexample's plane shadow rather than a hypothetical.

**If you run two: A and C.** They meet — Path A's degeneracy line contains one of its two colliding points, which is Path C's tear-and-Jacobian coincidence appearing concretely for the first time.

