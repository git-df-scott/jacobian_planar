import sys, time
sys.path.insert(0, '/home/user/jacobian_planar/night6')
import wface as W
p = 999983
B, res = W.build(p)
print('residual weights', [W.wdeg(next(iter(f))) for f in res],
      'nterms', [len(f) for f in res], flush=True)
for d in range(20, 60):
    t = time.time()
    tm = W.pure_mons(d, 7)
    rows, tail, nr, nc = W.macaulay(res, d, p, tm)
    print('d=%d rows=%d cols=%d pure=%d relations=%d (%.1fs)'
          % (d, nr, nc, len(tail), len(rows), time.time() - t), flush=True)
    if rows:
        for r in rows[:4]:
            print('   ', r, flush=True)
        break
