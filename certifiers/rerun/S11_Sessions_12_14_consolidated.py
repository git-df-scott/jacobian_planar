"""
Plane Jacobian campaign - Sessions 12-14 (consolidated)
First Framework decision system: three theorems and a census.
All certifications exact over Q(sqrt(-3)); executable checks recorded
in the transcript inline runs (v-Laurent engine, ~150 lines).

THEOREM 1 (sqrt-reduction).  Write y2 = q^-6 v^-18 g^2 (1 + T),
T = sum_{m>=1} q^m v^{3m} B~_{-6+m}/g^2.  The chain + divisibility
ladder is equivalent to:
    A~_{-9+m} = g^3 S_m   for m = 0..12,
where (sum S_m x^m)^2 = (1+T)^3 formally, polynomiality of g^3 S_m
being the ladder.  The endgame functional collapses to
    W~_-5 = 2 g^3 (A~_4 - g^3 S_13).
Near-miss certification: S_m = p_{8-m} v^{-3m} (m<=8), S_9..12 = 0,
S_13 = -n3 v^{-39}/2, recovering R = n3 - the miracle cancellation IS
the truncation of sqrt(r-tower) to the p-tower.

THEOREM 2 (total rigidity).  The layer-1 (-5)-pole conditions are the
divisibilities (U-1)^{-2-3n} | B~_n, (U-1)^{-3-3n} | A~_n, and the
cross-chart pins are pointwise Taylor conditions at U = 1:
    B~_n^{(t)}(1) = t! eps mu^{-n-1} r_{-n-1}   (t = -2-3n),
    A~_n^{(t)}(1) = t! gam mu^{-n-1} p_{-n-1}   (t = -3-3n).
At n = -6 (B~_-6 = g^2, r_5 = 1) these force the (U-1)-order of g^2
to be EXACTLY 16, so with U | g and deg g = 9 exact:
    g = alpha U (U-1)^8,     alpha^2 = eps mu^5,  alpha^3 = gam mu^8.
The boundary polynomial of ANY framework solution equals the
near-miss's up to one scalar.  Total rigidity.

THEOREM 3 (pole-fiber).  R = 2 v^39 (A~_4 - g^3 S_13)/g^3 has poles
confined to {v = 0, v = -1}; the Belyi-13 fibers have 13/9/5/1
points; only the 1-point fiber fits a <=2-point pole set, so the pole
fiber is the order-13 point at v = infinity and R is a DEGREE-13
POLYNOMIAL.  The forced divisibilities close the v = 0 pole exactly
(boundary partition sigma_1^13, v-order 0).

SESSION 14 (census + structure, probe-corrected).
Parameters entering the realization system: 190
  (B-tower after divisibilities and Taylor pins: 165; A~_4: 23;
   scalars alpha, mu: 2).
Box caps force deg sigma_m <= -m/3, so deg(v^39 S_13) <= 34
STRUCTURALLY - equal to the A~_4-part's reach 15 + 22 - 3.  The
degree-13 collapse (orders 14..34, 21 conditions) is triangular and
linear in A~_4's 23 parameters: ALWAYS SOLVABLE, 2 freedoms spare.
Realization therefore costs only ~9 conditions (U^3-polynomiality at
U = 0, ramification profile R' = kappa (v-a)^4 h(v)^2, marked
values).  The decision mass sits in the BRANCH LAYERS (attachment
conditions at the marked fibers of R and of the (-5)-Belyi map,
carrying Borisov's (e1, e2)) and in the KELLER condition.
"""
print(__doc__)
