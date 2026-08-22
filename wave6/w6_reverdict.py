#!/usr/bin/env python3
"""Re-run every NOVERDICT cell from the sweep with a REAL budget.

The sweep gave each cell 150 seconds and 3 GB. 69 cells came back NOVERDICT,
and most of them are TINY -- 7, 17, 20, 22, 23, 25, 27, 30 variables. A
7-variable system does not fail because it is hard; it fails because 150s is
not a budget. The same mistake as tier 1, where the easiest form of the target
got 4 GB and two minutes while the hardest got 9 GB and hours.

Cheapest first, each with 20 minutes and 6 GB, both engines. Reports UNIT
(EMPTY), NOTUNIT (NONEMPTY -- a lead), or an honest NOVERDICT.
"""
import os, re, sys, subprocess, time, json

ROOT = '/home/user/jacobian_planar'
SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad/reverdict')
T = int(os.environ.get('RV_T', '1200'))
MEM = os.environ.get('RV_MEM', '6000000')


def cells():
    out, seen = [], set()
    for line in open(os.path.join(ROOT, 'wave6/sweep_cells.log')):
        if not line.startswith('NOVERDICT'):
            continue
        m = re.match(r'NOVERDICT\s+(\S+)\s+\((\d+)v\s+(\d+)eq', line)
        if not m:
            continue
        rel, nv, ne = m.group(1), int(m.group(2)), int(m.group(3))
        if rel in seen:
            continue
        seen.add(rel)
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        try:
            ch = open(p).read().split('\n')[1].strip()
        except Exception:
            ch = '0'
        # Characteristic ZERO last, regardless of size. Sorting purely by
        # variable count put two 7-variable char-0 cells at the head of the
        # queue, and char-0 Groebner is far harder than mod p at any size --
        # so the two hardest cells would have consumed the budget before the
        # 60-odd tractable ones were reached. Size is not difficulty here.
        out.append((1 if ch == '0' else 0, nv, ne, rel))
    out.sort()
    return [(nv, ne, rel) for _, nv, ne, rel in out]


def run(rel, nv, ne):
    src = os.path.join(ROOT, rel)
    L = open(src).read().split('\n')
    vs = [v.strip() for v in L[0].split(',') if v.strip()]
    ch = L[1].strip()
    body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    if leak:
        return 'MALFORMED', f'undeclared {leak[:4]}'
    tag = re.sub(r'\W+', '_', rel)
    f = os.path.join(SCR, tag + '.sing')
    open(f, 'w').write(
        f'ring R = {ch}, ({",".join(vs)}), dp;\nideal I = ' + ",\n".join(body) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "RV UNIT"; }\n'
        'else { "RV NOTUNIT"; "dim:"; dim(G); }\nexit;\n')
    r = subprocess.run(['bash', '-c',
                        f'ulimit -v {MEM}; timeout {T} Singular -q {f}'],
                       capture_output=True, text=True)
    o = r.stdout
    if 'RV UNIT' in o:
        return 'EMPTY', 'slimgb'
    if 'RV NOTUNIT' in o:
        d = re.search(r'dim:\s*\n?\s*(-?\d+)', o)
        return 'NONEMPTY', f'dim={d.group(1) if d else "?"}'
    # second engine, only where msolve can apply (positive characteristic)
    if ch != '0':
        ms = os.path.join(SCR, tag + '.ms')
        open(ms, 'w').write(",".join(vs) + f"\n{ch}\n" + ",\n".join(body) + "\n")
        subprocess.run(['bash', '-c',
                        f'ulimit -v {MEM}; timeout {T} msolve -f {ms} '
                        f'-o {ms}.out 2>/dev/null'], capture_output=True, text=True)
        try:
            v = open(ms + '.out').read().strip()
        except OSError:
            v = ''
        if v.startswith('[-1]'):
            return 'EMPTY', 'msolve'
        if v.startswith('[0') or v.startswith('[1'):
            return 'NONEMPTY', 'msolve'
    return 'NOVERDICT', f'both engines, {T}s'


def main():
    os.makedirs(SCR, exist_ok=True)
    todo = cells()
    # RESUME: the container restarted mid-run once and killed every process
    # abruptly. Completed cells are already in reverdict.json, so skip them
    # rather than paying for them again on each restart.
    done = {}
    jp = os.path.join(ROOT, 'wave6/reverdict.json')
    if os.path.exists(jp):
        try:
            for r in json.load(open(jp)):
                if r['status'] in ('EMPTY', 'NONEMPTY', 'MALFORMED'):
                    done[r['file']] = r
        except Exception:
            done = {}
    if done:
        print(f"resuming: {len(done)} cells already decided, skipping them",
              flush=True)
    todo = [t for t in todo if t[2] not in done]
    print(f"NOVERDICT cells to re-run: {len(todo)}  "
          f"(budget {T}s / {int(MEM)//1000}MB each, was 150s/3000MB)", flush=True)
    res = list(done.values())
    t0 = time.time()
    for i, (nv, ne, rel) in enumerate(todo):
        st, info = run(rel, nv, ne)
        res.append({'file': rel, 'vars': nv, 'eqs': ne, 'status': st, 'info': info})
        mark = '***' if st == 'NONEMPTY' else '   '
        print(f"{mark} [{i+1}/{len(todo)}] {st:9s} {rel}  ({nv}v {ne}eq) {info}",
              flush=True)
        json.dump(res, open(os.path.join(ROOT, 'wave6/reverdict.json'), 'w'), indent=1)
    n = lambda s: sum(1 for r in res if r['status'] == s)
    print(f"\nDONE in {time.time()-t0:.0f}s: {n('EMPTY')} EMPTY, "
          f"{n('NONEMPTY')} NONEMPTY, {n('NOVERDICT')} still no verdict, "
          f"{n('MALFORMED')} malformed")
    for r in res:
        if r['status'] == 'NONEMPTY':
            print(f"  *** LEAD: {r['file']} {r['info']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
