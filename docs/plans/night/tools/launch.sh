#!/bin/bash
# usage: launch.sh <name> <file.ms> <threads> <memKB>
n=$1; f=$2; t=$3; mem=$4
M=/tmp/msolve-0.10.1/bin/msolve
( ulimit -v $mem; S=$(date +%s); echo "START $(date -u +%FT%TZ) $f threads=$t memKB=$mem" >> $n.log
  $M -g 2 -t $t -f $f -o $n.out 2> $n.err; ec=$?
  echo "END $(date -u +%FT%TZ) exit=$ec wall=$(( $(date +%s)-S ))s outbytes=$(stat -c %s $n.out 2>/dev/null)" >> $n.log ) &
echo $!
