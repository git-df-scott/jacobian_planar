# Cross-door theory notes — the two campaigns are one geometry (22:30Z pass)

New results from reading GGV [4] (Pro Mathematica 27) construction Sec 2
against GGHV, plus campaign data.  Checked tonight, not folklore.

## 1. The B=16 degree map (rigorous, from GGV [4] Sec 2, sixth step)

A solution of (1.2)+(1.3) in the cell deg(q1)=d constructs a counterexample
with EXACTLY
    deg(P) = 16m = 16(3d-2),   deg(Q) = 16n = 16(2d-1),
gcd(m,n)=1 always (gcd(3d-2,2d-1)=gcd(d-1,1)=1).  Consequences:

- **The two doors are disjoint.**  B = gcd(degrees) = 16 for the ladder;
  (72,108) has gcd 36.  A B=16 hit is NOT a (72,108) object and vice versa.
  Two independent CE programs; a hit in either suffices.
- **GGHV kills exactly d=2,3** of the ladder (max degrees 64, 112 < 125,
  and gcd 16 != 36 so not the surviving pair).  Our unconditional d=2,3
  EMPTYs are therefore an independent partial VERIFICATION of GGHV's
  (unrefereed) elimination on the B=16 slice.
- **d >= 4 cells live above GGHV's frontier** (max 160, 208, ... 544 at
  d=12).  The twin is unconstrained by GGHV; a twin hit means a CE of
  degrees (544, 368).
- **Byproduct nobody else has:** our d=5..12 EMPTY verdicts eliminate the
  specific above-125 degree pairs (208,144), (256,176), ..., (544,368) --
  territory NO published elimination covers (GGHV stops at 125).
  Publishable regardless of CE outcome.
- **Same asymptotic ray.**  16(3d-2):16(2d-1) -> 3:2 = 108:72.  The B=16
  line approaches exactly the ray of the surviving GGHV pair.  The two
  literatures study the same direction in degree space and never cite each
  other's constraints; GGHV's ray-specific polygon estimates plausibly
  transfer to the B=16 line (and would attack ALL d>=4 cells at once).
  This transfer has never been attempted by anyone.  [open project]

## 2. Resistance-is-geometry (campaign law, heuristic)

Every solver blowup we have hit co-occurred with positive-dimensional
degenerate structure: pentagon OOM <-> 2-torus grading; d12-unsat OOM <->
conjectured resonant family; the 16 unique TIMEOUT systems resist while
dozens of siblings die instantly.  (Counterexample to the naive law: d=3
unsat is instant AND has a family -- smallness wins there.)  Strategy
inversion: treat computational resistance as a TREASURE MAP -- for each of
the 16 resisters, first run the grading/torus finder (cheap exponent-vector
linear algebra, as done for pentagons), slice the torus, and look for the
degenerate locus; only then spend 1800s budgets.  Solving is secondary to
understanding WHY they resist, because the obstruction is where solutions
can hide.

## 3. The mu0-walk (operational form of the bifurcation program)

Cheapest version of Lyapunov-Schmidt: take a point on a mu0=0 degenerate
family mod p, and Newton/Hensel-iterate toward mu0 = eps != 0.  Each step
is one linear solve (34 vars at d=12) -- milliseconds, no Groebner, fixed
memory.  Obstruction = non-liftability at some finite step (a rank drop
against the mu0-direction).  Either a lifted point (-> CANDIDATE pipeline)
or a certified local obstruction.  Needs: an explicit family point, i.e.
the d=12 slice decomposition (queued with real memory post-twin).

## 4. Descent well-ordering (path to closing B=16 entirely)

Reframe the GGV conjecture as a well-founded descent: if solutions at cell
d descend to lower cells except at resonance obstructions, and resonances
exist only at d=3k^2 (our law, verified d=3..14), then B=16 reduces to
checking the resonant levels -- finitely many below any bound, each a
LOCAL computation (Sec 3).  Twin-EMPTY + 1/20-N-EMPTY + obstructed walks
at d=27, 48, 75 with a uniform pattern would be the skeleton of a THEOREM
closing B=16.  Nobody has formulated GGV's conjecture as a descent with
computable local obstructions.

## 5. Tail-closure (frontier finiteness)

Tonight's dedup found reduced systems depend only on the chain TAIL.
Predictor test: (last-2-segments, shape index) -> system hash has ZERO
violations across every system ever generated here (16 groups).  Current
library: 34 chains -> 26 distinct tails.  Conjecture: the tail set
SATURATES as max degree grows (tails are bounded final-polygon data), so
the 429-case frontier + beyond collapses to finitely many tail-systems,
most already decided.  If true, the chain-compiler extension only needs to
compute each case's TAIL, not its full chain -- an order-of-magnitude
cheaper build, and [125,300] becomes finite work.  Test: extend compiler
on 20 sample cases across (150,300], count new tails vs reused.

## 6. Nullstellensatz certificates for the 16 resisters

F4/facstd memory is unpredictable (cgroup kills); a degree-bounded
Nullstellensatz certificate search (1 = sum h_i f_i mod p) is a LINEAR
system in the h coefficients: streamable, fixed memory, parallel, and the
instant-empty siblings suggest low certificate degrees are typical in this
family.  One experiment at cert degree <= 3 on a resister decides
feasibility of the whole route.
