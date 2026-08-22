#!/bin/bash
cd /home/user/jacobian_planar
for f in wave5/ms/m16_d6_p1000003.ms wave5/ms/m16_d7_p1000033.ms \
         wave5/ms2/b16r_d5_A_q.ms wave5/ms2/b16r_d6_A_q.ms wave5/ms2/b16r_d7_A_q.ms \
         wave5/ms/u16_d7_q.ms wave4/artifacts/c2_w4_one_real_p1000003.ms \
         wave4/artifacts/probe_w4m4_real_p1000003.ms; do
  [ -f "$f" ] || continue
  echo "### $f" >> wave6/frontier/ranked.log
  LEAF_T=180 LEAF_MEM=4000000 timeout 1500 python3 -u wave6/w6_branch_solve.py "$f" \
      >> wave6/frontier/ranked.log 2>&1
done
echo "RANKED DONE" >> wave6/frontier/ranked.log
