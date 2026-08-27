# Literature batch 3 -- assessed, with honest value ratings

## 1. arXiv:1202.2949 -- L.A. Campbell (2012, rev. 2013), unpublished
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
