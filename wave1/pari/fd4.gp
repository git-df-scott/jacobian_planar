default(parisize, 8000000000);
f = read("/home/user/jacobian_planar/wave1/edgeQ_eliminant.txt");
print("primitive integer poly, degree ", poldegree(f), ", content ", content(f));
show(p) = my(F, ds); F = factormod(f, p); ds = vector(matsize(F)[1], i, poldegree(F[i,1])); if(vecmax(vector(matsize(F)[1], i, F[i,2]))>1, print(p, ": NOT squarefree mod p -- skipped"), print(p, ": ", vecsort(ds)); write("/tmp/degs2.txt", ds));
show(100003); show(100019); show(100043); show(100057); show(100069); show(100103); show(100109); show(100129);
quit;
