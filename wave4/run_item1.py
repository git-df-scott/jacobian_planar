import json, os, sys, time
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import w4_c2_residual as RS, w4_run as RUN
OUT=os.path.join(HERE,'artifacts'); os.makedirs(OUT,exist_ok=True)
PRIMES=[1000003,1000033,1000039]
res={}
for p in PRIMES:
    assert p%3==1, p
    for chart in ('one','zero'):
        tag=f"{chart}_p{p}"
        # ---- stage 1: the w=-4 block, with its own controls
        st1={}
        for variant in ('real','mutant','pin'):
            f=os.path.join(OUT,f"item1_w4_{variant}_{tag}.ms")
            RS.export_w4(p, chart, f,
                         mutant_seed=(abs(hash(tag))%10**6 if variant=='mutant' else None),
                         pin=(variant=='pin'))
            r=RUN.run_msolve(f, f[:-3]+'.out', timeout=1800, threads=2)
            st1[variant]=r
            print(f"  w4 {variant} {tag}: {r['verdict']} {r['seconds']}s", flush=True)
        res[f"w4_{tag}"]=st1
        RUN.save(res, os.path.join(OUT,'item1_results.json'))
        if st1['real']['verdict']!='NONEMPTY-PARAMETRIZATION':
            res[f"residual_{tag}"]={'skipped':'w=-4 block gave '+st1['real']['verdict']}
            RUN.save(res, os.path.join(OUT,'item1_results.json'))
            continue
        rur=RS.parse_rur(os.path.join(OUT,f"item1_w4_real_{tag}.out"))
        sign=None; note=None
        vals,_lf=RS.rur_values(rur)
        for s in (1,-1):
            ok,nt=RS.verify_rur(vals, s, rur, p, chart=chart,
                                gauge=RS.GAUGE_BY_CHART[chart])
            if ok:
                sign, note = s, nt
                break
            note=nt
        res[f"rur_{tag}"]={'eliminant_degree':rur['deg'],'sign':sign,'verification':note,
                           'eliminant_coeffs':rur['elim']}
        print(f"  RUR {tag}: deg {rur['deg']} sign {sign} -- {note}", flush=True)
        if sign is None:
            RUN.save(res, os.path.join(OUT,'item1_results.json')); continue
        # ---- stage 2: the residual system over F_p[w]/(f)
        st2={}
        for variant in ('real','mutant','pin'):
            f=os.path.join(OUT,f"item1_residual_{variant}_{tag}.ms")
            path,nv,npoly,pt=RS.export_residual(p,chart,rur,sign,f,
                    mutant_seed=(abs(hash('r'+tag))%10**6 if variant=='mutant' else None),
                    pin=(variant=='pin'))
            r=RUN.run_msolve(f, f[:-3]+'.out', timeout=2700, threads=2)
            r['nvars']=nv; r['npolys']=npoly
            if pt is not None: r['planted_point']={k:int(v) for k,v in sorted(pt.items())}
            st2[variant]=r
            print(f"  residual {variant} {tag}: {r['verdict']} {r['seconds']}s "
                  f"({nv} vars, {npoly} polys)", flush=True)
        res[f"residual_{tag}"]=st2
        RUN.save(res, os.path.join(OUT,'item1_results.json'))
print("DONE")
