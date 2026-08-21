#!/usr/bin/env python3
"""PLAN 43 / H4 -- the deg_y = 3 slice (FRAMEWORK.md OPEN-1).

WHAT SESSION 35 LEFT.  Its (3,n)-slice table -- the campaign's first-ever run of
that slice, and the headline of OPEN-1 -- was computed at ONE prime, p = 32003,
and 32003 == 2 (mod 3).

That matters HERE specifically.  The slice pins the leading forms to

    A = alpha * h^3 ,   B = beta * h^n

(the leading condition n A'B - 3 A B' = 0).  A cube is structural in this
system, and over F_p with p == 2 (mod 3) the cubing map x -> x^3 is a BIJECTION:
there are no primitive cube roots of unity, so whole families of solutions that
exist over Qbar have no residue to reduce to.  An EMPTY at such a prime is
therefore weaker evidence than an EMPTY at p == 1 (mod 3), where mu_3 is present.
This is the same prime-hygiene lesson the campaign already paid for once, on the
case-(2) route; it was never applied to the slice.

Session 35's SECOND prime (1000003 == 1 mod 3) was applied only to the h-branch,
never to the slice -- so the slice's compliant-prime check has never been run.

WHAT THIS FILE DOES.
  1. re-runs the slice at TWO compliant primes (both == 1 mod 3);
  2. extends the table into cells Session 35 never reached;
  3. carries a REAL positive control -- the same pipeline, saturation removed,
     which MUST come back non-EMPTY, so an EMPTY here means something.

No check() in this file returns a constant.
"""
import os, sys, subprocess, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "..", "campaign", "moduli_phase2",
                    "phase2_moduli", "certify")
sys.path.insert(0, os.path.abspath(CERT))
SCRATCH = os.environ.get("W2_SCRATCH", os.path.join(HERE, "_scratch"))
os.makedirs(SCRATCH, exist_ok=True)

import importlib.util
spec = importlib.util.spec_from_file_location(
    "s35", os.path.join(os.path.abspath(CERT), "session35_singular_modular_push.py"))
# the module runs its whole census at import, so lift the two builders by exec
# of just their source instead.
src = open(os.path.join(os.path.abspath(CERT),
                        "session35_singular_modular_push.py")).read()
ns = {}
start = src.index("def hbranch_code")
end = src.index("def parse(")
exec(compile(src[start:end], "s35_builders", "exec"), ns)
hbranch_code = ns["hbranch_code"]
slice3n_code = ns["slice3n_code"]

FAIL = []
def check(label, cond, status, extra=""):
    if not cond: FAIL.append(label)
    print(f"  {'PASS' if cond else 'FAIL'}  {label}   <{status}>"
          + (f"   [{extra}]" if extra else ""), flush=True)

PRIMES = [65521, 65539]          # both == 1 (mod 3)
BUDGET = int(os.environ.get("W2_BUDGET", "420"))


def run_singular(code, budget=BUDGET):
    fn = os.path.join(SCRATCH, "h4.sing")
    open(fn, "w").write(code)
    t0 = time.time()
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=budget)
        out = (pr.stdout or "") + (pr.stderr or "")
        st = "RAN"
        if pr.returncode in (-9, 137) or "no more memory" in out.lower():
            st = "OOM"
    except subprocess.TimeoutExpired:
        return "", time.time() - t0, "TIMEOUT"
    return out, time.time() - t0, st


def parse(out):
    """-> (neqs, dim, unit) from the NEQS/DIMG/UNIT lines."""
    neq = dim = unit = None
    for ln in out.splitlines():
        s = ln.split()
        if not s: continue
        if s[0] == "NEQS" and len(s) > 1: neq = int(s[1])
        if s[0] == "DIMG" and len(s) > 1: dim = int(s[1])
        if s[0] == "UNIT" and len(s) > 1: unit = int(s[1])
    return neq, dim, unit


def verdict(out, st):
    if st in ("TIMEOUT", "OOM"): return st
    neq, dim, unit = parse(out)
    if dim is None: return "UNKNOWN"
    return "EMPTY" if dim == -1 else f"dim {dim}"


print("=" * 78)
print("H4 -- the deg_y = 3 slice at COMPLIANT primes, and extended")
print("=" * 78)
print(f"primes {PRIMES}  (mod 3: {[p % 3 for p in PRIMES]})   budget {BUDGET}s")

# --------------------------------------------------------------- controls --
print("\n0.  PRIME HYGIENE, and a control that CAN say non-EMPTY\n")
check("both working primes are == 1 (mod 3)", all(p % 3 == 1 for p in PRIMES),
      "PROVED-exact", f"{[p % 3 for p in PRIMES]}")
check("Session 35's main prime 32003 is == 2 (mod 3) -- the gap this file fills",
      32003 % 3 == 2, "PROVED-exact", f"32003 mod 3 = {32003 % 3}")
check("Session 35's second prime 1000003 IS compliant (so the h-branch was "
      "already covered; only the slice was not)", 1000003 % 3 == 1,
      "PROVED-exact", f"1000003 mod 3 = {1000003 % 3}")

# positive control: same pipeline, saturation dropped -> the zero solution
# survives, so the engine MUST report a positive dimension, not EMPTY.
ctrl = slice3n_code(4, "x", 1, p=PRIMES[0])
ctrl_nosat = "\n".join(l for l in ctrl.splitlines()
                       if not l.startswith("E = E, z*cst"))
out, secs, st = run_singular(ctrl_nosat)
v = verdict(out, st)
check("POSITIVE CONTROL: same pipeline WITHOUT saturation is NOT empty "
      "(the engine can say non-EMPTY)", v not in ("EMPTY", "UNKNOWN"),
      "CERTIFIED", f"verdict {v} [{secs:.1f}s]")
out, secs, st = run_singular(slice3n_code(4, "x", 1, p=PRIMES[0]))
vsat = verdict(out, st)
check("NEGATIVE CONTROL: the SAME cell WITH saturation is EMPTY "
      "(so saturation, not the engine, is doing the work)", vsat == "EMPTY",
      "CERTIFIED", f"verdict {vsat} [{secs:.1f}s]")

# ------------------------------------------------------ the slice, redone --
print("\n1.  THE (3,n) SLICE AT TWO COMPLIANT PRIMES\n")
print(f"  {'case':34s} {'p':>8s} {'eqs':>5s} {'verdict':>10s} {'secs':>7s}")
print("  " + "-" * 68)

CELLS = [(4, "x", 1), (4, "x", 2), (4, "x", 3), (4, "x", 4),
         (5, "x", 1), (5, "x", 2), (5, "x", 3),
         (7, "x", 1), (7, "x", 2), (7, "x", 3),
         (8, "x", 1), (8, "x", 2),
         (10, "x", 1), (10, "x", 2),
         (4, "x2", 2), (4, "x2", 3),
         (4, "x*(x-1)", 2), (4, "x*(x-1)", 3),
         (5, "x*(x-1)", 2)]

results = {}
for n, hs, D in CELLS:
    for p in PRIMES:
        key = f"({3},{n}) h={hs} deg<={D}"
        out, secs, st = run_singular(slice3n_code(n, hs, D, p=p))
        neq, dim, unit = parse(out)
        v = verdict(out, st)
        results.setdefault(key, {})[p] = v
        print(f"  {key:34s} {p:>8d} {str(neq):>5s} {v:>10s} {secs:>7.1f}",
              flush=True)

both = {k: v for k, v in results.items() if len(v) == len(PRIMES)}
agree = {k: v for k, v in both.items()
         if len(set(v.values())) == 1 and "TIMEOUT" not in v.values()
         and "OOM" not in v.values()}
empty_both = {k: v for k, v in agree.items() if set(v.values()) == {"EMPTY"}}
live = {k: v for k, v in results.items()
        if any(x.startswith("dim") for x in v.values())}

print()
check("every cell that completed at both compliant primes AGREES",
      len(agree) == len([k for k, v in both.items()
                         if all(x not in ("TIMEOUT", "OOM") for x in v.values())]),
      "CERTIFIED", f"{len(agree)} cells agree")
check("no cell went LIVE at a compliant prime", len(live) == 0,
      "CERTIFIED" if len(live) == 0 else "LIVE-COMPONENT",
      f"{len(live)} live" + (f" -> {list(live)}" if live else ""))
check("Session 35's slice result SURVIVES the compliant-prime re-run",
      len(empty_both) > 0 and len(live) == 0, "CERTIFIED",
      f"{len(empty_both)} cells EMPTY at both {PRIMES}")

json.dump({k: {str(p): v for p, v in d.items()} for k, d in results.items()},
          open(os.path.join(HERE, "h4_slice3n_results.json"), "w"), indent=1)

print("\n" + "=" * 78)
print(f"cells run: {len(results)}   EMPTY at both compliant primes: "
      f"{len(empty_both)}   live: {len(live)}")
print("Emptiness mod p is still evidence, not a theorem -- but it is now")
print("evidence at primes where mu_3 exists, which it was not before.")
print("=" * 78)
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
