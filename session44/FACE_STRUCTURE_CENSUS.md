# Face-structure census: 1506 unused constraints in the campaign's own data

Built by generalising the verified (72,108) face argument to every shape in
the catalogue. For each distinct system (638 of them) and each primitive
direction, a face is recorded when BOTH polygons present an edge there and
the weight arithmetic forces the two face forms to commute -- exactly the
argument verified for the open case (w(result) = w1 + w2 + w(-1,-1), and
the bracket target's weight lies strictly below the top, so the top
component vanishes identically).

Result: 1506 such faces. On every one of them,

    face(P) = R^a   and   face(Q) = R^b,   a/b = L_P/L_Q in lowest terms,
    deg R = gcd(L_P, L_Q).

Census of the structures found:

    R^2/R^3, deg R = 1  : 635 faces      R^3/R^4, deg R = 1 :  78
    R^2/R^3, deg R = 4  : 160            R^2/R^5, deg R = 1 :  74
    R^2/R^3, deg R = 2  : 148            R^3/R^4, deg R = 4 :  30
    R^2/R^3, deg R = 3  :  84            R^3/R^4, deg R = 2 :  24
    R^2/R^3, deg R = 5  :  50            R^2/R^3, deg R = 7 :  20
    R^2/R^3, deg R = 6  :  36            R^2/R^3, deg R = 9 :  20

The (2,3) structure of the open case is by far the commonest: 1181 faces
across 16 distinct shapes, with deg R running from 1 to 10.
Table written to lead4/face_structure_table.json.

## Why this matters, and it is not a curiosity

Each such face imposes PERFECT-POWER conditions the campaign has never
used. Concretely, on a face with deg R = d:

  * face(P) has 2d+1 coefficients but only d+1 free parameters (those of
    R), so d of them are determined -- e.g. deg R = 1 forces the classic
    a_1^2 = 4 a_0 a_2 on the three face coefficients of P;
  * face(Q) has 3d+1 coefficients determined by the SAME d+1 parameters,
    eliminating a further 2d.

For the open subcase 2 (deg R = 4) that is 4 conditions on P's face and 8
on Q's -- twelve constraints available before any solver is started, on a
system with only 25 parameters.

## The instrument this suggests

Pre-impose the face factorisations, i.e. parameterise each face by its
root R instead of by free coefficients, THEN run the descent. This shrinks
the unknown count instead of discovering the same relations one slow level
at a time -- which is precisely what the current descent is doing by hand:
its level-4 and level-8 obstructions are nothing more than two of these
face conditions, rediscovered expensively.

## Caveat, stated plainly

The census records which faces CARRY the structure; it does not by itself
kill any shape. A kill needs the structure to collide with the vertex
conditions (as in the edge-gap argument, where multiplicity >= 3 forced a
vertex coefficient to vanish). The table is the input to that search, not
its conclusion.
