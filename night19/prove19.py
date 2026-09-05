"""night19 -- machine verification of the all-D proof for P = gamma x y^2 + c y.

Two independent checks:

  (A) THE ROW FORMULA.  UNCONDITIONAL.md derives, by hand,
          [P, x^i y^j] = (j - 2i)*gamma * x^i y^{j+1}  -  c*i * x^{i-1} y^j .
      Here that closed form is compared, monomial by monomial, against the
      bracket computed by honest polynomial multiplication in mate19.bracket.

  (B) THE CERTIFICATE.  The closed form
          lambda_{n,n} = (-1)^n c^n / ((n+1) gamma^n),  0 <= n <= floor((D+1)/2)
      is written down independently of any elimination and checked to satisfy
      lambda^T M = 0 on EVERY column of the carrier S(D) and lambda^T e = 1,
      over the field Q(gamma, c), for D = 2 .. DMAX.
"""
import json, os, sys, time
import sympy as sp
import mate19 as m

HERE = os.path.dirname(os.path.abspath(__file__))
gam, c = sp.symbols('gamma c')
P = {(1, 2): gam, (0, 1): c}
DMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def closed_lambda(D):
    return {(n, n): sp.Rational((-1) ** n, n + 1) * c**n / gam**n
            for n in range((D + 1) // 2 + 1)}


def row_formula(i, j):
    out = {}
    if (j - 2 * i) != 0:
        out[(i, j + 1)] = (j - 2 * i) * gam
    if i != 0:
        out[(i - 1, j)] = -c * i
    return out


if __name__ == "__main__":
    out = {"P": "gamma*x*y^2 + c*y", "DMAX": DMAX, "row_formula_check": {}, "rows": []}

    print("=" * 78)
    print("(A)  the hand-derived ROW FORMULA vs bracket() by polynomial multiplication")
    print("=" * 78)
    Dchk = 30
    bad = []
    n = 0
    for (i, j) in m.carrier(Dchk):
        n += 1
        got = m.bracket(P, {(i, j): 1})
        want = row_formula(i, j)
        if set(got) != set(want) or any(m._iszero(got[k] - want[k]) is False for k in want):
            bad.append((i, j))
    print("  all %d monomials x^i y^j with i+j <= %d: closed row formula agrees with"
          " the expanded bracket: %s" % (n, Dchk, not bad))
    if bad:
        print("  MISMATCHES:", bad[:10])
    out["row_formula_check"] = {"carrier_D": Dchk, "monomials": n, "agree": not bad,
                                "mismatches": bad[:10]}

    print()
    print("=" * 78)
    print("(B)  the closed-form lambda over Q(gamma, c), carrier by carrier")
    print("=" * 78)
    ok = True
    for D in range(2, DMAX + 1):
        t0 = time.time()
        S = m.carrier(D)
        cols, rows = m.build(P, S)
        lam = closed_lambda(D)
        # every row carrying a nonzero lambda entry must be an actual row of M
        insupp = all(r in set(rows) for r in lam)
        good, msg = m.verify_lambda(lam, cols)
        ok &= (good and insupp)
        dt = time.time() - t0
        out["rows"].append({"D": D, "n_unknowns": len(S), "n_equations": len(rows),
                            "lambda_support": len(lam),
                            "support_inside_row_set": bool(insupp),
                            "verified": bool(good), "verification": msg,
                            "secs": round(dt, 2)})
        print("  D=%-3d n=%-5d rows=%-5d |supp|=%-3d supp_are_rows=%-5s verified over Q(gamma,c): %-5s (%.1fs)"
              % (D, len(S), len(rows), len(lam), insupp, good, dt))
        sys.stdout.flush()
    out["all_verified"] = bool(ok)
    json.dump(out, open(os.path.join(HERE, 'prove19.json'), 'w'), indent=1)
    print()
    print("CLOSED FORM VERIFIED AT EVERY CARRIER D = 2..%d" % DMAX if ok else "*** FAILED ***")
