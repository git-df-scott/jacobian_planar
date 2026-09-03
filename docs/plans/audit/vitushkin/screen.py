"""Abstract pre-screen: irreducible S with involution meridians (e/2 transpositions, n = D - e fixed points),
c cusps of types (2,k_i), nu ordinary nodes.  Enumerate local orbit decompositions and test
Euler = 1 and chi(R) >= 1.  Prints feasible singularity multisets."""
import itertools, sys
def cusp_decomps(D, e, k):
    # orbits of D_k on D points: sizes 1,2,k,2k with transposition counts 0,1,(k-1)/2,k for a reflection
    out = set()
    tk = (k - 1) // 2
    for n2k in range(0, D // (2*k) + 1):
        for nk in range(0, D // k + 1):
            for n2 in range(0, D // 2 + 1):
                pts = 2*k*n2k + k*nk + 2*n2
                tr = k*n2k + tk*nk + n2
                if pts <= D and tr == e // 2:
                    s = D - pts
                    o = n2k + nk + n2
                    out.add((s, o))
    return out
def node_decomps(D, e):
    # Klein group orbits: size 4 regular (a,b each 2 transp... a=(12)(34): 2 transp for a, 2 for b),
    # size 2 with a=b transposition, size 2 with a swaps and b fixes (b fixes both: contributes to b's fixed pts),
    # size 2 with b swaps a fixes.  Both a and b need e/2 transpositions in total.
    out = set()
    for n4 in range(0, D // 4 + 1):
        for nab in range(0, D // 2 + 1):
            for na in range(0, D // 2 + 1):
                for nb in range(0, D // 2 + 1):
                    pts = 4*n4 + 2*(nab + na + nb)
                    if pts > D: continue
                    ta = 2*n4 + nab + na
                    tb = 2*n4 + nab + nb
                    if ta == e // 2 and tb == e // 2:
                        out.add((D - pts, n4 + nab + na + nb))
    return out
res = []
for D in range(4, 13):
    for e in range(2, D, 2):
        n = D - e
        for c in range(1, 5):
            for types in itertools.combinations_with_replacement([3, 5, 7, 9], c):
                for nu in range(0, 5):
                    k = c + 2*nu
                    if nu == 0: continue   # Zaidenberg-Lin / Nguyen: S must have a node
                    need = 1 - D*nu - n*(1 - k)   # required sum of s_p
                    if need < 0: continue
                    # cycles of meridian on moved points = e/2
                    base_chiR = (e // 2) * (1 - k)
                    cd = [cusp_decomps(D, e, kk) for kk in types]
                    nd = node_decomps(D, e)
                    if not all(cd) or not nd: continue
                    for choice in itertools.product(*cd, *([nd] * nu)):
                        s = sum(x[0] for x in choice); o = sum(x[1] for x in choice)
                        if s == need and base_chiR + o >= 1:
                            res.append((D, e, n, types, nu, s, base_chiR + o, choice))
print(len(res), 'feasible abstract configurations')
seen = set()
for r in res:
    key = r[:5]
    if key in seen: continue
    seen.add(key)
    print('D=%d e=%d n=%d cusps=%s nodes=%d  sum_s=%d chiR=%d  example=%s' % r)
