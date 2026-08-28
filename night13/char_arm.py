"""night13 stage 2b -- the small-characteristic arm of the H-support screen.

The two extreme-ray rows carry integer factors 2*e0 and 3*(m-e1).  In a
characteristic p dividing only one of them the other row still bites, so the
verdict is unchanged; only p dividing BOTH can make both rows vacuous.  Those
supports are re-screened here with the characteristic-aware route test
(a route contributes only when p1*a2 - p2*a1 is nonzero mod p), which can
also promote further rows to normalization-forced.
"""
import itertools, json, math, sys, screen

out = {}
for m in (42, 45, 48):
    exps = screen.exponents(m, 2)
    rows = []
    n_aff = n_surv = 0
    for s in (3, 4, 5, 6):
        for E in itertools.combinations(exps, s):
            e0, e1 = min(E), max(E)
            g = math.gcd(2 * e0, 3 * (m - e1))
            if g <= 1:
                continue
            for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
                if g % p:
                    continue
                n_aff += 1
                r = screen.analyse(E, m, 1, 0, char=p)
                if r["survives"]:
                    n_surv += 1
                    rows.append({"E": list(E), "char": p,
                                 "n_pool_P": r["n_pool_P"],
                                 "n_pool_Q": r["n_pool_Q"]})
    out[m] = {"n_support_char_pairs_rescreened": n_aff,
              "n_survivors": n_surv, "survivors": rows[:200]}
    print(m, out[m]["n_support_char_pairs_rescreened"],
          "rescreened,", n_surv, "survivors", flush=True)
json.dump(out, open("char_arm.json", "w"), indent=1)
