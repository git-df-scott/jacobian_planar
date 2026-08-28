# night1 OVERNIGHT LOG

Executor log. Records only.

controls: CONTROLS: PASS

## n1_moderate

- csv: night1/results/n1_moderate.csv
- rows written: 320
- wall-clock: 4 s

10 deepest cells with calibrated=0:

| F | g | d | p | depth | status | indep_check |
|---|---|---|---|---|---|---|
| Fa | u^1v^2 | 18 | 999983 | 10 | obstructed@11:degree-overflow | PASS |
| Fa | u^1v^2 | 18 | 1000003 | 10 | obstructed@11:degree-overflow | PASS |
| Fa | u^1v^2 | 14 | 999983 | 8 | obstructed@9:degree-overflow | PASS |
| Fa | u^1v^2 | 14 | 1000003 | 8 | obstructed@9:degree-overflow | PASS |
| Fc | u^1v^2 | 18 | 999983 | 7 | obstructed@8:degree-overflow |  |
| Fc | u^1v^2 | 18 | 1000003 | 7 | obstructed@8:degree-overflow |  |
| Fa | u^1v^2 | 10 | 999983 | 6 | obstructed@7:degree-overflow |  |
| Fa | u^1v^2 | 10 | 1000003 | 6 | obstructed@7:degree-overflow |  |
| Fb | u^2v^1 | 18 | 999983 | 6 | obstructed@7:inconsistent |  |
| Fb | u^2v^1 | 18 | 1000003 | 6 | obstructed@7:inconsistent |  |

Prime agreement on the depth of those cells: AGREE (999983 vs 1000003, over the 5 distinct (F,g,d) cells listed).


## n2_deepcaps

- csv: night1/results/n2_deepcaps.csv
- rows written: 486
- wall-clock: 41 s

10 deepest cells with calibrated=0:

| F | g | d | p | depth | status | indep_check |
|---|---|---|---|---|---|---|
| Fa | u^1v^2 | 30 | 999983 | 16 | survived | PASS |
| Fa | u^1v^2 | 30 | 1000003 | 16 | survived | PASS |
| Fa | u^1v^2 | 26 | 999983 | 14 | obstructed@15:degree-overflow | PASS |
| Fa | u^1v^2 | 26 | 1000003 | 14 | obstructed@15:degree-overflow | PASS |
| Fa | u^1v^2 | 22 | 999983 | 12 | obstructed@13:degree-overflow | PASS |
| Fa | u^1v^2 | 22 | 1000003 | 12 | obstructed@13:degree-overflow | PASS |
| Fc | u^1v^2 | 30 | 999983 | 11 | obstructed@12:degree-overflow | PASS |
| Fc | u^1v^2 | 30 | 1000003 | 11 | obstructed@12:degree-overflow | PASS |
| Fc | u^1v^2 | 26 | 999983 | 10 | obstructed@11:degree-overflow | PASS |
| Fc | u^1v^2 | 26 | 1000003 | 10 | obstructed@11:degree-overflow | PASS |

Prime agreement on the depth of those cells: AGREE (999983 vs 1000003, over the 5 distinct (F,g,d) cells listed).


## n3_identity_baseline

- csv: night1/results/n3_identity_baseline.csv
- rows written: 352
- wall-clock: 1 s

10 deepest cells with calibrated=0:

| F | g | d | p | depth | status | indep_check |
|---|---|---|---|---|---|---|
| Fid | u^1v^2 | 20 | 999983 | 16 | survived | PASS |
| Fid | u^1v^2 | 20 | 1000003 | 16 | survived | PASS |
| Fid | u^2v^1 | 20 | 999983 | 16 | survived | PASS |
| Fid | u^2v^1 | 20 | 1000003 | 16 | survived | PASS |
| Fid | u^1v^2 | 16 | 999983 | 15 | obstructed@16:degree-overflow | PASS |
| Fid | u^1v^2 | 16 | 1000003 | 15 | obstructed@16:degree-overflow | PASS |
| Fid | u^2v^1 | 16 | 999983 | 15 | obstructed@16:degree-overflow | PASS |
| Fid | u^2v^1 | 16 | 1000003 | 15 | obstructed@16:degree-overflow | PASS |
| Fid | u^1v^2 | 12 | 999983 | 11 | obstructed@12:degree-overflow | PASS |
| Fid | u^1v^2 | 12 | 1000003 | 11 | obstructed@12:degree-overflow | PASS |

Prime agreement on the depth of those cells: AGREE (999983 vs 1000003, over the 5 distinct (F,g,d) cells listed).


## end of night1 run

All three specs completed. controls: PASS. Total rows: 1158 (320 + 486 + 352).
