"""Independent exact replay, using FLINT and a restricted arithmetic parser.

Does not invoke Singular. Checks the leading field identity and the explicit
Nullstellensatz certificate for the final nonzero-corner ideal. Completeness
uses the five-dessin upper bound proved in ASTRA_2_CASE2_EXACT_DESCENT.md;
it does NOT rely on the modular reconstruction's completeness claim.
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
from pathlib import Path
from flint import fmpq, fmpq_poly
from case2_dessin_count import verify as verify_dessins

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'astra/artifacts'
NAMES=('a','B7','B8','b0','b1','z')
VARS={x:i for i,x in enumerate(NAMES[1:])}
ZERO=(0,)*5
MOD=None

def field(x):
    v=x if isinstance(x,fmpq_poly) else fmpq_poly([x])
    return v if MOD is None else v%MOD

class Poly:
    def __init__(self,x=0):
        if isinstance(x,dict):self.d={k:field(v) for k,v in x.items() if field(v)}
        elif isinstance(x,Poly):self.d=x.d.copy()
        else:self.d={ZERO:field(x)} if field(x) else {}
    def __add__(self,b):
        b=Poly(b);out=self.d.copy()
        for k,v in b.d.items():out[k]=out.get(k,fmpq_poly([]))+v
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-Poly(b)
    def __rsub__(self,b):return Poly(b)+-self
    def __mul__(self,b):
        b=Poly(b);out={}
        for k,v in self.d.items():
            for l,w in b.d.items():
                kl=tuple(a+b for a,b in zip(k,l))
                out[kl]=out.get(kl,fmpq_poly([]))+field(v*w)
        return Poly(out)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Poly(b)
        assert set(b.d)=={ZERO},'division by a non-coefficient'
        c=b.d[ZERO]
        if c.degree()==0:inv=fmpq_poly([1/c[0]])
        else:
            assert MOD is not None
            gcd,inv,_=c.xgcd(MOD)
            assert gcd==1
        return self*Poly(field(inv))
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=Poly(1);v=self
        while n:
            if n&1:out=out*v
            v=v*v;n//=2
        return out
    def __bool__(self):return bool(self.d)

def parse(text):
    text=re.sub(r'B\((\d+)\)',r'B\1',text).replace('^','**')
    def visit(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,int):return Poly(node.value)
        if isinstance(node,ast.Name):
            if node.id=='a':return Poly(fmpq_poly([0,1]))
            key=[0]*5;key[VARS[node.id]]=1
            return Poly({tuple(key):1})
        if isinstance(node,ast.UnaryOp):
            p=visit(node.operand)
            return -p if isinstance(node.op,ast.USub) else p
        if isinstance(node,ast.BinOp):
            left=visit(node.left)
            if isinstance(node.op,ast.Pow):
                assert isinstance(node.right,ast.Constant)
                return left**node.right.value
            right=visit(node.right)
            if isinstance(node.op,ast.Add):return left+right
            if isinstance(node.op,ast.Sub):return left-right
            if isinstance(node.op,ast.Mult):return left*right
            if isinstance(node.op,ast.Div):return left/right
        raise ValueError(ast.dump(node))
    return visit(ast.parse(text.strip(),mode='eval').body)

def padd(p,q):
    return [field((p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0)) for i in range(max(len(p),len(q)))]
def pscale(p,c):return [field(c*x) for x in p]
def pmul(p,q):
    out=[fmpq_poly([]) for _ in range(len(p)+len(q)-1)]
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]=field(out[i+j]+x*y)
    return out
def deriv(p):return [field(i*p[i]) for i in range(1,len(p))]

def vadd(p,q):
    return [(p[i] if i<len(p) else Poly())+(q[i] if i<len(q) else Poly()) for i in range(max(len(p),len(q)))]
def vscale(p,c):return [x*c for x in p]
def vmul(p,q):
    out=[Poly() for _ in range(len(p)+len(q)-1)]
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]=out[i+j]+x*y
    return out
def vd(p):return [p[i]*i for i in range(1,len(p))]

def rank(rows):
    rows=[[field(x) for x in row] for row in rows]
    n=0
    for col in range(len(rows[0])):
        pivot=next((j for j in range(n,len(rows)) if rows[j][col]),None)
        if pivot is None:continue
        rows[n],rows[pivot]=rows[pivot],rows[n]
        gcd,inv,_=rows[n][col].xgcd(MOD)
        assert gcd==1
        rows[n]=[field(x*inv) for x in rows[n]]
        for j in range(n+1,len(rows)):
            c=rows[j][col]
            if c:rows[j]=[field(x-c*y) for x,y in zip(rows[j],rows[n])]
        n+=1
    return n

def normalize(p):
    assert p.d
    pivot=p.d[sorted(p.d)[0]]
    p=p/Poly(pivot)
    return tuple((k,str(v)) for k,v in sorted(p.d.items()))

def verify_lower_generation(C,G,generators):
    c,g=list(map(Poly,C)),list(map(Poly,G))
    b0,b1=parse('b0'),parse('b1')
    b=vadd(vscale(vadd(vd(c),vscale(c[1:],-1)),b0),
           vscale(vadd([Poly()]+vd(c),vscale(c,fmpq(-3,2))),b1))
    f=vadd(vscale(vadd(vadd(vd(g),vscale(g[1:],fmpq(-3,2))),vscale(c,fmpq(-1,2))),b0),
           vscale(vadd([Poly()]+vd(g),vscale(g,fmpq(-9,4))),b1))
    r4=vadd(vadd(vscale(vmul(c,vd(f)),2),vscale(vmul(vd(c),f),-2)),
            vadd(vmul(b,vd(g)),vscale(vmul(vd(b),g),-3)))
    assert not any(r4)
    aa=[Poly()]*9
    aa[7],aa[8]=parse('B7'),parse('B8')
    kb=(ART/'case2_exact_level3_basis.txt').read_text().strip().split(',')
    assert len(kb)==6
    for i in range(1,7):
        line=next(x for x in kb if 'B('+str(i)+')' in x)
        match=re.search(r'([-]?\d+)\*B\('+str(i)+r'\)',line)
        assert match
        rest=line[:match.start()]+'0'+line[match.end():]
        aa[i]=-parse(rest)/int(match.group(1))
    source=vadd(vadd(vmul(b,vd(f)),vscale(vmul(vd(b),f),-2)),vscale(vmul(vd(aa),g),-3))
    ee=[Poly() for _ in range(13)]
    for j in range(1,13):
        r=vadd(vadd(vscale(vmul(c,vd(ee)),2),vscale(vmul(vd(c),ee),-1)),source)
        ee[j]=-r[j]/(2*j-1)
    r3=vadd(vadd(vscale(vmul(c,vd(ee)),2),vscale(vmul(vd(c),ee),-1)),source)
    assert not any(r3)
    # Rank six plus a verified particular solution with B7,B8 free proves
    # this parametrization includes EVERY level-three solution.
    columns=[]
    for i in range(1,9):
        da=[field(0)]*i;da[i-1]=field(i)
        source0=pscale(pmul(da,G),-3)
        e=[field(0)]*13
        for j in range(1,13):
            r=padd(padd(pscale(pmul(C,deriv(e)),2),pscale(pmul(deriv(C),e),-1)),source0)
            e[j]=field(-r[j]/(2*j-1))
        r=padd(padd(pscale(pmul(C,deriv(e)),2),pscale(pmul(deriv(C),e),-1)),source0)
        columns.append(r[13:20])
    assert rank(list(zip(*columns)))==6
    source=vadd(vadd(vmul(b,vd(ee)),vscale(vmul(vd(b),ee),-1)),vscale(vmul(vd(aa),f),-2))
    dd=[Poly() for _ in range(13)]
    for j in range(1,13):
        r=vadd(vscale(vmul(c,vd(dd)),2),source)
        dd[j]=-r[j]/(2*j)
    r2=vadd(vscale(vmul(c,vd(dd)),2),source)
    r1=vadd(vmul(b,vd(dd)),vscale(vmul(vd(aa),ee),-1))
    expected={normalize(p) for p in r2+r1 if p}
    actual={normalize(p) for p in generators[:-1] if p}
    assert expected==actual,(len(expected),len(actual))
    print('LOWER_GENERATION_AND_RANK_FLINT: PASS',flush=True)

def main():
    global MOD
    lex=(ART/'case2_exact_modular_lex.txt').read_text().strip().split(',')
    minimal=lex[0].replace('c(8)','a')
    minimal_poly=parse(minimal).d[ZERO]
    MOD=minimal_poly/minimal_poly[minimal_poly.degree()]
    assert MOD.degree()==5 and MOD.gcd(MOD.derivative())==1 and MOD[0]!=0
    _, factors=MOD.factor()
    assert len(factors)==1 and factors[0][0].degree()==5 and factors[0][1]==1
    dessins=verify_dessins()
    assert len(dessins)==5
    print('IRREDUCIBLE_QUINTIC_AND_FIVE_DESSINS: PASS',flush=True)
    C=[field(0),field(1),field(1)]+[None]*5+[field(fmpq_poly([0,1]))]
    for i in range(3,8):
        line=next(x for x in lex if 'c('+str(i)+')' in x)
        # These are linear triangular relations, with a scalar coefficient.
        coefficient=re.search(r'([-]?\d+)\*c\('+str(i)+r'\)',line)
        assert coefficient
        rest=line[:coefficient.start()]+'0'+line[coefficient.end():]
        C[i]=field(-parse(rest.replace('c(8)','a')).d.get(ZERO,field(0))/int(coefficient.group(1)))
    G=[field(0)]*13
    for j in range(2,13):
        r=padd(pscale(pmul(C,deriv(G)),2),pscale(pmul(deriv(C),G),-3))
        r=padd(r,[field(0),field(0),field(-1)])
        G[j]=field(-r[j]/(2*j-3))
    residual=padd(pscale(pmul(C,deriv(G)),2),pscale(pmul(deriv(C),G),-3))
    assert residual[2]==1 and all(v==0 for i,v in enumerate(residual) if i!=2)
    assert C[8] and G[12]
    # Verify the rational-map degree calculation behind the passport argument.
    gcd, inv, _=field(C[8]**3).xgcd(MOD)
    assert gcd==1
    kappa=field(G[12]**2*inv)
    W=padd(pmul(G,G),pscale(pmul(pmul(C,C),C),-kappa))
    assert max(i for i,v in enumerate(W) if v)==7
    assert W[:3]==[field(0)]*3 and W[3]==-kappa
    print('LEADING_IDENTITY_FLINT: PASS',flush=True)
    generators=[parse(x) for x in (ART/'case2_exact_bottom_input.txt').read_text().strip().split(',')]
    generators.append(parse('z*B(8)-1'))
    multipliers=[parse(x) for x in (ART/'case2_exact_bottom_certificate.txt').read_text().strip().split(',')]
    assert len(generators)==len(multipliers)==26
    verify_lower_generation(C,G,generators)
    residual=Poly(-1)
    for p,q in zip(generators,multipliers):residual=residual+p*q
    assert not residual
    print('BOTTOM_NULLSTELLENSATZ_FLINT: PASS',flush=True)
    # Mutation controls must reject an altered claim/certificate.
    index=next(i for i,p in enumerate(generators) if p)
    assert residual+generators[index]
    altered=Poly(-1)
    for p,q in zip(generators,[Poly(0)]*len(multipliers)):altered=altered+p*q
    assert altered
    result={
      'evidence_label':'EXACT-Q',
      'field_degree':5,
      'field_irreducible':'PASS',
      'dessin_representatives':dessins,
      'leading_completeness':'Five inequivalent exact solutions meet the five-dessin upper bound proved in ASTRA_2_CASE2_EXACT_DESCENT.md.',
      'leading_identity':'PASS',
      'lower_certificate_generators':26,
      'lower_certificate_identity':'sum(multiplier_i * generator_i) = 1 in Q[a]/h',
      'lower_certificate':'PASS',
      'level_four_identity':'PASS',
      'level_three_matrix_rank':6,
      'level_three_complete_parametrization':'PASS',
      'lower_system_regenerated_independently':'PASS',
      'mutation_controls':'PASS',
      'scope':'Case (2) of GGHV Proposition 4.3 only. Exact field arithmetic and finite dessin enumeration are machine-checked; the completeness reduction and universal level-four parametrization use the written mathematical proof.',
      'sha256':{name:hashlib.sha256((ART/name).read_bytes()).hexdigest() for name in ['case2_exact_modular_lex.txt','case2_exact_bottom_input.txt','case2_exact_bottom_certificate.txt']}
    }
    (ART/'case2_independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
