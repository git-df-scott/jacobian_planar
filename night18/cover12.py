import json, os, sys
import cover18
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for H in (1, 2):
    print("=" * 78); print("COVER  deg h = %d,  carrier deg Q <= 12 (= 4 deg P)" % H)
    print("=" * 78); sys.stdout.flush()
    ch = cover18.walk(H, 12)
    for c in ch:
        c.pop('_dens', None); c.pop('_lamraw', None); c.pop('_restr', None)
    out["H%d_D12" % H] = ch
    json.dump(out, open(os.path.join(HERE, 'cover18_D12.json'), 'w'), indent=1)
print("done")
