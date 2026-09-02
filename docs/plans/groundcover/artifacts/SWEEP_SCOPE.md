# AUDIT 1 — scope of "THE SWEEP MECHANISM IS DEAD IN THE PLANE"

Files read in full: `canon/wave6/w6_plane_sweep.py` (190 ln),
`canon/wave6/w6_plane_sweep_search.py` (87 ln), `canon/CATCHES.md` §815–890 and
§1355–1405, plus `canon/wave6/plane_sweep_search.{json,log}`.

**Verdict in one line.** The dichotomy is *correct as stated* but its statement
is narrower than the headline. It is a theorem about sweeps **affine-linear in
gamma**, and branch (a)'s "the twist cannot repair it" is an argument about
**one ansatz** (`w = gamma*u`, `C = gamma*x^s`, five `(i,j)` pairs), not a
general theorem. Nothing above Moh's bound was ever built.

---

## (i) Is S assumed affine-linear in gamma? — YES, explicitly.

The dichotomy's own hypothesis line:

> `CATCHES.md:1382` — `THE SWEEP DICHOTOMY.  For a general plane sweep S(gamma,w) = X(w) + gamma*Delta(w)`
> `CATCHES.md:1383` — `with X, Delta in C[w]^2, direct differentiation gives (verified symbolically)`
> `CATCHES.md:1385` — `        det J(S)  =  det(Delta, X')  +  gamma * det(Delta, Delta').`

"general" here modifies `X, Delta`, **not** the gamma-degree. Every line of code
agrees:

> `w6_plane_sweep.py:58-59` —
> ```
>     S1 = p + 2*g
>     S2 = q + g*w
> ```
> `w6_plane_sweep.py:100-101` — `P = sp.expand(p.subs(w, wexpr) + 2*gam)` / `Q = sp.expand(q.subs(w, wexpr) + gam*wexpr)`
> `w6_plane_sweep_search.py:45-46` — same two lines.

So `deg_gamma(S) = 1` throughout. The claim "NO PLANE SWEEP IS A COUNTEREXAMPLE"
(`CATCHES.md:1401`) is proved only for the gamma-linear family. Section (iv)
below extends it one order.

## (ii) Is branch (a)'s twist rebuttal general? — NO. One ansatz, five (i,j).

Branch (a) in full:

> `CATCHES.md:1389-1394` —
> ```
>  (a) det(Delta, Delta') != 0.  Then det J(S) has positive degree in gamma, so it
>      vanishes on a curve and S is not Keller.  The divisional twist cannot
>      repair this in the plane: with w = gamma*u the twisted Jacobian is
>      u^2 * Psi(gamma,u) * {gamma,u}, and a product of polynomials equal to a
>      nonzero constant forces u to be constant, whence {gamma,u} = 0.
> ```

The first sentence is a theorem (a polynomial of positive gamma-degree is not a
nonzero constant). The rebuttal in sentences 2–3 is conditional on `w = gamma*u`
— the *specific* substitution — and says nothing about a general divisor `C`.
The searched family is even narrower:

> `w6_plane_sweep_search.py:11-13` —
> ```
>     phi : (x,y) -> (gamma, w),   gamma = c0 + a*x^al*y^be,   w = gamma*u,
>                                  u = 1 + b*x^mu*y^nu,        C = gamma*x^s
> ```
> `w6_plane_sweep_search.py:68-74` — `al,be in 0..2` (minus `(0,0)`), `mu,nu in 0..2`, `s in 0..2`, `d in 2..dmax`.

**`C` is never general.** It is always `gamma * x^s` with `s <= 2`
(`w6_plane_sweep_search.py:47`, `w6_plane_sweep.py:150`). A divisor with a
second irreducible factor, or one not divisible by `gamma`, is untested.

**The (i,j) lists are finite and short**, and *three different lists* appear:

| where | `file:line` | list |
|---|---|---|
| Gröbner search (the real run) | `w6_plane_sweep_search.py:72` | `(1,2), (1,1), (0,1), (2,3)` |
| exploratory `search()` | `w6_plane_sweep.py:151` | `(1,2), (1,1), (2,3), (0,1), (1,3)` |
| identity control | `w6_plane_sweep.py:109` | `(1,2), (2,1), (0,1), (3,2)` |
| CATCH 2 circularity check | `CATCHES.md:882` | `(1,2), (2,1), (1,1), (2,3), (3,1)` |

Exponents are all `<= 3`. No general `(i,j)` argument exists anywhere in the
tree. **Branch (a) is rebutted for one shape family, not in general.**

## (iii) The side-condition identity: present, and already known to be vacuous.

Present verbatim, three times:

> `w6_plane_sweep.py:78` — `        det J(F) = C^{-i-j-1} * [ C*{P,Q} - j*Q*{P,C} + i*P*{Q,C} ]`
> `w6_plane_sweep.py:84-85` — `        C * 2*gamma(phi) * det J(phi)  -  j*Q*{P,C}  +  i*P*{Q,C}` / `              =  kappa * C^(i+j+1)                              (SIDE CONDITION)`
> `CATCHES.md:829` and `CATCHES.md:838-840` — the same, called "the object nobody has written down".
> Implemented at `w6_plane_sweep_search.py:49` — `lhs = sp.expand(C*2*gam*detJphi - j*Q*br(P,C) + i*P*br(Q,C) - kap*C**(i+j+1))`.

It is a true identity (`verify_identity`, `w6_plane_sweep.py:104-120`), **and the
archive has already retracted its content**:

> `CATCHES.md:870-878` — `CATCH 2 -- THE TWIST ANSATZ WAS CIRCULAR IN TWO VARIABLES. ... Once the divisibilities hold, write P = C^i A and Q = C^j B; then` / `    C{P,Q} - j Q{P,C} + i P{Q,C}  ==  C^{i+j+1} {A,B}` / `identically ... So the "side condition" says {A,B} = kappa, i.e. "F = (A,B) is a Keller map" -- which is what we were trying to solve.`

**Was anything above Moh's bound built on it? NO.**

> `CATCHES.md:855-861` — `CATCH 1 -- THE SEARCH WAS VACUOUS BY MOH'S THEOREM.  The shape family I launched (gamma = c0 + a x^al y^be with al,be <= 2; u = 1 + b x^mu y^nu with mu,nu <= 2; w = gamma*u; deg p <= 3) produces maps of total degree at most about 32.  Moh proved JC2 for all maps of degree <= 100.`

Degree audit of the only family ever run: `deg gamma <= 4`, `deg u <= 4`,
`deg w = gamma*u <= 8`, `deg p <= 3` so `deg q <= 4` and `deg q(w) <= 32`;
`deg C <= 6`. Max total degree **32 < 100**. The committed artefact confirms the
run never escaped it: `plane_sweep_search.json` holds **501 of 1728 shapes**
(499 `EMPTY`, 2 `LIVE`), every `shape` tuple entry `<= 3` — i.e. killed mid-run
exactly as CATCH 1 says. The two `LIVE` rows are
`shape [1,0,0,1,1,0,1,2]` and `[1,0,0,1,1,0,1,3]` (`plane_sweep_search.log`),
both `(i,j) = (0,1)` inside the degree-32 family, hence Moh-vacuous *and*
subject to the CATCH-2 circularity. **No system with max total degree > 100 was
ever constructed.**

---

## (iv) The generalization: S with a gamma^2 term

`S(gamma,w) = X(w) + gamma*Delta(w) + gamma^2*E(w)`, computed in sympy
(`groundcover/sweep_gamma2.py`, output `sweep_gamma2.out`). det J is **cubic**
in gamma, and every coefficient is a Wronskian-type 2x2 determinant:

```
[gamma^0]  det(D, X')
[gamma^1]  det(D, D') + 2*det(E, X')
[gamma^2]  det(D, E') + 2*det(E, D')
[gamma^3]  2*det(E, E')
```

(all four verified against the hand-derived forms: `matches claim: True`.)
Keller forces coefficients 1,2,3 to vanish and `det(D,X') = kappa != 0`.

**Branch (b)'s collapse does NOT hold verbatim.** The old branch (b) hypothesis
`det(Delta,Delta') = 0` is no longer the alternative to (a): the gamma^1
coefficient is now `det(D,D') + 2 det(E,X')`, so **`Delta` may turn freely** and
have its turning cancelled by the quadratic term. `Delta` is *not* forced
parallel to a constant vector, and the one-line "hence triangular" argument of
`CATCHES.md:1395-1400` fails.

**What replaces it.** Run the vanishing conditions from the top down:

1. `[gamma^3] = 0` gives `det(E,E') = 0`, so `E = k(w)*v` for a constant vector
   `v`; normalise `v = (0,1)`, `E = (0,k)`. (Same lemma as old branch (b), now
   applied to `E`.)
2. `[gamma^2] = 0` becomes `D1*k' - 2*k*D1' = 0`, i.e. `k = c*D1^2`
   (verified: substituting `k = c*D1**2` gives `0`). *This is new — it is a
   Riccati-type link between `E` and `Delta`, absent at gamma-degree 1.*
3. `[gamma^1] = 0` becomes `D1*D2' - D2*D1' = 2c*D1^2*X1'`, i.e.
   `(D2/D1)' = 2c*X1'`, so `D2 = D1*(2c*X1 + e)`. All three coefficients then
   vanish identically (verified: `0, 0, 0`).
4. `[gamma^0] = -D1*(2c*X1*X1' + e*X1' - X2') = kappa`. A **polynomial factor of
   a nonzero constant**, so `D1 = d1` is a nonzero constant.

So the surviving family is exactly
`S = ( X1 + d1*gamma ,  X2 + d1*(2c*X1+e)*gamma + c*d1^2*gamma^2 )`,
and the sympy check closes it:

```
T := S2 - c*S1^2 - e*S1  =  X2(w) - c*X1(w)^2 - e*X1(w)      (gamma-free: True)
det J(S1, T) = d1*(X2' - 2c*X1*X1' - e*X1')                  (= kappa)
```

`(u,v) -> (u, v - c*u^2 - e*u)` is a **triangular automorphism of the target**,
so post-composing with it turns `S` into `(X1(w) + d1*gamma, G(w))` with
`G = X2 - c*X1^2 - e*X1`. Keller then forces `G'` constant, `G` linear, and
`w`, then `gamma`, are recovered. **S is injective.**

**Statement of the gamma^2 dichotomy.** For `S = X + gamma*D + gamma^2*E`:
either some positive-gamma coefficient of det J is nonzero, and `S` is not
Keller; or all vanish, and **S is a triangular automorphism composed with an
elementary (quadratic shear) automorphism of the target — hence injective.**

The correct generalization of branch (b) is therefore *not* "Delta parallel to a
constant vector ⇒ triangular" but **"S is triangularisable after an elementary
target shear of degree `deg_gamma(S)`."** The gamma-linear case is the shear-of-
degree-1 (i.e. identity) special case, which is why it read as "triangular".

**Consequence for the campaign.** The archive's headline is safe at gamma-degree
2 — but only because the collapse *reappears one automorphism wider*. The proof
does **not** transfer by inspection; it had to be re-run, and the branch-(b)
hypothesis had to be replaced. Higher gamma-degree is untested here, and the
natural conjecture (shear of degree `deg_gamma`) is the thing to prove, not to
assume. Branch (a)'s twist rebuttal (ii) remains the genuine gap: it is an
ansatz result, and no divisor `C` outside `gamma*x^s` has ever been tried.
