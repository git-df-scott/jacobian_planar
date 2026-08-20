default(parisize, 8000000000);
f = read("/home/user/jacobian_planar/wave1/edgeQ_eliminant.txt");
print("degree: ", poldegree(f), "  squarefree: ", issquarefree(f));
lc = polcoef(f, poldegree(f));
diag(p) = my(F, ds); if(Mod(lc,p)==0, return(0)); F = factormod(f, p); ds = vecsort(vector(matsize(F)[1], i, poldegree(F[i,1]))); print("  p=", p, "  #factors=", matsize(F)[1], "  min/max deg=", ds[1], "/", ds[#ds], "  first 10: ", vecextract(ds, Str("1..", min(10,#ds))));
diag(100003);
diag(100019);
diag(100043);
quit;
