#!/usr/bin/env python3
"""Exact right-edge consequence of degree-144 reverse polynomiality.

The four highest pole rows of the driver and three of the partner do not
contain lambda_2 or lambda_3.  Exact rational row reduction forces their
rightmost columns to be fourth and third powers respectively.  This is a
necessary condition on the entire simultaneous-shear chart lambda_4 != 0.
"""
from fractions import Fraction as F


def rref(a):
    a = [[F(x) for x in row] for row in a]
    row = 0
    pivots = []
    for col in range(len(a[0])):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [x/scale for x in a[row]]
        for r in range(len(a)):
            if r != row and a[r][col]:
                scale = a[r][col]
                a[r] = [x-scale*y for x, y in zip(a[r], a[row])]
        pivots.append(col)
        row += 1
    return a, pivots


def kernel_vector(matrix):
    rr, pivots = rref(matrix)
    free = [c for c in range(len(matrix[0])) if c not in pivots]
    assert len(free) == 1
    v = [F(0)]*len(matrix[0])
    v[free[0]] = F(1)
    for row, pivot in enumerate(pivots):
        v[pivot] = -rr[row][free[0]]
    return v


driver = [
    [1, -1, 1, -1, 1],
    [-12, 13, -14, 15, -16],
    [66, -78, 91, -105, 120],
    [-220, 286, -364, 455, -560],
]
partner = [
    [-1, 1, -1, 1],
    [9, -10, 11, -12],
    [-36, 45, -55, 66],
]

dv = kernel_vector(driver)
ov = kernel_vector(partner)
assert dv == list(map(F, [1, 4, 6, 4, 1]))
assert ov == list(map(F, [1, 3, 3, 1]))

print("EXACT RIGHT-EDGE CERTIFICATE: PASS")
print("driver row 16 = A*y^12*(1+y)^4")
print("partner row 12 = B*y^9*(1+y)^3")
print("independent of lambda_2 and lambda_3 on lambda_4=1")
