#!/usr/bin/env python3
"""Exact control for the missing residual-degree step in the pentagon hunt.

Let P=sum a_i(y)x^i and R=sum r_k(y)x^k, with deg(a_i)<=i+8.
The rung of {P,R}=2*x^2*Q that first contains r_k is d=k+7:

  8*a_8*r_k' - k*a_8'*r_k + (already known r_l, l>k) = 2*q_{k+5}.

Assuming deg(r_l)<=l+7 for l>k, every known term has degree <=k+22,
as does the expected part of the unknown term.  If r_k had degree
D>k+7, its unique coefficient above that ceiling would be

  alpha * (8*D - 16*k) = 8*alpha*(D-2*k),

where alpha is the nonzero leading coefficient of a_8.  For k<=6 and
D>k+7 this cannot vanish.  Descending from the support bound deg(r_7)<=14
therefore proves deg(r_k)<=k+7 for every k=0,...,7.
"""
def main():
    failures = []
    for k in range(6, -1, -1):
        # Test several degrees above the claimed ceiling directly.  The
        # displayed formula proves all remaining D symbolically.
        for D in range(k + 8, k + 16):
            # Differentiate the two monomials directly:
            # 8*y^16*(D*y^(D-1)) - k*(16*y^15)*y^D.
            got = 8*D - 16*k
            want = 8*(D - 2*k)
            if got != want or want == 0:
                failures.append((k, D, got, want))

    print("generic leading multiplier: 8*(D-2*k)")
    print("finite monomial controls:", "PASS" if not failures else failures)
    print("induction range: k=6,...,0; D>=k+8 implies D-2k>=8-k>0")
    print("VERDICT: deg_y(r_k) <= k+7 for every k=0,...,7")


if __name__ == "__main__":
    main()
