"""Decide the tight survivors with facstd (factorizing Groebner).

Full std() timed out at 240s on case (2) -- 25 params, jmax 26, degree-26
polynomials.  facstd splits the ideal into components as it goes, so a system
that collapses to (1) on every branch never has to build one dense basis.

Targets come from trackD_targets.json: survivors of BOTH gates (vertex
non-degeneracy, and not already closed in the literature) whose sweep dim
bound is <= 1, i.e. finite point sets modulo the additive constant -- exactly
the state case (2) was in before its elimination.  Ordered by parameter count,
smallest first.
"""
import json, sys, time, os
import trackD_extract as EX

if __name__ == "__main__":
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    T = json.load(open("trackD_targets.json"))
    T.sort(key=lambda t: (t["params"], t["size"]))
    print(f"{len(T)} tight >=125 targets; running {min(nmax,len(T))} "
          f"at {budget}s each, smallest first", flush=True)
    res = []
    for k, t in enumerate(T[:nmax]):
        nm = f"tgt{k:03d}"
        r = EX.run(t["NP"], t["NQ"], t["r"], nm, timeout=budget)
        line = {"tag": t["tag"], "max": t["max"], "params": t["params"],
                "status": r["status"], "secs": round(r.get("secs", 0)),
                "out": (r.get("out") or "").replace("\n", " | ")}
        res.append(line)
        print(f"[{k+1}/{min(nmax,len(T))}] max={t['max']} params={t['params']} "
              f"{r['status']} [{r.get('secs',0):.0f}s]", flush=True)
        print(f"    {t['tag'][:96]}", flush=True)
        for l in (r.get("out") or "").splitlines():
            print("      " + l, flush=True)
        json.dump(res, open("trackD_solve.json", "w"), indent=1)
    print("[done]")
