# Stop trusting EMPTY. Demand a certificate.

## The campaign's actual epistemic gap

Today established two things that together leave a hole:

1. **msolve's modular emptiness is unsound for contradictions** — an `EMPTY`
   verdict mod p is not a proof, and empty output files from timeouts and
   crashes have repeatedly *looked* like verdicts.
2. **Direct Gröbner does not reach these systems.** Job #1 (90 min) and job #2
   both ended with no verdict; the level cascade failed three times.

So for the systems that matter the campaign currently has **no sound route to
a negative answer at all** — only timeouts and untrusted `EMPTY`s. Every
"closed" cell below rests either on a small enough Gröbner run or on modular
evidence that was itself shown unsound this morning.

## The fix: a Nullstellensatz certificate, found by linear algebra

Hilbert's Nullstellensatz: the system `F₁ = … = F_m = 0` has **no** solution
over an algebraically closed field **iff** there exist polynomials `λ_k` with

        Σ_k λ_k · F_k  =  1                      (identically)

For a **fixed multiplier degree D**, finding the `λ_k` is a **linear system**
in their coefficients — no Gröbner basis, no ideal membership, no monomial
ordering. This is Nullstellensatz Linear Algebra (NulLA, De Loera et al.).

Why this is the right tool here:

- **Sound and independently checkable.** A certificate is verified by expanding
  a polynomial identity. It cannot be a can't-fail certifier — the campaign's
  recurring failure mode — because the check has an obvious way to fail.
- **Linear algebra scales where Gröbner does not.** Memory is predictable, the
  computation is streamable and restartable (this container drops every 30–50
  minutes; a linear solve survives that pattern, a monolithic Gröbner run does
  not), and it parallelises.
- **The certificate is a small committable artifact.** Unlike a 46 MB RUR, a
  degree-1 certificate is a sparse coefficient vector that any future session
  can re-verify in seconds without re-running anything.
- **The bilinear structure keeps it small.** Because every monomial of the
  pentagon system has c-degree ≤ 1 and d-degree ≤ 1, products `λ_k · F_k` have
  tightly controlled support — the monomial basis does not blow up the way it
  would for a dense system of the same degree.

## The ladder

- **D = 0** (λ constant): `Σ λ_k F_k = nonzero constant`. **Already done** —
  this is exactly the "no equation collapses to a nonzero constant" check in
  `w6_pent_lineloop.py`. No certificate exists at D = 0. That is a real,
  already-paid-for negative datum, and it is the first rung of this ladder
  rather than an isolated fact.
- **D = 1** (λ linear): unknowns = 283 × 166 = **46,978**. This is the next
  rung and it has never been attempted.
- **D = 2** if D = 1 fails, subject to size.

## Reading the outcomes — both directions are informative

- **A certificate is found** → case (1) is **PROVED empty**, soundly, with an
  artifact that survives the session. This is strictly stronger than anything
  the campaign currently has for any cell, and the same machinery then applies
  to the 41 timeout shapes and to case (2)'s missing char-0 confirmation.
- **No certificate at low degree** → weak evidence *toward* feasibility, i.e.
  toward a counterexample. Infeasible systems arising from real structure
  usually admit low-degree certificates; a system that resists D = 1 and D = 2
  is behaving unusually, and that is a reason to spend more on the hunt.

Either way it converts a timeout into information, which is what the last three
sessions of pentagon compute failed to do.

## The characteristic-0 caveat, stated precisely

A certificate found mod p proves emptiness over the algebraic closure of `F_p`
only. That is **not** automatically a char-0 result — and this campaign has
already been burned by exactly that inference. But the direction of the
implication is favourable here:

- If the system had a solution over `C`, it would have one over `Q̄`, hence
  a good reduction with a solution mod **almost every** p. So a certificate at
  a single p is compatible with a char-0 solution only if that p is one of
  finitely many bad primes; certificates at several independent primes make
  that escape route very narrow.
- **The clean finish**: reconstruct the certificate coefficients over `Q` by
  rational reconstruction from the mod-p solution and verify the identity
  `Σ λ_k F_k = 1` exactly over `Q`. That is a *proof* in characteristic zero,
  and the verification is pure exact arithmetic — no solver is trusted at any
  point.

This is the piece the campaign has been missing: a way to finish a cell
negatively without believing a black box.
