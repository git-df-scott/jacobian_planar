"""Full-depth two-prime run on the (72,108) subcases, with the (0,0) driver
coefficient c(1) set to 0.

Justification: [P + c, Q] = [P, Q] for any constant c, so the value of the
(0,0) coefficient of the driver is free -- it is the single dim-1 freedom the
full-depth rank measured. Normalizing it to 0 removes that freedom, giving a
0-dimensional system, which Groebner bases decide quickly (vdim, not dim).
This is a WLOG normalization, not a relaxation: a solution with c(1)=a maps
to one with c(1)=0 by subtracting the constant a from P.
"""
import sys, os, time, json
import trackD_twoprime as TW
import trackD_extract as EX

TW.TARGETS = "trackD_targets_108.json"
TW.STATE = "state_108_norm.json"
PRIMES = TW.PRIMES

def norm_run(NP, NQ, r, name, prime, budget):
    os.environ["TRACKD_PRIME"] = str(prime)
    for m in [k for k in list(sys.modules) if k.startswith("trackD_extract")]:
        del sys.modules[m]
    import trackD_extract as EX2
    src, info = EX2.build_singular(NP, NQ, r, jextra=15, name=name)
    if src is None:
        return "OOS", info, ""
    # inject c(1)=0 as an ideal generator (the (0,0) driver coefficient)
    src = src.replace("ideal I;", "ideal I; I = I + ideal(c(1));")
    import subprocess, tempfile
    fn = os.path.join(EX2.SCRATCH, f"norm_{name}.sing")
    os.makedirs(EX2.SCRATCH, exist_ok=True)
    open(fn, "w").write(src)
    t0 = time.time()
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=budget)
        out = pr.stdout or ""
    except subprocess.TimeoutExpired:
        return "TIMEOUT", info, ""
    return TW.classify(out), info, out

def main():
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
    targets = json.load(open(TW.TARGETS))
    st = TW.load() if os.path.exists(TW.STATE) else {}
    for t in targets:
        per = {}
        for prime in PRIMES:
            vd, info, out = norm_run(t["NP"], t["NQ"], t["r"],
                                     f"n{prime}", prime, budget)
            per[str(prime)] = {"verdict": vd, "out": out.replace("\n"," | ")[:400]}
            print(f"{t['tag'][:50]}  p={prime}: {vd}  {out.strip()[-120:]}",
                  flush=True)
            if vd == "TIMEOUT":
                break
        vs = [per[str(p)]["verdict"] for p in PRIMES if str(p) in per]
        comb = TW.combine(vs[0], vs[1] if len(vs) > 1 else "TIMEOUT")
        st[t["tag"] + " | NORM c(1)=0"] = {"verdict": comb, "per_prime": per}
        TW.save.__wrapped__(st) if hasattr(TW.save,"__wrapped__") else json.dump(st, open(TW.STATE,"w"), indent=1)
        print(f"  => {comb}\n", flush=True)

if __name__ == "__main__":
    main()
