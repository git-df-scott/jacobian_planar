
---

## 4. What the atypical fibres of the survivors are, in closed form

### 4.1 The G1 family (53 of the 57 survivors), at `lam = 0`

night15's G1 family is `P = h0 v + c (x-a)^n v^m`, `v = y + t(x)/2`,
`h0 != 0`, `c != 0`, `n >= 1`, `m >= 2`.  The shears `y -> y - t(x)/2` and
`x -> x + a` are triangular with Jacobian 1, so they carry fibres to fibres by
maps pulling `eta` back to `eta`; after them

    P = h0 y + c x^n y^m .

At `lam = 0` this factors:

    P = y * ( h0 + c x^n y^(m-1) ) .

The two factors have no common zero (`h0 != 0` on `{y = 0}`), so the fibre is
the **disjoint** union of

    L  = {y = 0}                        ~  C ,
    C0 = {h0 + c x^n y^(m-1) = 0}       =  {x^n y^(m-1) = -h0/c} ,

and with `d = gcd(n, m-1)` the second is `d` disjoint copies of `C*` (write
`n = d n'`, `m-1 = d k'`, `gcd(n',k') = 1`; the equation splits as `d` equations
`x^(n') y^(k') = B_i`, `B_i^d = -h0/c`, and each of those is parametrised by
`t -> (B_i^p t^(k'), B_i^q t^(-n'))` with `p n' + q k' = 1`).  Hence

    chi(F_0) = 1 + d * 0 = 1 ,

while the generic fibre has `chi = 2 - 2g - r` with `g, r` as tabulated by
night15 — so `c = 0` **is** atypical for every member with `chi_gen != 1`.

Now the periods.  `P_y = h0 + m c x^n y^(m-1)`, so

* on `L`:  `P_y = h0`, hence `eta = -dx/P_y = d(-x/h0)`;
* on `C0`: `c x^n y^(m-1) = -h0`, hence `P_y = h0 - m h0 = (1-m) h0 != 0`
  (this uses `m >= 2`), and `eta = -dx/P_y = d( x / ((m-1) h0) )`.

`eta` is therefore **exact on every component of `F_0`, with a primitive that
is linear in `x`**, and every period on the atypical fibre vanishes.  This is a
closed-form statement about the whole family; the machine run below reproduces
it independently, on the actual (sheared, un-normalised) `P` of each record,
through EXACT-PRIM, which returns a verified certificate of degree 1 or 2 for
every component.

Note where this uses `m >= 2`: if `m = 1` the factor `(1-m) h0` is `0` and the
argument gives nothing — and indeed `m = 1` members are not in the G1 family
(`P = h0 v + c (x-a)^n v` is `v` times a polynomial in `x`, of `deg_y 1`).

### 4.2 The G2 family (4 of the 57 survivors)

`P = alpha x + beta + c B(x) y^m`, `B = prod (x - a_i)^(e_i)`, `e_i >= 2`,
`alpha != 0`.  Here `P_y = c m B y^(m-1)` and `P_x = alpha + c B' y^m`.  The
detector's output for these four is reported in the table; the derivation of
their atypical sets from the shape is given with the results, since it depends
on `m` and on the roots `a_i`.

---

## 5. Results
