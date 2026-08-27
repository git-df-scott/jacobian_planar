"""Bottom-level (w-minimal) core system for open subcase 2, exact.

 [P^(-2), Q^(-3)] = x^2   <=>   2 f2 g3' - 3 f2' g3 = t^2
 with f2 = t*A(t), deg A = 7 ; g3 = t^2*B(t), deg B = 10
 <=>  sum_{i+j=k} (1+2j-3i) A_i B_j = [k==0],  k = 0..17  (k=17 vacuous).
"""
import sympy as sp
A=[sp.Symbol(f"A{i}") for i in range(8)]
B=[sp.Symbol(f"B{j}") for j in range(11)]
eqs=[]
for k in range(0,18):
    e=sum((1+2*j-3*i)*A[i]*B[j] for i in range(8) for j in range(11) if i+j==k)
    e=sp.expand(e-(1 if k==0 else 0))
    eqs.append(e)
if __name__=="__main__":
    for k,e in enumerate(eqs):
        print(k, e)
