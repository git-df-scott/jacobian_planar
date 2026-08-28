"""night14 -- U-test: is 1 in the ideal (P_x, P_y)?

Verdict ring is Q (char 0).  A mod-p shadow at p = 999983 is recorded first as
a fast prefilter: if 1 is in the ideal mod p then it is in the ideal over Q
(the reduction of a char-0 certificate specializes), so a mod-p PASS is a
proof of the char-0 PASS; a mod-p FAIL is only evidence and the char-0 test is
run regardless.  Both are computed by Singular (groebner over the stated ring)
and the char-0 answer is the recorded verdict.

1 in (P_x, P_y)  <=>  P_x, P_y have no common zero over C  (Nullstellensatz)
                 <=>  the critical locus of P is empty
                 <=>  every fibre of P is smooth.
"""

import subprocess
import tempfile
import os
import time
import poly14 as P14

PRIME = 999983
SINGULAR = "Singular"


def _script(P, char):
    px = P14.to_singular(P14.dx(P))
    py = P14.to_singular(P14.dy(P))
    return """
ring r = %s,(x,y),dp;
poly px = %s;
poly py = %s;
ideal I = px, py;
ideal G = groebner(I);
int u = (deg(G[1]) == 0 && size(G) == 1) || (G[1] == 1);
if (u) { "UNIMODULAR"; } else { "NOT_UNIMODULAR"; }
quit;
""" % (char, px, py)


def _run(P, char, timeout=120):
    fd, path = tempfile.mkstemp(suffix=".sing", dir=os.environ.get("TMPDIR", "/tmp"))
    with os.fdopen(fd, "w") as fh:
        fh.write(_script(P, char))
    try:
        out = subprocess.run([SINGULAR, "-q", "--no-warn", path],
                             capture_output=True, text=True, timeout=timeout)
        txt = out.stdout
        if "UNIMODULAR" in txt and "NOT_UNIMODULAR" not in txt:
            return "PASS"
        if "NOT_UNIMODULAR" in txt:
            return "FAIL"
        return "ERROR:" + (txt.strip()[:120] or out.stderr.strip()[:120])
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    finally:
        os.unlink(path)


def utest(P, timeout=120):
    """Returns dict with the mod-p shadow, the char-0 verdict, and timings."""
    t0 = time.time()
    shadow = _run(P, str(PRIME), timeout)
    t1 = time.time()
    q = _run(P, "0", timeout)
    t2 = time.time()
    return {"u_modp": shadow, "u_q": q,
            "t_modp": round(t1 - t0, 3), "t_q": round(t2 - t1, 3)}


CONTROLS = [
    ("x",         {(1, 0): 1},            "PASS"),
    ("x + x^2*y", {(1, 0): 1, (2, 1): 1}, "PASS"),
    ("x + y^2",   {(1, 0): 1, (0, 2): 1}, "PASS"),
    ("x*y",       {(1, 1): 1},            "FAIL"),
    ("x^2 + y^2", {(2, 0): 1, (0, 2): 1}, "FAIL"),
    ("x^2*y",     {(2, 1): 1},            "FAIL"),
    ("y + x^3",   {(0, 1): 1, (3, 0): 1}, "PASS"),
]

if __name__ == "__main__":
    ok = True
    for lab, p, exp in CONTROLS:
        r = utest(P14.clean(p))
        good = r["u_q"] == exp
        ok &= good
        print("%-14s modp=%-6s Q=%-6s expected %-5s %s  (%.2fs/%.2fs)"
              % (lab, r["u_modp"], r["u_q"], exp, "ok" if good else "MISMATCH",
                 r["t_modp"], r["t_q"]))
    print("ALL MATCH" if ok else "SOME MISMATCH")
