#!/usr/bin/env python3
"""Tiny Q-certificate for the degree-144 length-1 lift obstruction.

On chart (lambda_2,lambda_3,lambda_4)=(0,0,1), let
  a = coefficient of x in the driver,
  b = coefficient of x*y in the driver,
  w = inverse of a.
The full support+reverse-lift ideal contains
  F1=a-b, F2=-(1/2)*b*w^2+w, F3=a*w-1.
This script verifies the three-term Nullstellensatz certificate exactly.
"""
from fractions import Fraction as Q


def add(*ps):
    out={}
    for p in ps:
        for m,c in p.items(): out[m]=out.get(m,Q(0))+c
    return {m:c for m,c in out.items() if c}


def mul(p,q):
    out={}
    for (i,j,k),c in p.items():
        for (u,v,z),d in q.items():
            m=(i+u,j+v,k+z); out[m]=out.get(m,Q(0))+c*d
    return {m:c for m,c in out.items() if c}


one={(0,0,0):Q(1)}; a={(1,0,0):Q(1)}; b={(0,1,0):Q(1)}; w={(0,0,1):Q(1)}
neg=lambda p:{m:-c for m,c in p.items()}
scale=lambda c,p:{m:c*v for m,v in p.items()}

F1=add(a,neg(b))
F2=add(scale(Q(-1,2),mul(b,mul(w,w))),w)
F3=add(mul(a,w),neg(one))
M1=add(neg(mul(b,mul(w,w))),w)
M2=scale(2,b)
M3=add(mul(b,w),neg(one))
cert=add(mul(M1,F1),mul(M2,F2),mul(M3,F3))

print("F1 = a-b  (driver reverse-polynomiality)")
print("F2 = -b*w^2/2+w  (partner reverse-polynomiality)")
print("F3 = a*w-1  (a nonzero)")
print("CERTIFICATE:", "PASS" if cert==one else f"FAIL {cert}")
print("(-b*w^2+w)*F1 + 2*b*F2 + (b*w-1)*F3 = 1")

# The opposite orientation is structurally dead before lift: its driver row
# upper x-degrees are unchanged by c'=0 versus c'=4.  Propagate the exact
# y-adic degree recurrence; the required generated vertex is (16,12).
driver_hi={j:v for j,v in enumerate([1,2,3,4,5,7,8,9,10,12,12,12,12])}
u={0:-1,1:2}
for k in range(1,19):
    ds=[]
    for aa in range(k+1):
        bb=k-aa
        if aa+1 in driver_hi and u.get(bb,-1)>=0:
            ds.append(driver_hi[aa+1]+u[bb]-1)
        if aa>=1 and aa in driver_hi and u.get(bb+1,-1)>=0:
            ds.append(driver_hi[aa]-1+u[bb+1])
    u[k+1]=max(ds,default=-1)
print("OPPOSITE ORIENTATION DEGREE GATE:",
      "PASS" if u[12]==15 else f"FAIL upper={u[12]}")
print("generated row 12 has x-degree <= 15, so required vertex (16,12) is zero")
