"""Build an exact number-field lower descent from the saved leading lex basis."""
from pathlib import Path
import re
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
cs=s.symbols('c3:9')
a=s.Symbol('a')
raw=(ROOT/'astra/artifacts/case2_exact_modular_lex.txt').read_text()
polys=[s.sympify(re.sub(r'c\((\d+)\)',r'c\1',p).replace('^','**')) for p in raw.strip().split(',')]
minimal=s.Poly(polys[0],cs[-1])
assert minimal.degree()==5
assert minimal.is_irreducible
print('exact quintic irreducible over Q',flush=True)
vals={1:s.Integer(1),2:s.Integer(1),8:a}
for k in range(3,8):
    symbol=s.Symbol('c'+str(k))
    p=next(p for p in polys if symbol in p.free_symbols)
    vals[k]=s.expand(-p.subs(symbol,0)/p.coeff(symbol)).subs(cs[-1],a)
def fmt(p):
    # Singular's algebraic-number parser needs division outside the exponent.
    terms=[]
    for (k,),c in s.Poly(p,a).terms():
        num,den=c.as_numer_denom()
        terms.append('('+str(num)+'/'+str(den)+')*(a^'+str(k)+')')
    return '+'.join(terms) or '0'
head='''// Exact lower descent over the irreducible quintic leading field.
ring R=(0,a),(B(1..8),b0,b1,z,T),(dp(8),dp(3),dp(1));
option(redSB);
short=0;
minpoly=MINPOLY;
poly C=CPOLY;
proc cf(poly p,int k){
  matrix M=coeffs(p,T);
  if(k+1>nrows(M)){return(poly(0));}
  return(M[k+1,1]);
}
proc coefficients(poly p){
  matrix M=coeffs(p,T);ideal I;
  int k;for(k=1;k<=nrows(M);k++){I=I+M[k,1];}
  return(simplify(I,2));
}
poly G=0;poly residual;int n;
for(n=2;n<=12;n++){
  residual=2*C*diff(G,T)-3*diff(C,T)*G-T^2;
  G=G-cf(residual,n)*T^n/(2*n-3);
}
if(2*C*diff(G,T)-3*diff(C,T)*G-T^2!=0){ERROR("leading identity failed");quit;}
"LEADING_IDENTITY_EXACT";
// Complete solution of level four in the prescribed polynomial windows.
poly B=b0*(diff(C,T)-C/T)+b1*(T*diff(C,T)-3*C/2);
poly F=b0*(diff(G,T)-3*G/(2*T)-C/2)+b1*(T*diff(G,T)-9*G/4);
if(2*C*diff(F,T)-2*diff(C,T)*F+B*diff(G,T)-3*diff(B,T)*G!=0){ERROR("level four identity failed");quit;}
"LEVEL_FOUR_EXACT";
poly A=0;for(n=1;n<=8;n++){A=A+B(n)*T^n;}
poly E=0;
poly source=B*diff(F,T)-2*diff(B,T)*F-3*diff(A,T)*G;
for(n=1;n<=12;n++){
  residual=2*C*diff(E,T)-diff(C,T)*E+source;
  E=E-cf(residual,n)*T^n/(2*n-1);
}
ideal level3=coefficients(2*C*diff(E,T)-diff(C,T)*E+source);
"LEVEL_THREE_EQUATIONS="+string(size(level3));
ideal K=std(level3);
write(":w astra/artifacts/case2_exact_level3_basis.txt",string(K));
"LEVEL_THREE_BASIS="+string(size(K));
poly An=reduce(A,K);
poly En=reduce(E,K);
poly D=0;
source=B*diff(En,T)-diff(B,T)*En-2*diff(An,T)*F;
for(n=1;n<=12;n++){
  residual=2*C*diff(D,T)+source;
  D=D-cf(residual,n)*T^n/(2*n);
  D=reduce(D,K);
}
ideal bottom=coefficients(reduce(2*C*diff(D,T)+source,K))
             +coefficients(reduce(B*diff(D,T)-diff(An,T)*En,K));
bottom=simplify(bottom,2);
"BOTTOM_EQUATIONS="+string(size(bottom));
write(":w astra/artifacts/case2_exact_bottom_input.txt",string(bottom));
poly corner=reduce(B(8),K);
write(":w astra/artifacts/case2_exact_corner.txt",string(corner));
ideal I=bottom+ideal(z*corner-1);
ideal H=std(I);
write(":w astra/artifacts/case2_exact_bottom_basis.txt",string(H));
"BOTTOM_DIM="+string(dim(H));
"BOTTOM_SIZE="+string(size(H));
if(size(H)==1 && H[1]==1){"CASE2_EXACT_Q_EMPTY";}
else{"CASE2_EXACT_Q_SURVIVOR_OR_UNRESOLVED";}
quit;
'''
head=head.replace('MINPOLY',fmt(minimal.as_expr().subs(cs[-1],a)))
head=head.replace('CPOLY','+'.join('('+fmt(vals[i])+')*T^'+str(i) for i in range(1,9)))
(ROOT/'astra/case2_exact_descent.sing').write_text(head)
certificate_block='''if(size(H)==1 && H[1]==1){
 "CASE2_EXACT_Q_EMPTY";
 matrix cert=lift(I,H);
 ideal discrepancy=ideal(matrix(I)*cert-matrix(H));
 "BOTTOM_CERTIFICATE_RESIDUAL="+string(size(simplify(discrepancy,2)));
 write(":w astra/artifacts/case2_exact_bottom_certificate.txt",string(cert));
}'''
certificate_head=head.replace('if(size(H)==1 && H[1]==1){"CASE2_EXACT_Q_EMPTY";}',certificate_block)
assert certificate_head != head
(ROOT/'astra/case2_exact_descent_certificate.sing').write_text(certificate_head)
print('wrote lower descent and certificate producer',flush=True)
