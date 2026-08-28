# RANK16b: degrees (175, 125)

**Verdict: UNCLEAR**  Conditional-pattern verdict: UNCLEAR.

Coverage: `conjectural_pattern` — Beyond the published <=150 inventory; conditional output of the disproved-as-universal trackD pattern.

Chain: `[{'x': {'numerator': 5, 'denominator': 1}, 'y': 20}, {'x': {'numerator': 8, 'denominator': 5}, 'y': 3}]`; `(m,n)=(7, 5)`.

Reduced target: `{'monomial': [3, 0], 'coefficient': 1}`. Emitted charts: 2.

## RANK16b_c0_3_1 — KILLED

`N(P)=[[0, 0], [3, 1], [25, 15], [25, 20]]`

`N(Q)=[[0, 0], [1, 0], [35, 21], [35, 28]]`

- weight `[1, -3]`: P face `[[0, 0], [3, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
- weight `[1, -2]`: P face `[[3, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
- weight `[21, -34]`: P face `[[3, 1]]`, Q face `[[1, 0], [35, 21]]`; budget `1 vs 1`; KILLED.
  Kill: coefficient `28` forces `p_3_1=0`; residues `{'999983': 28, '1000003': 28}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `-1*p_3_1*q_1_0 = 1`
  - coefficient `[37, 21]`: `28*p_3_1*q_35_21 = 0`
## RANK16b_c0_1_0 — UNCLEAR

`N(P)=[[0, 0], [1, 0], [25, 15], [25, 20]]`

`N(Q)=[[0, 0], [3, 1], [35, 21], [35, 28]]`

- weight `[1, -3]`: P face `[[1, 0]]`, Q face `[[0, 0], [3, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
- weight `[1, -2]`: P face `[[1, 0]]`, Q face `[[3, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
- weight `[5, -8]`: P face `[[1, 0], [9, 5], [17, 10], [25, 15]]`, Q face `[[3, 1], [11, 6], [19, 11], [27, 16], [35, 21]]`; budget `7 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [8, 5], 'P_base': [1, 0], 'Q_base': [3, 1], 'degrees': [3, 4], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': -7, 'gamma': 5, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_3', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[3, 0]`: `1*p_1_0*q_3_1 = 1`
  - coefficient `[11, 5]`: `6*p_1_0*q_11_6 + -6*p_9_5*q_3_1 = 0`
  - coefficient `[19, 10]`: `11*p_1_0*q_19_11 + -1*p_9_5*q_11_6 + -13*p_17_10*q_3_1 = 0`
  - coefficient `[27, 15]`: `16*p_1_0*q_27_16 + 4*p_9_5*q_19_11 + -8*p_17_10*q_11_6 + -20*p_25_15*q_3_1 = 0`
  - coefficient `[35, 20]`: `21*p_1_0*q_35_21 + 9*p_9_5*q_27_16 + -3*p_17_10*q_19_11 + -15*p_25_15*q_11_6 = 0`
  - coefficient `[43, 25]`: `14*p_9_5*q_35_21 + 2*p_17_10*q_27_16 + -10*p_25_15*q_19_11 = 0`
  - coefficient `[51, 30]`: `7*p_17_10*q_35_21 + -5*p_25_15*q_27_16 = 0`
