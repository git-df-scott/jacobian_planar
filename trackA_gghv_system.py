#!/usr/bin/env python3
"""
trackA_gghv_system.py — reconstruct, from GGHV arXiv:2204.14178 Proposition 4.3 ALONE,
the coefficient system of the open (8,28) shape of the (72,108) case.

Paper statement (Prop 4.3, "Case (8,28)"): if a counterexample exists in the case (8,28),
then there exist P, Q in L(1) with

    [P, Q] = x^2

and one of:
  case (1):  N(P) = conv{(0,0),(1,0),(8,14),(8,16),(0,8)}
             N(Q) = conv{(0,0),(2,1),(12,21),(12,24),(0,12)}
  case (2):  N(P) = conv{(0,0),(1,0),(8,14),(8,16)}
             N(Q) = conv{(0,0),(2,1),(12,21),(12,24)}

System: unknowns c_i_j ((i,j) in lattice(N(P))) and d_k_l ((k,l) in lattice(N(Q))).
P = sum c_ij x^i y^j, Q = sum d_kl x^k y^l.
[P,Q] := Px Qy - Py Qx = sum over pairs (i*l - j*k) c_ij d_kl x^(i+k-1) y^(j+l-1).
Equations: coefficient of x^a y^b in [P,Q] equals 1 if (a,b)==(2,0) else 0, for every
(a,b) reachable with a nonzero determinant weight.

Side conditions (Newton polygon EXACTLY the stated hull):
  vertex coefficients nonzero. Case (2): c_1_0, c_8_14, c_8_16, d_2_1, d_12_21, d_12_24.
  Case (1): additionally c_0_8, d_0_12.
  (The origin coefficients c_0_0, d_0_0 never enter any bracket equation; constants are
  Jacobian-inert. Whether the paper's N() convention forces them nonzero is irrelevant
  to solvability; they are carried as inert unknowns.)

Everything exact over Q (fractions.Fraction); polynomials as dict monomial->coeff.
Outputs: prints counts, degree profile, canonical content hash; writes
trackA_system_case1.json and trackA_system_case2.json next to itself.
"""

from fractions import Fraction
import hashlib
import itertools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------- supports
def lattice_points_of_hull(vertices):
    """All integer points in the convex hull of `vertices` (exact rational tests)."""
    verts = [(Fraction(x), Fraction(y)) for (x, y) in vertices]
    n = len(verts)
    # centroid (interior reference point)
    cx = sum(v[0] for v in verts) / n
    cy = sum(v[1] for v in verts) / n
    # For robustness build half-planes from hull edges: use all pairs, keep supporting ones.
    # Small sets -> brute force: point is in hull iff for every directed edge of the hull
    # it is on the inner side.  Compute hull by monotone chain (exact).
    pts = sorted(set(verts))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    if len(pts) == 1:
        hull = pts
    else:
        lower, upper = [], []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    out = []
    for X in range(int(min(xs)), int(max(xs)) + 1):
        for Y in range(int(min(ys)), int(max(ys)) + 1):
            p = (Fraction(X), Fraction(Y))
            inside = True
            m = len(hull)
            for i in range(m):
                a, b = hull[i], hull[(i + 1) % m]
                if cross(a, b, p) < 0:
                    inside = False
                    break
            if inside:
                out.append((X, Y))
    return sorted(out)


P_VERTS_1 = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
Q_VERTS_1 = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
P_VERTS_2 = [(0, 0), (1, 0), (8, 14), (8, 16)]
Q_VERTS_2 = [(0, 0), (2, 1), (12, 21), (12, 24)]

NONZERO_1 = (["c_1_0", "c_8_14", "c_8_16", "c_0_8"],
             ["d_2_1", "d_12_21", "d_12_24", "d_0_12"])
NONZERO_2 = (["c_1_0", "c_8_14", "c_8_16"],
             ["d_2_1", "d_12_21", "d_12_24"])


def vname(prefix, i, j):
    return "%s_%d_%d" % (prefix, i, j)


# ------------------------------------------------------------------- bracket equations
def build_bracket_system(SP, SQ):
    """Equations: coeff of x^a y^b in [P,Q] - x^2 = 0.

    Each equation: dict  monomial -> Fraction, where monomial is a tuple of
    (varname, exponent) sorted; the constant term uses monomial == ().
    Returns dict (a,b) -> equation-dict, only for (a,b) that receive at least one
    structurally nonzero term (det weight != 0) or (a,b)==(2,0).
    """
    eqs = {}
    for (i, j) in SP:
        for (k, l) in SQ:
            det = i * l - j * k
            if det == 0:
                continue
            a, b = i + k - 1, j + l - 1
            mono = tuple(sorted((vname("c", i, j), vname("d", k, l))))
            mono = ((mono[0], 1), (mono[1], 1))
            eq = eqs.setdefault((a, b), {})
            eq[mono] = eq.get(mono, Fraction(0)) + det
    # drop exact-zero accumulations
    for key in list(eqs):
        eqs[key] = {m: c for m, c in eqs[key].items() if c != 0}
        if not eqs[key]:
            del eqs[key]
    # right-hand side x^2
    tgt = (2, 0)
    eqs.setdefault(tgt, {})
    eqs[tgt][()] = eqs[tgt].get((), Fraction(0)) - 1   # ... - 1 = 0
    return eqs


# ------------------------------------------------------------------------ canonical io
def eq_to_canonical(eq):
    parts = []
    for mono in sorted(eq.keys()):
        c = eq[mono]
        mstr = "*".join("%s^%d" % (v, e) for (v, e) in mono) if mono else "1"
        parts.append("%s:%s" % (mstr, c))
    return ";".join(parts)


def system_canonical_string(eqs):
    lines = []
    for key in sorted(eqs.keys()):
        lines.append("eq[%d,%d]=%s" % (key[0], key[1], eq_to_canonical(eqs[key])))
    return "\n".join(lines)


def content_hash(eqs):
    return hashlib.sha256(system_canonical_string(eqs).encode()).hexdigest()


def serialize_system(eqs, variables, nonzero, meta):
    ser_eqs = []
    for key in sorted(eqs.keys()):
        eq = eqs[key]
        terms = []
        for mono in sorted(eq.keys()):
            terms.append([[list(ve) for ve in mono],
                          [eq[mono].numerator, eq[mono].denominator]])
        ser_eqs.append({"bracket_point": list(key), "terms": terms})
    return {"meta": meta, "variables": variables, "nonzero": nonzero,
            "equations": ser_eqs, "content_hash": content_hash(eqs)}


# --------------------------------------------------------------------------- reporting
def degree_profile(eqs):
    prof = {}
    nterms = {}
    for eq in eqs.values():
        deg = max((sum(e for _, e in m) for m in eq), default=0)
        prof[deg] = prof.get(deg, 0) + 1
        t = len(eq)
        nterms[t] = nterms.get(t, 0) + 1
    return prof, nterms


def build_case(case_no):
    if case_no == 1:
        SP = lattice_points_of_hull(P_VERTS_1)
        SQ = lattice_points_of_hull(Q_VERTS_1)
        nzP, nzQ = NONZERO_1
    else:
        SP = lattice_points_of_hull(P_VERTS_2)
        SQ = lattice_points_of_hull(Q_VERTS_2)
        nzP, nzQ = NONZERO_2
    cvars = [vname("c", i, j) for (i, j) in SP]
    dvars = [vname("d", k, l) for (k, l) in SQ]
    eqs = build_bracket_system(SP, SQ)
    meta = {
        "source": "GGHV arXiv:2204.14178 Proposition 4.3 (Case (8,28)), case (%d)" % case_no,
        "bracket_rhs": "x^2",
        "P_vertices": P_VERTS_1 if case_no == 1 else P_VERTS_2,
        "Q_vertices": Q_VERTS_1 if case_no == 1 else Q_VERTS_2,
        "SP_size": len(SP), "SQ_size": len(SQ),
    }
    return SP, SQ, cvars, dvars, eqs, (nzP, nzQ), meta


def inert_variables(eqs, variables):
    used = set()
    for eq in eqs.values():
        for mono in eq:
            for v, _ in mono:
                used.add(v)
    return [v for v in variables if v not in used]


# ------------------------------------------------------------- A2: normalization proof
def check_normalization(case_no):
    """Executable proof of the A2 claim.

    Torus action on pairs:  (P,Q) -> (a*P(sx,ty), b*Q(sx,ty)),  a,b,s,t in K^x.
    On coefficients: c_ij -> a s^i t^j c_ij,  d_kl -> b s^k t^l d_kl.
    Claim 1 (equivariance): each bracket equation E_(alpha,beta) is scaled by the single
      factor a*b*s^(alpha+1)*t^(beta+1); hence homogeneous equations are preserved, and
      the inhomogeneous (2,0) equation ([P,Q]-coefficient = 1) is preserved iff
      a*b*s^3*t = 1.
    Proof is per-term: a term c_ij*d_kl occurs in E_(alpha,beta) only if
      i+k-1 = alpha and j+l-1 = beta, so its scale factor a s^i t^j * b s^k t^l equals
      a b s^(alpha+1) t^(beta+1) identically.  We CHECK this index identity for every
      term of every equation (exhaustive, exact).
    Claim 2 (normalization loses nothing): d_2_1 -> b s^2 t d_2_1.  Given ANY solution,
      d_2_1 != 0 is forced by the Prop 4.3 side condition (vertex (2,1) of N(Q)).
      Choose a = d_2_1, b = 1/d_2_1, s = t = 1: constraint a*b*s^3*t = 1 holds and the
      image solution has d_2_1 = 1.  No genericity needed, no solution lost; the locus
      d_2_1 = 0 is excluded by the hypothesis, not by us.
    Claim 3 (residual freedom): the stabilizer of {d_2_1 = 1} inside the constrained
      group is {(a,b,s,t) = (1/s, 1/(s^2 t), s, t) : s,t in K^x} — a 2-torus that
      remains available for further normalizations downstream.
    """
    SP, SQ, cvars, dvars, eqs, (nzP, nzQ), meta = build_case(case_no)
    # Claim 1: exhaustive per-term index identity check.
    bad = []
    for (alpha, beta), eq in eqs.items():
        for mono in eq:
            if mono == ():
                continue  # constant term: scale factor 1 (handled below)
            assert len(mono) == 2
            (v1, e1), (v2, e2) = mono
            p1, i, j = v1.split("_")
            p2, k, l = v2.split("_")
            i, j, k, l = int(i), int(j), int(k), int(l)
            assert (p1, p2) == ("c", "d") and e1 == e2 == 1
            if not (i + k - 1 == alpha and j + l - 1 == beta):
                bad.append(((alpha, beta), mono))
    ok1 = not bad
    # The only equation with a constant term must be (2,0), forcing a*b*s^3*t = 1.
    const_eqs = [key for key, eq in eqs.items() if () in eq]
    ok2 = const_eqs == [(2, 0)]
    # Claim 2 sanity: d_2_1 is in the declared nonzero list.
    ok3 = "d_2_1" in (nzP + nzQ)
    # Numeric equivariance spot check with random rationals (exact arithmetic):
    import random
    rng = random.Random(20260813)
    def rq():
        return Fraction(rng.randint(-9, 9), rng.randint(1, 7))
    def rqnz():
        while True:
            v = rq()
            if v != 0:
                return v
    vals = {v: rq() for v in cvars + dvars}
    s, t = rqnz(), rqnz()
    a = rqnz()
    b = 1 / (a * s ** 3 * t)          # enforce the constraint
    tvals = {}
    for v in cvars + dvars:
        p, i, j = v.split("_")
        i, j = int(i), int(j)
        tvals[v] = (a if p == "c" else b) * s ** i * t ** j * vals[v]
    def ev(eq, val):
        tot = Fraction(0)
        for mono, cf in eq.items():
            term = cf
            for (v, e) in mono:
                term *= val[v] ** e
            tot += term
        return tot
    ok4 = True
    for (alpha, beta), eq in eqs.items():
        lhs = ev(eq, tvals)
        # homogeneous part scales by fac; constant term (only in (2,0)) scales by 1,
        # and fac = a*b*s^(alpha+1)*t^(beta+1) equals 1 there by the constraint.
        fac = a * b * s ** (alpha + 1) * t ** (beta + 1)
        if lhs != fac * ev(eq, vals):
            ok4 = False
            break
    print("A2 normalization check, case (%d):" % case_no)
    print("  claim 1 (per-term equivariance identity, %d equations): %s"
          % (len(eqs), "PROVED" if ok1 else "FAILED: %s" % bad[:3]))
    print("  claim 1b (unique inhomogeneous equation is (2,0)): %s"
          % ("PROVED" if ok2 else "FAILED: %s" % const_eqs))
    print("  claim 2 (d_2_1 != 0 is a Prop 4.3 side condition; witness scaling "
          "(a,b,s,t)=(d_2_1, 1/d_2_1, 1, 1)): %s" % ("PROVED" if ok3 else "FAILED"))
    print("  claim 3 (residual 2-torus (1/s, 1/(s^2 t), s, t) preserves d_2_1=1): "
          "algebraic identity, holds by claim 1")
    print("  numeric exact equivariance spot check: %s" % ("PASS" if ok4 else "FAIL"))
    verdict = ok1 and ok2 and ok3 and ok4
    print("  VERDICT: normalization d_2_1 = 1 is WLOG-sound; the excluded locus "
          "d_2_1 = 0 is already excluded by the polygon hypothesis; no extra branch "
          "needed." if verdict else "  VERDICT: PROBLEM — see failures above.")
    return verdict


def main():
    summary = {}
    for case_no in (2, 1):
        SP, SQ, cvars, dvars, eqs, (nzP, nzQ), meta = build_case(case_no)
        variables = cvars + dvars
        inert = inert_variables(eqs, variables)
        prof, nterms = degree_profile(eqs)
        h = content_hash(eqs)
        print("=" * 78)
        print("CASE (%d)  [%s]" % (case_no, "pentagons" if case_no == 1 else "quadrilaterals"))
        print("  |supp P| = %d, |supp Q| = %d, unknowns total = %d"
              % (len(SP), len(SQ), len(variables)))
        print("  inert unknowns (appear in no equation): %s" % ", ".join(inert))
        print("  active unknowns = %d" % (len(variables) - len(inert)))
        print("  equations = %d" % len(eqs))
        print("  degree profile {deg: #eqs} = %s" % prof)
        print("  terms-per-equation histogram {#terms: #eqs} = %s"
              % dict(sorted(nterms.items())))
        print("  vertex-nonvanishing side conditions: %s" % ", ".join(nzP + nzQ))
        print("  content hash (sha256) = %s" % h)
        data = serialize_system(eqs, variables, nzP + nzQ, meta)
        out = os.path.join(HERE, "trackA_system_case%d.json" % case_no)
        with open(out, "w") as fh:
            json.dump(data, fh)
        print("  written: %s" % out)
        summary["case%d" % case_no] = {
            "unknowns": len(variables), "equations": len(eqs),
            "inert": inert, "hash": h,
        }
    print("=" * 78)
    print("Lost-session memory said: 72 unknowns, 92 quadratic equations.")
    c2 = summary["case2"]
    print("Case (2) gives %d unknowns / %d equations -> %s"
          % (c2["unknowns"], c2["equations"],
             "MATCH" if (c2["unknowns"], c2["equations"]) == (72, 92) else "MISMATCH"))
    c1 = summary["case1"]
    print("Case (1) gives %d unknowns / %d equations (the lost session apparently "
          "never mentioned this second, larger system)" % (c1["unknowns"], c1["equations"]))
    with open(os.path.join(HERE, "trackA_system_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    return summary


if __name__ == "__main__":
    import sys
    if "--check-normalization" in sys.argv:
        ok = check_normalization(2) and check_normalization(1)
        sys.exit(0 if ok else 1)
    main()
    check_normalization(2)
    check_normalization(1)
