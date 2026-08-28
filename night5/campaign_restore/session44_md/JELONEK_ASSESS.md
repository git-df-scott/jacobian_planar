# Jelonek non-properness lane -- assessed (active work, Session 44)

Motivation: JC2 is equivalent to "every Keller map is proper", since a
Keller map is an automorphism iff it is proper (proper + etale over the
simply connected C^2 forces degree 1). So a counterexample is exactly a
Keller map with non-empty Jelonek set S_F. This lane asks whether the
non-properness invariant constrains our (72,108) candidate.

## Bounds pulled

Jelonek: S_F is empty or a C-uniruled hypersurface, and for f: K^n -> K^n
    deg S_F <= (prod_i deg f_i - mu(f)) / min_i deg f_i .
For our target (deg P, deg Q) = (72,108) and geometric degree mu:
    deg S_F <= (7776 - mu)/72 = 108 - mu/72,
so deg S_F <= 107 for any mu >= 1. An upper bound only; not restrictive,
and it kills nothing by itself. Recorded so the arithmetic is not redone.

## El Hilany, arXiv:1909.07016 -- Jelonek set via Newton polytopes

Theorem 1.1: for T-boundary-generic ("T-BG") maps the equations of S_f are
computable from data on faces of the Newton polytopes alone. This is the
paper that composes with our polygon catalogue in principle.

**Corollary 1.3** (necessary condition for properness): if f is proper and
non-degenerate then New f_1 u ... u New f_n intersects all coordinate axes.

VERDICT ON COROLLARY 1.3: **vacuous for Keller maps** -- established here,
so it is not worth anyone's time later. If N(P) u N(Q) missed the y-axis,
then P(0,y) and Q(0,y) are both constant, hence P_y = Q_y = 0 along x = 0,
hence det J = P_x Q_y - P_y Q_x = 0 there, contradicting det J = c != 0.
Symmetrically for the x-axis. So a Keller map's polytopes always meet both
axes and the criterion never fires. (Our target does satisfy it: N(P) has
(3,0) and (0,12); N(Q) has (2,0) and (0,8).)

**Corollary 6.1** (sufficient condition for PROPERNESS, the interesting
direction): for a T-BG map, if New_f has no minimized almost semi-origin
tuples and all its minimized semi-origin tuples are basic, then f is
proper. For us properness would mean automorphism, i.e. the case DIES --
a cheap combinatorial kill if it applies.

CAVEAT, stated before any attempt: Corollary 6.1 requires f to be T-BG
(Definition 3.13), a genericity condition on how faces of the polytopes
meet. Our candidates are the opposite of generic -- they are highly
degenerate shapes with proportional leading forms (we showed the top-corner
bracket vanishes identically). So T-BG most likely FAILS for exactly the
maps we care about, and Corollary 6.1 would not apply. The paper's own
Remark 1.4 says extending beyond T-BG "would be the subject of a future
work", i.e. the non-generic case is open.

## Net assessment of this lane

- Cor 1.3: dead for Keller maps (proved above), no further work warranted.
- deg S_F bound: gives 107, not restrictive.
- Cor 6.1: the only live piece, but its hypothesis (T-BG) is precisely what
  our degenerate candidates are expected to violate. Checking T-BG for the
  (72,108) shape is the honest next step here, and a NEGATIVE result there
  closes the lane cleanly rather than leaving it as a vague "maybe".
- Still genuinely open and untouched: Jelonek's C-uniruledness of S_F. A
  counterexample's S_F must be a curve whose components are images of
  polynomial maps C -> C^2. That is a strong structural demand on a
  degree <= 107 curve and has never been checked against our candidate.
  Recorded as the successor lead in this lane.
