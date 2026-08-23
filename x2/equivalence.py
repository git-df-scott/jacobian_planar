"""Certificate that the graded system and the campaign system p108_525122 have
the SAME solution set.

The argument has two halves; both are checked here mechanically.

ALGEBRA.  The campaign system determines Q from P by the cascade with Q_0 = 0,
and imposes "Q's coefficients outside the windows vanish".  The graded system
POSITS a Q whose support is inside the windows and imposes {P,Q} = x^2.  These
agree because the cascade solution is unique given Q_0 = 0:
  (<=) graded solved  =>  that Q satisfies {P,Q}=x^2 and Q_0=0, so it IS the
       cascade's Q, and its support lies in the windows;
  (=>) campaign solved =>  the cascade's Q has support in the windows, hence is
       of graded form, hence the level residuals vanish.
The identity {P_rho,Q_sigma} = y^(1-rho-sigma)(rho f g' - sigma f' g) and the
coefficientwise levels are checked in verify.py (PASS).

COMBINATORICS (checked below).  The graded ansatz's support must be exactly the
union of the campaign windows -- for P, for Q, and Q must have no y^0 part.
"""
import sys
import sympy as sp
sys.path.insert(0, '/home/user/jacobian_planar/x2')
import gsys, singspec

SPEC = '/home/user/jacobian_planar/x2/c19711d9c1808fefd6c0a8236cf67dfbe61b4764.sing'
spec = singspec.parse(SPEC)

# --- P ---
spec_P = set()
cindex = {}
for j, d in enumerate(spec['Pd']):
    for e, expr in d.items():
        spec_P.add((e, j))
        cindex[(e, j)] = list(expr.free_symbols)[0]

graded_P = set()
label = {}
for name, n_coeff, start, rho in (('F', gsys.dF + 1, 1, 2),
                                  ('A', gsys.dA + 1, 1, 1),
                                  ('B', gsys.dB + 1, 0, 0)):
    for i in range(n_coeff):
        n = start + i
        graded_P.add((n, 2 * n - rho))
        label[(n, 2 * n - rho)] = f'{name}{i}'

# --- Q ---
spec_Q = set()
for k, w in spec['windows'].items():
    if w is None:
        continue
    lo, hi = w
    for e in range(lo, hi + 1):
        spec_Q.add((e, k))

graded_Q = set()
for n_coeff, start, sigma in ((gsys.dG + 1, 2, 3), (gsys.dG2 + 1, 2, 2),
                              (gsys.dG1 + 1, 1, 1), (gsys.dG0 + 1, 1, 0)):
    for i in range(n_coeff):
        n = start + i
        graded_Q.add((n, 2 * n - sigma))

checks = []
checks.append(("supp(P) ansatz == union of campaign Pd windows", spec_P == graded_P))
checks.append(("supp(Q) ansatz == union of campaign Q windows", spec_Q == graded_Q))
checks.append(("Q has no y^0 part (matches Q_0 = 0)",
               not any(k == 0 for _, k in graded_Q)))
nd = [cindex_key for cindex_key, s in cindex.items()
      if s in [spec['c'][i - 1] for i in spec['nd']]]
checks.append(("nondegeneracy vertices are (1,0),(8,14),(8,16)",
               sorted(nd) == [(1, 0), (8, 14), (8, 16)]))
checks.append(("their graded labels are F0, F7, B8",
               sorted(label[v] for v in nd) == ['B8', 'F0', 'F7']))
checks.append(("p10 (the vertex (1,0) coefficient) is F0, normalised to 1",
               label[(1, 0)] == 'F0'))
checks.append(("bracket is +x^2", spec['Rr'][0] == {2: 1}
               and all(not d for d in spec['Rr'][1:])))

for name, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if spec_P != graded_P:
    print("  P sym diff:", sorted(spec_P ^ graded_P))
if spec_Q != graded_Q:
    print("  Q sym diff:", sorted(spec_Q ^ graded_Q))
print("EQUIVALENCE:", "PASS" if all(o for _, o in checks) else "FAIL")
