"""night15 -- EXACT-G1: the period screen in closed form for the whole
v-power family  P = h0*v + c*(x-a)^n * v^m,  v = y + t(x)/2,  m >= 2.

REDUCTION.  y -> y - t(x)/2 and x -> x + a are triangular automorphisms of
Jacobian 1, so (G3) they carry fibres to fibres by maps pulling eta back to eta
and the period verdict is unchanged.  After them

        P = h0*y + c*x^n*y^m.

FORM.  On the fibre {P = lam},  c x^n y^m = lam - h0 y,  and
        P_x = c*n*x^(n-1)*y^m,
so
        eta = dy/P_x = x*dy/(c*n*x^n*y^m) = x*dy / ( n*(lam - h0*y) ).      (*)

SUPERELLIPTIC MODEL.  Put z = c*y^m*x.  Raising  c y^m x^n = lam - h0 y  to a
suitable power gives

        z^n = c^(n-1) * y^(m(n-1)) * (lam - h0*y)  =:  R(y),
        eta = z*dy / ( c*n*y^m*(lam - h0*y) ).                              (**)

so the fibre is the superelliptic curve z^n = R(y), an n-sheeted cover of the
y-line, and eta is explicit on it.

PLACES (lam != 0, so lam/h0 != 0).
  y = 0        : R vanishes to order m(n-1); gcd(n, m(n-1)) = gcd(n, m) =: d0
                 places, each with ramification n/d0.  There x -> infinity, so
                 these are PUNCTURES.
  y = lam/h0   : R has a simple zero; one place, ramification n.  There x = 0,
                 an honest AFFINE point of the fibre.
  y = infinity : deg R = m(n-1)+1 = 1-m (mod n); gcd(n, m-1) =: dinf places.
                 There x -> 0 (m >= 2), so these are PUNCTURES.

GENUS (Riemann-Hurwitz for the degree-n cover of the y-line; the three loci
above are the only ramification):
    2 - 2g = 2n - (n - d0) - (n - 1) - (n - dinf)
    ==>  2g = n + 1 - gcd(n, m) - gcd(n, m-1).
(For m = 2 this is n - gcd(n,2), i.e. g = floor((n-1)/2), matching EXACT-HE.)

LEADING EXPONENTS OF eta.
  at y = infinity: R ~ -c^(n-1) h0 y^(m(n-1)+1), so z ~ const*y^((m(n-1)+1)/n)
      and by (**) eta ~ const * y^((1-m-n)/n) dy.  With y = tau^(-n/dinf) this
      is  const * tau^((m-1)/dinf - 1) d tau:  NO residue for m >= 2, and
      holomorphic there.
  at y = 0: the FULL local expansion is needed, not just the leading exponent
      (an earlier version of this file read the residue off the leading term
      and got the wrong answer for n = 2, m = 4; the corrected computation is
      below and is what the numerical instrument confirms).
      Take the local parameter tau with y = tau^(n'), n' = n/d0, d0 = gcd(n,m).
      Then ord_tau(z) = m(n-1)/d0 and, writing N(y) = lam - h0 y,

          eta/d tau = tau^((n-m)/d0 - 1) * (1/(c*d0)) * c^((n-1)/n)
                      * N(tau^(n'))^((1-n)/n) .

      N(tau^(n'))^((1-n)/n) = lam^((1-n)/n) * sum_j binom((1-n)/n, j)
                              * (-h0/lam)^j * tau^(j n') .
      The residue is the coefficient of tau^(-1), i.e. of tau^k with
      k = (m-n)/d0, so it is nonzero exactly when
          k >= 0,  n' | k,  and  binom((1-n)/n, k/n') != 0.
      Now n' | k  <=>  n | (m-n)  <=>  n | m, and for n >= 2 the exponent
      (1-n)/n is a negative non-integer so every binomial coefficient is
      nonzero, while for n = 1 the exponent is 0 and only j = 0 survives.
      Hence

          residues at y = 0 are nonzero  <=>  n >= 2, m >= n and n | m.

      (n = m is the sub-case k = 0, where u = z/y^(n-1) satisfies
       u^n = c^(n-1)(lam - h0 y), eta = u dy/(c n y (lam - h0 y)) and
       Res = u0/(c n lam) for each of the n roots u0 of u0^n = c^(n-1) lam;
       those n roots sum to 0, which is control C3 discharged symbolically.
       The same cancellation holds for general k because the d0 places differ
       exactly by the d0-th roots of unity in the chosen branch of z.)

VERDICTS (lam != 0).
  (i)   n >= 2 and n | m : nonzero residues at the places over y = 0.
                           VERDICT: NONVANISHING.
  (ii)  otherwise, g = 0 : all residues vanish and the compact model is P^1;
                           on P^1 every residue-free meromorphic 1-form is
                           exact (partial fractions), so every period is 0.
                           VERDICT: VANISHING.
  (iii) otherwise, n > m : eta is holomorphic at every place (exponents above),
                           so with g >= 1 it is a nonzero holomorphic 1-form on
                           a compact curve of positive genus.
                           VERDICT: NONVANISHING.
  (iv)  otherwise        : eta is of the second kind (poles at y = 0, zero
                           residues) on a curve of genus >= 1; its class in
                           H^1 is not settled by these exponents.
                           VERDICT: DEFERRED_TO_NUM.
"""

from math import gcd


def screen(n, m, lam_is_zero=False):
    if m < 2 or n < 1:
        return {"applicable": False, "reason": "needs m >= 2, n >= 1"}
    if lam_is_zero:
        return {"applicable": False, "reason": "derivation assumes lam != 0"}
    d0, dinf = gcd(n, m), gcd(n, m - 1)
    two_g = n + 1 - d0 - dinf
    assert two_g >= 0 and two_g % 2 == 0, (n, m, two_g)
    g = two_g // 2
    out = {"applicable": True, "n": n, "m": m, "genus": g,
           "n_places_at_infinity": d0 + dinf,
           "places_over_y0": d0, "places_over_yinf": dinf,
           "eta_exponent_at_y0_minus_1": "(n-m)/d0",
           "sum_residues": "0"}
    res_nonzero = (n >= 2 and m >= n and m % n == 0)
    out["residues_at_y0_nonzero"] = res_nonzero
    if res_nonzero:
        out.update({"verdict": "NONVANISHING", "case": "i",
                    "witness": "nonzero residues at the %d places over y = 0 "
                               "(n >= 2 and n | m)" % d0,
                    "residues_nonzero": True})
    elif g == 0:
        out.update({"verdict": "VANISHING", "case": "ii",
                    "witness": "all residues zero and the compact model is P^1",
                    "residues_nonzero": False})
    elif n > m:
        out.update({"verdict": "NONVANISHING", "case": "iii",
                    "witness": "nonzero holomorphic 1-form on a compact curve "
                               "of genus %d" % g,
                    "residues_nonzero": False})
    else:
        out.update({"verdict": "DEFERRED_TO_NUM", "case": "iv",
                    "witness": "second-kind differential, genus %d" % g,
                    "residues_nonzero": False})
    return out


if __name__ == "__main__":
    print("  n   m  genus  places  verdict")
    for m in range(2, 8):
        for n in range(1, 13):
            r = screen(n, m)
            print("%3d %3d %5d %6d  %s" % (n, m, r["genus"],
                                           r["n_places_at_infinity"], r["verdict"]))
