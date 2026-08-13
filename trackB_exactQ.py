#!/usr/bin/env python3
"""Exact-Q closure of case-(2) leaf 2 — the theorem-grade pass.

Everything runs inside Singular over ring 0 (char 0); no mod-p arithmetic
anywhere. Structure mirrors the prime sweep: normalized edge eliminant over Q,
Q-irreducible factors -> per-factor closure of the full system (44 leaf-2
equations + edge GB + Rabinowitsch nonvanishing), plus the d_3_3 = 0 chart
and the d_9_15 = 0 (r0) chart with recursive radicalization if needed.

Every node writes a marker; reruns resume. Verdicts -> trackB_staged_verdicts.log
tagged Q_. A branch that exceeds its timeout logs STALLED (never silently).
"""
import json, os, re, sys, time
import trackB_staged as S

WD = S.WD
# Leaf-2 keeps the historical unprefixed names (its markers are already on
# disk and its verdicts are the ones on record); leaf 1 gets its own
# namespace so the two exact-Q passes cannot share a marker.
PFX = "" if S.LEAF_ID == 2 else "L%d_" % S.LEAF_ID

def qsing(script, name, timeout):
    try:
        return S.sing(script, name, timeout=timeout)
    except Exception as e:
        S.log(f"{name}: STALLED/ERROR ({type(e).__name__}: {e})")
        return ""

def edge_header():
    scr = [f"ring R = 0, ({','.join(S.EDGE_VARS)}), lp;", "ideal I;"]
    n = 0
    for i in S.EDGE_IDX:
        n += 1; scr.append(f"I[{n}] = {S.leaf['equations'][i]};")
    return scr, n

def q_eliminant_factors():
    mark = os.path.join(WD, f"trackB_{PFX}Q_elim.json")
    if os.path.exists(mark):
        return json.load(open(mark))
    scr, n = edge_header()
    scr.append(f"I[{n+1}] = d_3_3-1;")
    scr += ["short=0;",
            "ideal E = eliminate(I, d_3_3*d_4_5*d_5_7*d_6_9*d_7_11*d_8_13);",
            '"ELIMDEG: " + string(deg(E[1]));',
            "list f = factorize(E[1]);", '"FACTORS:"; f[1];', "quit;"]
    out = qsing("\n".join(scr), f"trackB_{PFX}Q_elim.sing", int(os.environ.get("QELIM_TIMEOUT", "10800")))
    facs = []
    for ln in out.splitlines():
        m = re.match(r"_\[\d+\]=(.+)$", ln.strip())
        if m and m.group(1) != "1":
            facs.append(m.group(1))
    # Soundness guard: only cache a factor list from a run that actually
    # reached the factorization. A timeout/crash returns "" (or no FACTORS
    # block); caching [] there would silently skip every rk-branch on rerun
    # and read as a closure. Raise instead.
    if "FACTORS:" not in out or not facs:
        S.log("Q-SWEEP: eliminant factorization produced NO factors "
              "(timeout/crash) — marker NOT written; use the P1 fallback route")
        raise SystemExit("Q-eliminant factorization did not complete")
    json.dump(facs, open(mark, "w"))
    S.log(f"{PFX}Q-SWEEP: eliminant factors over Q: {len(facs)}  "
          f"degs {[max((len(x) // 40, 1)) for x in facs] if facs else []}")
    return facs

def q_close(tag, pin, extras, timeout=7200):
    """Full-system closure over Q for one branch: edge GB then residual GB."""
    mark = os.path.join(WD, f"trackB_{PFX}Q_done_{tag}")
    if os.path.exists(mark):
        return
    scr, n = edge_header()
    for x in [pin] + extras:
        n += 1; scr.append(f"I[{n}] = {x};")
    scr += ["short=0;", "option(redSB);", "ideal G = groebner(I);",
            'int d = dim(G);', f'"Q-EDGE {tag} DIM: " + string(d);',
            'if (d==0) { "Q-EDGE VDIM: " + string(vdim(G)); }',
            'if (d==-1) { "Q-EDGE EMPTY"; quit; }']
    # residual: full ring, all 44 equations + edge GB + Rabinowitsch
    allvars = sorted(set(v for e in S.leaf["equations"] for v in re.findall(r"d_\d+_\d+", e))
                     | set(S.EDGE_VARS) | set(S.leaf.get("nonzero", [])),
                     key=lambda s: tuple(map(int, s.split("_")[1:])))
    prod = "*".join([f"({v})" for v in S.leaf.get("nonzero", [])] +
                    [f"({e})" for e in S.leaf.get("nonzero_exprs", [])])
    scr += [f"ring RR = 0, ({','.join(allvars)},w), dp;",
            "ideal J = imap(R, G);", "int k;",
            "ideal I2;"]
    m = 0
    for e in S.leaf["equations"]:
        m += 1; scr.append(f"I2[{m}] = {e};")
    for x in [pin] + extras:
        m += 1; scr.append(f"I2[{m}] = {x};")
    scr.append(f"I2[{m+1}] = w*({prod})-1;")
    scr += ["I2 = I2 + J;", "ideal G2 = groebner(I2);", "int d2 = dim(G2);",
            f'"Q-BRANCH {tag} RESIDUAL DIM: " + string(d2);',
            f'if (d2==0) {{ "Q-BRANCH {tag} RESIDUAL VDIM: " + string(vdim(G2)); }}',
            f'if (d2==-1) {{ "Q-BRANCH {tag} EMPTY"; }}',
            "quit;"]
    out = qsing("\n".join(scr), f"trackB_{PFX}Q_{tag}.sing", timeout)
    lines = [l for l in out.splitlines() if "Q-EDGE" in l or "Q-BRANCH" in l]
    if lines:
        S.log(f"{PFX}Q {tag}: " + " | ".join(lines))
        open(mark, "w").write(out[-3000:])
    else:
        S.log(f"{PFX}Q {tag}: NO VERDICT (stalled or crashed — see trackB_{PFX}Q_{tag}.sing.out)")

def main():
    t0 = time.time()
    facs = q_eliminant_factors()
    nz = [f for f in facs if f.strip() != "d_9_15"]
    for k, f in enumerate(nz):
        q_close(f"rk{k}", "d_3_3-1", [f])
    q_close("r0a", "d_3_3-1", ["d_9_15"], timeout=10800)
    q_close("r0b", "d_3_3", ["d_9_15"], timeout=10800)
    S.log(f"{PFX}Q-SWEEP: pass finished in {time.time()-t0:.0f}s — check for STALLED/NO VERDICT lines before claiming closure")

if __name__ == "__main__":
    main()
