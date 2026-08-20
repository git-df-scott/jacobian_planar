#!/usr/bin/env python3
"""Assemble ggv/GGV_REPORT.md from the campaign's artifacts.  TABLES ONLY.

This script reads artifacts and tabulates them.  It performs no mathematics,
draws no conclusions, and contains no interpretation of the recorded data.
"""
import glob, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(REPO, "ggv")

def rd(p):
    return open(p).read() if os.path.exists(p) else ""

def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)

def mb(kb):
    try:
        kb = int(kb)
    except (TypeError, ValueError):
        return "n/a"
    return "n/a" if kb < 0 else f"{kb/1024:.0f}"

def sec_gate():
    log = rd(os.path.join(G, "logs", "GATE.log"))
    rows = []
    for line in log.splitlines():
        m = re.match(r"(PASS|FAIL) (.*?)(   \[(.*)\])?$", line.strip())
        if m:
            rows.append([m.group(1), m.group(2).strip(), (m.group(4) or "").strip()])
    return "## Gate (run before every computation)\n\n" + \
           table(["result", "check", "recorded detail"], rows) + \
           "\n\nArtifact: `ggv/logs/GATE.log`\n"

def sec_ladder():
    p = os.path.join(G, "ladder.tsv")
    if not os.path.exists(p):
        return "## G1 ladder\n\nNo `ggv/ladder.tsv` present.\n"
    lines = [l.rstrip("\n").split("\t") for l in open(p) if l.strip()]
    hdr, body = lines[0], lines[1:]
    ix = {h: i for i, h in enumerate(hdr)}
    rows = []
    for r in body:
        rows.append([r[ix["d"]], r[ix["chart"]], r[ix["prime"]], r[ix["verdict"]],
                     r[ix["exit"]], mb(r[ix["peak_rss_kb"]]), r[ix["wall_s"]],
                     r[ix["timeout_s"]], r[ix["mem_policy"]],
                     r[ix["out_bytes"]],
                     "`%s`" % r[ix["output"]] if r[ix["output"]] else "-",
                     "`%s`" % r[ix["P1_output"]] if r[ix["P1_output"]] else "-"])
    counts = {}
    for r in body:
        counts[r[ix["verdict"]]] = counts.get(r[ix["verdict"]], 0) + 1
    s = "## G1 -- ladder d = 8..12, reduced charts, mod p\n\n"
    s += "Serialized: one msolve process at a time, chart A before chart B.\n"
    s += "`peak RSS` in MiB; `[-1]` output = verdict EMPTY.\n\n"
    s += table(["d", "chart", "prime", "verdict-class", "exit", "peak RSS (MiB)",
                "wall (s)", "timeout (s)", "memory policy", "out bytes",
                "artifact", "-P 1 artifact"], rows)
    s += "\n\nVerdict-class counts: " + \
         ", ".join(f"`{k}` {v}" for k, v in sorted(counts.items())) + "\n"
    s += "\nInputs: `ggv/ms_ladder/`, manifest `ggv/ladder_inputs.json`, "
    s += "generation log `ggv/logs/G1_gen.log`, run log `ggv/logs/G1_ladder.log`.\n"
    return s

def sec_inputs():
    p = os.path.join(G, "ladder_inputs.json")
    if not os.path.exists(p):
        return ""
    m = json.load(open(p))
    rows = []
    for d in sorted(m, key=int):
        for c in sorted(m[d]["charts"]):
            i = m[d]["charts"][c]
            rows.append([d, c, i["n_eqs"], i["n_vars"],
                         i["files"]["1000003"]["bytes"],
                         i["files"]["1000003"]["rows"], m[d]["gen_seconds"]])
    return "### G1 inputs as generated\n\n" + table(
        ["d", "chart", "#eqs", "#vars", "bytes (p=1000003)", "rows written",
         "gen (s)"], rows) + "\n"

def sec_elim(chart, title):
    """Tabulate the per-d eliminant files.

    Each file is a sequence of blocks written as

        ======================================================================
        <block name>
        ======================================================================
        key: value
        ...
        generators:
          <one per line>

    so the block NAME lives between the two rules and must be read from there,
    not from the first line after a naive split on the rule.
    """
    rows = []
    blockre = re.compile(r"={70}\n(.*?)\n={70}\n(.*?)(?=\n={70}|\Z)", re.S)
    for p in sorted(glob.glob(os.path.join(G, "mu_eliminants", f"chart{chart}_d*.txt")),
                    key=lambda x: int(re.search(r"_d(\d+)", x).group(1))):
        d = int(re.search(r"_d(\d+)", p).group(1))
        txt = rd(p)
        for name, blk in blockre.findall(txt):
            f = dict(re.findall(r"^(\w+): (.*)$", blk, re.M))
            gens, ingens = [], False
            for line in blk.splitlines():
                if line.startswith("generators:"):
                    ingens = True
                    continue
                if ingens and line.startswith("  "):
                    gens.append(line.strip())
            if gens == ["<empty list: the ZERO ideal>"]:
                shown, n = "the ZERO ideal <0>", 0
            elif gens == ["<none: run did not produce an artifact>"]:
                shown, n = "no artifact", 0
            else:
                shown, n = "; ".join(gens), len(gens)
            rows.append([d, name.strip(), f.get("status", ""),
                         f.get("n_generators_in", ""), f.get("n_eliminated", ""),
                         mb(f.get("peak_rss_kb")), f.get("wall_s", ""), n,
                         "`" + shown[:110] + "`" if shown else "`<empty>`"])
    if not rows:
        return f"## {title}\n\nNo eliminant artifacts present.\n"
    s = f"## {title}\n\n" + table(
        ["d", "block (gauge / engine / control)", "status", "#gens in",
         "#eliminated", "peak RSS (MiB)", "wall (s)", "#gens out",
         "eliminant"], rows)
    ctl = rd(os.path.join(G, "mu_eliminants",
                          "CONTROLS.log" if chart == "A" else "CONTROLS_chartB.log"))
    crows, notes = [], []
    for line in ctl.splitlines():
        m = re.match(r"(PASS|FAIL) (.*?)(   \[(.*)\])?$", line.strip())
        if m:
            crows.append([m.group(1), m.group(2).strip()[:150],
                          (m.group(4) or "").strip()[:150]])
        elif line.startswith(("DATA ", "NOT RUN ", "FALLBACK ")):
            notes.append(line.strip())
    if crows:
        s += "\n\n### Controls\n\n" + table(["result", "control", "recorded detail"], crows)
    if notes:
        s += "\n\n### Recorded, not a control\n\n```\n" + "\n".join(notes) + "\n```\n"
    s += "\n\nFull exact polynomials and per-block run records: " \
         "`ggv/mu_eliminants/chart%s_d*.txt`\n" % chart
    return s


def sec_recursion():
    p = os.path.join(G, "recursion_table.json")
    if not os.path.exists(p):
        return "## G4\n\nNo `ggv/recursion_table.json` present.\n"
    t = json.load(open(p))["rows"]
    rows = []
    for d in sorted(t, key=int):
        r = t[d]
        rows.append([d, "`" + r["row0_polynomial_in_a2d"] + "`",
                     "`" + r["row0_discriminant"] + "`",
                     "`" + "; ".join(r["row0_roots"]) + "`",
                     r["row1_next_unknown"],
                     "`" + r["row1_linear_coeff_of_next_unknown"] + "`",
                     r["row2_next_unknown"],
                     "`" + r["row2_linear_coeff_of_next_unknown"] + "`"])
    s = "## G4 -- descent-recursion data table, d = 3..10 (no solving)\n\n"
    s += table(["d", "polynomial satisfied by a_{2d}", "discriminant",
                "roots (data)", "row1 next unknown", "row1 linear coeff",
                "row2 next unknown", "row2 linear coeff"], rows)
    ctl = rd(os.path.join(G, "logs", "G4.log"))
    crows = [[m.group(1), m.group(2).strip()[:150], (m.group(4) or "").strip()[:150]]
             for m in (re.match(r"(PASS|FAIL) (.*?)(   \[(.*)\])?$", l.strip())
                       for l in ctl.splitlines()) if m]
    if crows:
        s += "\n\n### Controls\n\n" + table(["result", "check", "recorded detail"], crows)
    s += "\n\nFull rows (each row's complete polynomial and full linear part): " \
         "`ggv/recursion_table.json`\n"
    return s

def sec_g5():
    ctl = rd(os.path.join(G, "g5", "G5_CONTROLS.log"))
    if not ctl:
        return "## G5\n\nNo G5 artifacts present.\n"
    rows = [[m.group(1), m.group(2).strip()[:170], (m.group(4) or "").strip()[:170]]
            for m in (re.match(r"(PASS|FAIL) (.*?)(   \[(.*)\])?$", l.strip())
                      for l in ctl.splitlines()) if m]
    facts = [l for l in ctl.splitlines() if ":" in l and not l.startswith(("PASS", "FAIL"))]
    s = "## G5 -- reproduction of GGV's printed d=3 family through the G2/G3 pipeline\n\n"
    s += table(["result", "check", "recorded detail"], rows)
    s += "\n\n### Recorded run facts\n\n```\n" + "\n".join(facts) + "\n```\n"
    s += "\nInputs and full raw outputs: `ggv/g5/`\n"
    return s

def main():
    parts = [
        "# GGV B=16 evidence campaign -- run record\n",
        "Data only: what ran, on which artifact, its verdict class, its exit "
        "status and its peak resident set size. No interpretation of the "
        "recorded values appears in this file.\n",
        "Engines: msolve 0.10.1 (built from source per the campaign tooling "
        "contract), Singular 4.3.2, sympy 1.14.0. Primes used: 1000003, "
        "1000033, 1000039 (all 1 mod 3). System builder: "
        "`wave5/w5_b16_abel.py::build_system`, charts: "
        "`wave5/w5_b16_reduce.py::reduced_charts`, writer: "
        "`wave5/w5_b16_reduce.py::to_ms`. No equations were re-derived.\n",
        sec_gate(), sec_ladder(), sec_inputs(),
        sec_elim("A", "G2 -- mu-eliminants, chart A (mu2 = 1): constraints on (mu0, mu3)"),
        sec_elim("B", "G3 -- mu-eliminants, chart B (mu2 = 0, mu3 = 1): constraints on mu0"),
        sec_recursion(), sec_g5(),
    ]
    open(os.path.join(G, "GGV_REPORT.md"), "w").write("\n\n".join(parts) + "\n")
    print("wrote ggv/GGV_REPORT.md")

if __name__ == "__main__":
    main()
