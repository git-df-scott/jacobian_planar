"""Item 1 at more primes.  Same pipeline as run_item1_cascade.py, more primes.

Emptiness modulo one prime is weak; modulo many compliant primes it is the
strongest form the campaign's own section 6.2 permits without a char-0 proof.
The cascade costs seconds per prime, so the prime count is cheap to raise.
Every prime is p = 1 (mod 3) and none appears in the campaign record.
"""
import json, os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w4_c2_cascade_solve as CS, w4_c2_residual as RS, w4_run as RUN, w4_msformat as MF
W = CS.W
OUT = os.path.join(HERE, 'artifacts'); os.makedirs(OUT, exist_ok=True)
CAMPAIGN = {32003, 65521, 65537, 65539, 65599, 100003, 100019, 100043, 100057,
            100069, 100103, 100109, 100129}
DONE = {1000003, 1000033, 1000039}
NPRIMES = int(sys.argv[1]) if len(sys.argv) > 1 else 12
primes, n = [], 1000039
while len(primes) < NPRIMES:
    n += 1
    if n % 3 == 1 and sp.isprime(n) and n not in CAMPAIGN and n not in DONE:
        primes.append(n)
print(f"extra primes (all = 1 mod 3, none in the campaign record): {primes}")
res = {}
path = os.path.join(OUT, 'item1_more_primes.json')
for p in primes:
    for chart in ('one', 'zero'):
        tag = f"{chart}_p{p}"
        f = os.path.join(OUT, f"more_w4_real_{tag}.ms")
        RS.export_w4(p, chart, f)
        txt = open(f).read().split('\n')
        body = [l.rstrip(',') for l in txt[2:] if l.strip()]
        open(f, 'w').write(txt[0] + '\n' + txt[1] + '\n'
                           + ',\n'.join(MF.sanitize_lines(body, p)) + '\n')
        assert not MF.validate(f)
        r = RUN.run_msolve(f, f[:-3] + '.out', timeout=1800, threads=1)
        cell = {"w4_verdict": r['verdict'], "w4_seconds": r['seconds']}
        if r['verdict'] == 'EMPTY':
            cell["residual"] = "not reached: the w=-4 block is already EMPTY"
            res[tag] = cell
            print(f"  {tag}: w=-4 EMPTY ({r['seconds']}s)", flush=True)
            RUN.save(res, path); continue
        if r['verdict'] != 'NONEMPTY-PARAMETRIZATION':
            cell["residual"] = f"not reached: {r['verdict']}"
            res[tag] = cell
            print(f"  {tag}: w=-4 {r['verdict']}", flush=True)
            RUN.save(res, path); continue
        rur = RS.parse_rur(f[:-3] + '.out')
        vals, _ = RS.rur_values(rur)
        sign = None
        for s in (1, -1):
            ok, _ = RS.verify_rur(vals, s, rur, p, chart=chart,
                                  gauge=RS.GAUGE_BY_CHART[chart])
            if ok:
                sign = s; break
        cell["eliminant_degree"] = rur['deg']; cell["sign"] = sign
        if sign is None:
            cell["residual"] = "RUR sign undetermined"
            res[tag] = cell; RUN.save(res, path); continue
        fpoly = sum(c * W ** i for i, c in enumerate(rur['elim']))
        fl = sp.Poly(fpoly, W, modulus=p, symmetric=False).factor_list()
        facs = [sp.Poly(b, W, modulus=p, symmetric=False).as_expr() for b, _ in fl[1]]
        cell["factor_degrees"] = [int(sp.Poly(b, W).degree()) for b in facs]
        verdicts = {}
        for fi, g in enumerate(facs):
            params, conds, env, Kf = CS.cascade(p, chart, rur, sign, g, verbose=False)
            sub = {}
            for variant in ('real', 'mutant', 'pin'):
                fn = os.path.join(OUT, f"more_res_{variant}_{tag}_f{fi}.ms")
                CS.emit_ms(fn, p, g, params, conds, env, variant=variant,
                           seed=abs(hash(tag + str(fi))) % 10 ** 6)
                rr = RUN.run_msolve(fn, fn[:-3] + '.out', timeout=1800, threads=1)
                sub[variant] = rr['verdict']
            verdicts[f"factor{fi}_deg{int(sp.Poly(g, W).degree())}"] = sub
        cell["residual"] = verdicts
        res[tag] = cell
        allempty = all(v['real'] == 'EMPTY' for v in verdicts.values())
        ctrl = all(v['mutant'] != 'EMPTY' and v['pin'] == 'EMPTY'
                   for v in verdicts.values())
        print(f"  {tag}: eliminant deg {rur['deg']} factors "
              f"{cell['factor_degrees']} -> residual "
              f"{'EMPTY everywhere' if allempty else verdicts}; "
              f"controls {'PASS' if ctrl else 'FAIL'}", flush=True)
        RUN.save(res, path)
print("DONE")
