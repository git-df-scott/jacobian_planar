import sys, time, random
sys.path.insert(0, "/home/user/jacobian_planar/night12")
import matekit as M

rnd = random.Random(1)
for d, cap in [(9, 4000), (84, 400), (84, 900), (84, 1600)]:
    P = {(1, 0): 1}
    for _ in range(4):
        i = rnd.randrange(0, d + 1)
        j = rnd.randrange(0, d + 1 - i)
        P[(i, j)] = rnd.randrange(1, 5)
    P[(d - 1, 1)] = 3
    t0 = time.time()
    S, info = M.q_support(P, cap_work=cap)
    t1 = time.time()
    rows, _ = M.build_system(P, S)
    t2 = time.time()
    r = M.consistency_mod_p(rows, len(S), M.P1, seed=7)
    t3 = time.time()
    print(d, info, "rows", len(rows), "| supp t=%.2f build=%.2f elim=%.2f" % (t1 - t0, t2 - t1, t3 - t2), r["rank_A"], r["consistent"])
