#!/usr/bin/env python3
"""Le-Weber canonical-divisor sieve (Kodai Math. J. 17 (1994) 374-381).

Le Dung Trang & C. Weber prove: for a Jacobian pair (f,g), if w: Z -> P^2 is
a composition of point blow-ups over the line at infinity making
phi = F/T^d o w and psi = G/T^d' o w morphisms, then the divisor of
dphi ^ dpsi is a CANONICAL divisor of Z confined to infinity, and its
multiplicities are determined by the blow-up sequence alone -- independent
of phi and psi.

Corollary (their p.379): f is not a Jacobian polynomial if some dicritical
component D0 of phi is strongly non-equisingular AND its multiplicity in
that canonical divisor is strictly negative (then psi has a pole along D0,
so D0 cannot be a common dicritical component).

Multiplicity calculus used here (standard, and the controls below pin it):
  * K_{P^2} = -3L, so the line at infinity L starts at multiplicity -3.
  * Blowing up a FREE point (on exactly one divisor D, multiplicity m):
        the exceptional curve gets   m + 1.
  * Blowing up a SATELLITE point (the intersection of D1, D2 with
    multiplicities m1, m2):
        the exceptional curve gets   m1 + m2 + 1.
This is the usual discrepancy/adjunction bookkeeping for point blow-ups of
a surface, applied to the canonical class rather than to a curve.

The sieve: a component can only be a COMMON dicritical (which any
counterexample needs, by the Main Theorem's case analysis) if its
multiplicity is >= 0. Free blow-ups raise multiplicity by 1 each, so a
component reached by a free chain of length L off the line at infinity has
multiplicity -3 + L: it takes at least THREE free blow-ups to reach 0.
Satellite blow-ups between two negative divisors drive it more negative.
"""
import sys


class Tree:
    """Blow-up tree over the line at infinity, tracking K-multiplicities."""

    def __init__(self):
        self.mult = {"L": -3}          # line at infinity in P^2
        self.parent = {"L": None}
        self.kind = {"L": "line"}

    def blow_free(self, on, name):
        """Blow up a free point lying on exactly one component `on`."""
        self.mult[name] = self.mult[on] + 1
        self.parent[name] = (on,)
        self.kind[name] = "free"
        return name

    def blow_sat(self, on1, on2, name):
        """Blow up the intersection point of two components."""
        self.mult[name] = self.mult[on1] + self.mult[on2] + 1
        self.parent[name] = (on1, on2)
        self.kind[name] = "satellite"
        return name

    def report(self):
        return {k: self.mult[k] for k in self.mult}


def free_chain(length):
    """Multiplicity of the last component of a free chain off L."""
    T = Tree()
    prev = "L"
    for i in range(1, length + 1):
        prev = T.blow_free(prev, f"E{i}")
    return T.mult[prev], T


def controls():
    ok = True
    # C1: P^2 itself -- the 2-form dx^dy has a pole of order 3 at infinity.
    T = Tree()
    c1 = (T.mult["L"] == -3)
    print(f"C1 line at infinity has K-multiplicity -3: {'PASS' if c1 else 'FAIL'}")
    ok &= c1

    # C2: free chain arithmetic -- each free blow-up adds exactly 1, so
    # reaching multiplicity 0 requires a chain of length 3.
    vals = [free_chain(L)[0] for L in range(1, 6)]
    c2 = vals == [-2, -1, 0, 1, 2]
    print(f"C2 free chain multiplicities {vals} (expect [-2,-1,0,1,2]): "
          f"{'PASS' if c2 else 'FAIL'}")
    ok &= c2

    # C3: a satellite blow-up between L and its first exceptional curve is
    # MORE negative than either -- satellites cannot rescue a component.
    T = Tree()
    T.blow_free("L", "E1")
    T.blow_sat("L", "E1", "E2")
    c3 = T.mult["E2"] == -3 + -2 + 1 == -4
    print(f"C3 satellite(L,E1) multiplicity {T.mult['E2']} (expect -4): "
          f"{'PASS' if c3 else 'FAIL'}")
    ok &= c3
    return ok


def sieve_free_depth(depth, dicritical_is_strongly_nonequisingular=True):
    """Verdict for a dicritical component reached by `depth` free blow-ups."""
    m, _ = free_chain(depth)
    if m < 0 and dicritical_is_strongly_nonequisingular:
        return "KILLED", m, ("negative multiplicity -> psi has a pole there "
                             "-> cannot be a common dicritical (Le-Weber "
                             "Corollary, p.379)")
    return "SURVIVES", m, "multiplicity >= 0: the criterion gives no kill"


if __name__ == "__main__":
    print("=== controls ===")
    good = controls()
    print(f"multiplicity calculus: {'VALIDATED' if good else 'BROKEN'}\n")
    if not good:
        sys.exit(1)
    print("=== sieve applied to free-chain depths ===")
    for d in range(1, 6):
        v, m, why = sieve_free_depth(d)
        print(f"  depth {d}: multiplicity {m:+d}  -> {v}")
    print("\nReading: any candidate whose dicritical component sits within")
    print("two free blow-ups of the line at infinity is killed outright.")
    print("A counterexample needs a dicritical component at free-depth >= 3,")
    print("and satellite blow-ups only make multiplicities more negative.")
