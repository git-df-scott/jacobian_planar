"""night19 -- THE MECHANISM, and deliberately broken cases.

The general row formula.  For P = sum_{(a,b) in A} p_ab x^a y^b,

    [P, x^i y^j] = sum_{(a,b) in A} p_ab * (a*j - b*i) * x^{a+i-1} y^{b+j-1} .

So the column of the mate matrix M indexed by the monomial x^i y^j meets at most
|A| rows: the translates of (i,j) by the SHIFT VECTORS s_ab = (a-1, b-1), with
coefficient p_ab*(a j - b i) -- which vanishes exactly on the ray a j = b i.

|A| = 2  =>  every column meets at most TWO rows, so columns are EDGES of a
graph whose vertices are rows, and all edges are the SAME translation
delta = (a2-a1, b2-b1): the graph is a disjoint union of paths, i.e. a FOREST.
Potentials on a forest are integrable, so a certificate exists unless the
"forced zeros" (columns that meet only ONE row force that row's lambda to 0)
propagate to the row (0,0), where lambda must be 1.

This module measures, for a list of P:
  - the support A, the shift vectors, the RANK of the lattice of shift
    differences, and the maximum number of rows a column meets;
  - the cycle rank (first Betti number) of the bipartite incidence graph of M
    on the carrier, and, for |A| = 2, whether the row graph is a forest and
    whether the forced-zero propagation reaches (0,0);
  - unimodularity (Groebner: (P_x,P_y) = (1)) with an explicit Bezout identity
    of zero residual, and non-coordinacy (Shpilrain-Yu, night14/sy14.py) with a
    fibre witness;
  - the EXACT verdict of the mate system at a range of carriers, with a lambda
    certificate re-verified by expansion, and whether that lambda is DIAGONAL
    (the closed-form shape).

HIT GATE: if any mate system is CONSISTENT, the run stops and writes HIT_<hash>/.
"""
import hashlib, json, os, sys, time
from fractions import Fraction as F
import sympy as sp
import mate19 as m

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'night14'))
import sy14, poly14

HERE = os.path.dirname(os.path.abspath(__file__))
x, y = sp.symbols('x y')
DS = [3, 5, 7, 9, 11, 13, 15]


def line(s=""):
    print(s)
    sys.stdout.flush()


def expr(P):
    return sp.expand(sum(sp.Rational(v) * x**i * y**j for (i, j), v in P.items()))


def row_formula(P, i, j):
    out = {}
    for (a, b), p in P.items():
        co = p * (a * j - b * i)
        if co:
            k = (a + i - 1, b + j - 1)
            out[k] = out.get(k, 0) + co
    return {k: v for k, v in out.items() if v}


def unimodular(P):
    Px, Py = expr(m.dx(P)), expr(m.dy(P))
    if Px == 0 or Py == 0:
        return False
    return list(sp.groebner([Px, Py], x, y, order='grevlex').exprs) == [1]


def structure(P, D=12):
    A = sorted(P)
    shifts = [(a - 1, b - 1) for (a, b) in A]
    diffs = [(A[k][0] - A[0][0], A[k][1] - A[0][1]) for k in range(1, len(A))]
    rank = int(sp.Matrix(diffs).rank()) if diffs else 0
    S = m.carrier(D)
    cols, rows = m.build(P, S)
    maxrows = max((len(cc) for cc in cols.values()), default=0)
    # bipartite incidence graph
    parent = {}

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    V, E = 0, 0
    for r in rows:
        parent[('r', r)] = ('r', r)
    for cm, cc in cols.items():
        if cc:
            parent[('c', cm)] = ('c', cm)
    V = len(parent)
    for cm, cc in cols.items():
        for r in cc:
            E += 1
            ru, cu = find(('r', r)), find(('c', cm))
            if ru != cu:
                parent[ru] = cu
    comps = len({find(u) for u in parent})
    betti = E - V + comps
    # forest test on the ROW graph (columns as edges) and forced zeros
    forest, forced_hits_00 = None, None
    if len(A) == 2:
        p2 = {r: r for r in rows}

        def f2(u):
            while p2[u] != u:
                p2[u] = p2[p2[u]]
                u = p2[u]
            return u
        forest = True
        for cm, cc in cols.items():
            if len(cc) == 2:
                a1, a2 = list(cc)
                if f2(a1) == f2(a2):
                    forest = False
                else:
                    p2[f2(a1)] = f2(a2)
        zero = set()
        changed = True
        while changed:
            changed = False
            for cm, cc in cols.items():
                live = [r for r in cc if r not in zero]
                if len(live) == 1 and len(cc) >= 1:
                    zero.add(live[0])
                    changed = True
        forced_hits_00 = ((0, 0) in zero)
    return {"support": [list(a) for a in A], "n_terms": len(A),
            "shift_vectors": [list(s) for s in shifts],
            "shift_differences": [list(d) for d in diffs],
            "rank_of_shift_lattice": rank,
            "max_rows_per_column": maxrows,
            "carrier_for_graph": D, "bipartite_V": V, "bipartite_E": E,
            "bipartite_components": comps, "cycle_rank": betti,
            "row_graph_is_forest": forest,
            "forced_zeros_reach_(0,0)": forced_hits_00}


CASES = [
    ("K0  base            y*(x*y + 1)          two-term, delta=(1,1)",
     {(1, 2): F(1), (0, 1): F(1)}),
    ("K1  x + x^2 y                            two-term, delta=(1,1), other ray",
     {(1, 0): F(1), (2, 1): F(1)}),
    ("K2  y + x y^3                            two-term, delta=(1,2)",
     {(0, 1): F(1), (1, 3): F(1)}),
    ("K3  y + x y^2 + x^2 y^3                  three-term, shift diffs PARALLEL (rank 1)",
     {(0, 1): F(1), (1, 2): F(1), (2, 3): F(1)}),
    ("K4  y + y^2 + x y^2                      three-term, shift diffs rank 2",
     {(0, 1): F(1), (0, 2): F(1), (1, 2): F(1)}),
    ("K5  y + y^3 + x y^2                      three-term, shift diffs rank 2",
     {(0, 1): F(1), (0, 3): F(1), (1, 2): F(1)}),
    ("K6  y + y^2 + y^3 + x y^2                four-term, shift diffs rank 2",
     {(0, 1): F(1), (0, 2): F(1), (0, 3): F(1), (1, 2): F(1)}),
]


if __name__ == "__main__":
    OUT = {"row_formula_check": None, "cases": []}

    line("=" * 78)
    line("THE GENERAL ROW FORMULA, checked against expanded brackets")
    line("=" * 78)
    bad = []
    tot = 0
    for lab, P in CASES:
        for (i, j) in m.carrier(12):
            tot += 1
            g = m.bracket(P, {(i, j): F(1)})
            w = row_formula(P, i, j)
            if {k: F(v) for k, v in g.items()} != {k: F(v) for k, v in w.items()}:
                bad.append((lab, i, j))
    line("  [P, x^i y^j] = sum_{(a,b) in A} p_ab (a j - b i) x^{a+i-1} y^{b+j-1}")
    line("  checked on %d (case, monomial) pairs, i+j <= 12: agrees with expanded bracket: %s"
         % (tot, not bad))
    OUT["row_formula_check"] = {"pairs": tot, "agree": not bad, "mismatches": bad[:5]}
    assert not bad

    for lab, P in CASES:
        line()
        line("=" * 78)
        line(lab)
        line("=" * 78)
        rec = {"label": lab, "P": sp.sstr(expr(P))}
        st = structure(P)
        rec["structure"] = st
        line("  P = %s   deg = %d" % (sp.sstr(expr(P)), m.tdeg(P)))
        line("  support A = %s   shift vectors = %s" % (st["support"], st["shift_vectors"]))
        line("  shift differences = %s   rank = %d   max rows per column = %d"
             % (st["shift_differences"], st["rank_of_shift_lattice"], st["max_rows_per_column"]))
        line("  bipartite incidence graph on S(12): V=%d E=%d comps=%d  CYCLE RANK = %d"
             % (st["bipartite_V"], st["bipartite_E"], st["bipartite_components"], st["cycle_rank"]))
        if st["row_graph_is_forest"] is not None:
            line("  row graph (columns as edges) is a FOREST: %s ; forced zeros reach (0,0): %s"
                 % (st["row_graph_is_forest"], st["forced_zeros_reach_(0,0)"]))
        # certification
        um = unimodular(P)
        bz = m.bezout(P, maxdeg=6)
        syv, syst = sy14.certify(poly14.clean(P))
        fac = sp.factor_list(sp.Poly(expr(P), x, y))
        rec["unimodular_groebner"] = bool(um)
        rec["bezout"] = {"found": bz is not None, "deg_bound": bz[2] if bz else None,
                         "residual_terms": len(bz[3]) if bz else None,
                         "U": m.to_str(bz[0]) if bz else None, "V": m.to_str(bz[1]) if bz else None}
        rec["shpilrain_yu"] = syv
        rec["fibre_factorisation"] = sp.sstr(sp.factor(expr(P)))
        rec["fibre_n_components"] = len(fac[1])
        line("  unimodular: (P_x,P_y)=(1) by Groebner: %s ; explicit Bezout at deg <= %s with"
             " residual %s terms" % (um, bz[2] if bz else "-", len(bz[3]) if bz else "-"))
        line("     U = %s" % (m.to_str(bz[0]) if bz else "-"))
        line("     V = %s" % (m.to_str(bz[1]) if bz else "-"))
        line("  Shpilrain-Yu: %s (nodes=%d) ; zero fibre factors as %s  (%d components)"
             % (syv, syst["nodes"], sp.sstr(sp.factor(expr(P))), len(fac[1])))
        if not (um and bz is not None and len(bz[3]) == 0 and syv == "NON_COORDINATE"):
            line("  *** NOT a certified unimodular non-coordinate point -- skipping mate solve")
            rec["mate_rows"] = "SKIPPED_NOT_CERTIFIED"
            OUT["cases"].append(rec)
            continue
        rows = []
        for D in DS:
            t0 = time.time()
            d = m.decide(P, D)
            if d["verdict"] == "MATE_over_Q":
                # ---------------- HIT GATE ----------------
                Q = d["Q"]
                res = m.psub(m.bracket(P, Q), {(0, 0): F(1)})
                h = hashlib.sha256(("%s|%s" % (sp.sstr(expr(P)), m.to_str(Q))).encode()).hexdigest()[:12]
                hd = os.path.join(HERE, "HIT_%s" % h)
                os.makedirs(hd, exist_ok=True)
                json.dump({"P": sp.sstr(expr(P)), "P_dict": {str(k): str(v) for k, v in P.items()},
                           "Q": m.to_str(Q), "Q_dict": {str(k): str(v) for k, v in Q.items()},
                           "D": D, "bracket_minus_1_terms": len(res),
                           "bracket_minus_1": m.to_str(res),
                           "unimodular_groebner": bool(unimodular(P)),
                           "bezout_residual_terms": len(m.bezout(P, maxdeg=8)[3]),
                           "shpilrain_yu": sy14.certify(poly14.clean(P))[0],
                           "fibre": sp.sstr(sp.factor(expr(P)))},
                          open(os.path.join(hd, "hit.json"), "w"), indent=1)
                line("  *** SYSTEM CONSISTENT at D=%d -- HIT GATE, files at %s" % (D, hd))
                json.dump(OUT, open(os.path.join(HERE, 'broken19.json'), 'w'), indent=1)
                sys.exit(0)
            lam = {eval(k): sp.Rational(v) for k, v in d["lambda"].items()}
            diag = all(a == b for (a, b) in lam)
            rows.append({"D": D, "verdict": d["verdict"], "n_unknowns": d["n_unknowns"],
                         "n_equations": d["n_equations"], "lambda_support": d["lambda_support"],
                         "lambda_verified": d["lambda_verified"], "lambda_is_diagonal": bool(diag),
                         "lambda": d["lambda"], "secs": round(time.time() - t0, 2)})
            line("  D=%-3d n=%-4d rows=%-4d %-14s |supp lambda|=%-4d verified=%-5s  diagonal support=%-5s (%.1fs)"
                 % (D, d["n_unknowns"], d["n_equations"], d["verdict"], d["lambda_support"],
                    d["lambda_verified"], diag, time.time() - t0))
        rec["mate_rows"] = rows
        OUT["cases"].append(rec)

    json.dump(OUT, open(os.path.join(HERE, 'broken19.json'), 'w'), indent=1)
    line()
    line("NO MATE SYSTEM WAS CONSISTENT; no HIT directory written.")
