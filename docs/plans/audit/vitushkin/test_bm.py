import sys; sys.path.insert(0, '.')
from bm import *
import json
cases = {
 'cuspcubic': [(t**2, t**3)],
 'nodalcubic': [(t**2, t**3 - t)],
 'c25': [(t**2, t**5 - t**3)],
 'c34': [(t**3 - 3*t, t**4/4 - sp.Rational(1,3)*t**3*0 - t**2/2 + 0*t)],
}
# c34 with s=0: b' = (t^2-1) t -> b = t^4/4 - t^2/2 : but that is even in t with a odd -> t->-t symmetry? a(-t) = -a(t), so no.
for name, comps in cases.items():
    res = analyse(comps, name)
    print(name, 'n =', res['n'], 'crit =', [tuple(round(x,3) for x in c) for c in res['crit']])
    for lp in res['loops']:
        print('  c=%s W=%s P=%s L=%s' % (tuple(round(x,3) for x in lp['c']), lp['W'], lp['P'], lp['L']))
        for loc in lp['local']:
            print('     local: strands', loc['strands'], 'branches', loc['branches'], 'merA', loc['merA'], 'merB', loc['merB'])
    print('  rels:', [gapword(r) for r in res['rels']])
    to_gap(res, '/tmp/%s.g' % name)
