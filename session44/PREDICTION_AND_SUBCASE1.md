# A falsifiable prediction, and subcase 1 is structurally different

## 1. Prediction: a_10_5 = 0

From the VERIFIED face structure of open subcase 2 -- face(P) = R^2 with
R(t) = c0 + c3 t^3 + c4 t^4 -- expanding the square gives the full edge
coefficient list along the (0,0)-(8,16) face:

    k : lattice point : a_k
    0 : (0,0)   : c0^2
    1 : (1,2)   : 0        <- descent FOUND this (level 4)
    2 : (2,4)   : 0        <- descent FOUND this (level 8)
    3 : (3,6)   : 2 c0 c3
    4 : (4,8)   : 2 c0 c4
    5 : (5,10)  : 0        <- PREDICTED, not yet found by the descent
    6 : (6,12)  : c3^2
    7 : (7,14)  : 2 c3 c4
    8 : (8,16)  : c4^2

The gap in R at degrees 1,2 propagates to a gap in R^2 at degrees 1,2,5.
So the structure predicts a THIRD forced zero the descent has not yet
reached: the coefficient at lattice point (5,10), symbol a_10_5.

This is a genuine falsifiable test of everything derived so far. If the
descent forces a_10_5 to be nonzero, or produces a solution with
a_10_5 != 0, then the face-form analysis is WRONG and must be discarded.
If it independently forces a_10_5 = 0, that is confirmation from a
completely separate computation.

## 2. Subcase 1 does NOT share this face

Subcase 1 has the extra vertices (0,8) in N(P) and (0,12) in N(Q). Under
the same weight w = j - 2i:

    w on N(P): {(0,0):0, (1,0):-2, (8,14):-2, (8,16):0, (0,8):8}
    w on N(Q): {(0,0):0, (2,1):-3, (12,21):-3, (12,24):0, (0,12):12}

The extra vertices DOMINATE, so the w-max face is a single vertex, not an
edge. A one-point face form is a monomial, and the R^2/R^3 factorisation
argument does not apply in that direction at all. The edge-gap result is
therefore specific to subcase 2 and must NOT be quoted for subcase 1.

## 3. But subcase 1 has its own R^2/R^3 face

Scanning directions where BOTH polygons present an edge:

    (1,0)  : P-face [(8,14),(8,16)]  Q-face [(12,21),(12,24)]
    (2,-1) : P-face [(1,0),(8,14)]   Q-face [(2,1),(12,21)]
    (-1,1) : P-face [(8,16),(0,8)]   Q-face [(12,24),(0,12)]

The (-1,1) face is the structural twin of subcase 2's: the P-edge runs
(0,8) to (8,16), direction (8,8), primitive (1,1), lattice length 8; the
Q-edge runs (0,12) to (12,24), lattice length 12; gcd = 4. The commuting
argument carries over -- for this weight w' = j - i one has
w'(result) = w'(1) + w'(2) + w'(-1,-1) = w'(1) + w'(2), so the top
component of [P,Q] has w' = 20 while the target x^2 has w' = -2, forcing
the top component to vanish. Hence face(P) = R^2, face(Q) = R^3 with
deg R = 4 on that face too.

So the same machinery applies to subcase 1, just on the (-1,1) face
instead of the (-2,1) one. Running the descent's obstructions through that
face is the natural next analysis, and it is cheap.
