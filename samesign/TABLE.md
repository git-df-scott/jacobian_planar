# T2 — the same-sign weighted-homogeneous sector, empirical table

Certifier `samesign/run_sweep.py` (9/9 controls, log `samesign/sweep.log`),
data `samesign/sweep_results.json`. Weights (a,b) with a, b >= 0 and
a + b <= 12; monomial bases taken to total degree 20;
`[P,Q] in K^*` forces dP + dQ = a + b, which is CHECKED on every off-shell
cell rather than assumed. Each cell is decomposed exactly over Q in Singular
(minAssGTZ) — no sampling — and every branch is classified by an explicit
inverse over K(s,t), verified both ways, plus an independent generic-fibre
count by resultant elimination.

| weights (a,b) | cells (dP,dQ) | cells with Keller pairs | branches | non-automorphisms |
|---|---:|---:|---:|---:|
| (1,1) | 1 | 1 | 3 | 0 |
| (1,2) | 2 | 2 | 6 | 0 |
| (1,3) | 3 | 2 | 6 | 0 |
| (1,4) | 4 | 2 | 6 | 0 |
| (1,5) | 5 | 2 | 6 | 0 |
| (1,6) | 6 | 2 | 6 | 0 |
| (1,7) | 7 | 2 | 6 | 0 |
| (1,8) | 8 | 2 | 6 | 0 |
| (1,9) | 9 | 2 | 6 | 0 |
| (1,10) | 10 | 2 | 6 | 0 |
| (1,11) | 11 | 2 | 6 | 0 |
| (2,1) | 2 | 2 | 6 | 0 |
| (2,2) | 1 | 1 | 3 | 0 |
| (2,3) | 2 | 2 | 6 | 0 |
| (2,4) | 2 | 2 | 6 | 0 |
| (2,5) | 2 | 2 | 6 | 0 |
| (2,6) | 3 | 2 | 6 | 0 |
| (2,7) | 2 | 2 | 6 | 0 |
| (2,8) | 4 | 2 | 6 | 0 |
| (2,9) | 2 | 2 | 6 | 0 |
| (2,10) | 5 | 2 | 6 | 0 |
| (3,1) | 3 | 2 | 6 | 0 |
| (3,2) | 2 | 2 | 6 | 0 |
| (3,3) | 1 | 1 | 3 | 0 |
| (3,4) | 2 | 2 | 6 | 0 |
| (3,5) | 2 | 2 | 6 | 0 |
| (3,6) | 2 | 2 | 6 | 0 |
| (3,7) | 2 | 2 | 6 | 0 |
| (3,8) | 2 | 2 | 6 | 0 |
| (3,9) | 3 | 2 | 6 | 0 |
| (4,1) | 4 | 2 | 6 | 0 |
| (4,2) | 2 | 2 | 6 | 0 |
| (4,3) | 2 | 2 | 6 | 0 |
| (4,4) | 1 | 1 | 3 | 0 |
| (4,5) | 2 | 2 | 6 | 0 |
| (4,6) | 2 | 2 | 6 | 0 |
| (4,7) | 2 | 2 | 6 | 0 |
| (4,8) | 2 | 2 | 6 | 0 |
| (5,1) | 5 | 2 | 6 | 0 |
| (5,2) | 2 | 2 | 6 | 0 |
| (5,3) | 2 | 2 | 6 | 0 |
| (5,4) | 2 | 2 | 6 | 0 |
| (5,5) | 1 | 1 | 3 | 0 |
| (5,6) | 2 | 2 | 6 | 0 |
| (5,7) | 2 | 2 | 6 | 0 |
| (6,1) | 6 | 2 | 6 | 0 |
| (6,2) | 3 | 2 | 6 | 0 |
| (6,3) | 2 | 2 | 6 | 0 |
| (6,4) | 2 | 2 | 6 | 0 |
| (6,5) | 2 | 2 | 6 | 0 |
| (6,6) | 1 | 1 | 3 | 0 |
| (7,1) | 7 | 2 | 6 | 0 |
| (7,2) | 2 | 2 | 6 | 0 |
| (7,3) | 2 | 2 | 6 | 0 |
| (7,4) | 2 | 2 | 6 | 0 |
| (7,5) | 2 | 2 | 6 | 0 |
| (8,1) | 8 | 2 | 6 | 0 |
| (8,2) | 4 | 2 | 6 | 0 |
| (8,3) | 2 | 2 | 6 | 0 |
| (8,4) | 2 | 2 | 6 | 0 |
| (9,1) | 9 | 2 | 6 | 0 |
| (9,2) | 2 | 2 | 6 | 0 |
| (9,3) | 3 | 2 | 6 | 0 |
| (10,1) | 10 | 2 | 6 | 0 |
| (10,2) | 5 | 2 | 6 | 0 |
| (11,1) | 11 | 2 | 6 | 0 |
| **total** | **230** | **126** | **378** | **0** |

## Shape of what is there

Monomial-basis sizes of the cells that carry Keller pairs (|M_P|,|M_Q|) -> count: {(1, 1): 156, (1, 2): 102, (2, 1): 102, (2, 2): 18}.

Every branch found has generic fibre exactly 1 and an explicit polynomial
inverse. Three sample branches, verbatim from the sweep:

* weights (1, 1), (dP,dQ) = (1,1): P = x - 2*y,  Q = -2*x + y,  det J = -3,  inverse = ['-s/3 - 2*t/3', '-2*s/3 - t/3']
* weights (1, 2), (dP,dQ) = (1,2): P = -2*x,  Q = x**2 + y,  det J = -2,  inverse = ['-s/2', '-s**2/4 + t']
* weights (1, 2), (dP,dQ) = (2,1): P = x**2 - 2*y,  Q = x,  det J = 2,  inverse = ['t', '-s/2 + t**2/2']
* weights (1, 3), (dP,dQ) = (1,3): P = -2*x,  Q = x**3 + y,  det J = -2,  inverse = ['-s/2', 's**3/8 + t']
* weights (1, 3), (dP,dQ) = (3,1): P = x**3 - 2*y,  Q = x,  det J = 2,  inverse = ['t', '-s/2 + t**3/2']
* weights (1, 4), (dP,dQ) = (1,4): P = -2*x,  Q = x**4 + y,  det J = -2,  inverse = ['-s/2', '-s**4/16 + t']

No theorem is claimed here. The table is the result; the auditor decides
whether a theorem is worth proving from it.
