\\ E8 - INDEPENDENT PARI/GP CROSS-CHECK OF THE ALPOGE MAP AND ITS DESCENT.
\\ No code shared with the sympy certifier E7.
default(parisize, 800000000);
PASS = 0; FAILN = 0;
chk(name, cond) = {if(cond, PASS++; print("  [PASS] ", name), FAILN++; print("  [FAIL] ", name));}
f1 = (1 + x*y)^3*z + y^2*(1 + x*y)*(4 + 3*x*y);
f2 = y + 3*x*(1 + x*y)^2*z + 3*x*y^2*(4 + 3*x*y);
f3 = 2*x - 3*x^2*y - x^3*z;
d(f, t) = deriv(f, t);
JF = [d(f1,x), d(f1,y), d(f1,z); d(f2,x), d(f2,y), d(f2,z); d(f3,x), d(f3,y), d(f3,z)];
chk("det JF == -2 (PARI)", matdet(JF) == -2);
ev(f, a, b, cc) = subst(subst(subst(f, x, a), y, b), z, cc);
im(a, b, cc) = [ev(f1,a,b,cc), ev(f2,a,b,cc), ev(f3,a,b,cc)];
A = im(0, 0, -1/4); B = im(1, -3/2, 13/2); C = im(-1, 3/2, 13/2);
print("  PARI  F(0,0,-1/4) = ", A);
print("  PARI  F(1,-3/2,13/2) = ", B);
print("  PARI  F(-1,3/2,13/2) = ", C);
chk("three distinct rational points collide (PARI)", A == B && B == C && A == [-1/4, 0, 0]);
\\ equivariance: substitute x->L*x, y->y/L, z->z/L^2 and compare with L^w * f
eq(f, wgt) = {my(g = subst(subst(subst(f, x, L*x), y, y/L), z, z/L^2)); numerator(g - L^wgt*f) == 0;}
chk("weight -2 on f1 (PARI)", eq(f1, -2));
chk("weight -1 on f2 (PARI)", eq(f2, -1));
chk("weight  1 on f3 (PARI)", eq(f3,  1));
\\ descent: substitute y -> u/x, z -> w/x^2 into f1*f3^2 and f2*f3
dec(f) = {my(g = subst(subst(f, y, u/x), z, w/x^2)); g = numerator(g)/denominator(g); g;}
G1 = dec(f1*f3^2); G2 = dec(f2*f3);
chk("G1 is x-free (PARI)", deriv(G1, x) == 0);
chk("G2 is x-free (PARI)", deriv(G2, x) == 0);
JG = [deriv(G1,u), deriv(G1,w); deriv(G2,u), deriv(G2,w)];
DJ = matdet(JG);
print("  PARI  det JG = ", DJ);
chk("det JG == -2 (3u + w - 2)^2 (PARI)", DJ == -2*(3*u + w - 2)^2);
chk("det JG is not constant (PARI)", deriv(DJ, u) != 0);
g1q(a, bb) = subst(subst(G1, u, a), w, bb);
g2q(a, bb) = subst(subst(G2, u, a), w, bb);
chk("quotient collision G(0,0) == G(-3/2,13/2) (PARI)", [g1q(0,0), g2q(0,0)] == [g1q(-3/2,13/2), g2q(-3/2,13/2)]);
chk("(-3/2,13/2) lies on 3u+w-2 = 0 (PARI)", 3*(-3/2) + 13/2 - 2 == 0);
chk("(0,0) does not (PARI)", 3*0 + 0 - 2 != 0);
print(""); print(Str("E8: PASS = ", PASS, "   FAIL = ", FAILN));
if(FAILN > 0, error("E8 FAILED"));
quit(0);
