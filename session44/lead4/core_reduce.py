"""Triangular reduction of the core system.

Equation k:  sum_{i+j=k} (1+2j-3i) A_i B_j = [k==0],  k=0..16.
The B_k coefficient in equation k is (1+2k) A_0 != 0, so B_0..B_10 are
determined RECURSIVELY by A_0..A_7 (k=0..10).  Equations k=11..16 are then
6 polynomial conditions on A alone.  Gauge: A_0 = 1 (scaling of P,Q) and
A_7 = 1 (scaling of t; A_7 != 0 is the driver vertex (8,14)).
"""
import sympy as sp

def build(gauge_A7=True):
    A = [sp.Integer(1)] + [sp.Symbol(f"A{i}") for i in range(1, 8)]
    if gauge_A7:
        A[7] = sp.Integer(1)
    B = [None]*11
    for k in range(11):
        # (1+2k)A_0 B_k + sum_{i>=1,i+j=k} (1+2j-3i) A_i B_j = [k==0]
        rest = sp.Add(*[(1+2*j-3*i)*A[i]*B[j] for i in range(1, min(k, 7)+1)
                        for j in [k-i] if 0 <= j <= 10 and B[j] is not None])
        B[k] = sp.expand((sp.Integer(1 if k == 0 else 0) - rest)*sp.Rational(1, 1+2*k))
    conds = []
    for k in range(11, 17):
        e = sp.expand(sum((1+2*j-3*i)*A[i]*B[j] for i in range(8)
                          for j in range(11) if i+j == k))
        conds.append(e)
    return A, B, conds

if __name__ == "__main__":
    A, B, conds = build()
    unk = sorted({s for c in conds for s in c.free_symbols}, key=str)
    print("unknowns:", unk)
    for k, c in zip(range(11, 17), conds):
        print(f"cond k={k}: total degree {sp.total_degree(c)}, {len(c.args) if c.is_Add else 1} terms")
    print("B10 terms:", len(sp.Poly(B[10], *unk).coeffs()))
    import json
    sp.srepr
    open("core_conds.txt","w").write("\n".join(str(c) for c in conds))
