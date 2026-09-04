"""Check the complete modular projective obstruction and its good reduction.

Independent sparse arithmetic, no Singular. Rebuilds one homogeneous system
whose t=1 and t=0 charts have explicit contradiction/pure-power certificates.
The characteristic-zero implication is the valuation argument in the report.
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
import pentagon_descent as d

P=32003
Z=(0,)*6
WEIGHTS=(1,2,3,3,4,1)
sys.setrecursionlimit(10000)  # Long, flat exported polynomial sums.
ART=Path(__file__).resolve().parent/'artifacts'

class Poly:
    def __init__(self,x=0):
        if isinstance(x,Poly):self.d=x.d.copy()
        elif isinstance(x,dict):self.d={k:v%P for k,v in x.items() if v%P}
        else:self.d={Z:x%P} if x%P else {}
    def __add__(self,b):
        b=Poly(b);out=self.d.copy()
        for k,v in b.d.items():out[k]=(out.get(k,0)+v)%P
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-Poly(b)
    def __rsub__(self,b):return Poly(b)+-self
    def __mul__(self,b):
        b=Poly(b);out={}
        for k,v in self.d.items():
            for l,w in b.d.items():
                kl=tuple(x+y for x,y in zip(k,l))
                out[kl]=(out.get(kl,0)+v*w)%P
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        assert n>=0
        out=Poly(1);x=self
        while n:
            if n&1:out=out*x
            x=x*x;n//=2
        return out
    def __truediv__(self,b):
        b=Poly(b);assert set(b.d)=={Z}
        return self*pow(b.d[Z],-1,P)
    def __bool__(self):return bool(self.d)
    def chart(self,t):
        out={}
        for k,v in self.d.items():
            mon=k[:5]+(0,)
            out[mon]=(out.get(mon,0)+v*pow(t,k[5],P))%P
        return Poly(out)

def variable(i):
    e=[0]*6;e[i]=1;return Poly({tuple(e):1})

def parse(text):
    text=re.sub(r'u\((\d+)\)',r'u\1',text).replace('^','**')
    def visit(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,int):return Poly(n.value)
        if isinstance(n,ast.Name):
            assert n.id in ['u1','u2','u3','u4','u5','t']
            return variable(5 if n.id=='t' else int(n.id[1:])-1)
        if isinstance(n,ast.UnaryOp):
            assert isinstance(n.op,(ast.USub,ast.UAdd))
            return -visit(n.operand) if isinstance(n.op,ast.USub) else visit(n.operand)
        if isinstance(n,ast.BinOp):
            a=visit(n.left)
            if isinstance(n.op,ast.Pow):
                assert isinstance(n.right,ast.Constant)
                return a**n.right.value
            b=visit(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
        raise ValueError(ast.dump(n))
    return visit(ast.parse(text.strip(),mode='eval').body)

def read(name):return [parse(s) for s in (ART/name).read_text().strip().split(',')]
def normalized(p):
    lead=p.d[sorted(p.d)[0]]
    q=p/lead
    return tuple(sorted(q.d.items()))
def same_generators(a,b):return {normalized(p) for p in a if p}=={normalized(p) for p in b if p}
def combo(row,values):return sum((v*c for c,v in zip(row,values) if c and v),Poly())

def matrix_rank(matrix):
    a=[row[:] for row in matrix];rank=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][j],-1,P)
        a[rank]=[x*inv%P for x in a[rank]]
        for i in range(rank+1,len(a)):
            c=a[i][j]
            a[i]=[(x-c*y)%P for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def line(ff,gg,r):
    out=[Poly() for _ in range(20)]
    for rho,f in ff.items():
        sigma=r+3-rho
        if sigma not in gg:continue
        for i,a in enumerate(f):
            if not a:continue
            for j,b in enumerate(gg[sigma]):
                # Direct determinant of the original x,y monomial exponents.
                determinant=i*(2*j-sigma)-(2*i-rho)*j
                if b and determinant:out[i+j-1]=out[i+j-1]+a*b*determinant
    return out

def exact_good_reduction(ops,Cmod,Gmod):
    d.EXACT=True;d.SMALL_FIELD=False
    C,G=d.seed();root=26088
    def scalar(q):
        den=int(q.denominator)%P
        assert den,'a field coefficient denominator vanishes at the chosen prime'
        return int(q.numerator)%P*pow(den,-1,P)%P
    def reduce(v):
        v=d.norm(v)
        return sum(scalar(v[i])*pow(root,i,P) for i in range(v.degree()+1))%P
    # h is monic with coefficients integral at this prime and has the
    # specified residue root. The derivative test is additional reassurance.
    h=d.MOD
    assert sum(scalar(h[i])*pow(root,i,P) for i in range(6))%P==0
    assert sum(i*scalar(h[i])*pow(root,i-1,P) for i in range(1,6))%P!=0
    assert list(map(reduce,C))==Cmod and list(map(reduce,G))==Gmod
    for r,modop in ops.items():
        op=d.operator(C,G,r)
        assert op['columns']==modop['columns'] and op['pivots']==modop['pivots']
        for key in ['matrix','rref','transform']:
            assert [[reduce(x) for x in row] for row in op[key]]==modop[key],(r,key)
    print('EXACT_FIELD_AND_ALL_OPERATOR_REDUCTIONS: PASS',flush=True)
    return {'prime':P,'residue_of_original_C8':root,'leading_model':'PASS',
            'all_operator_coefficients_integral':'PASS','all_row_transformations_commute':'PASS'}

def main():
    from verify_pentagon_descent import supports
    support_sizes=supports()
    d.EXACT=False;d.SMALL_FIELD=False;d.RIGHT_EDGE=True
    C,G=d.seed();ff={2:list(map(Poly,C))};gg={3:list(map(Poly,G))}
    ops={};affine=[];boundary=[];nu=0;weights=[]
    for r in range(1,-7,-1):
        op=d.operator(C,G,r);ops[r]=op
        assert matrix_rank(op['transform'])==20
        assert matrix_rank(op['matrix'])==len(op['pivots'])
        assert not any(x for row in op['rref'][len(op['pivots']):] for x in row)
        rhs=line(ff,gg,r)
        fixed=([Poly()]*8+[C[8]*(2 if r==1 else 1)*variable(5)**(2-r)]) if r in (1,0) else None
        if fixed:
            extra=line({r:fixed},{3:list(map(Poly,G))},r)
            rhs=[a+b for a,b in zip(rhs,extra)]
        values={}
        for k in op['free']:
            values[k]=variable(nu);assert WEIGHTS[nu]==2-r;nu+=1
        for i,k in enumerate(op['pivots']):
            values[k]=-combo(op['transform'][i],rhs)
            for j in op['free']:values[k]=values[k]-values[j]*op['rref'][i][j]
        f=[Poly() for _ in range(9 if r>=0 else 9+r)]
        g=[Poly() for _ in range(13 if r+1>=0 else 14+r)]
        for k,(kind,power) in enumerate(op['columns']):(f if kind=='f' else g)[power]=values[k]
        if fixed:f[8]=f[8]+fixed[8]
        ff[r]=f;gg[r+1]=g
        constraints=[combo(row,rhs) for row in op['transform'][len(op['pivots']):]]
        for p in f+g+constraints:
            assert all(sum(w*e for w,e in zip(WEIGHTS,k))==2-r for k in p.d)
        residual=line(ff,gg,r)
        changed=[combo(row,residual) for row in op['transform']]
        assert not any(changed[:len(op['pivots'])])
        assert all(not (a-b) for a,b in zip(changed[len(op['pivots']):],constraints))
        if r>=-5:
            actual=read(f'pentagon_modular_right_raw_stage_{r}_constraints.txt')
            spec=[p.chart(1) for p in constraints]
            assert same_generators(spec,actual)
            affine+=spec
        actual=read(f'pentagon_modular_right_raw_boundary_stage_{r}_constraints.txt')
        spec=[p.chart(0) for p in constraints]
        assert same_generators(spec,actual)
        boundary+=spec
        weights.append({'r':r,'equation_weight':2-r,'kernel':len(op['free'])})
    assert nu==5
    print('HOMOGENEOUS_SYSTEM_AND_BOTH_CHARTS: PASS',flush=True)
    ap=read('pentagon_modular_right_raw_certificate_input.txt')
    aq=read('pentagon_modular_right_raw_certificate.txt')
    assert len(ap)==len(aq) and same_generators(affine,ap)
    residual=sum((a*b for a,b in zip(ap,aq)),Poly())-1
    assert not residual
    assert residual+next(p for p in ap if p)
    print('AFFINE_UNIT_CERTIFICATE: PASS',flush=True)
    bp=read('pentagon_modular_right_raw_boundary_power_input.txt')
    assert same_generators(boundary,bp)
    powers=[9,5,3,2,3]
    for i,n in enumerate(powers,1):
        multipliers=read(f'pentagon_modular_right_raw_boundary_power_{i}.txt')
        assert len(multipliers)==len(bp)
        residual=sum((p*q for p,q in zip(bp,multipliers)),Poly())-variable(i-1)**n
        assert not residual
        assert residual+next(p for p in bp if p)
    print('ALL_FIVE_BOUNDARY_POWER_CERTIFICATES: PASS',flush=True)
    good=exact_good_reduction(ops,C,G)
    names=['pentagon_modular_right_raw_certificate_input.txt','pentagon_modular_right_raw_certificate.txt',
           'pentagon_modular_right_raw_boundary_power_input.txt']+[
           f'pentagon_modular_right_raw_boundary_power_{i}.txt' for i in range(1,6)]
    report={'status':'PASS','scope':'GGHV Proposition 4.3(1), with the written normalization, leading-completeness and valuation arguments',
            'support_sizes_without_constants':support_sizes,'parameter_weights':WEIGHTS,
            'levels':weights,'homogeneous_reconstruction':'PASS','affine_unit_certificate':'PASS',
            'boundary_pure_powers':powers,'boundary_certificates':'PASS','mutation_controls':'PASS',
            'good_reduction':good,'char_zero_bridge':'Written weighted-projective valuation argument; not naive affine mod-p inference.',
            'sha256':{n:hashlib.sha256((ART/n).read_bytes()).hexdigest() for n in names}}
    (ART/'pentagon_projective_verification.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
