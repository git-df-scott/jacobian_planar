#!/bin/bash
# Solve the sieved seed-pinned systems.  Each capped so a runaway cannot take
# the machine.  An EMPTY output file from a dead process is NOT a verdict.
cd /home/user/jacobian_planar
run(){ f=$1; cap=$2; th=$3
  ( ulimit -v $cap; timeout 3300 msolve -t $th -f wave6/pentseed/$f.ms \
      -o wave6/pentseed/$f.out 2>wave6/pentseed/$f.err )
  echo "$(date +%T) $f exit=$? size=$(stat -c%s wave6/pentseed/$f.out 2>/dev/null)" \
      >> wave6/pentseed/reduced_runs.log
}
run reduced_99v 5000000 2 &
run reduced_93v 6000000 2 &
wait
echo DONE >> wave6/pentseed/reduced_runs.log
