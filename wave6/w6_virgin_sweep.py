#!/usr/bin/env python3
"""WAVE 6 -- sweep the uncovered enumeration cases the queue never carried.

INPUT: audit_queue/queue_coverage.json (uncovered cases, 125 <= max <= 150
first).  For each case: locate its chain in trackD_chain_map.all_chains(),
generate EVERY reduced candidate shape (reduced_candidates) -- deliberately
WITHOUT the triage filters (dim bound, size cap) that silently dropped
vertex-LIVE shapes from the original queue -- and run the campaign's own
exact realization system (trackD_extract.run, Singular facstd) on each,
smallest first, with a per-shape timeout.

Verdicts recorded per shape: EMPTY / dim d (LIVE -> CANDIDATE pipeline) /
TIMEOUT / ERROR.  Nothing is interpreted here; LIVE shapes are raw material
for lifting + the HIT gate.

Controls:
  C1 (positive): a shape from the EXISTING queue that the campaign recorded
      EMPTY must come back EMPTY through this driver (pipeline sanity).
  C2 (negative): the same shape with its bracket target corrupted must NOT
      come back with the same verdict signature.
"""
import os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AT = os.path.join(ROOT, "campaign", "audit_tracks")
sys.path.insert(0, AT)
os.chdir(AT)   # trackD modules use relative paths

import trackD_chain_map as CM
import trackD_extract as EX

def npoints(NP):
    return len(NP)

def main():
    cov = json.load(open(os.path.join(ROOT, "audit_queue/queue_coverage.json")))
    unc = cov.get("uncovered_cases") or cov.get("uncovered")
    import os as _os
    cap = int(_os.environ.get("W6_MAXCAP", "150"))
    lo = sorted([u for u in unc if u.get("max", 999) <= cap],
                key=lambda u: u["max"])
    only = sys.argv[1] if len(sys.argv) > 1 else None
    chains = {getattr(c, "name", str(c)): c for c in CM.all_chains()}
    out_path = os.path.join(ROOT, "wave6", "virgin_results.json")
    results = json.load(open(out_path)) if os.path.exists(out_path) else []
    done = {(r["case"], r["shape_tag"]) for r in results}
    budget = int(os.environ.get("W6_TIMEOUT", "300"))

    for u in lo:
        cid = u["chain"]
        if only and only not in cid:
            continue
        # find the chain: match by the chain string the coverage audit recorded
        ch = None
        for name, c in chains.items():
            if cid.replace(" ", "") in name.replace(" ", "") or \
               name.replace(" ", "") in cid.replace(" ", ""):
                ch = c; break
        if ch is None:
            # fall back: match by A0 + final corner data
            for c in chains.values():
                try:
                    if list(getattr(c, "A0", [])) == list(u["A0"]):
                        ch = c; break
                except Exception:
                    pass
        if ch is None:
            results.append({"case": cid, "shape_tag": "-", "verdict":
                            "CHAIN-NOT-FOUND"})
            continue
        try:
            cands = CM.reduced_candidates(ch)
            if isinstance(cands, tuple):
                cands = cands[0]
        except Exception as e:
            results.append({"case": cid, "shape_tag": "-", "verdict":
                            f"CAND-ERROR {e}"})
            continue
        cands = sorted(cands, key=lambda cd: npoints(cd["NP"]) + npoints(cd["NQ"]))
        print(f"[{cid}] {len(cands)} candidate shapes")
        for i, cd in enumerate(cands):
            tag = f"a={cd.get('a')} b={cd.get('b')} r={cd.get('r')} i={i}"
            if (cid, tag) in done:
                continue
            t0 = time.time()
            try:
                r = EX.run(cd["NP"], cd["NQ"], cd["r"],
                           f"w6_{abs(hash(cid))%10**6}_{i}", timeout=budget)
                verdict = str(r)
            except Exception as e:
                verdict = f"ERROR {type(e).__name__}: {e}"
            rec = {"case": cid, "max": u["max"], "shape_tag": tag,
                   "verdict": verdict, "wall_s": round(time.time()-t0, 1)}
            results.append(rec)
            json.dump(results, open(out_path, "w"), indent=1)
            flag = "  <-- LIVE?" if ("dim" in verdict and "EMPTY" not in verdict) else ""
            print(f"  {tag}: {verdict} ({rec['wall_s']}s){flag}")
    print("sweep pass complete:", len(results), "records")

if __name__ == "__main__":
    main()
