"""night20 -- Task 2/4: decide the linear system D_P(A) = P exactly over Q for
every certified object, with carriers escalating in deg A and a lambda
certificate on EMPTY.  A CONSISTENT system is the hit case when the object's
fibres are all irreducible (then A/P is a rational mate and, by the pole
theorem, a polynomial one)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import pole20 as PL
x, y = I.x, I.y


def rhs_list(P, rec):
    """The right-hand sides allowed by the pole theorem: prod_i (P - c_i)^{k_i}.
    Taken here over the rational special values of c (the reducible ones and,
    when there are none, c = 0 and c = P(0,0)) with pole order k <= 2."""
    import sympy as _sp
    cs = []
    for m in (rec.get("reducible_c") or []):
        mm = _sp.Poly(_sp.sympify(m, locals={'c': _sp.Symbol('c')}),
                      _sp.Symbol('c'))
        if mm.degree() == 1:
            cs.append(list(_sp.roots(mm))[0])
    cs += [_sp.Integer(0), _sp.expand(P).subs({x: 0, y: 0})]
    ded = []
    for c0 in cs:
        if not any(_sp.simplify(c0 - d) == 0 for d in ded):
            ded.append(c0)
    out = []
    for c0 in ded:
        out.append(("(P - %s)" % _sp.sstr(c0), _sp.expand(P - c0)))
        out.append(("(P - %s)^2" % _sp.sstr(c0), _sp.expand((P - c0)**2)))
    if len(ded) >= 2:
        out.append(("prod (P - c_i)", _sp.expand(_sp.prod([P - c0 for c0 in ded]))))
    return out


def decide_A(P, Dlist, rhss):
    rows = []
    for (nm, RHS) in rhss:
        for D in Dlist:
            r = PL.solve_A_rhs(P, RHS, D)
            r["D"] = D
            r["rhs"] = nm
            rows.append(r)
            if r["verdict"] == "A_over_Q":
                return "A_FOUND", rows
    return "EMPTY", rows


def main(src, dst, extra=8, cap=24, limit=None):
    recs = json.load(open(os.path.join(HERE, src)))
    if limit:
        recs = recs[:limit]
    out = []
    t0 = time.time()
    for n, r in enumerate(recs):
        P = sp.sympify(r["P"], locals={'x': x, 'y': y})
        d = r["deg"]
        top = min(cap, d + extra)
        sched = sorted(set(list(range(1, min(top, 8) + 1))
                           + list(range(8, top + 1, 2)) + [top]))
        v, rows = decide_A(P, sched, rhs_list(P, r))
        r2 = dict(r)
        r2["A_verdict"] = v
        r2["A_top_D"] = rows[-1]["D"]
        if v == "A_FOUND":
            r2["A_rhs"] = rows[-1]["rhs"]
            r2["A"] = rows[-1]["A"]
            r2["A_residual"] = rows[-1]["residual"]
            r2["A_verified"] = rows[-1]["verified"]
        else:
            r2["A_rhs_tried"] = sorted(set(rr["rhs"] for rr in rows))
            r2["A_lambda_support"] = rows[-1].get("lambda_support")
            r2["A_lambda_verified"] = rows[-1].get("lambda_verified")
            r2["A_lambda_verification"] = rows[-1].get("verification")
        out.append(r2)
        print("[%4d/%4d %6.0fs] deg=%-3d %-40s allirr=%-5s A: %-8s topD=%-3d %s"
              % (n + 1, len(recs), time.time() - t0, d, r["P"][:40],
                 r.get("all_fibres_irreducible"), v, r2["A_top_D"],
                 ("A = " + str(r2.get("A"))[:40]) if v == "A_FOUND"
                 else ("|lambda|=%s verified=%s" % (r2.get("A_lambda_support"),
                                                    r2.get("A_lambda_verified")))),
              flush=True)
        json.dump(out, open(os.path.join(HERE, dst), "w"), indent=1)
        if v == "A_FOUND" and r.get("all_fibres_irreducible"):
            print("HIT GATE CANDIDATE: consistent A-system on an "
                  "all-fibres-irreducible P: %s" % r["P"], flush=True)
            return out
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],
         limit=int(sys.argv[3]) if len(sys.argv) > 3 else None)
