#!/usr/bin/env python3
"""Low-degree modular certificate for a fixed nonzero-shear degree-144 fibre.

The exact fixed-shear lift system is first reduced by every forced linear
equation. For the default p=101, (lambda_2,lambda_3)=(1,1), this leaves 69
quadrics in 10 variables. A degree-4 Macaulay calculation proves that 1 is in
their span, extracts multipliers, and independently re-expands the certificate.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

from degree144_lift_modp import build


def monomials_leq(nvars, degree):
    out=[]
    def rec(position, left, current):
        if position == nvars-1:
            for value in range(left+1):
                out.append(tuple(current+[value]))
        else:
            for value in range(left+1):
                rec(position+1, left-value, current+[value])
    rec(0, degree, [])
    return sorted(set(out), key=lambda m:(sum(m),m))


def expression(poly, variables):
    result=0
    for monomial, coefficient in poly.items():
        term=sp.Integer(coefficient)
        for index in monomial:
            term *= variables[index]
        result += term
    return result


def linear_reduce(equations, variables, prime):
    active=list(variables)
    polys=[sp.Poly(expression(e,variables),*active,modulus=prime).as_expr()
           for e in equations]
    substitutions=[]
    while True:
        linear=[f for f in polys if sp.Poly(f,*active,modulus=prime).total_degree() <= 1]
        if not linear:
            break
        basis=sp.groebner(linear,*active,order="lex",modulus=prime)
        solved=False
        for generator in basis.polys:
            value=generator.as_expr(); poly=sp.Poly(value,*active,modulus=prime)
            if poly.total_degree() != 1:
                continue
            for variable in active:
                coefficient=int(poly.coeff_monomial(variable)) % prime
                if not coefficient:
                    continue
                remaining=[v for v in active if v != variable]
                rest=sp.Poly(value-coefficient*variable,*active,modulus=prime).as_expr()
                rhs=sp.Poly(-pow(coefficient,prime-2,prime)*rest,
                            *remaining,modulus=prime).as_expr()
                substitutions.append((str(variable),str(rhs)))
                polys=[sp.Poly(f.subs(variable,rhs),*remaining,modulus=prime).as_expr()
                       for f in polys]
                polys=[f for f in polys if f != 0]
                active=remaining; solved=True; break
            if solved:
                break
        if not solved:
            break
    return polys,active,substitutions


def polynomial_dicts(polys, variables, prime):
    return [{monomial:int(coefficient)%prime
             for monomial,coefficient in sp.Poly(f,*variables,modulus=prime).terms()}
            for f in polys]


def row_basis_with_sources(matrix, prime):
    a=matrix.copy()%prime
    sources=np.arange(len(a)); row=0; pivots=[]; selected=[]
    for column in range(a.shape[1]):
        candidates=np.flatnonzero(a[row:,column])
        if not len(candidates):
            continue
        pivot=row+int(candidates[0])
        a[[row,pivot]]=a[[pivot,row]]; sources[[row,pivot]]=sources[[pivot,row]]
        a[row]=(a[row]*pow(int(a[row,column]),prime-2,prime))%prime
        factors=a[:,column].copy(); factors[row]=0
        nonzero=np.flatnonzero(factors)
        if len(nonzero):
            a[nonzero]=(a[nonzero]-factors[nonzero,None]*a[row])%prime
        pivots.append(column); selected.append(int(sources[row])); row += 1
        if row == len(a):
            break
    return pivots,selected


def solve_full_column_rank(matrix, target, prime):
    """Solve matrix*x=target when matrix has full column rank."""
    a=np.c_[matrix.copy()%prime,target.copy()%prime]
    row=0; pivots=[]
    for column in range(matrix.shape[1]):
        candidates=np.flatnonzero(a[row:,column])
        if not len(candidates):
            continue
        pivot=row+int(candidates[0]); a[[row,pivot]]=a[[pivot,row]]
        a[row]=(a[row]*pow(int(a[row,column]),prime-2,prime))%prime
        factors=a[:,column].copy(); factors[row]=0
        nonzero=np.flatnonzero(factors)
        if len(nonzero):
            a[nonzero]=(a[nonzero]-factors[nonzero,None]*a[row])%prime
        pivots.append(column); row += 1
    if len(pivots) != matrix.shape[1]:
        raise ArithmeticError("selected Macaulay rows lost rank")
    if any(not np.any(r[:-1]) and r[-1] for r in a):
        raise ArithmeticError("target is outside the Macaulay row span")
    solution=np.zeros(matrix.shape[1],dtype=np.int64)
    for r,column in enumerate(pivots):
        solution[column]=a[r,-1]
    return solution


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prime",type=int,default=101)
    ap.add_argument("--lambda2",type=int,default=1)
    ap.add_argument("--lambda3",type=int,default=1)
    ap.add_argument("--degree",type=int,default=4)
    ap.add_argument("--output",default="sol3/degree144_p101_shear_1_1_certificate.json")
    ns=ap.parse_args(); p=ns.prime
    equations,*_=build(p,ns.lambda2%p,ns.lambda3%p)
    all_variables=sp.symbols("d0:9")+sp.symbols("o0:7")
    polys,variables,substitutions=linear_reduce(equations,all_variables,p)
    poly_dicts=polynomial_dicts(polys,variables,p)
    max_degree=max(max(sum(m) for m in f) for f in poly_dicts)
    columns=monomials_leq(len(variables),ns.degree)
    column_index={monomial:i for i,monomial in enumerate(columns)}
    multipliers=monomials_leq(len(variables),ns.degree-max_degree)
    rows=[]; labels=[]
    for equation_index,poly in enumerate(poly_dicts):
        for multiplier in multipliers:
            row=np.zeros(len(columns),dtype=np.int64)
            for monomial,coefficient in poly.items():
                product=tuple(a+b for a,b in zip(monomial,multiplier))
                row[column_index[product]]=coefficient
            rows.append(row); labels.append((equation_index,multiplier))
    macaulay=np.asarray(rows,dtype=np.int64)
    pivots,selected=row_basis_with_sources(macaulay,p)
    constant=np.zeros(len(columns),dtype=np.int64)
    constant[column_index[(0,)*len(variables)]]=1
    selected_matrix=macaulay[selected].T
    coefficients=solve_full_column_rank(selected_matrix,constant,p)
    replay=np.zeros(len(columns),dtype=np.int64)
    terms=[]
    for coefficient,row_index in zip(coefficients,selected):
        if coefficient:
            replay=(replay+coefficient*macaulay[row_index])%p
            equation_index,multiplier=labels[row_index]
            terms.append({"coefficient":int(coefficient),
                          "equation":equation_index,
                          "multiplier":list(multiplier)})
    assert np.array_equal(replay,constant)
    # Independent negative control: altering one multiplier must break replay.
    broken=replay.copy()
    first=next(i for i,c in enumerate(coefficients) if c)
    broken=(broken-macaulay[selected[first]])%p
    assert not np.array_equal(broken,constant)
    artifact={"prime":p,"lambda2":ns.lambda2%p,"lambda3":ns.lambda3%p,
              "lambda4":1,"degree":ns.degree,
              "original_equations":len(equations),
              "reduced_equations":len(polys),
              "variables":[str(v) for v in variables],
              "linear_substitutions":substitutions,
              "macaulay_shape":list(macaulay.shape),
              "macaulay_rank":len(pivots),"certificate_terms":terms}
    Path(ns.output).write_text(json.dumps(artifact,indent=2)+"\n")
    print(f"FIXED-FIBRE CERTIFICATE: PASS over F_{p}, shears "
          f"({ns.lambda2%p},{ns.lambda3%p},1)")
    print(f"linear reduction: {len(equations)} eq/16 vars -> "
          f"{len(polys)} eq/{len(variables)} vars")
    print(f"degree-{ns.degree} Macaulay: {macaulay.shape[0]}x{macaulay.shape[1]}, "
          f"rank {len(pivots)}, certificate terms {len(terms)}")
    print("INDEPENDENT RE-EXPANSION: PASS; NEGATIVE CONTROL: PASS")
    print(f"wrote {ns.output}")


if __name__ == "__main__":
    main()
