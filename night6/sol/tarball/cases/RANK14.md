# RANK14: degrees (112, 160)

**Verdict: UNCLEAR**  Conditional-pattern verdict: UNCLEAR.

Coverage: `conjectural_pattern` — Beyond the published <=150 inventory; conditional output of the disproved-as-universal trackD pattern.

Chain: `[{'x': {'numerator': 4, 'denominator': 1}, 'y': 12}, {'x': {'numerator': 7, 'denominator': 4}, 'y': 3}]`; `(m,n)=(7, 10)`.

Reduced target: `{'monomial': [2, 0], 'coefficient': 1}`. Emitted charts: 2.

## RANK14_c0_2_1 — UNCLEAR

`N(P)=[[0, 0], [2, 1], [28, 21], [28, 28]]`

`N(Q)=[[0, 0], [1, 0], [40, 30], [40, 40]]`

- weight `[1, -2]`: P face `[[0, 0], [2, 1]]`, Q face `[[1, 0]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 1, 'Q_degree': 0, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `-1*p_2_1*q_1_0 = 1`
- weight `[2, -3]`: P face `[[2, 1]]`, Q face `[[1, 0]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `-1*p_2_1*q_1_0 = 1`
- weight `[10, -13]`: P face `[[2, 1], [15, 11], [28, 21]]`, Q face `[[1, 0], [14, 10], [27, 20], [40, 30]]`; budget `5 vs 0`; UNSOLVED.
  Family: `{'kind': 'edge_ode', 'u_step': [13, 10], 'P_base': [2, 1], 'Q_base': [1, 0], 'degrees': [2, 3], 'normalized_equation': "p*q + beta*u*p'*q + gamma*u*p*q' = 1", 'beta': 10, 'gamma': -7, 'top_cancellation': 0, 'dimension_after_coefficient_scaling': 1, 'normalization': 'p(0)=q(0)=1 and leading(P)=1', 'residual_group_after_normalization': 'mu_2', 'weighted_cover_count': None, 'normalized_solution_count': None, 'checker': 'face_hurwitz_general.py'}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `-1*p_2_1*q_1_0 = 1`
  - coefficient `[15, 10]`: `6*p_2_1*q_14_10 + -11*p_15_11*q_1_0 = 0`
  - coefficient `[28, 20]`: `13*p_2_1*q_27_20 + -4*p_15_11*q_14_10 + -21*p_28_21*q_1_0 = 0`
  - coefficient `[41, 30]`: `20*p_2_1*q_40_30 + 3*p_15_11*q_27_20 + -14*p_28_21*q_14_10 = 0`
  - coefficient `[54, 40]`: `10*p_15_11*q_40_30 + -7*p_28_21*q_27_20 = 0`
## RANK14_c0_1_0 — KILLED

`N(P)=[[0, 0], [1, 0], [28, 21], [28, 28]]`

`N(Q)=[[0, 0], [2, 1], [40, 30], [40, 40]]`

- weight `[1, -2]`: P face `[[1, 0]]`, Q face `[[0, 0], [2, 1]]`; budget `1 vs 0`; SOLVED.
  Family: `{'kind': 'diagonal_edge_vertex', 'P_degree': 0, 'Q_degree': 1, 'solution': 'set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints', 'dimension_after_coefficient_scaling': 1}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `1*p_1_0*q_2_1 = 1`
- weight `[2, -3]`: P face `[[1, 0]]`, Q face `[[2, 1]]`; budget `0 vs 0`; SOLVED.
  Family: `{'kind': 'vertex_relation', 'dimension_after_coefficient_scaling': 0}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `1*p_1_0*q_2_1 = 1`
- weight `[29, -38]`: P face `[[1, 0]]`, Q face `[[2, 1], [40, 30]]`; budget `1 vs 1`; KILLED.
  Kill: coefficient `30` forces `p_1_0=0`; residues `{'999983': 30, '1000003': 30}`.
  Face coefficient rules:
  - coefficient `[2, 0]`: `1*p_1_0*q_2_1 = 1`
  - coefficient `[40, 29]`: `30*p_1_0*q_40_30 = 0`
