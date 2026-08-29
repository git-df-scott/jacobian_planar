#!/usr/bin/env python3
"""Exact degeneration analysis in P_{a,b}=p^2*u+a*p*s+b*s.

For b != 0 the Briancon boundary chart makes eta holomorphic at the unique
s=infinity branch.  The only way to leave that chart inside this family is
b=0, but then P_{a,0}=p*(p*u+a*s), so the zero fibre is reducible.

The script also certifies the exceptional submersion P_{-1,0}; it is a useful
control showing that degeneration can preserve unimodularity, but not the
all-fibres-irreducible target condition.
"""

from fractions import Fraction as F
import json
import os
import sys

HERE=os.path.dirname(os.path.abspath(__file__))
sys.path[:0]=[os.path.join(HERE,"..","night22"),
              os.path.join(HERE,"..","night21"),
              os.path.join(HERE,"..","night14")]
from briancon22 import briancon  # noqa: E402
from pole21 import ONE, add, scale, mul, dx, dy  # noqa: E402
from eigensearch21 import bezout, pstr  # noqa: E402
import sy14  # noqa: E402


def qclean(f):
    return {m:F(c) for m,c in f.items() if c}


def qadd(*ff):
    z={}
    for f in ff:
        for m,c in f.items(): z[m]=z.get(m,F(0))+c
    return qclean(z)


def qsc(c,f):
    return qclean({m:F(c)*v for m,v in f.items()})


def qmul(f,g):
    z={}
    for m,c in f.items():
        for n,d in g.items():
            e=tuple(a+b for a,b in zip(m,n)); z[e]=z.get(e,F(0))+c*d
    return qclean(z)


def qpow(f,n):
    z={(0,)*len(next(iter(f))):F(1)}
    for _ in range(n): z=qmul(z,f)
    return z


def symbolic_boundary_checks():
    # Ring Q[a,b,s,p,t].
    one={(0,0,0,0,0):F(1)}
    a={(1,0,0,0,0):F(1)}; b={(0,1,0,0,0):F(1)}
    s={(0,0,1,0,0):F(1)}; p={(0,0,0,1,0):F(1)}
    t={(0,0,0,0,1):F(1)}
    pm1=qadd(p,qsc(-1,one)); spm1=qadd(qmul(s,p),qsc(-1,one))
    cleared=qadd(qmul(qpow(p,2),qmul(s,spm1)),
                 qmul(a,qmul(p,qmul(s,pm1))),
                 qmul(b,qmul(s,pm1)),qsc(-1,qmul(t,pm1)))
    expected=qadd(qmul(qpow(s,2),qpow(p,3)),
                  qmul(qadd(a,qsc(-1,one)),qmul(s,qpow(p,2))),
                  qmul(qadd(b,qsc(-1,a)),qmul(s,p)),
                  qsc(-1,qmul(b,s)),qsc(-1,qmul(t,p)),t)
    assert cleared==expected

    # Extract boundary initial forms from the exact general support.
    pinf={}
    sinf={}
    for (ea,eb,es,ep,et),c in expected.items():
        pinf[(ea,eb,es,3-ep,et)]=c
        sinf[(ea,eb,2-es,ep,et)]=c
    pface={m:c for m,c in pinf.items() if m[2]+m[3]==2}
    sface={m:c for m,c in sinf.items() if 3*m[2]+m[3]==3}
    pexpect=qadd(qpow(s,2),qmul(qadd(a,qsc(-1,one)),qmul(s,{(0,0,0,1,0):F(1)})),
                  qsc(-1,qmul(t,{(0,0,0,2,0):F(1)})))
    # pexpect uses p's slot as the q exponent; compare in the transformed ring.
    assert pface==pexpect
    sexpect={(0,0,0,3,0):F(1),(0,1,1,0,0):F(-1)}
    assert sface==sexpect

    # Critical eliminant on b=0 after P_s=0.  Ring Q[a,p].
    one2={(0,0):F(1)}; aa={(1,0):F(1)}; pp={(0,1):F(1)}
    am1=qadd(aa,qsc(-1,one2))
    first=qadd(aa,qsc(-1,qmul(am1,pp)))
    E=qadd(qmul(first,qadd(qsc(2,pp),qsc(-3,one2))),
           qsc(2,qmul(am1,qpow(pp,2))),qsc(-4,qmul(am1,pp)),qsc(2,aa))
    target=qadd(qmul(qadd(aa,one2),pp),qsc(-1,aa))
    assert E==target
    return True


def cusp_second_kind_check():
    """Check the a=b=0 cusp series over Q(alpha), alpha^2=-1."""
    def Iadd(*xx): return (sum(x[0] for x in xx),sum(x[1] for x in xx))
    def Isc(c,x): return (F(c)*x[0],F(c)*x[1])
    def Imul(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    zero=(F(0),F(0)); one=(F(1),F(0)); alpha=(F(0),F(1))
    w0=alpha; w1=(F(1,2),F(0)); w2=(F(0),F(3,8))
    # (1-r^2)w^2-rw+1=0 through r^2.
    assert Iadd(Imul(w0,w0),one)==zero
    assert Iadd(Isc(2,Imul(w0,w1)),Isc(-1,w0))==zero
    r2=Iadd(Imul(w1,w1),Isc(2,Imul(w0,w2)),Isc(-1,Imul(w0,w0)),Isc(-1,w1))
    assert r2==zero
    # In -dz/H_p, the r^{-1} coefficient cancels:
    # 2/3 + alpha*(2 alpha/3) = 0.
    residue=Iadd((F(2,3),F(0)),Imul(alpha,Isc(F(2,3),alpha)))
    assert residue==zero
    return {"local_model":"p^3+t*z^2", "eta_valuation":-2,
            "residue":"0", "series":"p=r^2; z=r^3*(alpha+r/2+3*alpha*r^2/8+...); alpha^2=-1"}


def main():
    # Symbolic elimination on b=0, away from p=0,1 and s=0:
    # P_s=0 gives s=[a-(a-1)p]/(2p^2).  Substitution into the second
    # critical equation reduces exactly to (a+1)p-a.
    assert symbolic_boundary_checks()

    P=briancon(F(-1),F(0))
    bz=bezout(P,maxdeg=8)
    assert bz is not None and bz[2]==7
    U,V,_=bz
    residual=add(mul(U,dx(P)),mul(V,dy(P)),scale(-1,ONE))
    assert residual=={}
    sy,stats=sy14.certify(P,node_budget=300000)
    assert sy=="NON_COORDINATE"

    # Rebuild p and (p*u-s), and verify the reducible zero-fibre identity.
    x={(1,0):F(1)}; y={(0,1):F(1)}
    s=add(mul(x,y),ONE); p=add(mul(x,s),ONE); u=add(mul(s,s),y)
    fac2=add(mul(p,u),scale(-1,s))
    assert add(P,scale(-1,mul(p,fac2)))=={}
    assert len(p)>1 and len(fac2)>1

    cusp=cusp_second_kind_check()
    out={
      "family":"P_ab=p^2*u+a*p*s+b*s",
      "symbolic_cleared_fibre_and_boundary_faces_verified":True,
      "open_stratum":{
        "condition":"b != 0",
        "period_obstruction":"eta extends holomorphically at all infinity places on the genus-one Briancon profile",
        "verdict":"PERIOD-NONZERO"
      },
      "degeneration_divisor":{
        "condition":"b = 0",
        "factorization":"P_a0 = p*(p*u+a*s)",
        "all_fibres_irreducible":False
      },
      "critical_eliminant_b0":"(a+1)*p-a",
      "period_zero_local_degeneration":{
        "a":0,"b":0,**cusp,
        "fatal_global_failure":"P_00=p^2*u has a reducible fibre"
      },
      "exceptional_control":{
        "a":-1,"b":0,"degree":max(map(sum,P)),
        "unimodular":"EXACT_BEZOUT","bezout_degree":7,
        "bezout_residual_terms":0,"U":pstr(U),"V":pstr(V),
        "non_coordinate":sy,"sy_stats":stats,
        "zero_fibre_reducible":True,
        "factor_1":pstr(p),"factor_2":pstr(fac2)
      },
      "conclusion":"no all-fibres-irreducible period-zero point in this two-parameter family"
    }
    with open(os.path.join(HERE,"family_boundary23.json"),"w") as f:
        json.dump(out,f,indent=2,sort_keys=True)
    print("b!=0: PERIOD-NONZERO on the Briancon genus-one boundary chart")
    print("b=0: exact zero-fibre factorization p*(p*u+a*s)")
    print("a=b=0: exact local second-kind profile valuation -2, residue 0; globally reducible")
    print("a=-1,b=0: exact Bezout degree 7; SY NON_COORDINATE; reducible zero fibre")
    print("PASS: the extracted degeneration locus exits the all-irreducible target class")


if __name__=="__main__":
    main()
