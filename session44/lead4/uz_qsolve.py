#!/usr/bin/env python3
"""Read an msolve RUR for the q-layer and return explicit GF(p) solutions."""
import ast
import sys

from uz_eliminate import run
from uz_system import PVARS


def polyeval(co, T, mod):
    r = 0
    for c in reversed(co):
        r = (r * T + c) % mod
    return r


def roots_gfp(co, mod):
    """roots of a univariate polynomial over GF(mod) via gcd(x^mod - x, f)."""
    # cheap: for mod up to a few million just scan with Horner in C-speed loops
    f = [c % mod for c in co]
    while f and f[-1] == 0:
        f.pop()
    if not f:
        return list(range(mod))
    # x^mod mod f  by square-and-multiply, then gcd(x^mod - x, f)
    def polymulmod(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        res[i + j] = (res[i + j] + x * y) % mod
        return polymod(res)

    def polymod(a):
        a = a[:]
        d = len(f) - 1
        inv = pow(f[-1], mod - 2, mod)
        while len(a) - 1 >= d and len(a) > 0:
            while a and a[-1] == 0:
                a.pop()
            if len(a) - 1 < d:
                break
            c = a[-1] * inv % mod
            sh = len(a) - 1 - d
            for i in range(d + 1):
                a[sh + i] = (a[sh + i] - c * f[i]) % mod
            while a and a[-1] == 0:
                a.pop()
        return a or [0]

    # x^mod mod f
    e = mod
    base = polymod([0, 1])
    acc = [1]
    while e:
        if e & 1:
            acc = polymulmod(acc, base)
        base = polymulmod(base, base)
        e >>= 1
    g = acc[:]
    if len(g) < 2:
        g = g + [0] * (2 - len(g))
    g[1] = (g[1] - 1) % mod
    while g and g[-1] == 0:
        g.pop()
    if not g:
        g = f[:]

    def polygcd(a, b):
        a, b = a[:], b[:]
        while b and any(b):
            # a mod b
            fb = b
            r = a[:]
            d = len(fb) - 1
            inv = pow(fb[-1], mod - 2, mod)
            while True:
                while r and r[-1] == 0:
                    r.pop()
                if len(r) - 1 < d or not r:
                    break
                c = r[-1] * inv % mod
                sh = len(r) - 1 - d
                for i in range(d + 1):
                    r[sh + i] = (r[sh + i] - c * fb[i]) % mod
                while r and r[-1] == 0:
                    r.pop()
            a, b = b, (r or [0])
        return a
    G = polygcd(f, g)
    deg = len(G) - 1
    if deg <= 0:
        return []
    # split G (all roots simple, in GF(mod)) by equal-degree splitting
    import random
    rng = random.Random(12345)
    out = []
    stack = [G]
    while stack:
        h = stack.pop()
        while h and h[-1] == 0:
            h.pop()
        d = len(h) - 1
        if d <= 0:
            continue
        if d == 1:
            out.append((-h[0]) * pow(h[1], mod - 2, mod) % mod)
            continue
        # random split
        for _ in range(200):
            a = rng.randrange(mod)
            # compute (x+a)^((mod-1)/2) - 1 mod h
            def mm(u, v):
                res = [0] * (len(u) + len(v) - 1)
                for i, x in enumerate(u):
                    if x:
                        for j, y in enumerate(v):
                            if y:
                                res[i + j] = (res[i + j] + x * y) % mod
                # reduce mod h
                r = res
                dd = len(h) - 1
                inv = pow(h[-1], mod - 2, mod)
                while True:
                    while r and r[-1] == 0:
                        r.pop()
                    if not r or len(r) - 1 < dd:
                        break
                    c = r[-1] * inv % mod
                    sh = len(r) - 1 - dd
                    for i in range(dd + 1):
                        r[sh + i] = (r[sh + i] - c * h[i]) % mod
                return r or [0]
            e = (mod - 1) // 2
            base = [a % mod, 1]
            acc = [1]
            while e:
                if e & 1:
                    acc = mm(acc, base)
                base = mm(base, base)
                e >>= 1
            cand = acc[:]
            if len(cand) < 1:
                continue
            cand = cand[:] + [0] * max(0, 1 - len(cand))
            cand[0] = (cand[0] - 1) % mod
            while cand and cand[-1] == 0:
                cand.pop()
            if not cand:
                continue
            g2 = polygcd(h, cand)
            while g2 and g2[-1] == 0:
                g2.pop()
            if 0 < len(g2) - 1 < d:
                # h / g2
                r = h[:]
                quo = [0] * (len(h) - len(g2) + 1)
                inv = pow(g2[-1], mod - 2, mod)
                while True:
                    while r and r[-1] == 0:
                        r.pop()
                    if not r or len(r) < len(g2):
                        break
                    c = r[-1] * inv % mod
                    sh = len(r) - len(g2)
                    quo[sh] = c
                    for i in range(len(g2)):
                        r[sh + i] = (r[sh + i] - c * g2[i]) % mod
                stack.append(g2)
                stack.append(quo)
                break
        else:
            raise RuntimeError("splitting failed")
    return sorted(set(out))


def qsolutions(path, verbose=True):
    txt = open(path).read().strip().rstrip(":").replace("\n", "")
    D = ast.literal_eval(txt)
    if D[0] != 0:
        raise RuntimeError(f"not 0-dimensional: {D[0]}")
    mod, nv, deg, varn, lf, rest = D[1]
    elim, den, plist = rest[1]
    w = elim[1]
    wp = [(i * c) % mod for i, c in enumerate(w)][1:]
    rts = roots_gfp(w, mod)
    obs, _ = run(mod=mod, fixed={}, verbose=False)
    obs = dict(obs)
    qeq = [obs[(n, 4)] for n in range(13, 19)]

    def ep(poly, val):
        tot = 0
        for m, c in poly.items():
            t = c
            for i, e in enumerate(m):
                if e:
                    t = t * pow(val[PVARS[i]], e, mod) % mod
            tot = (tot + t) % mod
        return tot
    sols = []
    for T in rts:
        for conv in ("den", "wp"):
            dv = polyeval(den[1], T, mod) if conv == "den" \
                else polyeval(wp, T, mod)
            if dv == 0:
                continue
            inv = pow(dv, mod - 2, mod)
            val = {v: 0 for v in PVARS}
            val[varn[-1]] = T
            for name, entry in zip(varn[:len(plist)], plist):
                d, co = entry[0]
                val[name] = (-polyeval(co, T, mod) * inv) % mod
            if all(ep(e, val) == 0 for e in qeq):
                sols.append({k: val[k] for k in PVARS if k.startswith("q")})
                break
    if verbose:
        print(f"{path}: mod {mod}, elim deg {deg}, "
              f"{len(rts)} rational roots -> {len(sols)} verified q-solutions")
    return mod, sols


if __name__ == "__main__":
    for path in sys.argv[1:]:
        mod, sols = qsolutions(path)
        for s in sols:
            print("   ", s)
