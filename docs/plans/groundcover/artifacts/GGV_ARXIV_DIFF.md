# GGV (1.2) row 3: journal print vs arXiv 1310.8249v3

Fetched https://arxiv.org/pdf/1310.8249v3 (10 pages, 151,540 bytes) on 2026-09-02 and extracted with pdftotext -layout.

Both the journal version (Pro Mathematica 27, 2013, p.85 eq (1.2) and p.93 eq (3.6)) and the arXiv v3 (eq (2) and eq (3.9)) print the third relation with the term -2 mu3 q1''(0):

```
Theorem 2. B = 16 if and only if there exist A, q1 ∈ K[y] and µ0 , µ1 , µ2 , µ3 ∈ K with µ0 6= 0,
                          1
                  A(0) = − µ23 ,      A′ (0) = µ2     and    µ3 A′′ (0) = −6µ1 − 2µ3 q1′′ (0),              (2)
                          4
...
Moreover we have
                            1
                  A(0) = − µ23 , A′ (0) = µ2 and u3 A′′ (0) = −6µ1 − 2µ3 q1′′ (0).                (3.9)
                            4
```

Conclusion: the -2 mu3 q1''(0) term is in the authors' source, not a journal typesetting slip. The campaign's re-derivation (mu3 A''(0) = -6 mu1, confirmed independently in run/row3_check.py from the polynomiality of (3.2)/(3.3), valid on the mu3 != 0 stratum) stands against both printed versions. Any B=16 verdict computed with the printed row on the mu3 != 0 stratum is about a proper subvariety.

Context lines from the arXiv text bearing on the GGV conjecture:
```
µ3 = 2 as in 3.1 then we can construct a pair P, Q ∈ K[x, y] with deg(P ) = 112, deg(Q) = 80
and [P, Q] = 2x3 + x4 y.
   The only other solutions were the homogeneous solutions with µ3 = µ2 = µ1 = µ0 = 0. For
deg(q1 ) = 5, after an hour the PC hadn’t solved the resulting system. We also were able to show
that in the case µ1 = 0 = µ2 (and q1 with arbitrary degree), any solution of (3.8) satisfying (3.9)
must have µ0 = 0.
   Based on this partial results, we state the following conjecture:

   CONJECTURE: The only solutions of (3.8) are the solutions with µ2 = µ1 = 0.

   If the conjecture is true, then the only solutions of (3.8) satisfying (3.9) are the solutions with
µ2 = µ1 = µ0 = 0, which implies B > 16.

```
