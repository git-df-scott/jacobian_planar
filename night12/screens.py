"""night12 v1 -- the P-screens, run before any mate matrix is built.

S1  unimodular gradient: is 1 in the ideal (P_x, P_y) over Q?  Decided by a
    Groebner basis (Singular, ring 0,(x,y),dp).  A common zero of P_x and P_y
    kills every mate (the Keller equation evaluated there reads 0 = 1), so a
    P failing S1 is rejected.  Cheap pre-check first: if P_x and P_y both have
    zero constant term the origin is a common zero and S1 fails immediately.

S2  composition screen: reject P = h(R) with deg h > 1.  Cheap form -- such a
    P has P_x = h'(R) R_x and P_y = h'(R) R_y, so gcd(P_x, P_y) is nonconstant.
    gcd(P_x,P_y) = 1 therefore rejects every proper composition, and it is
    implied by S1 (a root of h' would contradict S1), so it is run first as
    the cheap check.

S3  diagnostics recorded per P (selection bias, not a gate):
      places_at_infinity : number of distinct roots of the leading form as a
                           binary form (each distinct root of P_n is a point
                           of the curve at infinity)
      genus_newton       : interior lattice points of the Newton polygon of P
                           (Pick's theorem).  For a nondegenerate generic
                           fibre this equals the geometric genus (Khovanskii);
                           it is recorded with that nondegeneracy caveat.
    Theorem on file: a P with a rational irreducible generic fibre that has a
    mate is a coordinate.  So the selection bias is toward genus_newton > 0 or
    places_at_infinity > 1; both numbers are recorded for every P.
"""

import os
import subprocess
import tempfile
from fractions import Fraction
import matekit as M

SINGULAR = "/usr/bin/Singular"


def poly_str(P):
    ts = []
    for (i, j), c in sorted(P.items()):
        ts.append("(%d)*x^%d*y^%d" % (c, i, j))
    return "+".join(ts) if ts else "0"


def _singular(script, timeout):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as f:
        f.write(script)
        path = f.name
    try:
        r = subprocess.run([SINGULAR, "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return None, -1
    finally:
        os.unlink(path)


def S2_gcd(P, timeout=120):
    """returns (verdict, detail).  verdict in {'pass','reject','timeout'}."""
    s = """ring r = 0,(x,y),dp;
poly P = %s;
poly g = gcd(diff(P,x),diff(P,y));
if (deg(g) == 0) { "GCD_UNIT"; } else { "GCD_NONUNIT"; string(deg(g)); }
quit;
""" % poly_str(P)
    out, rc = _singular(s, timeout)
    if out is None:
        return "timeout", "singular_timeout"
    if "GCD_UNIT" in out:
        return "pass", "gcd(P_x,P_y) is a unit"
    return "reject", "gcd(P_x,P_y) nonconstant: " + out.replace("\n", " ")


def S1_unimodular(P, timeout=600):
    px, py = M.dx(P), M.dy(P)
    if px.get((0, 0), 0) == 0 and py.get((0, 0), 0) == 0:
        return "reject", "origin is a common zero of (P_x,P_y)"
    s = """ring r = 0,(x,y),dp;
poly P = %s;
ideal I = diff(P,x),diff(P,y);
ideal G = std(I);
if (dim(G) == -1) { "UNIMODULAR"; } else { "HAS_COMMON_ZERO"; string(dim(G)); }
quit;
""" % poly_str(P)
    out, rc = _singular(s, timeout)
    if out is None:
        return "timeout", "singular_timeout"
    if "UNIMODULAR" in out:
        return "pass", "1 in (P_x,P_y) over Q"
    return "reject", "common zero of (P_x,P_y): " + out.replace("\n", " ")


def _distinct_roots_binary(F, n):
    """number of distinct roots of the binary form F of degree n, over Q-bar."""
    import sympy
    t = sympy.symbols("t")
    uni = sum(sympy.Integer(c) * t ** i for (i, j), c in F.items())
    p = sympy.Poly(uni, t)
    if p.is_zero:
        return 0
    g = sympy.gcd(p, p.diff(t))
    k = sympy.degree(sympy.simplify(sympy.div(p, g)[0]), t)
    at_inf = 1 if p.degree() < n else 0
    return int(k) + at_inf


def S3_diagnostics(P):
    n = M.pdeg(P)
    lead = {k: v for k, v in P.items() if k[0] + k[1] == n}
    places = _distinct_roots_binary(lead, n)
    pts = sorted(set(list(P.keys()) + [(0, 0)]))
    hull = M._hull(pts)
    # Pick: I = A - B/2 + 1
    if len(hull) < 3:
        area2, bnd = 0, 0
    else:
        area2 = 0
        for i in range(len(hull)):
            a, b = hull[i], hull[(i + 1) % len(hull)]
            area2 += a[0] * b[1] - a[1] * b[0]
        area2 = abs(area2)
        from math import gcd
        bnd = 0
        for i in range(len(hull)):
            a, b = hull[i], hull[(i + 1) % len(hull)]
            bnd += gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
    interior = (area2 - bnd) // 2 + 1 if area2 else 0
    return {"places_at_infinity": int(places),
            "genus_newton": int(max(interior, 0)),
            "lead_terms": len(lead)}


def screen(P, t2=120, t1=600):
    rec = {}
    v2, d2 = S2_gcd(P, t2)
    rec["S2"] = v2
    rec["S2_detail"] = d2
    if v2 == "reject":
        rec["S1"] = "not_run"
        rec["S1_detail"] = "short-circuited by S2"
        rec.update(S3_diagnostics(P))
        rec["passed"] = False
        return rec
    v1, d1 = S1_unimodular(P, t1)
    rec["S1"] = v1
    rec["S1_detail"] = d1
    rec.update(S3_diagnostics(P))
    rec["passed"] = (v1 == "pass" and v2 == "pass")
    return rec


if __name__ == "__main__":
    import carriers, time
    tests = [("x", {(1, 0): 1}),
             ("x + y^126", {(1, 0): 1, (0, 126): 1}),
             ("x^126+y^127+x^2y^2 (neg control)",
              {(126, 0): 1, (0, 127): 1, (2, 2): 1}),
             ("x*y", {(1, 1): 1}),
             ("(x+y^2)^2 + x  [composition-ish]",
              M.padd(M.ppow({(1, 0): 1, (0, 2): 1}, 2), {(1, 0): 1}))]
    for nm, P in tests:
        t0 = time.time()
        print("%-38s %s  (%.1fs)" % (nm, screen(P, 60, 120), time.time() - t0))
    it = carriers.build_M1(1)[0]
    t0 = time.time()
    print("M1 sample %s |supp P|=%d -> %s (%.1fs)"
          % (it["profile"], len(it["P"]), screen(it["P"], 120, 600), time.time() - t0))
