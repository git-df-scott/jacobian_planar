#!/bin/bash
cd /tmp/wt/fastx
for sid in s4f232a scb0881 s440259 sab7d9e s6cc334 s0a07a3 s20640c s96695e s3a7bae s084c74 sefaf8c s93673d; do
  for p in 65521 1000003 1000033; do
    ( ulimit -v 2500000; timeout 900 python3 genone.py $sid $p ) >> gen_index.jsonl 2> gen_err_${sid}_$p.txt
    ec=$?; [ $ec -ne 0 ] && echo "{\"sid\": \"$sid\", \"p\": $p, \"failed_exit\": $ec}" >> gen_index.jsonl
  done
done
echo DONE >> gen_index.jsonl
