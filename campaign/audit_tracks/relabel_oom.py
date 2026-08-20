"""Re-label the two-prime sweep's UNKNOWN verdicts using the repaired engine.

Pass 1 produced 8 UNKNOWNs.  UNKNOWN is not in the engine contract
(EMPTY | NONEMPTY | TIMEOUT | OOM); it was an artefact of trackD_extract.run()
ignoring the subprocess returncode, so an OOM-killed Singular looked like a
successful run that printed nothing.  Diagnosed directly on
    F11(m,n)=2,5 | a=7 b=4 c'=2 r=5
which returns rc = -9 after 281 s with zero stdout and zero stderr, and WITHOUT
Singular's "no more memory" message -- so only the returncode check catches it.

This re-runs each UNKNOWN through the repaired engine and records the real
reason.  It never converts an UNKNOWN into EMPTY on the strength of the old run:
each one is decided by a fresh execution.
"""
import json, os, sys, time, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "trackD_twoprime_state.json")
TARGETS = os.path.join(HERE, "trackD_targets.json")
BUDGET = int(os.environ.get("RELABEL_BUDGET", "420"))


def save(st):
    fd, tmp = tempfile.mkstemp(dir=HERE, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def main():
    os.environ["TRACKD_PRIME"] = "65521"
    import trackD_extract as EX
    st = json.load(open(STATE))
    tg = {t["tag"]: t for t in json.load(open(TARGETS))}
    todo = [k for k, v in st.items() if v["verdict"] == "UNKNOWN"]
    print(f"re-labelling {len(todo)} UNKNOWN targets, budget {BUDGET}s", flush=True)
    for n, tag in enumerate(todo, 1):
        t = tg[tag]
        t0 = time.time()
        r = EX.run(t["NP"], t["NQ"], t["r"], "relabel", timeout=BUDGET)
        out = r.get("out") or ""
        status = r["status"]
        if status == "RAN":
            vd = ("LIVE" if "live component" in out else
                  "EMPTY" if "VERDICT: EMPTY" in out else "UNKNOWN")
        else:
            vd = status                       # OOM / CRASH / TIMEOUT / OOS
        st[tag]["verdict"] = vd
        st[tag]["relabel"] = {"status": status, "rc": r.get("rc"),
                              "secs": round(time.time() - t0),
                              "out": out.replace("\n", " | ")[:200]}
        save(st)
        mark = "   <<< LIVE" if vd == "LIVE" else ""
        print(f"[{n}/{len(todo)}] {vd} rc={r.get('rc')} "
              f"[{time.time()-t0:.0f}s]{mark}\n    {tag[:100]}", flush=True)
    from collections import Counter
    print("TALLY:", dict(Counter(v["verdict"] for v in st.values())), flush=True)


if __name__ == "__main__":
    main()
