"""night20 -- run the full instrument pipeline on a list of candidate P."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import gen20 as G
x, y, c = I.x, I.y, I.c


def certify(P, tmo=240):
    rec = {"P": sp.sstr(P), "deg": int(sp.Poly(P, x, y).total_degree())}
    u = I.unimodular(P)
    rec["unimodular"] = u.get("unimodular")
    if u.get("unimodular"):
        rec["bezout_U"] = sp.sstr(u["U"])
        rec["bezout_V"] = sp.sstr(u["V"])
        rec["bezout_residual"] = sp.sstr(u["residual"])
        rec["bezout_ok"] = bool(u["residual_zero"])
    else:
        rec["reduce_1"] = str(u.get("reduce_1_mod_std", u.get("reason")))
        return rec
    rec["baker_interior_pts"] = G.interior(sp.Poly(P, x, y).monoms())
    g, gm = I.genus_generic(P, timeout=tmo)
    rec["genus"] = g
    rec["genus_msg"] = gm
    if g is None:
        return rec
    fi = I.all_fibres_irreducible(P, timeout=tmo)
    rec["fibre_ok"] = fi.get("ok")
    if fi.get("ok"):
        rec["all_fibres_irreducible"] = fi["all_irreducible"]
        rec["n_special_c"] = fi["n_candidates"]
        rec["fibre_rows"] = fi["rows"]
        rec["reducible_c"] = [r["m(c)"] for r in fi["rows"]
                              if r["abs_components"] != "1"]
    else:
        rec["fibre_reason"] = fi.get("reason")
    return rec


def main(src, dst, limit=None):
    raw = json.load(open(os.path.join(HERE, src)))
    if limit:
        raw = raw[:limit]
    out = []
    t0 = time.time()
    for n, r in enumerate(raw):
        P = sp.sympify(r["P"], locals={'x': x, 'y': y})
        rec = certify(P)
        rec["baker"] = r.get("baker")
        out.append(rec)
        print("[%3d/%3d %6.0fs] deg=%-3d %-42s unimod=%-5s genus=%-4s allirr=%-5s bad_c=%s"
              % (n + 1, len(raw), time.time() - t0, rec["deg"], rec["P"][:42],
                 rec["unimodular"], rec.get("genus"),
                 rec.get("all_fibres_irreducible"), rec.get("reducible_c")),
              flush=True)
        json.dump(out, open(os.path.join(HERE, dst), "w"), indent=1)
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
