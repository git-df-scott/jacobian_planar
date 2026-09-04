import re, sys
dump, out, p = sys.argv[1], sys.argv[2], sys.argv[3]
gens=[]
for line in open(dump):
    line=line.strip()
    if line.startswith('GEN '):
        gens.append(line[4:].strip())
gens=[g for g in gens if g and g!='0']
txt="\n".join(gens)
txt2=re.sub(r'c\((\d+)\)', r'c_\1', txt)
gens=[re.sub(r'c\((\d+)\)', r'c_\1', g) for g in gens]
vs=sorted({v for v in re.findall(r'[A-Za-z_]\w*', "\n".join(gens))},
          key=lambda s:(s[0], int(s.split('_')[1]) if '_' in s and s.split('_')[1].isdigit() else 0))
open(out,'w').write(",".join(vs)+"\n"+p+"\n"+",\n".join(gens)+"\n")
print(f"{out}: {len(vs)} variables, {len(gens)} equations, char {p}")
