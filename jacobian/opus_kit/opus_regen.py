#!/usr/bin/env python3
"""Regenerate the 16 unique resister systems + 1 control from the committed
trackD pipeline, verify against pinned MD5s, convert to msolve, run at long
budget.  Selection is BY CHECKSUM: every candidate shape of a matched chain
is generated (facstd budget 1s, we only want the .sing) and kept only if its
md5 appears in resister_specs.json.  Fail-loud on any spec never matched.

Usage: python3 opus_regen.py /path/to/repo [budget_seconds=1800]
Requires: Singular on PATH, msolve on PATH, repo cloned at branch
claude/opus-5-counterexample-plan-sep6yk.
Reports RAW verdict lines only; [-1] = EMPTY, nonempty head = CANDIDATE
(report immediately, do NOT interpret), 0 bytes = FAILURE not verdict.
Control gate: w6_289012_0 MUST come back [-1] quickly; if it does not,
STOP and report the control failure instead of any other result.
"""
import sys, os, json, hashlib, subprocess, time, re

ROOT = os.path.abspath(sys.argv[1])
BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
AT = os.path.join(ROOT, 'campaign/audit_tracks')
SCR = os.path.join(AT, '_scratch')
OUT = os.path.join(ROOT, 'wave6/ms_opus')
os.makedirs(OUT, exist_ok=True)
os.makedirs(SCR, exist_ok=True)
sys.path.insert(0, AT)
os.chdir(AT)
import trackD_chain_map as CM, trackD_extract as EX

specs = json.load(open(os.path.join(ROOT, 'jacobian/opus_kit/resister_specs.json')))
want = {s['md5']: s for s in specs}
heads = set()
for s in specs:
    heads.add(s['case'].split('|')[0].strip().replace(' ', ''))

chains = {getattr(c, 'name', str(c)): c for c in CM.all_chains()}
found = {}   # md5 -> local .sing path
gen = 0
for cname, ch in chains.items():
    cn = cname.replace(' ', '')
    if not any(cn.startswith(h) or h.startswith(cn) for h in heads):
        continue
    r = CM.reduced_candidates(ch)
    cands = r[0] if isinstance(r, tuple) else r
    for i, cd in enumerate(cands):
        nm = f"regen_{abs(hash(cname)) % 10**6}_{i}"
        try:
            EX.run(cd['NP'], cd['NQ'], cd['r'], nm, timeout=1)
        except Exception:
            pass
        p = os.path.join(SCR, f'extract_{nm}.sing')
        if not os.path.exists(p):
            continue
        gen += 1
        h = hashlib.md5(open(p, 'rb').read()).hexdigest()
        if h in want and h not in found:
            found[h] = p
            print(f"MATCH {want[h]['name']} <- {cname} shape {i} md5 {h}", flush=True)

missing = [s['name'] for s in specs if s['md5'] not in found]
print(f"generated {gen} shapes; matched {len(found)}/{len(specs)}; MISSING: {missing}", flush=True)
if missing:
    print("SPEC-MISMATCH: report this and STOP; do not run partial results as if complete.", flush=True)

def bridge_and_run(name, sing_path, budget):
    txt = open(sing_path).read()
    cut = txt.index('int t0 = timer')
    dump = txt[:cut] + f'\nwrite(":w {OUT}/{name}.gens", string(simplify(I,2)));\nquit;\n'
    dpath = os.path.join(OUT, f'{name}_dump.sing')
    open(dpath, 'w').write(dump)
    subprocess.run(['Singular', '-q', dpath], capture_output=True, text=True, timeout=900)
    gens = open(os.path.join(OUT, f'{name}.gens')).read().strip().rstrip(',')
    gens = gens.replace('c(', 'c_').replace(')', '')
    if '(' in gens:
        raise RuntimeError('unexpected parens in generators')
    m = re.search(r'ring R = (\d+), \(c\(1\.\.(\d+)\), ([a-z0-9, ]+)\)', txt)
    char, nc, extra = m.group(1), int(m.group(2)), m.group(3)
    vars_ = [f'c_{i}' for i in range(1, nc + 1)] + [v.strip() for v in extra.split(',')]
    ms = ','.join(vars_) + '\n' + char + '\n' + ',\n'.join(
        g.strip() for g in gens.split(',') if g.strip()) + '\n'
    mpath = os.path.join(OUT, f'{name}.ms')
    open(mpath, 'w').write(ms)
    opath = os.path.join(OUT, f'{name}.out')
    t0 = time.time()
    try:
        subprocess.run(['msolve', '-t', '2', '-f', mpath, '-o', opath], timeout=budget)
    except subprocess.TimeoutExpired:
        return {'name': name, 'verdict': 'MS-TIMEOUT', 'wall': round(time.time() - t0, 1)}
    data = open(opath).read(80) if os.path.exists(opath) else ''
    v = 'EMPTY' if data.startswith('[-1]') else ('NO-OUTPUT-FAILURE' if not data else 'NONEMPTY-RAW')
    return {'name': name, 'verdict': v, 'head': data[:60], 'wall': round(time.time() - t0, 1)}

results = []
order = ['w6_289012_0'] + [s['name'] for s in specs if s['name'] != 'w6_289012_0']
by_name = {s['name']: s for s in specs}
for name in order:
    s = by_name[name]
    if s['md5'] not in found:
        continue
    budget = 120 if name == 'w6_289012_0' else BUDGET
    try:
        r = bridge_and_run(name, found[s['md5']], budget)
    except Exception as e:
        r = {'name': name, 'verdict': f'BRIDGE-ERROR {e}'}
    print(json.dumps(r), flush=True)
    results.append(r)
    json.dump(results, open(os.path.join(OUT, 'opus_results.json'), 'w'), indent=1)
    if name == 'w6_289012_0' and r.get('verdict') != 'EMPTY':
        print('CONTROL-FAILURE: w6_289012_0 did not return [-1]. STOP. Report this.', flush=True)
        break
print('OPUS-REGEN-DONE', flush=True)
