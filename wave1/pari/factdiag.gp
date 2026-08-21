default(parisize, 8000000000);
f = read("/home/user/jacobian_planar/wave1/edgeQ_eliminant.txt");
print("degree: ", poldegree(f), "   squarefree: ", issquarefree(f));
\\ Cheap, sound diagnostic: factor mod several good primes.  The Q-factorisation
\\ degrees must be sums of the mod-p degrees for EVERY p, so if f is irreducible
\\ mod any one p it is irreducible over Q, and in general the mod-p patterns
\\ bound how f can split.
lc = polcoef(f, poldegree(f));
forprime(p = 100003, 100060,
  if(Mod(lc,p) != 0,
    F = factormod(f*Mod(1,p));
    ds = vecsort(vector(#F[,1], i, poldegree(F[i,1])));
    print("  p = ", p, "  #factors = ", #F[,1], "  degrees(first 12) = ", vecextract(ds, "1..", if(#ds>12,12,#ds)));
  );
);
quit;
