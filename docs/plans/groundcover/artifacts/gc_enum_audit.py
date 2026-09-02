"""
groundcover / independent instrumentation of gghv_audit/ggv_algorithms.py.

Answers, from the code's own filters and nothing else:
  (1) counts at M=35 / M=50 (max<=150) / M=100 (max<=300);
  (2) EVERY admissible complete chain NOT in [5]'s printed tables, traced
      forward through Definition 3.3 / Proposition 3.2 to a degree pair;
  (3) whether ANY unprinted chain yields a degree pair with max < 125;
  (4) the admissible A'_0 for A0=(10,1,40) enumerated from Algorithm 2's own
      filters instead of importing the unprinted assumption A'_t=(1,0);
  (5) the F6 gcd(m,n)=2-at-even-j discrepancy.
"""
import json, os, re, sys, time
from math import gcd
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "run"))
import ggv_algorithms as G
import ggv_reference_tables as T

OUTJ = {}

def chains_at(M, PLLC):
    raw = G.admissible_complete_chains(M, PLLC=PLLC)
    d = {}
    for c, last in raw:
        d[(tuple((x[0], x[1]) for x in c), last)] = (c, last)
    return d

def cases_from(chains, bound):
    cs = set()
    for (_, _), (c, last) in chains.items():
        A0 = c[0][0]; v11 = A0[0] + A0[2]
        for k, m, n in G.mn_pairs(last, max_mn=200):
            if max(m, n) * v11 <= bound:
                cs.add((A0, tuple(x[0] for x in c[1:]), last, m, n, m*v11, n*v11))
    return cs

t0 = time.time()
PLLC, PFL = G.get_possible_last_lower_corners(60)
print(f"[A] PLLC xmax=60: {len(PLLC)} corners  ({time.time()-t0:.1f}s)")

ch35 = chains_at(35, PLLC)
ch50 = chains_at(50, PLLC)
cs150 = cases_from(ch50, 150)
print(f"[B] chains M=35: {len(ch35)}   chains M=50: {len(ch50)}   cases max<=150: {len(cs150)}")
OUTJ["pllc_xmax60"] = len(PLLC)
OUTJ["chains_M35"] = len(ch35)
OUTJ["chains_M50"] = len(ch50)
OUTJ["count_max150"] = len(cs150)

# ---------------------------------------------------------------- printed set
pub_l1 = set(T.GGV_CHAINS_L1)                                    # (A0,A'0,A1)
pub_l2 = {(f[1], f[2], f[3], f[4], f[5]) for f in T.GGV_FAMILIES_L2}
# section 6 prints (A0, A1.., final) WITHOUT the A'_i -- project to that shape
pub_s6_shapes = set()
for A0, last, mn, mx in T.GGV_S6_L1:            pub_s6_shapes.add((A0, (), last))
for A0, A1, last, mn, mx in T.GGV_S6_L2:        pub_s6_shapes.add((A0, (A1,), last))
for A0, A1, A2, last, mn, mx in T.GGV_S6_L3:    pub_s6_shapes.add((A0, (A1, A2), last))
for f in T.GGV_FAMILIES_L1:                     pub_s6_shapes.add((f[1], (), f[3]))
for f in T.GGV_FAMILIES_L2:                     pub_s6_shapes.add((f[1], (f[3],), f[5]))

def full_key(c, last):
    return tuple([(x[0], x[1]) for x in c]) + (last,)
def shape_key(c, last):
    return (c[0][0], tuple(x[0] for x in c[1:]), last)

# ---- extras vs section 5 (the bound at which section 5's tables are stated)
extras = []
for (_, _), (c, last) in sorted(ch35.items(), key=lambda kv: str(kv[0])):
    L = len(c)
    if L == 1:
        k = (c[0][0], c[0][1], last)
        printed = k in pub_l1
    elif L == 2:
        k = (c[0][0], c[0][1], c[1][0], c[1][1], last)
        printed = k in pub_l2
    else:
        k = full_key(c, last); printed = False
    if printed:
        continue
    A0 = c[0][0]; v11 = A0[0] + A0[2]
    mns = G.mn_pairs(last, max_mn=200)
    pairs = [{"k": kk, "m": m, "n": n, "gcd": gcd(m, n),
              "deg_P": m*v11, "deg_Q": n*v11, "max": max(m, n)*v11}
             for (kk, m, n) in mns]
    # why does Definition 3.3 give nothing?  recompute I(A) explicitly
    a, l, b = last
    bl_a = b*l - a
    ivals = []
    kk = 1
    while kk < Fraction(l) - Fraction(a, b):
        ek = gcd(kk, bl_a)
        ivals.append({"k": kk, "bl_a": bl_a, "e_k": ek,
                      "gcd_b_over": gcd(b, bl_a//ek) if bl_a % ek == 0 else None,
                      "in_I": (bl_a % ek == 0 and gcd(b, bl_a//ek) == 1)})
        kk += 1
    if not pairs:
        if not any(x["in_I"] for x in ivals):
            step = ("Definition 3.3 / Algorithm 9: I(A_final) = empty "
                    "(gcd(b,(bl-a)/e_k) != 1 for every admissible k) -- no "
                    "(m,n)-family, so Algorithm 9 emits no degree pair")
        else:
            step = "Proposition 3.2 Diophantine has no coprime solution with m,n>1"
    else:
        step = ("does NOT die: Algorithm 9 emits degree pairs; it is absent from "
                "[5] section 5's printed table only")
    extras.append({"chain": [list(x[0]) for x in c] , "chain_full":
                   [[list(x[0]), list(x[1]), x[2]] for x in c],
                   "final": list(last), "length": L, "v11_A0": v11,
                   "printed_in_sec5": False,
                   "shape_printed_in_sec6": shape_key(c, last) in pub_s6_shapes,
                   "I_of_A": ivals, "degree_pairs": pairs, "dies_at_step": step,
                   "min_max_deg": min([p["max"] for p in pairs]) if pairs else None,
                   "any_sub125": any(p["max"] < 125 for p in pairs)})
OUTJ["extras_vs_sec5"] = extras
print(f"[C] chains at M=35 not printed in [5] section 5: {len(extras)}")
for e in extras:
    print(f"    L{e['length']}  {e['chain_full']} -> {e['final']}  "
          f"n_pairs={len(e['degree_pairs'])} min_max={e['min_max_deg']} "
          f"pairs_max<=300={[(p['m'],p['n'],p['max']) for p in e['degree_pairs'] if p['max']<=300]}  "
          f"sub125={e['any_sub125']}")

# ---- the real question: any case at max<125 whose SHAPE is not printed ------
unprinted_cases = []
for (A0, mid, last, m, n, dp, dq) in sorted(cs150, key=lambda r: max(r[5], r[6])):
    if (A0, mid, last) not in pub_s6_shapes:
        unprinted_cases.append([list(A0), [list(x) for x in mid], list(last), m, n, dp, dq])
OUTJ["cases_max150_with_unprinted_shape"] = unprinted_cases
sub125 = [c for c in cs150 if max(c[5], c[6]) < 125]
OUTJ["count_max_lt125"] = len(sub125)
OUTJ["pairs_max_lt125"] = sorted({(c[5], c[6]) for c in sub125})
print(f"[D] cases max<=150 whose (A0,mid,final) shape is NOT in a printed table: "
      f"{len(unprinted_cases)}  {unprinted_cases}")
print(f"[E] cases with max<125: {len(sub125)}; degree pairs "
      f"{OUTJ['pairs_max_lt125']}")

# ---- extras across the WHOLE M=50 run (any chain producing an unprinted case)
extras50 = []
for (_, _), (c, last) in ch50.items():
    A0 = c[0][0]; v11 = A0[0] + A0[2]
    mns = G.mn_pairs(last, max_mn=200)
    best = [(m, n, max(m, n)*v11) for (_, m, n) in mns if max(m, n)*v11 <= 150]
    if best and shape_key(c, last) not in pub_s6_shapes:
        extras50.append({"chain": [[list(x[0]), list(x[1]), x[2]] for x in c],
                         "final": list(last), "pairs": best})
OUTJ["chains_M50_yielding_unprinted_max150_case"] = extras50
print(f"[F] chains at M=50 yielding a max<=150 case with an unprinted shape: {len(extras50)}")

# ---------------------------------------------------------- A'_t for (10,40)
A0 = (10, 1, 40)
rows = []
for (A, Ap, mu) in G.get_starting_edges(10, 40, PLLC):
    d = G.edge_data(A, Ap)
    comp = G.get_complete_chains(A, Ap, mu, PLLC)
    adm = [(ch, lst) for (ch, lst) in comp if G.is_admissible(ch, lst)]
    fins = []
    for ch, lst in adm:
        v11 = 50
        mns = G.mn_pairs(lst, max_mn=200)
        fins.append({"mid": [list(x[0]) for x in ch[1:]], "final": list(lst),
                     "n_pairs_total": len(mns),
                     "min_max_deg": min([max(m, n)*v11 for (_, m, n) in mns]) if mns else None,
                     "pairs_max_le_300": [(m, n, max(m, n)*v11) for (_, m, n) in mns
                                          if max(m, n)*v11 <= 300]})
    fins = [f for f in fins]
    rows.append({"A_prime_0": list(Ap), "mu": mu, "dir": list(d),
                 "n_complete_chains": len(comp),
                 "n_admissible_complete": len(adm), "admissible": fins})
OUTJ["a_prime_0_for_10_40"] = rows
print(f"\n[G] A0=(10,1,40): Algorithm 2 admits {len(rows)} starting edges (A'_0, mu)")
for r in rows:
    if r['n_admissible_complete'] == 0:
        continue
    print(f"    A'_0={r['A_prime_0']} mu={r['mu']} dir={r['dir']}  "
          f"complete={r['n_complete_chains']} admissible={r['n_admissible_complete']}")
    for f in r["admissible"]:
        print(f"        mid={f['mid']} final={f['final']} "
              f"n_pairs={f['n_pairs_total']} min_max={f['min_max_deg']} "
              f"pairs_max<=300={f['pairs_max_le_300']}")

# ------------------------------------------------------------------ F6 check
def fam_mn(expr, j):
    # parse "aj+b" / "j+b" forms without eval
    m = re.fullmatch(r"(\d*)j\+(\d+)", expr.replace(" ", ""))
    assert m, expr
    c = int(m.group(1)) if m.group(1) else 1
    return c * j + int(m.group(2))
f6 = []
allfam = [(f[0], f[5], f[6]) for f in T.GGV_FAMILIES_L1] + \
         [(f[0], f[7], f[8]) for f in T.GGV_FAMILIES_L2]
noncoprime = {}
for name, me, ne in allfam:
    bad = []
    for j in range(0, 8):
        m, n = fam_mn(me, j), fam_mn(ne, j)
        if gcd(m, n) != 1:
            bad.append({"j": j, "m": m, "n": n, "gcd": gcd(m, n)})
    if bad:
        noncoprime[name] = bad
# does the re-derivation exclude F6(j=0)?  A1 of F6 = (9,5,4), k=2
f6_final = (9, 5, 4)
f6_mn = G.mn_pairs(f6_final, max_mn=200)
OUTJ["f6_check"] = {
    "families_with_noncoprime_members": noncoprime,
    "F6_MN_from_Definition_3.3": [{"k": k, "m": m, "n": n} for (k, m, n) in f6_mn],
    "F6_j0_pair_(4,10)_in_MN": any(m == 4 and n == 10 for (_, m, n) in f6_mn),
    "F6_diophantine_check_8m_minus_3n": {"m": 4, "n": 10, "value": 8*4 - 3*10},
}
print(f"\n[H] families whose printed (m,n) formula ever has gcd>1 for j=0..7: "
      f"{sorted(noncoprime)}")
for nm, bad in noncoprime.items():
    print(f"    {nm}: {[(x['j'], x['m'], x['n'], x['gcd']) for x in bad]}")
print(f"    MN((9/5,4)) from Definition 3.3 = {f6_mn}")
print(f"    (4,10) present in MN? {OUTJ['f6_check']['F6_j0_pair_(4,10)_in_MN']}")

with open(os.path.join(HERE, "gc_enum_audit.json"), "w") as fh:
    json.dump(OUTJ, fh, indent=1, default=str)
print(f"\n[done] {time.time()-t0:.1f}s -> gc_enum_audit.json")
