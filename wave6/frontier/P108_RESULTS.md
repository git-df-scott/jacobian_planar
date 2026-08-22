# The (9,27) branch of (72,108): 2 of 4 now decided

All four of these systems were **TIMEOUT / NO VERDICT** in `pair108_results.json`
— the reopened (9,27) branch, the cells sitting closest to the main (72,108)
line, which is why they were ranked first by proximity rather than by count.

| system | size | campaign | branching + 2 engines |
|---|---|---|---|
| `p108_843700` | 41 var / 165 eq | TIMEOUT | **EMPTY** — 2 leaves, both empty |
| `p108_821326` | — | TIMEOUT | **EMPTY** — 2 leaves, both empty |
| `p108_525122` | 28 var / 140 eq | TIMEOUT | NO VERDICT — 5 leaves: **3 EMPTY**, 2 unresolved |
| `p108_192622` | — | TIMEOUT | NO VERDICT — 1 leaf unresolved (139 eq / 38 var) |

**Two cells closed outright.** A third is 3/5 closed by leaf: the root stays
unresolved because one unresolved leaf makes it unresolved, but three of its
five branches are now proved empty and only two specific leaves remain. That is
strictly more than the campaign had, and the residual work is now *named*
rather than being a monolithic timeout.

## Where the method works and where it does not

The h-branch frontier cases collapsed beautifully (15 and 22 easy leaves)
because they carry **single-monomial equations that share variables** — `c_46`
alone appeared in 4 of 6. The (9,27) systems do not have that shape to the same
degree, so their trees are shallow (1–5 leaves) and the leaves stay nearly as
hard as the root: `p108_192622` produced a single leaf of 139 equations in 38
variables that **neither engine** could decide.

So the honest scope of the branching method: **it converts a memory wall into
progress exactly when the system carries shared monomial equations, and it does
essentially nothing when it does not.** Recording both halves, because a method
that is reported only where it wins is not a method.

## The two engines earned their place

Leaves that stall under `slimgb` now fall through to msolve before being called
NO VERDICT. The final unresolved leaves are labelled "both engines: no verdict",
which is a materially stronger statement than one engine timing out.
