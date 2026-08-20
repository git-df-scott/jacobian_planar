# jacobian_planar — plane Jacobian conjecture campaign

## Start here

* **`TRUST_MAP.md`** — which of the campaign's closures are real and which were only
  claimed. Every load-bearing claim, with a verdict and a certificate reference.
* **`L4_ENDGAME_REPORT.md`** — the mathematics: the endgame residue equation
  `T_{D,m}(R) = −c` solved completely, what that does to the Sessions 16–18 emptiness
  theorem, and the corrected transfer theorem.
* **`LIVE_MAP.md`** — what moved, what is still open, and the terminal state of this
  iteration.

## Headline

The Sessions 16–18 proof that Borisov's First Framework at `(99,66)` is empty rests on
the step *"the left side vanishes at `v = −1`; the right side is `−c ≠ 0`"*. That step is
**invalid**: it assumes `R` has no pole at `v = −1`. The equation

```
    (v+1)^4 ( 3 v(v+1) R'(v) − 13 R(v) ) = κ ≠ 0
```

has **exactly one** rational solution,

```
    R(v) = − κ (243 v^4 − 81 v^3 + 54 v^2 − 42 v + 35) / (455 (v+1)^4),
```

with a pole at `v = −1` of order exactly 4.

The **conclusion survives** on two repaired closures — a ladder bound capping the pole
order at 3, and a degree ledger giving `deg R = 4 ≠ 13` — neither of which needs the lost
THEOREM 2/3 certificates. The transfer conjecture is **refuted in both halves** and
replaced by a proved statement that kills the whole published framework family at once,
with no Belyi rederivation required.

## Reproduce

```
./run_all.sh
```

Runs every certifier — the 15 re-runnable archive scripts and the 12 new ones — under
exact arithmetic. Nonzero exit if anything fails. Requires `python3` + `sympy` and
`gp` (PARI/GP). Current status: all pass (183 sympy checks, 47 PARI checks, no shared
code between the toolchains).

## Layout

```
certifiers/rerun/   the archive's own scripts, split out of the status-report file
certifiers/new/     this session's certifiers (E1…E9, EA, EB, EC)
logs/               output of the last ./run_all.sh
39, 40.md, 41.md, 42.md, "Sessions 1-18 status reports"   the archive, unmodified
```
