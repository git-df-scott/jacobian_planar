"""Braid monodromy of an affine plane curve given by parametrisations
(a_i(t), b_i(t)) (one per component), projection (u,v) -> u.
Produces a Zariski-van Kampen presentation of pi_1(C^2 - S) plus, for each
singular fibre, the transported meridians of the strands meeting each
singular point, the local branch permutation, and the multiplicity data
needed for the Euler-characteristic bookkeeping.  Output: a GAP file.
"""
import sys, json, itertools
import numpy as np
import sympy as sp

t, u, v = sp.symbols('t u v')

def curve_equation(comps):
    """comps: list of (a(t), b(t)) sympy polys.  Returns F(u,v) = prod Res_t(a-u, v-b), monic in v."""
    F = sp.Integer(1)
    for a, b in comps:
        R = sp.resultant(a - u, v - b, t)
        R = sp.Poly(R, v)
        F = F * R.as_expr() / R.LC()
    return sp.Poly(sp.expand(F), v, u)

def vroots(Fpoly_coeffs, uval):
    # Fpoly_coeffs: list of numpy poly1d in u (coeffs of v^deg..v^0), or sympy exprs
    c = np.array([complex(cf(uval)) if isinstance(cf, np.poly1d) else complex(cf.subs(u, uval)) for cf in Fpoly_coeffs])
    return np.roots(c)

def critical_values(F):
    disc = sp.discriminant(F.as_expr(), v)
    disc = sp.Poly(sp.expand(disc), u)
    sqf = sp.Poly(sp.sqf_part(disc.as_expr()), u)
    cs = [complex(r) for r in sqf.nroots(n=30, maxsteps=500)]
    # cluster
    out = []
    for c in cs:
        for o in out:
            if abs(c - o[0]) < 1e-6:
                o[1] += 1; break
        else:
            out.append([c, 1])
    return out, disc

def match(prev, new):
    """assign new roots to prev by nearest; return permuted new and ok flag"""
    n = len(prev)
    D = np.abs(prev[:, None] - new[None, :])
    # greedy with global check
    order = []
    used = set()
    for i in range(n):
        j = int(np.argmin(np.where([k in used for k in range(n)], np.inf, D[i])))
        order.append(j); used.add(j)
    newp = new[order]
    disp = np.abs(newp - prev).max()
    sep = min(abs(prev[i]-prev[j]) for i in range(n) for j in range(i+1, n))
    return newp, disp < 0.25 * sep

def track(Fc, path, n, init=None):
    """track roots along a list of u-values (refined adaptively). returns (pts, roots)"""
    r0 = vroots(Fc, path[0])
    if init is not None:
        r0, ok = match(init, r0)
        if not ok: raise RuntimeError('cannot seed tracking')
    roots = [r0]
    i = 1
    pts = list(path)
    while i < len(pts):
        new = vroots(Fc, pts[i])
        newp, ok = match(roots[-1], new)
        if ok:
            roots.append(newp); i += 1
        else:
            mid = (pts[i-1] + pts[i]) / 2
            if abs(pts[i] - pts[i-1]) < 1e-13:
                raise RuntimeError('cannot resolve strands near u=%s' % pts[i])
            pts.insert(i, mid)
    return pts, roots

def braid_word(roots):
    """from tracked roots (list of arrays, strand index fixed), produce Artin word.
    Positions ordered by real part; crossing of adjacent positions i,i+1 -> sigma_i^{+-1}.
    sign: +1 if the strand moving right (increasing real part) passes with smaller imaginary part."""
    word = []
    prev_order = list(np.argsort(roots[0].real))
    for k in range(1, len(roots)):
        r = roots[k]
        order = list(np.argsort(r.real))
        if order == prev_order:
            continue
        # find adjacent transpositions turning prev_order into order (bubble)
        cur = list(prev_order)
        changed = True
        steps = 0
        while cur != order:
            steps += 1
            if steps > 50:
                raise RuntimeError('too many crossings in one step')
            for i in range(len(cur) - 1):
                # strands at positions i, i+1 in cur; do they need to swap?
                s1, s2 = cur[i], cur[i+1]
                if order.index(s1) > order.index(s2):
                    # s1 moves right past s2.  imaginary parts at crossing ~ average of both times
                    im1 = (roots[k-1][s1].imag + r[s1].imag) / 2
                    im2 = (roots[k-1][s2].imag + r[s2].imag) / 2
                    sign = 1 if im1 < im2 else -1
                    word.append(sign * (i + 1))
                    cur[i], cur[i+1] = s2, s1
                    break
        prev_order = order
    return word, prev_order

def artin_act(word, gens):
    """apply braid word (list of signed ints) to free-group words; words are lists of signed ints (generator indices 1..n)."""
    n = len(gens)
    cur = [list(g) for g in gens]
    def inv(w): return [-x for x in reversed(w)]
    def subst(w, images):
        out = []
        for x in w:
            if x > 0: out += images[x-1]
            else: out += inv(images[-x-1])
        return out
    for s in word:
        i = abs(s) - 1
        images = [[j+1] for j in range(n)]
        if s > 0:
            images[i] = [i+1, i+2, -(i+1)]
            images[i+1] = [i+1]
        else:
            images[i] = [i+2]
            images[i+1] = [-(i+2), i+1, i+2]
        cur = [subst(w, images) for w in cur]
    return [freereduce(w) for w in cur]

def freereduce(w):
    out = []
    for x in w:
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return out


def conj_decompose(word):
    """word = w g w^-1 (free-reduced) -> (g, w) with g a signed generator; returns (None, None) if not of that form."""
    w = list(word)
    L = len(w)
    if L % 2 == 0: return None, None
    h = L // 2
    pre, g, post = w[:h], w[h], w[h+1:]
    if [-x for x in reversed(pre)] == post:
        return g, pre
    return None, None

def gapword(w, name='g'):
    if not w: return 'One(F)'
    return '*'.join(('%s%d' % (name, x)) if x > 0 else ('%s%d^-1' % (name, -x)) for x in w)

def analyse(comps, name, base=None, radius_frac=0.25, seed=0):
    F = curve_equation(comps)
    n = F.degree(v)
    Fc = [np.poly1d([complex(x) for x in sp.Poly(F.as_expr().coeff(v, k), u).all_coeffs()]) for k in range(n, -1, -1)]
    crit, disc = critical_values(F)
    cvals = [c for c, m in crit]
    rng = np.random.default_rng(seed)
    def path_score(b, rads):
        sc = np.inf
        for k, c in enumerate(cvals):
            for j, o in enumerate(cvals):
                if j == k: continue
                seg = c - b
                tt = np.clip(((o - b) * np.conj(seg)).real / abs(seg)**2, 0, 1)
                sc = min(sc, abs(b + tt * seg - o) / rads[j])
        return sc
    cx = np.array(cvals)
    R = max(abs(cx - cx.mean()).max(), 1.0) if len(cvals) > 1 else 1.0
    rad0 = []
    for c in cvals:
        d = min(abs(c - o) for o in cvals if o != c) if len(cvals) > 1 else 1.0
        rad0.append(min(radius_frac * d, 0.3))
    if base is None:
        best = None
        for trial in range(300):
            cand = complex(cx.mean()) + R * (1.2 + 2.0 * rng.random()) * np.exp(2j * np.pi * rng.random())
            sc = path_score(cand, rad0)
            if best is None or sc > best[0]: best = (sc, cand)
        base = best[1]
    # shrink radii until the paths clear the other discs
    shrink = 1.0
    while path_score(base, [r * shrink for r in rad0]) < 1.5 and shrink > 1e-3:
        shrink *= 0.5
    if shrink <= 1e-3:
        raise RuntimeError('cannot find a base point with clear paths')
    # order critical values by argument from base
    cvals.sort(key=lambda c: np.angle(c - base))
    rad = [r * shrink for r in rad0]
    gens = [[i+1] for i in range(n)]
    base_roots = vroots(Fc, base)
    base_order = list(np.argsort(base_roots.real))
    # generator j corresponds to position j (sorted by real part) at the base fibre
    comp_of_gen = []
    for p in range(n):
        z = base_roots[base_order[p]]
        vals = [abs(complex(sp.resultant(a - u, v - b, t).subs({u: base, v: z}))) for a, b in comps]
        comp_of_gen.append(int(np.argmin(vals)))
    rels = []
    sing = []   # per critical value: list of local clusters
    loops = []
    for k, c in enumerate(cvals):
        r = rad[k]
        for attempt in range(8):
            try:
                direction = (c - base) / abs(c - base)
                near = c - r * direction
                N1 = 60
                path_in = [base + (near - base) * s for s in np.linspace(0, 1, N1)]
                circle = [c - r * direction * np.exp(1j * th) for th in np.linspace(0, 2*np.pi, 90)]
                pts_in, roots_in = track(Fc, path_in, n)
                pts_c, roots_c = track(Fc, circle, n, init=roots_in[-1])
                path_out = list(reversed(pts_in))
                pts_o, ro = track(Fc, path_out, n, init=roots_c[-1])
                full_roots = roots_in + roots_c[1:] + ro[1:]
                W, _ = braid_word(full_roots)
                P, order_near = braid_word(roots_in)
                L, _ = braid_word(roots_c)
                # local permutation on the circle: strand i (index) ends at position of which strand
                start, end = roots_c[0], roots_c[-1]
                perm = {}
                for i in range(n):
                    j = int(np.argmin(np.abs(start - end[i])))  # strand i ends where strand j started
                    perm[i] = j
                # clusters at c: exact roots of F(c,v)
                ex = vroots(Fc, c)
                near_roots = roots_c[0]
                assign = [int(np.argmin(np.abs(ex - z))) for z in near_roots]
                # cluster exact roots with a tolerance adapted to high multiplicity (numpy error ~ eps^(1/mult))
                tol = 2e-2 * (1 + np.abs(ex).max())
                clusters = {}
                for i, j in enumerate(assign):
                    key = None
                    for kk in clusters:
                        if abs(ex[kk] - ex[j]) < tol: key = kk; break
                    if key is None: key = j; clusters[key] = []
                    clusters[key].append(i)
                # sanity: each near root must be unambiguously closer to its own cluster than to any other cluster
                keys = list(clusters.keys())
                for i, z in enumerate(near_roots):
                    own = [kk for kk in keys if i in clusters[kk]][0]
                    dmine = abs(z - ex[own])
                    dother = [abs(z - ex[kk]) for kk in keys if kk != own]
                    if dother and dmine > 0.5 * min(dother):
                        raise RuntimeError('cluster assignment ambiguous at u=%s' % c)
                pos_of = {s_: p for p, s_ in enumerate(order_near)}
                Pinv = [-x for x in reversed(P)]
                images_Pinv = artin_act(Pinv, gens)
                local = []
                fibre = []
                for key, strands in clusters.items():
                    fibre.append(dict(positions=sorted(pos_of[s_] for s_ in strands),
                                      mer=[images_Pinv[pos_of[s_]] for s_ in sorted(strands, key=lambda x: pos_of[x])],
                                      singular=False))
                    if len(strands) < 2: continue
                    vp = ex[key]
                    # parameter values on each component mapping to (c, vp)
                    branches = []
                    for ci, (a, b) in enumerate(comps):
                        ap = sp.Poly(a - c, t)
                        trs = []
                        mult = []
                        for tr in np.roots([complex(x) for x in ap.all_coeffs()]):
                            for q_, x in enumerate(trs):
                                if abs(tr - x) < 1e-2: mult[q_] += 1; break
                            else:
                                trs.append(tr); mult.append(1)
                        aprime_roots = np.roots([complex(x) for x in sp.Poly(sp.diff(a, t), t).all_coeffs()]) if sp.Poly(a, t).degree() > 1 else np.array([])
                        for q_, tr in enumerate(trs):
                            if mult[q_] >= 2 and len(aprime_roots):
                                tr = aprime_roots[int(np.argmin(np.abs(aprime_roots - tr)))]
                            if abs(complex(b.subs(t, tr)) - vp) < 1e-3 * (1 + abs(vp)):
                                gcdab = sp.gcd(sp.Poly(sp.diff(a, t), t), sp.Poly(sp.diff(b, t), t))
                                cusp_params = np.roots([complex(x) for x in gcdab.all_coeffs()]) if gcdab.degree() >= 1 else np.array([])
                                singular_branch = mult[q_] >= 2 and len(cusp_params) > 0 and np.min(np.abs(cusp_params - tr)) < 1e-2
                                branches.append(dict(comp=ci, t=[float(tr.real), float(tr.imag)], cusp=bool(singular_branch)))
                    if len(branches) != len(clusters[key]) and len(branches) < 2:
                        pass
                    r_p = len(branches)
                    is_sing = r_p >= 2 or any(br['cusp'] for br in branches)
                    if not is_sing:
                        continue   # smooth point with vertical tangent
                    fibre[-1]['singular'] = True
                    local.append(dict(strands=strands, positions=[pos_of[s_] for s_ in strands],
                                      branches=r_p, branch_comps=[br['comp'] for br in branches],
                                      cusps=sum(br['cusp'] for br in branches),
                                      merB=[images_Pinv[pos_of[s_]] for s_ in strands],
                                      point=[float(vp.real), float(vp.imag)]))

                break
            except RuntimeError as ex_:
                if 'ambiguous' in str(ex_) and attempt < 7:
                    r = r / 2
                    continue
                raise
        loops.append(dict(c=[c.real, c.imag], W=W, P=P, L=L, local=local, fibre=fibre))
        imgs = artin_act(W, gens)
        longit = []
        for j in range(n):
            rels.append(freereduce([-(j+1)] + imgs[j]))
            g_, w_ = conj_decompose(imgs[j])
            longit.append(dict(to=(abs(g_) if g_ else None), sign=(1 if (g_ or 1) > 0 else -1), w=w_))
        loops[-1]['longit'] = longit
    degs = [[max(sp.Poly(a, t).degree(), 0), max(sp.Poly(b, t).degree(), 0)] for a, b in comps]
    return dict(name=name, n=n, F=str(F.as_expr()), crit=[[c.real, c.imag] for c in cvals],
                loops=loops, rels=rels, comp_of_gen=comp_of_gen, degs=degs, m=len(comps))

def to_gap(res, path):
    n = res['n']
    lines = []
    lines.append('F := FreeGroup(%d);;' % n)
    for i in range(n):
        lines.append('g%d := F.%d;;' % (i+1, i+1))
    lines.append('rels := [ %s ];;' % ', '.join(gapword(r) for r in res['rels'] if r))
    lines.append('G := F / rels;;')
    lines.append('gg := GeneratorsOfGroup(G);;')
    lines.append('tofp := function(w) return MappedWord(w, GeneratorsOfGroup(F), gg); end;;')
    sp_list = []
    for lp in res['loops']:
        for loc in lp['local']:
            merB = ', '.join('tofp(%s)' % gapword(w) for w in loc['merB'])
            sp_list.append('rec(branches := %d, nstr := %d, cusps := %d, comps := %s, mer := [%s])'
                           % (loc['branches'], len(loc['strands']), loc['cusps'], [c+1 for c in loc['branch_comps']], merB))
    lines.append('singpts := [ %s ];;' % ', '.join(sp_list))
    fl = []
    for lp in res['loops']:
        cl = []
        for f in lp['fibre']:
            cl.append('rec(positions := %s, singular := %s, mer := [%s])' % (list(f['positions']), 'true' if f['singular'] else 'false', ', '.join('tofp(%s)' % gapword(w) for w in f['mer'])))
        fl.append('[ %s ]' % ', '.join(cl))
    lines.append('fibres := [ %s ];;' % ', '.join(fl))
    ll = []
    for lp in res['loops']:
        ll.append('[ %s ]' % ', '.join(('rec(to := %d, w := tofp(%s))' % (d['to'], gapword(d['w']))) if d['to'] else 'fail' for d in lp['longit']))
    lines.append('longitudes := [ %s ];;' % ', '.join(ll))
    lines.append('compofgen := %s;;' % [c+1 for c in res['comp_of_gen']])
    lines.append('degs := %s;;' % res['degs'])
    lines.append('m := %d;;' % res['m'])
    open(path, 'w').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    pass
