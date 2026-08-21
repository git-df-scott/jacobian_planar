#!/bin/bash
# Reduce case (1) mod p, then solve.  Real run and planted control, same code.
cd /home/user/jacobian_planar
P=$1; MODE=$2   # MODE = "" or "control"
TAG="p${P}"; [ -n "$MODE" ] && TAG="p${P}ctl"
timeout 2000 python3 -u wave6/w6_prime2.py $P $MODE > wave6/pentseed/${TAG}_chain.log 2>&1
echo "chain exit=$?" >> wave6/pentseed/${TAG}_chain.log
for f in $(ls -S wave6/pentseed/reduced_${TAG}_*v.ms 2>/dev/null | tail -2); do
  b=$(basename $f .ms)
  ( ulimit -v 7000000; timeout 2400 msolve -t 2 -f $f -o wave6/pentseed/${b}.out 2>/dev/null )
  echo "$b exit=$? bytes=$(stat -c%s wave6/pentseed/${b}.out 2>/dev/null) verdict=$(head -c 14 wave6/pentseed/${b}.out 2>/dev/null|tr -d '\n')" >> wave6/pentseed/prime_runs.log
done
echo "$TAG DONE" >> wave6/pentseed/prime_runs.log
