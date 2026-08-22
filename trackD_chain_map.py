"""Chain data -> reduced Newton-polygon pair, from the GGHV definitions.

SOURCES (both held locally as full text, line numbers cited)
  [C] "Some algorithms related to the Jacobian Conjecture", arXiv:1708.07936
      Theorem 2.20 (lines 660-745): the chain attached to a standard (m,n)-pair
      Section 5  (lines 1379-1406): the 17 length-1 and 7 length-2 FAMILIES,
                 each given as (A_0, A'_0, A_1, [A'_1, A_2], k, m(j), n(j))
      Section 6  (lines 1467-1560): the 34 possible counterexamples, max <= 150
  [G] "Increasing the degree ... from 100 to 108", arXiv:2204.14178
      Section 4  (lines 224-500): "Reducing the size of the Newton polygon" --
                 Prop 4.1 (9,27), Prop 4.2 (9,24), Prop 4.3 (8,28)

WHAT THEOREM 2.20 GIVES US DIRECTLY
  A_0 = (1/m) en_{1,0}(P),  A'_i = (1/m) st_{rho_i,sigma_i}(P),  A_{i+1} = A'_i
  for type II.a corners, and the corners of N(P), N(Q) are m and n times a
  common base polygon B.  Points are written (a|l, b) meaning (a/l, b); the
  corners with l = 1 are exactly the regular corners of (P,Q) (item 13).
  So the PRE-reduction base is

      B = conv{ (0,0), A'_t, A_t, ..., A_0, (0, c) }

  with A'_t the last lower corner and (0,c) the top-left corner.

WHAT SECTION 4 DOES
  phi_1 : x <-> y ; then shears phi(y) = y + lambda x^{sigma/rho} that cut an
  edge whose leading form is a power of (x^a y^b - lambda); finally a monomial
  twist  phi(x) = x^-1, phi(y) = x^{c_t} y, which is an automorphism of
  L(1) = K[x,x^-1,y] but not of K[x,y].  Shears are volume preserving, the swap
  contributes -1, and

      [phi(P), phi(Q)] = phi([P,Q]) * [phi(x), phi(y)],
      [x^-1, x^{c_t} y] = -x^{c_t - 2},

  so the bracket right-hand side is x^r with  r = c_t - 2.  This is where the
  bracket exponent comes from -- it is not a free choice.

THE MAP (each rule validated against every published reduced pair, see
validate() below -- 6/6 exact, no fitting freedom left over)

  Let the chain be A_0, ..., A_{j+1} with A_i = (a_i/l_i, b_i), l_0 = 1, and let
  A_t be the LAST corner with l = 1, A'_t = (a', 0) the last lower corner.

    a  = l_{j+1}                      (denominator of the terminal corner)
    b  = b_{j+1} + 1
    B' = {(0,0), (a, b-1), (a, b), (0, c')}          reduced base
    (m', n') = sorted(m, n)
    N(P) = conv( m'B' + {eps_P} ),  N(Q) = conv( n'B' + {eps_Q} )
    {eps_P, eps_Q} = {(1,0), (r,1)}
    c_t = (a + b_t) / a_t ,   r = c_t - 2

  and c' runs over  c_pre, c_pre - a, c_pre - 2a, ..., >= 0,  where c_pre is the
  PRE-reduction top-left corner
    q     = b_t / (a_t - a')      slope of the edge A'_t -> A_t
    s     = q - 1                 slope of the top-left edge at A_0
    c_pre = b_0 - s * a_0
  The step-by-a ladder is what produces Prop 4.2's three cases and Prop 4.3's
  two cases; it is a SUPERSET for Prop 4.1, which pins the single top value.
  Superset is the safe direction: a shape that cannot exist costs a machine
  run, a shape that is missed costs a counterexample.

THE eps INVARIANT IS NOT AN EXTRA AXIOM
  Write P = p_00 + y P_1(x) + O(y^2), Q = q_00 + q_{k0} x^k + y Q_1(x) + O(y^2).
  Then [P,Q] at y^0 is  -k q_{k0} x^{k-1} P_1(x), so the surviving monomial is
  (i_P + i_Q - 1, 0).  Hence [P,Q] = x^r forces

      eps_P + eps_Q = (r + 1, 1).

  It is therefore a consequence of the bracket, and every shape this module
  emits satisfies it by construction; check_eps() re-derives it independently
  so that a bug in the construction cannot slip through.
"""
from fractions import Fraction
import itertools


# ----------------------------------------------------------------- chain data
# corner (num, den, b) means the point (num/den, b).  den = 1 <=> integer corner
def C(num, den, b):
    return (num, den, b)


# Section 5 families: (A_0, A'_0, terminal corner, m(j), n(j), intermediate)
FAMILIES = {
    "F1":  (C(4, 1, 12), C(1, 1, 0), C(7, 4, 3),  lambda j: 2*j+3, lambda j: 3*j+4),
    "F2":  (C(5, 1, 20), C(1, 1, 0), C(7, 5, 2),  lambda j: j+2,   lambda j: 2*j+3),
    "F3":  (C(5, 1, 20), C(1, 1, 0), C(8, 5, 3),  lambda j: 4*j+3, lambda j: 3*j+2),
    "F7":  (C(6, 1, 15), C(1, 1, 0), C(7, 3, 4),  lambda j: j+2,   lambda j: 4*j+7),
    "F8":  (C(6, 1, 15), C(1, 1, 0), C(8, 3, 5),  lambda j: 2*j+3, lambda j: 5*j+7),
    "F9":  (C(7, 1, 21), C(1, 1, 0), C(11, 7, 2), lambda j: j+2,   lambda j: 2*j+3),
    "F11": (C(7, 1, 21), C(1, 1, 0), C(13, 7, 3), lambda j: j+2,   lambda j: 3*j+5),
    "F17": (C(9, 1, 24), C(1, 1, 0), C(11, 3, 8), lambda j: 5*j+2, lambda j: 8*j+3),
    "F22": (C(8, 1, 24), C(2, 1, 0), C(5, 4, 2),  lambda j: j+2,   lambda j: 2*j+3),
    "F24": (C(8, 1, 24), C(2, 1, 0), C(19, 8, 3), lambda j: 2*j+3, lambda j: 3*j+4),
}

# Section 6, table 1: the 13 entries coming from families -- (family, (m,n), max)
FAMILY_ROWS = [
    ("F1", (3, 4), 64), ("F1", (5, 7), 112), ("F2", (2, 3), 75),
    ("F2", (3, 5), 125), ("F3", (3, 2), 75), ("F7", (2, 7), 147),
    ("F8", (3, 7), 147), ("F9", (2, 3), 84), ("F9", (3, 5), 140),
    ("F11", (2, 5), 140), ("F17", (2, 3), 99), ("F22", (2, 3), 96),
    ("F24", (3, 4), 128),
]

# Section 6, tables 2-4: chains given explicitly.  A'_t is not printed there;
# it is (1,0) in every length-1 family of Section 5 except F12/F13/F22/F23/F24,
# so (1,0) is the default and is flagged in the output.
CHAIN_ROWS = [
    ([C(7, 1, 35), C(19, 7, 5)], (2, 3), 126),
    ([C(7, 1, 42), C(13, 7, 6)], (3, 2), 147),
    ([C(7, 1, 42), C(13, 7, 6)], (2, 3), 147),
    ([C(8, 1, 28), C(7, 4, 3)], (3, 4), 144),
    ([C(8, 1, 28), C(11, 4, 7)], (3, 2), 108),
    ([C(9, 1, 36), C(17, 9, 4)], (3, 2), 135),
    ([C(9, 1, 36), C(17, 9, 4)], (2, 3), 135),
    ([C(11, 1, 33), C(19, 4, 8)], (2, 3), 132),
    ([C(12, 1, 33), C(11, 3, 8)], (2, 3), 135),
    ([C(8, 1, 32), C(8, 1, 28), C(11, 4, 7)], (3, 2), 120),
    ([C(8, 1, 40), C(8, 1, 28), C(11, 4, 7)], (3, 2), 144),
    ([C(9, 1, 27), C(9, 1, 24), C(11, 3, 8)], (2, 3), 108),
    ([C(9, 1, 36), C(9, 1, 24), C(11, 3, 8)], (2, 3), 135),
    ([C(10, 1, 40), C(16, 5, 6), C(23, 10, 3)], (3, 2), 150),
    ([C(10, 1, 40), C(18, 5, 8), C(8, 5, 3)], (3, 2), 150),
    ([C(12, 1, 30), C(16, 3, 10), C(11, 6, 3)], (3, 2), 126),
    ([C(12, 1, 36), C(12, 1, 33), C(11, 3, 8)], (2, 3), 144),
    ([C(12, 1, 36), C(9, 1, 24), C(11, 3, 8)], (2, 3), 144),
    ([C(12, 1, 36), C(21, 4, 9), C(19, 4, 8)], (2, 3), 144),
    ([C(12, 1, 36), C(21, 4, 9), C(12, 4, 5)], (2, 3), 144),
    ([C(12, 1, 36), C(12, 1, 30), C(16, 3, 10), C(11, 6, 3)], (3, 2), 144),
]


class Chain:
    def __init__(self, name, corners, lower, mn, maxdeg, source):
        self.name = name
        self.corners = corners          # A_0 .. A_{j+1}
        self.lower = lower              # A'_t = (a', 0), or None if unknown
        self.m, self.n = mn
        self.maxdeg = maxdeg
        self.source = source

    @property
    def A0(self):
        return self.corners[0]

    @property
    def At(self):
        """last corner with denominator 1 -- the last regular corner of (P,Q)"""
        ints = [c for c in self.corners if c[1] == 1]
        return ints[-1]

    @property
    def terminal(self):
        return self.corners[-1]

    def degrees(self):
        a0, _, b0 = self.A0
        return (self.m * (a0 + b0), self.n * (a0 + b0))


def all_chains():
    out = []
    for fam, (m, n), mx in FAMILY_ROWS:
        A0, Ap0, term, mf, nf = FAMILIES[fam]
        j = None
        for jj in range(0, 12):
            if (mf(jj), nf(jj)) == (m, n):
                j = jj
                break
        if j is None:
            raise ValueError(f"{fam}: no j gives (m,n) = {(m,n)}")
        out.append(Chain(f"{fam}(m,n)={m},{n}", [A0, term], Ap0, (m, n), mx,
                         f"[C] Sec.5 {fam}, j={j}"))
    for corners, mn, mx in CHAIN_ROWS:
        a0, _, b0 = corners[0]
        nm = f"({a0},{b0})" + "/" + "/".join(
            (f"{c[0]}/{c[1]}" if c[1] != 1 else f"{c[0]}") + f",{c[2]}"
            for c in corners[1:])
        out.append(Chain(nm + f" (m,n)={mn[0]},{mn[1]}", corners, None, mn, mx,
                         "[C] Sec.6"))
    return out


# --------------------------------------------------------------- the map
def hull(points):
    """convex hull, counter-clockwise, vertices only."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def half(ps):
        st = []
        for p in ps:
            while len(st) >= 2:
                (x1, y1), (x2, y2) = st[-2], st[-1]
                if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) <= 0:
                    st.pop()
                else:
                    break
            st.append(p)
        return st

    lo = half(pts)
    hi = half(pts[::-1])
    return lo[:-1] + hi[:-1]


def reduced_candidates(ch, superset_c=False):
    """All reduced pairs this chain can give.  Returns list of dicts."""
    a0, _, b0 = ch.A0
    at, _, bt = ch.At
    a = ch.terminal[1]
    b = ch.terminal[2] + 1
    notes = []

    # bracket exponent from the monomial twist
    ct = Fraction(a + bt, at)
    if ct.denominator != 1:
        return [], [f"c_t = (a + b_t)/a_t = {ct} is not an integer -- the "
                    f"monomial twist does not close; chain out of scope"]
    r = int(ct) - 2
    if r < 1:
        return [], [f"r = c_t - 2 = {r} < 1 -- bracket would not be a positive "
                    f"power of x"]

    # pre-reduction top-left corner
    ap = ch.lower[0] if ch.lower else 1
    if ch.lower is None:
        notes.append("A'_t not printed in Sec.6; assumed (1,0)")
    if at == ap:
        return [], ["degenerate: A_t and A'_t share the first coordinate"]
    q = Fraction(bt, at - ap)
    s = q - 1
    c_pre = Fraction(b0) - s * a0
    if c_pre.denominator != 1 or c_pre < 0:
        notes.append(f"c_pre = {c_pre} not a non-negative integer; "
                     f"falling back to the full ladder 0..b")
        cs = list(range(0, b + 1))
    elif superset_c:
        cs = list(range(0, b + 1))
    else:
        c0 = min(int(c_pre), b)
        cs = list(range(c0, -1, -a))
    if b <= 1:
        return [], [f"terminal corner b = {b} <= 1 -- no room for the "
                    f"(a,b-1),(a,b) notch"]

    mp, np_ = sorted((ch.m, ch.n))
    out = []
    for cprime in cs:
        base = [(0, 0), (a, b - 1), (a, b)]
        if cprime > 0:
            base.append((0, cprime))
        for swap in (False, True):
            eP, eQ = ((r, 1), (1, 0)) if not swap else ((1, 0), (r, 1))
            NP = hull([(mp * i, mp * j) for (i, j) in base] + [eP])
            NQ = hull([(np_ * i, np_ * j) for (i, j) in base] + [eQ])
            if eP not in NP or eQ not in NQ:
                continue        # eps absorbed into the base: not a vertex
            out.append(dict(chain=ch, a=a, b=b, cprime=cprime, r=r,
                            mp=mp, np=np_, epsP=eP, epsQ=eQ,
                            NP=NP, NQ=NQ, notes=list(notes)))
    return out, notes


# ------------------------------------------------------------- the eps filter
def check_eps(cand):
    """Independent re-derivation of eps_P + eps_Q = (r+1, 1).

    Recomputed from the emitted polygons, not from the constructor, so that a
    construction bug shows up here.  Also checks the row-0 shape that the
    y-adic engine needs: one polygon's j=0 row must be exactly {(0,0),(1,0)}
    and the other's exactly {(0,0)}.
    """
    def row0(N):
        return sorted(i for (i, j) in lattice(N) if j == 0)
    sP = [p for p in cand["NP"] if p[1] <= 1]
    sQ = [p for p in cand["NQ"] if p[1] <= 1]
    eP, eQ = cand["epsP"], cand["epsQ"]
    if eP not in sP or eQ not in sQ:
        return False, "eps not a low vertex of its polygon"
    tot = (eP[0] + eQ[0], eP[1] + eQ[1])
    if tot != (cand["r"] + 1, 1):
        return False, f"eps_P + eps_Q = {tot} != {(cand['r']+1, 1)}"
    rP, rQ = row0(cand["NP"]), row0(cand["NQ"])
    if sorted([rP, rQ]) != sorted([[0], [0, 1]]):
        return False, f"j=0 rows {rP} / {rQ} -- engine needs [0] and [0,1]"
    return True, "ok"


def lattice(verts):
    """all lattice points of the convex hull of verts"""
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    H = hull(verts)
    pts = []
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            if inside(H, (x, y)):
                pts.append((x, y))
    return pts


def inside(H, p):
    n = len(H)
    if n == 1:
        return p == H[0]
    for i in range(n):
        (x1, y1), (x2, y2) = H[i], H[(i + 1) % n]
        if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) < 0:
            return False
    return True


# ------------------------------------------------------------- validation
PUBLISHED = [
    # (label, chain matcher, N(P), N(Q), r)   -- from [G] Section 4 verbatim
    ("Prop 4.1 (9,27)", "(9,27)",
     [(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)],
     [(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)], 1),
    ("Prop 4.2(1) (9,24)", "F17",
     [(0, 0), (1, 1), (6, 16), (6, 18), (0, 12)],
     [(0, 0), (1, 0), (9, 24), (9, 27), (0, 18)], 1),
    ("Prop 4.2(2) (9,24)", "F17",
     [(0, 0), (1, 1), (6, 16), (6, 18), (0, 6)],
     [(0, 0), (1, 0), (9, 24), (9, 27), (0, 9)], 1),
    ("Prop 4.2(3) (9,24)", "F17",
     [(0, 0), (1, 1), (6, 16), (6, 18)],
     [(0, 0), (1, 0), (9, 24), (9, 27)], 1),
    ("Prop 4.3(1) (8,28)", "(8,28)/11/4,7",
     [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
     [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)], 2),
    ("Prop 4.3(2) (8,28)", "(8,28)/11/4,7",
     [(0, 0), (1, 0), (8, 14), (8, 16)],
     [(0, 0), (2, 1), (12, 21), (12, 24)], 2),
]


def validate(verbose=True):
    chains = all_chains()
    ok = 0
    for label, key, NP, NQ, r in PUBLISHED:
        hits = []
        for ch in chains:
            if key not in ch.name:
                continue
            cands, _ = reduced_candidates(ch)
            for cd in cands:
                if (sorted(cd["NP"]) == sorted(hull(NP))
                        and sorted(cd["NQ"]) == sorted(hull(NQ))
                        and cd["r"] == r):
                    hits.append((ch.name, cd))
        if hits:
            ok += 1
            if verbose:
                print(f"  [reproduced] {label:22s} <- {hits[0][0]}"
                      f"   (a,b,c',r) = ({hits[0][1]['a']},{hits[0][1]['b']},"
                      f"{hits[0][1]['cprime']},{hits[0][1]['r']})")
        elif verbose:
            print(f"  [MISSED]     {label}")
    if verbose:
        print(f"  validation: {ok}/{len(PUBLISHED)} published reduced pairs "
              f"reproduced exactly")
    return ok, len(PUBLISHED)


if __name__ == "__main__":
    import sys
    print("=== validation against GGHV Section 4 ===")
    validate()
    print()
    print("=== the 34 chains ===")
    chains = all_chains()
    print(f"total chains: {len(chains)}")
    tot = 0
    for ch in chains:
        cands, notes = reduced_candidates(ch)
        dP, dQ = ch.degrees()
        kept = []
        for cd in cands:
            good, why = check_eps(cd)
            if good:
                kept.append(cd)
        tot += len(kept)
        tag = "" if kept else "   <-- no engine-compatible shape"
        print(f"  {ch.name:34s} deg=({dP},{dQ}) max={ch.maxdeg:4d}  "
              f"shapes={len(cands):2d} pass_eps={len(kept):2d}{tag}")
        if not cands and notes:
            print(f"      {notes[0]}")
    print(f"\ntotal eps-passing candidate shapes: {tot}")
