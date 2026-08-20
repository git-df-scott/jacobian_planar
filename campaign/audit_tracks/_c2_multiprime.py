"""Re-decide case (2) at fresh primes, from a freshly computed RUR.

A single prime cannot certify a characteristic-0 statement.  This runs the
whole case-(2) chain at primes other than 65521, starting from the RUR that
_c2_rur.py computes at that prime (so nothing is inherited from the original
hard-coded table -- not even g_2 = 1, which was a derived fact at 65521 and is
read off the RUR here instead).

For each irreducible factor m of the degree-35 eliminant, K = F_q[th]/(m) and
the chain runs exactly as in _c2_branch.py.  Degree-1 factors give F_q-rational
branch points, where no field extension is needed at all.
"""
import sys, re, random, os
import numpy as np
import trackB1_case2_extend as M
import trackB1_case2_final as FN
import _w0 as W
import _c2_branch as BR
from _w0np import rref_mod_p

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")


# ------------------------------------------------------ Singular poly parser
def parse_univ(s, q):
    """Singular univariate polynomial in g(12) -> {exponent: coefficient}."""
    s = s.replace(" ", "").replace("g(12)", "T")
    out = {}
    for sign, body in re.findall(r"([+-]?)([^+-]+)", s):
        if not body:
            continue
        sg = -1 if sign == "-" else 1
        mexp = re.search(r"T\^(\d+)", body)
        if mexp:
            e = int(mexp.group(1))
            body = body[:mexp.start()].rstrip("*")
        elif "T" in body:
            e = 1
            body = body.replace("T", "").rstrip("*")
        else:
            e = 0
        c = int(body) if body not in ("", "+", "-") else 1
        out[e] = (out.get(e, 0) + sg * c) % q
    return {e: c for e, c in out.items() if c}


def load_rur(q):
    txt = open(os.path.join(SCRATCH, f"c2rur_{q}.txt")).read()
    facs, rur = [], {}
    for line in txt.splitlines():
        if line.startswith("FACTOR "):
            d = parse_univ(line[7:], q)
            deg = max(d)
            lead = d[deg]
            inv = pow(lead, q - 2, q)
            facs.append([(d.get(i, 0) * inv) % q for i in range(deg)])
        elif line.startswith("VAR "):
            _, nm, rest = line.split(" ", 2)
            rur[nm] = parse_univ(rest, q)
    return facs, rur


# ------------------------------------------------------------- field helpers
def ktheta(mod):
    if M.DEG == 1:
        return [(-mod[0]) % M.p]
    e = M.kzero()
    e[1] = 1
    return e


def tpow(e, th):
    r = M.kone()
    for _ in range(e):
        r = M.kmul(r, th)
    return r


def build_CG(rur, th):
    C = [M.kzero()] * 9
    C[1] = M.kone()
    C[8] = M.kone()
    for i in range(2, 8):
        acc = M.kzero()
        for ex, cf in rur[f"c{i}"].items():
            acc = M.kadd(acc, M.kscal(tpow(ex, th), cf))
        C[i] = acc
    G = [M.kzero()] * 13
    for i in range(2, 12):
        acc = M.kzero()
        for ex, cf in rur[f"g{i}"].items():
            acc = M.kadd(acc, M.kscal(tpow(ex, th), cf))
        G[i] = acc
    G[12] = th
    return C, G


def sing_ring(q, mod):
    if len(mod) == 1:
        return [f"ring R = {q}, (b(1..3), al(1..3)), dp;"]
    ts = []
    for i, c in enumerate(mod):
        if c % q:
            ts.append(f"{c % q}" if i == 0 else
                      (f"{c % q}*a" if i == 1 else f"{c % q}*a^{i}"))
    mp = f"a^{len(mod)}" + ("+" + "+".join(ts) if ts else "")
    return [f"ring R = ({q}, a), (b(1..3), al(1..3)), dp;",
            f"minpoly = {mp};"]


def run_branch(q, mod, rur, idx, seed=23):
    M.p = q
    M.set_modulus(mod)
    BR.p = q
    th = ktheta(mod)
    C, G = build_CG(rur, th)
    edge = M.kpadd(M.kpadd(M.kpscal(M.kpmul(C, M.kpder(G)), 2),
                           M.kpscal(M.kpmul(M.kpder(C), G), -3)),
                   [M.kzero(), M.kzero(), M.ksub(M.kzero(), M.kone())])
    if not all(M.kis0(c) for c in edge):
        print(f"  branch {idx} (deg {M.DEG}): EDGE EQUATION FAILS -- bad parse")
        return None
    BF0, BFb = M.ksolve(*M.eq_w3_matrix(C, G))
    Mx, _ = M.eq_w2_system(C, G, *M.split_BF(BF0))
    _, Kb = M.ksolve(Mx, [M.kzero()] * len(Mx))
    rng = random.Random(seed + idx)
    w1 = BR.interp("(w=-1)", FN.MONOS, BR.w1_resid, C, G, BF0, BFb, Kb, rng)
    w0 = BR.interp("(w= 0)", W.MON, W.w0_resid, C, G, BF0, BFb, Kb, rng)
    g1, g0 = BR.to_sing(w1, FN.MONOS), BR.to_sing(w0, W.MON)
    L = sing_ring(q, mod) + [
        'LIB "primdec.lib";',
        "ideal I = " + ",\n".join(g1 + g0) + ";",
        "ideal Gb = std(I);",
        'if (size(Gb)==1 && Gb[1]==1) { "VERDICT: EMPTY"; }',
        'else { "VERDICT: dim = " + string(dim(Gb));',
        '  list pd = minAssGTZ(I); "components: " + string(size(pd));',
        '  int i; for (i=1;i<=size(pd);i++) {',
        '    "  comp "+string(i)+": dim "+string(dim(std(pd[i]))); pd[i]; } }',
        "quit;"]
    fn = os.path.join(SCRATCH, f"c2mp_{q}_{idx}.sing")
    open(fn, "w").write("\n".join(L))
    print(f"  branch {idx} (deg {M.DEG}): edge OK, (w=-3) dim {len(BFb)}, "
          f"(w=-2) ker {len(Kb)}, gens {len(g1)}+{len(g0)} -> {fn}",
          flush=True)
    return fn


if __name__ == "__main__":
    q = int(sys.argv[1])
    only = set(int(x) for x in sys.argv[2:]) if len(sys.argv) > 2 else None
    facs, rur = load_rur(q)
    print(f"=== q = {q}: {len(facs)} factors, degrees "
          f"{[len(f) for f in facs]} (sum {sum(len(f) for f in facs)}), "
          f"{len(rur)} RUR variables ===", flush=True)
    import subprocess
    for i, mod in enumerate(facs):
        if only is not None and i not in only:
            continue
        fn = run_branch(q, mod, rur, i)
        if fn is None:
            continue
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=1800)
        for line in r.stdout.strip().splitlines():
            print("      " + line)
        if r.stderr.strip():
            print("      STDERR " + r.stderr.strip()[:300])
