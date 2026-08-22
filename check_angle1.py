# Angle 1 control: the ladder identity
#   sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2
# is EXACTLY the coefficient expansion of
#   H_s (w G_w) - (w H_w) G_s = s^2 w^-2
# with H = sum h_a(s) w^a, G = sum g_b(s) w^b.
import sympy as sp, random
s, w = sp.symbols('s w')
random.seed(7)
# random Laurent supports a in [-1..4], b in [-1..5], random poly coeffs
ha = {a: sp.Poly([random.randint(-5,5) for _ in range(4)], s).as_expr() for a in range(-1,5)}
gb = {b: sp.Poly([random.randint(-5,5) for _ in range(4)], s).as_expr() for b in range(-1,6)}
H = sum(h*w**a for a,h in ha.items()); G = sum(g*w**b for b,g in gb.items())
lhs = sp.expand(sp.diff(H,s)*w*sp.diff(G,w) - w*sp.diff(H,w)*sp.diff(G,s))
# coefficient of w^L from generating function vs direct ladder sum
ok = True
for L in range(-3, 10):
    gf = sp.expand(lhs.coeff(w, L))
    ladder = sp.expand(sum(b*sp.diff(ha[a],s)*gb[b] - a*ha[a]*sp.diff(gb[b],s)
                 for a in ha for b in gb if a+b==L))
    if sp.simplify(gf - ladder) != 0: ok=False; print("MISMATCH at L=",L)
print("generating-function identity matches ladder at all L:", ok)
# gauge control: h_{-1}=s, g_{-1}=s^2 alone -> L=-2 gives s^2
print("gauge control:", sp.expand((-1)*sp.diff(s,s)*s**2 - (-1)*s*sp.diff(s**2,s)) == s**2)
# cover statement control: dH^dG in (s,theta), w=exp(theta): substitute numerically
th = sp.symbols('theta')
Ht = H.subs(w, sp.exp(th)); Gt = G.subs(w, sp.exp(th))
jac = sp.expand(sp.diff(Ht,s)*sp.diff(Gt,th) - sp.diff(Ht,th)*sp.diff(Gt,s))
# this should equal lhs with w=e^theta
print("Jacobian-in-(s,theta) equals torus bracket:", sp.simplify(jac - lhs.subs(w, sp.exp(th))) == 0)
