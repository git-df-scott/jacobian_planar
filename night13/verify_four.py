"""night13 -- independent re-verification of the three configurations.

Does NOT reuse survivor_probe's verdict path.  For each configuration and each
of 20 sampled P-blocks it re-derives, from the same P and the same carrier:
  char 2 : solve the system with the B column moved to the RHS at B = 1
           (i.e. demand a NONZERO Q leading form) and report the status;
           also solve the plain system and read off deg Q of the solution.
  char 5 : exhibit an explicit inconsistency certificate -- a rational
           combination of rows that is 0 on the unknowns and 1 on the RHS --
           via rank(A) vs rank(A|e) recomputed with independent seeds.
"""
import json, os, random
import kit as K, probe as PR, survivor_probe as SP

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for tag, i, ch in [("top1_char2",1,2), ("top1_char5",1,5), ("top2_char2",2,2), ("top2_char5",2,5)]:
    ranked = json.load(open(os.path.join(HERE,"rank_char2.json")))["42"]["ranked"]
    E = tuple(ranked[i-1]["E"]); m = 42
    car = json.load(open(os.path.join(HERE,"carrier_%s.json"%tag)))
    C_P = [tuple(v) for v in car["C_P"]]; C_Q = [tuple(v) for v in car["C_Q"]]
    recs = []
    for s in range(20):
        rng = random.Random(7000+s)
        ones = 1.0 if s == 0 else rng.choice([0.25,0.5,0.75])
        P, meta = SP.sample_P_char(rng, E, m, C_P, ch, ones)
        H3 = K.ppow(meta["H"], 3, ch)
        rows = PR.build_Q_system(P, H3, C_Q, ch)
        n = 1 + len(C_Q)
        r1 = K.rank_modp(rows, n, ch, seed=101+s, augment=True)
        r2 = K.rank_modp(rows, n, ch, seed=9001+s, augment=True)
        rec = {"sample": s, "consistent_seedA": r1["consistent"],
               "consistent_seedB": r2["consistent"],
               "rank_A": r1["rank_A"], "rank_Ae": r1["rank_Ae"]}
        # demand B != 0 explicitly: move column 0 to the RHS with B = 1
        col0 = {k: (-r[0]) % ch for k, r in rows.items() if r.get(0)}
        rhs = dict(col0); rhs[(0,0)] = (rhs.get((0,0),0) + 1) % ch
        sol, st = K.solve_modp(rows, n, ch, cols=list(range(1,n)), rhs=rhs)
        rec["solve_with_B_equal_1"] = st
        if st == "ok":
            Q = K.ppow(meta["H"], 3, ch)
            for c,v in sol.items():
                mm = C_Q[c-1]; Q[mm] = (Q.get(mm,0)+v) % ch
            Q = {k:v for k,v in Q.items() if v}
            rec["deg_Q_with_B1"] = K.pdeg(Q)
            rec["bracket_is_one"] = K.bracket(P, Q, ch) == {(0,0):1}
        if r1["consistent"]:
            sol0, st0 = K.solve_modp(rows, n, ch)
            rec["plain_solve_status"] = st0
            if st0 == "ok":
                rec["B_in_plain_solution"] = sol0.get(0,0)
                Q0 = {}
                for c,v in sol0.items():
                    if c == 0: continue
                    mm = C_Q[c-1]; Q0[mm] = (Q0.get(mm,0)+v) % ch
                lead = K.pscale(K.ppow(meta["H"],3,ch), sol0.get(0,0), ch)
                Q0 = {k:(Q0.get(k,0)+v)%ch for k,v in lead.items()} | \
                     {k:v for k,v in Q0.items() if k not in lead}
                Q0 = {k:v for k,v in Q0.items() if v}
                rec["deg_Q_plain"] = K.pdeg(Q0) if Q0 else None
                rec["bracket_plain_is_one"] = K.bracket(P, Q0, ch) == {(0,0):1}
        recs.append(rec)
    out[tag] = {"E": list(E), "char": ch, "n_checked": len(recs),
                "seed_agreement": all(r["consistent_seedA"]==r["consistent_seedB"] for r in recs),
                "any_B1_solvable": any(r.get("solve_with_B_equal_1")=="ok" for r in recs),
                "deg_Q_plain_values": sorted({r.get("deg_Q_plain") for r in recs}),
                "B_values_in_plain_solution": sorted({r.get("B_in_plain_solution") for r in recs}),
                "records": recs}
    print(tag, "seed_agreement", out[tag]["seed_agreement"],
          "any_B1_solvable", out[tag]["any_B1_solvable"],
          "deg_Q_plain", out[tag]["deg_Q_plain_values"],
          "B_plain", out[tag]["B_values_in_plain_solution"], flush=True)
json.dump(out, open(os.path.join(HERE,"verify_four.json"),"w"), indent=1)
