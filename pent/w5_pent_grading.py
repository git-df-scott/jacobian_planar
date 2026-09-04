"""
Does the pentagon system carry the grading that decided case (2)?

In case (2) the weight w = j - 2i on the coefficient c_i_j / d_i_j split the
92-equation system into blocks, one of which (w = -4) was self-contained in two
letters and decided the whole chart in under a second -- after a direct Groebner
run on the full system had been OOM-killed at 10 GB.  The pentagon system
(wave1/pent_L23.ms, 66 generators in 61 unknowns) OOMs the same way.  If the
same kind of grading is present, the same reduction is available.

This asks the question exactly, with no guessing: find EVERY linear weight
assignment mu(p_i_j) = alpha*i + beta*j + gamma under which every generator is
weighted-homogeneous, by solving the linear conditions "all monomials of a
generator have equal weight" over Q.  Then report how the generators
distribute over the resulting grading -- a block that involves few variables is
the lever; no nontrivial grading is an equally definite answer.

CONTROLS
  W1 POSITIVE: the solver finds the KNOWN grading of a planted homogeneous
     system;
  W2 NEGATIVE: adding one inhomogeneous generator to that planted system
     destroys it;
  W3 POSITIVE: the weights reported for the real system really do make every
     generator homogeneous -- re-checked monomial by monomial, not inferred
     from the solve.
"""
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def read_ms(path):
    lines = [l.strip().rstrip(",") for l in open(path) if l.strip()]
    return lines[0].split(","), lines[2:]


def monomials(gen):
    """[(varname -> exponent, )] for each term of a generator."""
    out = []
    for term in re.split(r"\+", gen.replace("-", "+-")):
        term = term.strip()
        if not term:
            continue
        d = {}
        for f in term.split("*"):
            f = f.strip()
            m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", f)
            if m:
                d[m.group(1)] = d.get(m.group(1), 0) + int(m.group(2) or 1)
        out.append(d)
    return out


def rref(rows, ncols):
    rows = [r[:] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        k = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if k is None:
            continue
        rows[r], rows[k] = rows[k], rows[r]
        inv = Fraction(1, 1) / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], piv


def nullspace(rows, ncols):
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fcol in free:
        v = [Fraction(0)] * ncols
        v[fcol] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][fcol]
        basis.append(v)
    return basis


def gradings(vars_, gens, param=lambda v: None):
    """Nullspace of 'every generator is homogeneous' in the ansatz
    mu(p_i_j) = alpha*i + beta*j + gamma.  Columns: alpha, beta, gamma."""
    ij = {}
    for v in vars_:
        m = re.fullmatch(r"[a-z]+_(\d+)_(\d+)", v)
        ij[v] = (int(m.group(1)), int(m.group(2))) if m else None
    rows = []
    for g in gens:
        ms = [m for m in monomials(g) if m]
        if len(ms) < 2:
            continue
        def wt(mon):
            a = b = c = 0
            for v, e in mon.items():
                if ij.get(v) is None:
                    return None
                a += e * ij[v][0]
                b += e * ij[v][1]
                c += e
            return [Fraction(a), Fraction(b), Fraction(c)]
        w0 = wt(ms[0])
        if w0 is None:
            continue
        for mon in ms[1:]:
            w = wt(mon)
            if w is None:
                continue
            rows.append([x - y for x, y in zip(w, w0)])
    return nullspace(rows, 3), rows


def homogeneous(vars_, gens, weight):
    """Is every generator homogeneous for this weight?  Returns the degrees."""
    degs = []
    for g in gens:
        ms = [m for m in monomials(g) if m]
        ws = set()
        for mon in ms:
            s = Fraction(0)
            for v, e in mon.items():
                if v not in weight:
                    return None
                s += e * weight[v]
            ws.add(s)
        if len(ws) > 1:
            return None
        degs.append(next(iter(ws)) if ws else None)
    return degs


def main():
    print("=" * 78)
    print("weighted-homogeneous gradings of the pentagon system")
    print("=" * 78)

    pv = ["p_1_0", "p_1_1", "p_2_0"]
    pg = ["p_1_0*p_1_1 + p_2_0*p_1_1", "p_1_0^2*p_2_0 + p_2_0^2*p_1_0"]
    nb, _ = gradings(pv, pg)
    check("W1 POSITIVE: the solver finds a grading of a planted homogeneous "
          "system", len(nb) >= 1, f"{len(nb)}-dimensional space of weights")

    nb2, _ = gradings(pv, pg + ["p_1_0 + p_1_0*p_1_1*p_2_0"])
    check("W2 NEGATIVE: one inhomogeneous generator shrinks the space",
          len(nb2) < len(nb), f"{len(nb)} -> {len(nb2)}")

    path = os.path.join(HERE, "..", "wave1", "pent_L23.ms")
    vars_, gens = read_ms(path)
    print(f"    {len(gens)} generators in {len(vars_)} variables")
    basis, rows = gradings(vars_, gens)
    print(f"    {len(rows)} homogeneity conditions on (alpha, beta, gamma); "
          f"solution space dimension {len(basis)}")
    for b in basis:
        print(f"      weight mu(p_i_j) = {b[0]}*i + {b[1]}*j + {b[2]}")

    verified, blocks = [], {}
    for b in basis:
        w = {}
        for v in vars_:
            m = re.fullmatch(r"[a-z]+_(\d+)_(\d+)", v)
            w[v] = (b[0] * int(m.group(1)) + b[1] * int(m.group(2)) + b[2]
                    if m else None)
        if any(x is None for x in w.values()):
            continue
        degs = homogeneous(vars_, gens, w)
        if degs is not None:
            verified.append([str(x) for x in b])
            d = {}
            for g, deg in zip(gens, degs):
                d.setdefault(str(deg), []).append(
                    sorted({v for mon in monomials(g) for v in mon
                            if v in w}))
            blocks[str(b)] = {k: {"generators": len(v),
                                  "variables": len(set().union(*v)) if v else 0}
                              for k, v in d.items()}
    check("W3 POSITIVE: every weight the solver returns really does make every "
          "generator homogeneous, re-checked monomial by monomial",
          len(verified) == len(basis),
          f"{len(verified)} of {len(basis)} verified")

    for bk, d in blocks.items():
        print(f"    grading {bk}: {len(d)} weight blocks")
        for k in sorted(d, key=lambda s: Fraction(s)):
            print(f"      degree {k}: {d[k]['generators']} generators, "
                  f"{d[k]['variables']} variables")

    json.dump({"n_generators": len(gens), "n_variables": len(vars_),
               "grading_space_dimension": len(basis),
               "weights": [[str(x) for x in b] for b in basis],
               "verified_weights": verified, "blocks": blocks,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "pent_grading.json"), "w"), indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
