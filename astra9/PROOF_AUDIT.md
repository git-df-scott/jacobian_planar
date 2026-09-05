# Scope and boundary-case audit of the full obstruction

The proof is a written arbitrary-degree argument, supported by symbolic
identities. It is not a finite-degree census or a proof-assistant certificate.

| Potential gap | Resolution |
|---|---|
| Only the normalized (6,9) system was checked | The proof starts with arbitrary P,Q in B and uses no degree range. |
| A minimal counterexample or standard Newton position was assumed | Neither is used. The cited Corollary 1.6 precedes and is independent of those later hypotheses. |
| Newton slope means slope -1 | The exponent line is i-j=d, hence slope +1; its outward weight is (1,-1). |
| Adding the origin changes the exposed face | The relevant weight is d>0, so the origin lies strictly below it. |
| A unique leading monomial could satisfy parity | Its first odd coefficient is explicitly nonzero. Lower weights start one power later and cannot cancel it. |
| A nonmonomial L could have only zero roots | After factoring out z^j, it has positive degree and nonzero constant term, so it has a nonzero root over C. |
| The root of L must be simple | Newton-Puiseux allows ramification e>=1. The residue becomes e*lambda, still nonzero. |
| F must be irreducible | It need not be. A branch on any component of F=0 with the indicated leading term suffices. |
| The fibre branch exists only to finite order | It is an exact algebraic Puiseux branch; no truncation supplies the contradiction. |
| H could acquire a logarithm along the branch | A polynomial H composed with Laurent v and power-series c belongs to C((s)); it has no logarithmic term. |
| Laurent differentiation could have nonzero residue | The s^(-1) term would have to come from the derivative of the constant term, whose derivative is zero. |
| kappa=-1 or complex constants escape | Only kappa!=0 is used. Swapping coordinates changes its sign and nothing else. |
| Weight zero was incorrectly called forbidden | It is included in the nonpositive case. Only positive weight is excluded by collision parity and the edge lemma. |
| Both functions of c, or zero/constant components, escape | Their Jacobian is zero directly. |
| Only one B component is excluded | No: one B component can occur in an ordinary Keller pair, for example (c,-v). The proof applies separately to each component before using both nonpositive weights. |
| Finite conductor compatibility contradicts the theorem | The residue proof requires a finite polynomial primitive and an exact algebraic fibre. A conductor completion does not supply that global object. |
| This proves all JC2 Keller maps invertible | No. Membership in this specific collision algebra is essential. |

The global negative control c*(Q+v)^2=1 is rejected independently: its
c-valuation is odd on the left for every rational Q+v. Ordinary polynomial
Keller maps continue to satisfy the ambient criterion and the no-edge test.
They fail simultaneous membership in B, as they must.

## Why the preceding strikes missed the closure

Astra 6--8 correctly retained multiple terms on the leading mixed-weight
face, but treated those terms as input to residual systems. They did not
apply the slope-one edge obstruction at that face. The needed global
infinity residue was already present before any degree-specific elimination.
The earlier OPEN verdicts are superseded by this argument, not by a further
coefficient sweep or a claim that the surviving resonance was generically
irreducible.
