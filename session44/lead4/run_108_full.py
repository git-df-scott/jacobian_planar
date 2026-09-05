"""Full-depth (jextra=15 -> jmax=39) two-prime run on the open (72,108)
subcases: every bracket row constrained, so this system is EQUIVALENT to
the existence question at the shape (not a relaxation). More conditions,
same 25/61 unknowns - facstd tends to reach <1> faster on overdetermined
systems."""
import sys
import trackD_twoprime as TW
import trackD_extract  # noqa: F401  (re-imported per prime by TW)

TW.TARGETS = "trackD_targets_108.json"
TW.STATE = "state_108_full.json"
_orig = None

def _patch():
    import trackD_twoprime as T
    old_run_one = T.run_one
    def run_one_full(t, budget):
        import os, time
        per = {}
        for p in T.PRIMES:
            os.environ["TRACKD_PRIME"] = str(p)
            for m in [k for k in list(sys.modules) if k.startswith("trackD_extract")]:
                del sys.modules[m]
            import trackD_extract as EX
            t0 = time.time()
            r = EX.run(t["NP"], t["NQ"], t["r"], f"fd{p}", timeout=budget, jextra=15)
            vd = "TIMEOUT" if r["status"] == "TIMEOUT" else (
                 "OOS" if r["status"] == "OUT OF SCOPE" else T.classify(r.get("out") or ""))
            per[str(p)] = {"verdict": vd, "secs": round(time.time() - t0),
                           "out": (r.get("out") or "").replace("\n", " | ")[:300]}
            if vd in ("OOS",):
                return "OOS", per
            if vd == "TIMEOUT":
                break
        vs = [per[str(p)]["verdict"] for p in T.PRIMES if str(p) in per]
        return T.combine(vs[0], vs[1] if len(vs) > 1 else "TIMEOUT"), per
    T.run_one = run_one_full

_patch()
sys.argv = ["run_108_full", "3600"]
TW.main()
