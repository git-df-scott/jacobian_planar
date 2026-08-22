# The SF target system: resolved. NONEMPTY, vdim = 14.

## The flag

`d23_n3_msolve.py` builds two systems and ends by printing:

    run:  msolve -P 2 -f ff_h_system.ms -o ff_h_out.ms   (validation)
          msolve -P 2 -f sf_h_system.ms -o sf_h_out.ms   (the target)

`ff_h_out.ms` is in the repo. **`sf_h_out.ms` is not.** The validation was run;
the target never was. A Rosetta-Stone flag: the resolving command is written
out verbatim and simply undone.

## Both systems, now decided

| system | (m,d,D) | size | verdict | vdim |
|---|---|---|---|---|
| FF (validation) | (8,5,13) | 13 var / 13 eq | NONEMPTY, dim 0 | **2** |
| **SF (the target)** | **(14,9,23)** | **23 var / 23 eq** | **NONEMPTY, dim 0** | **14** |

FF's `vdim = 2` is exactly right: the Session-7 certified dessin has
coefficients in `Q(i√3)`, so it comes with one Galois conjugate. Verified
directly — the certified `(p, r)`, scaled to the slice `r_4 = 1`, satisfies
**13 of 13** equations of the parsed system.

## What SF nonempty does and does not mean

**It does not contradict the campaign's verdict.** Phase 1 concludes the Second
Framework dies by `23/3 ∉ ℤ` — an *integrality* obstruction at the
osculation/chain layer, not a realizability obstruction at h-constancy. So the
SF dessins existing is consistent with, and indeed expected under, that reading:
the configurations exist, and the death happens when one tries to osculate a
23-chain with them.

What is new is the count. **There are exactly 14 SF solutions in this slice**,
against 2 for FF. That is a concrete invariant of the Second Framework that the
campaign did not have, and it is the object any future transfer argument has to
quantify over.

## Caveat carried forward from the generator's own docstring

>  "Caveat: dessins with `r_{d-1} = 0` are missed by this slice; rerun with
>   another slice to exclude/catch them."

That rerun has **not** been done, for either framework. So `vdim = 2` and
`vdim = 14` count the dessins **in the slice `r_{d-1} = 1` only**. This is a
second flag of exactly the same kind, now recorded rather than left implicit.

## Provenance

Found by a Singular sweep of 160 unsolved `.ms` exports, which flagged
`ff_h_system.ms` as NONEMPTY. That hit was correctly triaged as expected (a
Belyi system is *supposed* to have solutions) — but chasing what produced it
led to the unrun target next door.
