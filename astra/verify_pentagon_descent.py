"""Independent replay of the raw five-parameter necessary subsystem.

Uses FLINT, no Singular. Checks the lattice supports and every basis-monomial
bracket identity, reconstructs the coefficient operators directly in x,y,
and verifies every row transformation. Rebuilds the raw parameter equations
before multiplying any exported Nullstellensatz certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from flint import fmpq,fmpq_poly
import pentagon_descent as producer
import verify_case2_certificate as v

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'astra/artifacts'
TAG='pentagon_exact_small_right_raw'

def read_poly(s):return v.parse(re.sub(r'u\((\d+)\)',r'u\1',s))

def polygon_points(vertices):
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    return {(i,j) for i in range(max(x for x,y in vertices)+1)
            for j in range(max(y for x,y in vertices)+1)
            if all(cross(a,b,(i,j))>=0 for a,b in zip(vertices,vertices[1:]+vertices[:1]))}

def supports():
    pp=polygon_points([(0,0),(1,0),(8,14),(8,16),(0,8)])-{(0,0)}
    qq=polygon_points([(0,0),(2,1),(12,21),(12,24),(0,12)])-{(0,0)}
    f={(j,2*j-r) for r in range(-8,3) for j in range(1 if r>=0 else 0,(8 if r>=0 else 8+r)+1)}
    g={(j,2*j-s) for s in range(-12,4)
       for j in range(2 if s>=2 else 1 if s>=0 else 0,(12 if s>=0 else 12+s)+1)}
    assert f==pp and g==qq
    for a,b in pp:
        for c,d in qq:
            r,s=2*a-b,2*c-d
            assert a*d-b*c==r*c-s*a
            assert b+d-1==2*(a+c-1)+1-r-s
    return len(pp),len(qq)

def xy_column(C,G,r,kind,k):
    out=[v.field(0)]*20
    if kind=='g':
        q=(k,2*k-r-1)
        for i,ci in enumerate(C):
            if not ci:continue
            p=(i,2*i-2)
            coefficient=p[0]*q[1]-p[1]*q[0]
            if coefficient:out[i+k-1]=v.field(out[i+k-1]+ci*coefficient)
    else:
        p=(k,2*k-r)
        for i,gi in enumerate(G):
            if not gi:continue
            q=(i,2*i-3)
            coefficient=p[0]*q[1]-p[1]*q[0]
            if coefficient:out[i+k-1]=v.field(out[i+k-1]+gi*coefficient)
    return out

def line_source(ff,gg,r):
    out=[v.Poly() for _ in range(20)]
    for rho,f in ff.items():
        sigma=r+3-rho
        if sigma not in gg:continue
        for i,a in enumerate(f):
            if not a:continue
            for j,b in enumerate(gg[sigma]):
                coefficient=rho*j-sigma*i
                if b and coefficient:out[i+j-1]=out[i+j-1]+a*b*coefficient
    return out

def combo(row,polys):
    out=v.Poly()
    for a,b in zip(row,polys):
        if a and b:out=out+b*v.Poly(a)
    return out

def main(certificate=True):
    pc,qc=supports()
    producer.EXACT=True;producer.SMALL_FIELD=True;producer.RIGHT_EDGE=True
    C,G=producer.seed();v.MOD=producer.MOD
    v.VARS={f'u{i+1}':i for i in range(5)}
    ff={2:list(map(v.Poly,C))};gg={3:list(map(v.Poly,G))}
    all_constraints=[];nu=0;rank_records=[]
    for r in range(1,-6,-1):
        op=producer.operator(C,G,r)
        columns=[xy_column(C,G,r,kind,k) for kind,k in op['columns']]
        direct=[list(row) for row in zip(*columns)]
        assert direct==op['matrix']
        assert v.rank(direct)==len(op['pivots'])
        rank_records.append((r,len(op['pivots']),len(op['free'])))
        rhs=line_source(ff,gg,r)
        fixed=v.field(C[8]*(2 if r==1 else 1)) if r in (1,0) else v.field(0)
        if fixed:
            extra=xy_column(C,G,r,'f',8)
            rhs=[a+v.Poly(v.field(b*fixed)) for a,b in zip(rhs,extra)]
        values={}
        for k in op['free']:
            nu+=1;values[k]=read_poly(f'u{nu}')
        for i,k in enumerate(op['pivots']):
            values[k]=-combo(op['transform'][i],rhs)
            for j in op['free']:
                values[k]=values[k]-values[j]*v.Poly(op['rref'][i][j])
        f=[v.Poly() for _ in range(9 if r>=0 else 9+r)]
        g=[v.Poly() for _ in range(13 if r+1>=0 else 14+r)]
        for k,(kind,power) in enumerate(op['columns']):
            (f if kind=='f' else g)[power]=values[k]
        if fixed:f[8]=f[8]+v.Poly(fixed)
        ff[r]=f;gg[r+1]=g
        constraints=[combo(row,rhs) for row in op['transform'][len(op['pivots']):]]
        all_constraints.extend(p for p in constraints if p)
        stored=[read_poly(s) for s in (ART/f'{TAG}_stage_{r}_constraints.txt').read_text().strip().split(',')]
        assert {v.normalize(p) for p in constraints if p}=={v.normalize(p) for p in stored if p}
        # Every full equation equals the verified row-system residual. In
        # particular its pivot rows vanish and other rows are the constraints.
        residual=line_source(ff,gg,r)
        transformed=[combo(row,residual) for row in op['transform']]
        assert not any(transformed[:len(op['pivots'])])
        assert all(not (a-b) for a,b in zip(transformed[len(op['pivots']):],constraints))
        print('EXACT_RAW_STAGE',r,'PASS',flush=True)
    assert nu==5
    result={'scope':'Necessary graded prefix through r=-5 of the normalized pentagon',
            'support_sizes_without_constants':[pc,qc],
            'support_and_monomial_bracket_checks':'PASS',
            'direct_xy_operator_checks':'PASS','complete_kernel_parameters':nu,
            'ranks_and_kernels':rank_records,'raw_equations_regenerated':'PASS',
            'nonzero_raw_constraints':len(all_constraints)}
    if certificate:
        names=[f'{TAG}_certificate_input.txt',f'{TAG}_certificate.txt']
        pp,qq=([read_poly(s) for s in (ART/name).read_text().strip().split(',')] for name in names)
        assert len(pp)==len(qq)
        assert {v.normalize(p) for p in pp if p}=={v.normalize(p) for p in all_constraints}
        residual=v.Poly(-1)
        for p,q in zip(pp,qq):residual=residual+p*q
        assert not residual
        assert residual+next(p for p in pp if p)
        result.update(certificate='PASS',certificate_generators=len(pp),mutation_control='PASS',
                      sha256={name:hashlib.sha256((ART/name).read_bytes()).hexdigest() for name in names})
        print('PENTAGON_NULLSTELLENSATZ_FLINT: PASS',flush=True)
    (ART/'pentagon_independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--constraints-only',action='store_true')
    args=ap.parse_args();main(not args.constraints_only)
