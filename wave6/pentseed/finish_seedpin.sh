#!/bin/bash
# Sequence: wait for the chain, symbol-guard the file, then solve it ALONE.
cd /home/user/jacobian_planar
P=$1
while pgrep -f "w6_seed_prime.py $P" >/dev/null; do sleep 10; done
for F in $(ls wave6/pentseed/seedpin_${P}_*v.ms 2>/dev/null | sed 's/.*_\([0-9]*\)v\.ms/\1 &/' | sort -n | cut -d' ' -f2); do
  B=$(basename $F .ms)
  python3 - "$F" <<'PY' >> wave6/pentseed/prime_runs.log
import re,sys
L=open(sys.argv[1]).read().split('\n')
hdr=set(v.strip() for v in L[0].split(','))
used={t for t in re.findall(r'[A-Za-z_]\w*',"\n".join(L[2:]))}
print(f"{sys.argv[1].split('/')[-1]}: hdr {len(hdr)} used {len(used)} undeclared {len(used-hdr)} -> {'WELL-FORMED' if not used-hdr else 'MALFORMED'}")
PY
  ( ulimit -v 12000000; timeout 3000 msolve -t 3 -f $F -o wave6/pentseed/${B}.out 2>/dev/null )
  E=$?
  V=$(head -c 14 wave6/pentseed/${B}.out 2>/dev/null | tr -d '\n')
  S=$(stat -c%s wave6/pentseed/${B}.out 2>/dev/null)
  echo "SEEDPIN p=$P $B exit=$E bytes=$S verdict=$V" >> wave6/pentseed/prime_runs.log
  [ $E -eq 139 ] && echo "  ^ SIGSEGV = NO VERDICT (memory)" >> wave6/pentseed/prime_runs.log
  [ $E -eq 124 ] && echo "  ^ timeout = NO VERDICT" >> wave6/pentseed/prime_runs.log
  [ "$S" != "0" ] && break     # got a real verdict; deeper files unnecessary
done
echo "SEEDPIN $P DONE" >> wave6/pentseed/prime_runs.log
