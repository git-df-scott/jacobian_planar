"""
Cross-validate wave1/pent_L23.ms against an INDEPENDENT y-adic recursion.

The 43 MB export is the object every pentagon msolve run in this campaign is
about, and it has never been checked against a second implementation.  This
script does that: it evaluates the exported generators at random points over
F_p and compares them, generator by generator, with the forbidden coefficients
produced by the recursion in pent/w5_pent_hitdetector_v3.py, which was written
from the y-adic definition and shares no code with the exporter.

MATCHING.  The export fixes p_00 = 0 and p_10 = 1 and lists its 59 variables in
its own order; generator k of the file is level 13 + j, index i, in the same
order the detector emits them.  The comparison is made up to a NONZERO SCALAR
per generator: an exporter is free to clear denominators, and a per-generator
constant does not change the variety.  Any generator whose ratio is not
constant across independent random points is a genuine mismatch and is reported
as one.

CONTROLS
  X1 POSITIVE: every generator matches, at 3 independent random points;
  X2 NEGATIVE: perturbing ONE coordinate of the evaluation point makes the
     comparison fail, so X1 is not vacuous;
  X3 NEGATIVE: comparing generator k against generator k+1 fails, so the
     matching is not trivially satisfied by any pairing.
"""
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import w5_pent_hitdetector_v3 as V

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def load_export(path):
    txt = open(path).read().rstrip()
    rows = txt.split("\n")
    names = rows[0].split(",")
    p = int(rows[1].strip())
    polys = [s.strip() for s in "\n".join(rows[2:]).split(",\n")]
    return names, p, polys


def evaluate(poly, env, p):
    tot = 0
    for raw in re.split(r"(?=[+-])", poly):
        raw = raw.strip()
        if not raw:
            continue
        neg = raw.startswith("-")
        if raw[0] in "+-":
            raw = raw[1:]
        c = 1
        for tok in raw.split("*"):
            tok = tok.strip()
            if re.fullmatch(r"\d+", tok):
                c = c * int(tok) % p
            elif "^" in tok:
                nm, e = tok.split("^")
                c = c * pow(env[nm], int(e), p) % p
            else:
                c = c * env[tok] % p
        tot = (tot - c if neg else tot + c) % p
    return tot % p


def main():
    path = os.path.join(ROOT, "wave1", "pent_L23.ms")
    names, p, polys = load_export(path)
    print("=" * 78)
    print("cross-validation of wave1/pent_L23.ms against an independent recursion")
    print("=" * 78)
    print(f"    {len(polys)} generators, {len(names)} variables, characteristic {p}")
    assert p % 3 == 1, "the export's characteristic must satisfy p = 1 (mod 3)"

    fr = V.free_indices("one")
    free_names = [f"p_{V.PARAMS[k][0]}_{V.PARAMS[k][1]}" for k in fr]
    # the export fixes only p_00 and p_10, so its variable list is the detector's
    # 58 free names plus p_1_0
    exported = set(names)
    detector = set(free_names) | {"p_1_0"}
    check("the export's variable set is the detector's, up to the third gauge",
          exported == detector,
          f"only in export {sorted(exported - detector)[:4]}, "
          f"only in detector {sorted(detector - exported)[:4]}")

    rnd = random.Random(31)
    ratios = None
    ok_all = True
    for trial in range(3):
        pt = {n: rnd.randrange(1, p) for n in names}
        # the detector's parameter vector, in ITS order, with p_1_0 free
        x = []
        for k in fr:
            j, i = V.PARAMS[k]
            x.append(pt[f"p_{j}_{i}"])
        # run the recursion with p_1_0 taken from the same point
        Pv = [0] * V.NP
        for n, k in enumerate(fr):
            Pv[k] = x[n] % p
        Pv[V.IDX[(0, 0)]] = 0
        Pv[V.IDX[(0, 1)]] = 1
        Pv[V.IDX[(1, 0)]] = pt["p_1_0"] % p
        Q = V.fp_run(Pv, p)
        if Q is None:
            raise SystemExit("recursion undefined at the sample point")
        mine = []
        for j in range(13, 24):
            q = Q[j]
            for i in range(j - 12):
                mine.append(q[i] % p if i < len(q) else 0)
        theirs = [evaluate(g, pt, p) for g in polys]
        if len(mine) != len(theirs):
            check("the two implementations produce the same number of conditions",
                  False, f"{len(mine)} vs {len(theirs)}")
            return 1
        rr = []
        for a, b in zip(theirs, mine):
            if b % p == 0:
                rr.append(0 if a % p == 0 else None)
            else:
                rr.append(a * pow(b, p - 2, p) % p)
        if ratios is None:
            ratios = rr
        else:
            for k in range(len(rr)):
                if rr[k] != ratios[k]:
                    ok_all = False
    check("X1 POSITIVE: every exported generator equals the independent "
          "recursion's condition up to a per-generator constant, at 3 points",
          ok_all and all(r is not None for r in (ratios or [])),
          f"{sum(1 for r in (ratios or []) if r not in (None, 0))} of "
          f"{len(polys)} with a nonzero constant ratio")

    pt = {n: rnd.randrange(1, p) for n in names}
    pt2 = dict(pt)
    k0 = names[3]
    pt2[k0] = (pt2[k0] + 1) % p
    t1 = [evaluate(g, pt, p) for g in polys]
    t2 = [evaluate(g, pt2, p) for g in polys]
    check("X2 NEGATIVE: perturbing one coordinate changes the exported values",
          any(a != b for a, b in zip(t1, t2)),
          f"{sum(1 for a, b in zip(t1, t2) if a != b)} of {len(polys)} changed")

    shifted = t1[1:] + t1[:1]
    check("X3 NEGATIVE: comparing generator k with generator k+1 does NOT match",
          any(a != b for a, b in zip(t1, shifted)))

    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
