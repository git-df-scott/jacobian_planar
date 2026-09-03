import json, re, sys, subprocess, os
res, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
M='/tmp/msolve-0.10.1/bin/msolve'; p=65521
R=json.load(open(res)); ends=[r for r in R if r['result']=='END']
summary=[]
for k,r in enumerate(ends):
    C=r['C']; N=sorted(set(r['N']))
    vs=sorted(set(v for f in C+N for v in re.findall(r'c_\d+', f)), key=lambda v:int(v[2:]))
    ts=[f't{i}' for i in range(len(N))]
    polys=C+[f'({n})*{t}-1' for n,t in zip(N,ts)]
    # expand products: msolve does not accept parentheses -> distribute
    def dist(n,t):
        return '+'.join(term+'*'+t if not term.startswith('-') else term+'*'+t for term in re.findall(r'[+-]?[^+-]+', n.replace(' ','')))+'-1'
    polys=C+[dist(n,t) for n,t in zip(N,ts)]
    if not polys: summary.append((k, r['zeros'], r['free'], 'NO CONSTRAINTS: NONEMPTY, dim = #free')); continue
    fn=f'{outdir}/end{k}.ms'; open(fn,'w').write(','.join(vs+ts)+f'\n{p}\n'+',\n'.join(polys)+'\n')
    pr=subprocess.run(f'ulimit -v 5000000; timeout 1200 {M} -g 2 -t 2 -f {fn} -o {fn}.out', shell=True, capture_output=True, text=True)
    out=open(fn+'.out').read() if os.path.exists(fn+'.out') else ''
    if not out.strip(): v=f'WALL exit={pr.returncode}'
    elif re.search(r'\[1\]:\s*$', out): v='EMPTY [1]'
    else:
        basis=re.search(r'\[(.*)\]:\s*$', out, re.S).group(1); bl=[re.sub(r'\^1(?![0-9])','',b.strip()) for b in basis.split(',\n') if b.strip()]
        s=f"ring R = {p}, ({','.join(vs+ts)}), dp;\nideal G = "+',\n'.join(bl)+';\nattrib(G,"isSB",1);\n"dim " + string(dim(G));\nif (dim(G)==0) { "vdim " + string(vdim(G)); }\nquit;\n'
        open(fn+'.sing','w').write(s); d=subprocess.run(f'ulimit -v 3000000; timeout 600 Singular -q {fn}.sing', shell=True, capture_output=True, text=True).stdout.strip().replace('\n',' ')
        v=f'NONUNIT basis {len(bl)}: {d}'
    summary.append((k, r['zeros'], r['nz'], r['free'], len(C), len(N), v)); print(summary[-1], flush=True)
json.dump(summary, open(f'{outdir}/summary.json','w'), indent=1)
