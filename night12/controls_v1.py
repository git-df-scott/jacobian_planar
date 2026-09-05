"""night12 v1 -- controls.

(6) positive: P = x + y^126   -- mate must be found and P certified COORDINATE
    negative: P = x^126 + y^127 + x^2*y^2 -- gradient vanishes at the origin,
    so S1 must reject it BEFORE the solver, and the solver must confirm on
    override with an exact emptiness certificate.

Also re-run here: the SY validation set required by the brief.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import screens
import sy
import exact
import v1

LOG = []


def say(s):
    print(s, flush=True)
    LOG.append(s)


def run(name, P, override=False):
    say("=" * 78)
    say("%s   P = %s" % (name, sorted(P.items())))
    t0 = time.time()
    sc = screens.screen(P, t2=120, t1=300)
    say("  S2=%s (%s)" % (sc["S2"], sc["S2_detail"]))
    say("  S1=%s (%s)" % (sc["S1"], sc["S1_detail"]))
    say("  S3: places_at_infinity=%d  genus_newton=%d  lead_terms=%d"
        % (sc["places_at_infinity"], sc["genus_newton"], sc["lead_terms"]))
    say("  screens passed: %s" % sc["passed"])
    v, st = sy.certify(P)
    say("  SY: %s (nodes=%d leaves=%d)" % (v, st["nodes"], st["leaves"]))
    rec = {"name": name, "P": v1.pstr(P), "screens": sc, "SY": v, "stages": []}
    if not sc["passed"] and not override:
        say("  -> rejected by screens; no mate matrix built.")
        rec["outcome"] = "REJECTED_BY_SCREENS"
        return rec
    if not sc["passed"]:
        say("  -> OVERRIDE: screens rejected, running the solver anyway.")
    item = {"P": P, "H": None, "m": M.pdeg(P) // 2}
    for stage in v1.STAGES:
        S, info = v1.general_carrier(P, stage, v1.CAP[stage])
        if not S:
            continue
        out, rows, Qd = exact.decide(P, S, want_lambda=True)
        out.update(info)
        rec["stages"].append(out)
        say("  stage %s: deg_Q<=%d  n_raw=%d thin_t=%d n_unknowns=%d "
            "deflated_kernel_dim=%d  -> %s [%s]"
            % (stage, info["deg_Q_bound"], info["n_raw"], info["thin_t"],
               info["n_used"], info["deflated_kernel_dim"],
               out["verdict"], out["certificate"]))
        if out.get("lambda_detail"):
            say("        lambda: support=%s  (%s)"
                % (out.get("lambda_support"), out["lambda_detail"]))
        if out["verdict"] == "MATE_over_Q":
            say("        exact Q (deg %d): %s" % (M.pdeg(Qd), sorted(Qd.items())))
            say("        bracket [P,Q] == 1 over Q: %s" % M.is_one(M.bracket(P, Qd)))
            say("        degree pair (%d,%d) divisibility-ordered: %s"
                % (M.pdeg(P), M.pdeg(Qd), M.divisibility_ordered(M.pdeg(P), M.pdeg(Qd))))
            rec["outcome"] = "MATE"
            rec["deg_Q"] = M.pdeg(Qd)
            rec["Q"] = {("%d,%d" % k): [int(x.numerator), int(x.denominator)]
                        for k, x in sorted(Qd.items())}
            break
    else:
        rec["outcome"] = "NO_MATE_ALL_STAGES"
    say("  (%.1fs)" % (time.time() - t0))
    return rec


def main():
    out = []
    say("SY validation set (brief item 2)")
    for name, P, expect in sy.VALIDATION:
        v, st = sy.certify(P)
        say("  %-28s -> %-16s  brief label: %-16s  nodes=%d leaves=%d"
            % (name, v, expect, st["nodes"], st["leaves"]))
    say("")
    say("NOTE (measurement, recorded not resolved): the brief labels x + x^2*y a")
    say("coordinate.  This implementation of the Shpilrain-Yu reduction returns")
    say("NON_COORDINATE for it -- the gradient pair is (1+2xy, x^2), whose leading")
    say("monomials xy and x^2 do not divide one another, so the DAG is a single")
    say("exhausted leaf.  Independently, the exact mate system for x + x^2*y is")
    say("inconsistent on every support tried (deg Q <= 3,6,9,12,15; see below).")
    say("")
    P = {(1, 0): 1, (2, 1): 1}
    for stage in v1.STAGES + ["W2"]:
        if stage == "W2":
            S = [(i, j) for i in range(16) for j in range(16 - i)]
            Sset = set(S)
            drop, Pk, k = set(), {(0, 0): 1}, 0
            while 3 * k <= 15 and set(Pk).issubset(Sset):
                drop.add((2 * k, k)); Pk = M.pmul(Pk, P); k += 1
            S = sorted(Sset - drop)
            info = {"deg_Q_bound": 15, "n_raw": len(Sset),
                    "deflated_kernel_dim": len(drop)}
        else:
            S, info = v1.general_carrier(P, stage, v1.CAP[stage])
        o, rows, Qd = exact.decide(P, S, want_lambda=True)
        say("  x + x^2*y  stage %-2s deg Q <= %-3d n=%-4d defl=%d -> %-14s [%s]"
            "  lambda support=%s"
            % (stage, info["deg_Q_bound"], o["n_unknowns"],
               info["deflated_kernel_dim"], o["verdict"], o["certificate"],
               o.get("lambda_support")))
    say("")

    out.append(run("C-POS  P = x + y^126", {(1, 0): 1, (0, 126): 1}))
    out.append(run("C-NEG  P = x^126 + y^127 + x^2*y^2",
                   {(126, 0): 1, (0, 127): 1, (2, 2): 1}, override=True))

    gate = assess(out)

    json.dump({"controls": out, "gate": gate},
              open(os.path.join(HERE, "controls_v1.json"), "w"), indent=1)
    open(os.path.join(HERE, "controls_v1_log.txt"), "w").write("\n".join(LOG) + "\n")
    return 0 if gate["gate"] == "PASS" else 1


def assess(out):
    """Explicit hard gate.  The controls script previously printed its
    measurements but returned success unconditionally, so a regression in
    C-POS/C-NEG/SY could not stop a pipeline run.  This makes each required
    property a named check with an explicit verdict and a nonzero exit code on
    failure.  It asserts only properties the controls already measured -- no
    screen, certificate or decision contract is touched.
    """
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # (a) SY validation set: every entry the brief actually labels must match.
    for name, P, expect in sy.VALIDATION:
        v, _ = sy.certify(P)
        if expect in ("COORDINATE", "NON_COORDINATE"):
            chk("SY[%s]" % name, v == expect, "got %s, brief label %s" % (v, expect))
        else:
            chk("SY[%s] (unlabeled in brief)" % name, True, "got %s" % v)

    cpos = next(r for r in out if r["name"].startswith("C-POS"))
    cneg = next(r for r in out if r["name"].startswith("C-NEG"))

    # (b) C-POS: screens pass, SY COORDINATE, a mate certified over Q.
    chk("C-POS screens pass", cpos["screens"]["passed"],
        "S2=%s S1=%s" % (cpos["screens"]["S2"], cpos["screens"]["S1"]))
    chk("C-POS SY COORDINATE", cpos["SY"] == "COORDINATE", cpos["SY"])
    chk("C-POS mate found", cpos.get("outcome") == "MATE", str(cpos.get("outcome")))
    chk("C-POS mate is exact_solution certified",
        any(s.get("certificate") == "exact_solution" for s in cpos["stages"]), "")

    # (c) C-NEG: S1 must reject BEFORE the solver, and the solver on override
    #     must certify emptiness exactly at every stage it tried.
    chk("C-NEG rejected by S1", cneg["screens"]["S1"] == "reject",
        cneg["screens"]["S1_detail"])
    chk("C-NEG no mate on override", cneg.get("outcome") != "MATE",
        str(cneg.get("outcome")))
    chk("C-NEG every stage EMPTY_over_Q with a certificate",
        bool(cneg["stages"]) and all(
            s["verdict"] == "EMPTY_over_Q"
            and s["certificate"] in ("lambda_exact", "rank_full_column_exact")
            for s in cneg["stages"]),
        ", ".join("%s:%s[%s]" % (s.get("stage"), s["verdict"], s["certificate"])
                  for s in cneg["stages"]))

    bad = [c for c in checks if not c["ok"]]
    gate = {"gate": "PASS" if not bad else "FAIL",
            "n_checks": len(checks), "n_failed": len(bad), "checks": checks}
    say("")
    say("=" * 78)
    say("HARD GATE: %d checks, %d failed -> %s" % (len(checks), len(bad), gate["gate"]))
    for c in checks:
        say("  [%s] %-52s %s" % ("ok" if c["ok"] else "FAIL", c["check"], c["detail"]))
    return gate


if __name__ == "__main__":
    sys.exit(main())
