from fractions import Fraction as F
import mono15, exact_g1_15 as G, sys
for (n,m) in [(1,2),(2,2),(3,2),(1,3),(2,3),(3,3),(4,3),(2,4),(3,4),(2,5),(3,5)]:
    P={(0,1):F(1),(n,m):F(2)}
    e=G.screen(n,m)
    try:
        r=mono15.screen_fibre_checked(P,F(1))
        nm='%s ls=%.2e g=%s npunct=%s sumres=%.1e'%(r['verdict'],r['ls_residual'],r['genus_sum'],r['n_punctures'],r['infinity'].get('sum_abs',-1))
        ok=(r['verdict']==e['verdict']) or e['verdict']=='DEFERRED_TO_NUM'
        gok=(r['genus_sum']==e['genus']); pok=(r['n_punctures']==e['n_places_at_infinity'])
    except Exception as ex:
        nm='ERR %s'%ex; ok=gok=pok=None
    print('n=%2d m=%d EXACT-G1:%-16s g=%d pl=%d | NUM:%-52s v=%s g=%s pl=%s'%(n,m,e['verdict'],e['genus'],e['n_places_at_infinity'],nm,ok,gok,pok))
    sys.stdout.flush()
