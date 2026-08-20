# RURs at prime-hygiene-compliant primes

STATUS.md §2.4 item 2. The CASE2 route had used 65521 (compliant) plus 32003 and
65537, **both ≡ 2 (mod 3)**, violating the campaign's rule that primes satisfy
`p ≡ 1 (mod 3)` (so that √−3 exists mod p, matching the ℚ(√−3) Belyi field).

Regenerated at compliant primes with `_c2_rur.py`:

| file | prime | p mod 3 | eliminant factors |
|---|---|---|---|
| `c2rur_65539.txt` | 65539 | 1 ✓ | 8, degrees 1,2,2,6,6,6,6,6 (sum 35) |
| `c2rur_65599.txt` | 65599 | 1 ✓ | 6, degrees 1,3,3,4,12,12 (sum 35) |

Running the full Route-2 chain on these (`_c2_multiprime.py`, log in
`../c2_route2_compliant.log`) reproduces **`VERDICT: dim = 2`** on every branch,
same component `(α₂,α₃,β₂,β₃)`. **The verdict survives the hygiene fix.**

Note: `_c2_rur.py` writes to a hard-coded scratch path from an earlier session;
these are copies, preserved here so the result does not depend on a scratch
directory that no longer exists.
