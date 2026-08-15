"""Chain data -> eps filter -> y-adic / dual-number engine, for all 34 shapes.

Stage 1  trackD_chain_map.reduced_candidates  (validated 6/6 on GGHV Sec.4)
Stage 2  trackD_chain_map.check_eps           eps_P + eps_Q = (r+1,1), and the
                                              j=0 row shape the engine needs
Stage 3  trackB1_shapes.run_pair              y-adic recursion + exact Jacobian
                                              rank over F_p[e]/(e^2)

Chains whose rules do not close (non-integer twist exponent c_t, unknown A'_t,
eps absorbed into the base) are NOT reported as discarded -- they are re-run in
superset mode, where r and c' are enumerated over bounded ranges, so that a
shape is never silently dropped.  A missed shape costs a counterexample; a
spurious shape costs one machine run.
"""
import sys, random, time, json
import trackD_chain_map as CM
from trackD_chain_map import (all_chains, reduced_candidates, check_eps,
                              hull, lattice, validate)
import trackB1_shapes as SH
from trackB1_polygon import hull_rows


def npoints(verts):
    return len(lattice(verts))


def superset_candidates(ch, rmax=8):
    """Bounded enumeration for chains the derived rules do not close."""
    a = ch.terminal[1]
    b = ch.terminal[2] + 1
    if b <= 1:
        return []
    mp, np_ = sorted((ch.m, ch.n))
    out = []
    for cprime in range(0, b + 1):
        base = [(0, 0), (a, b - 1), (a, b)]
        if cprime > 0:
            base.append((0, cprime))
        for r in range(1, rmax + 1):
            for swap in (False, True):
                eP, eQ = ((r, 1), (1, 0)) if not swap else ((1, 0), (r, 1))
                NP = hull([(mp * i, mp * j) for (i, j) in base] + [eP])
                NQ = hull([(np_ * i, np_ * j) for (i, j) in base] + [eQ])
                if eP not in NP or eQ not in NQ:
                    continue
                out.append(dict(chain=ch, a=a, b=b, cprime=cprime, r=r,
                                mp=mp, np=np_, epsP=eP, epsQ=eQ,
                                NP=NP, NQ=NQ, notes=["superset mode"]))
    return out


def degree_crosscheck():
    """(m,n)*v11(A_0) must reproduce the paper's max column for all 34 rows."""
    bad = []
    for ch in all_chains():
        dP, dQ = ch.degrees()
        if max(dP, dQ) != ch.maxdeg:
            bad.append((ch.name, (dP, dQ), ch.maxdeg))
    return bad


def build_all(rmax=8):
    shapes = []
    for ch in all_chains():
        cands, notes = reduced_candidates(ch)
        kept = [c for c in cands if check_eps(c)[0]]
        mode = "derived"
        if not kept:
            cands = superset_candidates(ch, rmax)
            kept = [c for c in cands if check_eps(c)[0]]
            mode = "superset"
        for c in kept:
            c["mode"] = mode
            c["size"] = npoints(c["NP"]) + npoints(c["NQ"])
            shapes.append(c)
    return shapes


def run_one(cd, rng, jextra=2):
    ch = cd["chain"]
    name = (f"{ch.name} | a={cd['a']} b={cd['b']} c'={cd['cprime']} "
            f"r={cd['r']} eps=({cd['epsP']},{cd['epsQ']}) [{cd['mode']}]")
    pair = SH.Pair(name, cd["NP"], cd["NQ"], [(cd["r"], 0, 1)],
                   f"orig deg {ch.degrees()}, max {ch.maxdeg}")
    t0 = time.time()
    try:
        res = SH.run_pair(pair, rng, jextra=jextra)
    except Exception as ex:
        return dict(name=name, status="ERROR", detail=f"{type(ex).__name__}: {ex}",
                    secs=time.time() - t0)
    res["name"] = name
    res["secs"] = time.time() - t0
    res["maxdeg"] = ch.maxdeg
    res["chain"] = ch.name
    res["chain_max"] = ch.maxdeg
    res["size"] = cd["size"]
    res["mode"] = cd["mode"]
    return res


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    maxsize = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    only125 = "--ge125" in sys.argv
    rng = random.Random(seed)

    print("=== stage 0: validation ===")
    validate()
    print("  regression vs the three hand-entered shapes in trackB1_shapes:")
    for sh in SH.SHAPES:
        rr = SH.run_pair(sh, random.Random(1))
        if rr["status"] == "OK":
            print(f"    {sh.name[:44]:44s} params={rr['nparams']:4d} "
                  f"conds={rr['nconds']:4d} rank={rr['rank']:4d} "
                  f"dim<={rr['dim_bound']}")
    bad = degree_crosscheck()
    print(f"  degree cross-check (m,n)*v11(A_0) vs paper max: "
          f"{'ALL 34 AGREE' if not bad else bad}")
    print()

    shapes = build_all()
    shapes.sort(key=lambda c: (c["size"], c["chain"].name))
    print(f"=== stage 1+2: {len(shapes)} eps-passing shapes "
          f"({sum(1 for s in shapes if s['mode']=='derived')} derived, "
          f"{sum(1 for s in shapes if s['mode']=='superset')} superset) ===")
    todo = [s for s in shapes if s["size"] <= maxsize]
    if only125:
        todo = [s for s in todo if s["chain"].maxdeg >= 125]
    print(f"    running {len(todo)} with size <= {maxsize}")
    print()

    print("=== stage 3: y-adic + exact Jacobian ===")
    out = []
    for cd in todo:
        r = run_one(cd, rng)
        out.append(r)
        if r["status"] != "OK":
            print(f"  {r['name'][:78]}")
            print(f"      size={r['size']:4d}  {r['status']}: "
                  f"{str(r.get('detail'))[:90]}  [{r['secs']:.0f}s]")
        else:
            # dim_bound 1 is the BASELINE: the identically-zero p_00 column
            # is present in every shape.  The two open (8,28) cases both sit
            # at 1.  Only >= 2 means the polygon conditions left real freedom.
            flag = ("  <-- loose (real freedom left)" if r["dim_bound"] >= 2
                    else "  tight (== open (8,28) strength)")
            print(f"  {r['name'][:78]}")
            print(f"      size={r['size']:4d}  params={r['nparams']:4d} "
                  f"conds={r['nconds']:4d} rank={r['rank']:4d} "
                  f"dim<={r['dim_bound']:4d}  [{r['secs']:.0f}s]{flag}")
        sys.stdout.flush()
    with open("trackD_results.json", "w") as f:
        json.dump([{k: v for k, v in r.items() if k != "chain_obj"}
                   for r in out], f, indent=1, default=str)
    print(f"\n[wrote trackD_results.json: {len(out)} runs]")
