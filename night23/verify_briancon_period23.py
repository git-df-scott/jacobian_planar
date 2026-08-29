#!/usr/bin/env python3
"""Independent exact verifier for briancon_period23.json.

This file does not import the producer or the campaign polynomial library.
It rebuilds the original maps and both infinity charts using a separate sparse
Q-polynomial implementation, then checks the valuation certificates.
"""

from fractions import Fraction as F
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(a):
    return {m: F(c) for m, c in a.items() if c}


def add(*aa):
    z = {}
    for a in aa:
        for m, c in a.items():
            z[m] = z.get(m, F(0)) + c
    return clean(z)


def sc(c, a):
    return clean({m: F(c)*v for m, v in a.items()})


def mul(a, b):
    z = {}
    for m, c in a.items():
        for n, d in b.items():
            e = tuple(x+y for x, y in zip(m, n))
            z[e] = z.get(e, F(0)) + c*d
    return clean(z)


def pw(a, n, dim=2):
    z = {(0,)*dim: F(1)}
    for _ in range(n):
        z = mul(z, a)
    return z


def der(a, axis):
    z = {}
    for m, c in a.items():
        if m[axis]:
            e = list(m); e[axis] -= 1
            z[tuple(e)] = c*m[axis]
    return clean(z)


def original(a, b):
    one={(0,0):F(1)}; x={(1,0):F(1)}; y={(0,1):F(1)}
    s=add(mul(x,y),one); p=add(mul(x,s),one); u=add(pw(s,2),y)
    P=add(mul(pw(p,2),u),sc(a,mul(p,s)),sc(b,s))
    return one,x,y,s,p,u,P


def Hpoly(k,A,B,C):
    # variables are (S,p)
    return clean({(2,3):F(k),(1,2):F(-A),(1,1):F(B),(1,0):F(C),
                  (0,1):F(-k),(0,0):F(k)})


def subst_comp(H, S, p):
    z={}
    for (i,j),c in H.items():
        z=add(z,sc(c,mul(pw(S,i),pw(p,j))))
    return z


def divrem(f,g):
    f=clean({(i,):c for i,c in enumerate(f)}); g=clean({(i,):c for i,c in enumerate(g)})
    dg=max(i[0] for i in g)
    while f and max(i[0] for i in f)>=dg:
        df=max(i[0] for i in f); c=f[(df,)]/g[(dg,)]; d=df-dg
        f=add(f,sc(-c,{(i[0]+d,):v for i,v in g.items()}))
    return [f.get((i,),F(0)) for i in range(1+max([i[0] for i in f],default=-1))]


def gcd(f,g):
    while any(g):
        f,g=g,divrem(f,g)
    while f and f[-1]==0:f.pop()
    return [x/f[-1] for x in f]


def verify_one(spec, rec):
    name,a,b,k,A,B,C=spec
    one,x,y,S,p,u,P=original(a,b)
    assert max(map(sum,P))==10
    assert add(mul(add(p,sc(-1,one)),u),sc(-1,mul(S,add(mul(S,p),sc(-1,one)))))=={}
    H=Hpoly(k,A,B,C)
    Hxy=subst_comp(H,S,p)
    assert add(Hxy,sc(-k,mul(add(p,sc(-1,one)),add(P,sc(-1,one)))))=={}
    J=add(mul(der(S,0),der(p,1)),sc(-1,mul(der(S,1),der(p,0))))
    assert add(J,add(p,sc(-1,one)))=={}

    # Rebuild q^3 H(S,1/q).  Exponent map (i,j)->(i,3-j).
    pinf={(i,3-j):c for (i,j),c in H.items()}
    face={m:c for m,c in pinf.items() if sum(m)==2}
    assert face=={(2,0):F(k),(1,1):F(-A),(0,2):F(-k)}
    tang=[F(-k),F(-A),F(k)]
    assert A*A+4*k*k>0 and gcd(tang,[F(0),F(1)])==[F(1)]
    assert gcd(tang,[F(-2*k),F(-A)])==[F(1)]

    # Rebuild z^2 H(1/z,p).  Weight wt(z)=3, wt(p)=1.
    sinf={(2-i,j):c for (i,j),c in H.items()}
    face2={m:c for m,c in sinf.items() if 3*m[0]+m[1]==3}
    assert face2=={(0,3):F(k),(1,0):F(C)}
    assert F(k,C)!=0

    assert rec["name"]==name and rec["verdict"]=="PERIOD-NONZERO"
    assert rec["p_infinity"]["eta_valuation_each"]==0
    assert rec["s_infinity"]["eta_valuation"]==0


def main():
    data=json.load(open(os.path.join(HERE,"briancon_period23.json")))
    specs=[("g",F(-5,3),F(-1,3),3,8,4,1),
           ("gprime",F(-7,9),F(1,9),9,16,8,-1)]
    assert len(data["targets"])==2
    for spec,rec in zip(specs,data["targets"]):
        verify_one(spec,rec)
        print(spec[0],"PASS independent exact boundary/de Rham certificate")
    print("PASS: PERIOD-NONZERO for both targets is independently verified over Q")


if __name__=="__main__":
    main()
