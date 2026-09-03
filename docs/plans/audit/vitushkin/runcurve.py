import sys, subprocess, json, time; sys.path.insert(0, '/home/user/jacobian_planar/docs/plans/audit/vitushkin')
from bm import *
def run(name, comps, Dmin=4, Dmax=8, base=None, verbose=True, seeds=(0,1,2,3,4)):
    t0 = time.time()
    last = None
    for sd in seeds:
        try:
            res = analyse(comps, name, base=base, seed=sd); break
        except RuntimeError as ex:
            last = ex; res = None
    if res is None:
        print(name, 'TRACKING FAILED', last); return None
    to_gap(res, '/tmp/%s.g' % name)
    if verbose:
        print('==', name, 'comps', [(str(a), str(b)) for a, b in comps], 'alpha', res['n'], 'degs', res['degs'])
        for lp in res['loops']:
            print('  c=%s W=%s' % (tuple(round(x,3) for x in lp['c']), lp['W']), [(loc['strands'], 'br', loc['branches'], 'cusps', loc['cusps']) for loc in lp['local']])
    script = 'SizeScreen([4000,]);; Read("/tmp/%s.g");; Read("/home/user/jacobian_planar/docs/plans/audit/vitushkin/gapcheck.g");; Print("abelianization: ", AbelianInvariants(G), "\\n");; r := CheckCurve(G, singpts, compofgen, degs, m, %d, %d, fibres);; Report(r);; QUIT;' % (name, Dmin, Dmax)
    try:
        out = subprocess.run(['gap', '-q', '-b'], input=script, capture_output=True, text=True, timeout=7200)
        print(out.stdout.strip())
        if out.stderr.strip(): print('STDERR', out.stderr.strip()[:1500])
    except subprocess.TimeoutExpired:
        print('GAP TIMEOUT')
    print('  [%.0f s]' % (time.time() - t0))
    return res
if __name__ == '__main__':
    run('c34', [(t**3 - 3*t, t**4/4 - t**3/9 - t**2/2 + t/3)])
    run('cc_line', [(t**2, t**3), (t, t + 1)])
