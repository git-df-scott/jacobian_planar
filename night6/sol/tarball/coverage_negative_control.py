#!/usr/bin/env python3
import argparse
import sys

ap=argparse.ArgumentParser();ap.add_argument("--chain-map-dir",required=True);args=ap.parse_args()
sys.path.insert(0,args.chain_map_dir)
import trackD_chain_map as t
f9=next(c for c in t.all_chains() if c.name=="F9(m,n)=2,3")
candidates,_=t.reduced_candidates(f9)
assert candidates and {c["r"] for c in candidates}=={2}
published_r=1
published_P=t.hull([(0,0),(4,0),(6,2),(0,14)])
published_Q=t.hull([(0,0),(6,0),(9,3),(0,21)])
assert published_r!=candidates[0]["r"]
assert all(c["NP"]!=published_P or c["NQ"]!=published_Q for c in candidates)
print("PASS: universal extrapolator predicts x^2/different polygons; published Proposition 4.4 gives x")
