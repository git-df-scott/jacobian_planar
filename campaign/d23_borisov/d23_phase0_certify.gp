\\ Plane Jacobian campaign - Session N2, Phase 0 (PARI/GP exact ledger)
\\ D=23 Second Framework (-2)-curve Belyi map: full certification over
\\ K = Q[w]/(f), f irreducible of degree 15 (all 15 dessins at once).
\\ Run:  gp -q d23_phase0_certify.gp < /dev/null
\\ Variable priorities: x (Belyi parameter t) > y (b0 unknown) > w (field gen).

f = 219667417263*w^15 + 8420584328415*w^14 + 151570517911470*w^13 + 1699502624702820*w^12 + 13273524003701970*w^11 + 76456374411324330*w^10 + 335086960286980080*w^9 + 1134575058498085080*w^8 + 2976589985569280190*w^7 + 5999062805992824390*w^6 + 9088367576724803808*w^5 + 9941860073485256400*w^4 + 7296761536003866960*w^3 + 3067536989980774080*w^2 + 401854216485173760*w - 115156208770167488;

print("f irreducible over Q: ", polisirreducible(f));
print("number of real roots of f (expect 3 = symmetric dessins): ", polsturm(f));

be = Mod(w, f);  \\ beta = b1

\\ triangular chain from the master equation L = 23(t-1)^6, coeffs t^5..t^2
A3(b0) = -(18*be + 138)/20;
A2(b0) = -(15*A3(b0)*be + 13*b0 - 345)/17;
A1(b0) = -(12*A2(b0)*be + 10*A3(b0)*b0 + 460)/14;
A0(b0) = -(9*A1(b0)*be + 7*A2(b0)*b0 - 345)/11;
E1 = 6*A0(y)*be + 4*A1(y)*y + 138;   \\ [t^1]
E2 = A0(y)*y - 23;                   \\ [t^0]
g = gcd(E1, E2);
print("gcd(E1,E2) degree in y (expect 1 => unique b0 per root): ", poldegree(g, y));
b0 = -polcoef(g, 0, y)/polcoef(g, 1, y);
b1 = be;
a3 = A3(b0); a2 = A2(b0); a1 = A1(b0); a0 = A0(b0);

a = x^4 + a3*x^3 + a2*x^2 + a1*x + a0;
b = x^2 + b1*x + b0;

\\ ===== CERTIFICATION LEDGER (all exact over K; K a field, so any =====
\\ ===== nonzero element is a valid nonvanishing certificate)       =====
L = a*b + 3*x*deriv(a,x)*b + 5*x*a*deriv(b,x);
print("[", if(L - 23*(x-1)^6 == 0,"PASS","FAIL"), "] master identity  L == 23(t-1)^6");
print("[", if(poldisc(a,x) != 0,"PASS","FAIL"), "] a squarefree (disc != 0 in K)");
print("[", if(poldisc(b,x) != 0,"PASS","FAIL"), "] b squarefree (disc != 0 in K)");
print("[", if(polresultant(a,b,x) != 0,"PASS","FAIL"), "] gcd(a,b)=1  (Res != 0)");
a1v = subst(a,x,1); b1v = subst(b,x,1);
print("[", if(a1v != 0 && b1v != 0,"PASS","FAIL"), "] a(1) != 0, b(1) != 0");
print("[", if(a0*b0 == 23,"PASS","FAIL"), "] a(0)b(0) = 23  (0-fiber avoids t=0 collision & t=1)");

c = 1/(a1v^3*b1v^5);
B = c*x*a^3*b^5;
D1 = B - 1;
q7 = (x-1)^7;
s = D1 \ (c*q7);
print("[", if(D1 - c*q7*s == 0,"PASS","FAIL"), "] B - 1 == c(t-1)^7 s  exactly");
print("[", if(poldegree(s,x) == 16,"PASS","FAIL"), "] deg s = 16");
print("[", if(subst(s,x,1) != 0,"PASS","FAIL"), "] s(1) != 0  (order at t=1 exactly 7)");
print("[", if(poldisc(s,x) != 0,"PASS","FAIL"), "] s squarefree (16 simple points above 1)");
print("[", if(polresultant(s, x*a*b, x) != 0,"PASS","FAIL"), "] 1-fiber disjoint from 0-fiber");
print("[", if(poldegree(B,x) == 23,"PASS","FAIL"), "] deg B = 23 (unique pole at infinity, order 23)");
print();
print("Profile certified: {0}: 1x1 (t=0) + 4x3 (roots of a) + 2x5 (roots of b);");
print("{1}: 1x7 (t=1) + 16x1 (roots of s); {inf}: 1x23.  All 15 embeddings at once.");
print("GP LEDGER DONE");
