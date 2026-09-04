"""Verify and save a small defining polynomial for the exact leading field.

PARI polredabs suggested this generator. FLINT verifies the change of field,
all transported coefficients, and the leading identity independently.
"""
from pathlib import Path
import json
from flint import fmpq, fmpq_mat, fmpq_poly
import pentagon_descent as d

def main():
    d.EXACT=True
    C,G=d.seed();oldmod=d.MOD
    powers=[d.norm(1)]
    for _ in range(4):powers.append(d.norm(powers[-1]*C[3]))
    basis=fmpq_mat([[powers[j][i] for j in range(5)] for i in range(5)])
    inverse=basis.inv()
    newmod=fmpq_poly([26,0,3,3,-1,1])
    den=60579126468209266677769
    v=fmpq_poly([fmpq(n,den) for n in [15000285910282089504192,5134565172670933272,
          -137539431432626359836,-336800193197460147624,84325443098952382698]])
    newpowers=[fmpq_poly([1])]
    for _ in range(4):newpowers.append(newpowers[-1]*v%newmod)
    # Irreducibility and the old C3 minimal polynomial relation prove this is
    # an isomorphism, rather than just a numerical correspondence.
    cols=[d.norm(C[3]*fmpq_poly([0]*j+[1])) for j in range(5)]
    old_c3_mod=fmpq_mat([[cols[j][i] for j in range(5)] for i in range(5)]).charpoly()
    residual=fmpq_poly([])
    for i in range(5,-1,-1):residual=(residual*v+old_c3_mod[i])%newmod
    assert residual==0
    _,factors=newmod.factor();assert len(factors)==1 and factors[0][0].degree()==5
    def transfer(x):
        coords=inverse*fmpq_mat([[x[i]] for i in range(5)])
        assert d.norm(sum(powers[j]*coords[j,0] for j in range(5)))==x
        return sum(newpowers[j]*coords[j,0] for j in range(5))%newmod
    CC,GG=list(map(transfer,C)),list(map(transfer,G))
    d.MOD=newmod
    residual=d.add(d.scale(d.mul(CC,d.deriv(GG)),2),d.scale(d.mul(d.deriv(CC),GG),-3))
    assert residual[2]==1 and not any(x for i,x in enumerate(residual) if i!=2)
    result={'minimal_polynomial':[str(newmod[i]) for i in range(6)],
            'C':[[str(c[i]) for i in range(5)] for c in CC],
            'G':[[str(g[i]) for i in range(5)] for g in GG],
            'old_C3_in_new_field':[str(v[i]) for i in range(5)],
            'field_isomorphism':'PASS','leading_identity':'PASS'}
    out=Path(__file__).resolve().parent/'artifacts/pentagon_small_field.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    # A denominator-ideal calculation in PARI suggested this T scale.
    # Its validity needs only exact substitution, checked here with FLINT.
    lam=fmpq_poly([257,33,113,13,11])
    assert lam.gcd(newmod)==1
    CCC=[(v*(lam**(i-1)))%newmod if i>=1 else v for i,v in enumerate(CC)]
    GGG=[(v*(lam**(i-2)))%newmod if i>=2 else v for i,v in enumerate(GG)]
    residual=d.add(d.scale(d.mul(CCC,d.deriv(GGG)),2),d.scale(d.mul(d.deriv(CCC),GGG),-3))
    assert residual[2]==1 and not any(x for i,x in enumerate(residual) if i!=2)
    integral=dict(result)
    integral.update(C=[[str(c[i]) for i in range(5)] for c in CCC],
                    G=[[str(g[i]) for i in range(5)] for g in GGG],
                    T_scale=[str(lam[i]) for i in range(5)],
                    normalization='C_1=G_2=1; C_2=11*a^4+13*a^3+113*a^2+33*a+257',
                    scale_identity='PASS')
    out.with_name('pentagon_integral_field.json').write_text(json.dumps(integral,indent=2)+'\n')
    print('FIELD_ISOMORPHISM_AND_LEADING_IDENTITY: PASS')
    print('NEW_FIELD: a^5-a^4+3*a^3+3*a^2+26')
    print('MAX_COEFFICIENT_CHARACTERS',max(len(str(x)) for poly in CC+GG for x in poly))
    print('SCALED_MAX_COEFFICIENT_CHARACTERS',max(len(str(x)) for poly in CCC+GGG for x in poly))

if __name__=='__main__':main()
