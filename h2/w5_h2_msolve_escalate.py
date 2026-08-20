"""
ITEM 3, second engine -- msolve on the above-125 targets Singular cannot decide.

The queue's engine is Singular `facstd`.  At a 90 s cap 14 targets timed out; at
900 s the first two re-run still time out.  msolve implements F4 + FGLM, a
different algorithm with a different memory and time profile, so it is a genuine
second engine rather than a longer run of the first -- the same escalation the
H4 track already uses.

Pipeline: build the ideal exactly as trackD_extract does, print its generators
instead of calling facstd, convert to msolve input (sanitised and validated),
and solve at two compliant primes.  Verdicts are combined without averaging.

CONTROLS
  M1 PARSER, both directions: a unit ideal must read EMPTY and a solvable system
     must read NONEMPTY.
  M2 CROSS-ENGINE: a target Singular already decided EMPTY must read EMPTY here.
  M3 NEGATIVE: with the two Rabinowitsch non-degeneracy generators removed, the
     same target must NOT read EMPTY (the all-zero point survives).
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "campaign", "audit_tracks"))
sys.path.insert(0, os.path.join(ROOT, "wave4"))
import trackD_extract as EX
import w4_msformat as MF
import w4_run as RUN

PRIMES = [65521, 65539]
RAB = re.compile(r"^\s*I\s*=\s*I\s*\+\s*ideal\(\s*[a-zA-Z]\w*\s*\*\s*\w+\s*-\s*1\s*\)\s*;\s*$")
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def dump_generators(src, budget=1200):
    lines = []
    for l in src.splitlines():
        if l.strip().startswith("list LL = facstd(I)"):
            lines.append('int gi; for (gi=1; gi<=size(I); gi++) { "GEN", I[gi]; }')
            lines.append("quit;")
            break
        lines.append(l)
    fn = os.path.join(EX.SCRATCH, "h2gen.sing")
    os.makedirs(EX.SCRATCH, exist_ok=True)
    open(fn, "w").write("\n".join(lines))
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        return None
    gens, cur = [], None
    for ln in pr.stdout.splitlines():
        if ln.startswith("GEN "):
            if cur is not None:
                gens.append(cur)
            cur = ln[4:].strip()
        elif cur is not None and ln.strip() and not ln.startswith("//"):
            cur += ln.strip()
    if cur is not None:
        gens.append(cur)
    return [g for g in gens if g and g != "0"]


def to_ms(gens, p, path):
    names = sorted({v for g in gens for v in re.findall(r"[A-Za-z]\w*", g)})
    conv = [re.sub(r"c\((\d+)\)", r"c\1", g) for g in gens]
    names = sorted({v for g in conv for v in re.findall(r"[A-Za-z]\w*", g)})
    lines = MF.sanitize_lines(conv, p)
    open(path, "w").write(",".join(names) + "\n" + f"{p}\n" + ",\n".join(lines) + "\n")
    probs = MF.validate(path)
    if probs:
        raise SystemExit(f"{path}: {probs[:3]}")
    return names


def solve(gens, p, tag, timeout=1800):
    path = os.path.join(EX.SCRATCH, f"h2ms_{tag}_{p}.ms")
    names = to_ms(gens, p, path)
    r = RUN.run_msolve(path, path[:-3] + ".out", timeout=timeout, threads=1)
    return r, len(names)


def main():
    targets = json.load(open(os.path.join(HERE, "trackD_targets.json")))
    state = json.load(open(os.path.join(HERE, "h2_state.json")))
    print("=" * 78)
    print("ITEM 3 second engine -- msolve on the above-125 queue")
    print("=" * 78)
    # M1
    open(os.path.join(EX.SCRATCH, "u.ms"), "w").write("x,y\n65521\nx,\ny,\nx+y+1\n")
    open(os.path.join(EX.SCRATCH, "s.ms"), "w").write("x,y\n65521\nx*y+65520,\nx+65520*y\n")
    ru = RUN.run_msolve(os.path.join(EX.SCRATCH, "u.ms"),
                        os.path.join(EX.SCRATCH, "u.out"), timeout=120, threads=1)
    rs = RUN.run_msolve(os.path.join(EX.SCRATCH, "s.ms"),
                        os.path.join(EX.SCRATCH, "s.out"), timeout=120, threads=1)
    check("M1a parser: a unit ideal reads EMPTY", ru["verdict"] == "EMPTY",
          ru["verdict"])
    check("M1b parser: a solvable system does NOT read EMPTY",
          rs["verdict"] != "EMPTY", rs["verdict"])
    # M2 / M3 on a target Singular decided EMPTY
    dec = [t for t in targets if state.get(t["tag"], {}).get("verdict") == "EMPTY"]
    tod = [t for t in targets if state.get(t["tag"], {}).get("verdict") == "TIMEOUT"]
    print(f"    targets: {len(targets)}; Singular-EMPTY {len(dec)}; "
          f"Singular-TIMEOUT {len(tod)}")
    if dec:
        src, info = EX.build_singular(dec[0]["NP"], dec[0]["NQ"], dec[0]["r"], name="x")
        g = dump_generators(src)
        r, nv = solve(g, PRIMES[0], "ctl")
        check("M2 CROSS-ENGINE: msolve agrees with Singular's EMPTY on a decided "
              "target", r["verdict"] == "EMPTY",
              f"{r['verdict']} in {r['seconds']}s over {nv} variables")
        gnos = [x for x in g]
        src2 = "\n".join(l for l in src.splitlines() if not RAB.match(l))
        g2 = dump_generators(src2)
        r2, nv2 = solve(g2, PRIMES[0], "ctl_nosat")
        check("M3 NEGATIVE: with the non-degeneracy generators removed msolve "
              "does NOT say EMPTY", r2["verdict"] != "EMPTY",
              f"{r2['verdict']}")
    out = {}
    for t in tod:
        per = {}
        for p in PRIMES:
            os.environ["TRACKD_PRIME"] = str(p)
            for m in [k for k in list(sys.modules) if k.startswith("trackD_extract")]:
                del sys.modules[m]
            import trackD_extract as EX2
            src, info = EX2.build_singular(t["NP"], t["NQ"], t["r"], name="e")
            if src is None:
                per[p] = "OOS"
                continue
            g = dump_generators(src)
            if not g:
                per[p] = "BUILD-FAIL"
                continue
            r, nv = solve(g, p, "t" + str(abs(hash(t["tag"])) % 10 ** 6))
            per[p] = r["verdict"]
            print(f"    {t['tag'][:52]}  p={p}  {r['verdict']}  {r['seconds']}s  "
                  f"rss={r['peak_rss_kb_children']}kB", flush=True)
        vs = set(per.values())
        comb = ("DISAGREE" if ("EMPTY" in vs and
                               any(v in ("NONEMPTY-PARAMETRIZATION",
                                         "POSITIVE-DIMENSIONAL") for v in vs))
                else (list(vs)[0] if len(vs) == 1 else "MIXED"))
        out[t["tag"]] = {"per_prime": per, "combined": comb, "max": t.get("max")}
        json.dump(out, open(os.path.join(HERE, "h2_msolve_results.json"), "w"),
                  indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} controls passed;  "
          f"{sum(1 for v in out.values() if v['combined'] == 'EMPTY')} of "
          f"{len(out)} Singular-TIMEOUT targets decided EMPTY by msolve")
    print("=" * 78)


if __name__ == "__main__":
    main()
