# Dessin combinatorics parsed from arXiv:1901.04073 (TeX source figures)

Machine-parsed from the paper's LaTeX picture environments (segment-endpoint
matching + rotation-system face tracing, both verified: face degrees match the
stated ramification profiles exactly). This is the seed data for the
Session-N3 derivation of the Second Framework's (-5)-curve map (P, R).

## Figure 28 — degree-23 (-2)-curve dessin, Second Framework (used in Phase 0)

Star-of-stars tree; cyclic order of branch degrees around the order-7 white
hub, counterclockwise: **(5, 1, 5, 3, 3, 3, 3)** — the degree-1 branch sits
between the two degree-5 branches; reflection-symmetric, hence one of the 3
real embeddings. Identified in Phase 0 as the real embedding β ≈ 0.1250089
(root 3 of `d23_belyi_data/d23_roots.txt`).

## Figure 16 — degree-13 (-2)-curve dessin, First Framework (control)

Cyclic order around the order-5 hub: (3, 1, 3, 3, 3) — the unique necklace of
{1,3,3,3,3}, consistent with Borisov's "unique dessin" remark. (Control: the
parse machinery reproduces the known-unique case.)

## Figure 27 — degree-28 clean dessin, Second Framework (-5)-curve map

Profile 14×2 / 9×3+1×1 / 1×23+5×1. The paper draws the planar dual
(bullets = the nine order-3 + one order-1 points over {∞}; loops as circles;
preimages of {1} are the faces: one outer face of degree 23 + five degree-1
loop interiors). Dualized to "center vertex" form: center C of degree 23,
nine loops L1–L9 at C, five pendant edges P1–P5 to the order-1 leaves.

Cyclic order of the 23 edge-ends around C (counterclockwise):

    L1a, L2a, L3a, L4a, L4b, L5a, P4, L5b, L3b, L6a, P3, L6b,
    L2b, L7a, P2, L7b, L1b, L8a, P1, L8b, L9a, P5, L9b

Nesting forest (interval containment):

    L1 ⊃ ( L2 ⊃ ( L3 ⊃ ( L4 , L5 ⊃ P4 ) , L6 ⊃ P3 ) , L7 ⊃ P2 )
    L8 ⊃ P1
    L9 ⊃ P5

L4 is the bare loop bounding the unique degree-1 face; the nine order-3
faces are the five loop-with-pendant interiors, the three annular regions of
the L1–L3 chain, and the outer region of C beyond {L1, L8, L9}. Depth-4
nested caterpillar. Consistency: 23 ends = 9·2 + 5; F = 2 − 6 + 14 = 10 =
9 + 1. ("Not unique, there are some options" — the passport admits variants;
this is the one Borisov drew.)

## Figure 15 — degree-16 clean dessin, First Framework (control)

Same convention; dual form: center degree 13, loops M1–M5, pendants
Q1, Q2, QT. Cyclic order: M1a, M2a, M2b, M3a, Q2, M3b, M1b, M4a, Q1, M4b,
M5a, QT, M5b. Nesting: M1 ⊃ (M2, M3 ⊃ Q2), M4 ⊃ Q1, M5 ⊃ QT — the
depth-2 pattern of which Fig. 27 is the depth-4 extension. (Control for the
Session-7-certified (p, r): 2·8 = 1 + 3·5 = 16 ✓.)

## Structural note

Both frameworks use the same "caterpillar" template: an outermost nested
chain terminating in the bare loop, plus two unnested loops-with-pendants.
FF: chain depth 2, D = 13; SF: chain depth 4, D = 23.
