#!/usr/bin/env python3
"""The branches with deg q < 8.

2 q t' - 3 q' t = u^2 with deg q = Q, deg t = T forces, whenever
Q + T - 1 > 2, the vanishing of the leading coefficient (2T - 3Q) q_Q t_T,
i.e. 2T = 3Q; so Q is even.  The only other possibility is Q + T - 1 = 2,
i.e. (Q,T) = (1,2), q = u exactly.  Hence

    deg q  in  {1, 2, 4, 6, 8}.

deg q = 8 is the polygon branch (vertex (8,14) present) and is handled by
uz_ext_run.py.  Here we do 1, 2, 4, 6 -- each is a single point of the
q-layer once the residual torus is used to scale the leading coefficient
to 1, so the cascade is pure linear algebra.
"""
import subprocess
import sys

from uz_eliminate import run
from uz_system import PVARS
from uz_cascade import nullspace, solve_affine, partial
from uz_cascade_run import tadd, tmul, tscal, tpow
from uz_final import to_str

MOD = 999983
PV = ["p%d" % a for a in range(1, 9)]
FV = ["f%d" % a for a in range(1, 9)]
VN = ["lam", "mu", "nu1", "nu2", "nu3", "nu4", "nu5", "nu6"]


def singular(script, tag):
    open(f"{tag}.sing", "w").write(script)
    r = subprocess.run(["Singular", "-q", f"{tag}.sing"], capture_output=True,
                       text=True, timeout=7200)
    return r.stdout.strip()


def cascade(qval, tag, mod=MOD):
    obs, _ = run(mod=mod, fixed={}, verbose=False)
    obs = dict(obs)
    val = {v: 0 for v in PVARS}
    val.update(qval)
    E4 = [obs[(n, 4)] for n in range(13, 19)]
    bad4 = [n for n, e in zip(range(13, 19), E4)
            if partial(e, val, mod, [])]
    print(f"  q-layer satisfied: {not bad4}"
          + (f"  (fails at n={bad4})" if bad4 else ""))
    if bad4:
        return
    A = []
    for e in [obs[(n, 3)] for n in range(13, 20)]:
        d = partial(e, val, mod, PV)
        row = [0] * 8
        for mono, c in d.items():
            row[list(mono).index(1)] = c
        A.append(row)
    ker = nullspace(A, mod)
    nk = len(ker)
    Mrows, Qrows = [], []
    for e in [obs[(n, 2)] for n in range(13, 20)]:
        d = partial(e, val, mod, FV + PV)
        row = [0] * 8
        quad = {}
        for mono, c in d.items():
            fp, pp = mono[:8], mono[8:]
            if sum(fp) == 1 and sum(pp) == 0:
                row[list(fp).index(1)] = c
            elif sum(fp) == 0 and sum(pp) == 2:
                quad[pp] = c
            else:
                raise RuntimeError("unexpected monomial")
        Mrows.append(row)
        Qrows.append(quad)
    kerM = nullspace(Mrows, mod)
    nf = len(kerM)
    parts = {}
    bad = False
    for i in range(nk):
        for j in range(i, nk):
            vec = []
            for quad in Qrows:
                tot = 0
                for pp, c in quad.items():
                    idx = [a for a in range(8) for _ in range(pp[a])]
                    a, b = idx
                    if i == j:
                        tot += c * ker[i][a] * ker[i][b]
                    else:
                        tot += c * (ker[i][a] * ker[j][b]
                                    + ker[j][a] * ker[i][b])
                vec.append((-tot) % mod)
            r = solve_affine(Mrows, vec, mod)
            if r is None:
                bad = True
            parts[(i, j)] = r[0] if r else None
    print(f"  p-kernel dim {nk}, ker(M) dim {nf}, f-layer solvable {not bad}")
    if bad:
        # NOT "no solution": Q(p) leaves image(M), so there are extra
        # cokernel conditions on the parameters that this reduction drops.
        print("  -> UNDECIDED: non-surjective f-layer, extra cokernel "
              "conditions not carried by this reduction")
        return
    NV = nk + nf
    names = VN[:NV]

    def gen(i):
        e = [0] * NV
        e[i] = 1
        return {tuple(e): 1}
    X = [gen(i) for i in range(nk)]
    NUS = [gen(nk + i) for i in range(nf)]
    pexpr = []
    for a in range(8):
        e = {}
        for i in range(nk):
            e = tadd(e, tscal(X[i], ker[i][a], mod), mod)
        pexpr.append(e)
    fexpr = []
    for a in range(8):
        e = {}
        for i in range(nf):
            e = tadd(e, tscal(NUS[i], kerM[i][a], mod), mod)
        for (i, j), vec in parts.items():
            e = tadd(e, tscal(tmul(X[i], X[j], mod), vec[a], mod), mod)
        fexpr.append(e)

    def subst(poly):
        out = {}
        for m, c in poly.items():
            term = {(0,) * NV: c % mod}
            for i, e in enumerate(m):
                if not e:
                    continue
                nm = PVARS[i]
                if nm[0] == "q":
                    term = tscal(term, pow(val[nm], e, mod), mod)
                elif nm[0] == "p":
                    term = tmul(term, tpow(pexpr[int(nm[1:]) - 1], e, mod, NV),
                                mod)
                else:
                    term = tmul(term, tpow(fexpr[int(nm[1:]) - 1], e, mod, NV),
                                mod)
            out = tadd(out, term, mod)
        return out
    eqs = [to_str(subst(e), names)
           for e in [obs[(n, 1)] for n in range(13, 20)]
           + [obs[(n, 0)] for n in range(2, 20)]]
    eqs = [e for e in eqs if e != "0"]
    L = [f"ring R = {mod}, ({','.join(names)},W), dp;",
         "ideal I = " + ",".join(eqs) + ";",
         '"  base dim (incl. W) = " + string(dim(std(I)));']
    for a in range(8):
        for nm, ex in (("f", to_str(fexpr[a], names)),
                       ("p", to_str(pexpr[a], names))):
            if ex == "0":
                L.append(f'"  {nm}{a+1}: identically 0";')
                continue
            L.append(f"ideal J{nm}{a} = I, ({ex})*W-1;")
            L.append(f"ideal G{nm}{a} = std(J{nm}{a});")
            L.append(f'"  {nm}{a+1} can be nonzero: " + '
                     f"string(!(size(G{nm}{a})==1 and G{nm}{a}[1]==1));")
    L.append("exit;")
    print(singular("\n".join(L), tag))


if __name__ == "__main__":
    for m in (1, 2, 4, 6):
        qv = {}
        for a in range(2, 9):
            qv["q%d" % a] = 1 if a == m else 0
        print(f"=== branch deg q = {m}   (q = u"
              + (f" + u^{m}" if m > 1 else "") + ", torus-normalised)")
        cascade(qv, f"lowq_{m}")
