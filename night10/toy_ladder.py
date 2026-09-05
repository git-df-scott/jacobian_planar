"""night10 -- R0: the same Ladder machinery that runs the 9-variable system,
run unchanged on the toy f(x) = x^2 - 2 over O2 = Z[pi]/(pi^2-2), x0 = 0."""

import json
from ram import O2
from ladder import Ladder


def reval(v, R):
    return [R.sub(R.mul(v[0], v[0]), R.from_int(2))]


def jeval(x0):
    return [[2 * x0[0]]]


L = Ladder(O2, 1, reval, jeval, [0], ceiling=12)
print("J mod 2 =", L.J2, " rank =", L.rank, " kernel =", L.kernel)

# level-1 pass set
wm, rho, ok, sols = L.level_data({}, 1)
print("level 1: wmin(r(x0)) =", wm, " rho =", rho, " solvable =", ok, " d1 in", sols)

# level-2 test for each d1
lvl2 = {}
for d1 in [(0,), (1,)]:
    wm, rho, ok, sols = L.level_data({1: list(d1)}, 2)
    lvl2[d1[0]] = dict(wmin=wm, rho=rho, solvable=ok)
    print("level 2 with d1=%d: wmin=%d rho=%s solvable=%s" % (d1[0], wm, rho, ok))

res = L.run()
print("run:", json.dumps({k: v for k, v in res.items() if k != 'deaths'}, default=str))
print("deaths:", res["deaths"])

assert lvl2[1]["solvable"] and not lvl2[0]["solvable"], "toy disagrees -- HARD EXIT"
assert res["survivor"] is not None and res["survivor"]["ds"][1] == [1], "toy disagrees"
print("R0 TOY OK: ramified branch d_1 = 1 climbs, d_1 = 0 dies at level 2")
