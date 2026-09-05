# RANK15: degrees (99, 165)

**Verdict: UNCLEAR**  Conditional-pattern verdict: UNCLEAR.

Coverage: `conjectural_pattern` — Beyond the published <=150 inventory; conditional output of the disproved-as-universal trackD pattern.

Chain: `[{'x': {'numerator': 9, 'denominator': 1}, 'y': 24}, {'x': {'numerator': 10, 'denominator': 3}, 'y': 7}]`; `(m,n)=(3, 5)`.

Reduced target: `{'monomial': [1, 0], 'coefficient': 1}`. Emitted charts: 6.

## RANK15_c6_1_1 — UNCLEAR

`N(P)=[[0, 0], [1, 1], [9, 21], [9, 24], [0, 18]]`

`N(Q)=[[0, 0], [1, 0], [15, 35], [15, 40], [0, 30]]`

- weight `[1, -1]`: P face `[[0, 0], [1, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[2, -1]`: P face `[[1, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[5, -2]`: P face `[[1, 1], [3, 6], [5, 11], [7, 16], [9, 21]]`, Q face `[[1, 0], [3, 5], [5, 10], [7, 15], [9, 20], [11, 25], [13, 30], [15, 35]]`; budget `11 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [2, 5], 'P_base': [1, 1], 'Q_base': [1, 0], 'degrees': [4, 7], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': 5, 'gamma': -3, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_4', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
  - coefficient `[3, 5]`: `2*p_1_1*q_3_5 + -6*p_3_6*q_1_0 = 0`
  - coefficient `[5, 10]`: `5*p_1_1*q_5_10 + -3*p_3_6*q_3_5 + -11*p_5_11*q_1_0 = 0`
  - coefficient `[7, 15]`: `8*p_1_1*q_7_15 + -8*p_5_11*q_3_5 + -16*p_7_16*q_1_0 = 0`
  - coefficient `[9, 20]`: `11*p_1_1*q_9_20 + 3*p_3_6*q_7_15 + -5*p_5_11*q_5_10 + -13*p_7_16*q_3_5 + -21*p_9_21*q_1_0 = 0`
  - coefficient `[11, 25]`: `14*p_1_1*q_11_25 + 6*p_3_6*q_9_20 + -2*p_5_11*q_7_15 + -10*p_7_16*q_5_10 + -18*p_9_21*q_3_5 = 0`
  - coefficient `[13, 30]`: `17*p_1_1*q_13_30 + 9*p_3_6*q_11_25 + 1*p_5_11*q_9_20 + -7*p_7_16*q_7_15 + -15*p_9_21*q_5_10 = 0`
  - coefficient `[15, 35]`: `20*p_1_1*q_15_35 + 12*p_3_6*q_13_30 + 4*p_5_11*q_11_25 + -4*p_7_16*q_9_20 + -12*p_9_21*q_7_15 = 0`
  - coefficient `[17, 40]`: `15*p_3_6*q_15_35 + 7*p_5_11*q_13_30 + -1*p_7_16*q_11_25 + -9*p_9_21*q_9_20 = 0`
  - coefficient `[19, 45]`: `10*p_5_11*q_15_35 + 2*p_7_16*q_13_30 + -6*p_9_21*q_11_25 = 0`
  - coefficient `[21, 50]`: `5*p_7_16*q_15_35 + -3*p_9_21*q_13_30 = 0`
## RANK15_c6_1_0 — KILLED

`N(P)=[[0, 0], [1, 0], [9, 21], [9, 24], [0, 18]]`

`N(Q)=[[0, 0], [1, 1], [15, 35], [15, 40], [0, 30]]`

- weight `[1, -1]`: P face `[[1, 0]]`, Q face `[[0, 0], [1, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[2, -1]`: P face `[[1, 0]]`, Q face `[[1, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[17, -7]`: P face `[[1, 0]]`, Q face `[[1, 1], [8, 18], [15, 35]]`; budget `2 vs 2`; KILLED.
  Kill: coefficient `35` forces `p_1_0=0`; residues `{'999983': 35, '1000003': 35}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
  - coefficient `[8, 17]`: `18*p_1_0*q_8_18 = 0`
  - coefficient `[15, 34]`: `35*p_1_0*q_15_35 = 0`
## RANK15_c3_1_1 — UNCLEAR

`N(P)=[[0, 0], [1, 1], [9, 21], [9, 24], [0, 9]]`

`N(Q)=[[0, 0], [1, 0], [15, 35], [15, 40], [0, 15]]`

- weight `[1, -1]`: P face `[[0, 0], [1, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[2, -1]`: P face `[[1, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[5, -3]`: P face `[[1, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[5, -2]`: P face `[[1, 1], [3, 6], [5, 11], [7, 16], [9, 21]]`, Q face `[[1, 0], [3, 5], [5, 10], [7, 15], [9, 20], [11, 25], [13, 30], [15, 35]]`; budget `11 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [2, 5], 'P_base': [1, 1], 'Q_base': [1, 0], 'degrees': [4, 7], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': 5, 'gamma': -3, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_4', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
  - coefficient `[3, 5]`: `2*p_1_1*q_3_5 + -6*p_3_6*q_1_0 = 0`
  - coefficient `[5, 10]`: `5*p_1_1*q_5_10 + -3*p_3_6*q_3_5 + -11*p_5_11*q_1_0 = 0`
  - coefficient `[7, 15]`: `8*p_1_1*q_7_15 + -8*p_5_11*q_3_5 + -16*p_7_16*q_1_0 = 0`
  - coefficient `[9, 20]`: `11*p_1_1*q_9_20 + 3*p_3_6*q_7_15 + -5*p_5_11*q_5_10 + -13*p_7_16*q_3_5 + -21*p_9_21*q_1_0 = 0`
  - coefficient `[11, 25]`: `14*p_1_1*q_11_25 + 6*p_3_6*q_9_20 + -2*p_5_11*q_7_15 + -10*p_7_16*q_5_10 + -18*p_9_21*q_3_5 = 0`
  - coefficient `[13, 30]`: `17*p_1_1*q_13_30 + 9*p_3_6*q_11_25 + 1*p_5_11*q_9_20 + -7*p_7_16*q_7_15 + -15*p_9_21*q_5_10 = 0`
  - coefficient `[15, 35]`: `20*p_1_1*q_15_35 + 12*p_3_6*q_13_30 + 4*p_5_11*q_11_25 + -4*p_7_16*q_9_20 + -12*p_9_21*q_7_15 = 0`
  - coefficient `[17, 40]`: `15*p_3_6*q_15_35 + 7*p_5_11*q_13_30 + -1*p_7_16*q_11_25 + -9*p_9_21*q_9_20 = 0`
  - coefficient `[19, 45]`: `10*p_5_11*q_15_35 + 2*p_7_16*q_13_30 + -6*p_9_21*q_11_25 = 0`
  - coefficient `[21, 50]`: `5*p_7_16*q_15_35 + -3*p_9_21*q_13_30 = 0`
## RANK15_c3_1_0 — KILLED

`N(P)=[[0, 0], [1, 0], [9, 21], [9, 24], [0, 9]]`

`N(Q)=[[0, 0], [1, 1], [15, 35], [15, 40], [0, 15]]`

- weight `[1, -1]`: P face `[[1, 0]]`, Q face `[[0, 0], [1, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[2, -1]`: P face `[[1, 0]]`, Q face `[[1, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[5, -3]`: P face `[[1, 0]]`, Q face `[[1, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[17, -7]`: P face `[[1, 0]]`, Q face `[[1, 1], [8, 18], [15, 35]]`; budget `2 vs 2`; KILLED.
  Kill: coefficient `35` forces `p_1_0=0`; residues `{'999983': 35, '1000003': 35}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
  - coefficient `[8, 17]`: `18*p_1_0*q_8_18 = 0`
  - coefficient `[15, 34]`: `35*p_1_0*q_15_35 = 0`
## RANK15_c0_1_1 — UNCLEAR

`N(P)=[[0, 0], [1, 1], [9, 21], [9, 24]]`

`N(Q)=[[0, 0], [1, 0], [15, 35], [15, 40]]`

- weight `[1, -1]`: P face `[[0, 0], [1, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[2, -1]`: P face `[[1, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
- weight `[5, -2]`: P face `[[1, 1], [3, 6], [5, 11], [7, 16], [9, 21]]`, Q face `[[1, 0], [3, 5], [5, 10], [7, 15], [9, 20], [11, 25], [13, 30], [15, 35]]`; budget `11 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [2, 5], 'P_base': [1, 1], 'Q_base': [1, 0], 'degrees': [4, 7], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': 5, 'gamma': -3, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_4', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `-1*p_1_1*q_1_0 = 1`
  - coefficient `[3, 5]`: `2*p_1_1*q_3_5 + -6*p_3_6*q_1_0 = 0`
  - coefficient `[5, 10]`: `5*p_1_1*q_5_10 + -3*p_3_6*q_3_5 + -11*p_5_11*q_1_0 = 0`
  - coefficient `[7, 15]`: `8*p_1_1*q_7_15 + -8*p_5_11*q_3_5 + -16*p_7_16*q_1_0 = 0`
  - coefficient `[9, 20]`: `11*p_1_1*q_9_20 + 3*p_3_6*q_7_15 + -5*p_5_11*q_5_10 + -13*p_7_16*q_3_5 + -21*p_9_21*q_1_0 = 0`
  - coefficient `[11, 25]`: `14*p_1_1*q_11_25 + 6*p_3_6*q_9_20 + -2*p_5_11*q_7_15 + -10*p_7_16*q_5_10 + -18*p_9_21*q_3_5 = 0`
  - coefficient `[13, 30]`: `17*p_1_1*q_13_30 + 9*p_3_6*q_11_25 + 1*p_5_11*q_9_20 + -7*p_7_16*q_7_15 + -15*p_9_21*q_5_10 = 0`
  - coefficient `[15, 35]`: `20*p_1_1*q_15_35 + 12*p_3_6*q_13_30 + 4*p_5_11*q_11_25 + -4*p_7_16*q_9_20 + -12*p_9_21*q_7_15 = 0`
  - coefficient `[17, 40]`: `15*p_3_6*q_15_35 + 7*p_5_11*q_13_30 + -1*p_7_16*q_11_25 + -9*p_9_21*q_9_20 = 0`
  - coefficient `[19, 45]`: `10*p_5_11*q_15_35 + 2*p_7_16*q_13_30 + -6*p_9_21*q_11_25 = 0`
  - coefficient `[21, 50]`: `5*p_7_16*q_15_35 + -3*p_9_21*q_13_30 = 0`
## RANK15_c0_1_0 — KILLED

`N(P)=[[0, 0], [1, 0], [9, 21], [9, 24]]`

`N(Q)=[[0, 0], [1, 1], [15, 35], [15, 40]]`

- weight `[1, -1]`: P face `[[1, 0]]`, Q face `[[0, 0], [1, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[2, -1]`: P face `[[1, 0]]`, Q face `[[1, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
- weight `[17, -7]`: P face `[[1, 0]]`, Q face `[[1, 1], [8, 18], [15, 35]]`; budget `2 vs 2`; KILLED.
  Kill: coefficient `35` forces `p_1_0=0`; residues `{'999983': 35, '1000003': 35}`.
  Face coefficient rules:
  - coefficient `[1, 0]`: `1*p_1_0*q_1_1 = 1`
  - coefficient `[8, 17]`: `18*p_1_0*q_8_18 = 0`
  - coefficient `[15, 34]`: `35*p_1_0*q_15_35 = 0`
