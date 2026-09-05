#!/usr/bin/env python3
"""Exact controls for the conductor/global-termination strike.

Requires SymPy. Written all-order and all-degree arguments are in
CONDUCTOR_TERMINATION.md; finite checks are not promoted to those proofs.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
v, c, r, t, a = s.symbols("v c r t a")
R = 3*c*v-2
Delta = R**2-9*c
b = -3*c*v**2+4*v+2
inv = (R*v-3)/6
z = Delta*(c*v**2-1)/4
trace = {v: 3*(r+2)/r**2, c: r**2/9}


def zero(f):
    assert s.cancel(s.expand(f)) == 0, f


def J(f, g, x=v, y=c):
    return s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x)


def restrict(f):
    return s.cancel(f.subs(trace, simultaneous=True))


def residue_at_zero(f):
    return s.residue(s.cancel(f),r,0)


def verify_global_period():
    pv, cv = trace[v], trace[c]
    source = residue_at_zero(pv*s.diff(cv,r))
    old = residue_at_zero(cv*s.diff(restrict(b),r))
    corrected = residue_at_zero(cv*s.diff(restrict(-(b+1)/2),r))
    assert (source,old,corrected) == (s.Rational(4,3),-s.Rational(8,3),s.Rational(4,3))
    # General minimal even Laurent traces: residue equals 2(B*A'-A*B').
    A,B,C,D = s.symbols("A B C D")
    p,q = A*r*r+B/r**2, C*r*r+D/r**2
    zero(residue_at_zero(p*s.diff(q,r))-2*(B*C-A*D))
    # Volume in the two global rational coordinates (r,t=Delta).
    V,Cc = 3*(r+2)/(r*r-t), (r*r-t)/9
    zero(J(V,Cc,r,t)+1/(3*(r*r-t)))
    zero(J(R,Delta)+3*(R*R-Delta))
    return {"status":"PASS", "source_residue":str(source),
            "old_trace_residue":str(old), "corrected_trace_residue":str(corrected)}


def verify_all_order_controls():
    zero(R*inv-1-Delta*v/6)
    zero(9*c*inv**2-1-z)
    zero(restrict(inv)-1/r)
    zero(restrict(z))
    results = []
    Z = s.Symbol("Z")
    for n in (1,2,3,4):
        bn = s.binomial(-s.Rational(1,2),n)
        series = sum(s.binomial(-s.Rational(1,2),j)*Z**j for j in range(n+1))
        zero(series+2*(1+Z)*s.diff(series,Z)-(2*n+1)*bn*Z**n)
        qn = -v+3*inv*series.subs(Z,z)
        error = -(R+1)*(2*n+1)*bn*z**n
        zero(J(c,qn)-1-error)
        assert error != 0
        zero(restrict(qn)+6/r**2)
        # Both coordinates vary after a target shear. Its Jacobian is the
        # same; a superficial two-coordinate-free gate must not accept it.
        pn = c+qn**2
        zero(J(pn,qn)-1-error)
        images=[]
        for vv in (-s.Rational(1,3),s.Rational(2,3)):
            images.append((pn.subs({v:vv,c:4}),qn.subs({v:vv,c:4})))
        assert images[0] == images[1] == (s.Rational(145,36),-s.Rational(1,6))
        assert s.Poly(qn,v,c).total_degree() == 7*n+3
        zero(error.subs({v:0,c:0})-(2*n+1)*s.binomial(2*n,n)/4**n)
        results.append({"order":n,"degree_Q":7*n+3,"degree_sheared_P":14*n+6,
                        "Jacobian_error_at_origin":str(error.subs({v:0,c:0})),
                        "collision": [str(x) for x in images[0]], "is_Keller":False})
    # Independent positive control: a true polynomial automorphism is outside B.
    zero(J(c,-v)-1)
    assert restrict(-v) != restrict(-v).subs(r,-r)
    return {"status":"PASS","checked_orders":results,
            "formal_limit_relation":"c*(Q_hat+v)^2=1",
            "all_order_error":"-(r+1)*(2N+1)*binomial(-1/2,N)*z^N",
            "polynomial_termination":"IMPOSSIBLE for this explicit series"}


def verify_formal_recurrence():
    ps=[s.Function('p'+str(i))(r) for i in range(5)]
    qs=[s.Function('q'+str(i))(r) for i in range(5)]
    pp=sum(ps[i]*t**i for i in range(5))
    qq=sum(qs[i]*t**i for i in range(5))
    expansion=s.expand(J(pp,qq,r,t))
    for n in range(4):
        known=sum((n+1-i)*s.diff(ps[i],r)*qs[n+1-i]
                  -i*ps[i]*s.diff(qs[n+1-i],r) for i in range(1,n+1))
        zero(expansion.coeff(t,n)-(n+1)*(s.diff(ps[0],r)*qs[n+1]
                                       -s.diff(qs[0],r)*ps[n+1])-known)
    h=s.Function('h')(r)
    zero(s.diff(ps[0],r)*(h*s.diff(qs[0],r))
         -s.diff(qs[0],r)*(h*s.diff(ps[0],r)))
    badp=r*r+1/r**2
    badq=badp**2
    zero(s.diff(badp,r).subs(r,1))
    zero(s.diff(badq,r).subs(r,1))
    assert (-1/(3*r*r)).subs(r,1) != 0
    return {"status":"PASS","checked_symbolic_orders":[0,1,2,3],
            "free_kernel_retained":True,
            "formal_existence_criterion":"(p0',q0')=C[r,r^-1]",
            "nonimmersed_control":"p=r^2+r^-2, q=p^2: impossible at r=1"}


def verify_two_punctures():
    Cc = (r*r-a*a)/9
    V = 3*(r+2)/(r*r-a*a)
    source = s.factor(s.limit((r-a)*V*s.diff(Cc,r),r,a))
    zero(source-(a+2)/3)
    oldq = -(b+1)/2
    oldq = s.cancel(oldq.subs({v:V,c:Cc},simultaneous=True))
    base = s.factor(s.residue(Cc*s.diff(oldq,r),r,a))
    zero(base-(4-a*a)/6)
    # Compute directly from the rational fibre, independently of the Jacobian
    # error identity: res(c*dQ)=res(v*dc)-res((Q+v)*dc).
    iv = (2*r+a*a)/(2*(r*r-a*a))
    zz = a*a*(r+1+a*a/4)/(r*r-a*a)
    anomalies = []
    expected = [a*(a*a-4)/16, 5*a*(a*a-4)*(a*a+12)/1024]
    for n in (1,2):
        H = 3*iv*sum(s.binomial(-s.Rational(1,2),j)*zz**j for j in range(n+1))
        anomaly = s.factor(-s.residue(H*s.diff(Cc,r),r,a))
        zero(anomaly-expected[n-1])
        assert anomaly != 0
        zero(anomaly+anomaly.subs(a,-a))
        anomalies.append({"order":n,"individual_residue_error":str(anomaly),
                          "sum_of_two_residue_errors":"0"})
    return {"status":"PASS","necessary_residue_at_r=a":str(source),
            "base_trace_extension_residue":str(base),"polynomial_jet_anomalies":anomalies}


def verify_minimal_trace_factor():
    p0=c
    q0=-(b+1)/2
    zero(p0*q0+s.Rational(2,3)-Delta/6)
    p,q=restrict(p0),restrict(q0)
    # If S=PQ+2/3=Delta*H and J(P,Q)=1, then {P,S}=P forces this trace.
    Htrace=-1/(6*r)
    zero(Htrace*(-3*r*r*s.diff(p,r))-p)
    zero(restrict(-inv/6)-Htrace)
    # General hyperbola trace degree 2m has the same calculation with 1/m.
    for m in (1,2,3,5):
        pp=r**(2*m)
        qq=-s.Rational(2,3*m)*r**(-2*m)
        zero(residue_at_zero(pp*s.diff(qq,r))-s.Rational(4,3))
        zero((-1/(6*m*r))*(-3*r*r*s.diff(pp,r))-pp)
    return {"status":"PASS", "minimal_trace_H":"-1/(6r)",
            "complete_H_form":"-inv/6 + Delta*W(v,c)",
            "necessary_factorization":"P*Q=Delta*(-inv/6+Delta*W)-2/3",
            "factorization_alone_is_sufficient":False}


def verify_weight_algebra():
    x,Z=s.symbols("x Z",nonzero=True)
    f,g=s.Function('f')(Z),s.Function('g')(Z)
    # In coordinates (v,Z=cv), J_{v,c}=v*J_{v,Z}.
    for i,j in ((1,3),(2,3),(-2,3),(-1,-2)):
        actual=x*J(x**i*f,x**j*g,x,Z)
        zero(actual-x**(i+j)*(i*f*s.diff(g,Z)-j*s.diff(f,Z)*g))
    # Direct residue control for the regular-in-(r,c) obstruction.
    # P=r^2+c: generic P=t has r^2=t-c. At c=0, r=a!=0,
    # dQ/dc=1/(3c*P_r), hence residue 1/(6a), never zero.
    localr=s.sqrt(a*a-c)
    localeta=1/(6*c*localr)
    zero(s.limit(c*localeta,c,0)**2-1/(36*a*a))
    # Nonconstant polynomial leading terms cannot commute with weights of
    # opposite sign in the proposed all-polynomial coefficient ring.
    return {"status":"PASS", "weighted_bracket":"v^(i+j)*(i*f*g'-j*f'*g)",
            "written_theorem":"Keller component of max weight <=1 forces automorphism",
            "weights":"wt(v)=1, wt(c)=-1",
            "external_input":"Gwozdziewicz, Injectivity on one line (1993)"}


def in_B(f):
    value=restrict(f)
    return s.cancel(value-value.subs(r,-r)) == 0


def potential_gate(H):
    """Exact global gate; H is polynomial, and H+2r/3 must belong to B.

    Returns a scoped failure or the original polynomial Keller pair. A pair
    reaches the collision verdict only after original-bracket and B checks.
    No bounded search completeness is claimed by this function.
    """
    A=s.expand(s.diff(H,v))
    B=s.expand(s.diff(H,c)+v)
    g=s.Poly(s.gcd(A,B),v,c).monic().as_expr()
    aa,bb=s.cancel(A/g),s.cancel(B/g)
    closure=s.expand(s.diff(aa,c)-s.diff(bb,v))
    answer={"potential_in_required_class":in_B(H+2*R/3),
            "gcd":str(g),"quotient_closure_residual":str(closure)}
    if closure != 0:
        answer["verdict"]="QUOTIENT_NOT_CLOSED"
        return answer
    Q=s.integrate(aa,v)
    remaining=s.expand(bb-s.diff(Q,c))
    zero(s.diff(remaining,v))
    Q=s.expand(Q+s.integrate(remaining,c))
    zero(J(g,Q)-1)
    answer.update(P=str(g),Q=str(Q),P_in_B=in_B(g),Q_in_B=in_B(Q))
    if not (in_B(g) and in_B(Q)):
        answer["verdict"]="KELLER_PAIR_OUTSIDE_COLLISION_SUBALGEBRA"
    else:
        assert answer["potential_in_required_class"]
        left={v:-s.Rational(1,3),c:4}
        right={v:s.Rational(2,3),c:4}
        zero(g.subs(left)-g.subs(right))
        zero(Q.subs(left)-Q.subs(right))
        answer["verdict"]="EXACT_KELLER_PAIR_WITH_COLLISION"
    return answer


def verify_potential_gate():
    # Genuine polynomial automorphisms exercise the positive Jacobian path
    # and are correctly excluded from the collision subalgebra.
    first=potential_gate(-c*v)
    second=potential_gate(-c*v-v**3/3)
    assert first["verdict"] == second["verdict"] == "KELLER_PAIR_OUTSIDE_COLLISION_SUBALGEBRA"
    assert first['P_in_B'] and not first['Q_in_B']
    # The simplest admissible potential has no common factor.
    no_factor=potential_gate(-2*R/3)
    assert no_factor['potential_in_required_class']
    assert no_factor['gcd']=='1'
    assert no_factor['verdict']=='QUOTIENT_NOT_CLOSED'
    # A nontrivial common factor and the correct trace still are insufficient.
    H=-c*v-27*c*c*inv**3
    common_factor=potential_gate(H)
    assert common_factor['potential_in_required_class']
    assert common_factor['gcd']=='c'
    assert common_factor['verdict']=='QUOTIENT_NOT_CLOSED'
    return {"status":"PASS","positive_controls":[first,second],
            "negative_controls":[no_factor,common_factor],
            "scope":"Exact gate for a supplied potential; no exhaustive potential search"}


def main():
    results={}
    for name, fn in [("GLOBAL_CONDUCTOR_PERIOD",verify_global_period),
                     ("COMPLETE_FORMAL_RECURRENCE",verify_formal_recurrence),
                     ("ALL_ORDER_FALSE_POSITIVE_CONTROL",verify_all_order_controls),
                     ("SPLIT_INFINITY_RESIDUES",verify_two_punctures),
                     ("HYPERBOLA_FACTOR_CONSTRAINT",verify_minimal_trace_factor),
                     ("MIXED_WEIGHT_ALGEBRA",verify_weight_algebra),
                     ("GLOBAL_POTENTIAL_GATE",verify_potential_gate)]:
        results[name]=fn()
        print(name+": PASS",flush=True)
    results['counterexample_found']=False
    results['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'verification.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    main()
