#!/usr/bin/env python3
"""EXACT cascade sweep up the B=16 ladder -- no Groebner, no memory wall.

The cascade solves the GGV system by exact triangular descent with branching,
returning every solved branch.  A branch with mu0 != 0 is a COUNTEREXAMPLE
CANDIDATE (verify by exact substitution into the untouched system, then GGV
Sec 2).  Soundness notes recorded honestly:
 * denominators are dropped (num kept), which can only ADD spurious branches,
   never lose real ones -- so zero survivors is evidence of emptiness and a
   survivor must be verified;
 * sympy solve() may miss roots of high-degree univariate steps, and the
   4000-step cap can trip: either outcome is reported as INCOMPLETE, not as
   emptiness.
Control: d=3 must give 0 survivors (GGV proved that cell empty).

Usage: python3 w6_cascade_sweep.py DMIN DMAX PER_D_TIMEOUT
"""
import sys, os, json, time, signal
sys.path.insert(0, '/home/user/jacobian_planar/wave5')
os.chdir('/home/user/jacobian_planar/wave5')
from w5_b16_cascade import cascade, survivors_with_mu0

class TO(Exception): pass
def _alarm(sig, frm): raise TO()
signal.signal(signal.SIGALRM, _alarm)

dmin = int(sys.argv[1]); dmax = int(sys.argv[2])
per = int(sys.argv[3]) if len(sys.argv) > 3 else 900
out = []
for d in range(dmin, dmax + 1):
    t0 = time.time()
    rec = {'d': d}
    signal.alarm(per)
    try:
        br, dead = cascade(d, None, verbose=False)
        surv = survivors_with_mu0(br)
        rec.update({'branches': len(br), 'dead': dead, 'survivors_mu0': len(surv),
                    'verdict': ('CANDIDATE-SURVIVOR' if surv else 'no-survivor'),
                    'secs': round(time.time() - t0, 1)})
        if surv:
            rec['survivor_sample'] = [{str(k): str(v)[:200] for k, v in s.items()}
                                      for s in surv[:2]]
    except TO:
        rec.update({'verdict': 'INCOMPLETE-TIMEOUT', 'secs': per})
    except Exception as e:
        rec.update({'verdict': 'INCOMPLETE-ERROR', 'error': str(e)[:160],
                    'secs': round(time.time() - t0, 1)})
    finally:
        signal.alarm(0)
    print(json.dumps(rec), flush=True)
    out.append(rec)
    json.dump(out, open('/home/user/jacobian_planar/wave6/cascade_sweep.json', 'w'), indent=1)
