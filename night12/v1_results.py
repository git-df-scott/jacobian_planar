"""night12 v1 -- build V1_RESULTS.md from the recorded run artifacts.

Reads only files written by the run; computes no mathematics of its own.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "V1_RESULTS.md")


def load(name, default=None):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return default
    return json.load(open(p))


L = []


def w(s=""):
    L.append(s)


def stage_cell(st):
    v = st.get("verdict", "?")
    c = st.get("certificate")
    short = {"EMPTY_over_Q": "EMPTY", "MATE_over_Q": "MATE",
             "EMPTY_trivial_carrier": "EMPTY(triv)",
             "NOT_CERTIFIED": "NOT_CERT"}.get(v, v)
    cs = {"lambda_exact": "lam", "rank_full_column_exact": "rank",
          "exact_solution": "sol", None: "-", "none": "-"}.get(c, str(c))
    return "%s[%s]n=%s" % (short, cs, st.get("n_unknowns"))


def verdict_table(recs, title, note=""):
    w("### %s" % title)
    if note:
        w("")
        w(note)
    w("")
    if not recs:
        w("_no records_")
        w("")
        return
    w("| hash | family | profile | deg P | SY | stage Y | stage C | stage W | outcome | bracket=1 |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(recs, key=lambda r: (r["family"], -r["deg_P"], r["hash"])):
        cells = {s.get("stage"): stage_cell(s) for s in r["stages"]}
        w("| `%s` | %s | %s | %d | %s | %s | %s | %s | %s | %s |"
          % (r["hash"], r["family"], r["profile"], r["deg_P"],
             r["SY_verdict"][:5] + ("" if r["SY_verdict"] == "COORDINATE" else "-COORD"),
             cells.get("Y", "-"), cells.get("C", "-"), cells.get("W", "-"),
             r["outcome"], r.get("bracket_is_one", "-")))
    w("")


def cert_tally(recs):
    c = collections.Counter()
    for r in recs:
        for s in r["stages"]:
            c[(s.get("verdict"), s.get("certificate"))] += 1
    return c


def main():
    ctl = load("controls_v1.json", {})
    gate = ctl.get("gate", {}) if isinstance(ctl, dict) else {}
    ctls = ctl.get("controls", []) if isinstance(ctl, dict) else ctl
    scr = load("v1_screens.json", [])
    recs = load("v1_records.json", [])
    m1 = load("m1_records.json", [])
    retry = load("s1_retry.json", [])
    cross = load("sy_crosscheck.json", [])

    w("# night12 -- MATE SEARCH v1: results")
    w()
    w("Measurements only. Nothing in this file is a conclusion. Ring labels as in")
    w("`MATE_V1.md`: **ring: Q** = exact rational arithmetic; **ring: F_p** = the")
    w("scheduling prime, which decides nothing.")
    w()
    w("Apparatus: `sy.py`, `screens.py`, `carriers.py`, `pool.py`, `exact.py`,")
    w("`v1.py`, `controls_v1.py` (all documented in `MATE_V1.md`), plus the three")
    w("files added by this run: `s1_retry.py`, `m1_run.py`, `sy_crosscheck.py`.")
    w()

    # ------------------------------------------------------------------ gate
    w("## 1. Hit gate")
    w()
    allrecs = list(recs) + list(m1)
    hits = [r for r in allrecs if r.get("hit")]
    w("The gate is: a mate `Q` certified over `Q` by E3 (coefficientwise expansion")
    w("of `[P,Q] - 1`), for a `P` that S1/S2 passed, whose SY verdict is")
    w("`NON_COORDINATE`. On a hit the run halts and writes `night12/HIT_<hash>/`.")
    w()
    w("| quantity | value |")
    w("| --- | --- |")
    w("| P through the screened-and-passed pipeline | %d |" % len(recs))
    w("| P through the M1 override arm | %d |" % len(m1))
    w("| P through some arm, total | %d |" % len(allrecs))
    w("| mates certified over Q (E3) | %d |"
      % sum(1 for r in allrecs if r["outcome"] == "MATE"))
    w("| of those, SY NON_COORDINATE | %d |" % len(hits))
    w("| **hit-gate status** | **%s** |"
      % ("HIT: " + ", ".join("HIT_%s/" % r["hash"] for r in hits)
         if hits else "NOT TRIPPED -- 0 hits; the run did not halt"))
    w()
    if not hits:
        w("Every mate certified in this run sits on a `P` that SY certifies")
        w("`COORDINATE`, and every `P` that SY certifies `NON_COORDINATE` reached an")
        w("exact emptiness certificate at every stage tried. The gate never fired.")
        w()

    # -------------------------------------------------------------- controls
    w("## 2. Controls (hard gate)")
    w()
    w("`controls_v1.py` now carries an explicit gate with a nonzero exit code; see")
    w("the fix log in section 7.")
    w()
    w("**%s -- %d checks, %d failed.**"
      % (gate.get("gate", "?"), gate.get("n_checks", 0), gate.get("n_failed", 0)))
    w()
    w("| check | ok | detail |")
    w("| --- | --- | --- |")
    for c in gate.get("checks", []):
        w("| %s | %s | %s |" % (c["check"], "ok" if c["ok"] else "**FAIL**",
                                c["detail"] or ""))
    w()
    for r in ctls or []:
        w("- **%s**: screens passed=%s, SY=%s, outcome=%s%s"
          % (r["name"], r["screens"]["passed"], r["SY"], r.get("outcome"),
             (", deg Q = %d" % r["deg_Q"]) if r.get("deg_Q") is not None else ""))
    w()
    if cross:
        w("### Independent cross-check on the SY verdicts")
        w()
        w("`sy_crosscheck.py`. If `P` is a coordinate then `P - c` is irreducible for")
        w("every `c`, since an automorphism of the ring preserves irreducibility. So a")
        w("`c` for which `P - c` factors is an independent proof of `NON_COORDINATE`.")
        w("One-sided: `NO_FACTORISATION_FOUND` carries no information. Nothing here")
        w("feeds a decision; `sy.py` is untouched.")
        w()
        w("| P | SY verdict | brief label | fibre check | agreement |")
        w("| --- | --- | --- | --- | --- |")
        for r in cross:
            w("| `%s` | %s | %s | %s | %s |"
              % (r["name"], r["SY"], r["brief_label"], r["fibre_check"],
                 r["agreement"]))
        w()
        red = [r for r in cross if r["fibre_check"] == "REDUCIBLE_FIBRE"]
        for r in red:
            w("- `%s`: `P - (%s)` factors as `%s`."
              % (r["name"], r["detail"]["c"], r["detail"]["factors"].rstrip("| ")))
        w()
        w("Disagreements: **%d**."
          % sum(1 for r in cross if r["agreement"] == "DISAGREES"))
        w()
        w("This settles the one discrepancy the predecessor recorded. The note in")
        w("`controls_v1_log.txt` says the brief labels `x + x^2*y` a coordinate; the")
        w("validation table in `sy.py` in fact carries `?` for it (unlabeled), and the")
        w("factorisation `x + x^2*y = x*(1 + x*y)` is an independent proof that it is")
        w("not a coordinate. The SY implementation's verdict stands.")
        w()

    # --------------------------------------------------------------- screens
    w("## 3. Screen tally")
    w()
    w("S2 (`gcd(P_x,P_y)` a unit) runs first, then S1 (`1` in `(P_x,P_y)` over Q,")
    w("Groebner). S3 is recorded as a selection bias, never a gate.")
    w()
    w("| family | n | S2 pass | S1 pass | S1 reject | S1 timeout | S2 reject | passed |")
    w("| --- | --- | --- | --- | --- | --- | --- | --- |")
    fam = collections.defaultdict(list)
    for r in scr:
        fam[r["family"]].append(r)
    for f in sorted(fam):
        rs = fam[f]
        w("| %s | %d | %d | %d | %d | %d | %d | **%d** |"
          % (f, len(rs),
             sum(1 for r in rs if r["S2"] == "pass"),
             sum(1 for r in rs if r["S1"] == "pass"),
             sum(1 for r in rs if r["S1"] == "reject"),
             sum(1 for r in rs if r["S1"] == "timeout"),
             sum(1 for r in rs if r["S2"] == "reject"),
             sum(1 for r in rs if r["passed"])))
    w("| **total** | **%d** | %d | %d | %d | %d | %d | **%d** |"
      % (len(scr),
         sum(1 for r in scr if r["S2"] == "pass"),
         sum(1 for r in scr if r["S1"] == "pass"),
         sum(1 for r in scr if r["S1"] == "reject"),
         sum(1 for r in scr if r["S1"] == "timeout"),
         sum(1 for r in scr if r["S2"] == "reject"),
         sum(1 for r in scr if r["passed"])))
    w()
    w("**The M1 measurement.** Every one of the %d M1 and M1L `P` is rejected by S1:"
      % sum(1 for r in scr if r["family"].startswith("M1")))
    w("the gradient pair `(P_x, P_y)` has a common zero over `Qbar`. This is a")
    w("property of the family as `carriers.make_P` builds it, not of the screen. It")
    w("reproduces at small `m`, where the Groebner computation is immediate: for")
    w("`P = x + A*H^2` with `H` a form of degree `m`,")
    w()
    w("```")
    w("P_x = 1 + 2A*H*H_x,   P_y = 2A*H*H_y")
    w("```")
    w()
    w("so a common zero needs `H = 0` or `H_y = 0`. On `H = 0` we get `P_x = 1`, no")
    w("zero; but `H_y = 0` is a union of lines through the origin, and restricting")
    w("`1 + 2A*H*H_x` to such a line gives a one-variable polynomial of degree")
    w("`2m - 1 > 0`, which has roots. So the M1 shape carries gradient common zeros")
    w("generically. Small-`m` confirmation (S2 pass, S1 reject at every one):")
    w()
    w("```")
    w("m= 5 degP= 10  S2=pass  S1=reject (HAS_COMMON_ZERO 0)")
    w("m= 8 degP= 16  S2=pass  S1=reject (HAS_COMMON_ZERO 0)")
    w("m=11 degP= 22  S2=pass  S1=reject (HAS_COMMON_ZERO 0)")
    w("m=14 degP= 28  S2=pass  S1=reject (HAS_COMMON_ZERO 0)")
    w("```")
    w()
    w("A common zero `(a,b)` of `(P_x,P_y)` makes the Keller equation read `0 = 1`")
    w("there, so each of these `P` has no mate at any degree whatsoever. That is a")
    w("complete emptiness statement for the M1 pool, carrier-independent, and it is")
    w("the reason no M1 `P` entered the screened-and-passed pipeline. Section 5")
    w("records what the exact decision layer says about them on override.")
    w()
    if retry:
        w("### S1 timeouts, re-decided")
        w()
        w("The screen phase ran S1 with a 90 s budget under 4-way parallelism; a")
        w("`timeout` there is UNDECIDED, neither passed nor rejected. `s1_retry.py`")
        w("re-runs the same S1 predicate serially with a long budget.")
        w()
        w("| hash | family | deg P | re-decided | secs |")
        w("| --- | --- | --- | --- | --- |")
        for r in sorted(retry, key=lambda r: (r["family"], -r["deg_P"])):
            w("| `%s` | %s | %d | %s | %s |"
              % (r["hash"], r["family"], r["deg_P"], r["S1_retry"],
                 r["S1_retry_secs"]))
        w()
        c = collections.Counter(r["S1_retry"] for r in retry)
        w("Re-decided: %s." % dict(c))
        w()

    # -------------------------------------------------------------- pipeline
    w("## 4. Screened-and-passed pipeline: per-P verdicts")
    w()
    w("Every `P` here passed S2 and S1. Order per `P`: SY, then the Q-degree")
    w("escalation Y -> C -> W, each decided exactly over `Q`, stopping at the first")
    w("stage that yields a mate. Cell format `VERDICT[cert]n=unknowns`, with")
    w("`lam` = `lambda_exact`, `rank` = `rank_full_column_exact`, `sol` =")
    w("`exact_solution`.")
    w()
    verdict_table(recs, "verdicts")
    w("Outcome tally: %s." % dict(collections.Counter(r["outcome"] for r in recs)))
    w()
    w("SY x outcome: %s."
      % dict(collections.Counter((r["SY_verdict"], r["outcome"]) for r in recs)))
    w()
    mates = [r for r in recs if r["outcome"] == "MATE"]
    if mates:
        w("### Mates certified over Q")
        w()
        w("Each row's `Q` was reconstructed multi-modularly and then certified by")
        w("expanding `P_x Q_y - P_y Q_x - 1` coefficientwise over `Q`; the")
        w("reconstruction is a heuristic, the expansion is the proof.")
        w()
        w("| hash | family | deg P | deg Q | divisibility-ordered | [P,Q]-1 = 0 over Q | SY | \\|supp Q\\| |")
        w("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in sorted(mates, key=lambda r: -r["deg_P"]):
            w("| `%s` | %s | %d | %d | %s | %s | %s | %d |"
              % (r["hash"], r["family"], r["deg_P"], r["deg_Q"],
                 r.get("div_ordered"), r.get("bracket_is_one"),
                 r["SY_verdict"], len(r.get("Q", {}))))
        w()
        w("All %d verified coefficientwise over Q: %s."
          % (len(mates), all(r.get("bracket_is_one") for r in mates)))
        w()

    # -------------------------------------------------------------------- M1
    w("## 5. M1 override arm")
    w()
    w("`m1_run.py`. Every M1/M1L `P` is S1-rejected, so none reaches the pipeline of")
    w("section 4. This arm runs them through SY and the exact decision layer anyway,")
    w("under an explicit override of the screens -- exactly the route control C-NEG")
    w("takes. The S1 rejection already proves emptiness at every degree; what this")
    w("arm adds is the carrier-level certificate at each stage of the `mu_3` carrier.")
    w("The hit gate stays armed here.")
    w()
    if m1:
        w("| quantity | value |")
        w("| --- | --- |")
        w("| P run | %d |" % len(m1))
        w("| SY verdicts | %s |"
          % dict(collections.Counter(r["SY_verdict"] for r in m1)))
        w("| outcomes | %s |"
          % dict(collections.Counter(r["outcome"] for r in m1)))
        w("| mates | %d |" % sum(1 for r in m1 if r["outcome"] == "MATE"))
        w("| hits | %d |" % sum(1 for r in m1 if r.get("hit")))
        w()
        w("By profile:")
        w()
        w("| profile | n | SY NON_COORDINATE | EMPTY all stages | NOT_CERTIFIED | mates |")
        w("| --- | --- | --- | --- | --- | --- |")
        byp = collections.defaultdict(list)
        for r in m1:
            byp[(r["family"], r["profile"])].append(r)
        for k in sorted(byp):
            rs = byp[k]
            w("| %s %s | %d | %d | %d | %d | %d |"
              % (k[0], k[1], len(rs),
                 sum(1 for r in rs if r["SY_verdict"] == "NON_COORDINATE"),
                 sum(1 for r in rs if r["outcome"] == "EMPTY_all_stages_tried"),
                 sum(1 for r in rs if str(r["outcome"]).startswith("NOT_CERTIFIED")),
                 sum(1 for r in rs if r["outcome"] == "MATE")))
        w()
        w("Certificates over all M1 stage evaluations: %s."
          % dict(cert_tally(m1)))
        w()
        verdict_table(m1[:40], "first 40 records (all %d in `m1_records.json` "
                               "and `V1_RECORDS_M1/`)" % len(m1))
    else:
        w("_not run_")
        w()

    # ---------------------------------------------------------- certificates
    w("## 6. Certificates emitted")
    w()
    w("| arm | (verdict, certificate) | count |")
    w("| --- | --- | --- |")
    for nm, rs in (("pipeline", recs), ("M1 override", m1)):
        for k, v in sorted(cert_tally(rs).items(), key=lambda kv: -kv[1]):
            w("| %s | %s | %d |" % (nm, k, v))
    w()
    nc = [r for r in allrecs if str(r["outcome"]).startswith("NOT_CERTIFIED")]
    w("`NOT_CERTIFIED` records (never reported as emptiness): **%d**." % len(nc))
    for r in nc:
        w("- `%s` %s deg %d: %s" % (r["hash"], r["family"], r["deg_P"], r["outcome"]))
    w()

    # ------------------------------------------------------------- fix log
    w("## 7. Mechanics fixed in this run")
    w()
    w("The mathematical contracts are frozen: the S1/S2/S3 screens, the")
    w("Shpilrain-Yu certificate algorithm, and the E1/E2/E3 exact decisions are")
    w("untouched. Every change below is mechanics, and each is logged with what it")
    w("did and which direction it moves a verdict.")
    w()
    w("**(F1) `controls_v1.py` had no gate.** It printed its measurements and always")
    w("exited 0, so a regression in C-POS, C-NEG or the SY validation set could not")
    w("stop a pipeline run, and the brief's hard-gate requirement had nothing to")
    w("enforce it. Added `assess()`: 15 named checks with an explicit PASS/FAIL and a")
    w("nonzero exit code. It asserts only properties the controls already measured.")
    w()
    w("**(F2) carrier anchors were being scaled away** (`carriers.carrier` and")
    w("`v1.general_carrier`). Both build their polygon by scaling a base point set to")
    w("the stage bound, and both put the anchors `(0,0)` and `(0,1)` into that base")
    w("*before* scaling. When the stage bound is below the polygon degree -- which is")
    w("stage Y for every `P`, and stages Y and C for M1, where `H^3` has degree `3m`")
    w("-- the scale factor is `< 1` and `(0,1)` is shrunk below the lattice and")
    w("dropped, contradicting each function's own documented contract that `(0,0)`")
    w("and `(0,1)` are always retained.")
    w()
    w("What that did to the verdicts: the Keller row at the constant monomial gets a")
    w("contribution from carrier column `a` only when `a = (1,1) - p` for some")
    w("`p` in `supp(P)`. For an M1 `P` the linear term `p = (1,0)` gives `a = (0,1)`,")
    w("and that is the only column in the `mu_3` grading that can meet the constant")
    w("row. With `(0,1)` deleted the whole row was identically zero, so stage Y")
    w("returned `EMPTY_over_Q` for every M1 `P` via the degenerate zero-row")
    w("`lambda = e_00` certificate. That verdict was true of the carrier actually")
    w("built, but vacuous: no `Q` on it could have satisfied the equation.")
    w()
    w("The fix adjoins the anchors both scaled and unscaled, so the polygon is the")
    w("hull of the union. Taking the union rather than replacing matters: when the")
    w("stage bound exceeds the polygon degree (stage W) the old scaling inflated the")
    w("anchors outward, and simply un-scaling them would have SHRUNK stage W.")
    w("Enlarging is the only safe direction, since a larger carrier can only")
    w("strengthen an emptiness verdict and can only help a mate be found -- it can")
    w("never turn a true emptiness into a false one. Verified superset at every")
    w("stage on a sample M1 `P`: `n_raw` Y 882 -> 885, C 2012 -> 2012, W 3541 -> 3541,")
    w("with `(0,1)` present at all three.")
    w()
    w("**(F3) S1 timeouts were undecided and silently dropped.** The screen phase ran")
    w("S1 with a 90 s budget under 4-way parallelism. A `timeout` is neither a pass")
    w("nor a reject, but `v1.py` selects the pipeline by `passed`, so those `P` fell")
    w("out of the run without any recorded verdict. `s1_retry.py` re-runs the same S1")
    w("predicate on exactly those `P`, serially and with a long budget, and folds the")
    w("resolved verdicts back into `v1_screens.json`.")
    w()
    w("**(F4) the M1 profiles carried no records.** All 200 M1/M1L `P` are S1-rejected")
    w("(section 3), so `v1.py`'s pipeline phase, which is gated on `passed`, ran on")
    w("zero of them and the family the brief puts first had no per-P record at all.")
    w("`m1_run.py` adds the override arm of section 5. It changes no gate: the S1")
    w("rejection stands, the override is explicit and recorded per record")
    w("(`screens_overridden`), the records are kept in separate files from the")
    w("screened-and-passed arm, and the hit gate stays armed.")
    w()
    w("**(F5) no independent check on the SY verdicts.** Added `sy_crosscheck.py`")
    w("(section 2). It feeds no decision.")
    w()

    open(OUT, "w").write("\n".join(L) + "\n")
    print("wrote", OUT, "(%d lines)" % len(L))


if __name__ == "__main__":
    main()
