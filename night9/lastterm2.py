"""night9 — LAST-TERM KILL, widened.

Measurements only.  Every result is labelled with its characteristic or with
the ring it was computed in.  No assessment of what any of these numbers mean
is offered.  Every object produced is filed CANDIDATE-UNVERIFIED.

WHAT THIS ADDS TO night9/lastterm.py.

  (i)  TWO-TERM CASES DO NOT EXIST.  Over all 882 matched lifts recorded in
       night9/altitude/, the number of monomials in the exact integer residual
       R = P_x Q_y - P_y Q_x - 1 takes the values 1 (88 lifts), 3 (474),
       5 (256), 6 (16), 7 (48).  There is NO lift with a two-term residual.
       The prescribed two-term kill is therefore run on the smallest existing
       multi-term class, the THREE-TERM residuals, with the box taken over the
       UNION of all three terms' feeding coefficients.  This substitution is
       recorded here, not silently made.

  (ii) WIDENED BOX.  For every case, in addition to the [-4..4] box on the
       full feeding set, a [-9..9] box is run on the AT MOST FOUR MOST
       INFLUENTIAL feeding coefficients, the rest held at their lift values.
       INFLUENCE of a coefficient is defined as

           infl(a_i) = sum over the non-zero residual rows e of
                       | d v_e / d a_i |   evaluated at the lift,

       and symmetrically for b_j, where v_e is the exact integer value of row
       e.  Ties are broken by index.  This definition is a choice made here
       and is recorded as such.

  (iii) GLOBAL BEST tracked across every case and every box point: the minimum
        number of non-zero residual rows achieved WITH BOTH COLLISION
        EQUALITIES INTACT over Z, and an exact attaining pair (P, Q).

        DEGENERATE AND VACUOUS POINTS ARE EXCLUDED FROM THE GLOBAL BEST.
        Points failing the additive degeneracy screen of
        keller_solver.degenerate_screen are reported but do not set the global
        best; a second global best over the merely non-vacuous stratum is
        reported alongside.

        VACUOUS POINTS ARE EXCLUDED FROM THE GLOBAL BEST.  A box point at
        which the bracket [P,Q] = P_x Q_y - P_y Q_x is IDENTICALLY ZERO (for
        instance P identically 0) has residual equal to the constant -1: one
        non-zero row, content 1.  That is the far end of the landscape, not a
        near miss, so the global best is taken over the stratum
        "collisions intact AND bracket not identically zero".  The vacuous
        points are still counted and reported separately.

HALT EVENT (protocol unchanged): an assignment whose FULL residual over Z is
identically zero on ALL rows AND whose two collision differences are both
zero.  Reported paths-only if it occurs.

All residual arithmetic is exact integer arithmetic.  The box scan is
vectorised over int64 numpy arrays -- exact for these magnitudes, and every
short-listed point is re-verified in pure Python integers before being
recorded.

Outputs: night9/lastterm2/<hash>_<i>.json, night9/lastterm2_index.json.
"""
import json
import os
import sys
from itertools import product
from math import gcd

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from keller_solver import build_system, degenerate_screen  # noqa: E402

BOX4 = list(range(-4, 5))
BOX9 = list(range(-9, 10))
TOPK = 4
SHORTLIST = 40
FULLBOX_POINT_CAP = 300000


# ------------------------------------------------------------ exact python

def rows_over_Z(eqs, pairs, a, b):
    out = {}
    for e in eqs:
        v = 0
        for (mi, ni, c) in pairs[e]:
            v += c * a[mi] * b[ni]
        if e == (0, 0):
            v -= 1
        if v:
            out[e] = v
    return out


def collisions_over_Z(SP, SQ, a, b):
    cP = sum(a[i] for i, m in enumerate(SP) if m[0] == 0) - \
        sum(a[i] for i, m in enumerate(SP) if m[1] == 0)
    cQ = sum(b[j] for j, n in enumerate(SQ) if n[0] == 0) - \
        sum(b[j] for j, n in enumerate(SQ) if n[1] == 0)
    return cP, cQ


def content(rows):
    g = 0
    for v in rows.values():
        g = gcd(g, abs(v))
    return g


def poly_str(S, coef):
    ts = []
    for m, c in zip(S, coef):
        if not c:
            continue
        mon = ""
        if m[0]:
            mon += "*x^%d" % m[0]
        if m[1]:
            mon += "*y^%d" % m[1]
        ts.append("%+d%s" % (c, mon))
    return "".join(ts) if ts else "0"


# ------------------------------------------------------------- vectorised

def scan(eqs, pairs, SP, SQ, a0, b0, varlist, box):
    """Exhaustive scan of `box`^len(varlist).  Returns (nrows, collP, collQ,
    grids) as flat int64 arrays over the grid."""
    k = len(varlist)
    mesh = np.meshgrid(*([np.array(box, dtype=np.int64)] * k), indexing="ij")
    G = [m.ravel() for m in mesh]
    N = G[0].size
    amap, bmap = {}, {}
    for t, (side, idx) in enumerate(varlist):
        (amap if side == "a" else bmap)[idx] = G[t]

    def av(i):
        return amap[i] if i in amap else np.int64(a0[i])

    def bv(j):
        return bmap[j] if j in bmap else np.int64(b0[j])

    nrows = np.zeros(N, dtype=np.int64)
    nbracket = np.zeros(N, dtype=np.int64)   # non-zero rows of [P,Q] itself
    for e in eqs:
        v = np.zeros(N, dtype=np.int64)
        for (mi, ni, c) in pairs[e]:
            v = v + np.int64(c) * av(mi) * bv(ni)
        nbracket += (v != 0)
        if e == (0, 0):
            v = v - 1
        nrows += (v != 0)
    cP = np.zeros(N, dtype=np.int64)
    for i, m in enumerate(SP):
        s = (1 if m[0] == 0 else 0) - (1 if m[1] == 0 else 0)
        if s:
            cP = cP + np.int64(s) * av(i)
    cQ = np.zeros(N, dtype=np.int64)
    for j, n in enumerate(SQ):
        s = (1 if n[0] == 0 else 0) - (1 if n[1] == 0 else 0)
        if s:
            cQ = cQ + np.int64(s) * bv(j)
    return nrows, cP, cQ, G, nbracket


def assignment_at(a0, b0, varlist, G, t):
    a, b = list(a0), list(b0)
    for u, (side, idx) in enumerate(varlist):
        v = int(G[u][t])
        if side == "a":
            a[idx] = v
        else:
            b[idx] = v
    return a, b


def examine(tag, eqs, pairs, SP, SQ, a0, b0, varlist, box):
    """Run one box and return the record for it, exact-verifying shortlisted
    points in pure Python integers."""
    npoints = len(box) ** len(varlist)
    if npoints > FULLBOX_POINT_CAP:
        return {"box_tag": tag, "variables": [list(v) for v in varlist],
                "box": "[%d..%d]" % (box[0], box[-1]),
                "points": npoints, "status": "NOT-ATTEMPTED-point-cap",
                "point_cap": FULLBOX_POINT_CAP}
    nrows, cP, cQ, G, nbracket = scan(eqs, pairs, SP, SQ, a0, b0,
                                      varlist, box)
    coll = (cP == 0) & (cQ == 0)
    nonvac = nbracket > 0
    # degeneracy depends only on the zero-pattern of the varying coordinates
    N = nrows.size
    nz = [(g != 0) for g in G]
    degmask = np.zeros(N, dtype=bool)
    for bits in range(1 << len(varlist)):
        a, b = list(a0), list(b0)
        sel = np.ones(N, dtype=bool)
        for t, (side, idx) in enumerate(varlist):
            on = bool((bits >> t) & 1)
            if side == "a":
                a[idx] = 1 if on else 0
            else:
                b[idx] = 1 if on else 0
            sel &= (nz[t] if on else ~nz[t])
        if sel.any() and degenerate_screen(SP, SQ, a, b)[0]:
            degmask |= sel
    nondeg = ~degmask
    zero_all = int((nrows == 0).sum())
    zero_coll = int(((nrows == 0) & coll).sum())

    halts = []
    if zero_coll:
        for t in np.nonzero((nrows == 0) & coll)[0][:SHORTLIST]:
            a, b = assignment_at(a0, b0, varlist, G, int(t))
            R = rows_over_Z(eqs, pairs, a, b)
            dP, dQ = collisions_over_Z(SP, SQ, a, b)
            if not R and dP == 0 and dQ == 0:
                halts.append({"a": a, "b": b,
                              "degenerate_by_additive_screen":
                                  degenerate_screen(SP, SQ, a, b)[0],
                              "P": poly_str(SP, a), "Q": poly_str(SQ, b)})

    out = {"box_tag": tag, "variables": [list(v) for v in varlist],
           "box": "[%d..%d]" % (box[0], box[-1]), "points": npoints,
           "status": "COMPLETE",
           "assignments_with_residual_identically_zero_over_Z": zero_all,
           "of_those_with_collisions_intact": zero_coll,
           "HALT_EVENTS": halts, "n_halt_events": len(halts)}

    out["assignments_with_bracket_identically_zero"] = int((~nonvac).sum())
    out["assignments_degenerate_by_additive_screen"] = int(degmask.sum())
    for name, mask in (("all", np.ones_like(coll)),
                       ("collisions_ok", coll),
                       ("collisions_ok_and_bracket_nonzero", coll & nonvac),
                       ("collisions_ok_bracket_nonzero_nondegenerate",
                        coll & nonvac & nondeg)):
        if not mask.any():
            out["min_" + name] = None
            continue
        sel = np.nonzero(mask)[0]
        mn = int(nrows[sel].min())
        cand = sel[nrows[sel] == mn][:SHORTLIST]
        best = None
        for t in cand:
            a, b = assignment_at(a0, b0, varlist, G, int(t))
            R = rows_over_Z(eqs, pairs, a, b)
            assert len(R) == mn, "vectorised scan disagreed with exact recount"
            dP, dQ = collisions_over_Z(SP, SQ, a, b)
            g = content(R)
            key = (len(R), g)
            if best is None or key < best[0]:
                best = (key, a, b, dP, dQ, R,
                        degenerate_screen(SP, SQ, a, b)[0])
        out["min_" + name] = {
            "min_nonzero_residual_rows": best[0][0],
            "content_gcd_at_minimum": best[0][1],
            "attaining_assignment": {"a": best[1], "b": best[2]},
            "P": poly_str(SP, best[1]), "Q": poly_str(SQ, best[2]),
            "collision_P_diff_over_Z": best[3],
            "collision_Q_diff_over_Z": best[4],
            "collisions_hold_over_Z": best[3] == 0 and best[4] == 0,
            "residual_rows_there": {str(k): v for k, v in best[5].items()},
            "degenerate_by_additive_screen": best[6],
            "bracket_identically_zero": all(
                sum(c * best[1][mi] * best[2][ni]
                    for (mi, ni, c) in pairs[e]) == 0 for e in eqs),
        }
    return out


# ------------------------------------------------------------------ main

def main():
    outdir = os.path.join(HERE, "lastterm2")
    os.makedirs(outdir, exist_ok=True)
    want = {1, 3}
    cases = []
    seen = set()
    global_best = None
    global_best_vac = None
    halt_paths = []

    files = sorted(os.listdir(os.path.join(HERE, "altitude")))
    for f in files:
        d = json.load(open(os.path.join(HERE, "altitude", f)))
        SP = [tuple(m) for m in d["support_P"]]
        SQ = [tuple(m) for m in d["support_Q"]]
        eqs, pairs, cP0, cQ0 = build_system(SP, SQ)
        for i, z in enumerate(d["matched_lifts_over_Z"]):
            nt = z["residual_n_terms"]
            if nt not in want:
                continue
            a0 = list(z["balanced_lift_mod_6"]["a"])
            b0 = list(z["balanced_lift_mod_6"]["b"])
            key = (d["hash"], tuple(a0), tuple(b0))
            if key in seen:
                continue
            seen.add(key)
            R0 = rows_over_Z(eqs, pairs, a0, b0)
            assert len(R0) == nt

            # feeding set = union over the non-zero residual rows
            feed = set()
            infl = {}
            for e in R0:
                for (mi, ni, c) in pairs[e]:
                    feed.add(("a", mi))
                    feed.add(("b", ni))
                    infl[("a", mi)] = infl.get(("a", mi), 0) + abs(c * b0[ni])
                    infl[("b", ni)] = infl.get(("b", ni), 0) + abs(c * a0[mi])
            feed = sorted(feed)
            top = sorted(feed, key=lambda v: (-infl.get(v, 0), v))[:TOPK]
            top = sorted(top)

            boxes = [examine("full-feeding-set/[-4..4]", eqs, pairs, SP, SQ,
                             a0, b0, feed, BOX4),
                     examine("top%d-influential/[-9..9]" % len(top), eqs,
                             pairs, SP, SQ, a0, b0, top, BOX9)]
            if len(feed) <= TOPK:
                boxes.append(examine("full-feeding-set/[-9..9]", eqs, pairs,
                                     SP, SQ, a0, b0, feed, BOX9))

            rec = {
                "label": "CANDIDATE-UNVERIFIED",
                "hash": d["hash"], "lift_index_in_altitude_json": i,
                "max_total_degree": d["max_total_degree"],
                "ring": "Z (exact integer arithmetic)",
                "support_P": [list(m) for m in SP],
                "support_Q": [list(m) for m in SQ],
                "lift_mod_6": {"a": a0, "b": b0},
                "residual_n_terms": nt,
                "residual_rows_at_lift":
                    {str(k): v for k, v in R0.items()},
                "feeding_set": [list(v) for v in feed],
                "influence_at_lift":
                    {"%s_%d" % v: infl[v] for v in feed},
                "most_influential_used_for_the_wide_box":
                    [list(v) for v in top],
                "boxes": boxes,
            }
            path = os.path.join(outdir, "%s_%d.json" % (d["hash"], i))
            with open(path, "w") as g:
                json.dump(rec, g, indent=1)

            nh = sum(bx.get("n_halt_events", 0) for bx in boxes)
            if nh:
                halt_paths.append(path)
            bc = None
            bd = None
            for bx in boxes:
                m = bx.get("min_collisions_ok_bracket_nonzero_nondegenerate")
                if m is None:
                    continue
                k2 = (m["min_nonzero_residual_rows"],
                      m["content_gcd_at_minimum"])
                if bc is None or k2 < bc[0]:
                    bc = (k2, bx["box_tag"], m)
            for bx in boxes:
                m = bx.get("min_collisions_ok_and_bracket_nonzero")
                if m is None:
                    continue
                k3 = (m["min_nonzero_residual_rows"],
                      m["content_gcd_at_minimum"])
                if bd is None or k3 < bd[0]:
                    bd = (k3, bx["box_tag"], m)
            if bd and (global_best_vac is None or
                       bd[0] < global_best_vac["key"]):
                global_best_vac = {"key": bd[0], "hash": d["hash"],
                                   "lift_index": i, "box_tag": bd[1],
                                   "file": os.path.relpath(path, HERE),
                                   "detail": bd[2]}
            if bc and (global_best is None or
                       bc[0] < global_best["key"]):
                global_best = {"key": bc[0], "hash": d["hash"],
                               "lift_index": i, "box_tag": bc[1],
                               "file": os.path.relpath(path, HERE),
                               "detail": bc[2],
                               "support_P": [list(m) for m in SP],
                               "support_Q": [list(m) for m in SQ]}
            cases.append({
                "hash": d["hash"], "i": i, "residual_n_terms": nt,
                "feeding_set_size": len(feed), "n_halt_events": nh,
                "min_rows_collisions_ok": bc[0][0] if bc else None,
                "min_content_collisions_ok": bc[0][1] if bc else None,
                "points_scanned": sum(bx["points"] for bx in boxes
                                      if bx["status"] == "COMPLETE"),
                "file": os.path.relpath(path, HERE)})
            print("%s#%-3d terms=%d feed=%d pts=%d halts=%d  best(rows,content)=(%s,%s)"
                  % (d["hash"], i, nt, len(feed),
                     cases[-1]["points_scanned"], nh,
                     cases[-1]["min_rows_collisions_ok"],
                     cases[-1]["min_content_collisions_ok"]), flush=True)

    idx = {
        "two_term_residual_cases_exist": False,
        "note_on_substitution":
            "No matched lift has a two-term residual; the prescribed two-term "
            "kill was run on the three-term class instead, with the box over "
            "the union of all three terms' feeding coefficients.",
        "residual_term_multiset_over_all_882_lifts":
            {"1": 88, "3": 474, "5": 256, "6": 16, "7": 48},
        "cases_run": len(cases),
        "total_points_scanned": sum(c["points_scanned"] for c in cases),
        "total_halt_events": sum(c["n_halt_events"] for c in cases),
        "halt_event_files": halt_paths,
        "GLOBAL_BEST_collisions_intact_bracket_nonzero_NONDEGENERATE":
            global_best,
        "GLOBAL_BEST_collisions_intact_bracket_nonzero_any_degeneracy":
            global_best_vac,
        "cases": cases,
    }
    with open(os.path.join(HERE, "lastterm2_index.json"), "w") as g:
        json.dump(idx, g, indent=1)
    print("\ncases=%d  points=%d  HALT events=%d"
          % (len(cases), idx["total_points_scanned"],
             idx["total_halt_events"]))
    print("GLOBAL BEST (collisions intact, bracket nonzero, NON-DEGENERATE):",
          global_best["key"] if global_best else None)
    print("GLOBAL BEST (collisions intact, bracket nonzero, any degeneracy):",
          global_best_vac["key"] if global_best_vac else None)


if __name__ == "__main__":
    main()
