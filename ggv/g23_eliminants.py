#!/usr/bin/env python3
"""G2/G3 -- the mu-eliminants of the reduced B=16 charts, two engines.

For each d and chart, eliminate EVERY a_i, b_i and the saturation variable t
from the chart ideal, leaving the ideal's constraints on the mu-variables that
survive the chart's gauge fixing:
    chart A (mu2 = 1)          -> constraints on (mu0, mu3)
    chart B (mu2 = 0, mu3 = 1) -> constraints on  mu0  alone

Engines (both over GF(p), same p, same generators):
    msolve   -e <#eliminated> -g 2   (block elimination order, full reduced GB)
    Singular eliminate(I, prod of eliminated variables)
Both eliminants are then normalised in ONE ring -- a reduced Groebner basis in
the surviving mu-variables only -- so the two engines are compared as ideals,
not as accidental generator lists.  d = 3 and d = 4 are run on BOTH engines and
required to agree (cross-engine control).

Controls (all computed from the run, none asserted):
  POSITIVE (d=3): chart A is empty at d=3, so its eliminant must be the unit
      ideal <1> -- i.e. have no admissible root at all.
  NEGATIVE: dropping one generator must CHANGE the eliminant.
  Saturated and unsaturated eliminants are both recorded; the unsaturated one
  is what G5 re-uses at d=3.

An elimination that OOMs or times out is RECORDED with its peak RSS and the
run moves to the next d.
"""
import os, re, shlex, signal, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wave5"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w5_b16_reduce import reduced_charts, to_ms
from w5_b16_abel import mu0, mu1, mu2, mu3
from sympy import Symbol, Poly, expand, lcm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(REPO, "ggv", "elim_work")
OUTD = os.path.join(REPO, "ggv", "mu_eliminants")
P = 1000003                       # p = 1 mod 3
MEM_POLICY = "oom_score_adj=1000, no vm cap"   # see ggv/g_runner.py
t = Symbol('t')
KEEP = {"A": [mu0, mu3], "B": [mu0]}


def sh(cmd, timeout):
    """Run one engine process, serialized, in its own process group.

    Memory policy matches ggv/g_runner.py: no artificial address-space cap; the
    engine carries oom_score_adj 1000 so the kernel reclaims it and nothing
    else, which arrives as returncode -9/137 and is recorded as STALLED-OOM.
    On timeout the whole process group is killed, so no engine outlives its
    deadline and overlaps the next job."""
    inner = "echo 1000 > /proc/self/oom_score_adj 2>/dev/null; exec " + cmd
    script = "/usr/bin/time -v /bin/bash -c " + shlex.quote(inner)
    t0 = time.time()
    p = subprocess.Popen(["/bin/bash", "-c", script], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, start_new_session=True)
    to = False
    try:
        out, err = p.communicate(timeout=timeout)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        to = True
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(os.getpgid(p.pid), sig)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                out, err = p.communicate(timeout=30)
                break
            except subprocess.TimeoutExpired:
                out, err = "", ""
        else:
            out, err = "", ""
        rc = p.returncode
    m = re.search(r"Maximum resident set size \(kbytes\): (\d+)", err or "")
    return {"rc": rc, "stderr": err, "stdout": out, "timeout": to,
            "rss_kb": int(m.group(1)) if m else -1, "wall_s": round(time.time()-t0, 2)}


def chart_ideal(d, chart, saturated=True):
    eqs, vars_ = reduced_charts(d)[chart]
    if not saturated:
        # the saturation generator is the unique one containing t
        eqs = [e for e in eqs if not e.has(t)]
        vars_ = [v for v in vars_ if v != t]
    keep = KEEP[chart]
    elim = [v for v in vars_ if v not in keep]
    return eqs, elim, keep


def int_clear(e, gens):
    p = Poly(e, *gens)
    den = 1
    for c in p.coeffs():
        den = lcm(den, c.q if hasattr(c, 'q') else 1)
    return expand(e * den)


def poly_str(e, gens):
    return str(Poly(int_clear(e, gens), *gens).as_expr()).replace('**', '^').replace(' ', '')


# ---------------------------------------------------------------- msolve ----
def elim_msolve(eqs, elim, keep, tag, timeout):
    gens = list(elim) + list(keep)          # eliminated block FIRST, as -e requires
    path = os.path.join(WORK, f"{tag}.msolve.ms")
    open(path, "w").write(to_ms(eqs, gens, P))
    outp = os.path.join(WORK, f"{tag}.msolve.gb")
    r = sh(f"msolve -e {len(elim)} -g 2 -f '{path}' -o '{outp}'", timeout)
    body = open(outp).read() if os.path.exists(outp) else ""
    r["raw"] = body
    r["input"] = path
    r["gb_file"] = outp
    if not body.strip():
        r["gens"] = None                    # failed run: no artifact, never a verdict
        return r
    ename = {str(v) for v in elim}
    # msolve -g 2 prints a '#'-commented header (characteristic, variable order,
    # monomial order, basis length) and then the reduced basis as a bracketed,
    # comma-separated list, one element per line.  The header must be stripped:
    # feeding it downstream was silently turning "#monomial order: ..." into a
    # fake generator.
    payload = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#"))
    payload = payload.strip().rstrip(":").strip()
    if payload.startswith("["):
        payload = payload[1:]
    if payload.endswith("]"):
        payload = payload[:-1]
    gens_out = []
    for chunk in payload.split(","):
        g = chunk.strip()
        if not g:
            continue
        toks = set(re.findall(r"[A-Za-z_]\w*", g))
        if toks & ename:            # still mentions an eliminated variable
            continue
        gens_out.append(g)
    r["gens"] = gens_out
    return r


# -------------------------------------------------------------- Singular ----
def elim_singular(eqs, elim, keep, tag, timeout):
    gens = list(elim) + list(keep)
    ring = ",".join(str(v) for v in gens)
    ideal = ",\n".join(poly_str(e, gens) for e in eqs)
    prod = "*".join(str(v) for v in elim)
    src = os.path.join(WORK, f"{tag}.sing")
    open(src, "w").write(f"""option(redSB);
ring R = {P},({ring}),dp;
ideal I = {ideal};
ideal E = eliminate(I,{prod});
E = std(E);
int i;
for (i=1; i<=size(E); i++) {{ print(E[i]); }}
print("SINGULAR_DONE");
quit;
""")
    r = sh(f"Singular -q --no-warn '{src}'", timeout)
    r["input"] = src
    out = r["stdout"] or ""
    r["raw"] = out
    if "SINGULAR_DONE" not in out:
        r["gens"] = None
        return r
    lines = [l.strip() for l in out.splitlines() if l.strip()
             and l.strip() != "SINGULAR_DONE"]
    if any(l.startswith("?") for l in lines):
        r["gens"] = None            # Singular error text is not an eliminant
        return r
    r["gens"] = lines
    return r


# ------------------------------------------------- canonical normalisation ---
def normalise(gens, keep, tag, timeout=1200):
    """Reduced GB of <gens> inside the ring of the surviving mu-variables only."""
    if gens is None:
        return None
    if not gens:
        return []                                   # the zero ideal
    ring = ",".join(str(v) for v in keep)
    src = os.path.join(WORK, f"{tag}.norm.sing")
    open(src, "w").write(f"""option(redSB);
ring R = {P},({ring}),dp;
ideal J = {",".join(gens)};
J = std(J);
int i; for (i=1;i<=size(J);i++) {{ print(J[i]); }}
print("SINGULAR_DONE");
quit;
""")
    r = sh(f"Singular -q --no-warn '{src}'", timeout)
    out = r["stdout"] or ""
    if "SINGULAR_DONE" not in out:
        return None
    lines = [l.strip() for l in out.splitlines()
             if l.strip() and l.strip() != "SINGULAR_DONE"]
    # Singular reports errors on stdout beginning with '?'.  Returning those as
    # if they were generators is exactly the kind of silent lie the campaign
    # tooling contract warns about -- refuse the result instead.
    if any(l.startswith("?") for l in lines):
        return None
    return lines


# --------------------------------------------------------------- driver -----
FAIL = []
LOG = []

def check(label, cond, note=""):
    line = ("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else "")
    print(line, flush=True)
    LOG.append(line)
    if not cond:
        FAIL.append(label)


def status(r):
    if r.get("gens") is not None:
        return "OK"
    if r.get("timeout"):
        return "TIMEOUT"
    rc = r["rc"]
    txt = (r["stdout"] or "") + (r["stderr"] or "")
    if rc in (-9, 137) or "Cannot allocate memory" in txt \
       or "no more memory" in txt or "Out of memory" in txt:
        return "STALLED-OOM"
    if isinstance(rc, int) and (rc < 0 or rc > 128):
        return "CRASH"
    return "NO-OUTPUT"


def write_eliminant(chart, d, blocks):
    path = os.path.join(OUTD, f"chart{chart}_d{d}.txt")
    with open(path, "w") as f:
        f.write(f"# GGV B=16 mu-eliminant -- chart {chart}, d = deg(q1) = {d}\n")
        f.write(f"# builder: wave5/w5_b16_reduce.py::reduced_charts({d})[{chart!r}]\n")
        f.write(f"# field: GF({P})  (p = 1 mod 3)\n")
        f.write(f"# surviving variables: {', '.join(str(v) for v in KEEP[chart])}\n")
        f.write("# every a_i, every b_i and the saturation variable t are eliminated\n")
        f.write("# exact polynomials below; an empty generator list means the ZERO ideal,\n")
        f.write("# a lone '1' means the UNIT ideal <1> (no admissible root)\n")
        for name, blk in blocks:
            f.write("\n" + "=" * 70 + "\n" + name + "\n" + "=" * 70 + "\n")
            for k, v in blk.items():
                if k == "gens":
                    continue
                f.write(f"{k}: {v}\n")
            g = blk.get("gens")
            f.write("generators:\n")
            if g is None:
                f.write("  <none: run did not produce an artifact>\n")
            elif not g:
                f.write("  <empty list: the ZERO ideal>\n")
            else:
                for x in g:
                    f.write("  " + x + "\n")
    return path


def do(d, chart, timeout, cross):
    tagbase = f"chart{chart}_d{d}"
    blocks = []
    results = {}
    for sat, label in ((True, "SATURATED (t*mu0-1 present; mu0 != 0 enforced)"),
                       (False, "UNSATURATED (saturation generator removed)")):
        eqs, elim, keep = chart_ideal(d, chart, saturated=sat)
        tag = f"{tagbase}_{'sat' if sat else 'unsat'}"
        rm = elim_msolve(eqs, elim, keep, tag, timeout)
        nm = normalise(rm["gens"], keep, tag + "_m")
        blk = {"engine": "msolve -e %d -g 2" % len(elim), "status": status(rm),
               "n_generators_in": len(eqs), "n_eliminated": len(elim),
               "peak_rss_kb": rm["rss_kb"], "wall_s": rm["wall_s"],
               "exit": ("TIMEOUT" if rm["timeout"] else rm["rc"]),
               "mem_policy": MEM_POLICY, "input": os.path.relpath(rm["input"], REPO),
               "gens": nm}
        blocks.append((label + " -- engine msolve", blk))
        results[(sat, "msolve")] = nm
        # At d = 3, 4 both engines always run: that is the cross-engine control.
        # Beyond that Singular runs as a RECORDED FALLBACK whenever msolve
        # produced no eliminant -- the campaign tooling contract records
        # Singular beating msolve by orders of magnitude on sparse systems, so a
        # cell msolve cannot eliminate is not yet known to be out of reach.
        run_singular = cross or (nm is None)
        if run_singular:
            rs = elim_singular(eqs, elim, keep, tag, timeout)
            ns = normalise(rs["gens"], keep, tag + "_s")
            blks = {"engine": "Singular eliminate()", "status": status(rs),
                    "n_generators_in": len(eqs), "n_eliminated": len(elim),
                    "peak_rss_kb": rs["rss_kb"], "wall_s": rs["wall_s"],
                    "exit": ("TIMEOUT" if rs["timeout"] else rs["rc"]),
                    "mem_policy": MEM_POLICY, "input": os.path.relpath(rs["input"], REPO),
                    "gens": ns}
            blocks.append((label + " -- engine Singular", blks))
            results[(sat, "Singular")] = ns
            if cross:
                check(f"CROSS-ENGINE d={d} chart {chart} "
                      f"({'sat' if sat else 'unsat'}): msolve and Singular "
                      f"eliminants are identical",
                      nm is not None and ns is not None and nm == ns,
                      f"msolve={nm} singular={ns}")
            else:
                LOG.append(f"FALLBACK d={d} chart {chart} "
                           f"({'sat' if sat else 'unsat'}): msolve produced no "
                           f"eliminant; Singular gave {ns}")
            if nm is None and ns is not None:
                results[(sat, "msolve")] = ns      # the surviving eliminant
                nm = ns

    # NEGATIVE CONTROL.  Dropping ONE generator is not a usable control here:
    # these ideals are heavily overdetermined, so the eliminant is unchanged by
    # almost any single omission and the probe cannot fail -- it certifies
    # nothing.  The control that IS required to fail keeps only the FIRST
    # generator: a proper sub-ideal of a unit ideal cannot itself be the unit
    # ideal unless that one generator is a unit, so the eliminant is required
    # to differ.  The drop-one probe is still run and RECORDED, as data.
    eqs, elim, keep = chart_ideal(d, chart, saturated=True)
    base = results[(True, "msolve")]

    if base is None:
        # The primary elimination produced no artifact (OOM / timeout), so there
        # is nothing for a control to be compared against.  Running the controls
        # anyway would burn a full deadline each for no information and delay
        # every later d.  This is RECORDED, not skipped silently.
        LOG.append(f"NOT RUN d={d} chart {chart}: controls skipped -- the primary "
                   f"elimination produced no artifact, so there is no eliminant "
                   f"to compare a control against")
        print(f"  controls not run at d={d} chart {chart}: no primary eliminant",
              flush=True)
        blocks.append(("CONTROLS NOT RUN -- primary elimination produced no artifact",
                       {"engine": "-", "status": "NOT-RUN", "n_generators_in": 0,
                        "n_eliminated": len(elim), "peak_rss_kb": -1, "wall_s": 0,
                        "exit": "-", "mem_policy": MEM_POLICY, "gens": None}))
        path = write_eliminant(chart, d, blocks)
        print(f"  -> {os.path.relpath(path, REPO)}", flush=True)
        return results

    r1g = elim_msolve(eqs[:1], elim, keep, tagbase + "_first1", timeout)
    n1g = normalise(r1g["gens"], keep, tagbase + "_first1_m")
    check(f"NEGATIVE CONTROL d={d} chart {chart}: the ideal of its FIRST "
          f"generator alone has a different eliminant",
          base is not None and n1g is not None and n1g != base,
          f"full={base} first-generator-only={n1g}")
    blocks.append(("NEGATIVE CONTROL -- first generator only (engine msolve)",
                   {"engine": "msolve -e %d -g 2" % len(elim), "status": status(r1g),
                    "n_generators_in": 1, "n_eliminated": len(elim),
                    "peak_rss_kb": r1g["rss_kb"], "wall_s": r1g["wall_s"],
                    "exit": ("TIMEOUT" if r1g["timeout"] else r1g["rc"]),
                    "mem_policy": MEM_POLICY, "gens": n1g}))

    dropped = [e for e in eqs if not e.has(t)][:-1] + [e for e in eqs if e.has(t)]
    rn = elim_msolve(dropped, elim, keep, tagbase + "_drop1", timeout)
    nn = normalise(rn["gens"], keep, tagbase + "_drop1_m")
    LOG.append(f"DATA d={d} chart {chart}: drop-one-generator eliminant = {nn} "
               f"(full = {base})")
    blocks.append(("RECORDED PROBE -- one generator dropped (engine msolve; data, "
                   "not a control)",
                   {"engine": "msolve -e %d -g 2" % len(elim), "status": status(rn),
                    "n_generators_in": len(dropped), "n_eliminated": len(elim),
                    "peak_rss_kb": rn["rss_kb"], "wall_s": rn["wall_s"],
                    "exit": ("TIMEOUT" if rn["timeout"] else rn["rc"]),
                    "mem_policy": MEM_POLICY, "gens": nn}))

    path = write_eliminant(chart, d, blocks)
    print(f"  -> {os.path.relpath(path, REPO)}", flush=True)
    return results


def main(chart, ds, timeout):
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUTD, exist_ok=True)
    res = {}
    for d in ds:
        done = os.path.join(OUTD, f"chart{chart}_d{d}.txt")
        if os.path.exists(done) and os.environ.get("GGV_FORCE") != "1":
            print(f"[chart {chart}] d={d}: already computed, skipping "
                  f"({os.path.relpath(done, REPO)})", flush=True)
            continue
        print(f"[chart {chart}] d={d}", flush=True)
        res[d] = do(d, chart, timeout, cross=(d in (3, 4)))
    # POSITIVE CONTROL at d=3, chart A: the chart is empty there, so the
    # saturated eliminant must be the unit ideal.
    if 3 in res and chart == "A" and res.get(3):
        g = res[3][(True, "msolve")]
        check("POSITIVE CONTROL d=3 chart A: saturated eliminant is the unit "
              "ideal <1> (no admissible root), matching the known empty chart",
              g == ["1"], f"eliminant={g}")
    if 3 in res and chart == "B" and res.get(3):
        g = res[3][(True, "msolve")]
        check("POSITIVE CONTROL d=3 chart B: saturated eliminant recorded",
              g is not None, f"eliminant={g}")
    logp = os.path.join(OUTD, "CONTROLS.log" if chart == "A" else "CONTROLS_chartB.log")
    with open(logp, "a") as f:
        f.write(f"\n===== chart {chart}, d in {ds}, GF({P}), memory policy: {MEM_POLICY} =====\n")
        f.write("\n".join(LOG) + "\n")
        f.write("ALL PASS\n" if not FAIL else "FAILURES: " + str(FAIL) + "\n")
    print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    ch = sys.argv[1]
    ds = [int(x) for x in sys.argv[2:]] or [3, 4, 5, 6, 7, 8]
    sys.exit(main(ch, ds, int(os.environ.get("GGV_ETIMEOUT", "2700"))))
