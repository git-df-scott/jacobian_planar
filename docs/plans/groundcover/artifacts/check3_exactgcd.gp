default(parisize, 2*10^9);
F = "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave1/edgeQ_eliminant.txt";
f = extern(Str("cat ", F));
print("deg = ", poldegree(f));
gettime();
g = gcd(f, deriv(f));
print("EXACT deg_gcd_over_Q = ", poldegree(g), " ms=", gettime());
print("EXACT squarefree = ", poldegree(g) == 0);
quit;
