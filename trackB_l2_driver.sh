#!/bin/bash
cd /home/user/jacobian_planar
ls trackB_l2_r*.sing | xargs -P 4 -I{} sh -c 'Singular -q {} > {}.out 2>&1; grep -h "BRANCH" {}.out' | tee trackB_l2_verdicts.log
echo "ALL BRANCH RUNS DONE $(date -u)" >> trackB_l2_verdicts.log
