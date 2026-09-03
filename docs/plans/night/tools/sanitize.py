import sys, re
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().split('\n')
vars_ = [v.strip() for v in lines[0].split(',')]
p = int(lines[1].strip())
body = '\n'.join(lines[2:])
gens = [g.strip() for g in re.split(r',\s*\n', body) if g.strip()]
gens = [g.rstrip(',').strip() for g in gens]
used = set(re.findall(r'[A-Za-z_]\w*', body))
keep = [v for v in vars_ if v in used]
dropped = [v for v in vars_ if v not in used]
bad = []
for g in gens:
    for m in re.finditer(r'(?<![\w*^])(\d+)(?![\w^])', g):
        c = int(m.group(1))
        if c >= p or c == 0: bad.append((c, g[:60]))
    if re.fullmatch(r'-?\d+', g): bad.append(('CONST', g))
if bad:
    print('BAD', bad[:5]); sys.exit(2)
with open(dst, 'w') as f:
    f.write(','.join(keep) + '\n' + str(p) + '\n')
    f.write(',\n'.join(gens) + '\n')
# round trip
l2 = open(dst).read().split('\n')
g2 = [g.strip() for g in re.split(r',\s*\n', '\n'.join(l2[2:])) if g.strip()]
assert len(g2) == len(gens), (len(g2), len(gens))
print(f'{dst}: vars {len(vars_)}->{len(keep)} dropped {dropped}, gens {len(gens)}, p {p}, p mod 3 = {p%3}')
