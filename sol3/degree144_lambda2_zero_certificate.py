#!/usr/bin/env python3
"""Exact Q-certificate closing the degree-144 divisor lambda_2=0.

Reconstruct the complete symbolic lift kernels with lambda_3=t and lambda_4=1,
eliminate the two independent driver gauges, form the full bracket, and extract
four linear coefficient equations. Three of them have a one-line unit-ideal
certificate, valid for every t (including t=0).
"""
import sympy as sp

from degree144_numeric import CASES, Search
from degree144_lift_continuation import FastLift

t = sp.Symbol("t")
ds = sp.symbols("d0:9")
os = sp.symbols("o0:7")


def symbolic_lift_matrix(fast):
    matrix = sp.zeros(len(fast.rows), len(fast.supp))
    for row_index, row in enumerate(fast.rows):
        for column, lambda2_power, lambda3_power, coefficient in row:
            if lambda2_power == 0:  # lambda_2=0
                matrix[row_index, column] += coefficient*t**lambda3_power
    return matrix


def kernel(matrix):
    rr, pivots = matrix.rref(simplify=False)
    free = [column for column in range(matrix.cols) if column not in pivots]
    result = sp.zeros(matrix.cols, len(free))
    for j, column in enumerate(free):
        result[column, j] = 1
        for row, pivot in enumerate(pivots):
            result[pivot, j] = -rr[row, column]
    return result


data = next(case for case in CASES if case[0] == "Q-drives")
shape = Search(*data, pin_other=False, lift_chart=None)
driver_kernel = kernel(symbolic_lift_matrix(FastLift(shape.Dsupp)))
other_kernel = kernel(symbolic_lift_matrix(FastLift(shape.Osupp)))
assert driver_kernel.cols == 11 and other_kernel.cols == 7

# Set driver coefficients at (1,0) and (16,12) to one. The exact right-edge
# identity then makes (16,16)=1 automatically; it is not a third gauge.
gauge_rows = [shape.Dsupp.index(v) for v in ((1, 0), (16, 12))]
gauge = driver_kernel[gauge_rows, :]
_, gauge_pivots = gauge.rref(simplify=False)
gauge_pivots = gauge_pivots[:2]
gauge_free = [column for column in range(11) if column not in gauge_pivots]
u = [None]*11
for value, column in zip(ds, gauge_free):
    u[column] = value
z = sp.symbols("z0:2")
equations = []
for row in range(2):
    equations.append(sum(gauge[row, column]*u[column] for column in gauge_free)
                     + sum(gauge[row, column]*z[j]
                           for j, column in enumerate(gauge_pivots))-1)
solution = sp.solve(equations, z, dict=True, simplify=False)[0]
for j, column in enumerate(gauge_pivots):
    u[column] = solution[z[j]]

driver = driver_kernel*sp.Matrix(u)
other = other_kernel*sp.Matrix(os)
bracket = {}
for ai, (i, j) in enumerate(shape.Dsupp):
    for bi, (k, ell) in enumerate(shape.Osupp):
        multiplier = i*ell-j*k
        if multiplier:
            target = (i+k-1, j+ell-1)
            bracket[target] = bracket.get(target, 0) + multiplier*driver[ai]*other[bi]
bracket[(2, 0)] = bracket.get((2, 0), 0)-1

linear = {}
for target, expression in bracket.items():
    expression = sp.factor(expression)
    if expression and sp.Poly(expression, *(ds+os)).total_degree() <= 1:
        linear[target] = expression

expected = {
    (1, 0): t*(os[1]-t*os[2]+t**2*os[3]),
    (2, 0): os[1]-t*os[2]+t**2*os[3]-1,
    (2, 1): os[1]+t*os[2]-t**2*os[3],
    (3, 1): 2*(os[2]-t*os[3]),
}
assert set(linear) == set(expected)
assert all(sp.expand(linear[key]-value) == 0 for key, value in expected.items())

F20, F21, F31 = linear[(2, 0)], linear[(2, 1)], linear[(3, 1)]
certificate = sp.expand(F21-F20-t*F31)
assert certificate == 1

print("LAMBDA_2=0 EXACT Q-CERTIFICATE: PASS")
print("F21 - F20 - lambda_3*F31 = 1")
print("the complete simultaneous-shear lift/bracket system is EMPTY on lambda_2=0")
