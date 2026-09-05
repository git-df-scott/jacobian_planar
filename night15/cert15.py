"""night15 -- certificates carried by every P that enters the screen.

  U  : gradient unimodularity, as an EXACT Bezout identity
           A(x,y) P_x + B(x,y) P_y = 1   in Q[x,y]
       A and B are produced by Singular's `lift` and then re-expanded in
       exact rational arithmetic here; the record keeps the number of
       residual terms, which must be 0.  A Bezout identity is a proof that
       (P_x, P_y) = (1), i.e. that P_x and P_y have no common zero anywhere
       over the algebraic closure -- so every fibre of P is smooth.

  SY : Shpilrain-Yu gradient-row reduction (sy15), verdict NON_COORDINATE.

  FIB: an independent non-coordinate witness on the fibres (fib15): either a
       fibre that factors into >= 2 nonconstant factors (a U-passing P has
       smooth fibres, so a reducible fibre is a DISCONNECTED fibre, which the
       affine line is not), or an irreducible fibre of geometric genus > 0.
"""

import os
import subprocess
import tempfile
from fractions import Fraction as F

import pk15 as P14

SINGULAR = "Singular"


def _sing(code, timeout=180):
    fd, path = tempfile.mkstemp(suffix=".sing", dir=os.environ.get("TMPDIR", "/tmp"))
    with os.fdopen(fd, "w") as fh:
        fh.write(code)
    try:
        out = subprocess.run([SINGULAR, "-q", "--no-warn", path],
                             capture_output=True, text=True, timeout=timeout)
        return out.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    finally:
        os.unlink(path)


def _parse_poly(s):
    """parse a Singular poly string over Q in x, y into a dict."""
    s = s.replace(" ", "").replace("\n", "")
    if s in ("", "0"):
        return {}
    out = {}
    i = 0
    terms = []
    cur = ""
    for ch in s:
        if ch in "+-" and cur:
            terms.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        terms.append(cur)
    for t in terms:
        sign = F(1)
        while t and t[0] in "+-":
            if t[0] == "-":
                sign = -sign
            t = t[1:]
        if not t:
            continue
        import re
        num, den = F(1), F(1)
        ex, ey = 0, 0
        pos = 0
        while pos < len(t):
            if t[pos] == "*":
                pos += 1
                continue
            m = re.match(r"(\d+)/(\d+)", t[pos:])
            if m:
                num *= int(m.group(1)); den *= int(m.group(2)); pos += m.end()
                continue
            m = re.match(r"\d+", t[pos:])
            if m:
                num *= int(m.group(0)); pos += m.end()
                continue
            m = re.match(r"([xy])(\^?(\d+))?", t[pos:])
            if m:
                e = int(m.group(3)) if m.group(3) else 1
                if m.group(1) == "x":
                    ex += e
                else:
                    ey += e
                pos += m.end()
                continue
            raise ValueError("token at %r in %r" % (t[pos:], s))
        c = sign * F(num, den)
        out[(ex, ey)] = out.get((ex, ey), F(0)) + c
    return P14.clean(out)


def bezout_unimodular(P, timeout=240):
    """exact A P_x + B P_y = 1, or a report that 1 is not in the ideal."""
    Px, Py = P14.dx(P), P14.dy(P)
    if not Px and not Py:
        return {"U": False, "reason": "P constant"}
    code = """
ring r = 0,(x,y),dp;
ideal I = %s, %s;
ideal G = std(I);
poly nf = reduce(1, G);
if (nf != 0) { "NOTUNIT"; quit; }
matrix M = lift(I, ideal(1));
"A:", M[1,1];
"B:", M[2,1];
quit;
""" % (P14.to_singular(Px), P14.to_singular(Py))
    out = _sing(code, timeout)
    if out == "TIMEOUT":
        return {"U": None, "reason": "singular timeout"}
    if "NOTUNIT" in out:
        return {"U": False, "reason": "1 not in (P_x, P_y): critical locus nonempty"}
    A = B = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("A:"):
            A = _parse_poly(line[2:])
        elif line.startswith("B:"):
            B = _parse_poly(line[2:])
    if A is None or B is None:
        return {"U": None, "reason": "singular parse failure", "raw": out[:400]}
    # Singular clears denominators of the generators; rescale by the same
    # factor that to_singular applied, then verify exactly over Q.
    from math import gcd

    def scale_of(Q):
        den = 1
        for c in Q.values():
            den = den * c.denominator // gcd(den, c.denominator)
        return F(den)

    sx, sy = scale_of(Px), scale_of(Py)
    A = P14.pscal(sx, A)
    B = P14.pscal(sy, B)
    res = P14.psub(P14.padd(P14.pmul(A, Px), P14.pmul(B, Py)), {(0, 0): F(1)})
    return {"U": len(res) == 0, "residual_terms": len(res),
            "A_terms": len(A), "B_terms": len(B),
            "deg_A": P14.tdeg(A), "deg_B": P14.tdeg(B),
            "reason": "exact Bezout identity verified over Q" if not res
                      else "residual nonzero"}
