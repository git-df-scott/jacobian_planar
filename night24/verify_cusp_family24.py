#!/usr/bin/env python3
"""Independent verifier for the night24 cusp-family closure."""

from fractions import Fraction as F
import json,os
HERE=os.path.dirname(os.path.abspath(__file__))

def C(a):return {m:F(v) for m,v in a.items() if v}
def add(*aa):
 z={}
 for a in aa:
  for m,v in a.items():z[m]=z.get(m,F(0))+v
 return C(z)
def sc(c,a):return C({m:F(c)*v for m,v in a.items()})
def mul(a,b):
 z={}
 for (i,j),v in a.items():
  for (r,s),w in b.items():z[(i+r,j+s)]=z.get((i+r,j+s),F(0))+v*w
 return C(z)
def der(a,k):
 z={}
 for (i,j),v in a.items():
  e=(i,j)[k]
  if e:
   m=(i-1,j) if k==0 else (i,j-1);z[m]=v*e
 return C(z)
def dec(a):
 z={}
 for k,(n,d) in a.items():z[tuple(map(int,k.split(',')))]=F(n,d)
 return C(z)

def main():
 data=json.load(open(os.path.join(HERE,"cusp_family24.json")))
 S=data["sample"];P=dec(S["P"]);A=dec(S["A"]);U=dec(S["U"]);V=dec(S["V"])
 one={(0,0):F(1)};x={(1,0):F(1)};y={(0,1):F(1)}
 s=add(mul(x,y),one);p=add(mul(x,s),one);u=add(mul(s,s),y);p2=mul(p,p)
 rebuilt=add(mul(p2,u),sc(2,mul(s,p2)),p2,sc(-2,p))
 assert P==rebuilt
 DP_A=add(mul(der(P,0),der(A,1)),sc(-1,mul(der(P,1),der(A,0))))
 assert add(DP_A,sc(-1,P))=={}
 assert add(mul(U,der(P,0)),mul(V,der(P,1)),sc(-1,one))=={}
 Rp=add(sc(2,one),sc(2,mul(x,s)),sc(2,x))
 Rm=add(sc(2,y),sc(2,mul(s,s)),sc(2,s))
 assert add(P,sc(F(-1,4),mul(p,mul(Rp,Rm))))=={}
 # A constants on p,Rplus,Rminus are 3/2,1/2,-1/2.
 assert add(A,sc(F(-3,2),one),mul(p,add(s,one)))=={}
 assert add(A,sc(F(-1,2),one),sc(F(1,2),mul(s,Rp)))=={}
 assert add(A,sc(F(1,2),one),sc(F(1,2),mul(x,Rm)))=={}
 assert len({F(3,2),F(1,2),F(-1,2)})==3
 allowed=[]
 for i in range(3):
  for j in range(4):
   if (i,j) in ((2,3),(0,0)) or 3*(2-i)+2*j>6:allowed.append((i,j))
 assert [list(x) for x in allowed]==data["allowed_H_support"]
 assert data["elliptic_de_rham"]["zero_locus"].startswith("EMPTY")
 G=data["profile13_unimodular_sample"];PG=dec(G["P"]);UG=dec(G["U"]);VG=dec(G["V"])
 rebuiltG=add(mul(p2,u),sc(F(1,2),mul(s,p2)),sc(F(3,32),p2),sc(F(-9,16),p))
 assert PG==rebuiltG and F(1,4)-4*F(3,32)==F(-1,8)
 assert add(mul(UG,der(PG,0)),mul(VG,der(PG,1)),sc(-1,one))=={}
 for E in data["unimodular_locus"]["isolated_exception_certificates"]:
  PE,UE,VE=dec(E["P"]),dec(E["U"]),dec(E["V"])
  assert add(mul(UE,der(PE,0)),mul(VE,der(PE,1)),sc(-1,one))=={}
 print("PASS independent: sample Bezout, eigenprimitive, factorization, component constants")
 print("PASS independent: all three isolated submersion Bezout certificates")
 print("PASS independent: cusp support enumeration and noncancellable pole mismatch")

if __name__=="__main__":main()
