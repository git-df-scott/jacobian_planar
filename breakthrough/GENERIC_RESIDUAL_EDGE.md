# Generic residual-edge collapse

## Verdict

**NO VERDICT** for existence of a Keller map at any degree pair.  The argument
below is a necessary-condition theorem, not an emptiness argument.  It sharpens
the first upper-edge relation: under the stated edge hypotheses, the leading
edge of `P` is necessarily a full `m`-th power of a linear form.

## Setup and derivation

Let `m = deg_x(P)`, `n = deg_x(Q)`, `g = gcd(m,n)`, `a = m/g`, and
`b = n/g`.  Write `A(t)` and `B(t)` for the two nonzero leading edge
polynomials, of exact degrees `m` and `n`.  The top bracket equation gives

    m A B' = n A' B,

and hence

    B^m = c A^n.                                      (1)

Equivalently (over an algebraically closed characteristic-zero field), there
is a degree-`g` polynomial `G` with `A = alpha G^a` and `B = beta G^b`.

Form the primitive residual

    R = Q^a - lambda P^b,

choosing `lambda` to cancel its leading edge.  The Poisson identity is exact:

    {P,R} = a Q^(a-1) {P,Q} = a x^2 Q^(a-1).           (2)

Assume, as in the pentagon residual ladder, that cancellation exposes a
nonzero residual edge polynomial `H(t)` of exact degree `m-1`, and that the
right side of (2) lies below the edge used for the next top-coefficient
equation.  Extraction of that coefficient gives

    (m-1) A' H = m A H',

so

    H^m = d A^(m-1).                                  (3)

This is the generic form requested in `OPUS43-015`/`OPUS43-016`; at
`(m,n)=(8,12)` it is exactly `H^8 = d A^7`.

For every root `rho` of `A`, equation (3) says

    m ord_rho(H) = (m-1) ord_rho(A).

Since `gcd(m,m-1)=1`, every root multiplicity of `A` is divisible by `m`.
Because `deg(A)=m`,

    A(t) = alpha (t-rho)^m.                            (4)

Substitution in (1) then gives

    B(t) = beta (t-rho)^n.                             (5)

Thus the residual relation makes the intermediate perfect-power exponent
`m/g` irrelevant: the full leading row collapses to one linear factor for
**every** degree pair satisfying the residual-edge hypotheses.

## Scope and controls

The exact degree and nonzero-edge assumptions are essential.  In particular,
one may not declare a pair empty merely because `H` vanishes or has lower
degree; those cases are separate strata.  Equations (4)--(5) are compatible
with nonzero endpoint constraints whenever `alpha`, `beta`, and `rho` are
nonzero.  Consequently this filter alone returns **NO VERDICT**, including for
`(72,108)`.

At divisible degree ratios (`m | n`) the original relation (1) imposes no
perfect-power condition beyond choosing `B` as a power of `A`.  Explicit tame
automorphisms

    P = x + y^m,    Q = y + P^k,    n = km

have `{P,Q}=1`, degrees `(m,n)`, and leading forms `y^m`, `y^n`.  They survive
the full-power conclusion, providing the requested positive/negative control
at `(1,2)`, `(2,4)`, and `(2,6)`.  This is a control of the generic edge
theorem, not of pentagon-specific support bookkeeping.

The companion script performs exact symbolic checks of the bracket identity,
the two differential edge identities, the pentagon specialization, and all
three tame controls.
