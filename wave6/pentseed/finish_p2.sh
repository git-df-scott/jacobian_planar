#!/bin/bash
# Sequence, do not race: wait for the chain, then solve the DEEPEST export alone
# with the whole machine's memory.
cd /home/user/jacobian_planar
while pgrep -f "w6_prime2.py 1000033" >/dev/null; do sleep 10; done
# deepest = fewest variables = the file with the smallest NNv in its name
F=$(ls wave6/pentseed/reduced_p1000033_*v.ms 2>/dev/null \
    | sed 's/.*_\([0-9]*\)v\.ms/\1 &/' | sort -n | head -1 | cut -d' ' -f2)
[ -z "$F" ] && { echo "P2: no export produced" >> wave6/pentseed/prime_runs.log; exit 1; }
B=$(basename $F .ms)
# symbol guard re-check on the actual file before trusting any verdict
python3 - "$F" <<'PY' >> wave6/pentseed/prime_runs.log
import re,sys
L=open(sys.argv[1]).read().split('\n')
hdr=set(v.strip() for v in L[0].split(','))
used={t for t in re.findall(r'[A-Za-z_]\w*',"\n".join(L[2:]))}
print(f"{sys.argv[1].split('/')[-1]}: header {len(hdr)} used {len(used)} undeclared {len(used-hdr)} -> {'WELL-FORMED' if not used-hdr else 'MALFORMED'}")
PY
( ulimit -v 12000000; timeout 3000 msolve -t 3 -f $F -o wave6/pentseed/${B}.out 2>/dev/null )
E=$?
echo "P2=1000033 $B exit=$E bytes=$(stat -c%s wave6/pentseed/${B}.out 2>/dev/null) verdict=$(head -c 14 wave6/pentseed/${B}.out 2>/dev/null|tr -d '\n')" >> wave6/pentseed/prime_runs.log
[ $E -eq 139 ] && echo "  ^ exit 139 = SIGSEGV, NO VERDICT (memory)" >> wave6/pentseed/prime_runs.log
[ $E -eq 124 ] && echo "  ^ exit 124 = timeout, NO VERDICT" >> wave6/pentseed/prime_runs.log
echo "P2 SEQUENCE DONE" >> wave6/pentseed/prime_runs.log
