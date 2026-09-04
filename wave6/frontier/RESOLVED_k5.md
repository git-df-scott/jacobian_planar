# OPEN-1 frontier: k = 5 AND k = 6 (h = t, D = 4) are EMPTY

The campaign closed this case **by infeasibility**, not by proof:

>  `k=5, h=t, deg<=4` died at 2m46s of a 900 s budget on a 16 GB machine
>  (Linux OOM killer). "More RAM, or an F4/FGLM engine such as msolve, moves
>  the line further."

## What was tried tonight, and what it gave

| engine | budget | result |
|---|---|---|
| Singular `slimgb` (campaign) | 900 s / 16 GB | OOM-killed — NO VERDICT |
| **msolve** (the named, never-run fix) | 6 GB | SIGSEGV — **NO VERDICT** |
| msolve | 10 GB, machine to itself | **NO VERDICT** |
| Singular `slimgb` | 5 GB / 105 s | terminated — NO VERDICT |
| **branching + `slimgb` per leaf** | 3.5 GB per leaf | **EMPTY** |

**More memory and a different engine were both the wrong answer.** The named fix
does not suffice at this scale.

## What worked: the monomial equations are case splits, not constraints

The system (46 variables, 64 equations) contains **6 single-monomial equations,
every one a product of exactly two variables**, over 8 distinct variables, with
`c_46` occurring in 4 of them. A monomial equation `c_i · c_j = 0` is not
something to grind through — over a field it is an exhaustive binary split, and
*both* sides are cheap:

    c_46 = 0    ->  4 monomial equations vanish outright
    c_46 != 0   ->  all four of its partners are FORCED to zero

Because the monomial equations share variables, the tree **collapses** rather
than branching out. The root split into **15 leaves, and every leaf is EMPTY.**

A memory wall is a statement about the root system. Splitting first means the
solver never sees the root.

## Soundness and controls

Over a field `uv = 0` implies `u = 0` or `v = 0`, so the split is exhaustive and
**every leaf EMPTY implies the root EMPTY**. One unresolved leaf would make the
whole run NO VERDICT, and that is reported rather than rounded away.

The solver was checked against being a can't-fail certifier — the failure mode
that has caught this campaign repeatedly:

- **P-POS**: a system with known solutions (including a monomial equation, so the
  branching path is exercised too) → correctly **NOT EMPTY**, 2 lead leaves found.
- **P-NEG**: a contradictory system → correctly **EMPTY**.

It can say NONEMPTY, and does.

## k = 6 as well

The campaign's other unresolved case — `k=6, h=t, D=4`, which died on Singular's
own memory guard ("no more memory", halt 14) at 3m40s — was run by the same
route: **85 equations, 56 variables -> 22 leaves, every one EMPTY.**

So **both** unresolved cases of the h-branch frontier are now decided, and
neither needed more memory than a 3.5 GB-per-leaf budget.

| case | campaign | branching |
|---|---|---|
| `k=5, h=t, D=4` | OOM-killed, 2m46s | **EMPTY** — 15 leaves |
| `k=6, h=t, D=4` | "no more memory", halt 14, 3m40s | **EMPTY** — 22 leaves |

## Scope

This is `p = 1000003`, one prime, for both cases. Per the campaign's own note, emptiness mod p
for an integer system does imply emptiness over ℚ *provided p divides no
denominator* — these coefficients are small integers — but a second prime is the
standing requirement and is not yet run here. **Announced, not closed.**
