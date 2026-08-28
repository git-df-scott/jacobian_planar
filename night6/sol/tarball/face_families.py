#!/usr/bin/env python3
"""Emit explicit normalized coordinates for every edge-ODE survivor type."""
import json
from pathlib import Path
import sympy as sp

TYPES = {
    "T1": (2, 3, 4, -3, 2, 4),
    "T2": (2, 3, 7, -5, 2, 4),
    "T3": (1, 2, 3, -2, 1, 1),
    "T4": (1, 2, 5, -3, 1, 1),
    "T5": (3, 4, -3, 2, 1, 3),
    "T6": (1, 4, 7, -2, 1, 1),
    "T7": (2, 5, 7, -3, 3, 6),
    "T8": (5, 8, 3, -2, 2, 10),
    "T9": (7, 10, -3, 2, 5, 35),
}


def family(dp, dq, beta, gamma, covers, points):
    u = sp.symbols("u")
    pvars = list(sp.symbols(f"p1:{dp}"))
    p = 1 + sum(pvars[i-1]*u**i for i in range(1, dp)) + u**dp
    qcoeff = [sp.Integer(1)]
    for n in range(1, dq+1):
        z = sp.symbols("z")
        qpartial = sum(qcoeff[j]*u**j for j in range(n)) + z*u**n
        W = sp.Poly(sp.expand(p*qpartial + beta*u*sp.diff(p,u)*qpartial
                             + gamma*u*p*sp.diff(qpartial,u) - 1), u)
        qcoeff.append(sp.factor(sp.solve(W.coeff_monomial(u**n), z)[0]))
    q = sum(qcoeff[j]*u**j for j in range(dq+1))
    W = sp.Poly(sp.expand(p*q + beta*u*sp.diff(p,u)*q
                         + gamma*u*p*sp.diff(q,u) - 1), u)
    residual = [sp.factor(W.coeff_monomial(u**n))
                for n in range(dq+1, dp+dq)]
    return {
        "degrees": [dp,dq], "beta": beta, "gamma": gamma,
        "normalization": {"p_0":1,"q_0":1,f"p_{dp}":1},
        "p": str(p),
        "q_coefficients": {f"q_{j}":str(qcoeff[j]) for j in range(1,dq+1)},
        "residual_equations": [str(e)+" = 0" for e in residual],
        "top_identity": 1+beta*dp+gamma*dq,
        "dimension_before_u_normalization": 1,
        "residual_group": f"mu_{dp}",
        "weighted_cover_count": covers,
        "normalized_geometric_points_counted_with_mu": points,
        "existence_checker": "face_hurwitz_general.py"
    }


data={name:family(*args) for name,args in TYPES.items()}
Path("face_families.json").write_text(json.dumps(data,indent=2)+"\n")
print("PASS: emitted",len(data),"explicit normalized face families")
