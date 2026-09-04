#!/bin/sh
# Restart-resilient engine ladder on the bilinear pentagon system.
# Each stage writes its own verdict file; a restart loses at most one stage.
cd /tmp/hunt
log() { echo "$(date -u +%H:%M:%S) $*" >> attack.log; }

stage() {  # name, timeout, command...
  name=$1; shift; tmo=$1; shift
  [ -f "done_$name" ] && return 0
  log "START $name (timeout ${tmo}s)"
  t0=$(date +%s)
  timeout "$tmo" "$@" > "out_$name.log" 2>&1
  ec=$?
  el=$(( $(date +%s) - t0 ))
  log "END $name exit=$ec wall=${el}s"
  echo "exit=$ec wall=${el}s" > "done_$name"
}

# 1. Groebner-only emptiness on the bilinear form (cheapest decisive question)
stage g2_bilin 900 msolve -t 2 -g 2 -f bilin_rigid.ms -o g2_bilin.out
# 2. Singular slimgb -- sparse low-degree is its regime (Example 15)
cat > sing_bilin.sing <<'SING'
ring R = 1000003, (x(1..180)), dp;
SING
python3 - <<'PY' >> sing_bilin.sing
lines=open('/tmp/hunt/bilin_rigid.ms').read().split('\n')
vs=[v.strip() for v in lines[0].split(',')]
body="\n".join(lines[2:]).strip().rstrip(',')
polys=[q.strip() for q in body.split(',\n') if q.strip()]
m={v:f"x({i+1})" for i,v in enumerate(vs)}
import re
def tr(q):
    return re.sub(r'[A-Za-z_][A-Za-z0-9_]*', lambda mo: m.get(mo.group(0),mo.group(0)), q)
print("ideal I =")
print(",\n".join(tr(q) for q in polys)+";")
print('option(redSB); ideal G = slimgb(I); if (size(G)==1 and G[1]==1) { "VERDICT EMPTY"; } else { "VERDICT NONEMPTY_OR_POSDIM"; "size:"; size(G); "dim:"; dim(std(G)); }')
print('exit;')
PY
stage slimgb_bilin 1500 Singular -q sing_bilin.sing
# 3. full solve on the bilinear form
stage solve_bilin 1500 msolve -t 2 -f bilin_rigid.ms -o solve_bilin.out
log "LADDER COMPLETE"
