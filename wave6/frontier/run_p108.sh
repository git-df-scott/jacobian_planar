#!/bin/bash
# The (9,27) branch of (72,108): four systems, all previously TIMEOUT/NO VERDICT.
# Sequence, do not race.
cd /home/user/jacobian_planar
for f in wave6/ms/p108_525122.ms wave6/ms/p108_843700.ms wave6/ms/p108_821326.ms wave6/ms/p108_192622.ms; do
  b=$(basename $f .ms)
  echo "### $b" >> wave6/frontier/p108_branch.log
  LEAF_T=150 LEAF_MEM=4000000 timeout 2400 python3 -u wave6/w6_branch_solve.py $f \
      >> wave6/frontier/p108_branch.log 2>&1
  echo "### $b exit=$?" >> wave6/frontier/p108_branch.log
done
echo "P108 ALL DONE" >> wave6/frontier/p108_branch.log
