import sys, itertools
from fractions import Fraction
sys.path.insert(0, "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks")
import trackD_chain_map as CM
from trackD_chain_map import all_chains, reduced_candidates, check_eps

chs = all_chains()
print("chains:", len(chs))
rows=[]
for ch in chs:
    a0,_,b0 = ch.A0; at,_,bt = ch.At; a = ch.terminal[1]; b = ch.terminal[2]+1
    ap = ch.lower[0] if ch.lower else 1
    ct = Fraction(a+bt, at)
    if ct.denominator!=1 or int(ct)-2 < 1 or at==ap or b<=1:
        rows.append((ch.name,'OUT',None,None,None,None)); continue
    q = Fraction(bt, at-ap); s=q-1; c_pre = Fraction(b0)-s*a0
    clamped = (c_pre.denominator==1 and c_pre>=0 and int(c_pre)>=b)
    rows.append((ch.name,'IN',c_pre,b,clamped, (ch.At, ch.terminal, ch.lower, tuple(sorted((ch.m,ch.n))))))
nin=[r for r in rows if r[1]=='IN']
print("in-scope:", len(nin), " A0-clamped (c_pre>=b, so A0 drops out):",
      sum(1 for r in nin if r[4]), " A0-LIVE:", [ (r[0],str(r[2]),r[3]) for r in nin if not r[4]])
print()
# empirical: same tail  =>  same (NP,NQ,r) candidate set?
def key(ch): return (ch.At, ch.terminal, ch.lower, tuple(sorted((ch.m,ch.n))))
def sig(ch):
    cands,_ = reduced_candidates(ch)
    kept=[c for c in cands if check_eps(c)[0]]
    return tuple(sorted((c['r'],c['cprime'],c['mp'],c['np'],tuple(sorted(c['NP'])),tuple(sorted(c['NQ']))) for c in kept))
groups={}
for ch in chs: groups.setdefault(key(ch),[]).append(ch)
print("distinct tail keys (A_t, terminal, A'_t, sorted(m,n)):", len(groups))
viol=0
for k,v in groups.items():
    if len(v)<2: continue
    sigs={ch.name: sig(ch) for ch in v}
    same = len(set(sigs.values()))==1
    print(f"  tail {k[0]}->{k[1]} mn={k[3]} : {len(v)} chains  identical-systems={same}")
    for ch in v: print(f"      {ch.name}  A0={ch.A0}")
    if not same: viol+=1
print("tail-key violations:", viol)
# strict 'last two corners' key
def key2(ch): return (tuple(ch.corners[-2:]), ch.lower, tuple(sorted((ch.m,ch.n))))
g2={}
for ch in chs: g2.setdefault(key2(ch),[]).append(ch)
v2=0
for k,v in g2.items():
    if len(v)<2: continue
    if len(set(sig(ch) for ch in v))!=1:
        v2+=1; print("  LAST-2-CORNERS VIOLATION:", [ch.name for ch in v])
print("distinct last-2-corner keys:", len(g2), " violations:", v2)
# chains where A_t is NOT among the last two corners
print("chains whose A_t is outside the last two corners:",
      [ch.name for ch in chs if ch.At not in ch.corners[-2:]])
