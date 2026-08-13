#!/usr/bin/env python3
"""P2 — leaf-1 sweep: the old campaign's slice, closed by us for the first time.

Leaf 1 of the sound elimination tree (d_2_2 := 0) is the slice the Sessions
19-20 r0-r6 hunt actually lived in. THEY closed it mod 65521 only, through the
unsound R1 pipeline; we have so far only edge-validated it. This runs our
staged, certificate-emitting pipeline on it at an arbitrary prime P = 1 mod 3
(env JCP), so that "case (2) fully audited" covers both leaves.

Structurally identical to trackB_prime_sweep.py (leaf 2). Two differences, both
read from trackA_reduced_system.json rather than hardcoded:
  - the leaf is id 1 (41 equations / 4 nonzero_exprs, nonzero = []), selected
    via JCLEAF before trackB_staged is imported;
  - the Newton-edge subsystem sits at equation indices [34..39] (leaf 2: [38..43]);
    trackB_staged derives the indices from the equations themselves.
All artifact/marker names carry the L1_ prefix so leaf-1 and leaf-2 runs at the
same prime coexist without colliding markers. Verdicts land in the log of
record, trackB_staged_verdicts.log, tagged L1_.
"""
import os, re, sys, time

os.environ.setdefault("JCLEAF", "1")          # must precede the import
import trackB_staged as S                     # noqa: E402
import trackB_r0 as R0                        # noqa: E402

P = S.P
assert S.LEAF_ID == 1, "leaf-1 sweep imported the wrong leaf"


def eliminant_factors():
    """Normalized (d_3_3 = 1) edge eliminant mod P, factored: one branch per
    irreducible factor. Leaf 1 shares leaf 2's edge subsystem, so the factor
    list is expected to agree — that agreement is itself a cross-check and is
    logged, not assumed."""
    mark = os.path.join(S.WD, f"trackB_L1_elim_p{P}.json")
    scr = [f"ring R = {P}, ({','.join(S.EDGE_VARS)}), lp;", "ideal I;"]
    n = 0
    for i in S.EDGE_IDX:
        n += 1
        scr.append(f"I[{n}] = {S.leaf['equations'][i]};")
    scr.append(f"I[{n+1}] = d_3_3-1;")
    scr += ["short=0;",
            "ideal E = eliminate(I, d_3_3*d_4_5*d_5_7*d_6_9*d_7_11*d_8_13);",
            '"ELIMDEG: " + string(deg(E[1]));',
            "list f = factorize(E[1]);", '"FACTORS:"; f[1];', "quit;"]
    out = S.sing("\n".join(scr), f"trackB_L1_elim_p{P}.sing", timeout=900)
    facs = []
    for ln in out.splitlines():
        m = re.match(r"_\[\d+\]=(.+)$", ln.strip())
        if m and m.group(1) != "1":
            facs.append(m.group(1))
    deg = [l for l in out.splitlines() if l.startswith("ELIMDEG")]
    if not facs:
        S.log(f"L1 SWEEP p={P}: eliminant factorization produced NO factors "
              f"(timeout/crash) — STALLED, no closure claimed")
        raise SystemExit("leaf-1 eliminant factorization did not complete")
    S.log(f"L1 SWEEP p={P}: eliminant {deg}, {len(facs)} irreducible factors")
    open(mark, "w").write(repr(facs))
    return facs


def main():
    t0 = time.time()
    facs = eliminant_factors()
    nonzero_facs = [f for f in facs if f != "d_9_15"]
    for k, f in enumerate(nonzero_facs):
        tag = f"L1_p{P}_rk{k}"
        s1 = S.stage1(tag, {"pin": "d_3_3-1", "factor": f})
        if len(s1["vals"]) == len(S.EDGE_VARS):
            S.stage2(tag, s1["vals"], 1)
        else:
            S.stage2b(tag, s1["vals"], s1["full_gb_lines"], 1)
    R0.close(f"L1_p{P}_r0a", "d_3_3-1", [], 1, 0)
    R0.close(f"L1_p{P}_r0b", "d_3_3", [], 0, 0)
    S.log(f"L1 SWEEP p={P}: COMPLETE in {time.time()-t0:.0f}s "
          f"({len(nonzero_facs)} eliminant branches + r0a + r0b)")


if __name__ == "__main__":
    main()
