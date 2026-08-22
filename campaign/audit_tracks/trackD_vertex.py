"""Vertex non-degeneracy probe: is the non-driver's vertex coefficient forced
to zero as a FUNCTION of the driver's parameters?

The sweep imposes only support conditions.  Case (2) of Prop 4.3 showed a shape
can pass all of them and still be degenerate: every solution had B = 0, so
a_8 = d_0 = d_12 = 0 and the Newton polygons collapsed.  A shape is worthless
if the coefficients sitting at N(Q)'s required VERTICES cannot be nonzero.

The y-adic recursion makes Q a rational function of the driver's coefficients
(denominators are powers of p_10).  So each vertex coefficient of Q is a fixed
rational function; if it is IDENTICALLY zero, no choice of driver can rescue
the shape and it dies outright -- no Groebner basis needed.

Identical vanishing is decided by evaluation: the numerators have degree at
most ~jmax in the parameters, so a nonzero one survives a random point with
probability >= 1 - jmax/p, and p = 65521.  Twelve independent random points
put the false-"identically zero" probability below (30/65521)^12.

This is a NECESSARY test only.  Passing it does not mean the shape is alive:
case (2)'s d_12 is not identically zero on the whole parameter space, only on
the solution variety.  Deciding that needs the elimination.  What this probe
buys is a cheap outright kill for the shapes where the collapse is structural.
"""
import random, sys, json
import trackB1_shapes as SH
from trackB1_polygon import hull_rows, trim, pmul, padd, pscal, pderiv, p


def qrows(NP, NQ, r, vec_rng, jextra=2):
    """Run the y-adic recursion at a random driver and return Q's rows."""
    pair = SH.Pair("probe", NP, NQ, [(r, 0, 1)])
    o = pair.orient()
    if o is None:
        return None, None, None
    DR, OR_, rhs, flipped = o
    idx = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
    jmax = max(max(OR_), max(DR)) + jextra
    R = SH.rhs_rows(rhs, jmax)

    vec = [vec_rng.randrange(p) for _ in idx]
    vec[idx.index((0, 1))] = vec_rng.randrange(1, p)
    D = {}
    for ((j, i), val) in zip(idx, vec):
        A = D.setdefault(j, [])
        while len(A) <= i:
            A.append(0)
        A[i] = val % p
    D = {j: trim(a) for j, a in D.items()}

    p10 = D[0][1] if len(D[0]) > 1 else 0
    if p10 == 0:
        return None, None, None
    inv = pow(p10, p - 2, p)
    Q = {0: [0], 1: pscal(R.get(0, []), inv)}
    for k in range(1, jmax + 1):
        acc = list(R.get(k, []))
        for a in range(0, k + 1):
            b = k - a
            if (a + 1) in D and b in Q:
                acc = padd(acc, pscal(pmul(D[a + 1], pderiv(Q[b])), a + 1))
            if a >= 1 and a in D and (b + 1) in Q:
                acc = padd(acc, pscal(pmul(pderiv(D[a]), Q[b + 1]),
                                      -(b + 1) % p))
        Q[k + 1] = pscal(acc, inv * pow(k + 1, p - 2, p) % p)
    return Q, OR_, flipped


def probe(NP, NQ, r, trials=12, seed=5):
    """Return dict: which required vertices of the NON-DRIVER are forced 0."""
    rng = random.Random(seed)
    # the non-driver polygon, in the engine's orientation
    pair = SH.Pair("probe", NP, NQ, [(r, 0, 1)])
    o = pair.orient()
    if o is None:
        return {"status": "OUT OF SCOPE"}
    _, OR_, _, flipped = o
    other_verts = NQ if not flipped else NP
    checks = {}
    for _ in range(trials):
        Q, OR2, _ = qrows(NP, NQ, r, rng)
        if Q is None:
            continue
        for (vi, vj) in other_verts:
            if vj == 0:
                continue          # row 0 of the non-driver is {(0,0)} by design
            row = Q.get(vj, [])
            val = row[vi] if vi < len(row) else 0
            checks.setdefault((vi, vj), []).append(val)
    forced = [v for v, vals in checks.items() if vals and all(x == 0 for x in vals)]
    alive = [v for v, vals in checks.items() if any(x != 0 for x in vals)]
    return {"status": "OK", "forced_zero": forced, "can_be_nonzero": alive,
            "trials": trials, "flipped": flipped}


KNOWN = [
    ("(8,28) case (2) [CLOSED this session]",
     [(0, 0), (1, 0), (8, 14), (8, 16)],
     [(0, 0), (2, 1), (12, 21), (12, 24)], 2),
    ("(8,28) case (1) [OPEN]",
     [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
     [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)], 2),
    ("(9,27) [CLOSED by GGHV]",
     [(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)],
     [(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)], 1),
]

if __name__ == "__main__":
    print("=== calibration on shapes with known status ===")
    for nm, A, B, r in KNOWN:
        res = probe(A, B, r)
        print(f"  {nm}")
        print(f"     forced-zero vertices: {res.get('forced_zero')}")
        print(f"     can be nonzero:       {res.get('can_be_nonzero')}")

    print("\n=== all sweep shapes ===")
    import trackD_chain_map as CM
    from trackD_pipeline import build_all
    shapes = build_all()
    shapes.sort(key=lambda c: c["size"])
    dead, live, oos = [], [], []
    for cd in shapes:
        res = probe(cd["NP"], cd["NQ"], cd["r"])
        tag = (f"{cd['chain'].name} | a={cd['a']} b={cd['b']} c'={cd['cprime']} "
               f"r={cd['r']} eps=({cd['epsP']},{cd['epsQ']})")
        if res["status"] != "OK":
            oos.append(tag)
        elif res["forced_zero"]:
            dead.append((tag, res["forced_zero"]))
        else:
            live.append(tag)
    print(f"  shapes probed: {len(shapes)}")
    print(f"  structurally DEAD (a required vertex is identically zero): "
          f"{len(dead)}")
    print(f"  pass the probe: {len(live)}")
    print(f"  out of scope: {len(oos)}")
    for tag, fz in dead[:40]:
        print(f"    DEAD {fz}  {tag[:88]}")
    json.dump({"dead": [[t, [list(v) for v in f]] for t, f in dead],
               "live": live, "oos": oos},
              open("trackD_vertex.json", "w"), indent=1)
    print("[wrote trackD_vertex.json]")
