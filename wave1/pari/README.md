# PARI/GP scripts — the degree-1144 eliminant

These produced STATUS.md §2.5 (the eliminant is irreducible over ℚ). They were
written at the shell and are preserved here so the result is reproducible.

| file | role |
|---|---|
| `elim.gp` … `elim5.gp` | successive attempts to parse msolve's output; the early ones FAIL and are kept because they document the format wrestle (msolve writes `<bignum>/2^k`, which Python's `Fraction` cannot parse but GP evaluates natively) |
| `param.gp`, `param2.gp`, `param3.gp` | locating the eliminant inside the `-P 1` parametrization structure |
| `elimfinal.gp` | **extracts the eliminant**: degree 1144, squarefree, leading coefficient 4666 digits; writes `../edgeQ_eliminant.txt` |
| `factdiag.gp`, `fd2.gp`, `fd3.gp`, `fd4.gp` | mod-p factorization diagnostic; `fd4.gp` is the one that produced the 8-prime degree table |
| `eliminant_modp_degrees.txt` | that table, raw |

The Dedekind sieve itself (subset-sum over the degree multisets) is in
`../w1_h1f_eliminant.py`, which also carries the controls.

Reproduce: `msolve -P 1 -f ../edgeQ_input.ms -o ../edgeQ_param.out`, then
`gp -q elimfinal.gp`, then `gp -q fd4.gp`, then `python3 ../w1_h1f_eliminant.py`.
