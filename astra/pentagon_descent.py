"""Complete graded linear descent for the pentagon over exact or finite fields.

No free kernel coordinate is discarded. A finite-field verdict is only a
finite-field verdict. The saved exact leading seed is reduced and rescaled.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=32003
ROWS=20
EXACT=False
MOD=None
RIGHT_EDGE=False
SMALL_FIELD=False
BOUNDARY=False

def norm(x):
    if EXACT:
        from flint import fmpq_poly
        return (x if isinstance(x,fmpq_poly) else fmpq_poly([x]))%MOD
    return x%P

def inverse(x):
    if EXACT:
        gcd,inv,_=norm(x).xgcd(MOD)
        assert gcd==1
        return norm(inv)
    return pow(x,-1,P)

def fmt(x):
    if not EXACT:return str(x)
    x=norm(x)
    return '('+('+'.join(f'({x[j]})*(a^{j})' for j in range(x.degree()+1) if x[j]) or '0')+')'

def add(a,b):
    return [norm((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))
            for i in range(max(len(a),len(b)))]
def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=norm(out[i+j]+x*y)
    return out
def scale(a,c):return [norm(x*c) for x in a]
def deriv(a):return [norm(i*a[i]) for i in range(1,len(a))]
def basis(j):return [0]*j+[1]

def seed():
    global MOD
    if SMALL_FIELD:
        from flint import fmpq,fmpq_poly
        data=json.loads((ROOT/'astra/artifacts/pentagon_integral_field.json').read_text())
        MOD=fmpq_poly(list(map(fmpq,data['minimal_polynomial'])))
        C=[fmpq_poly(list(map(fmpq,v))) for v in data['C']]
        G=[fmpq_poly(list(map(fmpq,v))) for v in data['G']]
        residual=add(scale(mul(C,deriv(G)),2),scale(mul(deriv(C),G),-3))
        assert residual[2]==1 and not any(x for j,x in enumerate(residual) if j!=2)
        assert C[1]==G[2]==1 and C[8] and G[12]
        return C,G
    if EXACT:
        import re
        import verify_case2_certificate as vc
        vc.MOD=None
        lex=(ROOT/'astra/artifacts/case2_exact_modular_lex.txt').read_text().strip().split(',')
        minimal=vc.parse(lex[0].replace('c(8)','a')).d[vc.ZERO]
        MOD=minimal/minimal[minimal.degree()]
        vc.MOD=MOD
        C=[norm(0),norm(1),norm(1)]+[None]*5+[vc.field(vc.fmpq_poly([0,1]))]
        for i in range(3,8):
            line=next(x for x in lex if 'c('+str(i)+')' in x)
            coefficient=re.search(r'([-]?\d+)\*c\('+str(i)+r'\)',line)
            rest=line[:coefficient.start()]+'0'+line[coefficient.end():]
            C[i]=norm(-vc.parse(rest.replace('c(8)','a')).d.get(vc.ZERO,norm(0))/int(coefficient.group(1)))
        G=[norm(0)]*13
        for j in range(2,13):
            residual=add(scale(mul(C,deriv(G)),2),scale(mul(deriv(C),G),-3))
            G[j]=norm((int(j==2)-residual[j])*inverse(2*j-3))
        residual=add(scale(mul(C,deriv(G)),2),scale(mul(deriv(C),G),-3))
        assert residual[2]==1 and not any(x for j,x in enumerate(residual) if j!=2)
        return C,G
    old=[0,1,31680,28310,28903,29601,17548,31304,1]
    lam=pow(old[2],-1,P)
    C=[0]+[old[i]*pow(lam,i-1,P)%P for i in range(1,9)]
    G=[0]*13
    for j in range(2,13):
        residual=add(scale(mul(C,deriv(G)),2),scale(mul(deriv(C),G),-3))
        G[j]=((int(j==2)-residual[j])*pow(2*j-3,-1,P))%P
    residual=add(scale(mul(C,deriv(G)),2),scale(mul(deriv(C),G),-3))
    assert residual[2]==1 and not any(x for j,x in enumerate(residual) if j!=2)
    assert C[8] and G[12] and C[1:3]==[1,1]
    return C,G

def windows(r):
    f=[] if r < -8 else list(range(1 if r>=0 else 0,(8 if r>=0 else 8+r)+1))
    if RIGHT_EDGE and r in (1,0):f.remove(8)
    s=r+1
    if s==2: g=list(range(2,13))
    elif s>=0: g=list(range(1,13))  # Q's additive constant fixed to zero
    else:g=list(range(0,12+s+1))
    return [('g',j) for j in g]+[('f',j) for j in f]

def operator(C,G,r):
    cols=windows(r)
    vectors=[]
    for kind,j in cols:
        h=basis(j)
        if kind=='g':
            v=add(scale(mul(C,deriv(h)),2),scale(mul(deriv(C),h),-(r+1)))
        else:
            v=add(scale(mul(h,deriv(G)),r),scale(mul(deriv(h),G),-3))
        assert len(v)<=ROWS or not any(v[ROWS:])
        vectors.append(v+[0]*(ROWS-len(v)))
    A=[list(row) for row in zip(*vectors)]
    R=[row[:] for row in A]
    E=[[int(i==j) for j in range(ROWS)] for i in range(ROWS)]
    pivots=[]
    for col in range(len(cols)):
        k=len(pivots)
        pivot=next((i for i in range(k,ROWS) if R[i][col]),None)
        if pivot is None:continue
        R[k],R[pivot]=R[pivot],R[k]; E[k],E[pivot]=E[pivot],E[k]
        inv=inverse(R[k][col])
        R[k]=scale(R[k],inv);E[k]=scale(E[k],inv)
        for i in range(ROWS):
            if i==k:continue
            a=R[i][col]
            if a:
                R[i]=add(R[i],scale(R[k],-a))
                E[i]=add(E[i],scale(E[k],-a))
        pivots.append(col)
    # Verify row transformations and all null vectors independently by products.
    assert all(norm(sum(E[i][k]*A[k][j] for k in range(ROWS)))==R[i][j]
               for i in range(ROWS) for j in range(len(cols)))
    free=[j for j in range(len(cols)) if j not in pivots]
    for j in free:
        v=[0]*len(cols);v[j]=1
        for i,k in enumerate(pivots):v[k]=norm(-R[i][j])
        assert all(norm(sum(a*b for a,b in zip(row,v)))==0 for row in A)
    return {'r':r,'columns':cols,'matrix':A,'rref':R,'transform':E,
            'pivots':pivots,'free':free}

def pname(r):return 'f'+str(r+8)
def qname(s):return 'g'+str(s+12)
def coeffsum(values,terms):
    out=[f'({fmt(c)})*({term})' for c,term in zip(values,terms) if c]
    return '+'.join(out) or '0'
def source(r):
    terms=[]
    for i in range(-8,3):
        j=r+3-i
        if i<=r or j<=r+1 or j not in range(-12,4):continue
        if i:terms.append(f'({i})*{pname(i)}*diff({qname(j)},T)')
        if j:terms.append(f'({-j})*diff({pname(i)},T)*{qname(j)}')
    return '+'.join(terms) or '0'

def generate(saturate=True,ranks_only=False,stop_r=-13,defer_gb=False):
    C,G=seed()
    data=[]
    for r in range(1,stop_r-1,-1):
        d=operator(C,G,r);data.append(d)
        print('OPERATOR',r,'RANK',len(d['pivots']),'KERNEL',len(d['free']),flush=True)
    nfree=sum(len(d['free']) for d in data)
    summaries=[{'r':d['r'],'variables':len(d['columns']),
                'rank':len(d['pivots']),'kernel':len(d['free']),
                'cokernel_in_20_rows':ROWS-len(d['pivots'])} for d in data]
    tag=('exact' if EXACT else 'modular')+('_small' if SMALL_FIELD else '')+('_right' if RIGHT_EDGE else '')
    if defer_gb:tag+='_raw'
    if BOUNDARY:tag+='_boundary'
    report={'evidence':'EXACT-Q over the quintic field' if EXACT else 'EXACT mod 32003 at one leading seed',
            'right_edge_normalized':RIGHT_EDGE,'stop_r':stop_r,'defer_gb':defer_gb,
            'C':list(map(fmt,C)),'G':list(map(fmt,G)),'total_free_parameters':nfree,'stages':summaries}
    (ROOT/f'astra/artifacts/pentagon_linear_operators_{tag}.json').write_text(json.dumps(report,indent=2)+'\n')
    if ranks_only:return
    coeffield='(0,a)' if EXACT else str(P)
    lines=[f'ring R={coeffield},(u(1..{nfree}),z(1..4),T),(dp({nfree}),dp(4),dp(1));']
    if EXACT:
        h='+'.join(f'({MOD[j]})*(a^{j})' for j in range(MOD.degree()+1) if MOD[j])
        lines.append('minpoly='+h+';')
    lines += [
           'option(redSB); short=0;',
           'proc cf(poly h,int k){matrix M=coeffs(h,T); if(k+1>nrows(M)){return(poly(0));} return(M[k+1,1]);}',
           'ideal I; ideal constraints; ideal history; poly src; int j;',
           'poly C='+coeffsum(C,[f'T^{j}' for j in range(len(C))])+';',
           'poly G='+coeffsum(G,[f'T^{j}' for j in range(len(G))])+';']
    lines += [f'poly {pname(i)}=0;' for i in range(-8,3)]
    lines += [f'poly {qname(i)}=0;' for i in range(-12,4)]
    lines += [f'{pname(2)}=C;',f'{qname(3)}=G;']
    nu=0
    for d in data:
        r=d['r'];R,E=d['rref'],d['transform']
        fixed=(f'({fmt(norm(C[8]*(2 if r==1 else 1)))})*T^8'
               if RIGHT_EDGE and not BOUNDARY and r in (1,0) else '0')
        extras=f'({r})*({fixed})*diff(G,T)-3*diff(({fixed}),T)*G'
        lines += [f'"STAGE_R={r}";',f'src=reduce(({source(r)})+({extras}),I);']
        expr={}
        for k in d['free']:
            nu+=1;expr[k]=f'u({nu})'
        for i,k in enumerate(d['pivots']):
            rhs=coeffsum([norm(-a) for a in E[i]],[f'cf(src,{j})' for j in range(ROWS)])
            freeterms=coeffsum([norm(-R[i][j]) for j in d['free']],[expr[j] for j in d['free']])
            expr[k]=f'({rhs})+({freeterms})'
        for kind in ('f','g'):
            if kind=='f' and r < -8:continue
            terms=[f'({expr[k]})*T^{power}' for k,(tag,power) in enumerate(d['columns']) if tag==kind]
            name=pname(r) if kind=='f' else qname(r+1)
            expression='+'.join(terms) or '0'
            if kind=='f':expression=f'({expression})+({fixed})'
            lines.append(name+'=reduce('+expression+',I);')
        lines.append('constraints=0;')
        for row in E[len(d['pivots']):]:
            lines.append('constraints=constraints+('+coeffsum(row,[f'cf(src,{j})' for j in range(ROWS)])+');')
        if saturate:
            corner={0:(1,f'cf({pname(0)},8)'),-1:(2,f'cf({qname(0)},12)'),
                    -8:(3,f'cf({pname(-8)},0)'),-13:(4,f'cf({qname(-12)},0)')}.get(r)
            if corner and not (RIGHT_EDGE and corner[0] in (1,2)):
                lines.append(f'constraints=constraints+ideal(z({corner[0]})*({corner[1]})-1);')
        lines += ['constraints=simplify(reduce(constraints,I),2);',
                  '"NEW_CONSTRAINTS="+string(size(constraints));',
                  f'write(":w astra/artifacts/pentagon_{tag}_stage_{r}_constraints.txt",string(constraints));',
                  'history=history+constraints;',
                  ('I=std(history);' if not defer_gb or r==stop_r else '// Keep the raw polynomial parametrization; no intermediate reduction.'),
                  '"BASIS_SIZE="+string(size(I));',
                  f'write(":w astra/artifacts/pentagon_{tag}_stage_{r}_basis.txt",string(I));',
                  f'if(size(I)==1 && I[1]==1){{"{tag.upper()}_EMPTY_AT_R={r}";'
                  'ideal unit=1; matrix cert=lift(history,unit);'
                  f'write(":w astra/artifacts/pentagon_{tag}_certificate_input.txt",string(history));'
                  f'write(":w astra/artifacts/pentagon_{tag}_certificate.txt",string(cert));'
                  'ideal discrepancy=ideal(matrix(history)*cert-matrix(unit));'
                  '"CERTIFICATE_RESIDUAL="+string(size(simplify(discrepancy,2)));quit;}']
    for r in (range(-14,-24,-1) if stop_r==-13 else []):
        lines += [f'src=reduce({source(r)},I);',
                  'constraints=0; for(j=0;j<20;j++){constraints=constraints+cf(src,j);}',
                  'I=std(I+constraints);',f'"FINAL_LEVEL_R={r},BASIS_SIZE="+string(size(I));',
                  f'if(size(I)==1 && I[1]==1){{"{tag.upper()}_EMPTY_AT_R={r}";quit;}}']
    lines += [f'write(":w astra/artifacts/pentagon_{tag}_final_basis.txt",string(I));',
              '"PENTAGON_RESIDUAL_DIM="+string(dim(I));','quit;']
    if BOUNDARY:
        lines[-1:]=['ring SMALL=32003,(u(1..5)),dp;', 'ideal J=imap(R,I);',
                    'J=std(J);','"BOUNDARY_PARAMETER_DIM="+string(dim(J));',
                    '"BOUNDARY_PARAMETER_VDIM="+string(vdim(J));',
                    f'write(":w astra/artifacts/pentagon_{tag}_boundary_basis.txt",string(J));',
                    'ideal D=imap(R,history); int i; int n; ideal target; matrix powercert;',
                    f'write(":w astra/artifacts/pentagon_{tag}_power_input.txt",string(D));',
                    'for(i=1;i<=5;i++){',
                    ' for(n=1;n<=42;n++){if(reduce(u(i)^n,J)==0){break;}}',
                    ' if(n>42){ERROR("No bounded pure-power certificate found");quit;}',
                    ' target=ideal(u(i)^n); powercert=lift(D,target);',
                    ' ideal check=ideal(matrix(D)*powercert-matrix(target));',
                    ' if(size(simplify(check,2))!=0){ERROR("Power certificate failed");quit;}',
                    ' "POWER_CERTIFICATE="+string(i)+","+string(n);',
                    f' write(":w astra/artifacts/pentagon_{tag}_power_"+string(i)+".txt",string(powercert));',
                    '}', 'quit;']
    (ROOT/f'astra/pentagon_descent_{tag}.sing').write_text('\n'.join(lines)+'\n')
    print('TOTAL_FREE_PARAMETERS',nfree,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--unsaturated',action='store_true')
    parser.add_argument('--exact',action='store_true');parser.add_argument('--ranks-only',action='store_true')
    parser.add_argument('--right-edge',action='store_true')
    parser.add_argument('--small-field',action='store_true')
    parser.add_argument('--stop-r',type=int,default=-13);parser.add_argument('--defer-gb',action='store_true')
    parser.add_argument('--boundary',action='store_true')
    args=parser.parse_args();SMALL_FIELD=args.small_field;EXACT=args.exact or SMALL_FIELD
    RIGHT_EDGE=args.right_edge
    BOUNDARY=args.boundary
    assert not BOUNDARY or (RIGHT_EDGE and not EXACT)
    assert -13<=args.stop_r<=-2
    generate(not args.unsaturated,args.ranks_only,args.stop_r,args.defer_gb)
