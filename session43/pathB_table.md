# odd row: {'cell': '2 1 1 6', 'status': 'timeout'}
# odd row: {'cell': '2 -1 0 6', 'status': 'timeout'}
| n | b | p | q | D | vars/eqs | branches | example nonlinear |
|---|---|---|---|---|----------|----------|-------------------|
| 2 | -3 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0)* |  |
| 2 | -3 | 1 | 1 | 3 | 12/8 | 2x degenerate(det=0)*, 1x linear/affine, 3x nonlinear-tame-automorphism |  |
| 2 | -2 | 0 | 1 | 3 | 9/8 | 6x degenerate(det=0) |  |
| 2 | -2 | 1 | 0 | 3 | 9/8 | 9x degenerate(det=0) |  |
| 2 | -1 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0)* |  |
| 2 | -1 | 0 | - | 4 | -/- | timeout |  |
| 2 | -1 | 1 | 1 | 3 | 12/8 | 1x degenerate(det=0)*, 2x nonlinear-tame-automorphism |  |
| 2 | -1 | 1 | 1 | 4 | 12/8 | 2x degenerate(det=0), 1x linear/affine, 3x nonlinear-tame-automorphism | e.g. F=(x**3 + 8*x + 4*y ; 2*x**3 + 5*x + 8*y) |
| 2 | 1 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0)* |  |
| 2 | 1 | 0 | - | 4 | -/- | timeout |  |
| 2 | 1 | 1 | 1 | 3 | 12/8 | 1x degenerate(det=0)*, 2x nonlinear-tame-automorphism |  |
| 2 | 1 | 1 | 1 | 4 | 12/8 | 2x degenerate(det=0), 1x linear/affine, 3x nonlinear-tame-automorphism | e.g. F=(8*x**3 + x + 32*y ; 2*x**3 + 5*x + 8*y) |
| 2 | 3 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0)* |  |
| 2 | 3 | 1 | 1 | 3 | 12/8 | 1x degenerate(det=0)*, 2x nonlinear-tame-automorphism |  |
| 3 | -2 | 0 | 2 | 3 | 7/4 | 4x degenerate(det=0) |  |
| 3 | -2 | 1 | 1 | 3 | 4/0 | 1x linear/affine |  |
| 3 | -2 | 2 | 0 | 3 | 7/4 | 4x degenerate(det=0) |  |
| 3 | -1 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0)* |  |
| 3 | -1 | 1 | 2 | 3 | 6/4 | 3x degenerate(det=0)*, 4x nonlinear-tame-automorphism |  |
| 3 | -1 | 2 | 1 | 3 | 6/4 | 2x degenerate(det=0)*, 4x nonlinear-tame-automorphism |  |
| 3 | 1 | 0 | 2 | 3 | 7/4 | 1x degenerate(det=0)* |  |
| 3 | 1 | 0 | 2 | 4 | 7/4 | 4x degenerate(det=0) |  |
| 3 | 1 | 1 | 1 | 3 | 4/0 |  |  |
| 3 | 1 | 1 | 1 | 4 | 14/11 | 19x degenerate(det=0), 1x linear/affine, 4x nonlinear-tame-automorphism | e.g. F=(5*x**4/256 + 5*x**3*y/16 + 15*x**2*y**2/8 + 5*x*y**3 + 29*x/9 + 5*y**4 + 4*y ; 9*x**4/256 + 9*x**3*y/1 |
| 3 | 1 | 2 | 0 | 3 | 7/4 | 2x degenerate(det=0)* |  |
| 3 | 2 | 0 | 0 | 3 | 6/3 | 2x degenerate(det=0) |  |
| 3 | 2 | 1 | 2 | 3 | 6/4 | 3x degenerate(det=0), 4x nonlinear-tame-automorphism | e.g. F=(3*x ; 2*x**2 + 9*y) |
| 3 | 2 | 2 | 1 | 3 | 6/4 | 2x degenerate(det=0), 4x nonlinear-tame-automorphism | e.g. F=(9*y ; 2*x + 3*y**2) |
| 3 | 3 | 0 | 1 | 3 | 7/6 | 5x degenerate(det=0), 2x nonlinear-tame-automorphism | e.g. F=(x**3 + 2*y ; 8*x) |
| 3 | 3 | 1 | 0 | 3 | 7/6 | 4x degenerate(det=0), 1x nonlinear-tame-automorphism | e.g. F=(7*x ; 6*x**3 + 8*y) |
| 3 | 3 | 2 | 2 | 3 | 4/1 | 1x degenerate(det=0) |  |
| 4 | -3 | 0 | - | 3 | -/- | error:ubs(sol)); s2 = sp.expand(F2.subs(sol))
                   ^^^^^^^
AttributeError: 'int' object has no attribute 'subs'
 |  |
| 4 | -3 | 1 | 1 | 3 | 4/0 | 1x linear/affine |  |
| 4 | -3 | 2 | - | 3 | -/- | error:ubs(sol))
                                                 ^^^^^^^
AttributeError: 'int' object has no attribute 'subs'
 |  |
| 4 | -3 | 3 | 3 | 3 | 8/5 | 1x degenerate(det=0) |  |
| 4 | -1 | 0 | 0 | 3 | 2/0 |  |  |
| 4 | -1 | 1 | 3 | 3 | 6/4 | 3x degenerate(det=0)*, 3x nonlinear-tame-automorphism |  |
| 4 | -1 | 2 | 2 | 3 | 4/1 | 1x degenerate(det=0)* |  |
| 4 | -1 | 3 | 1 | 3 | 6/4 | 2x degenerate(det=0)*, 3x nonlinear-tame-automorphism |  |
| 4 | 1 | 0 | 2 | 3 | 3/0 |  |  |
| 4 | 1 | 1 | 1 | 3 | 4/0 |  |  |
| 4 | 1 | 2 | 0 | 3 | 3/0 |  |  |
| 4 | 1 | 3 | 3 | 3 | 8/5 | 1x degenerate(det=0)* |  |
| 4 | 2 | 0 | 3 | 3 | 4/3 | 4x degenerate(det=0) |  |
| 4 | 2 | 1 | 2 | 3 | 5/3 | 2x degenerate(det=0), 1x nonlinear-tame-automorphism | e.g. F=(2*x ; 9*x**2 + 3*y) |
| 4 | 2 | 2 | 1 | 3 | 5/3 | 2x degenerate(det=0), 1x linear/affine, 2x nonlinear-tame-automorphism | e.g. F=(7*x**2 + 6*y ; 3*x) |
| 4 | 2 | 3 | 0 | 3 | 4/3 | 4x degenerate(det=0) |  |
| 4 | 3 | 0 | 0 | 3 | 2/0 | 1x degenerate(det=0) |  |
| 4 | 3 | 1 | 3 | 3 | 6/4 | 2x degenerate(det=0), 3x nonlinear-tame-automorphism | e.g. F=(9*x ; 2*x**3 + 3*y) |
| 4 | 3 | 2 | 2 | 3 | 4/1 | 1x degenerate(det=0) |  |
| 4 | 3 | 3 | 1 | 3 | 6/4 | 4x degenerate(det=0), 3x nonlinear-tame-automorphism | e.g. F=(2*y ; 3*x + 9*y**3) |
| 6 | -1 | 0 | 0 | 3 | 2/0 |  |  |
| 6 | -1 | 1 | 5 | 3 | 4/2 | 2x degenerate(det=0)*, 1x linear/affine |  |
| 6 | -1 | 2 | 4 | 3 | 2/1 | 2x degenerate(det=0)* |  |
| 6 | -1 | 3 | 3 | 3 | 4/1 | 1x degenerate(det=0)* |  |
| 6 | -1 | 4 | 2 | 3 | 2/1 | 2x degenerate(det=0)* |  |
| 6 | -1 | 5 | 1 | 3 | 4/2 | 2x degenerate(det=0)*, 1x linear/affine |  |
| 6 | 1 | 0 | 2 | 3 | 3/0 |  |  |
| 6 | 1 | 1 | 1 | 3 | 4/0 |  |  |
| 6 | 1 | 2 | 0 | 3 | 3/0 |  |  |
| 6 | 1 | 3 | 5 | 3 | 4/0 |  |  |
| 6 | 1 | 4 | 4 | 3 | -/- | empty |  |
| 6 | 1 | 5 | 3 | 3 | 4/0 |  |  |
| 6 | 2 | 0 | 3 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 2 | 1 | 2 | 3 | 3/0 | 1x nonlinear-tame-automorphism | e.g. F=(6*x ; 3*x**2 + 7*y) |
| 6 | 2 | 2 | 1 | 3 | 3/0 | 1x nonlinear-tame-automorphism | e.g. F=(3*x**2 + 6*y ; 7*x) |
| 6 | 2 | 3 | 0 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 2 | 4 | 5 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 2 | 5 | 4 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 3 | 0 | 4 | 3 | 2/1 | 2x degenerate(det=0) |  |
| 6 | 3 | 1 | 3 | 3 | 5/3 | 2x degenerate(det=0), 1x nonlinear-tame-automorphism | e.g. F=(2*x ; 9*x**3 + 3*y) |
| 6 | 3 | 2 | 2 | 3 | 2/0 | 1x degenerate(det=0) |  |
| 6 | 3 | 3 | 1 | 3 | 5/3 | 2x degenerate(det=0), 1x linear/affine, 2x nonlinear-tame-automorphism | e.g. F=(6*x**3 + 3*y ; 7*x) |
| 6 | 3 | 4 | 0 | 3 | 2/1 | 2x degenerate(det=0) |  |
| 6 | 3 | 5 | 5 | 3 | 2/0 | 1x degenerate(det=0) |  |
| 6 | 4 | 0 | 5 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 4 | 1 | 4 | 3 | 2/0 | 1x linear/affine |  |
| 6 | 4 | 2 | 3 | 3 | 4/2 | 3x degenerate(det=0) |  |
| 6 | 4 | 3 | 2 | 3 | 4/2 | 3x degenerate(det=0) |  |
| 6 | 4 | 4 | 1 | 3 | 2/0 | 1x linear/affine |  |
| 6 | 4 | 5 | 0 | 3 | 3/2 | 1x degenerate(det=0) |  |
| 6 | 5 | 0 | 0 | 3 | 2/0 | 1x degenerate(det=0) |  |
| 6 | 5 | 1 | 5 | 3 | 4/2 | 2x degenerate(det=0), 2x linear/affine |  |
| 6 | 5 | 2 | 4 | 3 | 2/1 | 2x degenerate(det=0) |  |
| 6 | 5 | 3 | 3 | 3 | 4/1 | 1x degenerate(det=0) |  |
| 6 | 5 | 4 | 2 | 3 | 2/1 | 2x degenerate(det=0) |  |
| 6 | 5 | 5 | 1 | 3 | 4/2 | 2x degenerate(det=0), 2x linear/affine |  |

NO CANDIDATES: every nonzero-Jacobian solution branch in every solved cell classified as linear/affine or nonlinear tame automorphism (elementary-reducible).
