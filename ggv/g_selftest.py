#!/usr/bin/env python3
"""Self-test of the G1 ladder driver's control flow, with a STUB engine.

The driver decides what gets recorded and what gets re-run.  Those decisions
are tested here directly, by replacing ggv/g_runner.run with a stub, so the
tests need no msolve process and cannot disturb a real run.  Each property
below is a defect that was actually present and is now fixed:

  T1  every cell produces exactly one row -- including failure classes.
  T2  a cell whose launch RAISES is recorded as RUN-ERROR and the ladder
      CONTINUES; previously the exception escaped and silently dropped that
      cell and every later cell from the table.
  T3  the -P 1 follow-up fires for CANDIDATE-UNVERIFIED ...
  T4  ... and NOT for TIMEOUT / STALLED-OOM / CRASH / NO-OUTPUT, which have no
      artifact to parametrize; previously it fired there too, burning a second
      full deadline per failed cell for no information.
  T5  a 0-byte artifact is deleted, never left on disk to be committed as if
      it were a result, and its row's output column is blank.
  T6  restarting the ladder RESUMES: recorded cells are not re-run and rows
      are not duplicated.
  T7  NEGATIVE CONTROL on this very test file: a stub that returns EMPTY for a
      cell the table says is CANDIDATE-UNVERIFIED must make T3 fail.  Without
      it, T3 would pass against a driver that fired -P 1 unconditionally.
"""
import os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FAIL = []

def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else ""))
    if not cond:
        FAIL.append(label)


def make_rec(verdict, out_bytes, out_path):
    return {"input": "in", "output": out_path, "args": "-", "exit": "0",
            "wall_s": 0.0, "peak_rss_kb": 123, "mem_policy": "stub",
            "timeout_s": 1, "in_bytes": 10, "out_bytes": out_bytes,
            "verdict": verdict, "stderr_tail": ""}


def drive(plan, tmp, ds=(8,), reuse_tsv=None):
    """Run the driver with a stub engine.  `plan` maps a cell key to a verdict
    string, the literal 'RAISE', or a callable."""
    import g1_ladder, g_runner
    msdir = os.path.join(tmp, "ms"); outdir = os.path.join(tmp, "out")
    os.makedirs(msdir, exist_ok=True); os.makedirs(outdir, exist_ok=True)
    tsv = reuse_tsv or os.path.join(tmp, "ladder.tsv")
    for d in ds:
        for c in ("A", "B"):
            for p in g1_ladder.PRIMES:
                open(os.path.join(msdir, f"b16r_d{d}_{c}_p{p}.ms"), "w").write("x\n2\nx\n")
    g1_ladder.MSDIR, g1_ladder.OUTDIR, g1_ladder.TSV = msdir, outdir, tsv
    calls = []

    def stub(ms_in, out_path, extra_args=(), timeout=None):
        calls.append((os.path.basename(ms_in), tuple(extra_args)))
        key = os.path.basename(ms_in).replace(".ms", "")
        want = plan.get(key, "EMPTY")
        if want == "RAISE":
            raise RuntimeError("stub launch failure")
        if want == "EMPTY":
            open(out_path, "w").write("[-1]:\n")
            return make_rec("EMPTY", 6, out_path)
        if want == "CANDIDATE-UNVERIFIED":
            open(out_path, "w").write("[0, [2, 1, ...]]:\n")
            return make_rec("CANDIDATE-UNVERIFIED", 20, out_path)
        open(out_path, "wb").close()          # failure classes leave 0 bytes
        return make_rec(want, 0, out_path)

    g1_ladder.run = stub
    g1_ladder.main(list(ds), timeout=1)
    rows = [l.rstrip("\n").split("\t") for l in open(tsv) if l.strip()]
    g1_ladder.run = g_runner.run
    return rows[0], rows[1:], calls, outdir, tsv


def main():
    tmp = tempfile.mkdtemp(prefix="ggvself")
    try:
        plan = {
            "b16r_d8_A_p1000003": "TIMEOUT",
            "b16r_d8_A_p1000033": "STALLED-OOM",
            "b16r_d8_A_p1000039": "CRASH",
            "b16r_d8_B_p1000003": "CANDIDATE-UNVERIFIED",
            "b16r_d8_B_p1000033": "RAISE",
            "b16r_d8_B_p1000039": "EMPTY",
        }
        hdr, rows, calls, outdir, tsv = drive(plan, tmp)
        ix = {h: i for i, h in enumerate(hdr)}
        got = {(r[ix["chart"]], r[ix["prime"]]): r for r in rows}

        check("T1 every cell produced exactly one row", len(rows) == 6,
              f"rows={len(rows)} cells=6")
        check("T2 a raising cell is recorded RUN-ERROR and the ladder continues",
              got[("B", "1000033")][ix["verdict"]] == "RUN-ERROR"
              and ("B", "1000039") in got,
              f"verdict={got[('B','1000033')][ix['verdict']]}, "
              f"later cell present={('B','1000039') in got}")

        p1_for = {c[0].replace(".ms", "") for c in calls if c[1] == ("-P", "1")}
        check("T3 -P 1 fires for the CANDIDATE-UNVERIFIED cell",
              "b16r_d8_B_p1000003" in p1_for, f"p1_for={sorted(p1_for)}")
        check("T4 -P 1 does NOT fire for TIMEOUT / STALLED-OOM / CRASH",
              p1_for == {"b16r_d8_B_p1000003"}, f"p1_for={sorted(p1_for)}")

        left = sorted(os.listdir(outdir))
        zero = [f for f in left if os.path.getsize(os.path.join(outdir, f)) == 0]
        check("T5 no 0-byte artifact is left on disk", not zero, f"zero-byte={zero}")
        check("T5 a failed cell's output column is blank",
              got[("A", "1000003")][ix["output"]] == "",
              f"output={got[('A','1000003')][ix['output']]!r}")

        hdr2, rows2, calls2, _, _ = drive(plan, tmp, reuse_tsv=tsv)
        check("T6 restart re-runs nothing", not calls2, f"calls={calls2}")
        check("T6 restart duplicates no row", len(rows2) == 6, f"rows={len(rows2)}")

        # T7 NEGATIVE CONTROL on the test itself
        tmp2 = tempfile.mkdtemp(prefix="ggvself2")
        try:
            flat = dict(plan); flat["b16r_d8_B_p1000003"] = "EMPTY"
            _, _, calls3, _, _ = drive(flat, tmp2)
            p1_3 = {c[0] for c in calls3 if c[1] == ("-P", "1")}
            check("T7 NEGATIVE CONTROL: with no CANDIDATE-UNVERIFIED cell, "
                  "-P 1 fires for nothing (so T3 can fail)", not p1_3,
                  f"p1_for={sorted(p1_3)}")
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
