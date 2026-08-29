# night16 -- the atypical-value re-screen

night15's period screen evaluated the Gelfand-Leray periods only at a few
generic fibre values (c = 0, 1, -1, 3/2 depending on the instrument).  A
non-coordinate P with no critical points must have ATYPICAL VALUES: finitely
many c at which the fibration fails to be locally trivial purely because of
behaviour at infinity.  night16 closes that gap.

* `atyp16.py`   -- exact atypical-value detector (Euler characteristic of F_c
                   as an exact function of c, over Q and over number fields).
* `period16.py` -- EXACT-PRIM, the exact per-fibre exactness test with a
                   certificate, plus the NUM-MONO cross-check.
* `mono16.py`, `pk16.py`, `exact_he16.py` -- night15 instruments, copied into
                   this lane unchanged so that nothing is written outside it.
* `controls16.py` -- the control suite (hard gate).
* `screen16.py`  -- the re-screen of night15's 57 PERIODS-VANISHING survivors.
* `ATYPICAL.md`, `atypical.csv` -- the deliverables.

Measurements only.
