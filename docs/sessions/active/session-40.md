# **Path C — Build the Map From Its Tear**

**Session 40\.** **This is the only route in the campaign that constructs rather than excludes.**

---

## **The inversion**

Thirty-eight sessions have started from `(P,Q)` and asked what constrains it. Every one ended empty. This starts from the **non-properness set** and asks which maps could produce it.

The reason to do it now rather than earlier is that three pieces landed only recently:

* **T7 is proved** (Session 37), not merely consistent with one example: `Σ δᵢνᵢ = d − χ(C_L)`.  
* **The census gives a target profile** (Session 38): Alpöge's map has `r = 1`, `ν = 2`, `S_F` a single quartic, monodromy the full symmetric group, **origin inside `S_F`**.  
* **Path A's descent** exhibits a plane non-injective map whose Jacobian vanishes on a line, with one of its two colliding points **on that line** — the first concrete instance of tear-and-degeneracy coinciding in the plane.

---

## **The constraint system**

All `[LIT-READ]` except T7 which is `[PROVED-S37]`. Every one is a hard condition on `S_F`.

| Source | Condition |
| ----- | ----- |
| Keller \+ non-proper | `S_F` is a nonempty curve; a counterexample must be non-proper |
| **F2** (Chau Thm 1.2 \+ Keller) | every dicritical has `a_φ = b_φ = 0` — both coordinates converge to finite values along every escaping branch |
| Chau / Abhyankar–Moh | `deg p_φ : deg q_φ = deg P : deg Q`; **no component of `S_F` is isomorphic to `C`** |
| **F3** (McKay–Wang §2) | component equations are `h^q` with Newton polygon the full triangle and leading form `±[u_n^{m/g}W^{n/g} − v_m^{n/g}Z^{m/g}]^g`. For ratio 3:2: `(α²W³ − β³Z²)^M + lower` |
| **T7** | `Σ δᵢνᵢ = d − χ(C_L)`, with `C_L = {αP+βQ=γ}` smooth since `∇(αP+βQ) = (α,β)·JF ≠ 0` |
| Jelonek | `deg S_F ≤ (deg P·deg Q − d)/min(deg P, deg Q)` |
| Euler filter | `χ(F⁻¹(S_F)) ≡ 1 (mod d)` |

**Note what F2 kills.** Session 34's model examples `(x,xy)`, `(y,xy+x)`, `(x²y+x,y)` all tear by having one coordinate blow up — precisely the case Keller forbids. Correction \#12. Do not reuse any intuition built on them.

---

## **Procedure**

### **C1 — Enumerate `S_F` at `d = 2` `[2 days]`**

`r = 1` is now known to be possible (Alpöge, and T8 is refuted). At `d = 2`, T7 reads `2δ₁ = 2 − χ(C_L)` for `r = 1`, `ν₁ = 2`. Combined with F3's pinned leading form and Chau's "no component isomorphic to `C`", the configurations are finite and small.

For each configuration ask: **does a Keller map with this non-properness set exist?** Two attacks:

* via the covering it determines — the monodromy is `Z/2`, factoring through `H₁(C²∖S_F) = Z^r`, so the double cover is `z² = ∏_{i∈J} hᵢ(u,v)` with the `hᵢ` supplied explicitly by F3;  
* directly, solving for `(P,Q)` with prescribed behaviour at infinity.

### **C2 — The `d = 2` pincer `[1 day, run against C1]`**

Session 33 proved independently that `d = 2` requires a **fixed-point-free volume-preserving birational involution of `C²`**, that de Jonquières and linear Bayle–Beauville types are eliminated, and that only **Geiser** (fixed quartic, genus 3\) and **Bertini** (fixed sextic, genus 4\) remain.

These two routes constrain the same object from opposite directions. **Cross them.** Each `S_F` configuration surviving C1 determines a double cover and hence a candidate deck involution; check it against the Geiser/Bertini classification. Each Bayle–Beauville type determines a fixed curve; check its image against C1's admissible `S_F`.

The known risk `[CAMPAIGN]`: Bayle–Beauville's fixed curve is the *normalized* one, a birational invariant on a resolution, so under conjugation it can be contracted and hide over an indeterminacy point. **C1's `S_F` is not birational-invariant and does not have that hole** — which is exactly why crossing the two is worth more than either alone. If the pincer closes, `d = 2` closes outright, and the campaign record calls that its largest available single result.

### **C3 — `d = 3`, with the census profile `[3 days]`**

Alpöge sits at `d = 3`, `r = 1`, `ν = 2`, monodromy `S₃`. **Look for the plane analogue of exactly that profile.** `G = ⟨conjugates of the meridians⟩ ≤ S₃` transitive; `r = 1` with `ν = 2` means one transposition class generating `S₃` — the correct reading of T6's failure, established in Session 37\. T7 gives `2δ₁ = 3 − χ(C_L)`.

Cyclic `G` gives an explicit cover `z^d = ∏hᵢ^{εᵢ}`; `S₃` gives the degree-3 cover with its quadratic resolvent. Both are constructible.

### **C4 — Read Orevkov before day five `[half a day, do first]`**

Orevkov, *Counterexamples to the "Jacobian conjecture at infinity"*, Proc. Steklov Inst. Math. **235** (2001) 173–201. It bounds how far any at-infinity argument can be pushed. **This route is entirely an at-infinity argument.** If Orevkov's constructions show the at-infinity data is realisable without the map existing, C1–C3 produce candidates that cannot be completed, and you need to know that on day one rather than day five.

---

## **Success / abort**

**Success.** Either an explicit `S_F` configuration is realised by a Keller map — run §7 HIT protocol, do not skip a step — or `d = 2` closes via the pincer, removing the case where a counterexample would be easiest to find.

**Abort.** If Orevkov shows the at-infinity data underdetermines the map to the point where every configuration is realisable-in-principle but uncompletable, stop at C4 and record why.

**Deliverable.** `certifiers/session40_pathC_tear.py`; a table of `S_F` configurations at `d = 2, 3` with realisability status.

---

## **Honest odds**

A counterexample: **low**, but this is the only generative route with **no polynomial-degree ceiling** — it is Newton-polygon and covering-space combinatorics, which is the wall every computational session has hit and this one does not.

Closing `d = 2`: **good**, and it is the campaign's largest available result after the bound to 125\.

