# Literature batch 3 -- assessed, with honest value ratings

## 1. Campbell -- CORRECTION: this IS published
"On the Rational Real Jacobian Conjecture", Universitatis Iagellonicae
Acta Mathematica, Fasciculus LI (2013), doi:10.4467/20843828AM.13.001.2277.
(The arXiv note "too long to publish" refers to a longer manuscript; the
published paper is the one to cite.) arXiv:1202.2949
"Rational Jacobian conjectures" (real n-space, rational everywhere-defined
maps, NO constant-Jacobian requirement).
Abstract result: the associated rational function field extension "must be
of odd degree and must have no nontrivial automorphisms"; the Pinchuk
counterexamples to the strong REAL Jacobian conjecture have no nontrivial
automorphisms but are of degree six. Birational case proved; Galois case
clarified; general odd-degree case open.

VALUE TO US: LOW-MODERATE, and NOT transferable as stated. It is the real
rational setting, not complex polynomial n=2. The one idea worth carrying
over is structural: for a plane counterexample the extension
C(x,y)/C(P,Q) has degree = the geometric (generic) degree g >= 2, and
constraints of "non-Galois / no nontrivial automorphisms" type apply there
too. Our campaign already tracks that invariant: g in {2,3,4,5} is
excluded (Campbell/Orevkov/Domrina-Orevkov/Zoladek), g = 6 open. Campbell's
odd-degree conclusion does NOT import (different category of map), so it
does not exclude g = 6. Recorded, not used.

## 2. arXiv:2301.08221 = J. London Math. Soc. 113 (2026) e70416
Bisi, Dyszewski, Gantert, Johnston, Prochno, Schmid,
"Random planar trees and the Jacobian conjecture".
Reformulates JC via multi-type branching processes as a labelling problem
on rooted trees, then as shuffling subtrees of d-Catalan trees; shows that
if a certain Markov chain on large d-Catalan trees has uniform stationary
distribution, then JC is TRUE. Also an approximate version: inverses of
Keller maps have small high-degree power series coefficients.

VALUE TO US: LOW for counterexample-hunting, and worth being blunt about.
It is a strategy for PROVING the conjecture, not a test for refuting it,
and it yields no computable criterion that a given Keller map fails to
invert. The approximate result cuts the wrong way for us (it says inverse
coefficients are small, i.e. evidence toward JC holding). Useful as
context and for a future write-up; not an instrument.

## 3. The gist (Vitushkin "fake counterexample" note)
A cautionary explainer: Vitushkin's map has constant Jacobian -2 and is
non-injective, but contains 1/y, so it is NOT defined on all of C^2 and is
therefore not a counterexample. It also warns that any genuine
counterexample needs peer review, not a gist.

VALUE TO US: this is a VERIFICATION-STANDARD item and it is worth
honouring explicitly. Added to the endgame protocol:

  Before any candidate is called a counterexample, check that P and Q are
  honest polynomials in K[x,y] -- no denominators, no Laurent terms, no
  removable singularities -- so the map is defined on ALL of C^2. Our
  descent works in the reduced Laurent coordinates L^(1), so this check is
  NOT automatic for us: a candidate must be lifted back to original
  coordinates and confirmed polynomial there before anything is claimed.
  This is exactly the trap the gist describes, and our pipeline can fall
  into it if the lift step is skipped.

## Net

No new instrument from this batch. One real protocol tightening (item 3),
one structural note (item 1), one context paper (item 2). The three
instruments that DO have teeth remain: GGHV's reduction (the target),
McKay-Wang Cor 14 (the certificate), Le-Weber (the combinatorial sieve).


## ADDENDUM after reading the published Campbell paper in full

Contents confirmed: Prop 1 (geometric degree 1 => extension of odd degree
with trivial automorphism group); extension degree and maximum fiber size
have the same parity; Pinchuk maps have geometric degree 2, extension
degree 6, trivial automorphism group; Thm 1 (birational nonsingular =>
global inverse); Prop 2 (rational nonsingular + generically injective =>
invertible).

Still the REAL rational setting, so the odd-degree conclusion does not
import to complex plane JC and does NOT exclude geometric degree 6.

THE ONE TRANSFERABLE THREAD, and it is worth pursuing: Campbell's
discussion points at Jelonek's asymptotic variety A(F) (his refs 11,12,13)
-- the set where F fails to be proper. Facts he quotes: every connected
component of A(F) is unbounded and of positive dimension, and A(F) is
uniruled. In the COMPLEX plane case this is a genuine constraint on a
counterexample: a Keller map that is not an automorphism is not proper, so
A(F) is a nonempty curve, it is C-uniruled (parameterised by rational
curves), and Jelonek has degree bounds tying deg A(F) to the degrees of F.

This is the "Einstein's elevator" reframe parked in SWEEP_FRAMEWORKS.md.
It is now the best-supported unexplored lead: an independent numerical
constraint on the SAME (72,108) candidate, from a completely different
invariant than Newton polygons or resolution trees. Next step is to pull
Jelonek's actual bounds and check them against deg P = 72, deg Q = 108.

## 4. arXiv:1401.1784 (GGV, J. Algebra 471 (2017) 13-74)
"On the shape of possible counterexamples to the Jacobian Conjecture."
Already the BACKBONE of this campaign, used indirectly throughout: its
Theorem 8.10 is the B = 16 normal form our F-system lane is built on
(P = x^3 y + x^2 p2 + x p1 + p0, Q = x^2 y + x q1 + q0,
[P,Q] = x^4 y + mu3 x^3 + mu2 x^2 + mu1 x + mu0, mu0 != 0), and it is
reference [1] of GGHV 2022. It also contains the elementary proof of
Heitmann's B >= 16 and the result B != 2p for p prime.
Nothing new to extract -- confirming provenance, not a new lead.
