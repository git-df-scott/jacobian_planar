#!/bin/bash
# Auto-commit Track B Singular results when runs terminate. Pure shell, no model.
cd /home/user/jacobian_planar
for i in $(seq 1 360); do
  sleep 60
  n_running=$(pgrep -c Singular 2>/dev/null || echo 0)
  new=$(git status --porcelain trackB_leaf*.out trackB_leaf*.sing 2>/dev/null | wc -l)
  if [ "$n_running" -eq 0 ] && [ "$new" -gt 0 ]; then
    git add trackB_leaf*.out trackB_leaf*.sing trackB_leaf_runner.py 2>/dev/null
    git commit -q -m "Track B: Singular leaf run results (auto-checkpoint)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01S16hvx8YXLFQXDUhAX6ZH5" && git push -q origin claude/counter-example-audit-dnu9l9
    echo "[autopush] pushed at $(date -u)" >> trackB_autopush.log
  fi
done
