#!/usr/bin/env python3
"""Explicit F_p point of subcase 1's essential-face variety (all in Singular).

The eliminating polynomial of the reduced 6-variable system was computed
EXACTLY over Q by msolve: it is h(T^7) with T = a6 and

    h(s) = 9374377445732 s^5 + 62410476400737833472 s^4
         + 265472843532245531128968765 s^3
         + 591414847960503971284831143987840 s^2
         + 586529490054134032292876680565455306752 s
         - 1888043347611739526396142670327809715470336

irreducible over Q (sympy).  Pick p with 7 not dividing p-1 and h having a
root s0 in F_p; then a6 = s0^(1/7) is unique in F_p, and the remaining
unknowns follow from a Groebner basis of the sliced ideal.  The point is
then VERIFIED by evaluating W(u) = f g + 2u f g' - 3u f' g directly.
"""
import re as _re
import subprocess
import sys

from case1_ladder import coeffs, sym

M, N = 7, 10
HCO = [-1888043347611739526396142670327809715470336,
       586529490054134032292876680565455306752,
       591414847960503971284831143987840,
       265472843532245531128968765,
       62410476400737833472,
       9374377445732]


def sing_src(p, a6):
    W = coeffs(M, N)
    L = ["ring R = %d, (a1,a2,a3,a4,a5,a6), dp;" % p, "poly b0 = 1;"]
    for n in range(1, N + 1):
        rest = []
        for (c, i, j) in W[n]:
            if i == 0 and j == n:
                continue
            rest.append("(%d)*%s*b%d" % (c, sym('a', i, M), j))
        L.append("poly b%d = -(%s) / %d;"
                 % (n, " + ".join(rest) or "0", 1 + 2 * n))
    eqs = []
    for n in range(N + 1, M + N + 1):
        t = " + ".join("(%d)*%s*b%d" % (c, sym('a', i, M), j)
                       for (c, i, j) in W[n])
        if t:
            eqs.append(t)
    L.append("ideal I = " + ", ".join(eqs) + ", a6 - (%d);" % a6)
    L.append("ideal G = std(I);")
    L.append('"vdim " + string(vdim(G));')
    L.append('"BASIS"; int i; for (i=1;i<=size(G);i++) { string(G[i]); }')
    L.append("quit;")
    return "\n".join(L)


def build_fg(avals, p):
    a = [1] + [v % p for v in avals] + [1]
    W = coeffs(M, N)
    b = [1]
    for n in range(1, N + 1):
        rest = 0
        for (c, i, j) in W[n]:
            if i == 0 and j == n:
                continue
            rest = (rest + c * a[i] * b[j]) % p
        b.append((-rest * pow(1 + 2 * n, -1, p)) % p)
    return a, b


def Wval(a, b, p, n):
    return sum(c * a[i] * b[j] for (c, i, j) in coeffs(M, N)[n]) % p


def check(a, b, p):
    return [(n, Wval(a, b, p, n)) for n in range(0, M + N + 1)
            if Wval(a, b, p, n) != (1 if n == 0 else 0)]


def solve_linear(rows, p):
    """Gaussian elimination mod p on rows [c1..c6 | const] meaning sum=0."""
    m = [r[:] for r in rows]
    piv = {}
    r0 = 0
    for c in range(6):
        pr_ = None
        for r in range(r0, len(m)):
            if m[r][c] % p:
                pr_ = r
                break
        if pr_ is None:
            continue
        m[r0], m[pr_] = m[pr_], m[r0]
        inv = pow(m[r0][c], -1, p)
        m[r0] = [(v * inv) % p for v in m[r0]]
        for r in range(len(m)):
            if r != r0 and m[r][c] % p:
                f = m[r][c]
                m[r] = [(m[r][k] - f * m[r0][k]) % p for k in range(7)]
        piv[c] = r0
        r0 += 1
    if len(piv) != 6:
        return None
    return [(-m[piv[c]][6]) % p for c in range(6)]


def find(p, which=0):
    if (p - 1) % 7 == 0:
        return None, "p == 1 mod 7 (7th root not unique)"
    hc = [c % p for c in HCO]
    rts = [v for v in range(p)
           if sum(hc[i] * pow(v, i, p) for i in range(6)) % p == 0]
    if not rts:
        return None, "quintic has no root mod p"
    s0 = rts[which % len(rts)]
    a6 = pow(s0, pow(7, -1, p - 1), p)
    assert pow(a6, 7, p) == s0
    fn = "_scratch_case1/pt_%d_%d.sing" % (p, which)
    open(fn, "w").write(sing_src(p, a6))
    pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                        text=True, timeout=1800)
    # vdim is 1, so every basis element is an affine-linear form in a1..a6.
    rows = []
    for line in pr.stdout.splitlines():
        line = line.strip()
        if not line or not _re.fullmatch(r"[-+*0-9a-z ]+", line):
            continue
        if "a" not in line and not line.lstrip("-").isdigit():
            continue
        row = [0] * 7
        ok = True
        for tok in _re.findall(r"[+-]?[^+-]+", line.replace(" ", "")):
            mm = _re.fullmatch(r"([+-]?)(\d*)\*?(a[1-6])?", tok)
            if not mm:
                ok = False
                break
            sg = -1 if mm.group(1) == "-" else 1
            co = int(mm.group(2)) if mm.group(2) else 1
            v = mm.group(3)
            if v:
                row[int(v[1]) - 1] = (row[int(v[1]) - 1] + sg * co) % p
            else:
                row[6] = (row[6] + sg * co) % p
        if ok:
            rows.append(row)
    vals = solve_linear(rows, p)
    if vals is not None and len(vals) == 6:
        av = vals
        a, b = build_fg(av, p)
        return (av, a, b, check(a, b, p), len(rts)), None
    return None, "no rational point read; Singular said:\n" + pr.stdout[:900]


if __name__ == "__main__":
    for p in [int(v) for v in sys.argv[1:]]:
        r, err = find(p)
        print("=== p=%d (p mod 7 = %d) ===" % (p, p % 7))
        if err:
            print("   ", err)
            continue
        av, a, b, bad, nr = r
        print("    quintic roots in F_p:", nr)
        print("    a1..a6 =", av)
        print("    f = a_0..a_7  =", a)
        print("    g = b_0..b_10 =", b)
        print("    W-1 residuals:",
              bad if bad else "ALL ZERO -- point verified")
