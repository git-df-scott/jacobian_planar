"""ITEM 2 -- the v3 float search rerun with EXACT Jacobians.

Same three gauges, same absolute objective, same acceptance test; the only
change is that Newton's Jacobian is computed exactly over C[eps]/(eps^2)
instead of by a finite difference with h = 1e-7.  That removes a step-size
floor which by itself could stall a search near 1e-5 without that being a fact
about the pentagon system.

Controls (each required to behave differently):
  X-POS  a planted target F(x) = F(x0) must be recovered to below TOL;
  X-CMP  on the SAME start, the exact-Jacobian Newton must reach a residual at
         least as small as the finite-difference one (if it did not, the change
         would be a regression and the run is void);
  X-NEG  the acceptance test still refuses a blown-up point.
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w5_pent_hitdetector_v3 as V

NSTART = int(sys.argv[1]) if len(sys.argv) > 1 else 20
print("=" * 78)
print("ITEM 2 -- pentagon hit detector v3b (exact Jacobians)")
print("=" * 78)
rng = np.random.default_rng(20260821)
res = {"controls": [], "runs": []}

# The planted control must live where the detector is well posed.  The
# objective is ABSOLUTE, and at levels 13..23 the recursion amplifies: at a
# random point the coefficients run to 1e10 and beyond, where float64 cannot
# resolve 1e-9 at all.  The acceptance band (allowed coefficients O(1)) is
# exactly the region where an absolute test is meaningful, so the planted point
# is drawn from that region -- which is also the only region a reported hit
# could come from.
x0 = None
for _ in range(400):
    cand = rng.normal(size=58) + 1j * rng.normal(size=58)
    fq, Qq = V.Fvec(cand, 'one')
    if Qq is None:
        continue
    a = V.allowed_scale(Qq)
    if 1.0 / V.BAND <= a <= V.BAND and float(np.max(np.abs(fq))) < 1e6:
        x0 = cand
        break
if x0 is None:
    print("    NOTE: no in-band planted point found in 400 draws; "
          "the control below is run at a random point and is expected to be "
          "limited by float64 resolution, which is recorded, not hidden.")
    x0 = rng.normal(size=58) + 1j * rng.normal(size=58)
tgt0, _ = V.Fvec(x0, 'one')
_fq, _Qq = V.Fvec(x0, 'one')
print(f"    planted point: allowed scale {V.allowed_scale(_Qq):.3e}, "
      f"|F| {float(np.max(np.abs(_fq))):.3e}")
start = x0 + 1e-3 * (rng.normal(size=58) + 1j * rng.normal(size=58))
r_ex, x_ex = V.newton_exact(start, 'one', target=tgt0)
V.check("X-POS exact-Jacobian Newton recovers a planted root", r_ex < V.TOL,
        f"final max |F - F(x0)| = {r_ex:.3e}")
r_fd, _ = V.newton(start, 'one', target=tgt0)
V.check("X-CMP the exact Jacobian is not a regression on the same start",
        r_ex <= max(r_fd, V.TOL), f"exact {r_ex:.3e} vs finite-difference {r_fd:.3e}")
xb = x0 * 1e6
fb, Qb = V.Fvec(xb, 'one')
okb, whyb = V.accept(xb, Qb, fb)
V.check("X-NEG the acceptance test still refuses a blown-up point", not okb, whyb)

t0 = time.time()
for chart in ("one", "zero"):
    best = np.inf
    hits = 0
    for s in range(NSTART):
        st = rng.normal(size=58) + 1j * rng.normal(size=58)
        r, x = V.newton_exact(st, chart)
        f, Q = V.Fvec(x, chart)
        ok, why = V.accept(x, Q, f)
        best = min(best, r)
        res["runs"].append({"chart": chart, "start": s,
                            "best_abs_forbidden": float(r),
                            "allowed_scale": float(V.allowed_scale(Q)) if Q is not None else None,
                            "param_norm": float(np.max(np.abs(x))),
                            "in_acceptance_band": bool(
                                Q is not None
                                and 1.0 / V.BAND <= V.allowed_scale(Q) <= V.BAND),
                            "accepted": bool(ok), "why": why})
        if ok:
            hits += 1
            print(f"    *** chart {chart} start {s}: ACCEPTED -- {why}", flush=True)
            res["runs"][-1]["point"] = [[float(z.real), float(z.imag)] for z in x]
            res["runs"][-1]["label"] = "CANDIDATE-UNVERIFIED"
    inband = [d for d in res["runs"] if d["chart"] == chart and d["in_acceptance_band"]]
    bestin = min((d["best_abs_forbidden"] for d in inband), default=float("inf"))
    print(f"    chart {chart}: {NSTART} exact-Jacobian starts, {hits} accepted, "
          f"best |forbidden| = {best:.3e}; of those, {len(inband)} ended INSIDE "
          f"the acceptance band with best |forbidden| = {bestin:.3e}   "
          f"({time.time()-t0:.0f}s)", flush=True)
res["controls"] = [[a, b, c] for a, b, c in V.RESULTS]
json.dump(res, open(os.path.join(HERE, "pent_v3b_results.json"), "w"), indent=1)
n = sum(1 for _, o, _ in V.RESULTS if o)
print("=" * 78)
print(f"    {n}/{len(V.RESULTS)} controls passed")
print("=" * 78)
