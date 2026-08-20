"""Crash-safe, resumable driver for the Track D elimination queue.

Why this exists: the previous runs lost work twice.  trackD_solve.py wrote its
results only after each target but re-ran the whole list from the start, and
trackD_queue150.py wrote trackD_targets.json only at the very end -- so when
the container was reclaimed mid-run, the queue's work vanished entirely.

Design:

  * ONE state file, trackD_state.json, keyed by target tag.  Written after
    EVERY target with an atomic replace, so a kill at any instant loses at
    most the target in flight.
  * Resumption is the default: targets already carrying a terminal verdict
    (EMPTY / LIVE) are skipped.  TIMEOUTs are retried only when the new
    budget is larger than the one that produced them, which is recorded.
  * A supervisor loop restarts the worker if it dies.  That covers a dropped
    process; it CANNOT cover a container reset, which kills the supervisor
    too -- only an external scheduled trigger can, and that is a separate
    mechanism, deliberately not pretended at here.

Usage:
    python3 trackD_resume.py [budget_secs] [--supervise] [--commit]

--commit makes it git-commit the state file every COMMIT_EVERY targets, so
progress survives even if the working tree is lost with the container.
"""
import json, os, sys, time, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "trackD_state.json")
TARGETS = os.path.join(HERE, "trackD_targets.json")
COMMIT_EVERY = 10


def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE))
        except Exception:
            pass
    return {}


def save_state(st):
    """Atomic: write to a temp file in the same dir, then replace."""
    fd, tmp = tempfile.mkstemp(dir=HERE, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def classify(out):
    if "live component" in out:
        return "LIVE"
    if "VERDICT: EMPTY" in out:
        return "EMPTY"
    return "UNKNOWN"


def todo(targets, st, budget):
    out = []
    for t in targets:
        rec = st.get(t["tag"])
        if rec is None:
            out.append(t)
        elif rec["verdict"] in ("EMPTY", "LIVE"):
            continue                      # terminal, never redo
        elif rec["verdict"] == "TIMEOUT" and budget > rec.get("budget", 0):
            out.append(t)                 # retry only with a bigger budget
    # cheapest first: parameter count is the best predictor we have
    out.sort(key=lambda t: (t.get("params", 10**6), t.get("size", 0)))
    return out


def commit(msg):
    try:
        subprocess.run(["git", "add", "trackD_state.json", "trackD_targets.json"],
                       cwd=HERE, capture_output=True, timeout=60)
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=HERE,
                       capture_output=True, timeout=60)
        for k in range(4):
            r = subprocess.run(["git", "push", "-u", "origin",
                                "claude/counter-example-audit-dnu9l9"],
                               cwd=HERE, capture_output=True, timeout=180)
            if r.returncode == 0:
                return True
            time.sleep(2 ** (k + 1))
    except Exception:
        pass
    return False


def work(budget, do_commit):
    import trackD_extract as EX
    targets = json.load(open(TARGETS))
    st = load_state()
    queue = todo(targets, st, budget)
    done_terminal = sum(1 for v in st.values() if v["verdict"] in ("EMPTY", "LIVE"))
    print(f"targets {len(targets)}  terminal {done_terminal}  queue {len(queue)} "
          f"  budget {budget}s", flush=True)
    n = 0
    for t in queue:
        t0 = time.time()
        r = EX.run(t["NP"], t["NQ"], t["r"], "resume", timeout=budget)
        if r["status"] == "TIMEOUT":
            verdict, out = "TIMEOUT", ""
        else:
            out = r.get("out") or ""
            verdict = classify(out)
        st[t["tag"]] = {"verdict": verdict, "max": t.get("max"),
                        "params": t.get("params"), "tier": t.get("tier", "?"),
                        "budget": budget, "secs": round(time.time() - t0),
                        "out": out.replace("\n", " | ")[:400]}
        save_state(st)
        n += 1
        mark = "  <<< LIVE COMPONENT" if verdict == "LIVE" else ""
        print(f"[{n}/{len(queue)}] max={t.get('max')} params={t.get('params')} "
              f"{verdict} [{time.time()-t0:.0f}s]{mark}", flush=True)
        print(f"    {t['tag'][:100]}", flush=True)
        if verdict == "LIVE":
            print("    " + out.replace("\n", "\n    "), flush=True)
            if do_commit:
                commit("LIVE COMPONENT FOUND -- see trackD_state.json")
        if do_commit and n % COMMIT_EVERY == 0:
            commit(f"trackD_resume: {n} targets processed this pass")
    if do_commit:
        commit(f"trackD_resume: pass complete, {n} targets processed")
    return n


def tally():
    st = load_state()
    c = {}
    for v in st.values():
        c[v["verdict"]] = c.get(v["verdict"], 0) + 1
    return c


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    budget = int(args[0]) if args else 300
    do_commit = "--commit" in sys.argv
    if "--tally" in sys.argv:
        targets = json.load(open(TARGETS))
        print(f"targets {len(targets)}   " +
              "  ".join(f"{k} {v}" for k, v in sorted(tally().items())))
        sys.exit(0)
    if "--supervise" in sys.argv:
        # restart the worker if it dies; a container reset kills this too
        while True:
            try:
                left = work(budget, do_commit)
            except Exception as ex:
                print(f"worker died: {type(ex).__name__}: {ex}; restarting",
                      flush=True)
                time.sleep(5)
                continue
            if left == 0:
                print("[queue exhausted]", flush=True)
                break
    else:
        work(budget, do_commit)
    print("TALLY: " + "  ".join(f"{k} {v}" for k, v in sorted(tally().items())),
          flush=True)
