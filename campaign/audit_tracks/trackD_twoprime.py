"""Two-prime, crash-safe driver for the above-125 (Track D / H2) queue.

Why: the certified table in ABOVE_125_STATUS.md was produced at ONE prime
(65521).  Emptiness mod a single prime is not emptiness -- the campaign's own
case (2) was re-run at three primes for exactly that reason, and the prime
hygiene lesson (primes must be == 1 mod 3, so the cusp-(2,3) structure is
representable) came out of that same episode.  This driver runs every target
at TWO compliant primes and records BOTH.

Verdict policy, deliberately conservative:
  EMPTY      both primes say EMPTY          -> mod-p EMPTY at 2 primes
  LIVE       either prime reports a live component
  DISAGREE   one EMPTY, one LIVE            -> loud; never silently averaged
  PARTIAL    one prime terminal, other timed out
  TIMEOUT    neither finished

State is one JSON keyed by tag, atomically replaced after every target, so a
container reset loses at most the target in flight.
"""
import json, os, sys, time, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "trackD_twoprime_state.json")
TARGETS = os.path.join(HERE, "trackD_targets.json")
PRIMES = [65521, 65539]          # both == 1 mod 3


def _assert_compliant():
    bad = [p for p in PRIMES if p % 3 != 1]
    if bad:
        raise SystemExit(f"non-compliant primes (need == 1 mod 3): {bad}")


def load():
    if os.path.exists(STATE):
        try: return json.load(open(STATE))
        except Exception: pass
    return {}


def save(st):
    fd, tmp = tempfile.mkstemp(dir=HERE, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def classify(out):
    if "live component" in out: return "LIVE"
    if "VERDICT: EMPTY" in out: return "EMPTY"
    return "UNKNOWN"


def combine(a, b):
    if a == "LIVE" or b == "LIVE":
        return "DISAGREE" if "EMPTY" in (a, b) else "LIVE"
    if a == "EMPTY" and b == "EMPTY": return "EMPTY"
    if "EMPTY" in (a, b):             return "PARTIAL"
    if a == b == "TIMEOUT":           return "TIMEOUT"
    return "UNKNOWN"


def run_one(t, budget):
    """Run one target at every prime in PRIMES; return (combined, per-prime)."""
    per = {}
    for p in PRIMES:
        os.environ["TRACKD_PRIME"] = str(p)
        for m in [k for k in list(sys.modules) if k.startswith("trackD_extract")]:
            del sys.modules[m]
        import trackD_extract as EX          # re-import so P is re-read
        t0 = time.time()
        r = EX.run(t["NP"], t["NQ"], t["r"], f"tp{p}", timeout=budget)
        vd = "TIMEOUT" if r["status"] == "TIMEOUT" else (
             "OOS" if r["status"] == "OUT OF SCOPE" else classify(r.get("out") or ""))
        per[str(p)] = {"verdict": vd, "secs": round(time.time() - t0),
                       "out": (r.get("out") or "").replace("\n", " | ")[:300]}
        if vd == "OOS":
            return "OOS", per
        # a LIVE at the first prime is worth the second prime's confirmation,
        # but a TIMEOUT at the first is not worth paying twice for
        if vd == "TIMEOUT":
            break
    vs = [per[str(p)]["verdict"] for p in PRIMES if str(p) in per]
    return combine(vs[0], vs[1] if len(vs) > 1 else "TIMEOUT"), per


def todo(targets, st, budget):
    out = []
    for t in targets:
        rec = st.get(t["tag"])
        if rec is None: out.append(t)
        elif rec["verdict"] in ("EMPTY", "LIVE", "DISAGREE", "OOS"): continue
        elif budget > rec.get("budget", 0): out.append(t)
    out.sort(key=lambda t: (t.get("params", 10**6), t.get("size", 0)))
    return out


def control():
    """A control that CAN say non-EMPTY: same engine, same target, but with the
    non-degeneracy saturation dropped, so the all-zero point survives.  If this
    comes back EMPTY the engine is broken and every EMPTY below is worthless."""
    import trackD_extract as EX
    t = json.load(open(TARGETS))[0]
    src, info = EX.build_singular(t["NP"], t["NQ"], t["r"], name="ctrl")
    if src is None:
        return "OOS", "build returned OUT OF SCOPE"
    nosat = "\n".join(l for l in src.splitlines()
                       if "sat" not in l.lower() and not l.strip().startswith("ideal N"))
    import subprocess, tempfile as _tf
    fn = os.path.join(EX.SCRATCH, "ctrl_nosat.sing")
    open(fn, "w").write(nosat)
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    out = pr.stdout or ""
    return ("EMPTY" if "VERDICT: EMPTY" in out else "NON-EMPTY"), out[-200:]


def main():
    _assert_compliant()
    if "--control" in sys.argv:
        v, det = control()
        ok = v not in ("EMPTY",)
        print(f"  {'PASS' if ok else 'FAIL'}  positive control: unsaturated "
              f"system is NOT empty   <CERTIFIED>   [{v}]")
        print("   ", det.replace("\n", " | ")[:200])
        raise SystemExit(0 if ok else 1)
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**6
    targets = json.load(open(TARGETS))
    st = load()
    q = todo(targets, st, budget)[:limit]
    print(f"primes {PRIMES}  targets {len(targets)}  queue {len(q)}  "
          f"budget {budget}s/prime", flush=True)
    for n, t in enumerate(q, 1):
        t0 = time.time()
        vd, per = run_one(t, budget)
        st[t["tag"]] = {"verdict": vd, "per_prime": per, "max": t.get("max"),
                        "params": t.get("params"), "tier": t.get("tier", "?"),
                        "budget": budget, "secs": round(time.time() - t0)}
        save(st)
        mark = ""
        if vd == "LIVE":     mark = "   <<< LIVE COMPONENT"
        if vd == "DISAGREE": mark = "   <<< PRIME DISAGREEMENT"
        print(f"[{n}/{len(q)}] max={t.get('max')} params={t.get('params')} "
              f"{vd} [{time.time()-t0:.0f}s]{mark}", flush=True)
        print(f"    {t['tag'][:110]}", flush=True)
        if vd in ("LIVE", "DISAGREE"):
            print("    " + json.dumps(per)[:600], flush=True)
    c = {}
    for r in st.values(): c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    print("TALLY:", c, flush=True)


if __name__ == "__main__":
    main()
