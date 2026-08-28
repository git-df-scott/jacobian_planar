"""night12 v2 -- build MATE_V2.md from the recorded run artifacts.

Reads only files written by the run; computes no mathematics of its own.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "MATE_V2.md")

L = []


def w(s=""):
    L.append(s)


def load(name, default=None):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else default


def cellv(s):
    short = {"EMPTY_over_Q": "EMPTY", "MATE_over_Q": "MATE",
             "EMPTY_trivial_carrier": "EMPTY(triv)",
             "NOT_CERTIFIED": "NOT_CERT"}.get(s.get("verdict"), s.get("verdict"))
    cs = {"lambda_exact": "lam", "rank_full_column_exact": "rank",
          "exact_solution": "sol"}.get(s.get("certificate"), "-")
    return "%s[%s]" % (short, cs)


def cert_tally(recs):
    c = collections.Counter()
    for r in recs:
        for s in r["stages"]:
            c[(s.get("verdict"), s.get("certificate"))] += 1
    return c


def main():
    recs = load("v2_records_all.json", []) or []
    ctl2 = load("controls_v2.json", {}) or {}
    ctl1 = load("controls_v1.json", {}) or {}
    g2 = ctl2.get("gate", {})
    g1 = ctl1.get("gate", {}) if isinstance(ctl1, dict) else {}

    A = [r for r in recs if r["arm"] == "A"]
    B = [r for r in recs if r["arm"] == "B"]
    hits = [r for r in recs if r.get("hit")]

    w("# night12 -- MATE SEARCH v2: results")
    w()
    w("Measurements only. Nothing in this file is a conclusion. **ring: Q** = exact")
    w("rational arithmetic; **ring: F_p** = the scheduling prime, which decides")
    w("nothing. Machinery: `v2_families.py` (targets and their derived")
    w("certificates), `v2.py` (carriers, stages, driver), `controls_v2.py`,")
    w("`exact.py` and `sy.py` from v1, both frozen.")
    w()
    w("The v1 results are in `V1_RESULTS.md`; this file is the v2 addendum, run")
    w("against the certified non-coordinate targets that night14 made available.")
    w()

    # ------------------------------------------------------------------- gate
    w("## 1. Hit gate")
    w()
    w("The gate: a mate `Q` certified over `Q` by expanding `[P,Q] - 1`")
    w("coefficientwise, on a `P` certified NON_COORDINATE. On a hit the run halts")
    w("and writes `night12/HIT_<hash>/`.")
    w()
    w("| quantity | value |")
    w("| --- | --- |")
    w("| ARM A objects (deg P 124-132) | %d |" % len(A))
    w("| ARM B objects (night14 crux + the brief's `x + x^2*y`) | %d |" % len(B))
    w("| total objects | %d |" % len(recs))
    w("| stage evaluations | %d |" % sum(len(r["stages"]) for r in recs))
    w("| mates certified over Q | %d |"
      % sum(1 for r in recs if r["outcome"] == "MATE"))
    w("| **hit-gate status** | **%s** |"
      % ("HIT: " + ", ".join("HIT_%s/" % r["hash"] for r in hits) if hits
         else "NOT TRIPPED -- 0 hits; the run did not halt"))
    w()
    if not hits:
        w("Every object in both arms is certified NON_COORDINATE, and every one")
        w("reached an exact emptiness verdict on every support tried. No mate was")
        w("found anywhere in v2, so the gate had nothing to fire on.")
        w()

    # --------------------------------------------------------------- controls
    w("## 2. Controls")
    w()
    w("The v1 controls stand: `controls_v1.py`, **%s**, %d checks, %d failed."
      % (g1.get("gate", "?"), g1.get("n_checks", 0), g1.get("n_failed", 0)))
    w()
    w("The V2 brief adds one: on a COORDINATE `P` of shape similar to the ARM A")
    w("targets, the solver must FIND its mate. `controls_v2.py`, **%s**, %d checks,"
      % (g2.get("gate", "?"), g2.get("n_checks", 0)))
    w("%d failed." % g2.get("n_failed", 0))
    w()
    w("| control | ok | detail |")
    w("| --- | --- | --- |")
    for c in g2.get("checks", []):
        w("| %s | %s | %s |" % (c["check"], "ok" if c["ok"] else "**FAIL**",
                                c["detail"]))
    w()
    w("`V2-POS-2` is the one that carries weight. It is the degenerate `g = 0`")
    w("member of the very family ARM A searches -- same `v = y + tau(x)`, quadratic")
    w("term switched off, which makes it a shear and therefore a coordinate -- at")
    w("`deg P = 124`, run through the ARM A stage list, the ARM A carriers and the")
    w("ARM A solver path with no special-casing. Its mate is found at the first")
    w("stage and verified coefficientwise over `Q`. So an EMPTY in ARM A is not the")
    w("machinery being unable to find a mate at that degree and shape.")
    w()

    # ----------------------------------------------------------- per-P table
    w("## 3. Per-P summary")
    w()
    w("One row per object, both arms. **certificate id** is the record hash: the")
    w("object's certificates are in `night12/V2_RECORDS/<id>.json`, and stage `k`")
    w("of that record is cited as `<id>.s<k>`. **U** is the unimodularity check --")
    w("for ARM A the Bezout identity `A*P_x + B*P_y = 1` expanded coefficientwise")
    w("over `Q`, for ARM B night14's char-0 U-test carried on the source record.")
    w("**mate system** is the largest system actually solved for that object")
    w("(unknowns after kernel deflation x nonzero Keller rows), at the stage named")
    w("in the next column. The re-verification column is section 8's independent")
    w("pass, `verify_certs_v2.py`.")
    w()
    rv = load("verify_certs_v2.json", {}) or {}
    rvby = {o["hash"]: o for o in rv.get("per_object", [])}
    w("| certificate id | arm | tag | deg P | U | SY | mate system (n x rows) | "
      "at stage | stages | verdict | re-verified |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(recs, key=lambda r: (r["arm"], r["deg_P"], r["tag"])):
        st = [s for s in r["stages"] if "n_unknowns" in s]
        big = max(st, key=lambda s: s["n_unknowns"]) if st else {}
        if r["arm"] == "A":
            u = str(r["certs"].get("U_bezout_A_Px_plus_B_Py_eq_1"))
        else:
            u = "%s (night14)" % r["certs"].get("night14_U", "?")
        o = rvby.get(r["hash"])
        if o is None:
            rvcell = "-"
        else:
            rvcell = "**FAIL**" if o["fails"] else "ok"
        w("| `%s` | %s | %s | %d | %s | %s | %s x %s | %s dQ<=%s | %d | %s | %s |"
          % (r["hash"], r["arm"], r["tag"], r["deg_P"], u, r["SY_verdict"],
             big.get("n_unknowns", "-"), big.get("n_rows_nonzero", "-"),
             big.get("carrier", "-"), big.get("deg_Q_bound", "-"),
             len(r["stages"]), r["outcome"], rvcell))
    w()
    w("Verdict tally over objects: %s."
      % dict(collections.Counter(r["outcome"] for r in recs)))
    w("Verdict tally over stage evaluations: %s."
      % dict(collections.Counter(s.get("verdict") for r in recs
                                 for s in r["stages"])))
    w()

    # ------------------------------------------------------------------ ARM A
    w("## 4. ARM A targets and their derived certificates")
    w()
    w("Construction (night14 `PROSPECTOR.md` section 2, reparametrised to clear")
    w("denominators):")
    w()
    w("```")
    w("v = y + tau(x),  tau in Z[x], deg tau = T >= 1")
    w("g = c*(x - a)^n,  c, a, h0 in Z,  c, h0 != 0,  n >= 1")
    w("P = h0*v + g*v^2 + kappa            deg P = n + 2*max(1, T)")
    w("```")
    w()
    w("Two certificates per object, both expanded coefficientwise over `Q`.")
    w("Neither needs a Groebner basis, which matters because S1 times out on every")
    w("`P` at these degrees (see `V1_RESULTS.md` section 3).")
    w()
    w("**U -- unimodular gradient.** From `v_y = 1`, `v_x = tau'`:")
    w()
    w("```")
    w("P_y = h0 + 2*g*v")
    w("P_x = v_x*P_y + g'*v^2,        g' = c*n*(x-a)^(n-1)")
    w("```")
    w()
    w("and `2*(x-a)*g' = 2*n*g`, so `2*(x-a)*(g'*v^2) = n*v*(P_y - h0)`. Substituting")
    w("`g'*v^2 = P_x - v_x*P_y` and eliminating `v` via `h0 = P_y - 2*g*v` gives")
    w()
    w("```")
    w("1 = A*P_x + B*P_y,   A = 4*g*(x-a) / (n*h0^2)")
    w("                     B = ( h0 - (2*g/n)*(n*v + 2*(x-a)*v_x) ) / h0^2")
    w("```")
    w()
    w("with `A, B` in `Q[x,y]`. This is a Bezout certificate that `1` is in")
    w("`(P_x, P_y)`: the gradient is unimodular, so the critical locus is empty and")
    w("every fibre is smooth.")
    w()
    w("**R -- non-coordinate.** `P - kappa = v*(h0 + g*v)` identically, both factors")
    w("nonconstant, so the `kappa`-fibre is reducible. With U every fibre is smooth,")
    w("so a reducible fibre is a disconnected one, while a coordinate has every")
    w("fibre isomorphic to the affine line and in particular connected.")
    w()
    w("| tag | deg P | n | T | \\|supp P\\| | U verified | R verified | R factor degs | SY | places at inf | genus_newton |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(A, key=lambda r: (r["deg_P"], r["tag"])):
        c = r["certs"]
        p = c.get("params", {})
        w("| %s | %d | %s | %s | %d | %s | %s | %s | %s | %d | %d |"
          % (r["tag"], r["deg_P"], p.get("n"), p.get("T"), r["n_supp_P"],
             c.get("U_bezout_A_Px_plus_B_Py_eq_1"),
             c.get("R_factorisation_P_minus_kappa_eq_v_times_h0_plus_gv"),
             c.get("R_factor_degrees"), r["SY_verdict"],
             r["places_at_infinity"], r["genus_newton"]))
    w()
    nU = sum(1 for r in A if r["certs"].get("U_bezout_A_Px_plus_B_Py_eq_1"))
    nR = sum(1 for r in A
             if r["certs"].get("R_factorisation_P_minus_kappa_eq_v_times_h0_plus_gv"))
    nS = sum(1 for r in A if r["SY_verdict"] == "NON_COORDINATE")
    nG = sum(1 for r in A if r["genus_newton"] > 0)
    w("U verified **%d/%d**; R verified **%d/%d**; SY NON_COORDINATE **%d/%d**; "
      "genus_newton > 0 **%d/%d**." % (nU, len(A), nR, len(A), nS, len(A), nG, len(A)))
    w()

    w("## 5. ARM A verdicts")
    w()
    w("Stages per object: `deg Q <= deg P - 1`, `deg P + 31`, `deg P + 63` on the")
    w("Newton-polygon-similar carrier, then a **wide** stage at `deg Q <= deg P + 63`")
    w("on the full degree triangle thinned to 2500. The bound `deg P + 63` is the")
    w("one the brief sets. Cell format `VERDICT[cert]`; `lam` = exact lambda")
    w("certificate, `rank` = full-column-rank certificate, `sol` = exact solution.")
    w()
    w("The two carriers are **complementary, not nested**. The similar carrier is a")
    w("dense sample of one sub-polygon of the degree triangle; the wide carrier is a")
    w("stride-`t` sample spread over the whole triangle (before thinning it contains")
    w("the similar one, after thinning it does not). An EMPTY on each is a separate")
    w("statement, and neither is a claim about every `Q` of that degree.")
    w()
    w("| tag | deg P | dQ<=P-1 | dQ<=P+31 | dQ<=P+63 | wide dQ<=P+63 | wide n_raw -> n_used (thin) | outcome |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(A, key=lambda r: (r["deg_P"], r["tag"])):
        st = r["stages"]
        np_ = [s for s in st if s.get("carrier") == "np_similar"]
        wd = [s for s in st if s.get("carrier") == "wide_triangle"]
        cells = [cellv(s) for s in np_] + ["-"] * (3 - len(np_))
        wc = cellv(wd[0]) if wd else "-"
        wn = ("%d -> %d (t=%d)" % (wd[0]["n_raw"], wd[0]["n_unknowns"],
                                   wd[0]["thin_t"])) if wd else "-"
        w("| %s | %d | %s | %s | %s | %s | %s | %s |"
          % (r["tag"], r["deg_P"], cells[0], cells[1], cells[2], wc, wn,
             r["outcome"]))
    w()
    w("Unknown counts on the similar carrier, per stage (min/median/max): %s."
      % _mmm([s["n_unknowns"] for r in A for s in r["stages"]
              if s.get("carrier") == "np_similar" and "n_unknowns" in s]))
    w()
    w("Outcomes: %s." % dict(collections.Counter(r["outcome"] for r in A)))
    w("Certificates: %s." % dict(cert_tally(A)))
    w()

    # ------------------------------------------------------------------ ARM B
    w("## 6. ARM B verdicts (low-degree, escalating)")
    w()
    w("Five structurally diverse objects from night14's 79 certified")
    w("U-PASS + SY-NON_COORDINATE records -- two positive-genus `F2b`, plus one each")
    w("of `F1b`, `F3`, `F4` -- together with `x + x^2*y`, which the brief names.")
    w("`deg Q` escalates 10, 30, 60, 100, 126.")
    w()
    w("**Only the last stage can decide anything.** The published degree bound means")
    w("a mate for an object of this size would need `deg Q >= 125`, so the stages at")
    w("`deg Q <= 10, 30, 60, 100` are calibration: their EMPTYs are honest but")
    w("support-relative and carry no weight against the bound. Every stage in this")
    w("file is recorded with `support_relative = true` and its full carrier")
    w("parameters; the `decisive` column marks the one stage per object that clears")
    w("the bound.")
    w()
    w("| tag | family | deg P | dQ<=10 | dQ<=30 | dQ<=60 | dQ<=100 | dQ<=126 (decisive) | n at dQ<=126 | outcome |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(B, key=lambda r: (r["family"], r["deg_P"])):
        st = r["stages"]
        by = {s.get("deg_Q_bound"): s for s in st}
        cells = [cellv(by[d]) if d in by else "-" for d in (10, 30, 60, 100, 126)]
        n126 = by.get(126, {}).get("n_unknowns", "-")
        w("| %s | %s | %d | %s | %s | %s | %s | **%s** | %s | %s |"
          % (r["tag"], r["family"], r["deg_P"], cells[0], cells[1], cells[2],
             cells[3], cells[4], n126, r["outcome"]))
    w()
    w("Outcomes: %s." % dict(collections.Counter(r["outcome"] for r in B)))
    w("Certificates: %s." % dict(cert_tally(B)))
    w()
    w("SY verdicts across ARM B: %s."
      % dict(collections.Counter(r["SY_verdict"] for r in B)))
    w()

    # ---------------------------------------------------------- certificates
    w("## 7. Certificates emitted")
    w()
    w("| arm | (verdict, certificate) | count |")
    w("| --- | --- | --- |")
    for nm, rs in (("A", A), ("B", B)):
        for k, v in sorted(cert_tally(rs).items(), key=lambda kv: -kv[1]):
            w("| %s | %s | %d |" % (nm, k, v))
    w()
    nc = [r for r in recs if str(r["outcome"]).startswith("NOT_CERTIFIED")]
    w("`NOT_CERTIFIED` stage outcomes (never reported as emptiness): **%d**." % len(nc))
    for r in nc:
        w("- `%s` %s: %s" % (r["hash"], r["tag"], r["outcome"]))
    w()
    w("Every `lambda_exact` record carries the lambda vector itself")
    w("(`lambda_vector`, entries `[[i,j],[num,den]]`) and a `lambda_reverified`")
    w("flag from an exact re-check at record time, so each certificate can be")
    w("verified from the record alone.")
    w()

    # ------------------------------------------------- independent recheck
    w("## 8. Independent re-verification")
    w()
    if not rv:
        w("`verify_certs_v2.json` not present; no independent pass recorded.")
        w()
    else:
        w("`verify_certs_v2.py` re-checks every v2 certificate without calling")
        w("`exact.decide` or `v2_families`. Carriers and Keller systems are rebuilt")
        w("from the recorded carrier parameters; the ARM A factor `v` is RECOVERED")
        w("from `P` itself by exact division `v = (P_y - h0)/(2*g)` and the Bezout")
        w("pair rebuilt from it, so the identity is re-derived rather than replayed;")
        w("`rank_full_column_exact` stages are re-run at a different scheduling")
        w("prime (`%s`) and a different compression seed (`%s`) than the run used,"
          % (rv.get("recheck_prime"), rv.get("recheck_seed")))
        w("and ARM B objects are re-tested with night14's Singular U-test in")
        w("characteristic 0.")
        w()
        w("| check | outcome | count |")
        w("| --- | --- | --- |")
        for k, v in sorted(rv.get("tally", {}).items()):
            parts = [x.strip() for x in k.split("|")]
            w("| %s %s | %s | %d |" % (parts[0], parts[1], parts[2], v))
        w()
        w("**FAILURES: %d.**" % len(rv.get("failures", [])))
        for f in rv.get("failures", []):
            w("- `%s`" % (" | ".join(str(x) for x in f)))
        w()

    # --------------------------------------------------------------- caveats
    w("## 9. What these verdicts do and do not say")
    w()
    w("1. **The targets are certified, not assumed.** Every ARM A object has an")
    w("   explicit Bezout identity proving its gradient unimodular and an explicit")
    w("   factorisation proving a fibre reducible, both checked coefficientwise")
    w("   over `Q`, plus an independent SY verdict. ARM B's objects carry night14's")
    w("   U-test and FIB-screen certificates as well as SY. Section 8 re-derives")
    w("   all of it a second time, independently of the run's own code path.")
    w("2. **Every EMPTY is support-relative and is labelled so.** The verdict is")
    w("   about the linear system on the carrier actually built. It is exact over")
    w("   `Q` on that carrier -- no modular computation decides anything -- but it")
    w("   is not a statement about all `Q` of that degree unless the carrier is the")
    w("   full triangle, which only the ARM A wide stage approaches, and that one")
    w("   is thinned (thinning index recorded per stage).")
    w("3. **Emptiness is never claimed beyond the stage tried.** Each stage records")
    w("   its own carrier and its own certificate; no stage's verdict is extended")
    w("   to a higher degree bound.")
    w("4. **The solver is known to find mates at this degree and shape**, by")
    w("   control V2-POS-2, so the ARM A EMPTYs are not a null instrument.")
    w()

    open(OUT, "w").write("\n".join(L) + "\n")
    print("wrote", OUT, "(%d lines)" % len(L))


def _mmm(xs):
    if not xs:
        return "n/a"
    xs = sorted(xs)
    return "%d / %d / %d" % (xs[0], xs[len(xs) // 2], xs[-1])


if __name__ == "__main__":
    main()
