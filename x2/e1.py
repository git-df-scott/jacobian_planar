"""E1:  2 f2 g3' - 3 f2' g3 = T^2   with f2 = T*F (deg F = 7, F0 = 1),
g3 = T^2*G (deg G = 10).  Reduces to  sum_{i+j=n} (1+2j-3i) F_i G_j = delta_{n0}.
Triangular in G for n <= 10; n = 11..16 are conditions on F alone."""
import sympy as sp

dF, dG = 7, 10
F = [sp.Integer(1)] + list(sp.symbols(f'F1:{dF+1}'))
Gs = sp.symbols(f'G0:{dG+1}')
G = list(Gs)

sub = {}
conds = []
for n in range(0, dF + dG + 1):
    e = 0
    for i in range(0, dF + 1):
        j = n - i
        if 0 <= j <= dG:
            e += (1 + 2 * j - 3 * i) * F[i] * G[j]
    e = sp.expand(e - (1 if n == 0 else 0))
    e = sp.expand(e.subs(sub))
    if n <= dG:
        a = sp.expand(sp.diff(e, Gs[n]))
        assert a == 1 + 2 * n, (n, a)
        val = sp.expand(-(e - a * Gs[n]) / a)
        sub[Gs[n]] = val
        for k in list(sub):
            sub[k] = sp.expand(sub[k].subs({Gs[n]: val}))
    else:
        e = sp.expand(e)
        if e != 0:
            conds.append((n, sp.factor(e)))

print("G determined by F:")
for k in Gs:
    print(f"  {k} = {sp.factor(sub[k])}")
print()
print(f"{len(conds)} conditions on F_1..F_7:")
for n, e in conds:
    print(f"  [T^{n}]  {e}")
import pickle
pickle.dump({'sub': sub, 'conds': conds, 'F': F, 'G': Gs},
            open('/home/user/jacobian_planar/x2/e1.pkl', 'wb'))
