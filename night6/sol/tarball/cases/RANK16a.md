# RANK16a: degrees (100, 175)

**Verdict: UNCLEAR**  Conditional-pattern verdict: UNCLEAR.

Coverage: `conjectural_pattern` — Beyond the published <=150 inventory; conditional output of the disproved-as-universal trackD pattern.

Chain: `[{'x': {'numerator': 5, 'denominator': 1}, 'y': 20}, {'x': {'numerator': 7, 'denominator': 5}, 'y': 2}]`; `(m,n)=(4, 7)`.

Reduced target: `{'monomial': [3, 0], 'coefficient': 1}`. Emitted charts: 2.

## RANK16a_c0_3_1 — UNCLEAR

`N(P)=[[0, 0], [3, 1], [20, 8], [20, 12]]`

`N(Q)=[[0, 0], [1, 0], [35, 14], [35, 21]]`

- weight `[1, -3]`: P face `[[0, 0], [3, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
- weight `[2, -5]`: P face `[[3, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
- weight `[7, -17]`: P face `[[3, 1], [20, 8]]`, Q face `[[1, 0], [18, 7], [35, 14]]`; budget `3 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [17, 7], 'P_base': [3, 1], 'Q_base': [1, 0], 'degrees': [1, 2], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': 7, 'gamma': -4, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_1', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
  - coefficient `[20, 7]`: `3*p_3_1*q_18_7 + -8*p_20_8*q_1_0 = 0`
  - coefficient `[37, 14]`: `7*p_3_1*q_35_14 + -4*p_20_8*q_18_7 = 0`
## RANK16a_c0_1_0 — KILLED

`N(P)=[[0, 0], [1, 0], [20, 8], [20, 12]]`

`N(Q)=[[0, 0], [3, 1], [35, 14], [35, 21]]`

- weight `[1, -3]`: P face `[[1, 0]]`, Q face `[[0, 0], [3, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
- weight `[2, -5]`: P face `[[1, 0]]`, Q face `[[3, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
- weight `[13, -32]`: P face `[[1, 0]]`, Q face `[[3, 1], [35, 14]]`; budget `1 vs 1`; KILLED.
  Kill: coefficient `14` forces `p_1_0=0`; residues `{'999983': 14, '1000003': 14}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
  - coefficient `[35, 13]`: `14*p_1_0*q_35_14 = 0`
