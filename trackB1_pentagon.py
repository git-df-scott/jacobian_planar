#!/usr/bin/env python3
"""
trackB1_pentagon.py — Track B1: GGHV Prop 4.3 case (1) (pentagon polygons),
the 186-unknown / 302-equation system nobody has ever attacked.

Subcommands:
  --derive   B1a: derive & machine-verify the top-edge structure
             (equations on the bracket line beta - alpha = 20 are exactly the
             coefficients of [L_P, L_Q] = 0; parametrization L_P = a*S^2,
             L_Q = b*S^3 verified as an identity; converse is the UFD lemma,
             written out in trackB1_report.md).
  --build    B1b: substitute the parametrization into the full system (exact
             Fractions), apply the 4 sound gauge normalizations
             d_2_1 = 1, s_0_4 = 1, a = 1, b = 1, and write
             trackB1_param_system.json (same schema as trackA_system_*.json,
             so trackA_eliminator.py consumes it directly).
  --singular TREE LEAF_ID P [NAME]
             B1c: generate + run a Singular mod-p scout for a leaf of an
             eliminator output tree, with Rabinowitsch ties for every nonzero
             variable AND every transferred nonzero_expr.

Everything exact over Q (fractions.Fraction); mod-p is scouting evidence only.

Variable conventions (chosen to match trackA machinery and the d_/c_ regex
style): S = sum_{p=0..4} s_p_{p+4} x^p y^{p+4}  (slope-1 form, lattice points
(0,4)..(4,8));  gauge parameters 'a', 'b' exist only transiently inside
--build (they are normalized to 1 before serialization).
"""

from fractions import Fraction
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Reuse the exact-Q polynomial machinery of the sound eliminator.
import trackA_eliminator as EL

CASE1_JSON = os.path.join(HERE, "trackA_system_case1.json")
CASE1_HASH = "49d28a2fd7ca72eb4064564d02084b2fab1612222d0c2c86b22ee1fe4702be9a"

# Edge lattice points
P_EDGE = [("c_%d_%d" % (i, i + 8), i) for i in range(0, 9)]      # (0,8)..(8,16)
Q_EDGE = [("d_%d_%d" % (k, k + 12), k) for k in range(0, 13)]    # (0,12)..(12,24)
S_VARS = ["s_%d_%d" % (p, p + 4) for p in range(0, 5)]           # (0,4)..(4,8)

P_EDGE_SET = {n for n, _ in P_EDGE}
Q_EDGE_SET = {n for n, _ in Q_EDGE}


# --------------------------------------------------------------------- helpers
def load_case1():
    with open(CASE1_JSON) as fh:
        data = json.load(fh)
    if data["content_hash"] != CASE1_HASH:
        raise SystemExit("FATAL: trackA_system_case1.json hash mismatch: %s"
                         % data["content_hash"])
    eqs = []
    for ser in data["equations"]:
        p = {}
        for mono, (num, den) in ser["terms"]:
            p[tuple((v, e) for v, e in mono)] = Fraction(num, den)
        eqs.append((tuple(ser["bracket_point"]), p))
    return data, eqs


def conv(A, B):
    """Convolution of two coefficient lists of dict-polys (poly in u)."""
    out = [dict() for _ in range(len(A) + len(B) - 1)]
    for i, pa in enumerate(A):
        for j, pb in enumerate(B):
            out[i + j] = EL.padd(out[i + j], EL.pmul(pa, pb))
    return out


def s_coeff_polys():
    return [EL.pvar(v) for v in S_VARS]


def build_submap():
    """c_{i,i+8} -> a*[S^2]_i ; d_{k,k+12} -> b*[S^3]_k  (dict-polys)."""
    S1 = s_coeff_polys()
    S2 = conv(S1, S1)                       # degrees 0..8
    S3 = conv(S2, S1)                       # degrees 0..12
    sub = {}
    for name, i in P_EDGE:
        sub[name] = EL.pmul(EL.pvar("a"), S2[i])
    for name, k in Q_EDGE:
        sub[name] = EL.pmul(EL.pvar("b"), S3[k])
    return sub


def subst_eq(p, submap):
    out = {}
    for m, c in p.items():
        term = {(): c}
        for (v, e) in m:
            rp = submap.get(v)
            if rp is None:
                term = EL.pmul(term, {((v, e),): Fraction(1)})
            else:
                term = EL.pmul(term, EL.ppow(rp, e))
        out = EL.padd(out, term)
    return out


def pdiff(p, x):
    """d/dx of a dict-poly."""
    out = {}
    for m, c in p.items():
        md = dict(m)
        e = md.get(x, 0)
        if e == 0:
            continue
        md[x] = e - 1
        if md[x] == 0:
            del md[x]
        mm = tuple(sorted(md.items()))
        out[mm] = out.get(mm, Fraction(0)) + c * e
    return {m: c for m, c in out.items() if c != 0}


def bracket(P, Q):
    """[P,Q] = Px Qy - Py Qx for dict-polys in x,y (other vars = coefficients)."""
    return EL.padd(EL.pmul(pdiff(P, "x"), pdiff(Q, "y")),
                   EL.pscale(EL.pmul(pdiff(P, "y"), pdiff(Q, "x")), Fraction(-1)))


# ------------------------------------------------------------------ B1a derive
def derive():
    data, eqs = load_case1()
    print("B1a: input hash OK (%s...)" % CASE1_HASH[:16])
    results = {}

    # C1/C2: equations on the line beta - alpha = 20 are exactly the predicted
    # edge bracket equations sum_{i+k=n+1} 4*(3i-2k) c_{i,i+8} d_{k,k+12} = 0,
    # n = 0..18.
    top = [(bp, p) for bp, p in eqs if bp[1] - bp[0] == 20]
    other = [(bp, p) for bp, p in eqs if bp[1] - bp[0] != 20]
    c1 = (len(top) == 19 and
          sorted(bp for bp, _ in top) == [(n, n + 20) for n in range(19)])
    print("C1: 19 top-line equations at (n, n+20), n=0..18: %s"
          % ("PASS" if c1 else "FAIL (%d found: %s)" %
             (len(top), sorted(bp for bp, _ in top))))
    results["C1"] = c1

    c2 = True
    for bp, p in top:
        n = bp[0]
        want = {}
        for i in range(0, 9):
            k = n + 1 - i
            if 0 <= k <= 12:
                w = 4 * (3 * i - 2 * k)
                if w == 0:
                    continue
                m = tuple(sorted([("c_%d_%d" % (i, i + 8), 1),
                                  ("d_%d_%d" % (k, k + 12), 1)]))
                want[m] = want.get(m, Fraction(0)) + w
        want = {m: c for m, c in want.items() if c != 0}
        if want != p:
            c2 = False
            print("C2 FAIL at %s" % (bp,))
    print("C2: each top-line equation == sum 4*(3i-2k)*c_{i,i+8}*d_{k,k+12} "
          "(coefficients of 4*(3f'g - 2fg') under f_i = c_{i,i+8}, "
          "g_k = d_{k,k+12}): %s" % ("PASS" if c2 else "FAIL"))
    results["C2"] = c2

    # C3: no edge-x-edge product occurs anywhere off the top line (so the
    # substitution touches ONLY terms linear in an edge variable elsewhere).
    c3 = True
    for bp, p in other:
        for m in p:
            vs = [v for v, _ in m]
            if len(vs) == 2 and vs[0] in P_EDGE_SET | Q_EDGE_SET \
                    and vs[1] in P_EDGE_SET | Q_EDGE_SET:
                c3 = False
                print("C3 FAIL: edge*edge term %s at %s" % (m, bp))
    print("C3: edge*edge products occur ONLY on the top line: %s"
          % ("PASS" if c3 else "FAIL"))
    results["C3"] = c3

    # C4: substituting c-edge = a*[S^2], d-edge = b*[S^3] kills every top-line
    # equation IDENTICALLY (symbolic a, b, s_p; exact Q).
    sub = build_submap()
    c4 = True
    for bp, p in top:
        r = subst_eq(p, sub)
        if r != {}:
            c4 = False
            print("C4 FAIL at %s: residue %s" % (bp, EL.pstr(r)))
    print("C4: L_P = a*S^2, L_Q = b*S^3 satisfies all 19 top-line equations "
          "identically: %s" % ("PASS" if c4 else "FAIL"))
    results["C4"] = c4

    # C5 (independent route): the bracket of generic slope-1 leading forms
    # P8 = sum f_i x^i y^{i+8}, Q12 = sum g_k x^k y^{k+12}, computed via
    # derivatives (independent code path: pdiff/pmul, NOT the builder's
    # convolution), equals  sum_n 4*[sum_{i+k=n+1} (3i-2k) f_i g_k] x^n y^{n+20}.
    P8 = {}
    for i in range(0, 9):
        P8[(("f%d" % i, 1), ("x", i), ("y", i + 8)) if i > 0 else
           (("f0", 1), ("y", 8))] = Fraction(1)
    # rebuild cleanly (monomials must be sorted tuples)
    P8 = {}
    for i in range(0, 9):
        m = [("f%d" % i, 1), ("y", i + 8)]
        if i > 0:
            m.append(("x", i))
        P8[tuple(sorted(m))] = Fraction(1)
    Q12 = {}
    for k in range(0, 13):
        m = [("g%d" % k, 1), ("y", k + 12)]
        if k > 0:
            m.append(("x", k))
        Q12[tuple(sorted(m))] = Fraction(1)
    br = bracket(P8, Q12)
    want = {}
    for n in range(0, 20):
        for i in range(0, 9):
            k = n + 1 - i
            if 0 <= k <= 12:
                w = 4 * (3 * i - 2 * k)
                if w == 0:
                    continue
                m = [("f%d" % i, 1), ("g%d" % k, 1), ("y", n + 20)]
                if n > 0:
                    m.append(("x", n))
                mm = tuple(sorted(m))
                want[mm] = want.get(mm, Fraction(0)) + w
    want = {m: c for m, c in want.items() if c != 0}
    c5 = (br == want)
    print("C5: derivative-route bracket of generic top edge forms == "
          "4*y^20*(3f'g - 2fg')(xy) coefficientwise: %s"
          % ("PASS" if c5 else "FAIL"))
    results["C5"] = c5

    # C6: the logarithmic-derivative identity behind the UFD step:
    # 3 f^2 f' g^2 - 2 f^3 g g'  ==  f^2 g (3 f' g - 2 f g')   (generic f,g).
    u = "u"
    f = {}
    for i in range(0, 9):
        m = [("f%d" % i, 1)]
        if i > 0:
            m.append((u, i))
        f[tuple(sorted(m))] = Fraction(1)
    g = {}
    for k in range(0, 13):
        m = [("g%d" % k, 1)]
        if k > 0:
            m.append((u, k))
        g[tuple(sorted(m))] = Fraction(1)
    fp, gp = pdiff(f, u), pdiff(g, u)
    f2 = EL.pmul(f, f)
    lhs = EL.padd(EL.pscale(EL.pmul(EL.pmul(f2, fp), EL.pmul(g, g)), Fraction(3)),
                  EL.pscale(EL.pmul(EL.pmul(f2, f), EL.pmul(g, gp)), Fraction(-2)))
    rhs = EL.pmul(EL.pmul(f2, g),
                  EL.padd(EL.pscale(EL.pmul(fp, g), Fraction(3)),
                          EL.pscale(EL.pmul(f, gp), Fraction(-2))))
    c6 = (lhs == rhs)
    print("C6: numerator identity of (f^3/g^2)' [g^2*(f^3)' - f^3*(g^2)' = "
          "f^2*g*(3f'g-2fg')]: %s" % ("PASS" if c6 else "FAIL"))
    results["C6"] = c6

    ok = all(results.values())
    print("B1a machine checks: %s" % ("ALL PASS" if ok else "FAILURES — see above"))
    with open(os.path.join(HERE, "trackB1_derivation.json"), "w") as fh:
        json.dump({"checks": results, "all_pass": ok,
                   "top_line_equations": 19,
                   "note": "converse (surjectivity of the parametrization) is "
                           "the UFD lemma, prose proof in trackB1_report.md "
                           "section B1a"}, fh, indent=1)
    return ok


# ------------------------------------------------------------------- B1b build
def build():
    data, eqs = load_case1()
    sub = build_submap()
    norm = {"d_2_1": 1, "s_0_4": 1, "a": 1, "b": 1}

    out_eqs = []          # (bracket_point, poly)
    dropped = []
    for bp, p in eqs:
        q = subst_eq(p, sub)
        for v, val in norm.items():
            q = EL.psub_var(q, v, EL.pconst(Fraction(val)))
        if not q:
            dropped.append(bp)
        else:
            out_eqs.append((bp, q))

    top_bps = sorted(bp for bp, p in eqs if bp[1] - bp[0] == 20)
    drop_ok = sorted(dropped) == top_bps
    print("build: %d equations dropped as identically zero; equals the 19 "
          "top-line equations exactly: %s"
          % (len(dropped), "PASS" if drop_ok else
             "FAIL — dropped %s" % sorted(dropped)))

    # sanity: the (2,0) equation must now read c_1_0 - 1 = 0
    eq20 = [p for bp, p in out_eqs if bp == (2, 0)]
    s20 = EL.pstr(eq20[0]) if eq20 else "MISSING"
    ok20 = s20 in ("1*c_1_0 + -1*1", "-1*1 + 1*c_1_0")
    print("build: (2,0) equation after normalization: '%s' (expect c_1_0 - 1): %s"
          % (s20, "PASS" if ok20 else "FAIL"))

    allvars = sorted(set().union(*[EL.pvars(p) for _, p in out_eqs]))
    prof = {}
    maxterms = 0
    for _, p in out_eqs:
        d = max((sum(e for _, e in m) for m in p), default=0)
        prof[d] = prof.get(d, 0) + 1
        maxterms = max(maxterms, len(p))
    print("build: %d equations / %d variables; degree profile %s; largest "
          "equation %d terms" % (len(out_eqs), len(allvars),
                                 dict(sorted(prof.items())), maxterms))

    # Nonzero side conditions surviving the substitution + normalization:
    #   c_1_0, c_8_14, d_12_21 (untouched vertices), s_4_8 (carries BOTH
    #   c_8_16 = a*s_4_8^2 != 0 and d_12_24 = b*s_4_8^3 != 0);
    #   c_0_8 = a*s_0_4^2 = 1, d_0_12 = b*s_0_4^3 = 1, d_2_1 = 1: satisfied.
    nonzero = ["c_1_0", "c_8_14", "d_12_21", "s_4_8"]

    ser_eqs = []
    for bp, p in out_eqs:
        terms = []
        for mono in sorted(p.keys()):
            terms.append([[list(ve) for ve in mono],
                          [p[mono].numerator, p[mono].denominator]])
        ser_eqs.append({"bracket_point": list(bp), "terms": terms})
    canon = "\n".join(
        "eq[%d,%d]=%s" % (e["bracket_point"][0], e["bracket_point"][1],
                          ";".join("%s:%s" % (
                              "*".join("%s^%d" % (v, ex) for v, ex in mono) or "1",
                              Fraction(num, den))
                              for mono, (num, den) in
                              [(tuple((v, ex) for v, ex in t[0]), t[1])
                               for t in e["terms"]]))
        for e in ser_eqs)
    h = hashlib.sha256(canon.encode()).hexdigest()
    outdata = {
        "meta": {
            "source": "Track B1: GGHV Prop 4.3 case (1) pentagons, top-edge "
                      "S-parametrization substituted",
            "input_system": "trackA_system_case1.json",
            "input_hash": CASE1_HASH,
            "substitution": "c_{i,i+8} = a*[S^2]_i (i=0..8), "
                            "d_{k,k+12} = b*[S^3]_k (k=0..12), "
                            "S = sum_p s_p_{p+4} x^p y^{p+4}",
            "normalizations": {k: str(v) for k, v in norm.items()},
            "gauge_argument": "A2 torus (d_2_1=1, proved case 1) + "
                              "S-rescaling mu (fixes s_0_4=1; acts trivially "
                              "on all c,d) + residual (s,t) 2-torus with "
                              "exponent matrix [[-1,8],[-2,11]], det 5 != 0 "
                              "(fixes a=b=1 over Qbar). Sound for "
                              "closure/emptiness over Qbar; see trackB1_report.md",
            "vertex_conditions_transferred": {
                "c_0_8": "a*s_0_4^2 = 1 (satisfied)",
                "c_8_16": "a*s_4_8^2 != 0  <=>  s_4_8 != 0",
                "d_0_12": "b*s_0_4^3 = 1 (satisfied)",
                "d_12_24": "b*s_4_8^3 != 0  <=>  s_4_8 != 0",
                "d_2_1": "= 1 (satisfied)"},
        },
        "variables": allvars,
        "nonzero": nonzero,
        "equations": ser_eqs,
        "content_hash": h,
    }
    out = os.path.join(HERE, "trackB1_param_system.json")
    with open(out, "w") as fh:
        json.dump(outdata, fh)
    print("build: written %s (content hash %s)" % (out, h))
    return drop_ok and ok20


# ------------------------------------------------------------ B1b/2 truncation
def truncate(W):
    """Write the weight->=W closed subsystem of trackB1_param_system.json.

    Soundness: the (-1,1)-weight of a bracket point (alpha,beta) is
    beta - alpha and the bracket adds weights, so an equation of weight w only
    involves c-vars on lines j - i >= w - 12 and d-vars on lines l - k >= w - 8
    (s-vars carry the top edges, weight 4 as parts of S). Hence
    {equations of weight >= W} is closed in the tower variables, every full
    solution restricts to a truncation solution, and an EMPTY truncation
    (subject to the side conditions on the variables it contains) kills
    case (1) outright.
    """
    src = os.path.join(HERE, "trackB1_param_system.json")
    data = json.load(open(src))
    keep = [e for e in data["equations"]
            if e["bracket_point"][1] - e["bracket_point"][0] >= W]
    vars_used = sorted(set(v for e in keep for t in e["terms"] for v, _ in t[0]))
    nonzero = [v for v in data["nonzero"] if v in vars_used]
    canon = []
    for e in keep:
        parts = []
        for t in e["terms"]:
            mono = tuple((v, ex) for v, ex in t[0])
            num, den = t[1]
            parts.append("%s:%s" % ("*".join("%s^%d" % (v, ex)
                                             for v, ex in mono) or "1",
                                    Fraction(num, den)))
        canon.append("eq[%d,%d]=%s" % (e["bracket_point"][0],
                                       e["bracket_point"][1], ";".join(parts)))
    h = hashlib.sha256("\n".join(canon).encode()).hexdigest()
    out = {
        "meta": {"source": "Track B1 weight tower: equations of (-1,1)-weight "
                           ">= %d of trackB1_param_system.json" % W,
                 "parent_hash": data["content_hash"],
                 "threshold": W,
                 "soundness": "closed subsystem; empty truncation => case (1) "
                              "dead; converse false (truncation only necessary)"},
        "variables": vars_used, "nonzero": nonzero, "equations": keep,
        "content_hash": h}
    path = os.path.join(HERE, "trackB1_trunc%d.json" % W)
    with open(path, "w") as fh:
        json.dump(out, fh)
    print("truncate W=%d: %d equations / %d variables, nonzero=%s -> %s (hash %s...)"
          % (W, len(keep), len(vars_used), nonzero, path, h[:12]))
    return path


# -------------------------------------------------------------- B1b/3 witness
def witness():
    """Exact witness: P = Stilde^2, Q = Stilde^3 with
    Stilde = y^4*(1 + (xy)^4) + t*x^4*y^7   (t = 1).

    [P, Q] = 0 identically and P/Q are supported inside N(P)/N(Q), so the point
    satisfies every equation of the UNNORMALIZED case-(1) system except the
    inhomogeneous (2,0) one. In the NORMALIZED system (d_2_1 = 1 baked in,
    while the family has d_2_1 = 0) it additionally fails exactly the six
    equations where d_2_1 multiplies a nonzero family coefficient — bracket
    points (1,8), (5,11), (5,12), (9,14), (9,15), (9,16), all of weight
    (beta - alpha) <= 7. Expected failure set (verified below):
      (2,0) [weight -2, the x^2 equation] and those six [weights 5..7].
    Side conditions: s_4_8 = 1, c_8_14 = t^2 = 1, d_12_21 = t^3 = 1 nonzero.

    Consequences (certified by this run):
    - every normalized weight truncation W >= 8 is ALIVE (the restriction of
      this point to the tower variables satisfies it, side conditions incl.);
    - any death of case (1) MUST use equations of weight <= 7 — i.e. must
      engage the bottom-vertex data c_1_0 * d_2_1 = 1 against the top
      structure; the system minus that data admits this exact solution.
      (On the family c_1_0 = d_2_1 = 0 is FORCED: a coefficient at (1,0)
      resp. (2,1) of a square resp. cube supported in N(P)/N(Q) is
      impossible with nonzero value — squares would need x^2- resp.
      x^4y^2-support outside the polygons.)
    """
    data = json.load(open(os.path.join(HERE, "trackB1_param_system.json")))
    t = Fraction(1)
    assign = {
        "s_1_5": Fraction(0), "s_2_6": Fraction(0), "s_3_7": Fraction(0),
        "s_4_8": Fraction(1),
        "c_4_11": 2 * t, "c_8_15": 2 * t, "c_8_14": t * t,
        "d_4_15": 3 * t, "d_8_19": 6 * t, "d_12_23": 3 * t,
        "d_8_18": 3 * t * t, "d_12_22": 3 * t * t,
        "d_12_21": t * t * t,
    }
    fails = []
    for e in data["equations"]:
        tot = Fraction(0)
        for mono, (num, den) in [(tuple((v, ex) for v, ex in tt[0]), tt[1])
                                 for tt in e["terms"]]:
            term = Fraction(num, den)
            for v, ex in mono:
                term *= assign.get(v, Fraction(0)) ** ex
            tot += term
        if tot != 0:
            fails.append((tuple(e["bracket_point"]), str(tot)))
    expected = sorted([(2, 0), (1, 8), (5, 11), (5, 12), (9, 14), (9, 15),
                       (9, 16)])
    got = sorted(bp for bp, _ in fails)
    max_fail_weight = max(bp[1] - bp[0] for bp, _ in fails) if fails else None
    ok = (got == expected and max_fail_weight == 7)
    print("witness: failing equations: %s" % fails)
    print("witness: failure set == the (2,0) x^2-equation + the six "
          "d_2_1-interaction equations, all of weight <= 7: %s"
          % ("PASS" if ok else "FAIL"))
    sides = {v: str(assign.get(v, Fraction(0))) for v in
             ["c_1_0", "c_8_14", "d_12_21", "s_4_8"]}
    print("witness side-condition values:", sides,
          "(c_1_0 = d_2_1 = 0 is forced on the family; the normalized system "
          "has d_2_1 = 1 baked in — hence the six weight-5..7 failures)")
    with open(os.path.join(HERE, "trackB1_witness.json"), "w") as fh:
        json.dump({"assignment": {k: [v.numerator, v.denominator]
                                  for k, v in assign.items()},
                   "all_other_vars": 0,
                   "family": "P = Stilde^2, Q = Stilde^3, Stilde = "
                             "y^4*(1+(xy)^4) + t*x^4*y^7, t = 1",
                   "failing_equations": fails, "as_expected": ok,
                   "consequence": "normalized truncations W >= 8 ALIVE "
                                  "(witness passes all weight >= 8 equations "
                                  "+ side conditions); any kill of case (1) "
                                  "must use weight <= 7 equations, i.e. the "
                                  "bottom-vertex data c_1_0*d_2_1 = 1"},
                  fh, indent=1)
    return ok


# ------------------------------------------- B1b/4 case-1 vs case-2 (2,-1) tower
def tower_compare():
    """Certify: the subsystems {equations at bracket points with 2*alpha - beta
    >= w} of the RAW case-(1) and case-(2) systems are term-for-term identical
    for w >= 2, and diverge at w = 1.

    Reason (verified here by direct comparison, not assumed): the pentagon
    extras of case (1) are exactly the lattice points of (2,-1)-weight <= -1
    (P) resp. <= -1 (Q); every term of a bracket equation of weight w has its
    P-part weight t and Q-part weight u with t + u = w + 1, t <= 2, u <= 3, so
    w >= 2 forces t >= 0 and u >= 1 — lines shared by both cases.
    Consequence: any closure argument using only the slope-2-edge tower levels
    w >= 2 (the edge ODE at w = 4 sits here, x^2 included) applies to BOTH
    cases simultaneously; conversely case (1)'s specific content lives at
    (2,-1)-weight <= 1.
    """
    def load(path):
        data = json.load(open(path))
        out = {}
        for ser in data["equations"]:
            p = {}
            for mono, (num, den) in ser["terms"]:
                p[tuple((v, e) for v, e in mono)] = Fraction(num, den)
            out[tuple(ser["bracket_point"])] = p
        return out
    e1 = load(CASE1_JSON)
    e2 = load(os.path.join(HERE, "trackA_system_case2.json"))
    print("tower-compare: raw case (1) %d eqs, raw case (2) %d eqs"
          % (len(e1), len(e2)))
    ok_all = True
    for w in range(4, -9, -1):
        b1 = {bp for bp in e1 if 2 * bp[0] - bp[1] == w}
        b2 = {bp for bp in e2 if 2 * bp[0] - bp[1] == w}
        same_pts = b1 == b2
        same_eqs = same_pts and all(e1[bp] == e2[bp] for bp in b1)
        n_shared = len(b1 & b2)
        status = ("IDENTICAL" if same_eqs else
                  ("same points, different terms" if same_pts else
                   "different point sets (case1 %d / case2 %d, shared %d)"
                   % (len(b1), len(b2), n_shared)))
        print("  (2,-1)-weight %2d: %s" % (w, status))
        if w >= 2 and not same_eqs:
            ok_all = False
    print("tower-compare: levels w >= 2 identical between the two cases: %s"
          % ("PASS" if ok_all else "FAIL"))
    return ok_all


# ---------------------------------------------------------------- B1c singular
def singular_leaf(tree_path, leaf_id, p, name=None, timeout=3000):
    assert p % 3 == 1, "scouting prime must be = 1 mod 3"
    d = json.load(open(tree_path))
    leaf = next(n for n in d["nodes"] if n["id"] == leaf_id)
    eqs = leaf["equations"]
    nz_vars = list(leaf.get("nonzero", []))
    nz_exprs = [e for e in leaf.get("nonzero_exprs", [])]
    vs = sorted(set(v for e in eqs + nz_exprs
                    for v in re.findall(r"[cds]_\d+_\d+", e)),
                key=lambda s: (s[0], tuple(map(int, s.split("_")[1:]))))
    for v in nz_vars:
        if v not in vs:
            vs.append(v)
    wties = []
    k = 0
    for v in nz_vars:
        k += 1
        wties.append("w%d*(%s)-1" % (k, v))
    for ex in nz_exprs:
        k += 1
        wties.append("w%d*(%s)-1" % (k, ex))
    ws = ["w%d" % (i + 1) for i in range(k)]
    lines = ["ring R = %d, (%s), dp;" % (p, ",".join(vs + ws)), "ideal I;"]
    for i, e in enumerate(eqs):
        lines.append("I[%d] = %s;" % (i + 1, e))
    for j, t in enumerate(wties):
        lines.append("I[%d] = %s;" % (len(eqs) + j + 1, t))
    lines += [
        "short = 0;",
        '"NVARS: %d (incl %d rabinowitsch)";' % (len(vs) + len(ws), len(ws)),
        '"NEQS: %d";' % (len(eqs) + len(wties)),
        "ideal G = groebner(I);",
        '"GB done";',
        "int d = dim(G);",
        '"DIM: " + string(d) + " (in ring with rabinowitsch vars; '
        'rabinowitsch adds ' + str(len(ws)) + ' true dims iff locus nonempty)";',
        'if (d == 0) { "VDIM: " + string(vdim(G)); }',
        'if (d == 0) { "GBSIZE: " + string(size(G)); }',
        'if (d == -1) { "EMPTY: ideal = whole ring; branch DEAD mod %d"; }' % p,
        "quit;"]
    nm = name or ("trackB1_leaf%d_p%d" % (leaf_id, p))
    sname = os.path.join(HERE, nm + ".sing")
    open(sname, "w").write("\n".join(lines))
    t0 = time.time()
    r = subprocess.run(["Singular", "-q", sname], capture_output=True,
                       text=True, timeout=timeout)
    out = r.stdout
    open(os.path.join(HERE, nm + ".out"), "w").write(
        out + ("\n[stderr]\n" + r.stderr if r.stderr.strip() else ""))
    print("# %s: %.1fs, %d vars + %d w" % (nm, time.time() - t0, len(vs), len(ws)))
    for ln in out.splitlines():
        if any(t in ln for t in ("NVARS", "NEQS", "DIM", "VDIM", "GBSIZE",
                                 "EMPTY", "ELIM")):
            print(ln)
    return out


# ----------------------------------------------- B1b/5 level-19 identity check
def level19():
    """Independent verification of the substituted system one level below the
    top: its 20 equations of (-1,1)-weight 19 must equal, coefficient for
    coefficient, the first-order deformation equation

        [S^2, Q_11] + [P_7, S^3] = 0

    with S = y^4 + s_1_5 xy^5 + s_2_6 x^2y^6 + s_3_7 x^3y^7 + s_4_8 x^4y^8
    (s_0_4 = 1 normalized), P_7 = sum_i c_{i,i+7} x^i y^{i+7},
    Q_11 = sum_k d_{k,k+11} x^k y^{k+11}, computed via the derivative-route
    bracket (independent code path from the builder)."""
    data = json.load(open(os.path.join(HERE, "trackB1_param_system.json")))
    lvl = {}
    for e in data["equations"]:
        a, b = e["bracket_point"]
        if b - a == 19:
            p = {}
            for mono, (num, den) in [(tuple((v, ex) for v, ex in t[0]), t[1])
                                     for t in e["terms"]]:
                p[mono] = Fraction(num, den)
            lvl[(a, b)] = p
    print("level19: %d equations of weight 19 in the substituted system"
          % len(lvl))
    SS = {(("y", 4),): Fraction(1)}
    for pp in range(1, 5):
        SS[tuple(sorted([("s_%d_%d" % (pp, pp + 4), 1), ("x", pp),
                         ("y", pp + 4)]))] = Fraction(1)
    P7 = {}
    for i in range(0, 9):
        m = [("c_%d_%d" % (i, i + 7), 1), ("y", i + 7)]
        if i > 0:
            m.append(("x", i))
        P7[tuple(sorted(m))] = Fraction(1)
    Q11 = {}
    for k in range(0, 13):
        m = [("d_%d_%d" % (k, k + 11), 1), ("y", k + 11)]
        if k > 0:
            m.append(("x", k))
        Q11[tuple(sorted(m))] = Fraction(1)
    S2 = EL.pmul(SS, SS)
    S3 = EL.pmul(S2, SS)
    B = EL.padd(bracket(S2, Q11), bracket(P7, S3))
    # split B by x-degree: coefficient of x^m y^(m+19) as poly in the other vars
    got = {}
    for mono, c in B.items():
        md = dict(mono)
        m_x = md.pop("x", 0)
        m_y = md.pop("y", 0)
        assert m_y - m_x == 19, (mono, c)
        rest = tuple(sorted(md.items()))
        got.setdefault(m_x, {})[rest] = got.get(m_x, {}).get(rest,
                                                            Fraction(0)) + c
    got = {m: {mo: cc for mo, cc in p.items() if cc != 0}
           for m, p in got.items()}
    got = {m: p for m, p in got.items() if p}
    ok = True
    sys_by_x = {a: p for (a, b), p in lvl.items()}
    for m in sorted(set(got) | set(sys_by_x)):
        if got.get(m) != sys_by_x.get(m):
            ok = False
            print("  MISMATCH at x^%d: derived %s vs system %s"
                  % (m, len(got.get(m, {})), len(sys_by_x.get(m, {}))))
    print("level19: weight-19 equations == coefficients of "
          "[S^2, Q_11] + [P_7, S^3]: %s" % ("PASS" if ok else "FAIL"))
    return ok


# ------------------------------------------------------- shared singular runner
def run_singular(nm, lines, timeout, memcap_kb):
    """Write nm.sing, run Singular niced + vmem-capped, stream output straight
    to nm.out (survives container restarts), append a runner-status line."""
    sname = os.path.join(HERE, nm + ".sing")
    open(sname, "w").write("\n".join(lines))
    outp = os.path.join(HERE, nm + ".out")
    cmd = ("ulimit -v %d; exec nice -n 10 Singular -q %s > %s 2>&1"
           % (memcap_kb, sname, outp))
    t0 = time.time()
    try:
        r = subprocess.run(["bash", "-c", cmd], timeout=timeout)
        status = "exit %d" % r.returncode
    except subprocess.TimeoutExpired:
        status = "TIMEOUT after %ds" % timeout
    out = open(outp).read() if os.path.exists(outp) else ""
    with open(outp, "a") as fh:
        fh.write("\n[runner status] %s after %.1fs\n" % (status, time.time() - t0))
    print("# %s: %s, %.1fs" % (nm, status, time.time() - t0))
    for ln in out.splitlines():
        if any(t in ln for t in ("NVARS", "NEQS", "DIM", "VDIM", "GBSIZE",
                                 "EMPTY", "error", "STAGE", "DIED", "MEM-KB")):
            print(ln)
    return out


def poly_str(terms):
    """JSON term list -> Singular polynomial string."""
    parts = []
    for t in terms:
        mono = "*".join("%s^%d" % (v, ex) if ex > 1 else v for v, ex in t[0])
        num, den = t[1]
        cs = "%d" % num if den == 1 else "(%d/%d)" % (num, den)
        parts.append(cs + ("*" + mono if mono else ""))
    return " + ".join(parts)


# --------------------------------------------------- B1c weight-peeling scout
def peel(p, name=None, timeout=6600, memcap_kb=6500000):
    """Incremental GB down the weight tower, mod p, with per-stage ASCII
    checkpoints (NAME_W{W}.gbtxt) and RESUME from the lowest existing one.
    Ideal at stage W = ties + all equations of weight >= W; if 1 appears at
    stage W, print DIED-AT-STAGE W and stop (mod-p scouting evidence that the
    system with side conditions is empty, localized to weight level W)."""
    assert p % 3 == 1
    data = json.load(open(os.path.join(HERE, "trackB1_param_system.json")))
    nm = name or ("trackB1_peel_p%d" % p)
    vs = list(data["variables"])
    wties = ["w%d*(%s)-1" % (i + 1, v) for i, v in enumerate(data["nonzero"])]
    ws = ["w%d" % (i + 1) for i in range(len(wties))]
    by_w = {}
    for e in data["equations"]:
        a, b = e["bracket_point"]
        by_w.setdefault(b - a, []).append(poly_str(e["terms"]))
    levels = sorted(by_w, reverse=True)
    # resume: lowest W with an existing checkpoint
    done = [W for W in levels
            if os.path.exists(os.path.join(HERE, "%s_W%d.gbtxt" % (nm, W)))]
    start_after = min(done) if done else None
    todo = [W for W in levels if start_after is None or W < start_after]
    if not todo:
        print("peel: all stages already checkpointed; nothing to do")
        return
    lines = ["ring R = %d, (%s), dp;" % (p, ",".join(vs + ws)),
             "short = 0;", "ideal G;"]
    if start_after is None:
        lines.append("G = %s;" % ",".join(wties))
        lines.append('"PEEL start from ties (%d), levels %s down to %s";'
                     % (len(wties), todo[0], todo[-1]))
    else:
        ck = os.path.join(HERE, "%s_W%d.gbtxt" % (nm, start_after))
        lines.append('string s_ck = read("%s");' % ck)
        lines.append('execute("G = ideal(" + s_ck + ");");')
        lines.append('"PEEL resume after W=%d (GB size " + string(size(G)) + '
                     '"), levels %s down to %s";' % (start_after, todo[0],
                                                     todo[-1]))
    for W in todo:
        lines.append("ideal L%d = %s;" % (W + 100, ",".join(by_w[W])))
        lines.append("G = groebner(G + L%d);" % (W + 100))
        lines.append('"STAGE W=%d: GBSIZE: " + string(size(G)) + '
                     '" MEM-KB: " + string(memory(2) div 1024);' % W)
        lines.append('if (reduce(1, G) == 0) { "DIED-AT-STAGE: %d"; '
                     '"EMPTY: ideal = whole ring; system DEAD mod %d '
                     '(with side conditions)"; write(":w %s", "1"); quit; }'
                     % (W, p, os.path.join(HERE, "%s_W%d.gbtxt" % (nm, W))))
        lines.append('write(":w %s", G);'
                     % os.path.join(HERE, "%s_W%d.gbtxt" % (nm, W)))
    lines += ["int d = dim(G);",
              '"DIM: " + string(d) + " (ring includes %d rabinowitsch vars)";'
              % len(ws),
              'if (d == 0) { "VDIM: " + string(vdim(G)); }',
              'if (d == -1) { "EMPTY: ideal = whole ring; system DEAD mod %d '
              '(with side conditions)"; }' % p,
              "quit;"]
    return run_singular(nm, lines, timeout, memcap_kb)


# ------------------------------------------------------- B1c singular (system)
def singular_system(sys_path, p, name=None, timeout=3900, memcap_kb=1800000,
                    order="dp"):
    """mod-p Singular scout of a system JSON (trackB1_param_system.json schema):
    ideal = all equations + Rabinowitsch inverses for the nonzero list.
    Memory-capped via ulimit -v so it cannot disturb the Track B jobs."""
    assert p % 3 == 1, "scouting prime must be = 1 mod 3"
    data = json.load(open(sys_path))
    vs = list(data["variables"])
    polys = [poly_str(e["terms"]) for e in data["equations"]]
    wties = []
    for i, v in enumerate(data["nonzero"]):
        wties.append("w%d*(%s)-1" % (i + 1, v))
    ws = ["w%d" % (i + 1) for i in range(len(wties))]
    if order == "blockc":
        nc = sum(1 for v in vs if v.startswith("c_"))
        ordstr = "(dp(%d), dp(%d))" % (nc, len(vs) - nc + len(ws))
    else:
        ordstr = order
    lines = ["ring R = %d, (%s), %s;" % (p, ",".join(vs + ws), ordstr),
             "ideal I;"]
    for i, e in enumerate(polys):
        lines.append("I[%d] = %s;" % (i + 1, e))
    for j, t in enumerate(wties):
        lines.append("I[%d] = %s;" % (len(polys) + j + 1, t))
    nm = name or ("trackB1_sys_p%d" % p)
    lines += [
        "short = 0;",
        '"NVARS: %d (incl %d rabinowitsch)";' % (len(vs) + len(ws), len(ws)),
        '"NEQS: %d";' % (len(polys) + len(wties)),
        "option(prot);",
        "ideal G = groebner(I);",
        "option(noprot);",
        '"GB done";',
        '"MEM-KB: " + string(memory(2) div 1024);',
        '"GBSIZE: " + string(size(G));',
        "int d = dim(G);",
        '"DIM: " + string(d) + " (ring includes %d rabinowitsch vars)";'
        % len(ws),
        'if (d == 0) { "VDIM: " + string(vdim(G)); }',
        'if (d == -1) { "EMPTY: ideal = whole ring; system DEAD mod %d '
        '(with side conditions)"; }' % p,
        'write(":w %s", G);' % os.path.join(HERE, nm + ".gb.txt"),
        '"GB written";',
        "quit;"]
    return run_singular(nm, lines, timeout, memcap_kb)


# ===================================================================== TOWER
# Level-by-level linear tower solver (re-plan after the full-system GB blowup;
# see trackB1_report.md "Re-plan"). For FIXED (a, b, S) in F_p the case-(1)
# system with the top-edge parametrization is TRIANGULAR in the (-1,1)-weight:
# descending levels w = 19..-2, the level-w equations are affine-linear in the
# newest components P_{w-12} (c-vars on line j-i = w-12) and Q_{w-8} (d-vars on
# line l-k = w-8) — every other term pairs already-known components (a c-line
# pairs with the d-TOP line iff it is the newest one, and vice versa; mixed
# lower pairs were introduced at strictly higher levels). Free parameters
# (level-map kernels = moduli of the commuting family) are carried SYMBOLICALLY
# as tau-variables with mod-p polynomial arithmetic; consistency rows give
# obstruction polynomials in tau, which are substituted away when linear in
# some tau (exact operation over the field) or recorded. End state per sample:
# DEAD-at-level-w (an obstruction is a nonzero constant), or SURVIVOR with a
# residual tau-system (possibly empty = explicit point).
#
# Soundness: per sample this is Gaussian elimination over F_p on the exact
# level equations of the RAW hash-pinned system (with the identity C4 removing
# level 20), so verdicts are exact for that (a, b, S). The structural split
# (level equations == raw equations restricted, term classification) is
# machine-checked by --tower-check against random full assignments.

def _tw_madd(d, m, c, p):
    v = (d.get(m, 0) + c) % p
    if v:
        d[m] = v
    elif m in d:
        del d[m]


def tw_add(f, g, p):
    out = dict(f)
    for m, c in g.items():
        _tw_madd(out, m, c, p)
    return out


def tw_scale(f, c, p):
    c %= p
    if c == 0:
        return {}
    return {m: (cc * c) % p for m, cc in f.items()}


def tw_mul(f, g, p):
    out = {}
    for m1, c1 in f.items():
        for m2, c2 in g.items():
            md = dict(m1)
            for v, e in m2:
                md[v] = md.get(v, 0) + e
            _tw_madd(out, tuple(sorted(md.items())), c1 * c2, p)
    return out


def tw_const(f):
    """If f is a constant polynomial return the constant, else None."""
    if not f:
        return 0
    if len(f) == 1 and () in f:
        return f[()]
    return None


def tw_subst(f, var, rep, p):
    """Substitute tau-variable var := rep (a tau-poly) into f."""
    out = {}
    for m, c in f.items():
        md = dict(m)
        e = md.pop(var, 0)
        base = {tuple(sorted(md.items())): c}
        for _ in range(e):
            base = tw_mul(base, rep, p)
        out = tw_add(out, base, p)
    return out


def tower_precompute():
    """Sample-independent structure: slices, per-level classified equations."""
    data, eqs = load_case1()
    inert = {"c_0_0", "d_0_0"}
    cvars = {}
    dvars = {}
    for v in data["variables"]:
        if v in inert:
            continue
        kind, i, j = v.split("_")
        i, j = int(i), int(j)
        (cvars if kind == "c" else dvars)[v] = j - i
    # slices: weight -> ordered var list
    psl, qsl = {}, {}
    for v, w in cvars.items():
        psl.setdefault(w, []).append(v)
    for v, w in dvars.items():
        qsl.setdefault(w, []).append(v)
    for sl in (psl, qsl):
        for w in sl:
            sl[w].sort(key=lambda s: int(s.split("_")[1]))
    assert sorted(psl) == list(range(-1, 9)), sorted(psl)
    assert sorted(qsl) == list(range(-1, 13)), sorted(qsl)
    assert qsl[-1] == ["d_2_1"] and psl[-1] == ["c_1_0"]
    # group equations by weight; classify terms per level
    levels = {}
    for bp, poly in eqs:
        w = bp[1] - bp[0]
        levels.setdefault(w, []).append((bp, poly))
    assert max(levels) == 20 and min(levels) == -2
    # level-20 equations are killed identically by the parametrization (C4).
    lv = {}
    for w in range(19, -3, -1):
        lst = []
        for bp, poly in levels.get(w, []):
            newc, newd, known, const = [], [], [], 0
            for mono, coeff in poly.items():
                if len(mono) == 0:
                    const = coeff
                    continue
                # bilinear c*d terms (exponents always 1 in the raw system),
                # or the single inhomogeneous constant
                assert len(mono) == 2 and mono[0][1] == 1 and mono[1][1] == 1, \
                    (bp, mono)
                names = sorted(v for v, _ in mono)
                cn = [v for v in names if v.startswith("c")][0]
                dn = [v for v in names if v.startswith("d")][0]
                vc, vd = cvars[cn], dvars[dn]
                assert vc + vd == w, (bp, mono, vc, vd)
                if vc == w - 12 and -1 <= w - 12 <= 7 and vd == 12:
                    newc.append((cn, dn, coeff))
                elif vd == w - 8 and 0 <= w - 8 <= 11 and vc == 8:
                    newd.append((cn, dn, coeff))
                else:
                    known.append((cn, dn, coeff))
            lst.append({"bp": bp, "newc": newc, "newd": newd,
                        "known": known, "const": const})
        lv[w] = lst
    return {"psl": psl, "qsl": qsl, "cvars": cvars, "dvars": dvars,
            "levels": lv, "raw_eqs": eqs, "data": data}


def s_powers(svec, p):
    """[S^2] and [S^3] coefficient lists mod p for S with coeffs svec (len 5)."""
    s2 = [0] * 9
    for i in range(5):
        for j in range(5):
            s2[i + j] = (s2[i + j] + svec[i] * svec[j]) % p
    s3 = [0] * 13
    for i in range(9):
        for j in range(5):
            s3[i + j] = (s3[i + j] + s2[i] * svec[j]) % p
    return s2, s3


def tower_run(pre, p, a, b, svec, max_tau_terms=200000):
    """Run the tower for one (a, b, svec) sample mod p.

    Returns dict with outcome in {"DEAD", "SURVIVOR"}, dead_level,
    per-level stats, residual obstructions, component values (tau-polys),
    and the tau substitution log."""
    s2, s3 = s_powers(svec, p)
    topc = {v: (a * s2[i]) % p for i, v in enumerate(pre["psl"][8])}
    topd = {v: (b * s3[k]) % p for k, v in enumerate(pre["qsl"][12])}
    # value store: var name -> tau-poly (constants for top and d_2_1)
    val = {v: ({(): c} if c else {}) for v, c in topc.items()}
    for v, c in topd.items():
        val[v] = {(): c} if c else {}
    val["d_2_1"] = {(): 1}
    ntau = 0
    obstructions = []        # list of (level, tau-poly)
    subs_log = []            # (tau, level) substitutions applied
    stats = []
    dead = None

    def substitute(tau, rep, level):
        nonlocal obstructions
        for k in list(val):
            val[k] = tw_subst(val[k], tau, rep, p)
        newo = []
        for (lw, ob) in obstructions:
            ob2 = tw_subst(ob, tau, rep, p)
            c = tw_const(ob2)
            if c is None:
                newo.append((lw, ob2))
            elif c != 0:
                return ("DEAD", lw)
        obstructions = newo
        subs_log.append((tau, level))
        return None

    for w in range(19, -3, -1):
        eqs = pre["levels"][w]
        newvars = []
        if -1 <= w - 12 <= 7:
            newvars += pre["psl"][w - 12]
        if 0 <= w - 8 <= 11:
            newvars += pre["qsl"][w - 8]
        col = {v: i for i, v in enumerate(newvars)}
        nrow, ncol = len(eqs), len(newvars)
        M = [[0] * ncol for _ in range(nrow)]
        R = []
        for r, e in enumerate(eqs):
            if e["const"]:
                cst = (e["const"].numerator *
                       pow(e["const"].denominator, p - 2, p)) % p
            else:
                cst = 0
            rhs = {(): (-cst) % p} if cst else {}
            for cn, dn, coeff in e["newc"]:
                M[r][col[cn]] = (M[r][col[cn]] + coeff.numerator *
                                pow(coeff.denominator, p - 2, p) *
                                tw_const(val[dn])) % p
            for cn, dn, coeff in e["newd"]:
                M[r][col[dn]] = (M[r][col[dn]] + coeff.numerator *
                                pow(coeff.denominator, p - 2, p) *
                                tw_const(val[cn])) % p
            for cn, dn, coeff in e["known"]:
                cc = (coeff.numerator * pow(coeff.denominator, p - 2, p)) % p
                prod = tw_mul(val[cn], val[dn], p)
                rhs = tw_add(rhs, tw_scale(prod, (-cc) % p, p), p)
            R.append(rhs)
        # Gaussian elimination on M (numeric), applying row ops to R (tau-polys)
        piv = {}      # col -> row
        rowperm = list(range(nrow))
        rank = 0
        for c in range(ncol):
            sel = None
            for r in range(rank, nrow):
                if M[rowperm[r]][c] % p:
                    sel = r
                    break
            if sel is None:
                continue
            rowperm[rank], rowperm[sel] = rowperm[sel], rowperm[rank]
            pr = rowperm[rank]
            inv = pow(M[pr][c], p - 2, p)
            M[pr] = [(x * inv) % p for x in M[pr]]
            R[pr] = tw_scale(R[pr], inv, p)
            for r2 in range(nrow):
                pr2 = rowperm[r2]
                if pr2 != pr and M[pr2][c]:
                    f = M[pr2][c]
                    M[pr2] = [(x - f * y) % p for x, y in zip(M[pr2], M[pr])]
                    if R[pr]:
                        R[pr2] = tw_add(R[pr2], tw_scale(R[pr], (-f) % p, p), p)
            piv[c] = pr
            rank += 1
        # free columns -> fresh taus
        freecols = [c for c in range(ncol) if c not in piv]
        tau_of = {}
        for c in freecols:
            tau_of[c] = "t%d" % ntau
            ntau += 1
        # assign new component values
        for c, v in enumerate(newvars):
            if c in piv:
                expr = dict(R[piv[c]])
                for fc in freecols:
                    coefffc = M[piv[c]][fc]
                    if coefffc:
                        _tw_madd(expr, ((tau_of[fc], 1),), (-coefffc) % p, p)
                val[v] = expr
            else:
                val[v] = {((tau_of[c], 1),): 1}
        # consistency rows: zero M-row but nonzero RHS -> obstruction
        level_obs = 0
        for r in range(rank, nrow):
            pr = rowperm[r]
            ob = R[pr]
            cst = tw_const(ob)
            if cst is None:
                obstructions.append((w, ob))
                level_obs += 1
            elif cst != 0:
                dead = ("DEAD", w)
                break
        stats.append({"w": w, "eqs": nrow, "new": ncol, "rank": rank,
                      "kernel": len(freecols), "obstructions": level_obs})
        if dead:
            break
        # try to resolve obstructions LINEAR in a tau (exact substitution)
        progress = True
        while progress and not dead:
            progress = False
            for idx, (lw, ob) in enumerate(obstructions):
                lin = None
                for m, c in ob.items():
                    if len(m) == 1 and m[0][1] == 1:
                        t = m[0][0]
                        others = any(t == mv for mm, _ in ob.items()
                                     for mv, me in mm
                                     if mm != m and (mv == t))
                        if not others:
                            lin = (t, c, m)
                            break
                if lin:
                    t, c, m = lin
                    rest = {mm: cc for mm, cc in ob.items() if mm != m}
                    rep = tw_scale(rest, (-pow(c, p - 2, p)) % p, p)
                    del obstructions[idx]
                    dd = substitute(t, rep, lw)
                    if dd:
                        dead = dd
                    progress = True
                    break
        if dead:
            break
        # size guard
        total_terms = sum(len(v) for v in val.values())
        if total_terms > max_tau_terms:
            return {"outcome": "OVERFLOW", "level": w, "stats": stats,
                    "ntau": ntau, "total_terms": total_terms}
    if dead:
        return {"outcome": "DEAD", "dead_level": dead[1], "stats": stats,
                "ntau": ntau, "nsub": len(subs_log)}
    # survivor: residual obstruction system in surviving taus
    live_taus = sorted({v for (_, ob) in obstructions for m in ob
                        for v, _ in m},
                       key=lambda s: int(s[1:]))
    # vertex nonzero conditions that are tau-polys
    nz = {}
    for v in ("c_8_14", "d_12_21", "c_1_0"):
        nz[v] = val[v]
    return {"outcome": "SURVIVOR", "stats": stats, "ntau": ntau,
            "nsub": len(subs_log),
            "obstructions": [(lw, ob) for lw, ob in obstructions],
            "live_taus": live_taus, "val": val, "nonzero_polys": nz}


def tower_check(p=65521, seed=12345, n=5):
    """Structural validation: for random FULL assignments (all c, d numeric),
    the per-level assembled equations (M z - R with actual values) must equal
    the raw equations' values. Validates term classification/indexing/signs."""
    import random
    rng = random.Random(seed)
    pre = tower_precompute()
    ok_all = True
    for trial in range(n):
        assign = {}
        for v in list(pre["cvars"]) + list(pre["dvars"]):
            assign[v] = rng.randrange(p)
        # honest raw residuals by weight
        raw_by_bp = {}
        for bp, poly in pre["raw_eqs"]:
            tot = 0
            for mono, coeff in poly.items():
                t = (coeff.numerator * pow(coeff.denominator, p - 2, p)) % p
                for v, e in mono:
                    t = (t * pow(assign[v], e, p)) % p
                tot = (tot + t) % p
            raw_by_bp[bp] = tot
        # tower-side: for each level w <= 19, rebuild M,R with val := assign
        # (numeric) and check M z + (-R) == raw residual rowwise.
        for w in range(19, -3, -1):
            for e in pre["levels"][w]:
                tot = 0
                if e["const"]:
                    tot = (e["const"].numerator *
                           pow(e["const"].denominator, p - 2, p)) % p
                for grp in ("newc", "newd", "known"):
                    for cn, dn, coeff in e[grp]:
                        cc = (coeff.numerator *
                              pow(coeff.denominator, p - 2, p)) % p
                        cv = assign[cn] if cn != "d_2_1" else 1
                        dv = assign[dn]
                        tot = (tot + cc * cv * dv) % p
                if tot != raw_by_bp[e["bp"]]:
                    ok_all = False
                    print("tower-check MISMATCH at %s (w=%d)" % (e["bp"], w))
        # also: level-20 must be exactly the 19 parametrized-away equations
    n20 = sum(1 for bp, _ in pre["raw_eqs"] if bp[1] - bp[0] == 20)
    print("tower-check: level-20 equation count = %d (expect 19)" % n20)
    print("tower-check: raw-vs-assembled residual agreement on %d random "
          "assignments: %s" % (n, "PASS" if ok_all and n20 == 19 else "FAIL"))
    return ok_all and n20 == 19


def tower_scan(p, nsamples, seed=1, out_name=None, witness_first=True):
    """Random (a, b, S) scan mod p. Aggregates outcomes; checkpoints every
    25 samples; dumps any survivor's residual system."""
    import random
    assert p % 3 == 1
    rng = random.Random(seed)
    pre = tower_precompute()
    nm = out_name or ("trackB1_tower_scan_p%d" % p)
    path = os.path.join(HERE, nm + ".json")
    state = {"p": p, "seed": seed, "done": 0, "outcomes": {},
             "dead_levels": {}, "kernel_profile": None, "survivors": [],
             "overflow": 0, "started": time.time()}
    if os.path.exists(path):
        try:
            old = json.load(open(path))
            if old.get("p") == p and old.get("seed") == seed:
                state = old
                # fast-forward rng deterministically
                for _ in range(state["done"]):
                    for _ in range(6):
                        rng.randrange(p)
                print("tower-scan: resuming at sample %d" % state["done"])
        except Exception:
            pass
    t0 = time.time()
    first = state["done"] == 0
    while state["done"] < nsamples:
        if first and witness_first:
            a, b = 1, 1
            svec = [1, 0, 0, 0, 1]      # the exact-witness S (h = 1 + u^4)
            first = False
        else:
            a = 1 + rng.randrange(p - 1)
            b = 1 + rng.randrange(p - 1)
            svec = [1, rng.randrange(p), rng.randrange(p), rng.randrange(p),
                    1 + rng.randrange(p - 1)]
            rng.randrange(p)            # keep stride = 6 draws/sample
        res = tower_run(pre, p, a, b, svec)
        oc = res["outcome"]
        state["outcomes"][oc] = state["outcomes"].get(oc, 0) + 1
        if oc == "DEAD":
            dl = str(res["dead_level"])
            state["dead_levels"][dl] = state["dead_levels"].get(dl, 0) + 1
        elif oc == "OVERFLOW":
            state["overflow"] += 1
        elif oc == "SURVIVOR":
            surv = {"a": a, "b": b, "svec": svec,
                    "ntau": res["ntau"], "live_taus": res["live_taus"],
                    "n_obstructions": len(res["obstructions"]),
                    "obstruction_levels": sorted({lw for lw, _ in
                                                  res["obstructions"]}),
                    "obstruction_sizes": [len(ob) for _, ob in
                                          res["obstructions"]],
                    "nonzero_poly_sizes": {k: len(v) for k, v in
                                           res["nonzero_polys"].items()}}
            # store the residual system itself for small ones
            if sum(len(ob) for _, ob in res["obstructions"]) < 20000:
                surv["obstructions"] = [
                    [lw, [[list(map(list, m)), c] for m, c in ob.items()]]
                    for lw, ob in res["obstructions"]]
                surv["nonzero_polys"] = {
                    k: [[list(map(list, m)), c] for m, c in v.items()]
                    for k, v in res["nonzero_polys"].items()}
            state["survivors"].append(surv)
        if state["kernel_profile"] is None and oc in ("DEAD", "SURVIVOR"):
            state["kernel_profile"] = res["stats"]
        state["done"] += 1
        if state["done"] % 25 == 0 or state["done"] == nsamples:
            state["rate_per_s"] = state["done"] / max(1e-9, time.time() - t0)
            with open(path, "w") as fh:
                json.dump(state, fh)
            print("tower-scan: %d/%d done (%.1f/s) outcomes=%s dead_levels=%s"
                  " survivors=%d" % (state["done"], nsamples,
                                     state["rate_per_s"], state["outcomes"],
                                     state["dead_levels"],
                                     len(state["survivors"])), flush=True)
    with open(path, "w") as fh:
        json.dump(state, fh)
    print("tower-scan: DONE -> %s" % path)
    return state


# ----------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--derive", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--truncate", type=int, metavar="W")
    ap.add_argument("--witness", action="store_true")
    ap.add_argument("--tower-compare", action="store_true")
    ap.add_argument("--level19", action="store_true")
    ap.add_argument("--singular", nargs="+", metavar="ARG",
                    help="TREE LEAF_ID P [NAME]")
    ap.add_argument("--singular-system", nargs="+", metavar="ARG",
                    help="SYSTEM_JSON P [NAME [TIMEOUT_S [MEMCAP_KB [ORDER]]]]")
    ap.add_argument("--peel", nargs="+", metavar="ARG",
                    help="P [NAME [TIMEOUT_S [MEMCAP_KB]]] — weight-peeling "
                         "incremental GB with checkpoints + resume")
    ap.add_argument("--tower-check", action="store_true",
                    help="validate the tower level split against random full "
                         "assignments of the raw system")
    ap.add_argument("--tower-scan", nargs="+", metavar="ARG",
                    help="P NSAMPLES [SEED [NAME]] — random (a,b,S) tower scan")
    ap.add_argument("--tower-one", nargs="+", metavar="ARG",
                    help="P a b s1 s2 s3 s4 — run one tower sample verbosely "
                         "(s0 = 1)")
    args = ap.parse_args()
    if args.tower_check:
        ok = tower_check()
        sys.exit(0 if ok else 1)
    if args.tower_scan:
        a = args.tower_scan
        tower_scan(int(a[0]), int(a[1]), int(a[2]) if len(a) > 2 else 1,
                   a[3] if len(a) > 3 else None)
        return
    if args.tower_one:
        a = [int(x) for x in args.tower_one]
        p = a[0]
        pre = tower_precompute()
        res = tower_run(pre, p, a[1], a[2], [1] + a[3:7])
        print("outcome:", res["outcome"],
              "dead_level:", res.get("dead_level"))
        for st in res["stats"]:
            print("  w=%3d eqs=%2d new=%2d rank=%2d ker=%2d obs=%2d"
                  % (st["w"], st["eqs"], st["new"], st["rank"], st["kernel"],
                     st["obstructions"]))
        print("ntau:", res.get("ntau"), "nsub:", res.get("nsub"))
        if res["outcome"] == "SURVIVOR":
            print("live taus:", res["live_taus"])
            print("residual obstructions (level, #terms):",
                  [(lw, len(ob)) for lw, ob in res["obstructions"]])
            for lw, ob in res["obstructions"]:
                if len(ob) <= 12:
                    print("   w=%d: %s" % (lw, ob))
            print("nonzero polys sizes:",
                  {k: len(v) for k, v in res["nonzero_polys"].items()})
        return
    if args.derive:
        ok = derive()
        sys.exit(0 if ok else 1)
    if args.build:
        ok = build()
        sys.exit(0 if ok else 1)
    if args.truncate is not None:
        truncate(args.truncate)
        return
    if args.witness:
        ok = witness()
        sys.exit(0 if ok else 1)
    if args.tower_compare:
        ok = tower_compare()
        sys.exit(0 if ok else 1)
    if args.level19:
        ok = level19()
        sys.exit(0 if ok else 1)
    if args.singular_system:
        a = args.singular_system
        singular_system(a[0], int(a[1]),
                        a[2] if len(a) > 2 else None,
                        int(a[3]) if len(a) > 3 else 3900,
                        int(a[4]) if len(a) > 4 else 1800000,
                        a[5] if len(a) > 5 else "dp")
        return
    if args.peel:
        a = args.peel
        peel(int(a[0]), a[1] if len(a) > 1 else None,
             int(a[2]) if len(a) > 2 else 6600,
             int(a[3]) if len(a) > 3 else 6500000)
        return
    if args.singular:
        tree = args.singular[0]
        leaf_id = int(args.singular[1])
        p = int(args.singular[2])
        name = args.singular[3] if len(args.singular) > 3 else None
        singular_leaf(tree, leaf_id, p, name)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
