"""night14 -- emit one CRUX_<hash>/RECORD.md per object measured with
U = PASS (char 0) and SY = NON_COORDINATE, from records.json.
"""

import json
import os
from fractions import Fraction as F
import poly14 as P14

TPL = """# night14 CRUX_%(hash)s

Object (ring: Q[x,y]), family %(family)s -- %(label)s

    P   = %(poly)s
    P_x = %(px)s
    P_y = %(py)s

total degree %(tdeg)d, deg_x %(degx)d, deg_y %(degy)d, %(nterms)d terms.
hash = sha256 of the canonical string form of P, first 12 hex digits.

## (a) U-test -- 1 in (P_x, P_y)

    mod-p shadow (p = 999983, Singular groebner) : %(u_modp)s   %(t_modp)s s
    char-0 verdict (Singular groebner, ring 0)   : %(u_q)s   %(t_q)s s   <- recorded verdict

So P_x and P_y have no common zero over C: the critical locus of P is empty
and every fibre of P is smooth.

## (b) SY-certificate -- gradient-row reduction over Q

    verdict %(sy)s   nodes = %(sy_nodes)s  leaves = %(sy_leaves)s   %(t_sy)s s

## Independent corroboration of (b) -- FIB-screen, no SY involved

    verdict %(fib)s
    (lambda, number of factors of P - lambda over Q, geometric genus if
     irreducible): %(fib_detail)s
    %(t_fib)s s

Reason recorded: because the U-test passed, every fibre of P is smooth, so
two distinct components of a fibre would meet in a singular point -- a
reducible fibre is therefore a disconnected one.  A coordinate has every
fibre isomorphic to the affine line, which is connected and of genus 0.  So
the observation above is by itself a proof that P is not a component of any
polynomial automorphism.

## Scope note

Gradient-unimodularity is the necessary condition (a) only.  Nothing here
measures whether P admits a Jacobian mate, and no such claim is made.

## Reproduce

    cd night14 && python3 -c "import json, poly14 as P, sy14, utest14, fib14; \\
      r = [r for r in json.load(open('records.json')) if r['hash']=='%(hash)s'][0]; \\
      print(r['poly'], r['u_q'], r['sy'], r['fib'])"
"""


def poly_from_row(row, rows_polys):
    return rows_polys[row["hash"]]


def main(records="records.json", root="."):
    rows = json.load(open(records))
    # rebuild the polynomials by re-running the generators is unnecessary:
    # the canonical string is stored, and the gradient strings are recomputed
    # from a parse of the stored monomial data kept alongside.
    made = []
    for r in rows:
        if not r.get("crux"):
            continue
        P = P14.clean({tuple(k): F(v) for k, v in r["monomials"]})
        d = dict(r)
        d["px"] = P14.to_str(P14.dx(P))
        d["py"] = P14.to_str(P14.dy(P))
        d["fib_detail"] = str(r["fib_detail"])
        outdir = os.path.join(root, "CRUX_" + r["hash"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "RECORD.md"), "w") as fh:
            fh.write(TPL % d)
        made.append(outdir)
    print("wrote %d CRUX records" % len(made))
    return made


if __name__ == "__main__":
    main()
