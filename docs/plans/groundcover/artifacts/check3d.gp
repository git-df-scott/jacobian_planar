default(parisize, 2*10^9);
F = "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave1/edgeQ_eliminant.txt";
f = extern(Str("cat ", F));
ded(p) = my(fa, degs, mu, t); gettime(); fa = factormod(f, p); degs = vector(matsize(fa)[1], k, poldegree(fa[k,1])); mu = vector(matsize(fa)[1], k, fa[k,2]); t = gettime(); print("DED p=", p, " nfac=", #degs, " ms=", t, " maxmult=", vecmax(mu), " degs=", vecsort(degs));
ded(100189); ded(100193); ded(100207); ded(100213); ded(100237);
quit;
