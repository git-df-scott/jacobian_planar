"""night14 -- FIB-screen: an independent, non-SY measurement of the fibres.

Logic recorded with the instrument:

* A U-passing P has empty critical locus, so EVERY fibre {P = lam} is smooth.
  Two distinct components of a plane curve meet in a singular point of that
  curve, so for a U-passing P a reducible fibre is a DISCONNECTED fibre.
* A coordinate has every fibre isomorphic to the affine line A^1, which is
  connected, irreducible, and of geometric genus 0.

Hence, for a U-passing P, either of the two observations below is by itself a
proof that P is not a coordinate, independent of the SY instrument:

    (R) some fibre P - lam factors into 2 or more nonconstant factors over Q;
    (G) some fibre P - lam is irreducible with geometric genus > 0.

Instrument: Singular `factorize` (char 0) and `genus` from normal.lib.
"""

import subprocess
import tempfile
import os
import time
import poly14 as P14

SINGULAR = "Singular"


def _sing(code, timeout=120):
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


def fibre(P, lam=0, timeout=120):
    """Returns dict: n_factors of P - lam over Q, and the geometric genus of
    the fibre when it is irreducible."""
    f = P14.padd(P, {(0, 0): -lam})
    if not f:
        return {"lam": lam, "nfac": 0, "genus": None, "note": "zero"}
    body = P14.to_singular(f)
    code = """
LIB "normal.lib";
ring r = 0,(x,y),dp;
poly f = %s;
list L = factorize(f, 2);
int n = 0; int i;
for (i = 1; i <= size(L[1]); i++) { if (deg(L[1][i]) > 0) { n = n + L[2][i]; } }
"NFAC:", n;
if (n == 1) { "GENUS:", genus(f); }
quit;
""" % body
    t0 = time.time()
    out = _sing(code, timeout)
    dt = round(time.time() - t0, 3)
    if out == "TIMEOUT":
        return {"lam": lam, "nfac": None, "genus": None, "note": "timeout", "t": dt}
    nfac, gen = None, None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("NFAC:"):
            try:
                nfac = int(line.split()[-1])
            except ValueError:
                pass
        if line.startswith("GENUS:"):
            try:
                gen = int(line.split()[-1])
            except ValueError:
                pass
    return {"lam": lam, "nfac": nfac, "genus": gen, "note": "", "t": dt}


def screen(P, lams=(0, 1, -1), timeout=120):
    """Runs the FIB-screen on a few fibres; reports the independent verdict."""
    res = [fibre(P, l, timeout) for l in lams]
    reducible = [r for r in res if r["nfac"] is not None and r["nfac"] >= 2]
    positive = [r for r in res if r["genus"] is not None and r["genus"] > 0]
    if reducible:
        v = "NON_COORDINATE_BY_R"
    elif positive:
        v = "NON_COORDINATE_BY_G"
    else:
        v = "INCONCLUSIVE"
    return v, res


if __name__ == "__main__":
    tests = [("x + x^2*y", {(1, 0): 1, (2, 1): 1}),
             ("x", {(1, 0): 1}),
             ("x + y^2", {(1, 0): 1, (0, 2): 1}),
             ("y + x*y^2", {(0, 1): 1, (1, 2): 1})]
    for lab, p in tests:
        v, res = screen(P14.clean(p))
        print("%-12s %-22s %s" % (lab, v, [(r["lam"], r["nfac"], r["genus"]) for r in res]))
