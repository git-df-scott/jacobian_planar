import json, os, sys
import sympy as sp
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w4_c2_cascade_solve as CS, w4_c2_residual as RS, w4_run as RUN
W=CS.W
OUT=os.path.join(HERE,'artifacts'); os.makedirs(OUT,exist_ok=True)
PRIMES=[1000003,1000033,1000039]
res={}
for p in PRIMES:
    assert p%3==1
    for chart in ('one','zero'):
        tag=f"{chart}_p{p}"
        st1={}
        for variant in ('real','mutant','pin'):
            f=os.path.join(OUT,f"casc_w4_{variant}_{tag}.ms")
            RS.export_w4(p,chart,f,
                         mutant_seed=(abs(hash(tag))%10**6 if variant=='mutant' else None),
                         pin=(variant=='pin'))
            import w4_msformat as MF
            txt=open(f).read().split('\n'); body=[l.rstrip(',') for l in txt[2:] if l.strip()]
            open(f,'w').write(txt[0]+'\n'+txt[1]+'\n'+',\n'.join(MF.sanitize_lines(body,p))+'\n')
            probs=MF.validate(f)
            assert not probs, (f,probs[:3])
            r=RUN.run_msolve(f,f[:-3]+'.out',timeout=1800,threads=2)
            st1[variant]=r
            print(f"  w4 {variant} {tag}: {r['verdict']} {r['seconds']}s",flush=True)
        res[f"w4_{tag}"]=st1
        RUN.save(res,os.path.join(OUT,'item1_cascade_results.json'))
        if st1['real']['verdict']!='NONEMPTY-PARAMETRIZATION':
            res[f"cascade_{tag}"]={'skipped':st1['real']['verdict']}
            RUN.save(res,os.path.join(OUT,'item1_cascade_results.json')); continue
        rur=RS.parse_rur(os.path.join(OUT,f"casc_w4_real_{tag}.out"))
        vals,_=RS.rur_values(rur); sign=None; note=None
        for s in (1,-1):
            ok,nt=RS.verify_rur(vals,s,rur,p,chart=chart,gauge=RS.GAUGE_BY_CHART[chart])
            note=nt
            if ok: sign=s; break
        res[f"rur_{tag}"]={'deg':rur['deg'],'sign':sign,'note':note,'elim':rur['elim']}
        print(f"  RUR {tag}: deg {rur['deg']} sign {sign}",flush=True)
        if sign is None:
            RUN.save(res,os.path.join(OUT,'item1_cascade_results.json')); continue
        f_=sum(c*W**i for i,c in enumerate(rur['elim']))
        fl=sp.Poly(f_,W,modulus=p,symmetric=False).factor_list()
        facs=[(sp.Poly(b,W,modulus=p,symmetric=False).as_expr(),m) for b,m in fl[1]]
        res[f"factors_{tag}"]=[[sp.sstr(b),int(m),int(sp.Poly(b,W).degree())] for b,m in facs]
        print(f"  eliminant factors {tag}: degrees "
              f"{[int(sp.Poly(b,W).degree()) for b,_ in facs]}",flush=True)
        cell={}
        for fi,(gpoly,mult) in enumerate(facs):
            deg=int(sp.Poly(gpoly,W).degree())
            try:
                params,conds,env,Kf=CS.cascade(p,chart,rur,sign,gpoly)
            except SystemExit as e:
                cell[f"factor{fi}_deg{deg}"]={'error':str(e)}
                print(f"    factor {fi} (deg {deg}): ABORT {e}",flush=True); continue
            sub={}
            for variant in ('real','mutant','pin'):
                fn=os.path.join(OUT,f"casc_res_{variant}_{tag}_f{fi}.ms")
                _,nm,npoly,pt=CS.emit_ms(fn,p,gpoly,params,conds,env,
                                         variant=variant,seed=abs(hash(tag+str(fi)))%10**6)
                r=RUN.run_msolve(fn,fn[:-3]+'.out',timeout=1800,threads=2)
                r['nvars']=len(nm); r['npolys']=npoly
                r['params']=[sp.sstr(x) for x in params]
                if pt is not None: r['planted_point']={sp.sstr(k):int(v) for k,v in pt.items()}
                sub[variant]=r
                print(f"    factor {fi} (deg {deg}) {variant}: {r['verdict']} "
                      f"{r['seconds']}s [{len(nm)} vars, {npoly} polys]",flush=True)
            cell[f"factor{fi}_deg{deg}"]=sub
        res[f"cascade_{tag}"]=cell
        RUN.save(res,os.path.join(OUT,'item1_cascade_results.json'))
print("DONE")
