#!/bin/sh
# Restart-resilient job runner.
#
# The container is a microVM that the platform can restart at any time; a restart
# kills running processes but the filesystem survives, and git survives even a
# full container replacement.  So: every job checkpoints its verdict to disk AND
# to the remote before the next job starts.  A restart loses at most one job.
#
# Memory discipline: msolve CANNOT run under `ulimit -v` -- it reserves address
# space for its exponent hash table and segfaults ("Enlarging exponent vector for
# hash table failed") rather than failing cleanly.  I hit this at 05:45 with the
# planted instance, documented it, and then re-introduced it here at 15:21,
# sabotaging both Cor 5.7 runs.  So: NO ulimit for msolve.  Containment is by
# timeout plus one-job-at-a-time; a genuine memcg OOM is recorded as NO VERDICT.
#
# Usage:  runner.sh            # runs the queue, skipping anything already done
# Re-run it after any restart; it resumes.

Q=/home/user/jacobian_planar/session43/queue
mkdir -p "$Q/done"
log() { echo "$(date -u +%FT%TZ) $*" >> "$Q/runner.log"; }

verdict_of() {  # $1 = outfile, $2 = exit code
  if [ ! -s "$1" ]; then echo "NO VERDICT (exit=$2, empty output)"; return; fi
  head -c 4 "$1" | grep -q '\[-1\]' && { echo "EMPTY"; return; }
  grep -qa "VERDICT EMPTY" "$1" && { echo "EMPTY"; return; }
  grep -qa "VERDICT NONEMPTY" "$1" && { echo "NONEMPTY_OR_POSDIM"; return; }
  echo "NONEMPTY_OR_POSDIM (raw: $(head -c 60 "$1" | tr '\n' ' '))"
}

run_job() {   # name, memcap_kb, timeout_s, command...
  name=$1; cap=$2; tmo=$3; shift 3
  [ -f "$Q/done/$name" ] && return 0
  log "START $name cap=${cap}kb timeout=${tmo}s"
  t0=$(date +%s)
  if [ "$cap" = "none" ]; then
    timeout "$tmo" "$@" > "$Q/$name.raw" 2>&1
  else
    ( ulimit -v "$cap"; timeout "$tmo" "$@" ) > "$Q/$name.raw" 2>&1
  fi
  ec=$?
  el=$(( $(date +%s) - t0 ))
  v=$(verdict_of "$Q/$name.out" "$ec")
  printf 'job=%s exit=%s wall=%ss verdict=%s\n' "$name" "$ec" "$el" "$v" > "$Q/done/$name"
  log "END $name exit=$ec wall=${el}s verdict=$v"
  # checkpoint to the remote immediately -- survives even container replacement
  cd /home/user/jacobian_planar 2>/dev/null && {
    git add -A session43/queue >/dev/null 2>&1
    git commit -q -m "queue: $name -> $v (exit=$ec, ${el}s)" >/dev/null 2>&1
    git push -q origin claude/ce-acquisition-strategy-uyqftb >/dev/null 2>&1
  }
}

# ---- the queue -------------------------------------------------------------
# Cor 5.7 shape 2, Groebner-only.  Emptiness is exactly what Cor 5.7 claims, and
# -g 2 decides it at ANY dimension, unlike solve mode.
# NO ulimit cap: msolve reserves address space for its exponent hash table, so
# ulimit -v segfaults it rather than bounding it (ERRATA A13).
run_job cor57_g2b none 5400 \
  msolve -t 2 -g 2 -f /tmp/hunt/p108_525122_sliced.ms -o "$Q/cor57_g2b.out"

# Cor 5.7 shape 1 (40 vars), same treatment, never yet given Groebner-only.
run_job cor57_s1_g2b none 5400 \
  msolve -t 2 -g 2 -f /tmp/hunt/p108_192622_sliced.ms -o "$Q/cor57_s1_g2b.out"

log "QUEUE COMPLETE"
