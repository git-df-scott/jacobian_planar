# JC2 msolve system register -- summary

Generated from `/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt` (read-only). Files: `REGISTER.json`, `TIMEOUT_SHAPES.json`, `register_build.py`.

## 1. Counts

| quantity | value |
|---|---|
| `.ms` files found | 1489 |
| input systems (parsed) | 1481 |
| msolve *output* files misfiled as `.ms` | 8 |
| parse failures (input systems) | 0 |
| header-only (>5 MB) | 38 |
| distinct content hashes (all) | 455 |
| distinct content hashes (parsed systems) | 453 |
| duplicate hash groups | 386 |
| ... of which cross-name (not just worktree mirrors) | 27 |
| systems with excess <= 0 | 371 (88 unique) |
| systems with torus rank > 0 | 895 (262 unique) |

**Redundancy**: 1489 files collapse to 455 distinct systems -- a 3.3x duplication factor, almost all of it the four-way `canon`/`mailbox`/`p11`/`hunt` worktree mirror.

## 2. Cross-name duplicates (same mathematics, different file name)

- `29c3df507fa430ac` (9 files, 2 distinct names)
    - p108_192622.ms
    - w6_35657_0.ms
- `e8f4768d0f3d59f7` (8 files, 2 distinct names)
    - pent_L18.ms
    - pent_L18_g2.ms
- `21d39e883458d9a3` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000003.ms
    - sym_n6_a2_b5_p0_q0_one_mutant_nosat_P1000003.ms
- `71627dd7eb45c305` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000033.ms
    - sym_n6_a2_b5_p0_q0_one_mutant_nosat_P1000033.ms
- `dfe0c6a34b5bc78b` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000039.ms
    - sym_n6_a2_b5_p0_q0_one_mutant_nosat_P1000039.ms
- `00689d3b5115bad4` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000003.ms
    - sym_n6_a2_b5_p0_q0_one_pin_nosat_P1000003.ms
- `62c1bb1ca849d518` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000033.ms
    - sym_n6_a2_b5_p0_q0_one_pin_nosat_P1000033.ms
- `53274f8dc18d15df` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000039.ms
    - sym_n6_a2_b5_p0_q0_one_pin_nosat_P1000039.ms
- `8989a668bb99bacf` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_real_sat_P1000003.ms
    - sym_n6_a2_b5_p0_q0_one_real_sat_P1000003.ms
- `3c2ae9fd934540e7` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_real_sat_P1000033.ms
    - sym_n6_a2_b5_p0_q0_one_real_sat_P1000033.ms
- `23ddb6e98fea9fb8` (8 files, 2 distinct names)
    - sym_n4_a2_b1_p0_q0_one_real_sat_P1000039.ms
    - sym_n6_a2_b5_p0_q0_one_real_sat_P1000039.ms
- `cbbe5fbe0bea68a5` (8 files, 2 distinct names)
    - c2_w4_one_real_p1000003.ms
    - probe_w4m4_real_p1000003.ms
- `ddba96e2d47f60f3` (8 files, 2 distinct names)
    - casc_w4_pin_one_p1000003.ms
    - item1_w4_pin_one_p1000003.ms
- `c7d7aca7d653b10a` (8 files, 2 distinct names)
    - casc_w4_pin_one_p1000033.ms
    - item1_w4_pin_one_p1000033.ms
- `f3bf3aeb7c3f4fda` (8 files, 2 distinct names)
    - casc_w4_pin_zero_p1000003.ms
    - item1_w4_pin_zero_p1000003.ms
- `8a912e1178151d68` (8 files, 2 distinct names)
    - casc_w4_real_one_p1000003.ms
    - item1_w4_real_one_p1000003.ms
- `de14480b86d9e849` (8 files, 2 distinct names)
    - casc_w4_real_one_p1000033.ms
    - item1_w4_real_one_p1000033.ms
- `4b13c33d9d63b780` (8 files, 2 distinct names)
    - casc_w4_real_zero_p1000003.ms
    - item1_w4_real_zero_p1000003.ms
- `8c98cf0743a9fe6e` (6 files, 2 distinct names)
    - p108_821326.ms
    - p108_843700.ms
- `b7889adac5624464` (6 files, 1 distinct names)
    - w6_289012_0.ms
- `e915a19cc3913346` (5 files, 1 distinct names)
    - trackB1_case1_full_p65521.ms
- `0047b83a45f0fedb` (5 files, 1 distinct names)
    - trackB_edgeQ.ms
- `fcedb73568a99d10` (5 files, 1 distinct names)
    - trackD_calib_case2_p65521.ms
- `94823fee64382604` (2 files, 2 distinct names)
    - hbranch_k5_chained.ms
    - hbranch_k5_ht_D4_p1000003.ms
- `db02cca27b384085` (2 files, 2 distinct names)
    - reduced_102v.ms
    - reduced_verify_102v.ms
- `07c01643e6d1f805` (2 files, 2 distinct names)
    - reduced_72v.ms
    - reduced_verify_72v.ms
- `2fc70bb5a7edbb41` (2 files, 2 distinct names)
    - reduced_91v.ms
    - reduced_verify_91v.ms

## 3. Systems with excess = n_eqs - n_vars <= 0 (an emptiness run there is vacuous)

| system | n_vars | n_eqs | excess | char | files |
|---|---|---|---|---|---|
| `canon/pent/slice_ctl_pos.ms` | 59 | 2 | -57 | 1000003 | 4 |
| `hunt/pent/pent_L14_g2.ms` | 59 | 3 | -56 | 1000003 | 1 |
| `canon/pent/pent_L14_g3.ms` | 59 | 4 | -55 | 1000003 | 4 |
| `canon/wave1/pent_L15.ms` | 59 | 6 | -53 | 1000003 | 4 |
| `canon/pent/slice_ctl_pin.ms` | 59 | 9 | -50 | 1000003 | 4 |
| `canon/wave1/pent_L17.ms` | 59 | 15 | -44 | 1000003 | 4 |
| `canon/pent/pent_L18_g2.ms` | 59 | 21 | -38 | 1000003 | 8 |
| `canon/pent/pent_L18_g3.ms` | 59 | 22 | -37 | 1000003 | 4 |
| `canon/wave5/ms2/pent_L18_g4.ms` | 59 | 23 | -36 | 1000003 | 3 |
| `hunt/pent/pent_L19_g2.ms` | 59 | 28 | -31 | 1000003 | 1 |
| `canon/pent/pent_L19_g3.ms` | 59 | 29 | -30 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 22 | 2 | -20 | 1000003 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 22 | 2 | -20 | 1000033 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 22 | 2 | -20 | 1000039 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000003.ms` | 23 | 3 | -20 | 1000003 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000033.ms` | 23 | 3 | -20 | 1000033 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000039.ms` | 23 | 3 | -20 | 1000039 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000003.ms` | 22 | 4 | -18 | 1000003 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000033.ms` | 22 | 4 | -18 | 1000033 | 8 |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000039.ms` | 22 | 4 | -18 | 1000039 | 8 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 33 | 22 | -11 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 33 | 22 | -11 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 33 | 22 | -11 | 1000039 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000003.ms` | 34 | 23 | -11 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000033.ms` | 34 | 23 | -11 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000039.ms` | 34 | 23 | -11 | 1000039 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000003.ms` | 33 | 24 | -9 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000033.ms` | 33 | 24 | -9 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000039.ms` | 33 | 24 | -9 | 1000039 | 4 |
| `canon/wave0/a6c_ms_ctl_empty.ms` | 7 | 3 | -4 | 65521 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 41 | 39 | -2 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 41 | 39 | -2 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 41 | 39 | -2 | 1000039 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000003.ms` | 42 | 40 | -2 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000033.ms` | 42 | 40 | -2 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000039.ms` | 42 | 40 | -2 | 1000039 | 4 |
| `canon/wave6/bottomedge/be_free_p1000003.ms` | 18 | 17 | -1 | 1000003 | 3 |
| `canon/wave6/bottomedge/be_free_q.ms` | 18 | 17 | -1 | 0 | 3 |
| `canon/wave4/artifacts/c2_w4_one_real_p1000003.ms` | 20 | 19 | -1 | 1000003 | 8 |
| `canon/campaign/audit_tracks/trackB_edgeQ.ms` | 7 | 7 | 0 | 0 | 5 |
| `canon/wave0/a6c_ms_ctl_zero.ms` | 7 | 7 | 0 | 65521 | 4 |
| `canon/wave0/a6c_ms_plant_p65521.ms` | 7 | 7 | 0 | 65521 | 4 |
| `canon/wave0/a6c_ms_plant_p65539.ms` | 7 | 7 | 0 | 65539 | 4 |
| `canon/wave0/a6c_ms_plant_p65599.ms` | 7 | 7 | 0 | 65599 | 4 |
| `canon/wave0/a6c_ms_real_p65521.ms` | 7 | 7 | 0 | 65521 | 4 |
| `canon/wave0/a6c_ms_real_p65539.ms` | 7 | 7 | 0 | 65539 | 4 |
| `canon/wave0/a6c_ms_real_p65599.ms` | 7 | 7 | 0 | 65599 | 4 |
| `canon/wave1/edgeQ_input.ms` | 7 | 7 | 0 | 0 | 4 |
| `canon/wave4/artifacts/casc_w4_mutant_one_p1000003.ms` | 12 | 12 | 0 | 1000003 | 4 |
| `canon/wave4/artifacts/casc_w4_mutant_one_p1000033.ms` | 12 | 12 | 0 | 1000033 | 4 |
| `canon/wave4/artifacts/casc_w4_mutant_one_p1000039.ms` | 12 | 12 | 0 | 1000039 | 4 |
| `canon/wave4/artifacts/casc_w4_real_one_p1000003.ms` | 12 | 12 | 0 | 1000003 | 8 |
| `canon/wave4/artifacts/casc_w4_real_one_p1000033.ms` | 12 | 12 | 0 | 1000033 | 8 |
| `canon/wave4/artifacts/casc_w4_real_one_p1000039.ms` | 12 | 12 | 0 | 1000039 | 4 |
| `canon/wave4/artifacts/item1_w4_mutant_one_p1000003.ms` | 12 | 12 | 0 | 1000003 | 4 |
| `canon/wave4/artifacts/item1_w4_mutant_one_p1000033.ms` | 12 | 12 | 0 | 1000033 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000081.ms` | 12 | 12 | 0 | 1000081 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000099.ms` | 12 | 12 | 0 | 1000099 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000117.ms` | 12 | 12 | 0 | 1000117 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000159.ms` | 12 | 12 | 0 | 1000159 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000171.ms` | 12 | 12 | 0 | 1000171 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000183.ms` | 12 | 12 | 0 | 1000183 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000213.ms` | 12 | 12 | 0 | 1000213 | 4 |
| `canon/wave4/artifacts/more_w4_real_one_p1000231.ms` | 12 | 12 | 0 | 1000231 | 4 |
| `hunt/wave4/artifacts/more_w4_real_one_p1000249.ms` | 12 | 12 | 0 | 1000249 | 1 |
| `hunt/wave4/artifacts/more_w4_real_one_p1000273.ms` | 12 | 12 | 0 | 1000273 | 1 |
| `hunt/wave4/artifacts/more_w4_real_one_p1000291.ms` | 12 | 12 | 0 | 1000291 | 1 |
| `canon/campaign/d23_borisov/ff_h_system.ms` | 13 | 13 | 0 | 0 | 4 |
| `canon/wave6/bottomedge/be_c2is1_p1000003.ms` | 18 | 18 | 0 | 1000003 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000033.ms` | 18 | 18 | 0 | 1000033 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000039.ms` | 18 | 18 | 0 | 1000039 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000081.ms` | 18 | 18 | 0 | 1000081 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000117.ms` | 18 | 18 | 0 | 1000117 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000121.ms` | 18 | 18 | 0 | 1000121 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000133.ms` | 18 | 18 | 0 | 1000133 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000151.ms` | 18 | 18 | 0 | 1000151 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000159.ms` | 18 | 18 | 0 | 1000159 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p1000171.ms` | 18 | 18 | 0 | 1000171 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p999961.ms` | 18 | 18 | 0 | 999961 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p999979.ms` | 18 | 18 | 0 | 999979 | 3 |
| `canon/wave6/bottomedge/be_c2is1_p999983.ms` | 18 | 18 | 0 | 999983 | 3 |
| `canon/wave6/bottomedge/be_c2is1_q.ms` | 18 | 18 | 0 | 0 | 3 |
| `canon/wave6/bottomedge/be_c2is0_p1000003.ms` | 19 | 19 | 0 | 1000003 | 3 |
| `canon/wave6/bottomedge/be_c2is0_q.ms` | 19 | 19 | 0 | 0 | 3 |
| `canon/campaign/d23_borisov/sf_h_system.ms` | 23 | 23 | 0 | 0 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000003.ms` | 41 | 41 | 0 | 1000003 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000033.ms` | 41 | 41 | 0 | 1000033 | 4 |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000039.ms` | 41 | 41 | 0 | 1000039 | 4 |

## 4. Systems with grading torus rank > 0 (msolve solve mode cannot terminate; needs `-g 2` or a gauge)

| system | rank | n_vars | n_eqs | excess | size_bytes | char | Rabinowitsch |
|---|---|---|---|---|---|---|---|
| `mailbox/wave6/pentseed/char0_118v.ms` | 94 | 119 | 236 | 117 | 2443473 | 0 | True |
| `mailbox/wave6/pentseed/reduced_p1000033ctl_121v.ms` | 93 | 122 | 240 | 118 | 4005660 | 1000033 | True |
| `mailbox/wave6/pentseed/reduced_p1000033ctl_135v.ms` | 91 | 136 | 254 | 118 | 983753 | 1000033 | True |
| `mailbox/wave6/pentseed/reduced_p1000033_120v.ms` | 71 | 121 | 238 | 117 | 1202462 | 1000033 | True |
| `mailbox/wave6/pentseed/reduced_ctl111v.ms` | 69 | 112 | 230 | 118 | 969201 | 1000003 | True |
| `mailbox/wave6/pentseed/reduced_ctl96v.ms` | 67 | 97 | 215 | 118 | 4087958 | 1000003 | True |
| `mailbox/wave6/pentseed/reduced_102v.ms` | 56 | 103 | 220 | 117 | 1132591 | 1000003 | True |
| `canon/pent/slice_ctl_pos.ms` | 28 | 59 | 2 | -57 | 19446 | 1000003 | True |
| `canon/pent/pent_L18_g2.ms` | 23 | 59 | 21 | -38 | 2704006 | 1000003 | False |
| `canon/pent/pent_L18_g3.ms` | 23 | 59 | 22 | -37 | 2704015 | 1000003 | True |
| `canon/pent/pent_L19_g3.ms` | 23 | 59 | 29 | -30 | 5055198 | 1000003 | True |
| `canon/pent/slice_ctl_pin.ms` | 23 | 59 | 9 | -50 | 270280 | 1000003 | True |
| `canon/wave1/pent_L15.ms` | 23 | 59 | 6 | -53 | 255073 | 1000003 | False |
| `canon/wave1/pent_L17.ms` | 23 | 59 | 15 | -44 | 1360162 | 1000003 | False |
| `canon/wave5/ms2/pent_L18_g4.ms` | 23 | 59 | 23 | -36 | 2704024 | 1000003 | True |
| `hunt/pent/pent_L14_g2.ms` | 23 | 59 | 3 | -56 | 84342 | 1000003 | False |
| `hunt/pent/pent_L19_g2.ms` | 23 | 59 | 28 | -31 | 5055189 | 1000003 | False |
| `canon/pent/pent_L14_g3.ms` | 22 | 59 | 4 | -55 | 84351 | 1000003 | True |
| `canon/campaign/audit_tracks/trackB1_case1_full_p65521.ms` | 22 | 166 | 284 | 118 | 182714 | 65521 | True |
| `mailbox/wave6/frontier/trackB1_sat_Q.ms` | 22 | 166 | 284 | 118 | 151730 | 0 | True |
| `mailbox/wave6/frontier/trackB1_sat_p1000003.ms` | 22 | 166 | 284 | 118 | 170396 | 1000003 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 21 | 22 | 2 | -20 | 185 | 1000003 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 21 | 22 | 2 | -20 | 185 | 1000033 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 21 | 22 | 2 | -20 | 185 | 1000039 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000003.ms` | 21 | 23 | 3 | -20 | 215 | 1000003 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000033.ms` | 21 | 23 | 3 | -20 | 215 | 1000033 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_real_sat_P1000039.ms` | 21 | 23 | 3 | -20 | 215 | 1000039 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000003.ms` | 20 | 22 | 4 | -18 | 215 | 1000003 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000033.ms` | 20 | 22 | 4 | -18 | 215 | 1000033 | True |
| `canon/symslice/artifacts/sym_n4_a2_b1_p0_q0_one_pin_nosat_P1000039.ms` | 20 | 22 | 4 | -18 | 215 | 1000039 | True |
| `canon/wave6/ms/p108_192622.ms` | 18 | 40 | 139 | 99 | 1603469 | 65521 | True |
| `canon/wave6/ms/p108_821326.ms` | 18 | 41 | 165 | 124 | 1526110 | 65521 | True |
| `canon/wave6/pentseed/seed0_p1000003.ms` | 18 | 148 | 267 | 119 | 146851 | 1000003 | True |
| `canon/wave6/pentseed/seed0_p1000003_lin.ms` | 16 | 123 | 241 | 118 | 187977 | 1000003 | True |
| `p11/codex_p11zero/p11zero_full_sat_p1000003.ms` | 15 | 186 | 306 | 120 | 125784 | 1000003 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 14 | 33 | 22 | -11 | 2410 | 1000003 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 14 | 33 | 22 | -11 | 2489 | 1000033 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 14 | 33 | 22 | -11 | 2487 | 1000039 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000003.ms` | 14 | 34 | 23 | -11 | 2295 | 1000003 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000033.ms` | 14 | 34 | 23 | -11 | 2372 | 1000033 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_real_sat_P1000039.ms` | 14 | 34 | 23 | -11 | 2372 | 1000039 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000003.ms` | 13 | 33 | 24 | -9 | 2281 | 1000003 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000033.ms` | 13 | 33 | 24 | -9 | 2358 | 1000033 | True |
| `canon/symslice/artifacts/sym_n3_a1_b1_p0_q0_one_pin_nosat_P1000039.ms` | 13 | 33 | 24 | -9 | 2358 | 1000039 | True |
| `canon/wave6/ms/p108_525122.ms` | 10 | 28 | 140 | 112 | 1427984 | 65521 | True |
| `canon/wave6/ms/w6_35657_1.ms` | 7 | 23 | 128 | 105 | 522624 | 65521 | True |
| `canon/wave6/ms/w6_582584_0.ms` | 7 | 43 | 72 | 29 | 116654 | 65521 | True |
| `canon/wave6/ms/w6_582584_0_p2.ms` | 7 | 43 | 72 | 29 | 116656 | 1000003 | True |
| `canon/wave0/a6c_ms_ctl_empty.ms` | 6 | 7 | 3 | -4 | 79 | 65521 | True |
| `canon/wave0/a6c_ms_ctl_zero.ms` | 5 | 7 | 7 | 0 | 108 | 65521 | True |
| `canon/wave1/edgeQ_input.ms` | 5 | 7 | 7 | 0 | 20560 | 0 | True |
| `canon/wave6/ms/w6_289012_1.ms` | 5 | 23 | 69 | 46 | 55976 | 65521 | True |
| `canon/wave6/ms/w6_289012_1_p2.ms` | 5 | 23 | 69 | 46 | 55978 | 1000003 | True |
| `canon/wave6/ms/w6_582584_1.ms` | 5 | 23 | 54 | 31 | 73998 | 65521 | True |
| `canon/wave6/ms/w6_582584_1_p2.ms` | 5 | 23 | 54 | 31 | 74000 | 1000003 | True |
| `canon/wave6/ms/w6_289012_0.ms` | 5 | 41 | 82 | 41 | 69088 | 65521 | True |
| `canon/wave6/ms/w6_289012_0_p2.ms` | 5 | 41 | 82 | 41 | 69090 | 1000003 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000003.ms` | 5 | 42 | 40 | -2 | 5567 | 1000003 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000033.ms` | 5 | 42 | 40 | -2 | 5659 | 1000033 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_real_sat_P1000039.ms` | 5 | 42 | 40 | -2 | 5659 | 1000039 | True |
| `canon/campaign/audit_tracks/trackD_calib_case2_p65521.ms` | 5 | 73 | 93 | 20 | 19463 | 65521 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000003.ms` | 4 | 41 | 41 | 0 | 5554 | 1000003 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000033.ms` | 4 | 41 | 41 | 0 | 5646 | 1000033 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_pin_nosat_P1000039.ms` | 4 | 41 | 41 | 0 | 5646 | 1000039 | True |
| `canon/wave5/ms/b16_d12_p1000003.ms` | 4 | 42 | 55 | 13 | 69283 | 1000003 | True |
| `canon/wave5/ms/b16_d12_p1000033.ms` | 4 | 42 | 55 | 13 | 69283 | 1000033 | True |
| `canon/wave5/ms/b16_d12_p1000039.ms` | 4 | 42 | 55 | 13 | 69283 | 1000039 | True |
| `canon/wave5/ms/b16_d12_q.ms` | 4 | 42 | 55 | 13 | 69277 | 0 | True |
| `mailbox/wave6/frontier/hbranch_k5_chained.ms` | 4 | 46 | 64 | 18 | 6564 | 1000003 | False |
| `mailbox/wave6/frontier/hbranch_k6_ht_D4_p1000003.ms` | 4 | 56 | 85 | 29 | 8395 | 1000003 | False |
| `canon/wave6/slice_mu3z_d14.ms` | 3 | 42 | 55 | 13 | 62174 | 1000003 | True |
| `canon/wave6/slice_mu3z_d15.ms` | 3 | 45 | 59 | 14 | 79502 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000003_f0.ms` | 2 | 8 | 28 | 20 | 5273 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000003_f1.ms` | 2 | 8 | 28 | 20 | 10922 | 1000003 | False |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000003_f2.ms` | 2 | 8 | 28 | 20 | 10910 | 1000003 | False |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000033_f0.ms` | 2 | 8 | 28 | 20 | 10918 | 1000033 | False |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000033_f1.ms` | 2 | 8 | 28 | 20 | 17146 | 1000033 | False |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000039_f0.ms` | 2 | 8 | 28 | 20 | 5277 | 1000039 | True |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000039_f1.ms` | 2 | 8 | 28 | 20 | 10923 | 1000039 | False |
| `canon/wave4/artifacts/casc_res_mutant_one_p1000039_f2.ms` | 2 | 8 | 28 | 20 | 10923 | 1000039 | False |
| `canon/wave4/artifacts/casc_res_pin_one_p1000003_f0.ms` | 2 | 8 | 30 | 22 | 5082 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000003_f1.ms` | 2 | 8 | 30 | 22 | 10731 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000003_f2.ms` | 2 | 8 | 30 | 22 | 10722 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000033_f0.ms` | 2 | 8 | 30 | 22 | 10731 | 1000033 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000033_f1.ms` | 2 | 8 | 30 | 22 | 16956 | 1000033 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000039_f0.ms` | 2 | 8 | 30 | 22 | 5086 | 1000039 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000039_f1.ms` | 2 | 8 | 30 | 22 | 10737 | 1000039 | True |
| `canon/wave4/artifacts/casc_res_pin_one_p1000039_f2.ms` | 2 | 8 | 30 | 22 | 10733 | 1000039 | True |
| `canon/wave4/artifacts/casc_res_real_one_p1000003_f0.ms` | 2 | 8 | 28 | 20 | 5050 | 1000003 | True |
| `canon/wave4/artifacts/casc_res_real_one_p1000003_f1.ms` | 2 | 8 | 28 | 20 | 10699 | 1000003 | False |
| `canon/wave4/artifacts/casc_res_real_one_p1000003_f2.ms` | 2 | 8 | 28 | 20 | 10690 | 1000003 | False |
| `canon/wave4/artifacts/casc_res_real_one_p1000033_f0.ms` | 2 | 8 | 28 | 20 | 10699 | 1000033 | False |
| `canon/wave4/artifacts/casc_res_real_one_p1000033_f1.ms` | 2 | 8 | 28 | 20 | 16924 | 1000033 | False |
| `canon/wave4/artifacts/casc_res_real_one_p1000039_f0.ms` | 2 | 8 | 28 | 20 | 5054 | 1000039 | True |
| `canon/wave4/artifacts/casc_res_real_one_p1000039_f1.ms` | 2 | 8 | 28 | 20 | 10705 | 1000039 | False |
| `canon/wave4/artifacts/casc_res_real_one_p1000039_f2.ms` | 2 | 8 | 28 | 20 | 10701 | 1000039 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000081_f0.ms` | 2 | 8 | 28 | 20 | 5266 | 1000081 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000081_f1.ms` | 2 | 8 | 28 | 20 | 5271 | 1000081 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000081_f2.ms` | 2 | 8 | 28 | 20 | 5268 | 1000081 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000081_f3.ms` | 2 | 8 | 28 | 20 | 10917 | 1000081 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000099_f0.ms` | 2 | 8 | 28 | 20 | 5270 | 1000099 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000099_f1.ms` | 2 | 8 | 28 | 20 | 5283 | 1000099 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000099_f2.ms` | 2 | 8 | 28 | 20 | 17185 | 1000099 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000117_f0.ms` | 2 | 8 | 28 | 20 | 5273 | 1000117 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000117_f1.ms` | 2 | 8 | 28 | 20 | 23418 | 1000117 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000159_f0.ms` | 2 | 8 | 28 | 20 | 5260 | 1000159 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000159_f1.ms` | 2 | 8 | 28 | 20 | 23428 | 1000159 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000171_f0.ms` | 2 | 8 | 28 | 20 | 5284 | 1000171 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000171_f1.ms` | 2 | 8 | 28 | 20 | 5271 | 1000171 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000171_f2.ms` | 2 | 8 | 28 | 20 | 17161 | 1000171 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000183_f0.ms` | 2 | 8 | 28 | 20 | 10910 | 1000183 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000183_f1.ms` | 2 | 8 | 28 | 20 | 17161 | 1000183 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000213_f0.ms` | 2 | 8 | 28 | 20 | 10924 | 1000213 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000213_f1.ms` | 2 | 8 | 28 | 20 | 17162 | 1000213 | False |
| `canon/wave4/artifacts/more_res_mutant_one_p1000231_f0.ms` | 2 | 8 | 28 | 20 | 5270 | 1000231 | True |
| `canon/wave4/artifacts/more_res_mutant_one_p1000231_f1.ms` | 2 | 8 | 28 | 20 | 10922 | 1000231 | False |
| `canon/wave4/artifacts/more_res_pin_one_p1000081_f0.ms` | 2 | 8 | 30 | 22 | 5077 | 1000081 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000081_f1.ms` | 2 | 8 | 30 | 22 | 5081 | 1000081 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000081_f2.ms` | 2 | 8 | 30 | 22 | 5080 | 1000081 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000081_f3.ms` | 2 | 8 | 30 | 22 | 10730 | 1000081 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000099_f0.ms` | 2 | 8 | 30 | 22 | 5085 | 1000099 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000099_f1.ms` | 2 | 8 | 30 | 22 | 5093 | 1000099 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000099_f2.ms` | 2 | 8 | 30 | 22 | 16996 | 1000099 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000117_f0.ms` | 2 | 8 | 30 | 22 | 5084 | 1000117 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000117_f1.ms` | 2 | 8 | 30 | 22 | 23227 | 1000117 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000159_f0.ms` | 2 | 8 | 30 | 22 | 5071 | 1000159 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000159_f1.ms` | 2 | 8 | 30 | 22 | 23239 | 1000159 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000171_f0.ms` | 2 | 8 | 30 | 22 | 5095 | 1000171 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000171_f1.ms` | 2 | 8 | 30 | 22 | 5079 | 1000171 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000171_f2.ms` | 2 | 8 | 30 | 22 | 16975 | 1000171 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000183_f0.ms` | 2 | 8 | 30 | 22 | 10722 | 1000183 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000183_f1.ms` | 2 | 8 | 30 | 22 | 16973 | 1000183 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000213_f0.ms` | 2 | 8 | 30 | 22 | 10735 | 1000213 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000213_f1.ms` | 2 | 8 | 30 | 22 | 16974 | 1000213 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000231_f0.ms` | 2 | 8 | 30 | 22 | 5082 | 1000231 | True |
| `canon/wave4/artifacts/more_res_pin_one_p1000231_f1.ms` | 2 | 8 | 30 | 22 | 10732 | 1000231 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000081_f0.ms` | 2 | 8 | 28 | 20 | 5045 | 1000081 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000081_f1.ms` | 2 | 8 | 28 | 20 | 5049 | 1000081 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000081_f2.ms` | 2 | 8 | 28 | 20 | 5048 | 1000081 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000081_f3.ms` | 2 | 8 | 28 | 20 | 10698 | 1000081 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000099_f0.ms` | 2 | 8 | 28 | 20 | 5053 | 1000099 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000099_f1.ms` | 2 | 8 | 28 | 20 | 5061 | 1000099 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000099_f2.ms` | 2 | 8 | 28 | 20 | 16964 | 1000099 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000117_f0.ms` | 2 | 8 | 28 | 20 | 5052 | 1000117 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000117_f1.ms` | 2 | 8 | 28 | 20 | 23195 | 1000117 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000159_f0.ms` | 2 | 8 | 28 | 20 | 5039 | 1000159 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000159_f1.ms` | 2 | 8 | 28 | 20 | 23207 | 1000159 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000171_f0.ms` | 2 | 8 | 28 | 20 | 5063 | 1000171 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000171_f1.ms` | 2 | 8 | 28 | 20 | 5047 | 1000171 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000171_f2.ms` | 2 | 8 | 28 | 20 | 16943 | 1000171 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000183_f0.ms` | 2 | 8 | 28 | 20 | 10690 | 1000183 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000183_f1.ms` | 2 | 8 | 28 | 20 | 16941 | 1000183 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000213_f0.ms` | 2 | 8 | 28 | 20 | 10703 | 1000213 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000213_f1.ms` | 2 | 8 | 28 | 20 | 16942 | 1000213 | False |
| `canon/wave4/artifacts/more_res_real_one_p1000231_f0.ms` | 2 | 8 | 28 | 20 | 5050 | 1000231 | True |
| `canon/wave4/artifacts/more_res_real_one_p1000231_f1.ms` | 2 | 8 | 28 | 20 | 10700 | 1000231 | False |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000231_f2.ms` | 2 | 8 | 28 | 20 | 10916 | 1000231 | False |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000249_f0.ms` | 2 | 8 | 28 | 20 | 5266 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000249_f1.ms` | 2 | 8 | 28 | 20 | 5277 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000249_f2.ms` | 2 | 8 | 28 | 20 | 5273 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000249_f3.ms` | 2 | 8 | 28 | 20 | 10915 | 1000249 | False |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000273_f0.ms` | 2 | 8 | 28 | 20 | 5277 | 1000273 | True |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000273_f1.ms` | 2 | 8 | 28 | 20 | 23420 | 1000273 | False |
| `hunt/wave4/artifacts/more_res_mutant_one_p1000291_f0.ms` | 2 | 8 | 28 | 20 | 5286 | 1000291 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000231_f2.ms` | 2 | 8 | 30 | 22 | 10725 | 1000231 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000249_f0.ms` | 2 | 8 | 30 | 22 | 5074 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000249_f1.ms` | 2 | 8 | 30 | 22 | 5090 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000249_f2.ms` | 2 | 8 | 30 | 22 | 5088 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000249_f3.ms` | 2 | 8 | 30 | 22 | 10726 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000273_f0.ms` | 2 | 8 | 30 | 22 | 5089 | 1000273 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000273_f1.ms` | 2 | 8 | 30 | 22 | 23232 | 1000273 | True |
| `hunt/wave4/artifacts/more_res_pin_one_p1000291_f0.ms` | 2 | 8 | 30 | 22 | 5094 | 1000291 | True |
| `hunt/wave4/artifacts/more_res_real_one_p1000231_f2.ms` | 2 | 8 | 28 | 20 | 10693 | 1000231 | False |
| `hunt/wave4/artifacts/more_res_real_one_p1000249_f0.ms` | 2 | 8 | 28 | 20 | 5042 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_real_one_p1000249_f1.ms` | 2 | 8 | 28 | 20 | 5058 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_real_one_p1000249_f2.ms` | 2 | 8 | 28 | 20 | 5056 | 1000249 | True |
| `hunt/wave4/artifacts/more_res_real_one_p1000249_f3.ms` | 2 | 8 | 28 | 20 | 10694 | 1000249 | False |
| `hunt/wave4/artifacts/more_res_real_one_p1000273_f0.ms` | 2 | 8 | 28 | 20 | 5057 | 1000273 | True |
| `hunt/wave4/artifacts/more_res_real_one_p1000273_f1.ms` | 2 | 8 | 28 | 20 | 23200 | 1000273 | False |
| `hunt/wave4/artifacts/more_res_real_one_p1000291_f0.ms` | 2 | 8 | 28 | 20 | 5062 | 1000291 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000003.ms` | 2 | 41 | 39 | -2 | 5856 | 1000003 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000033.ms` | 2 | 41 | 39 | -2 | 5945 | 1000033 | True |
| `canon/symslice/artifacts/sym_n2_a0_b1_p0_q0_one_mutant_nosat_P1000039.ms` | 2 | 41 | 39 | -2 | 5944 | 1000039 | True |
| `canon/wave5/ms2/ctl_d3seedZ_unsat.ms` | 1 | 7 | 10 | 3 | 465 | 1000003 | False |
| `canon/wave5/ms2/b16seed2_d3_Z_p1000003.ms` | 1 | 8 | 11 | 3 | 493 | 1000003 | True |
| `canon/wave5/ms2/b16seed2_d3_Z_p1000033.ms` | 1 | 8 | 11 | 3 | 493 | 1000033 | True |
| `canon/wave5/ms2/ctl_d3seedZ_sat.ms` | 1 | 8 | 11 | 3 | 476 | 1000003 | True |
| `canon/wave5/ms/c16_d7_r0_p1000003.ms` | 1 | 9 | 18 | 9 | 1716041 | 1000003 | True |
| `canon/wave5/ms/c16_d7_r0_p1000033.ms` | 1 | 9 | 18 | 9 | 1716041 | 1000033 | True |
| `canon/wave5/ms/c16_d7_r0_q.ms` | 1 | 9 | 18 | 9 | 1716035 | 0 | True |
| `canon/wave5/ms/c16_d7_r1_p1000003.ms` | 1 | 9 | 18 | 9 | 1716034 | 1000003 | True |
| `canon/wave5/ms/c16_d7_r1_p1000033.ms` | 1 | 9 | 18 | 9 | 1716034 | 1000033 | True |
| `canon/wave5/ms/c16_d7_r1_q.ms` | 1 | 9 | 18 | 9 | 1716028 | 0 | True |
| `canon/wave5/ms/b16_d2_p1000003.ms` | 1 | 12 | 15 | 3 | 1068 | 1000003 | True |
| `canon/wave5/ms/b16_d2_p1000033.ms` | 1 | 12 | 15 | 3 | 1068 | 1000033 | True |
| `canon/wave5/ms/b16_d2_p1000039.ms` | 1 | 12 | 15 | 3 | 1068 | 1000039 | True |
| `canon/wave5/ms/b16_d2_q.ms` | 1 | 12 | 15 | 3 | 1062 | 0 | True |
| `canon/wave5/ms/CTRL_unsat_d3_q.ms` | 1 | 14 | 18 | 4 | 2186 | 0 | False |
| `canon/wave5/ms2/b16r_d5_B_p1000003.ms` | 1 | 14 | 20 | 6 | 2355 | 1000003 | True |
| `canon/wave5/ms2/b16r_d5_B_p1000033.ms` | 1 | 14 | 20 | 6 | 2355 | 1000033 | True |
| `canon/wave5/ms2/b16r_d5_B_p1000039.ms` | 1 | 14 | 20 | 6 | 2355 | 1000039 | True |
| `canon/wave5/ms2/b16r_d5_B_q.ms` | 1 | 14 | 20 | 6 | 2349 | 0 | True |
| `canon/wave5/ms/b16_d3_p1000003.ms` | 1 | 15 | 19 | 4 | 2203 | 1000003 | True |
| `canon/wave5/ms/b16_d3_p1000033.ms` | 1 | 15 | 19 | 4 | 2203 | 1000033 | True |
| `canon/wave5/ms/b16_d3_p1000039.ms` | 1 | 15 | 19 | 4 | 2203 | 1000039 | True |
| `canon/wave5/ms/b16_d3_q.ms` | 1 | 15 | 19 | 4 | 2197 | 0 | True |
| `canon/wave5/ms2/b16s_d5_Z_p1000003.ms` | 1 | 15 | 20 | 5 | 2732 | 1000003 | True |
| `canon/wave6/slice_mu3z_d5.ms` | 1 | 15 | 19 | 4 | 1954 | 1000003 | True |
| `canon/wave5/ms/CTRL_unsat_d4_q.ms` | 1 | 17 | 22 | 5 | 3975 | 0 | False |
| `canon/wave5/ms2/b16r_d6_B_p1000003.ms` | 1 | 17 | 24 | 7 | 4221 | 1000003 | True |
| `canon/wave5/ms2/b16r_d6_B_p1000033.ms` | 1 | 17 | 24 | 7 | 4221 | 1000033 | True |
| `canon/wave5/ms2/b16r_d6_B_p1000039.ms` | 1 | 17 | 24 | 7 | 4221 | 1000039 | True |
| `canon/wave5/ms2/b16r_d6_B_q.ms` | 1 | 17 | 24 | 7 | 4215 | 0 | True |
| `canon/wave5/ms/b16_d4_p1000003.ms` | 1 | 18 | 23 | 5 | 3992 | 1000003 | True |
| `canon/wave5/ms/b16_d4_p1000033.ms` | 1 | 18 | 23 | 5 | 3992 | 1000033 | True |
| `canon/wave5/ms/b16_d4_p1000039.ms` | 1 | 18 | 23 | 5 | 3992 | 1000039 | True |
| `canon/wave5/ms/b16_d4_q.ms` | 1 | 18 | 23 | 5 | 3986 | 0 | True |
| `canon/wave5/ms2/b16s_d6_Z_p1000003.ms` | 1 | 18 | 24 | 6 | 4789 | 1000003 | True |
| `canon/wave6/bottomedge/be_free_p1000003.ms` | 1 | 18 | 17 | -1 | 770 | 1000003 | True |
| `canon/wave6/bottomedge/be_free_q.ms` | 1 | 18 | 17 | -1 | 764 | 0 | True |
| `canon/wave6/bottomedge/be_c2is0_p1000003.ms` | 1 | 19 | 19 | 0 | 784 | 1000003 | True |
| `canon/wave6/bottomedge/be_c2is0_q.ms` | 1 | 19 | 19 | 0 | 778 | 0 | True |
| `canon/wave4/artifacts/c2_w4_one_real_p1000003.ms` | 1 | 20 | 19 | -1 | 1859 | 1000003 | True |
| `canon/wave5/ms2/b16r_d7_B_p1000003.ms` | 1 | 20 | 28 | 8 | 6930 | 1000003 | True |
| `canon/wave5/ms2/b16r_d7_B_p1000033.ms` | 1 | 20 | 28 | 8 | 6930 | 1000033 | True |
| `canon/wave5/ms2/b16r_d7_B_p1000039.ms` | 1 | 20 | 28 | 8 | 6930 | 1000039 | True |
| `canon/wave5/ms2/b16r_d7_B_q.ms` | 1 | 20 | 28 | 8 | 6924 | 0 | True |
| `canon/wave5/ms/b16_d5_p1000003.ms` | 1 | 21 | 27 | 6 | 6649 | 1000003 | True |
| `canon/wave5/ms/b16_d5_p1000033.ms` | 1 | 21 | 27 | 6 | 6649 | 1000033 | True |
| `canon/wave5/ms/b16_d5_p1000039.ms` | 1 | 21 | 27 | 6 | 6649 | 1000039 | True |
| `canon/wave5/ms/b16_d5_q.ms` | 1 | 21 | 27 | 6 | 6643 | 0 | True |
| `canon/wave5/ms2/b16s_d7_Z_p1000003.ms` | 1 | 21 | 28 | 7 | 7733 | 1000003 | True |
| `canon/wave6/slice_mu3z_d7.ms` | 1 | 21 | 27 | 6 | 5805 | 1000003 | True |
| `canon/wave5/ms/b16_d6_p1000003.ms` | 1 | 24 | 31 | 7 | 10380 | 1000003 | True |
| `canon/wave5/ms/b16_d6_p1000033.ms` | 1 | 24 | 31 | 7 | 10380 | 1000033 | True |
| `canon/wave5/ms/b16_d6_p1000039.ms` | 1 | 24 | 31 | 7 | 10380 | 1000039 | True |
| `canon/wave5/ms/b16_d6_q.ms` | 1 | 24 | 31 | 7 | 10374 | 0 | True |
| `canon/wave5/ms2/b16s_d8_Z_p1000003.ms` | 1 | 24 | 32 | 8 | 11745 | 1000003 | True |
| `canon/wave5/ms2/b16s_d8_Z_p1000033.ms` | 1 | 24 | 32 | 8 | 11745 | 1000033 | True |
| `canon/wave5/ms/b16_d7_p1000003.ms` | 1 | 27 | 35 | 8 | 15368 | 1000003 | True |
| `canon/wave5/ms/b16_d7_p1000033.ms` | 1 | 27 | 35 | 8 | 15368 | 1000033 | True |
| `canon/wave5/ms/b16_d7_p1000039.ms` | 1 | 27 | 35 | 8 | 15368 | 1000039 | True |
| `canon/wave5/ms/b16_d7_q.ms` | 1 | 27 | 35 | 8 | 15362 | 0 | True |
| `canon/wave5/ms2/b16s_d9_Z_p1000003.ms` | 1 | 27 | 36 | 9 | 17049 | 1000003 | True |
| `canon/wave5/ms2/b16s_d9_Z_p1000033.ms` | 1 | 27 | 36 | 9 | 17049 | 1000033 | True |
| `canon/wave5/ms/b16_d8_p1000003.ms` | 1 | 30 | 39 | 9 | 21830 | 1000003 | True |
| `canon/wave5/ms/b16_d8_p1000033.ms` | 1 | 30 | 39 | 9 | 21830 | 1000033 | True |
| `canon/wave5/ms/b16_d8_p1000039.ms` | 1 | 30 | 39 | 9 | 21830 | 1000039 | True |
| `canon/wave5/ms/b16_d8_q.ms` | 1 | 30 | 39 | 9 | 21824 | 0 | True |
| `canon/wave5/ms2/b16s_d10_Z_p1000003.ms` | 1 | 30 | 40 | 10 | 23855 | 1000003 | True |
| `canon/wave5/ms2/b16s_d10_Z_p1000033.ms` | 1 | 30 | 40 | 10 | 23855 | 1000033 | True |
| `canon/wave5/ms2/b16s_d11_Z_p1000003.ms` | 1 | 33 | 44 | 11 | 32935 | 1000003 | True |
| `canon/wave5/ms2/b16s_d11_Z_p1000033.ms` | 1 | 33 | 44 | 11 | 32935 | 1000033 | True |
| `canon/wave5/ms2/d12seedZ_unsat.ms` | 1 | 34 | 46 | 12 | 43420 | 1000003 | False |
| `canon/wave5/ms2/b16r12seed_Z_p1000003.ms` | 1 | 35 | 47 | 12 | 43431 | 1000003 | True |
| `canon/wave5/ms2/b16r12seed_Z_p1000033.ms` | 1 | 35 | 47 | 12 | 43431 | 1000033 | True |
| `canon/wave5/ms2/b16r_d12_B_p1000003.ms` | 1 | 35 | 48 | 13 | 41431 | 1000003 | True |
| `canon/wave5/ms2/b16r_d12_B_p1000033.ms` | 1 | 35 | 48 | 13 | 41431 | 1000033 | True |
| `canon/wave5/ms2/b16r_d12_B_p1000039.ms` | 1 | 35 | 48 | 13 | 41431 | 1000039 | True |
| `canon/wave5/ms2/b16seed2_d12_Z_p1000003.ms` | 1 | 35 | 47 | 12 | 44265 | 1000003 | True |
| `canon/wave5/ms2/b16seed2_d12_Z_p1000033.ms` | 1 | 35 | 47 | 12 | 44265 | 1000033 | True |
| `canon/wave6/slice_mu3z_d13.ms` | 1 | 39 | 51 | 12 | 47770 | 1000003 | True |

## 5. The 20 smallest undecided systems with excess > 0

| # | system | n_vars | n_eqs | excess | torus | maxdeg | char | bytes |
|---|---|---|---|---|---|---|---|---|
| 1 | `canon/wave0/a6c_ms_empty_p65521.ms` | 7 | 8 | 1 | 0 | 12 | 65521 | 14224 |
| 2 | `canon/wave0/a6c_ms_empty_p65539.ms` | 7 | 8 | 1 | 0 | 12 | 65539 | 14236 |
| 3 | `canon/wave0/a6c_ms_empty_p65599.ms` | 7 | 8 | 1 | 0 | 12 | 65599 | 14244 |
| 4 | `canon/wave5/ms/u16_d3_q.ms` | 7 | 9 | 2 | 0 | 4 | 0 | 602 |
| 5 | `canon/wave5/ms2/ctl_d3seedZ_unsat.ms` | 7 | 10 | 3 | 1 | 4 | 1000003 | 465 |
| 6 | `canon/wave5/ms/c16_d5_r0_q.ms` | 7 | 14 | 7 | 0 | 21 | 0 | 110348 |
| 7 | `canon/wave5/ms/c16_d5_r1_q.ms` | 7 | 14 | 7 | 0 | 21 | 0 | 110349 |
| 8 | `canon/wave5/ms/c16_d5_r0_p1000003.ms` | 7 | 14 | 7 | 0 | 21 | 1000003 | 110354 |
| 9 | `canon/wave5/ms/c16_d5_r0_p1000033.ms` | 7 | 14 | 7 | 0 | 21 | 1000033 | 110354 |
| 10 | `canon/wave5/ms/c16_d5_r1_p1000003.ms` | 7 | 14 | 7 | 0 | 21 | 1000003 | 110355 |
| 11 | `canon/wave5/ms/c16_d5_r1_p1000033.ms` | 7 | 14 | 7 | 0 | 21 | 1000033 | 110355 |
| 12 | `canon/wave5/ms/m16_d3_q.ms` | 8 | 10 | 2 | 0 | 4 | 0 | 613 |
| 13 | `canon/wave5/ms/m16_d3_p1000003.ms` | 8 | 10 | 2 | 0 | 4 | 1000003 | 619 |
| 14 | `canon/wave5/ms/m16_d3_p1000033.ms` | 8 | 10 | 2 | 0 | 4 | 1000033 | 619 |
| 15 | `canon/wave5/ms2/ctl_d3seedZ_sat.ms` | 8 | 11 | 3 | 1 | 4 | 1000003 | 476 |
| 16 | `canon/wave5/ms2/b16seed2_d3_Z_p1000003.ms` | 8 | 11 | 3 | 1 | 4 | 1000003 | 493 |
| 17 | `canon/wave5/ms2/b16seed2_d3_Z_p1000033.ms` | 8 | 11 | 3 | 1 | 4 | 1000033 | 493 |
| 18 | `canon/wave5/ms/c16_d6_r1_q.ms` | 8 | 16 | 8 | 0 | 25 | 0 | 470965 |
| 19 | `canon/wave5/ms/c16_d6_r0_q.ms` | 8 | 16 | 8 | 0 | 25 | 0 | 470968 |
| 20 | `canon/wave5/ms/c16_d6_r1_p1000003.ms` | 8 | 16 | 8 | 0 | 25 | 1000003 | 470971 |

## 6. Timeout shapes

| quantity | value |
|---|---|
| raw failure records in logs (after de-mirroring identical log files) | 6414 |
| deduplicated shapes (all failure kinds) | 566 |
| deduplicated shapes, TIMEOUT/OOM/KILLED only | 318 |
| shapes resolvable to a registered system | 76 |

Archive claims found, all mutually inconsistent and none enumerated:

- `OPEN_ITEMS.md` / `wave6/CERTIFICATE_ROUTE.md`: **41** timeout shapes
- `AUDIT_EOD.md`: **33** virgin TIMEOUT shapes (+ a separate `(8,28) four`)
- `STATE_FULL.md`: **36** TIMEOUT
- `CATCHES.md`: **49** TIMEOUT records = **16** unique systems

## 7. Parse failures

- `canon/campaign/d23_borisov/d23_PR_data/msolve_output_raw.ms` -- line 2 is not a bare characteristic ('23,') -> msolve output, not an input system
- `canon/campaign/d23_borisov/ff_h_out.ms` -- line 2 is not a bare characteristic ('13,') -> msolve output, not an input system
- `hunt/campaign/d23_borisov/d23_PR_data/msolve_output_raw.ms` -- line 2 is not a bare characteristic ('23,') -> msolve output, not an input system
- `hunt/campaign/d23_borisov/ff_h_out.ms` -- line 2 is not a bare characteristic ('13,') -> msolve output, not an input system
- `mailbox/campaign/d23_borisov/d23_PR_data/msolve_output_raw.ms` -- line 2 is not a bare characteristic ('23,') -> msolve output, not an input system
- `mailbox/campaign/d23_borisov/ff_h_out.ms` -- line 2 is not a bare characteristic ('13,') -> msolve output, not an input system
- `p11/campaign/d23_borisov/d23_PR_data/msolve_output_raw.ms` -- line 2 is not a bare characteristic ('23,') -> msolve output, not an input system
- `p11/campaign/d23_borisov/ff_h_out.ms` -- line 2 is not a bare characteristic ('13,') -> msolve output, not an input system

## 8. Timeout shapes -- tiered, and the arithmetic that does not close

| tier | definition | count |
|---|---|---|
| A | shapes that resolve to a `.ms` file actually present in the register | 7 |
| B | A + shapes identified only by a name / sweep key / (n_vars,n_eqs) pair | 18 |
| C | B + free-prose failure mentions in narrative `.md` (not machine-identifiable) | 318 |
| raw | individual failure lines, after de-mirroring identical log files | 6414 |

**The '41 timeout shapes' is not reconstructible.** No file in any worktree enumerates
41 systems. The largest machine-identifiable set of TIMEOUT/OOM/kill shapes is **18**,
of which only **7** name a `.ms` export that exists on disk. Everything else is prose.
The four archive claims (41 / 36 / 33 / 49->16) come from four different scopes that were
never reconciled: 36 = the above-125 virgin sweep (`STATE_FULL.md` C), 33 = the same sweep
minus three later-decided cases (`AUDIT_EOD.md`), 49->16 = the wave6 hash-dedup of run
records (`CATCHES.md` 3), and 41 has no derivation anywhere. 33 + the separately-listed
`(8,28) four` = 37, not 41.

## 9. Method notes / caveats

- Torus rank is the nullspace dimension of the stacked monomial-difference matrix,
  computed by exact Gaussian elimination mod two 31-bit primes (agreement required
  whenever rank < n_vars). Rows capped at 4000 with early exit at full rank.
- Files > 5 MB (38 of them) are header-only: n_vars/characteristic parsed, n_eqs from a
  streaming top-level comma count, and `content_hash` is sha256 of the whitespace-stripped
  bytes (`hash_mode: raw_ws`) rather than the canonical form. Degree, torus rank and the
  Rabinowitsch scan are skipped there, so those 38 are NOT covered by section 4.
- The corpus is paren-free, verified corpus-wide, which is what makes the comma count safe.
- 8 `.ms` files are msolve *output*, not input systems (second line is not a characteristic).

