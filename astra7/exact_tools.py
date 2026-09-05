"""Small exact helpers shared by the two live-system certificates."""
import sympy as s

def zero(expression):
    assert s.cancel(s.expand(expression)) == 0, expression

def polynomial_part_power(P, exponent, x):
    """Finite exact polynomial part for a monic P at x=infinity."""
    P=s.Poly(P,x)
    assert P.LC()==1
    n=P.degree()
    degree=s.Rational(exponent)*n
    assert degree.is_Integer and degree>=0
    degree=int(degree)
    z=s.Dummy('inverse_x')
    small=s.Poly(sum(coef*z**(n-i[0]) for i,coef in P.terms() if i[0]<n),z)
    power=s.Poly(1,z)
    out={0:s.Integer(1)}
    for j in range(1,degree+1):
        raw=power*small
        power=s.Poly.from_dict({mon:coef for mon,coef in raw.terms()
                               if mon[0]<=degree},z)
        for (i,),coef in power.terms():
            out[i]=out.get(i,0)+s.binomial(exponent,j)*coef
    return s.expand(sum(coef*x**(degree-i) for i,coef in out.items()))

def derivative_operator(variables, derivatives):
    return lambda expression:sum(s.diff(expression,v)*dv
                                 for v,dv in zip(variables,derivatives))
