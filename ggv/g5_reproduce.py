#!/usr/bin/env python3
"""G5 -- independent reproduction of GGV's printed d=3 solution family through
the G2/G3 elimination machinery.

GGV's Section 3.5 family (q1 monic, deg q1 = 3):
    A  = -mu3^2/4 - (mu3/2) y^3 - y^6/4 ,   q1 = y^3 + mu3 ,
    mu0 = mu1 = mu2 = 0 .
Under the reduced-chart gauge fixing this family lies in CHART B
(mu2 = 0, mu3 = 1), at the point
    a2 = 0, a3 = -1/2, a4 = 0, a5 = 0, a6 = -1/4, b2 = 0, mu0 = 0 .

What this file establishes, all computed:
  (1) that point satisfies EVERY generator of the UNSATURATED chart-B d=3 ideal;
  (2) msolve on the same UNSATURATED input returns a NON-empty variety, i.e.
      the pipeline sees real solutions when they exist (the positive control
      the saturated runs cannot provide);
  (3) NEGATIVE CONTROL: the SAME system with the saturation t*mu0 - 1 restored
      is EMPTY -- the family is excluded exactly because it has mu0 = 0;
  (4) NEGATIVE CONTROL: perturbing the point off the family breaks (1).
  (5) the mu-eliminant of the unsaturated chart-B d=3 ideal, recorded as data.

Inputs and full raw outputs are written to ggv/g5/.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wave5"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w5_b16_reduce import reduced_charts, to_ms
from w5_b16_abel import mu0, mu2, mu3
from sympy import symbols, expand, Rational, Symbol
from g_runner import run
from g23_eliminants import chart_ideal, elim_msolve, normalise, P, WORK

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G5 = os.path.join(REPO, "ggv", "g5")
t = Symbol('t')
FAIL, LOG = [], []

def check(label, cond, note=""):
    line = ("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else "")
    print(line, flush=True)
    LOG.append(line)
    if not cond:
        FAIL.append(label)

def main():
    os.makedirs(G5, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    a = symbols('a0:7'); b = symbols('b0:3')
    # GGV Sec 3.5 family, gauge-fixed into chart B (mu3 = 1, mu2 = 0)
    pt = {a[2]: 0, a[3]: Rational(-1, 2), a[4]: 0, a[5]: 0,
          a[6]: Rational(-1, 4), b[2]: 0, mu0: 0}

    eqs_u, elim_u, keep_u = chart_ideal(3, "B", saturated=False)
    eqs_s, vars_s = reduced_charts(3)["B"]

    # (1) reproduction: the published point satisfies every unsaturated generator
    resid = [expand(e.subs(pt)) for e in eqs_u]
    check("G5(1) GGV Sec 3.5 d=3 family satisfies EVERY generator of the "
          "UNSATURATED chart-B ideal", all(r == 0 for r in resid),
          f"{len(eqs_u)} generators, nonzero residuals: {[str(r) for r in resid if r != 0]}")

    # (4) negative control on the substitution
    bad = dict(pt); bad[a[3]] = Rational(-1, 2) + 1
    resid_b = [expand(e.subs(bad)) for e in eqs_u]
    check("G5(4) NEGATIVE CONTROL: perturbing a3 off the family breaks the ideal",
          any(r != 0 for r in resid_b),
          f"nonzero residuals: {sum(1 for r in resid_b if r != 0)}/{len(resid_b)}")

    # (2) the pipeline sees the solutions: msolve on the unsaturated input
    gens_u = [v for v in vars_s if v != t]
    fin = os.path.join(G5, "g5_d3_B_unsaturated_p%d.ms" % P)
    open(fin, "w").write(to_ms(eqs_u, gens_u, P))
    fout = os.path.join(G5, "g5_d3_B_unsaturated_p%d.out" % P)
    ru = run(fin, fout, timeout=1800)
    check("G5(2) msolve on the UNSATURATED chart-B d=3 input returns a NON-empty "
          "variety", ru["verdict"] != "EMPTY" and ru["out_bytes"] > 0,
          f"verdict={ru['verdict']} exit={ru['exit']} rss_kb={ru['peak_rss_kb']} "
          f"bytes={ru['out_bytes']} wall={ru['wall_s']}s")

    # (3) negative control: saturation restored -> EMPTY
    fin_s = os.path.join(G5, "g5_d3_B_saturated_p%d.ms" % P)
    open(fin_s, "w").write(to_ms(eqs_s, vars_s, P))
    fout_s = os.path.join(G5, "g5_d3_B_saturated_p%d.out" % P)
    rs = run(fin_s, fout_s, timeout=1800)
    check("G5(3) NEGATIVE CONTROL: the SAME system with t*mu0-1 restored is EMPTY",
          rs["verdict"] == "EMPTY",
          f"verdict={rs['verdict']} exit={rs['exit']} rss_kb={rs['peak_rss_kb']} "
          f"bytes={rs['out_bytes']} wall={rs['wall_s']}s")

    # (5) the unsaturated mu-eliminant, as data
    re_ = elim_msolve(eqs_u, elim_u, keep_u, "g5_d3_B_unsat", 1800)
    ne = normalise(re_["gens"], keep_u, "g5_d3_B_unsat_m")
    check("G5(5) unsaturated chart-B d=3 mu-eliminant computed (recorded as data)",
          ne is not None, f"eliminant in mu0: {ne}  peak_rss_kb={re_['rss_kb']}")

    with open(os.path.join(G5, "G5_CONTROLS.log"), "w") as f:
        f.write(f"GGV G5 -- reproduction of the printed d=3 family, GF({P})\n")
        f.write(f"point (chart B gauge, mu3=1, mu2=0): "
                f"{ {str(k): str(v) for k, v in pt.items()} }\n")
        f.write(f"unsaturated generators: {len(eqs_u)}   saturated: {len(eqs_s)}\n")
        f.write(f"unsaturated mu-eliminant: {ne}\n")
        f.write(f"msolve unsaturated: verdict={ru['verdict']} rss_kb={ru['peak_rss_kb']} "
                f"bytes={ru['out_bytes']} artifact={os.path.relpath(fout, REPO)}\n")
        f.write(f"msolve saturated:   verdict={rs['verdict']} rss_kb={rs['peak_rss_kb']} "
                f"bytes={rs['out_bytes']} artifact={os.path.relpath(fout_s, REPO)}\n")
        f.write("\n".join(LOG) + "\n")
        f.write("ALL PASS\n" if not FAIL else "FAILURES: " + str(FAIL) + "\n")
    print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
