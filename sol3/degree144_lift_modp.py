#!/usr/bin/env python3
"""Exact fixed-shear modular systems for the degree-144 lift intersection.

For a prime p and fixed (lambda_2,lambda_3,lambda_4=1), row-reduce the complete
Laurent-pole matrices over F_p, eliminate the two independent driver gauges,
and export the full bracket as quadrics in 16 variables (9 driver, 7 partner).
This is the exact finite-field counterpart of degree144_lift_kernel_search.py.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from degree144_numeric import CASES, Search
from degree144_lift_continuation import FastLift


def inv(a, p):
    return pow(a % p, p-2, p)


def matrix_mod(fast, l2, l3, p):
    out = [[0]*len(fast.supp) for _ in fast.rows]
    for ri, row in enumerate(fast.rows):
        for col, a, b, cc in row:
            out[ri][col] = (out[ri][col]+cc*pow(l2, a, p)*pow(l3, b, p)) % p
    return out


def rref(a, p):
    a = [[x % p for x in row] for row in a]
    nr, nc = len(a), len(a[0]); pivots=[]; row=0
    for col in range(nc):
        pivot = next((r for r in range(row, nr) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        z = inv(a[row][col], p)
        a[row] = [x*z % p for x in a[row]]
        for r in range(nr):
            if r != row and a[r][col]:
                z = a[r][col]
                a[r] = [(x-z*y) % p for x, y in zip(a[r], a[row])]
        pivots.append(col); row += 1
        if row == nr:
            break
    return a, pivots


def kernel(matrix, expected, p):
    rr, pivots = rref(matrix, p)
    free = [c for c in range(len(matrix[0])) if c not in pivots]
    if len(free) != expected:
        raise ArithmeticError(f"kernel dimension {len(free)} != {expected}")
    n = [[0]*expected for _ in range(len(matrix[0]))]
    for j, col in enumerate(free):
        n[col][j] = 1
        for row, pivot in enumerate(pivots):
            n[pivot][j] = -rr[row][col] % p
    return n


def gauge_coordinates(n, rows, p):
    """Affine kernel coordinates u: two pivots eliminated, nine variables."""
    g = [[n[row][j] for j in range(11)] for row in rows]
    _, pivots = rref(g, p)
    pivots = pivots[:2]
    free = [j for j in range(11) if j not in pivots]
    if len(pivots) != 2 or len(free) != 9:
        raise ArithmeticError("driver gauge rank is not exactly two")
    a, b = g[0][pivots[0]], g[0][pivots[1]]
    c, d = g[1][pivots[0]], g[1][pivots[1]]
    deti = inv(a*d-b*c, p)
    # Each coordinate is [constant, coeff(t0),...,coeff(t8)].
    u = [[0]*10 for _ in range(11)]
    for j, col in enumerate(free):
        u[col][j+1] = 1
    rhs = [[1]+[(-g[row][col]) % p for col in free] for row in range(2)]
    for k in range(10):
        u[pivots[0]][k] = (d*rhs[0][k]-b*rhs[1][k])*deti % p
        u[pivots[1]][k] = (-c*rhs[0][k]+a*rhs[1][k])*deti % p
    return u


def mat_lin(n, u, p, offset=0, nvars=16):
    """Matrix times affine-linear coordinates, as [constant, var coeffs]."""
    out=[]
    for row in n:
        v=[0]*(nvars+1)
        for j, scalar in enumerate(row):
            for k, value in enumerate(u[j]):
                target = 0 if k == 0 else offset+k
                v[target] = (v[target]+scalar*value) % p
        out.append(v)
    return out


def multiply_linear(a, b, p):
    out={}
    for i, x in enumerate(a):
        if not x: continue
        for j, y in enumerate(b):
            if not y: continue
            mon=tuple(sorted(k-1 for k in (i,j) if k))
            out[mon]=(out.get(mon,0)+x*y) % p
    return {m:c for m,c in out.items() if c}


def build(prime, l2, l3):
    data=next(c for c in CASES if c[0] == "Q-drives")
    shape=Search(*data, pin_other=False, lift_chart=None)
    fd,fo=FastLift(shape.Dsupp),FastLift(shape.Osupp)
    nd=kernel(matrix_mod(fd,l2,l3,prime),11,prime)
    no=kernel(matrix_mod(fo,l2,l3,prime),7,prime)
    gauges=[shape.Dsupp.index(v) for v in ((1,0),(16,12))]
    du=gauge_coordinates(nd,gauges,prime)
    ou=[]
    for j in range(7):
        row=[0]*8; row[j+1]=1; ou.append(row)
    dc=mat_lin(nd,du,prime)
    oc=mat_lin(no,ou,prime,offset=9)
    equations={}
    for ia,(i,j) in enumerate(shape.Dsupp):
        for ib,(k,ell) in enumerate(shape.Osupp):
            mult=i*ell-j*k
            if not mult: continue
            target=(i+k-1,j+ell-1)
            eq=equations.setdefault(target,{})
            for mon,val in multiply_linear(dc[ia],oc[ib],prime).items():
                eq[mon]=(eq.get(mon,0)+mult*val) % prime
    equations.setdefault((2,0),{})[()] = (equations.setdefault((2,0),{}).get((),0)-1) % prime
    equations=[{m:c for m,c in e.items() if c%prime} for e in equations.values()]
    equations=[e for e in equations if e]
    return equations,shape,dc,oc


def polynomial_text(poly, names, p):
    terms=[]
    for mon,c in sorted(poly.items(), key=lambda z:(len(z[0]),z[0])):
        cc=c if c <= p//2 else c-p
        factor="*".join(names[i] for i in mon)
        if factor:
            terms.append(f"({cc})*{factor}")
        else:
            terms.append(str(cc))
    return "+".join(terms).replace("+-","-") or "0"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prime",type=int,default=101)
    ap.add_argument("--lambda2",type=int,default=1)
    ap.add_argument("--lambda3",type=int,default=1)
    ap.add_argument("--output",default="sol3/degree144_fixed_shear.sing")
    ns=ap.parse_args(); p=ns.prime
    eqs,shape,dc,oc=build(p,ns.lambda2%p,ns.lambda3%p)
    names=[f"d{i}" for i in range(9)]+[f"o{i}" for i in range(7)]
    body=",\n ".join(polynomial_text(e,names,p) for e in eqs)
    text=(f"ring r={p},({','.join(names)}),dp;\n"
          f"ideal I=\n {body};\n"
          "option(redSB);\nideal G=std(I);\nsize(G);\nG;\n")
    Path(ns.output).write_text(text)
    print(f"EXACT MOD-p EXPORT: p={p} shears=({ns.lambda2%p},{ns.lambda3%p},1)")
    print(f"variables=16 equations={len(eqs)} driver-kernel=11 partner-kernel=7 gauges=2")
    print(f"wrote {ns.output}")


if __name__ == "__main__":
    main()
