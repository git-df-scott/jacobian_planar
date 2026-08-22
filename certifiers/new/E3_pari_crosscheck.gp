\\ E3 - INDEPENDENT PARI/GP CROSS-CHECK OF THE ENDGAME CLASSIFICATION.
\\ No code shared with the sympy certifier E2.  Exact rational arithmetic.
default(parisize, 800000000);
PASS = 0; FAILN = 0;
chk(name, cond) = {if(cond, PASS++; print("  [PASS] ", name), FAILN++; print("  [FAIL] ", name));}
T(R, D, m) = (v+1)^m * (3*v*(v+1)*deriv(R, v) - D*R);
Ssol(D, m, kap) = {my(s = vector(m+1), t); s[1] = -kap/D; for(n = 1, m, t = 3*n - D; if(t == 0, return(0)); s[n+1] = (3*(m+1-n)/t) * s[n]); sum(n = 0, m, s[n+1]*v^n);}
S13 = Ssol(13, 4, 1);
R13 = S13/(v+1)^4;
print("  PARI  S(v) = ", S13);
print("  PARI  R(v) = ", R13);
chk("T_{13,4}(R) == 1 exactly (PARI)", T(R13, 13, 4) == 1);
chk("S(-1) == -1  (pole order exactly 4)", subst(S13, v, -1) == -1);
chk("deg S == 4", poldegree(S13, v) == 4);
chk("map-degree of R == 4", max(poldegree(numerator(R13), v), poldegree(denominator(R13), v)) == 4);
chk("R is not a polynomial", poldegree(denominator(R13), v) > 0);
chk("R has no pole at v=0", subst(denominator(R13), v, 0) != 0);
chk("PARI S13 == -(243v^4 - 81v^3 + 54v^2 - 42v + 35)/455", S13 == -(243*v^4 - 81*v^3 + 54*v^2 - 42*v + 35)/455);
\\ --- independent brute force by exact linear algebra over Q ---------------
brute(D, m, K, L, dg, kap) = {my(polys = List(), maxdeg = 0, M, rhs, rhsP, sol, ker, P, N); for(j = 0, dg, N = (v+1)^m*(3*(deriv(v^j, v)*v*(v+1) - v^j*(K*v + L*(v+1))) - D*v^j); listput(polys, N); maxdeg = max(maxdeg, poldegree(N, v))); rhsP = kap*(v+1)^K*v^L; maxdeg = max(maxdeg, poldegree(rhsP, v)); M = matrix(maxdeg+1, dg+1, r, c, polcoeff(polys[c], r-1, v)); rhs = vectorv(maxdeg+1, r, polcoeff(rhsP, r-1, v)); sol = matinverseimage(M, rhs); if(type(sol) != "t_COL" || #sol != dg+1, return([-1])); ker = matker(M); P = sum(j = 0, dg, sol[j+1]*v^j); [matsize(ker)[2], P/((v+1)^K*v^L)];}
testrow(D, m) = {my(K = 10, L = 3, dg = 16, r, pred, got, j, RR, nn, dd); r = brute(D, m, K, L, dg, 1); if(D % 3 != 0, pred = ["unique", m], j = D/3; if(j > m, pred = ["line", j], pred = ["none", -1])); if(r[1] < 0, got = ["none", -1], RR = r[2]; nn = poldegree(numerator(RR), v); dd = poldegree(denominator(RR), v); got = [if(r[1] == 0, "unique", "line"), max(nn, dd)]; if(r[1] > 0, got[2] = D/3)); print("    D=", D, " m=", m, "  predicted ", pred, "   PARI ", got); chk(Str("PARI brute force agrees at D=", D, ", m=", m), pred == got);}
print(""); print("  --- PARI brute force vs THEOREM (E2) ---");
V = [[13,4],[23,4],[11,4],[14,4],[7,4],[1,4],[2,4],[5,4],[4,4],[8,4],[12,4],[15,4],[18,4],[21,4],[3,4],[6,4],[9,4],[13,1],[13,2],[13,3],[13,5],[13,6],[23,6],[5,2],[6,2],[9,2],[3,1],[6,1]];
for(i = 1, #V, testrow(V[i][1], V[i][2]));
print(""); print(Str("E3: PASS = ", PASS, "   FAIL = ", FAILN));
if(FAILN > 0, error("E3 FAILED"));
quit(0);
