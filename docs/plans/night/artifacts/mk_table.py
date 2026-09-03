import json, collections, re
S=json.load(open('/tmp/wt/fastx/sweep_mono.json')); C={c['sid']:c for c in json.load(open('/tmp/wt/fastx/certified.json'))}
rows=[]; summary=collections.Counter()
for r in S:
    res=r['result']; kind=res.split(' ')[0]; summary[kind]+=1
    if kind=='KILLED':
        c=C.get(r['sid']); cert=c['certs'][0] if c and c.get('certs') else None
        rows.append((tuple(r['degrees']), r['maxdeg'], r['tag'], int(re.search(r'jextra (\d+)',res).group(1)), (f"row {cert['row']}, x^{cert['xexp']}: {cert['gen']}" if cert else 'exact-Q pending'), c['exactQ'] if c else 'pending'))
rows.sort()
print('| degrees | max | shape (chain, c\', eps) | depth | exact certificate over Q (coefficient of x^e in Q_row) | status |')
print('|---|---|---|---|---|---|')
for d,m,tag,J,cert,st in rows: print(f'| {d} | {m} | {tag} | {J} | {cert} | {st} |')
print(); print('Summary:', dict(summary))
surv=[r for r in S if r['result'].startswith('SURVIVES')]
print(); print('Survivors (no monomial certificate to depth 12):'); 
for r in surv: print(f"- {tuple(r['degrees'])} max {r['maxdeg']}: {r['tag']}")
unb=[r for r in S if r['result'].startswith('UNBUILDABLE') or r['result'].startswith('SKIPPED')]
print(); print(f'Unbuildable or skipped ({len(unb)}):'); 
for r in unb: print(f"- {tuple(r['degrees'])} max {r['maxdeg']}: {r['tag']} | {r['result']} | npar {r['npar']}")
