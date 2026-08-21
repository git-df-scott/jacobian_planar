#!/usr/bin/env python3
"""Broad sweep: point the NEW engine at every unsolved cell in the repo.

MATTHEUS-VERSTRAETE MOVE
------------------------
The campaign's walls were set with the tools it had (msolve, sympy, Mathematica
upstream). Singular's `slimgb` was never installed here. Before treating any of
those walls as structural, re-run them with the newer engine -- that is what
broke the last wall, and the lesson is to ask it again at each one rather than
assume this one is different.

WHAT COUNTS AS A LEAD
  NOTUNIT  -> the ideal is proper, so the cell's variety is NONEMPTY over the
              algebraic closure. That is a live candidate and the whole point of
              the sweep. Report loudly; it does NOT yet mean a counterexample,
              because the cell's side conditions still have to be checked.
  UNIT     -> the cell is EMPTY. Closed (mod p), with a certificate available
              via lift if wanted.
  TIMEOUT / crash -> NO VERDICT. Never recorded as either of the above.

Cheapest first, one at a time (sequence, do not race), each capped.
"""
import os, re, sys, subprocess, json, time

ROOT = '/home/user/jacobian_planar'
SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad/sweep')
PER_FILE_TIMEOUT = int(os.environ.get('SWEEP_T', '150'))
MEM_KB = '3000000'


def unsolved():
    out = []
    for dirpath, _, files in os.walk(ROOT):
        if '/.git' in dirpath:
            continue
        for fn in files:
            if not fn.endswith('.ms'):
                continue
            p = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            if sz == 0 or sz > 8_000_000:
                continue
            o = p[:-3] + '.out'
            # unsolved = no .out, or an EMPTY .out (which is NOT a verdict)
            if os.path.exists(o) and os.path.getsize(o) > 0:
                continue
            out.append((sz, p))
    out.sort()
    return out


def to_singular(src, dst):
    L = open(src).read().split('\n')
    if len(L) < 3:
        return None
    vs = [v.strip() for v in L[0].split(',') if v.strip()]
    ch = L[1].strip()
    if not re.fullmatch(r'\d+', ch):
        return None
    body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    if not vs or not body:
        return None
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    if used - set(vs):
        return 'MALFORMED'
    open(dst, 'w').write(
        f'ring R = {ch}, ({",".join(vs)}), dp;\nideal I = ' + ",\n".join(body) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "RESULT UNIT"; }\n'
        'else { "RESULT NOTUNIT"; "dim:"; dim(G); "gbsize:"; size(G); }\nexit;\n')
    return (len(vs), len(body), ch)


def main():
    os.makedirs(SCR, exist_ok=True)
    todo = unsolved()
    print(f"unsolved exports found: {len(todo)}", flush=True)
    log = os.path.join(ROOT, 'wave6/sweep_cells.log')
    leads, empt, nov, mal = [], 0, 0, 0
    t0 = time.time()
    with open(log, 'a') as LG:
        LG.write(f"\n=== sweep start, {len(todo)} candidates, "
                 f"timeout {PER_FILE_TIMEOUT}s each ===\n")
        for k, (sz, p) in enumerate(todo):
            rel = os.path.relpath(p, ROOT)
            dst = os.path.join(SCR, f's{k}.sing')
            info = to_singular(p, dst)
            if info is None:
                continue
            if info == 'MALFORMED':
                mal += 1
                LG.write(f"MALFORMED {rel}\n"); LG.flush()
                continue
            nv, ne, ch = info
            r = subprocess.run(
                ['bash', '-c',
                 f'ulimit -v {MEM_KB}; timeout {PER_FILE_TIMEOUT} Singular -q {dst}'],
                capture_output=True, text=True)
            o = r.stdout
            if 'RESULT UNIT' in o:
                empt += 1
                LG.write(f"EMPTY     {rel}  ({nv}v {ne}eq char {ch})\n")
            elif 'RESULT NOTUNIT' in o:
                d = re.search(r'dim:\s*\n?\s*(-?\d+)', o)
                leads.append((rel, nv, ne, ch, d.group(1) if d else '?'))
                LG.write(f"*** NONEMPTY LEAD {rel}  ({nv}v {ne}eq char {ch}) "
                         f"dim={d.group(1) if d else '?'}\n")
                print(f"  *** LEAD: {rel} ({nv}v {ne}eq) dim={d.group(1) if d else '?'}",
                      flush=True)
            else:
                nov += 1
                LG.write(f"NOVERDICT {rel}  ({nv}v {ne}eq char {ch})\n")
            LG.flush()
            if k % 20 == 0:
                print(f"  [{k}/{len(todo)}] empty={empt} leads={len(leads)} "
                      f"noverdict={nov} elapsed={time.time()-t0:.0f}s", flush=True)
        LG.write(f"=== done: {empt} empty, {len(leads)} leads, {nov} no-verdict, "
                 f"{mal} malformed ===\n")
    print(f"\nSWEEP DONE: {empt} EMPTY, {len(leads)} NONEMPTY LEADS, "
          f"{nov} NO VERDICT, {mal} malformed")
    for l in leads:
        print(f"  LEAD {l}")
    json.dump([{'file': a, 'vars': b, 'eqs': c, 'char': d, 'dim': e}
               for a, b, c, d, e in leads],
              open(os.path.join(ROOT, 'wave6/sweep_leads.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
