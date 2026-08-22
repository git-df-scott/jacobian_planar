#!/usr/bin/env python
import json, glob, collections, os
SP = os.path.dirname(os.path.abspath(__file__))
rows = {}
for fn in ['cells.jsonl','d6.jsonl']:
    path = os.path.join(SP,fn)
    if not os.path.exists(path): continue
    for line in open(path):
        line=line.strip()
        if not line: continue
        try: r = json.loads(line)
        except: continue
        if 'n' not in r:
            print('# odd row:', r); continue
        key = (r['n'], r['b'], r.get('p'), r['D'])
        rows[key] = r

def summarize(r):
    st = r.get('status')
    if st != 'solved': return st, ''
    cnt = collections.Counter(b['cls'] for b in r.get('branches',[]))
    # normalize old label
    if 'no-keller-specialization' in cnt:
        cnt['degenerate(det=0)*'] = cnt.pop('no-keller-specialization')
    parts = ', '.join('%dx %s'%(v,k) for k,v in sorted(cnt.items()))
    ex = ''
    for bch in r.get('branches',[]):
        if bch['cls']=='CANDIDATE':
            ex = 'CANDIDATE! ' + json.dumps(bch)
            break
        if bch['cls']=='nonlinear-tame-automorphism' and 'F1' in bch and not ex:
            ex = 'e.g. F=(%s ; %s)'%(bch['F1'],bch['F2'])
    return parts, ex

# keep highest D per (n,b,p) but also print all
print('| n | b | p | q | D | vars/eqs | branches | example nonlinear |')
print('|---|---|---|---|---|----------|----------|-------------------|')
cand = []
for key in sorted(rows, key=lambda k:(k[0],k[1],k[2] if k[2] is not None else -1,k[3])):
    r = rows[key]
    s, ex = summarize(r)
    if 'CANDIDATE' in s or (ex and ex.startswith('CANDIDATE')):
        cand.append((key,r))
    print('| %s | %s | %s | %s | %s | %s/%s | %s | %s |' % (
        r['n'], r['b'], r.get('p'), r.get('q','-'), r['D'],
        r.get('nvars','-'), r.get('neqs','-'), s, ex[:110]))
print()
if cand:
    print('## CANDIDATES (LOUD FLAG)')
    for key,r in cand: print(json.dumps(r, indent=1))
else:
    print('NO CANDIDATES: every nonzero-Jacobian solution branch in every solved cell classified as linear/affine or nonlinear tame automorphism (elementary-reducible).')
