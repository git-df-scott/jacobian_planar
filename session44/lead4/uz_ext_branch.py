#!/usr/bin/env python3
"""uz_ext_run for a deg q < 8 branch: some q's are fixed by the branch
(q_m = 1, q_a = 0 for a > m) and only the rest appear in the RUR."""
import ast, subprocess, sys
from uz_eliminate import run
from uz_system import PVARS
from uz_ext import Field, nullspace_F, solve_affine_F, partial_F, PV, FV
import uz_ext_run as R


def main(path, base):
    txt = open(path).read().strip().rstrip(":").replace("\n", "")
    D = ast.literal_eval(txt)
    p, nv, deg, varn, lf, rest = D[1]
    elim, den, plist = rest[1]
    w = elim[1]
    facs = R.factor_univariate(w, p, "bfac")
    print(f"  eliminant degree {len(w)-1} factors as "
          f"{[(m, len(R.poly_from_string(f,p))-1) for m,f in facs]}")
    obs, _ = run(mod=p, fixed={}, verbose=False)
    obs = dict(obs)
    E4 = [obs[(n, 4)] for n in range(13, 19)]
    E3 = [obs[(n, 3)] for n in range(13, 20)]
    E2 = [obs[(n, 2)] for n in range(13, 20)]
    tot = 0
    for fi, (mult, fs) in enumerate(facs):
        h = R.poly_from_string(fs, p)
        if len(h) - 1 == 0:
            continue
        if h[-1] != 1:
            iv = pow(h[-1], p - 2, p); h = [c*iv % p for c in h]
        d = len(h) - 1
        K = Field(p, h)
        T = K.gen() if d > 1 else K.const((-h[0]) % p)
        tot += d
        def ev(co):
            r = K.zero()
            for c in reversed(co):
                r = K.add(K.mul(r, T), K.const(c))
            return r
        dv = ev(den[1])
        if K.iszero(dv):
            print(f"    factor {fi}: denominator vanishes, skipped"); continue
        iv = K.inv(dv)
        val = {v: K.zero() for v in PVARS}
        for k, v in base.items():
            val[k] = K.const(v)
        val[varn[-1]] = T
        for name, entry in zip(varn[:len(plist)], plist):
            dd, co = entry[0]
            val[name] = K.sub(K.zero(), K.mul(ev(co), iv))
        ok = all(not partial_F(K, e, val, []) for e in E4)
        A = []
        for e in E3:
            dd = partial_F(K, e, val, PV); row = [K.zero()]*8
            for mono, c in dd.items(): row[list(mono).index(1)] = c
            A.append(row)
        ker = nullspace_F(K, A)
        Mrows = []
        for e in E2:
            dd = partial_F(K, e, val, FV+PV); row = [K.zero()]*8
            for mono, c in dd.items():
                fp, pp = mono[:8], mono[8:]
                if sum(fp) == 1 and sum(pp) == 0:
                    row[list(fp).index(1)] = c
            Mrows.append(row)
        kerM = nullspace_F(K, Mrows)
        print(f"    factor {fi}: deg {d}, q verifies {ok}, "
              f"p-kernel dim {len(ker)}, ker(M) dim {len(kerM)} "
              f"-> endgame in {len(ker)+len(kerM)} parameters")
    print(f"  total degree covered: {tot}")


if __name__ == "__main__":
    for m in (4, 6):
        base = {('q%d' % a): 0 for a in range(m+1, 9)}
        base['q%d' % m] = 1
        print(f"=== deg q = {m}")
        main('bq%d.out' % m, base)
