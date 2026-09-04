"""
ITEM 3 -- controls for the above-125 (Track D / H2) elimination engine, and a
correction to the control that shipped with it.

THE SHIPPED CONTROL IS VACUOUS
------------------------------
campaign/audit_tracks/trackD_twoprime.py::control() builds the Singular source
and then forms an "unsaturated" variant by deleting

        every line containing the substring "sat"
        every line beginning with "ideal N"

The generated source contains NEITHER.  Its non-degeneracy conditions are
imposed by the Rabinowitsch lines

        I = I + ideal(w*p10 - 1);
        I = I + ideal(u*nd  - 1);

so the "unsaturated" variant is byte-identical to the real one, returns EMPTY,
and the control reports FAIL for a reason that has nothing to do with the
engine.  Running it as shipped:

        FAIL  positive control: unsaturated system is NOT empty   [EMPTY]

That is the control failing, not the engine.  This module supplies controls
that actually vary the input:

  C1 POSITIVE  delete the two Rabinowitsch generators.  The all-zero point then
               satisfies every remaining generator, so the ideal is proper and
               the engine must NOT say EMPTY.
  C2 NEGATIVE  add a contradictory pin to the real system.  The engine must say
               EMPTY.
  C3 NEGATIVE  the deletion in C1 must really change the source; the byte
               difference is asserted, which is exactly what the shipped
               control failed to do.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.environ.get("TRACKD_SRC",
                                  "/home/user/jacobian_planar/campaign/audit_tracks"))
import json

import trackD_extract as EX

RESULTS = []
RAB = re.compile(r"^\s*I\s*=\s*I\s*\+\s*ideal\(\s*[a-zA-Z]\w*\s*\*\s*\w+\s*-\s*1\s*\)\s*;\s*$")


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def run_src(src, tag, timeout=600):
    fn = os.path.join(EX.SCRATCH, f"h2ctl_{tag}.sing")
    os.makedirs(EX.SCRATCH, exist_ok=True)
    open(fn, "w").write(src)
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        return pr.stdout or pr.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def verdict(out):
    if out == "TIMEOUT":
        return "TIMEOUT"
    if "VERDICT: EMPTY" in out:
        return "EMPTY"
    if "live component" in out:
        return "LIVE"
    return "UNPARSED"


def main():
    targets = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "trackD_targets.json")))
    t = targets[0]
    src, info = EX.build_singular(t["NP"], t["NQ"], t["r"], name="ctl")
    if src is None:
        raise SystemExit("target 0 is OUT OF SCOPE; controls cannot run")
    print("=" * 78)
    print("ITEM 3 -- H2 engine controls")
    print("=" * 78)
    print(f"  target: {t['tag'][:70]}   params {info['nparams']}")

    rab = [l for l in src.splitlines() if RAB.match(l)]
    check("C3 the Rabinowitsch (non-degeneracy) generators are found in the source",
          len(rab) >= 1, f"{len(rab)} found: {rab}")

    nosat = "\n".join(l for l in src.splitlines() if not RAB.match(l))
    check("C3b deleting them really changes the source (the shipped control's "
          "deletion changed nothing)", nosat != src,
          f"{len(src) - len(nosat)} bytes removed")
    shipped = "\n".join(l for l in src.splitlines()
                        if "sat" not in l.lower() and not l.strip().startswith("ideal N"))
    check("C3c the SHIPPED deletion changes nothing, which is why it fails",
          shipped == src, "byte-identical to the real source")

    v_real = verdict(run_src(src, "real"))
    v_nosat = verdict(run_src(nosat, "nosat"))
    print(f"    real system verdict: {v_real};  unsaturated verdict: {v_nosat}")
    check("C1 POSITIVE: with the non-degeneracy generators removed the engine "
          "does NOT say EMPTY", v_nosat not in ("EMPTY",), f"[{v_nosat}]")

    pin = src.replace('"params: "', 'I = I + ideal(c(1) - 1, c(1) - 2);\n"params: "')
    v_pin = verdict(run_src(pin, "pin"))
    check("C2 NEGATIVE: a contradictory pin makes the engine say EMPTY",
          v_pin == "EMPTY", f"[{v_pin}]")

    npass = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {npass}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
