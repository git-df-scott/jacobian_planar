#!/usr/bin/env python3
"""Find the mod-p Nullstellensatz certificate SUPPORT, then verify over Q.

Why. Exact-Q closure of a case-(2) chart is blocked not by the geometry but by
coefficient growth: direct char-0 Buchberger burned >1h twice without output,
and modStd (modular + rational reconstruction) did not finish the char-0 EDGE
ideal in 10 minutes. Meanwhile the same systems close mod p in seconds. And
mod-p emptiness is NOT a proof of Q-emptiness — the standard counterexample is
I = (p*x - 1), which is (1) mod p while V(I_Q) = {1/p} is nonempty — so the
campaign's rule that mod-p is scouting only stands.

The route. A chart's ideal is (1) mod p, so Singular's lift gives cofactors
h_i with sum h_i f_i = 1 over F_p. Only a few of the many generators usually
carry nonzero cofactors. That SUPPORT is the useful mod-p output: it is a
guess at which handful of the generators already generate 1. Take that
handful, and over Q compute lift on it alone. If sum h_i f_i = 1 verifies
exactly over Q, emptiness is PROVED — a verified certificate is valid however
it was found, and the mod-p step contributed only a hint about where to look.
If it fails, nothing is claimed: the hint was wrong and the chart stays open.

Note the cofactors themselves are NOT reconstructed across primes. lift's
output depends on the computation path, so it is not canonical and CRT across
primes would be meaningless. Only the support — a set of indices — is carried
over, and the char-0 lift is recomputed from scratch on that subset.

Usage:  [JCLEAF=1] python3 trackB_certsupport.py CHART [PRIME]
        CHART in A_d33_1 | B_d33_0 | C_d915_0
"""
import os, re, sys, time
import trackB_staged as S
import trackB_exactQ_fallback as QF

WD = S.WD


def build_gens(chart):
    """The chart's generator list, in a fixed order, as Singular strings."""
    pin = QF.CHARTS[chart]
    prod = QF.nonzero_product()
    gens = list(S.leaf["equations"]) + [pin]
    gens.append(f"w*({prod})-1" if prod else "w-1")
    return gens, QF.all_vars()


def modp_support(chart, p, timeout=1800):
    """Cofactor support of 1 in the chart ideal over F_p."""
    gens, vs = build_gens(chart)
    scr = [f"ring R = {p}, ({','.join(vs)},w), dp;", "short=0;", "ideal I;"]
    for k, g in enumerate(gens):
        scr.append(f"I[{k+1}] = {g};")
    scr += ["ideal G = groebner(I);",
            '"DIM: " + string(dim(G));',
            'if (dim(G) != -1) { "NOT EMPTY MOD P — no certificate exists"; quit; }',
            "matrix T = lift(I, ideal(1));",
            "matrix C = matrix(I)*T;",
            '"CERTCHECK: " + string(C[1,1] == 1);',
            "int i; string s = \"\";",
            "for (i = 1; i <= nrows(T); i++) { if (T[i,1] != 0) "
            "{ s = s + string(i) + \",\"; } }",
            '"SUPPORT: " + s;',
            "quit;"]
    out = S.sing("\n".join(scr), f"trackB_certsup_{chart}_p{p}.sing",
                 timeout=timeout)
    sup, ok = [], False
    for ln in out.splitlines():
        if ln.startswith("SUPPORT: "):
            sup = [int(x) for x in ln[9:].strip().rstrip(",").split(",") if x]
        if ln.startswith("CERTCHECK: "):
            ok = ln.strip().endswith("1")
    return sup, ok, out


def q_verify(chart, support, timeout=5400):
    """Char-0 lift restricted to the mod-p support. A PASS here is a proof."""
    gens, vs = build_gens(chart)
    sub = [gens[i - 1] for i in support]
    scr = [f"ring R = 0, ({','.join(vs)},w), dp;", "short=0;", "ideal I;"]
    for k, g in enumerate(sub):
        scr.append(f"I[{k+1}] = {g};")
    scr += ["ideal G = groebner(I);",
            '"QDIM: " + string(dim(G));',
            'if (dim(G) == -1) {',
            "  matrix T = lift(I, ideal(1));",
            "  matrix C = matrix(I)*T;",
            '  "QCERT-VERIFIED: " + string(C[1,1] == 1);',
            f'  link lo = ":w {os.path.join(WD, "trackB_certQ_" + chart + ".cert")}";',
            '  fprintf(lo, "%s", T); close(lo);',
            "}",
            "quit;"]
    out = S.sing("\n".join(scr), f"trackB_certQ_{chart}.sing", timeout=timeout)
    return out


def main():
    chart = sys.argv[1] if len(sys.argv) > 1 else "A_d33_1"
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 65521
    assert chart in QF.CHARTS, chart
    gens, _ = build_gens(chart)
    S.log(f"CERTSUP {chart}: {len(gens)} generators, probing support mod {p}")
    t0 = time.time()
    sup, ok, _ = modp_support(chart, p)
    if not sup:
        S.log(f"CERTSUP {chart}: no support found mod {p} "
              f"({time.time()-t0:.0f}s) — see trackB_certsup_{chart}_p{p}.sing.out")
        return 1
    S.log(f"CERTSUP {chart}: mod-{p} certificate uses {len(sup)}/{len(gens)} "
          f"generators (indices {sup}), self-check {ok}, {time.time()-t0:.0f}s")
    t1 = time.time()
    out = q_verify(chart, sup)
    lines = [l for l in out.splitlines() if l.startswith(("QDIM", "QCERT"))]
    if any("QCERT-VERIFIED: 1" in l for l in lines):
        S.log(f"BRANCH {chart}: STATUS CLOSED (dim = -1, Q certificate "
              f"verified on the {len(sup)}-generator mod-p support) | "
              f"ENGINE Singular groebner+lift | TIME {time.time()-t1:.0f} sec")
    else:
        S.log(f"CERTSUP {chart}: char-0 lift on the mod-p support did NOT "
              f"certify ({'; '.join(lines) or 'no output'}) after "
              f"{time.time()-t1:.0f}s — nothing claimed, chart stays open")
    return 0


if __name__ == "__main__":
    sys.exit(main())
