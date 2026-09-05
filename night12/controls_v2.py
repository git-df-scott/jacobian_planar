"""night12 v2 -- controls.

The v1 controls stand and are not restated here; `controls_v1.py` carries them
and its own hard gate (15 checks).  This file adds the control the V2 brief
asks for: on a COORDINATE `P` of shape similar to the ARM A targets, the solver
must FIND its mate.  Two of them:

  V2-POS-1  P = x + y^2                     the shape the brief names
  V2-POS-2  P = y + tau(x), deg tau = 124   the degenerate (g = 0) member of
            the very family ARM A searches: same v = y + tau, but with the
            quadratic term switched off, which turns the object into a shear
            and therefore a coordinate.  Its mate is -x.  This is the control
            that matters, because it exercises the ARM A carriers and the ARM A
            solver path at ARM A degree on an object known to have a mate: if
            the machinery could not find a mate here, an EMPTY anywhere in
            ARM A would carry no weight.

Both of those coordinates are shears, whose mate has degree 1, so between them
they exercise ARM A's degree but not ARM A's carrier: a degree-1 mate is found
inside the first few columns.  Two further controls close that axis, built by
the elementary chain

    A = x + y^2 ,   B = y + A^k ,   P = A + B^2       deg P = 4k

every step of which preserves the bracket, so [P, B] = 1 identically and P is a
coordinate whose SMALLEST mate has degree 2k:

  V2-POS-3  k = 11, deg P = 44, mate degree 22
  V2-POS-4  k = 21, deg P = 84, mate degree 42

Here the mate is a dense polynomial of degree deg P / 2 that has to be found in
a carrier of several hundred to a couple of thousand unknowns and reconstructed
rationally -- exactly the work ARM A's EMPTY stages do, but on a system that is
consistent.

All four are run through exactly the ARM A stage list and carriers, with no
special-casing.  A control fails if no mate is found, or if the mate found does
not satisfy [P,Q] - 1 = 0 coefficientwise over Q.
"""

import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import v2
import sy

LOG = []


def say(s):
    print(s, flush=True)
    LOG.append(s)


def shear(deg):
    """P = y + tau(x) with deg tau = deg; a coordinate, mate -x."""
    tau = {(i, 0): Fraction((-1) ** i * (i % 5 + 1)) for i in range(2, deg + 1)
           if i % 7 in (0, 2, 3)}
    tau[(deg, 0)] = Fraction(3)
    P = {(0, 1): Fraction(1)}
    P.update(tau)
    return {k: v for k, v in P.items() if v != 0}


def chain(k):
    """P = A + B^2 with A = x + y^2, B = y + A^k; [P, B] = 1, deg P = 4k and
    the smallest mate of P is B, of degree 2k."""
    A = {(1, 0): Fraction(1), (0, 2): Fraction(1)}
    B = M.padd({(0, 1): Fraction(1)}, M.ppow(A, k))
    P = M.padd(A, M.pmul(B, B))
    return {k2: v for k2, v in P.items() if v != 0}, B


def run(name, P, stages, expect_mate=True):
    say("=" * 78)
    say("%s   deg P = %d, |supp P| = %d" % (name, M.pdeg(P), len(P)))
    t0 = time.time()
    job = {"arm": "control", "P": P, "family": "control", "tag": name,
           "certs": {}, "stages": stages}
    rec = v2.run_one(job)
    say("  SY: %s (nodes=%d leaves=%d)"
        % (rec["SY_verdict"], rec["SY_nodes"], rec["SY_leaves"]))
    for s in rec["stages"]:
        say("  deg Q <= %-4d %-14s n_raw=%-6d thin=%-2d n=%-6d defl=%-3d -> %-14s [%s]"
            % (s.get("deg_Q_bound"), s.get("carrier"), s.get("n_raw"),
               s.get("thin_t"), s.get("n_unknowns", 0),
               s.get("deflated_kernel_dim"), s.get("verdict"),
               s.get("certificate")))
    ok = True
    detail = ""
    if expect_mate:
        ok = (rec["outcome"] == "MATE" and rec.get("bracket_is_one") is True)
        if rec["outcome"] == "MATE":
            say("  mate found: deg Q = %d, |supp Q| = %d, [P,Q]-1 = 0 over Q: %s"
                % (rec["deg_Q"], len(rec["Q"]), rec["bracket_is_one"]))
            detail = "deg Q = %d, bracket ok = %s" % (rec["deg_Q"],
                                                      rec["bracket_is_one"])
        else:
            say("  NO MATE FOUND -- outcome %s" % rec["outcome"])
            detail = "outcome %s" % rec["outcome"]
    say("  (%.1fs)" % (time.time() - t0))
    rec["control_ok"] = ok
    rec["control_detail"] = detail
    return rec


def main():
    out = []
    say("night12 v2 controls -- the v1 controls stand (see controls_v1.py, "
        "15/15 PASS); these add the coordinate-of-similar-shape positive "
        "control the V2 brief requires.")
    say("")

    P1 = {(1, 0): Fraction(1), (0, 2): Fraction(1)}
    d1 = M.pdeg(P1)
    out.append(run("V2-POS-1  P = x + y^2", P1,
                   [(d1 - 1, "np", False), (d1 + 31, "np", False),
                    (d1 + 63, "np", True)]))

    P2 = shear(124)
    d2 = M.pdeg(P2)
    out.append(run("V2-POS-2  P = y + tau(x), deg tau = 124 (ARM A shape, g = 0)",
                   P2, [(d2 - 1, "np", False), (d2 + 31, "np", False),
                        (d2 + 63, "np", True)]))

    for (k, label) in ((11, "V2-POS-3"), (21, "V2-POS-4")):
        P3, B3 = chain(k)
        d3 = M.pdeg(P3)
        say("")
        say("  (chain k=%d: [P, B] - 1 = 0 over Q: %s; deg B = %d)"
            % (k, M.is_one(M.bracket(P3, B3)), M.pdeg(B3)))
        out.append(run("%s  P = A + B^2, A = x + y^2, B = y + A^%d "
                       "(coordinate, smallest mate degree %d)"
                       % (label, k, M.pdeg(B3)), P3,
                       [(d3 - 1, "np", False), (d3 + 31, "np", False),
                        (d3 + 63, "np", True)]))

    checks = [{"check": r["tag"], "ok": r["control_ok"],
               "detail": r["control_detail"]} for r in out]
    bad = [c for c in checks if not c["ok"]]
    gate = {"gate": "PASS" if not bad else "FAIL",
            "n_checks": len(checks), "n_failed": len(bad), "checks": checks}
    say("")
    say("=" * 78)
    say("V2 CONTROL GATE: %d checks, %d failed -> %s"
        % (len(checks), len(bad), gate["gate"]))
    for c in checks:
        say("  [%s] %-58s %s" % ("ok" if c["ok"] else "FAIL", c["check"],
                                 c["detail"]))

    json.dump({"controls": out, "gate": gate},
              open(os.path.join(HERE, "controls_v2.json"), "w"), indent=1)
    open(os.path.join(HERE, "controls_v2_log.txt"), "w").write("\n".join(LOG) + "\n")
    return 0 if gate["gate"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
