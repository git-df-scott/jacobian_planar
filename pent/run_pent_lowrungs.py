"""ITEM 2b, the LOW rungs of the graded ladder.

Emptiness is monotone in the generator set: if the levels-13..J prefix of the
pentagon conditions already has no common zero, the whole system has none.  The
ladder in run_pent_msolve.py starts at J = 18; the rungs below that are far
smaller (levels 13..14 is 3 generators, 13..17 is 15) and are worth trying
first, because a EMPTY there would settle the entire system cheaply.

Each rung is run twice: as exported (two gauges, so the variety carries a
one-dimensional gauge orbit and cannot be zero-dimensional) and with the third
gauge p_1_0 - 1 added.  Peak RSS, exit code and verdict go into the same
RUNLOG.tsv.

A non-EMPTY rung says nothing about emptiness -- only an EMPTY one is
informative, and only in the direction of emptiness.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_pent_msolve as L

if __name__ == "__main__":
    head, char, polys = L.load()
    print(f"  source: {len(polys)} generators")
    new = not os.path.exists(L.RUNLOG)
    fh = open(L.RUNLOG, "a")
    if new:
        fh.write("timestamp\tsystem\tgenerators\tlevels\tgauges\tbytes\tthreads\t"
                 "exit\tseconds\tpeak_rss_kb\tout_bytes\tverdict\thead\n")
    import time
    for J in (14, 15, 16, 17):
        for gauge3 in (True, False):
            n = L.cum(J)
            tag = f"L{J}_{'g3' if gauge3 else 'g2'}"
            ms = os.path.join(HERE, f"pent_{tag}.ms")
            ngen = L.write_prefix(ms, head, char, polys, n, gauge3)
            r = L.run(ms, ms[:-3] + ".out", timeout=1800)
            fh.write("\t".join([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                f"pent_{tag}.ms", str(ngen), f"13..{J}",
                                "3" if gauge3 else "2", str(os.path.getsize(ms)),
                                str(L.CORES), str(r["exit"]), str(r["seconds"]),
                                str(r["peak_rss_kb"]), str(r["out_bytes"]),
                                r["verdict"], r["head"]]) + "\n")
            fh.flush()
            print(f"    pent_{tag}: {r['verdict']}  exit {r['exit']}  "
                  f"{r['seconds']}s  peak {r['peak_rss_kb']} kB", flush=True)
    fh.close()
