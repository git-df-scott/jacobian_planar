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

# ERRATA A16: msolve silently mis-parses parentheses and reports basis [1] --
# a false EMPTY with exit 0 and no warning.  Refuse such input outright.
guard_msolve() {
  for f in "$@"; do
    case "$f" in
      *.ms) if grep -q '(' "$f"; then
              echo "REFUSED: $f contains parentheses; msolve would report a false EMPTY (A16)"
              return 1
            fi ;;
    esac
  done
  return 0
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
# EIGHTH-POWER target: A(t) = c0 (t-tau)^8 and Qh = c1 (t-tau)^12 substituted into
# Codex's degree-2 export.  21 coefficients eliminated, replaced by tau and its
# named powers T_j (T_j - tau*T_{j-1} = 0) so the degree stays 4.  179 vars --
# inside msolve's exponent-hash ceiling.  Fully expanded (A16).
# Controls: substitution value-preserving on all 306 equations, tau-power
# defining equations vanish, and TWO negative controls (perturb tau with all T_j
# recomputed; leave T_j stale while tau moves).  All PASS.
guard_msolve /tmp/red/eighth.ms && \
run_job eighth_g2 none 2400 \
  msolve -t 2 -g 2 -f /tmp/red/eighth.ms -o "$Q/eighth_g2.out"

# Weaker upper-edge form (A = c0 G^2), 170 vars, expanded.
guard_msolve /tmp/red/subst_exp.ms && \
run_job upper_subst_exp_g2 none 2400 \
  msolve -t 2 -g 2 -f /tmp/red/subst_exp.ms -o "$Q/upper_subst_exp_g2.out"

# Additive form, 214 vars, all degree 2 -- Singular's lane (it parses parens).
run_job reduced_sing none 2400 Singular -q /tmp/red/reduced.sing

log "QUEUE COMPLETE"
