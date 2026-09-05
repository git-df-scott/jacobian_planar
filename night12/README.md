# night12 -- mate search lane

Measurements only. See `MATE_SEARCH.md` for the construction, the support
design, the decision procedure and the tallies.

## Expected-outcome calibration (written before the sweep was read)

The calibration below is the yardstick the sweep is read against. It is a
statement of what the classical picture predicts, recorded so that the
measured tallies can be compared to something fixed rather than to a
post-hoc story.

1. **If the classical theory holds**, a consistent system occurs exactly when
   `P` is a coordinate -- a component of a polynomial automorphism of the
   plane -- and then every `Q` solving `P_x Q_y - P_y Q_x = 1` differs from a
   genuine second coordinate by an element of the kernel, i.e. by `f(P)` for
   `f` a one-variable polynomial (note `[P, f(P)] = 0`, which is why `A` is
   expected to have corank at least 1 whenever `supp(P)` sits inside the
   `Q`-support).

2. **Therefore, under that picture, every exactly verified pair `(P,Q)` found
   at any degree should have a divisibility-ordered degree pair**
   (Jung--van der Kulk), and the calibration arm `deg P in {4,6,9}` should
   produce consistent systems only on the coordinate family `F_coord` and on
   whatever other `P` in the sweep happens to be a coordinate.

3. **A generic `P` should be inconsistent.** The system is heavily
   overdetermined -- the bracket has `O(d * deg Q)` rows against `O(n)`
   unknowns -- so consistency is a codimension-large condition. Control C4
   (a random dense `P` of degree 5) is the instance of this that is measured.

4. **The recorded quantity of interest** is any consistent system at
   `deg P in {84, 96, 108, 126}` whose exact solution `Q` produces a
   **non-divisibility-ordered** degree pair with `P` (e.g. `(84,126)`).
   The count of these is reported in `MATE_SEARCH.md` section 7 and each one,
   if any, is committed to `night12/HIT_<hash>/` under the halt-and-commit
   protocol. This lane reports the count and the paths and stops there.

## Scope statement

Every negative verdict in this lane is a verdict about a **bounded** `Q`-support
(section 2 of `MATE_SEARCH.md`), recorded per `P` as `n_full_support`,
`thin_k` and `n_unknowns`, and about the two primes named. It is not a
statement about all `Q`.
