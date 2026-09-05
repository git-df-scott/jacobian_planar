import pickle, sympy as sp
d = pickle.load(open('e1.pkl','rb'))
conds = d['conds']
F = sp.symbols('F1:8')
lines = []
for n, e in conds:
    e = sp.expand(sp.together(e) * sp.denom(sp.together(e)))
    e = sp.expand(sp.numer(sp.cancel(sp.together(sp.factor(e)))))
    lines.append(sp.srepr)  # placeholder
polys = []
for n, e in conds:
    e = sp.factor(e)
    # strip rational content
    num, den = sp.fraction(sp.together(e))
    p = sp.Poly(sp.expand(num), *F)
    c = sp.gcd(list(p.coeffs()))
    p = sp.Poly(sp.expand(num / c), *F)
    polys.append(sp.expand(p.as_expr()))
txt = "ring R = 0, (F1,F2,F3,F4,F5,F6,F7), dp;\nideal I =\n"
txt += ",\n".join(str(p).replace('**','^') for p in polys) + ";\n"
open('e1_gens.sing','w').write(txt)
print("wrote", len(polys), "generators")
