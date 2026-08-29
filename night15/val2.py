from fractions import Fraction as F
import mono15, exact_g1_15 as G, time, sys
for (n,m) in [(3,4),(2,4),(2,5),(1,2),(2,2),(3,2),(4,3),(2,3),(1,3),(3,3),(3,5),(5,3)]:
    P={(0,1):F(1),(n,m):F(2)}
    e=G.screen(n,m); t=time.time()
    try:
        r=mono15.screen_fibre_checked(P,F(1))
        print('n=%d m=%d EXACT=%-16s | NUM=%-13s ls=%.3e err=%.1e g=%s pl=%s (%.0fs)  MATCH=%s'%(
          n,m,e['verdict'],r['verdict'],r['ls_residual'],r['err_ls_residual'],r['genus_sum'],r['n_punctures'],time.time()-t,
          e['verdict']==r['verdict'] or e['verdict']=='DEFERRED_TO_NUM'))
    except Exception as ex:
        print('n=%d m=%d EXACT=%-16s | NUM ERR %s'%(n,m,e['verdict'],ex))
    sys.stdout.flush()
