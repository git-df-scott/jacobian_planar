#!/bin/bash
cd /tmp/wt/charts; M=/tmp/msolve-0.10.1/bin/msolve
done_list=""
while true; do
  for j in $(ls */*_charts.json 2>/dev/null); do
    for f in $(python3 -c "import json,sys; [print(r['file']) for r in json.load(open('$j')) if 'file' in r]"); do
      n=$(basename $f .ms); echo "$done_list" | grep -q " $n " && continue
      S=$(date +%s); ( ulimit -v 4000000; timeout 1800 $M -g 2 -t 1 -f $f -o $n.out 2> $n.err ); ec=$?; W=$(( $(date +%s)-S ))
      if [ -s $n.out ] && grep -q "^\[1\]:" $n.out; then v="EMPTY-mod-p ([1] basis)";
      elif [ -s $n.out ] && grep -q "^\[" $n.out; then v="NONUNIT basis ($(grep -c . $n.out) lines) -- NOT EMPTY on this chart";
      elif [ $ec -eq 124 ]; then v="TIMEOUT 1800s"; else v="NO OUTPUT exit=$ec ($(head -c 100 $n.err | tr '\n' ' '))"; fi
      echo "$n | $(python3 -c "import json; print([r['hist'] for r in json.load(open('$j')) if r.get('file','').endswith('$n.ms')][0])") | ${W}s | $v" >> chartqueue.log
      done_list="$done_list $n "
    done
  done
  grep -q REDUCE_DONE reduce.log 2>/dev/null && [ $(ls */*_charts.json | wc -l) -le $(echo "$done_list" | wc -w) ] && break
  sleep 30
done
echo CHARTQUEUE_DONE >> chartqueue.log
