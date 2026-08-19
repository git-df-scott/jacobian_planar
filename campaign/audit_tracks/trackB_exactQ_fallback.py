#!/usr/bin/env python3
"""P1 fallback route — exact-Q closure WITHOUT the char-0 edge eliminant.

OPUS_PLAN P1: "if the char-0 eliminant factorization exceeded ~3h CPU total:
kill it and use the fallback: per-branch exact closure WITHOUT the Q-eliminant
... skip the factorization; one big GB over Q per chart: d_3_3 normalized
chart and d_3_3 = 0 chart, plus the d_9_15 = 0 chart."

This does not wait for the eliminant to fail. The fallback is independent of
it — it never factors anything — so it runs concurrently on otherwise idle
cores. Whichever route lands first is the certificate; if both land they are
an independent cross-check of each other.

Charts (over ring 0, exact rationals, no mod-p anywhere):
  A  d_3_3 = 1   the normalized chart (d_3_3 != 0 rescaled by the A2 torus)
  B  d_3_3 = 0
  C  d_9_15 = 0  the r0 chart, run as a standalone chart as the plan specifies
A and B alone already cover the variety; C is a sub-case of them and is run
because the plan asks for it — a redundant EMPTY there is a free consistency
check, and a non-EMPTY there would flag a bug in A/B.

Per chart the ideal is: every equation of the leaf (the Newton-edge subsystem
is among them), the chart pin, and one Rabinowitsch generator
w*(product of all nonzero conditions and nonzero_exprs) - 1, so a point of the
variety is exactly a solution with every side condition nonzero. dim = -1 is
EMPTY over the algebraic closure of Q — Nullstellensatz-strong, which is the
proof standard.

Verdicts append to trackB_staged_verdicts.log tagged QF (leaf 2) or L<n>QF.
A chart that exceeds its timeout logs STALLED, never silently.

Usage:  [JCLEAF=1] [QF_TIMEOUT=21600] python3 trackB_exactQ_fallback.py [chart ...]
"""
import os, re, sys, time
import trackB_staged as S

WD = S.WD
PFX = "QF" if S.LEAF_ID == 2 else "L%dQF" % S.LEAF_ID
TIMEOUT = int(os.environ.get("QF_TIMEOUT", "21600"))      # 6h per the plan

CHARTS = {
    "A_d33_1":  "d_3_3-1",
    "B_d33_0":  "d_3_3",
    "C_d915_0": "d_9_15",
}


def all_vars():
    vs = set()
    for e in S.leaf["equations"]:
        vs |= set(re.findall(r"[cd]_\d+_\d+", e))
    for e in S.leaf.get("nonzero_exprs", []):
        vs |= set(re.findall(r"[cd]_\d+_\d+", e))
    vs |= set(S.EDGE_VARS) | set(S.leaf.get("nonzero", []))
    return sorted(vs, key=lambda s: (s[0], tuple(map(int, s.split("_")[1:]))))


def nonzero_product():
    parts = [f"({v})" for v in S.leaf.get("nonzero", [])] + \
            [f"({e})" for e in S.leaf.get("nonzero_exprs", [])]
    return "*".join(parts)


def run_chart(name, pin):
    mark = os.path.join(WD, f"trackB_{PFX}_{name}.done")
    if os.path.exists(mark):
        S.log(f"{PFX} {name}: already done (marker present)")
        return
    vs = all_vars()
    prod = nonzero_product()
    # ENGINE. Direct char-0 Buchberger on this shape does not finish inside a
    # container lifetime (measured: ~2.5h, and the eliminant route burned >1h
    # twice with no output). modStd computes the standard basis over Q by
    # modular methods with rational reconstruction — same ring, same ideal,
    # exact rational output, far cheaper.
    #
    # SOUNDNESS. modStd is probabilistic, so its verdict is not taken on
    # faith. When it reports dim = -1 (i.e. 1 in I) we extract an explicit
    # Nullstellensatz certificate with lift: cofactors T with I*T = 1, then
    # check that identity by exact polynomial arithmetic in the same run and
    # write T to disk. A verified certificate is independent of how the basis
    # was found — anyone can replay it with polynomial multiplication alone,
    # which is what OPUS_PLAN's "replayable certificate" standard asks for.
    engine = os.environ.get("QF_ENGINE", "modStd")
    assert engine in ("modStd", "groebner"), engine
    certf = os.path.join(WD, f"trackB_{PFX}_{name}.cert")
    # modStd parallelizes over its primes and will otherwise grab every core
    # it can see (measured: 14 forked Singulars on a 4-core box), starving the
    # leaf-1 chain sharing the machine. Cap it.
    cpus = int(os.environ.get("QF_CPUS", "2"))
    scr = (['LIB "modstd.lib";', 'system("--cpus", %d);' % cpus]
           if engine == "modStd" else []) + [
           f"ring R = 0, ({','.join(vs)},w), dp;", "short=0;", "ideal I;"]
    n = 0
    for e in S.leaf["equations"]:
        n += 1
        scr.append(f"I[{n}] = {e};")
    n += 1
    scr.append(f"I[{n}] = {pin};")
    n += 1
    scr.append(f"I[{n}] = w*({prod})-1;" if prod else f"I[{n}] = w-1;")
    scr += [("ideal G = modStd(I);" if engine == "modStd"
             else "option(redSB); ideal G = groebner(I);"),
            "int d = dim(G);",
            f'"QF-CHART {name} ENGINE: {engine}";',
            f'"QF-CHART {name} DIM: " + string(d);',
            f'if (d==0) {{ "QF-CHART {name} VDIM: " + string(vdim(G)); }}',
            'if (d==-1) {',
            '  matrix T = lift(I, ideal(1));',
            '  matrix C = matrix(I)*T;',
            f'  "QF-CHART {name} CERT-VERIFIED: " + string(C[1,1] == 1);',
            f'  link lo = ":w {certf}";',
            '  fprintf(lo, "%s", T); close(lo);',
            f'  "QF-CHART {name} EMPTY";',
            '}',
            "quit;"]
    scr = [l for l in scr if l != ""]
    t0 = time.time()
    try:
        out = S.sing("\n".join(scr), f"trackB_{PFX}_{name}.sing", timeout=TIMEOUT)
    except Exception as e:
        S.log(f"{PFX} {name}: STALLED after {time.time()-t0:.0f}s "
              f"({type(e).__name__}) — no verdict, nothing claimed")
        return
    lines = [l for l in out.splitlines() if "QF-CHART" in l]
    secs = time.time() - t0
    if lines:
        # Mandated verdict format. CLOSED requires dim == -1 (1 in I) — a
        # Nullstellensatz-strong statement. vdim == 0 is NOT a closure
        # criterion: a finite non-empty zero-set also has dim 0, and the
        # ideal (1) is the only thing dim == -1 reports.
        dim = None
        for l in lines:
            m = re.search(r"DIM: (-?\d+)", l)
            if m:
                dim = int(m.group(1))
        cert_ok = any("CERT-VERIFIED: 1" in l for l in lines)
        # CLOSED requires BOTH dim == -1 and a verified 1 = sum h_i f_i
        # certificate. A dim == -1 whose certificate did not verify is
        # reported as UNCERTIFIED, never as a closure.
        if dim == -1:
            status = ("CLOSED (dim = -1, certificate verified)" if cert_ok
                      else "UNCERTIFIED (dim = -1 but certificate did NOT "
                           "verify — treat as no verdict)")
        elif dim is not None:
            status = f"SURVIVOR (dim = {dim})"
        else:
            status = "NO DIM"
        S.log(f"BRANCH {PFX}_{name}: STATUS {status} | ENGINE Singular "
              f"{os.environ.get('QF_ENGINE', 'modStd')} | TIME {secs:.0f} sec")
        S.log(f"{PFX} {name}: ({secs:.0f}s) " + " | ".join(lines))
        open(mark, "w").write(out[-3000:])
        if dim is not None and dim >= 0:
            S.log(f"BRANCH {PFX}_{name}: SURVIVOR — ESCALATION TRIGGER "
                  f"(OPUS_PLAN §E: any verdict that is not EMPTY). "
                  f"Extract points before any claim.")
    else:
        S.log(f"BRANCH {PFX}_{name}: STATUS STALLED (no verdict) | ENGINE "
              f"Singular std | TIME {secs:.0f} sec")
        S.log(f"{PFX} {name}: NO VERDICT after {secs:.0f}s "
              f"(crashed or killed) — see trackB_{PFX}_{name}.sing.out")


def main():
    want = sys.argv[1:] or list(CHARTS)
    S.log(f"{PFX}-FALLBACK: starting charts {want} on leaf {S.LEAF_ID} "
          f"({len(S.leaf['equations'])} equations, timeout {TIMEOUT}s each)")
    t0 = time.time()
    for name in want:
        if name not in CHARTS:
            S.log(f"{PFX}: unknown chart {name}")
            continue
        run_chart(name, CHARTS[name])
    S.log(f"{PFX}-FALLBACK: pass finished in {time.time()-t0:.0f}s — check for "
          f"STALLED / NO VERDICT lines before claiming closure")


if __name__ == "__main__":
    main()
