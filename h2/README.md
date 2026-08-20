# h2/ — the above-125 (Track D / H2) sweep, run without touching the campaign's files

`trackD_extract.py`, `trackD_twoprime.py` and `trackD_targets.json` are **copies**
of `campaign/audit_tracks/` files. The only edit is in `trackD_twoprime.py`: its
`STATE` path points at `h2/h2_state.json` instead of the campaign's
`trackD_twoprime_state.json`, so this session's runs never write to the campaign
state file. `h2_state.json` starts as a copy of the campaign state (38 targets:
24 EMPTY, 14 TIMEOUT at a 90 s budget) and is advanced from there at a 900 s
budget per prime.

Run as:

    cd h2
    PYTHONPATH=../campaign/audit_tracks TRACKD_SCRATCH=/tmp/scr \
      python3 trackD_twoprime.py 900 200

`w5_h2_controls.py` is new. It replaces the shipped `--control`, which is
vacuous: that control forms its "unsaturated" variant by deleting lines
containing `sat` or beginning `ideal N`, and the generated Singular source
contains neither — its non-degeneracy conditions are the Rabinowitsch lines
`I = I + ideal(w*p10 - 1);` and `I = I + ideal(u*nd - 1);`. So the variant is
byte-identical to the real system, returns EMPTY, and the control reports FAIL
for a reason unrelated to the engine. The replacement deletes the Rabinowitsch
generators for real (51 bytes), asserts that the deletion changed the source,
asserts that the shipped deletion does not, and then requires the unsaturated
system to be non-EMPTY and a contradictory pin to be EMPTY. 5/5 in
`h2_controls.log`.
