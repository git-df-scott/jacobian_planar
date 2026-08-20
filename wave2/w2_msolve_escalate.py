#!/usr/bin/env python3
"""H4 rung 2 -- route the deg_y=3 slice systems to msolve (F4/FGLM).

Session 35's own close-out names this exact escalation:

    "The boundary is now RAM, so a bigger machine or an F4/FGLM engine buys
     degrees directly."

Singular's slimgb ran out of MEMORY (not time) on
    k=4 h=t deg<=6,  k=5 h=t deg<=4,  k=5 h=t deg<=5,  k=6 h=t deg<=4
and those cells are recorded UNRESOLVED.  msolve 0.10.1 implements F4 + FGLM,
a different algorithm with a different memory profile, so it is a genuine
second engine rather than a longer run of the first.

Pipeline: build the ideal in Singular exactly as Session 35 does, but instead
of calling slimgb, PRINT the generators; convert to msolve's input format;
solve.  msolve's -g 2 reports the dimension, and an empty variety is reported
as such.
"""
import os, re, sys, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("W2_SCRATCH", os.path.join(HERE, "_scratch"))
os.makedirs(SCRATCH, exist_ok=True)
CERT = os.path.abspath(os.path.join(HERE, "..", "campaign", "moduli_phase2",
                                    "phase2_moduli", "certify"))
src = open(os.path.join(CERT, "session35_singular_modular_push.py")).read()
ns = {}
exec(compile(src[src.index("def hbranch_code"):src.index("def parse(")],
             "s35", "exec"), ns)
hbranch_code, slice3n_code = ns["hbranch_code"], ns["slice3n_code"]

FAIL = []
def check(label, cond, status, extra=""):
    if not cond: FAIL.append(label)
    print(f"  {'PASS' if cond else 'FAIL'}  {label}   <{status}>"
          + (f"   [{extra}]" if extra else ""), flush=True)


def dump_generators(code, budget=600):
    """Replace the slimgb call with a print of the generators."""
    lines = []
    for l in code.splitlines():
        if l.startswith("ideal G = slimgb(E);"):
            lines.append('for (i=1; i<=size(E); i++) { "GEN", E[i]; }')
            continue
        if l.startswith('"DIMG') or l.startswith('"UNIT') or l.startswith('"NEQS'):
            continue
        lines.append(l)
    fn = os.path.join(SCRATCH, "gen.sing")
    open(fn, "w").write("\n".join(lines))
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        return None
    gens, cur = [], None
    for ln in pr.stdout.splitlines():
        if ln.startswith("GEN "):
            if cur is not None: gens.append(cur)
            cur = ln[4:].strip()
        elif cur is not None and ln.strip() and not ln.startswith("//"):
            cur += ln.strip()
    if cur is not None: gens.append(cur)
    return [g for g in gens if g and g != "0"]


def to_msolve(gens, nvars, p, path):
    """Singular's c(1) notation -> msolve's c1; write msolve input."""
    def conv(g):
        return re.sub(r"c\((\d+)\)", r"c\1", g)
    vs = ",".join([f"c{i+1}" for i in range(nvars)] + ["z"])
    with open(path, "w") as f:
        f.write(vs + "\n")
        f.write(f"{p}\n")
        f.write(",\n".join(conv(g) for g in gens) + "\n")
    return path


def parse_msolve(txt):
    """Classify a `msolve -g 2` (reduced Groebner basis) dump.

    The dump is comment lines starting '#', then the basis as `[p1,\np2]:`.
    The ideal is the UNIT ideal -- i.e. the variety is EMPTY -- exactly when the
    basis is the single constant polynomial 1, printed as `[1]:`.

    An earlier version of this function read any non-comment output as
    "NONEMPTY" and so called the unit ideal non-empty.  The cross-engine control
    below caught it.  The control stays.
    """
    body = "\n".join(l for l in txt.splitlines() if not l.startswith("#")).strip()
    if not body:
        return "UNKNOWN"
    i, j = body.find("["), body.rfind("]")
    if i < 0 or j < 0:
        return "UNKNOWN"
    gens = [g.strip() for g in body[i + 1:j].split(",") if g.strip()]
    if len(gens) == 1 and gens[0] == "1":
        return "EMPTY"
    return "NONEMPTY" if gens else "UNKNOWN"


def run_msolve(path, budget=900):
    out = path + ".out"
    t0 = time.time()
    try:
        pr = subprocess.run(["msolve", "-g", "2", "-f", path, "-o", out],
                            capture_output=True, text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", time.time() - t0, ""
    blob = (pr.stdout or "") + (pr.stderr or "")
    if pr.returncode in (-9, 137) or "no more memory" in blob.lower():
        return "OOM", time.time() - t0, blob[:200]
    txt = open(out).read() if os.path.exists(out) else ""
    v = parse_msolve(txt)
    return v, time.time() - t0, txt.replace("\n", " ")[-120:]


print("=" * 78)
print("H4 rung 2 -- msolve (F4/FGLM) on the cells Singular could not hold")
print("=" * 78)

# ---- control first: a cell Singular already decided EMPTY must agree -------
print("\n0a. PARSER CONTROL -- both directions, on systems whose answer is known\n")
_emp = os.path.join(SCRATCH, "p_empty.ms")
open(_emp, "w").write("x,y\n65521\nx,\ny,\nx+y+1\n")        # 1 in the ideal
_non = os.path.join(SCRATCH, "p_nonempty.ms")
open(_non, "w").write("x,y\n65521\nx*y-1,\nx-y\n")           # y^2 = 1, solvable
_ve, _, _ = run_msolve(_emp, budget=120)
_vn, _, _ = run_msolve(_non, budget=120)
check("parser calls a UNIT ideal EMPTY", _ve == "EMPTY", "CERTIFIED",
      f"got {_ve}")
check("parser calls a solvable system NONEMPTY", _vn == "NONEMPTY", "CERTIFIED",
      f"got {_vn}")

print("\n0b. CROSS-ENGINE CONTROL (a cell with a known Singular verdict)\n")
P0 = 65521
g = dump_generators(slice3n_code(4, "x", 1, p=P0))
check("generators extracted from the Singular build", g is not None and len(g) > 0,
      "CERTIFIED", f"{0 if g is None else len(g)} generators")
if g:
    nv = 3 + 4
    N = nv * (1 + 1) + 2
    ms = to_msolve(g, N, P0, os.path.join(SCRATCH, "ctrl.ms"))
    v, secs, det = run_msolve(ms)
    check("msolve agrees with Singular's EMPTY on (3,4) h=x deg<=1",
          v == "EMPTY", "CERTIFIED", f"msolve says {v} [{secs:.1f}s] {det[:80]}")

# ---- the OOM cells --------------------------------------------------------
print("\n1. THE CELLS SESSION 35 RECORDED AS OUT OF MEMORY\n")
OOM_CELLS = [("hbranch", 4, "t", 6), ("hbranch", 5, "t", 4),
             ("hbranch", 5, "t", 5), ("hbranch", 6, "t", 4)]
print(f"  {'cell':28s} {'gens':>5s} {'verdict':>10s} {'secs':>8s}")
print("  " + "-" * 56)
res = {}
for kind, K, hs, D in OOM_CELLS:
    code = hbranch_code(K, hs, D, p=P0)
    gg = dump_generators(code, budget=900)
    if not gg:
        print(f"  k={K} h={hs} deg<={D:<15s} {'-':>5s} {'BUILD-FAIL':>10s}")
        res[f"k={K},{hs},{D}"] = "BUILD-FAIL"; continue
    nfree = 2 * (K - 1) * (D + 1) + (D + 1)
    N = nfree + 2
    ms = to_msolve(gg, N, P0, os.path.join(SCRATCH, f"h_{K}_{D}.ms"))
    v, secs, det = run_msolve(ms, budget=int(os.environ.get("W2_MSTMO", 900)))
    res[f"k={K},{hs},{D}"] = v
    print(f"  k={K} h={hs} deg<={D:<15s} {len(gg):>5d} {v:>10s} {secs:>8.1f}",
          flush=True)

decided = [k for k, v in res.items() if v in ("EMPTY", "NONEMPTY")]
live = [k for k, v in res.items() if v == "NONEMPTY"]
check("msolve decided at least one cell Singular could not hold",
      len(decided) > 0, "CERTIFIED" if decided else "STALLED",
      f"{len(decided)}/{len(OOM_CELLS)} decided: {decided}")
check("no cell came back NONEMPTY", len(live) == 0,
      "CERTIFIED" if not live else "LIVE-COMPONENT", f"{live}")

print("\n" + "=" * 78)
print(f"decided by msolve: {len(decided)}/{len(OOM_CELLS)}   live: {len(live)}")
print("=" * 78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
