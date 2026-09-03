import sys, re
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().split('\n'); names = lines[0].split(','); p = int(lines[1])
body = '\n'.join(lines[2:]); gens = [g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
s = f"ring R = {p}, ({','.join(names)}), dp;\noption(redSB);\nideal I = " + ',\n'.join(gens) + ";\n"
s += 'int t0 = timer;\nideal G = std(I);\n"STD time " + string(timer-t0) + " size " + string(size(G));\n'
s += 'if (size(G)==1 && G[1]==1) { "VERDICT: EMPTY (1 in ideal)"; } else { "VERDICT: NONUNIT dim " + string(dim(G)); if (dim(G)==0) { "vdim " + string(vdim(G)); } }\nquit;\n'
open(dst, 'w').write(s)
