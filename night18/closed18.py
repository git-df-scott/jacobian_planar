"""night18 -- the CLOSED FORM of the obstruction on the slice, checked carrier by carrier.

On the slice R = gamma x y^2 + c y the rref certificate came out, at every
carrier tested, as the diagonal vector

    lambda_{n,n} = (-1)^n c^n / ((n+1) gamma^n) ,   0 <= n <= floor((D+1)/2),
    lambda_m     = 0 otherwise.

This module writes that formula down independently of any elimination and
verifies lambda^T M = 0 on every column and lambda^T e = 1 over Q(gamma, c),
for a range of carriers.
"""
import json, os, sys, time
import sympy as sp
import spk18 as spk, mate18

X, Y = spk.X, spk.Y
HERE = os.path.dirname(os.path.abspath(__file__))
gam, c = sp.symbols('gamma c')


def closed_lambda(D):
    return {(n, n): sp.Rational((-1) ** n, n + 1) * c**n / gam**n
            for n in range((D + 1) // 2 + 1)}


if __name__ == "__main__":
    R = spk.from_expr(gam * X * Y**2 + c * Y)
    out = {"slice": spk.to_str(R),
           "closed_form": "lambda_{n,n} = (-1)^n c^n / ((n+1) gamma^n), 0 <= n <= floor((D+1)/2)",
           "rows": []}
    ok = True
    for D in range(2, 25):
        t0 = time.time()
        S = mate18.carrier(D)
        cols, rows = mate18.build(R, S)
        lam = closed_lambda(D)
        good, msg = mate18.verify_lambda(lam, cols)
        ok &= good
        out["rows"].append({"deg_Q_bound": D, "n_unknowns": len(S), "n_equations": len(rows),
                            "lambda_support": len(lam), "verified": bool(good),
                            "verification": msg, "secs": round(time.time() - t0, 1)})
        print("  D=%-3d n=%-4d rows=%-4d |supp lambda|=%-3d verified over Q(gamma,c): %s  (%.1fs)"
              % (D, len(S), len(rows), len(lam), good, time.time() - t0))
        sys.stdout.flush()
    out["all_verified"] = bool(ok)
    json.dump(out, open(os.path.join(HERE, 'closed18.json'), 'w'), indent=1)
    print("CLOSED FORM VERIFIED at every carrier tested" if ok else "*** FAILED ***")
