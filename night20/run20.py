"""night20 -- mate-solve every certified object, and, on EMPTY, look for the
rational mate and record where its poles are."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import mate20 as MT
x, y, c = I.x, I.y, I.c


def denominator_candidates(P, rec):
    """The night19 mechanism says the rational mate's poles sit on a component
    of a reducible fibre.  Candidates: every irreducible factor over Q of
    P - c0 for each rational reducible value c0, then the factors of P_x, P_y."""
    out = []
    for m in rec.get("reducible_c", []):
        mm = sp.Poly(sp.sympify(m, locals={'c': c}), c)
        if mm.degree() != 1:
            continue
        c0 = sp.roots(mm)
        c0 = list(c0)[0]
        F = sp.expand(P - c0)
        for (f, e) in sp.factor_list(F)[1]:
            if sp.Poly(f, x, y).total_degree() >= 1:
                out.append(("fibre c=%s" % c0, sp.expand(f)))
    for nm, D in (("P_x", sp.diff(P, x)), ("P_y", sp.diff(P, y))):
        for (f, e) in sp.factor_list(sp.expand(D))[1]:
            if sp.Poly(f, x, y).total_degree() >= 1:
                out.append((nm, sp.expand(f)))
    ded, seen = [], set()
    for nm, f in out:
        k = sp.sstr(f)
        if k in seen:
            continue
        seen.add(k)
        ded.append((nm, f))
    return ded


RM_K = 2
RM_A = 8


def main(src, dst, mult=2, cap=26, tlim=100000):
    recs = json.load(open(os.path.join(HERE, src)))
    out = []
    t0 = time.time()
    for n, r in enumerate(recs):
        if not r.get("unimodular") or r.get("genus") in (None, 0):
            continue
        P = sp.sympify(r["P"], locals={'x': x, 'y': y})
        d = r["deg"]
        m = 4 if d <= 6 else mult
        sched = MT.schedule(P, mult=m, cap=cap)
        v, rows = MT.mate_verdict(P, sched)
        r2 = dict(r)
        r2["mate_verdict"] = v
        r2["mate_carriers"] = [rr["D"] for rr in rows]
        r2["mate_top_D"] = rows[-1]["D"]
        r2["mate_deg_bound_multiple"] = m
        if v == "MATE":
            r2["Q"] = rows[-1]["Q"]
            r2["bracket_minus_1"] = rows[-1]["bracket_minus_1"]
            r2["verified"] = rows[-1]["verified"]
        else:
            last = rows[-1]
            r2["lambda_support"] = last.get("lambda_support")
            r2["lambda_verified"] = last.get("lambda_verified")
            r2["lambda_verification"] = last.get("verification")
            r2["certificate_id"] = "lam-%s-D%d" % (
                __import__("hashlib").sha1(r["P"].encode()).hexdigest()[:10],
                last["D"])
            gens = [g for (_, g) in denominator_candidates(P, r)]
            rr = MT.rational_mate_box(P, gens, kmax=RM_K, DAmax=min(RM_A, 2 * d))
            r2["rational_mate"] = rr
            r2["rational_mate_found"] = bool(rr.get("found"))
            r2["rational_mate_poles"] = rr.get("poles")
            r2["rational_mate_Q"] = rr.get("Q")
            r2["rational_mate_denominators_tried"] = rr.get("n_denominators_tried")
            r2["rational_mate_generators"] = [sp.sstr(g) for g in gens]
        out.append(r2)
        print("[%3d %6.0fs] deg=%-3d %-40s %-6s topD=%-3d |lam|=%-4s ratmate=%-5s poles=%s"
              % (n + 1, time.time() - t0, d, r["P"][:40], v, r2["mate_top_D"],
                 r2.get("lambda_support"), r2.get("rational_mate_found"),
                 r2.get("rational_mate_poles")), flush=True)
        json.dump(out, open(os.path.join(HERE, dst), "w"), indent=1)
        if v == "MATE":
            print("HIT GATE: a system was consistent at %s" % r["P"], flush=True)
            return out
        if time.time() - t0 > tlim:
            break
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
