# NIGHT22 MANIFEST

| artifact | claim | status | one-command verification |
|---|---|---|---|
| `PROFILE_STRIKE.md` | target class is realized; profile enumeration, closure chain, component-pole criterion | exact proofs plus cited theorems with hypotheses | read report and run all commands below |
| `profiles22.py`, `profiles22.csv` | exact Suzuki-compatible profile atoms in the displayed box; Briançon jump arithmetic | exact integer arithmetic | `python3 night22/profiles22.py` |
| `briancon22.py`, `briancon22.json` | builds both degree-10 targets; four systems EMPTY through degree 30 with lambda certificates | exact over Q, carrier-bounded | `python3 night22/briancon22.py 30` |
| `survivor_rational22.py`, `survivor_rational22.json` | two night15 period survivors have explicit rational mates and unequal component pole coefficients | exact over Q | `python3 night22/survivor_rational22.py` |
| `eigenpole22.py`, `eigenpole22.json` | all 2,755 reducible eigenmate hits have noncancellable component poles; all 143 cancellations are coordinate rows | exact over Q; individual absolute-component distribution partly unresolved | `python3 night22/eigenpole22.py` |

No numerical or modular result is promoted to an exact claim.  No
counterexample is claimed.
