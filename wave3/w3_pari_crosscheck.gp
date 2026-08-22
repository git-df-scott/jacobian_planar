\\ w3_pari_crosscheck.gp - six sample cells of the adjudication grid, in PARI/GP.
\\ Independent of every python script.  Exact rational arithmetic, c set to 1.
default(parisize, 400000000);
P = 0; F = 0;
ck(n, b) = {if(b, P++; print("  [PASS] ", n), F++; print("  [FAIL] ", n));}
T(R, D, k) = (v+1)^k*(3*v*(v+1)*deriv(R, v) - D*R);
\\ solve T(R,D,k) = -1 for R = N(v)/(v+1)^m, deg N <= n, by exact linear algebra
cell(D, k, m, n) = {my(cols = List(), md = 0, M, rhs, sol, ker, N, Nn); for(j = 0, n, N = (v+1)^k*(3*(deriv(v^j,v)*v*(v+1) - v^j*m*v) - D*v^j); listput(cols, N); md = max(md, poldegree(N, v))); rhs = -(v+1)^m; md = max(md, poldegree(rhs, v)); M = matrix(md+1, n+1, r, cc, polcoeff(cols[cc], r-1, v)); rhs = vectorv(md+1, r, polcoeff(-(v+1)^m, r-1, v)); sol = matinverseimage(M, rhs); if(type(sol) != "t_COL" || #sol != n+1, return([-1])); ker = matker(M); Nn = sum(j = 0, n, sol[j+1]*v^j); [matsize(ker)[2], Nn/(v+1)^m];}
md(R) = {my(a = numerator(R), b = denominator(R)); max(poldegree(a, v), poldegree(b, v));}
boxm(D, k) = max(max(k, if(D % 3 == 0, D/3, 0)), 1);
run(D, k, expst, expdeg) = {my(bm = boxm(D, k), r = cell(D, k, bm, bm+4), st, dg); if(r[1] < 0, st = "none"; dg = -1, st = if(r[1] == 0, "unique", "family"); dg = md(r[2]); if(st == "unique", ck(Str("D=",D," k=",k," substitution gives exactly -1"), T(r[2], D, k) == -1))); print("    D=", D, " k=", k, " -> ", st, "  map-degree ", dg); ck(Str("D=", D, ", k=", k, " agrees with the python grid"), st == expst && (expdeg < 0 || dg == expdeg));}
print("  --- six sample cells, PARI/GP ---");
run(13, 4, "unique", 4);
run(23, 4, "unique", 4);
run(12, 4, "none", -1);
run(15, 4, "family", -1);
run(1, 1, "unique", 1);
run(13, 13, "unique", 13);
print(""); print(Str("w3_pari_crosscheck: PASS = ", P, "  FAIL = ", F));
if(F > 0, error("PARI cross-check FAILED"));
quit(0);
