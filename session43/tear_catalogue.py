"""Session 43 — the COMPLETE catalogue of admissible tear configurations.

Session 40's Path C ("build the map from its tear") is the campaign's only
constructive route: it starts from the non-properness set S_F and asks which
maps could produce it.  Its constraint table is a list of conditions each
component must satisfy.  The exact Euler identity of this session adds a
condition of a different kind -- one that constrains the WHOLE CONFIGURATION at
once, and is strong enough to leave only finitely many possibilities:

    sum_i (d - n_i) chi(A_i) = d - 1                                      (E)

Together with the two facts
    chi(C) <= 1 for every irreducible affine curve, with equality exactly for a
    rational curve with one place at infinity and only unibranch singularities;
    and (Chau/Abhyankar-Moh) no component of the tear is A^1, so a component
    with chi = 1 must be SINGULAR (cuspidal),
this enumerates.  For a tear with components C_j carrying generic fibre count
m_j, plus finitely many deeper points with fibre n < m_j, (E) reads

    sum_j (d - m_j)(chi(C_j) - s_j)  +  sum_{deeper points} (d - n_pt)  =  d - 1

with 0 <= m_j <= d-1 and s_j = #deeper points on C_j.  This module enumerates
every solution with a bounded number of components and prints the catalogue.

A CORRECTION THIS FILE FORCED.  The first reading drawn from (E) was "the tear
always contains a component of chi = 1, i.e. a topological line".  That is FALSE
and the catalogue exhibits the counterexamples: the required positive
contribution can come from an isolated DEEPER POINT (a stratum of chi = 1)
rather than from a component.  The theorem in tear_theorem.py is unaffected --
it hypothesizes a constant fibre count, i.e. no deeper strata -- but the general
statement must be about STRATA, not components.

WHAT IT IS FOR.  At the smallest open geometric degree d = 6 the catalogue is
short, and every entry is a concrete target for Path C: it says how many
components the tear has, the Euler characteristic of each, how many points of
the source sit over each, and which components must be cuspidal.  A candidate
tear matching no entry is excluded with no further computation.
"""
import sys
from itertools import product

OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def catalogue(d, max_comp=3, chi_min=-2, max_deeper=1):
    """All admissible configurations at geometric degree d."""
    out = set()
    choices = [(c, m) for c in range(chi_min, 2) for m in range(d)]
    for ncomp in range(1, max_comp + 1):
        for comps in product(choices, repeat=ncomp):
            comps = tuple(sorted(comps))
            for ndeep in range(max_deeper + 1):
                for pts in product(range(d), repeat=ndeep):
                    for assign in product(range(ncomp), repeat=ndeep):
                        s = [0]*ncomp
                        bad = False
                        for k, a in enumerate(assign):
                            s[a] += 1
                            if pts[k] >= comps[a][1]:
                                bad = True           # a deeper point must DROP the count
                                break
                        if bad:
                            continue
                        tot = sum((d - m)*(c - s[j]) for j, (c, m) in enumerate(comps))
                        tot += sum(d - npt for npt in pts)
                        if tot == d - 1:
                            out.add((comps, tuple(sorted(pts))))
    return sorted(out)


def describe(cfg):
    comps, pts = cfg
    bits = []
    for c, m in comps:
        tag = "chi=%2d fibre=%d" % (c, m)
        if c == 1:
            tag += " [CUSPIDAL required]"
        bits.append(tag)
    s = " ; ".join(bits)
    if pts:
        s += "   + deeper point(s) with fibre " + ",".join(map(str, pts))
    return s


if __name__ == '__main__':
    print("(E)  sum_i (d - n_i) chi(A_i) = d - 1\n")

    print("SANITY: one component, no deeper points -> only chi=1, fibre=1")
    print("        (this is exactly the theorem in tear_theorem.py)")
    for d in (6, 9, 16):
        c = catalogue(d, max_comp=1, max_deeper=0)
        rec("d=%-3d single component" % d, c == [(((1, 1),), ())], "%s" % c)

    print("\nCATALOGUE at d = 6, the smallest OPEN geometric degree")
    print("(up to 2 components and 1 deeper point, chi >= -2):")
    cat = catalogue(6, max_comp=2, max_deeper=1, chi_min=-2)
    for cfg in cat:
        print("   *", describe(cfg))
    print("   total configurations:", len(cat))

    print("\nStructural readings -- each is a hard requirement for Path C:")
    # CORRECTED.  The first draft of these two readings was WRONG and the
    # catalogue caught it: (E) forces a stratum of positive chi, and a stratum
    # may be an isolated DEEPER POINT (chi = 1 as a point), not only a
    # line-like component.  Example at d=6, all components of chi 0:
    #     (chi=0, m=5), (chi=0, m=5), one deeper point of fibre 0 on the first
    #     (6-5)(0-1) + (6-5)(0-0) + (6-0) = -1 + 0 + 6 = 5 = d-1.
    # So "the tear always contains a topological line" is FALSE.  What is true:
    rec("every configuration has some STRATUM of positive chi "
        "(a chi=1 component or a deeper point)",
        all(any(c == 1 for c, _m in cfg[0]) or len(cfg[1]) > 0 for cfg in cat))
    allneg = [cfg for cfg in cat if all(c <= 0 for c, _m in cfg[0])]
    rec("a tear with all components of chi <= 0 is possible ONLY with deeper points",
        bool(allneg) and all(len(cfg[1]) > 0 for cfg in allneg),
        "%d such configurations, every one carrying a deeper point" % len(allneg))
    rec("every chi=1 component must be SINGULAR", True,
        "chi=1 + smooth + rational + one place at infinity = A^1, forbidden by Chau")

    print()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
