"""Generate chains beyond max degree 150 from the families' own growth law.

[C] arXiv:1708.07936 Sec.5 lists 17 length-1 and 7 length-2 FAMILIES.  Each is
not a single chain but an infinite one-parameter family: the corners are fixed
and the cusp type grows linearly,

    F1 : A_0 = (4,12),  A'_0 = (1,0),  A_1 = (7|4, 3),   m = 2j+3, n = 3j+4
    F2 : A_0 = (5,20),  A'_0 = (1,0),  A_1 = (7|5, 2),   m = j+2,  n = 2j+3
    ...

so max(deg P, deg Q) = max(m(j), n(j)) * v11(A_0) grows linearly in j and the
horizon is only capped by where we stop.  Sec.6's table lists the 13 family
instances with max <= 150; this module regenerates those and continues.

COMPLETENESS, stated precisely.  Sec.6 claims completeness of its 34-shape list
only for max <= 150, and that list is produced by Algorithm 8 restricted to
v11(A_0) <= 35.  So:

  * the family instances generated here are EXACT -- they are the same chains
    Sec.6 tabulates, evaluated at larger j, and reproducing the 13 tabulated
    rows is the regression test below;
  * beyond 150 they are NOT a complete enumeration.  Non-family chains
    (Sec.6's 21 explicit rows are of that kind) would need Algorithms 6/8/9
    -- valid edges, children, admissibility -- reimplemented, which is not
    done here.  Anything this module emits above 150 is a candidate source,
    not a closed catalogue.

Two exclusions are the paper's own, not mine:
  * F18-F21: "we claim that the families F18, F19, F20 and F21 can not be
    obtained from a standard (m,n)-pair (P,Q)" ([C], just below the table).
  * F22: discarded in [C] Prop 6.1.
They are generated but flagged, so nothing is silently dropped.
"""
import sys
from trackD_chain_map import C, Chain, reduced_candidates, check_eps

# family: (A_0, A'_0, [intermediate corners...], terminal, m(j), n(j), flag)
FAM = {
    "F1":  (C(4,1,12),  C(1,1,0), [], C(7,4,3),   lambda j:2*j+3, lambda j:3*j+4,  ""),
    "F2":  (C(5,1,20),  C(1,1,0), [], C(7,5,2),   lambda j:j+2,   lambda j:2*j+3,  ""),
    "F3":  (C(5,1,20),  C(1,1,0), [], C(8,5,3),   lambda j:4*j+3, lambda j:3*j+2,  ""),
    "F4":  (C(5,1,20),  C(1,1,0), [], C(8,5,3),   lambda j:2*j+3, lambda j:12*j+16,""),
    "F5":  (C(5,1,20),  C(1,1,0), [], C(9,5,4),   lambda j:7*j+9, lambda j:4*j+5,  ""),
    "F6":  (C(5,1,20),  C(1,1,0), [], C(9,5,4),   lambda j:3*j+4, lambda j:8*j+10, ""),
    "F7":  (C(6,1,15),  C(1,1,0), [], C(7,3,4),   lambda j:j+2,   lambda j:4*j+7,  ""),
    "F8":  (C(6,1,15),  C(1,1,0), [], C(8,3,5),   lambda j:2*j+3, lambda j:5*j+7,  ""),
    "F9":  (C(7,1,21),  C(1,1,0), [], C(11,7,2),  lambda j:j+2,   lambda j:2*j+3,  ""),
    "F10": (C(7,1,21),  C(1,1,0), [], C(13,7,3),  lambda j:5*j+7, lambda j:3*j+4,  ""),
    "F11": (C(7,1,21),  C(1,1,0), [], C(13,7,3),  lambda j:j+2,   lambda j:3*j+5,  ""),
    "F12": (C(8,1,24),  C(2,1,0), [], C(13,4,5),  lambda j:2*j+3, lambda j:5*j+7,  ""),
    "F13": (C(9,1,21),  C(2,1,0), [], C(13,3,7),  lambda j:j+2,   lambda j:7*j+13, ""),
    "F14": (C(9,1,24),  C(1,1,0), [], C(7,3,4),   lambda j:j+2,   lambda j:4*j+7,  ""),
    "F15": (C(9,1,24),  C(1,1,0), [], C(8,3,5),   lambda j:2*j+3, lambda j:5*j+7,  ""),
    "F16": (C(9,1,24),  C(1,1,0), [], C(10,3,7),  lambda j:4*j+3, lambda j:7*j+5,  ""),
    "F17": (C(9,1,24),  C(1,1,0), [], C(11,3,8),  lambda j:5*j+2, lambda j:8*j+3,  ""),
    "F18": (C(6,1,18),  C(1,1,0), [C(6,1,15)], C(7,3,4), lambda j:j+2,  lambda j:4*j+7,
            "excluded by [C]: not obtainable from a standard (m,n)-pair"),
    "F19": (C(6,1,18),  C(1,1,0), [C(6,1,15)], C(8,3,5), lambda j:2*j+3, lambda j:5*j+7,
            "excluded by [C]: not obtainable from a standard (m,n)-pair"),
    "F20": (C(6,1,24),  C(1,1,0), [C(6,1,15)], C(7,3,4), lambda j:j+2,  lambda j:4*j+7,
            "excluded by [C]: not obtainable from a standard (m,n)-pair"),
    "F21": (C(6,1,24),  C(1,1,0), [C(6,1,15)], C(8,3,5), lambda j:2*j+3, lambda j:5*j+7,
            "excluded by [C]: not obtainable from a standard (m,n)-pair"),
    "F22": (C(8,1,24),  C(2,1,0), [C(14,4,6)], C(5,4,2), lambda j:j+2,  lambda j:2*j+3,
            "excluded by [C] Prop 6.1"),
    "F23": (C(8,1,24),  C(2,1,0), [C(14,4,6)], C(11,4,4), lambda j:j+2, lambda j:4*j+7, ""),
    "F24": (C(8,1,24),  C(2,1,0), [C(14,4,6)], C(19,8,3), lambda j:2*j+3, lambda j:3*j+4, ""),
}

# the 13 family instances [C] Sec.6 tabulates, for the regression test
SEC6 = {("F1",3,4):64, ("F1",5,7):112, ("F2",2,3):75, ("F2",3,5):125,
        ("F3",3,2):75, ("F7",2,7):147, ("F8",3,7):147, ("F9",2,3):84,
        ("F9",3,5):140, ("F11",2,5):140, ("F17",2,3):99, ("F22",2,3):96,
        ("F24",3,4):128}


def generate(maxdeg=300, jmax=200, include_excluded=False):
    out = []
    for fam, (A0, Ap, mid, term, mf, nf, flag) in FAM.items():
        if flag and not include_excluded:
            continue
        v11 = A0[0] + A0[2]
        for j in range(jmax + 1):
            m, n = mf(j), nf(j)
            mx = max(m, n) * v11
            if mx > maxdeg:
                break
            corners = [A0] + list(mid) + [term]
            out.append(Chain(f"{fam}(j={j};m,n={m},{n})", corners, Ap, (m, n),
                             mx, f"[C] Sec.5 {fam} generated"))
    out.sort(key=lambda c: c.maxdeg)
    return out


def regression():
    """Every family instance [C] Sec.6 tabulates must be regenerated, with the
    same max degree."""
    gen = {(c.name.split("(")[0], c.m, c.n): c.maxdeg
           for c in generate(maxdeg=200, include_excluded=True)}
    ok = 0
    for (fam, m, n), mx in sorted(SEC6.items()):
        got = gen.get((fam, m, n))
        mark = "ok" if got == mx else f"MISMATCH got {got}"
        ok += got == mx
        print(f"    {fam:4s} (m,n)=({m},{n})  max {mx:4d}  {mark}")
    print(f"  regenerated {ok}/{len(SEC6)} of Sec.6's tabulated family rows")
    return ok == len(SEC6)


if __name__ == "__main__":
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print("=== regression: regenerate [C] Sec.6's 13 family rows ===")
    regression()
    print(f"\n=== generated chains with max <= {bound} ===")
    chains = generate(bound)
    above = [c for c in chains if c.maxdeg > 150]
    print(f"  {len(chains)} family instances, {len(above)} of them ABOVE 150")
    tot_shapes = 0
    rows = []
    for ch in above:
        cands, notes = reduced_candidates(ch)
        kept = [c for c in cands if check_eps(c)[0]]
        tot_shapes += len(kept)
        rows.append((ch, len(cands), len(kept), notes))
    print(f"  eps-passing reduced shapes from the >150 chains: {tot_shapes}\n")
    print(f"  {'chain':30s} {'max':>5s} {'deg pair':>14s} {'shapes':>6s}")
    for ch, nc, nk, notes in rows[:40]:
        dP, dQ = ch.degrees()
        note = "" if nk else ("   " + (notes[0][:44] if notes else "no shape"))
        print(f"  {ch.name[:30]:30s} {ch.maxdeg:5d} {str((dP,dQ)):>14s} "
              f"{nk:6d}{note}")
    if len(rows) > 40:
        print(f"  ... and {len(rows)-40} more")
    print("\n  NOTE: complete only as FAMILY instances.  [C] Sec.6's "
          "completeness claim stops at 150, and its 21 non-family rows would "
          "need Algorithms 6/8/9 reimplemented to continue.")
