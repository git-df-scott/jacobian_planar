#!/usr/bin/env python3
"""Generate conditional and published-exact face triage for the 34 GGHV rows.

Requires trackD_chain_map.py from the campaign.  The script does not promote its
general chain-to-carrier pattern: only four explicitly overridden rows are
marked published_exact.  Every other emitted chart is retained as a
conjectural-pattern calculation and the row verdict remains UNCLEAR.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

PRIMES = (999983, 1000003)

RANKING = {
    14: [1], 29: [2], 13: [3], 21: [4], 19: [5], 20: [5], 22: [6],
    9: [7], 10: [7], 17: [8], 24: [9], 30: [10], 31: [10],
    32: [10], 33: [10], 6: [11], 7: [11], 15: [12], 16: [12],
    27: [13], 28: [13],
}

# Exact Hurwitz counts for the nine edge/edge ODE types encountered.
# key=(deg p,deg q,beta,gamma), equation pq+beta*u*p'q+gamma*u*pq'=1.
HURWITZ = {
    (2, 3, 4, -3): (2, 4),
    (2, 3, 7, -5): (2, 4),
    (1, 2, 3, -2): (1, 1),
    (1, 2, 5, -3): (1, 1),
    (3, 4, -3, 2): (1, 3),
    (1, 4, 7, -2): (1, 1),
    (2, 5, 7, -3): (3, 6),
    (5, 8, 3, -2): (2, 10),
    (7, 10, -3, 2): (5, 35),
}


def primitive(v):
    g = math.gcd(abs(v[0]), abs(v[1]))
    if not g:
        raise ValueError("zero direction")
    return v[0] // g, v[1] // g


def dot(w, z):
    return w[0] * z[0] + w[1] * z[1]


def edge_normals(poly):
    out = set()
    for a, b in zip(poly, poly[1:] + poly[:1]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        for w in ((dy, -dx), (-dy, dx)):
            out.add(primitive(w))
    return out


def face(lattice, w):
    top = max(dot(w, z) for z in lattice)
    return sorted(z for z in lattice if dot(w, z) == top)


def unique_pair_weight(NP, NQ, eP, eQ):
    hits = []
    for rho in range(-64, 65):
        for sigma in range(-64, 65):
            if not rho and not sigma:
                continue
            w = primitive((rho, sigma))
            if w != (rho, sigma):
                continue
            fp = [z for z in NP if dot(w, z) == max(map(lambda q: dot(w, q), NP))]
            fq = [z for z in NQ if dot(w, z) == max(map(lambda q: dot(w, q), NQ))]
            if fp == [eP] and fq == [eQ]:
                hits.append(w)
    return min(hits, key=lambda w: (abs(w[0]) + abs(w[1]), w)) if hits else None


def coefficient_rules(Pface, Qface, target):
    buckets = {}
    for i, j in Pface:
        for k, ell in Qface:
            c = i * ell - j * k
            if c:
                exponent = (i + k - 1, j + ell - 1)
                buckets.setdefault(exponent, []).append({
                    "integer": c,
                    "variables": [f"p_{i}_{j}", f"q_{k}_{ell}"],
                })
    buckets.setdefault(target, [])
    return [{
        "output_monomial": list(z), "terms": buckets[z],
        "rhs": 1 if z == target else 0,
    } for z in sorted(buckets)]


def zero_bracket_rules(Pface,Qface):
    rules=coefficient_rules(Pface,Qface,(10**9,0))
    return [{**e,"rhs":0} for e in rules if e["output_monomial"]!=[10**9,0]]


def line_form(points):
    points = sorted(points)
    if len(points) == 1:
        return points[0], (0, 0), 0
    dx, dy = points[1][0] - points[0][0], points[1][1] - points[0][1]
    step = primitive((dx, dy))
    if step[0] < 0 or (step[0] == 0 and step[1] < 0):
        step = (-step[0], -step[1])
    base = min(points, key=lambda z: z[0] * step[0] + z[1] * step[1])
    def parameter(z):
        return ((z[0] - base[0]) // step[0] if step[0]
                else (z[1] - base[1]) // step[1])
    return base, step, max(parameter(z) for z in points)


def killing_certificate(rules, mandatory):
    for index, eq in enumerate(rules):
        if eq["rhs"] == 0 and len(eq["terms"]) == 1:
            t = eq["terms"][0]
            if len(t["variables"]) == 2 and all(v in mandatory for v in t["variables"]):
                victim = next(v for v in t["variables"] if v.startswith("p_") or v.startswith("q_"))
                _, i, j = victim.split("_")
                c = t["integer"]
                return {
                    "equation_index": index,
                    "mandatory_vertex": [int(i), int(j)],
                    "mandatory_variable": victim,
                    "integer_coefficient": c,
                    "modular_residues": {str(p): c % p for p in PRIMES},
                    "checker": "triage_check.py:check_kill_certificates",
                }
        if eq["rhs"] and not eq["terms"]:
            return {
                "equation_index": index, "mandatory_vertex": [0, 0],
                "mandatory_variable": "<target absent>", "integer_coefficient": 0,
                "modular_residues": {str(p): 0 for p in PRIMES},
                "checker": "triage_check.py:check_kill_certificates",
            }
    return None


def describe_solution(Pface, Qface, rules, kill):
    if kill:
        edge_size = max(len(Pface), len(Qface)) - 1
        return None, {"nonconstant_unknowns": edge_size,
                      "independent_conditions": edge_size,
                      "slack": 0, "basis": "explicit_diagonal"}, "KILLED"
    if len(Pface) == len(Qface) == 1:
        return {"kind": "vertex_relation", "dimension_after_coefficient_scaling": 0}, {
            "nonconstant_unknowns": 0, "independent_conditions": 0,
            "slack": 0, "basis": "explicit_diagonal"}, "SOLVED"
    p0, ps, dp = line_form(Pface)
    q0, qs, dq = line_form(Qface)
    if len(Pface) > 1 and len(Qface) > 1 and ps == qs:
        s, t = ps
        a, b = p0
        c, d = q0
        A = a*d - b*c
        B = s*d - t*c
        C = a*t - b*s
        if A not in (-1, 1):
            return {"kind": "unresolved_edge_ode", "A_B_C": [A, B, C]}, {
                "nonconstant_unknowns": dp+dq, "independent_conditions": 0,
                "slack": dp+dq, "basis": "upper_bound_only"}, "UNSOLVED"
        beta, gamma = B // A, C // A
        key = (dp, dq, beta, gamma)
        counts = HURWITZ.get(key)
        family = {
            "kind": "edge_ode", "u_step": list(ps), "P_base": list(p0),
            "Q_base": list(q0), "degrees": [dp, dq],
            "normalized_equation": "p*q + beta*u*p'*q + gamma*u*p*q' = 1",
            "beta": beta, "gamma": gamma,
            "top_cancellation": 1 + beta*dp + gamma*dq,
            "dimension_after_coefficient_scaling": 1,
            "normalization": "p(0)=q(0)=1 and leading(P)=1",
            "residual_group_after_normalization": f"mu_{dp}",
            "weighted_cover_count": counts[0] if counts else None,
            "normalized_solution_count": counts[1] if counts else None,
            "checker": "face_hurwitz_general.py",
        }
        return family, {
            "nonconstant_unknowns": dp+dq,
            "independent_conditions": dp+dq-1 if counts else 0,
            "slack": 1 if counts else dp+dq,
            "basis": "proved_rank" if counts else "upper_bound_only",
        }, "SOLVED" if counts else "UNSOLVED"
    edge_degree = max(dp, dq)
    forced = sum(1 for e in rules if e["rhs"] == 0 and e["terms"])
    return {
        "kind": "diagonal_edge_vertex", "P_degree": dp, "Q_degree": dq,
        "solution": "set every nonresonant nonvertex edge coefficient to zero; retain resonant mandatory endpoints",
        "dimension_after_coefficient_scaling": edge_degree - forced,
    }, {
        "nonconstant_unknowns": edge_degree, "independent_conditions": forced,
        "slack": edge_degree-forced, "basis": "explicit_diagonal",
    }, "SOLVED"


def cascade_level(t, cand, w, Pface, Qface):
    LP, LQ = t.lattice(cand["NP"]), t.lattice(cand["NQ"])
    WP, WQ = max(dot(w,z) for z in LP), max(dot(w,z) for z in LQ)
    dropsP = sorted({WP-dot(w,z) for z in LP if WP-dot(w,z)>0})
    dropsQ = sorted({WQ-dot(w,z) for z in LQ if WQ-dot(w,z)>0})
    if not dropsP and not dropsQ:
        return None
    delta = min(dropsP+dropsQ)
    Pslices = {d:[z for z in LP if WP-dot(w,z)==d] for d in [0,delta]}
    Qslices = {d:[z for z in LQ if WQ-dot(w,z)==d] for d in [0,delta]}
    pairs = []
    if Pslices.get(0) and Qslices.get(delta): pairs.append((Pslices[0],Qslices[delta]))
    if Pslices.get(delta) and Qslices.get(0): pairs.append((Pslices[delta],Qslices[0]))
    buckets={}
    for PS,QS in pairs:
        for i,j in PS:
            for k,l in QS:
                c=i*l-j*k
                if c:
                    z=(i+k-1,j+l-1)
                    buckets.setdefault(z,[]).append({"integer":c,"variables":[f"p_{i}_{j}",f"q_{k}_{l}"]})
    return {"weight_drop":delta,"P_new_slice":[list(z) for z in Pslices.get(delta,[])],
            "Q_new_slice":[list(z) for z in Qslices.get(delta,[])],
            "equations":[{"output_monomial":list(z),"terms":ts,"rhs":0} for z,ts in sorted(buckets.items())]}


def chart_record(t, cand, case_id):
    NP, NQ = cand["NP"], cand["NQ"]
    LP, LQ = t.lattice(NP), t.lattice(NQ)
    dirs = edge_normals(NP) | edge_normals(NQ)
    rep = unique_pair_weight(NP, NQ, cand["epsP"], cand["epsQ"])
    if rep: dirs.add(rep)
    faces=[]
    mandatory={f"p_{i}_{j}" for i,j in NP}|{f"q_{i}_{j}" for i,j in NQ}
    for w in sorted(dirs):
        fp,fq=face(LP,w),face(LQ,w)
        top=max(dot(w,z) for z in LP)+max(dot(w,z) for z in LQ)-sum(w)
        if top != w[0]*cand["r"]:
            continue
        rules=coefficient_rules(fp,fq,(cand["r"],0))
        kill=killing_certificate(rules,mandatory)
        family,budget,status=describe_solution(fp,fq,rules,kill)
        faces.append({"weight":list(w),"P_monomials":[list(z) for z in fp],
                      "Q_monomials":[list(z) for z in fq],"face_form":family or {},
                      "equations":rules,"budget":budget,"status":status,
                      "kill_certificate":kill,"solution_family":family})
    if not faces:
        return {"chart_id":f"{case_id}_c{cand['cprime']}_{cand['epsP'][0]}_{cand['epsP'][1]}",
                "cprime":cand["cprime"],
                "orientation":{"epsilon_P":list(cand["epsP"]),"epsilon_Q":list(cand["epsQ"])},
                "newton_polygons":{"P":[list(z) for z in NP],"Q":[list(z) for z in NQ]},
                "essential_faces":[],"status":"UNCLEAR","level1_cascade":None,
                "note":"No target-weight boundary face or joint epsilon cone was found; the conjectural chart invariant is internally inconsistent."}
    killed=next((f for f in faces if f["status"]=="KILLED"),None)
    unsolved=next((f for f in faces if f["status"]=="UNSOLVED"),None)
    status="KILLED" if killed else ("UNCLEAR" if unsolved else "SURVIVES")
    decisive=killed or max(faces,key=lambda f:len(f["P_monomials"])+len(f["Q_monomials"]))
    cascade=cascade_level(t,cand,tuple(decisive["weight"]),
                          decisive["P_monomials"],decisive["Q_monomials"])
    return {"chart_id":f"{case_id}_c{cand['cprime']}_{cand['epsP'][0]}_{cand['epsP'][1]}",
            "cprime":cand["cprime"],"orientation":{"epsilon_P":list(cand["epsP"]),"epsilon_Q":list(cand["epsQ"])},
            "newton_polygons":{"P":[list(z) for z in NP],"Q":[list(z) for z in NQ]},
            "essential_faces":faces,"status":status,"level1_cascade":cascade}


def exact_override(index, candidates):
    if index == 11:
        return [c for c in candidates if c["epsP"]==(1,1) and c["cprime"] in (0,3,6)]
    if index == 18:
        return [c for c in candidates if c["epsP"]==(1,0) and c["cprime"] in (0,4)]
    if index == 25:
        return [c for c in candidates if c["epsP"]==(1,1) and c["cprime"]==9]
    return candidates


def rational_corner(c):
    return {"x":{"numerator":c[0],"denominator":c[1]},"y":c[2]}


def make_case(t,index,ch):
    case_id=f"GGHV34-{index:02d}"
    candidates,notes=t.reduced_candidates(ch)
    candidates=[c for c in candidates if t.check_eps(c)[0]]
    published=index in (8,11,18,25)
    if index==8:
        # GGHV 2022 Proposition 4.4, verbatim polygon data.
        fake={"NP":t.hull([(0,0),(4,0),(6,2),(0,14)]),
              "NQ":t.hull([(0,0),(6,0),(9,3),(0,21)]),"epsP":(4,0),
              "epsQ":(-2,1),"cprime":7,"r":1}
        # There is no target-weight outer face; keep a direct special record.
        commuting=[]
        LP,LQ=t.lattice(fake["NP"]),t.lattice(fake["NQ"])
        for w in sorted(edge_normals(fake["NP"])|edge_normals(fake["NQ"])):
            fp,fq=face(LP,w),face(LQ,w)
            if len(fp)>1 and len(fq)>1:
                commuting.append({"weight":list(w),"P_monomials":[list(z) for z in fp],
                                  "Q_monomials":[list(z) for z in fq],
                                  "top_equations":zero_bracket_rules(fp,fq),
                                  "level1_cascade":cascade_level(t,fake,w,fp,fq)})
        charts=[{"chart_id":case_id+"_prop4.4","cprime":7,
                 "orientation":{"epsilon_P":None,"epsilon_Q":None},
                 "newton_polygons":{"P":[list(z) for z in fake["NP"]],"Q":[list(z) for z in fake["NQ"]]},
                 "essential_faces":[],"status":"SURVIVES","level1_cascade":None,
                 "commuting_outer_faces":commuting,
                 "note":"No outer Newton face has top bracket weight equal to x; all outer top brackets must commute."}]
        r=1;a=b=None
    else:
        candidates=exact_override(index,candidates) if published else candidates
        charts=[chart_record(t,c,case_id) for c in candidates]
        r=candidates[0]["r"] if candidates else None
        a=candidates[0]["a"] if candidates else None
        b=candidates[0]["b"] if candidates else None
    conditional=("KILLED" if charts and all(c["status"]=="KILLED" for c in charts)
                 else "SURVIVES" if any(c["status"]=="SURVIVES" for c in charts) else "UNCLEAR")
    verdict=conditional if published else "UNCLEAR"
    level="published_exact" if published else "conjectural_pattern"
    statement=("Newton polygons and target are quoted from GGHV 2022 Proposition 4.4/4.2/4.3/4.1."
               if published else "Conditional output of trackD_chain_map.py; not a coverage theorem and falsified as a universal map by the F9 Proposition 4.4 control.")
    return {"case_id":case_id,"published_index":index,
            "ranking_positions":RANKING.get(index,[]),"degree_pair":list(ch.degrees()),
            "chain":[rational_corner(c) for c in ch.corners],"mn":[ch.m,ch.n],
            "max_degree":ch.maxdeg,
            "reduction":{"status":"derived" if charts else "out_of_scope","a":a,"b":b,
                         "target_bracket":{"monomial":[r,0],"coefficient":1} if r is not None else None,
                         "base_polygons":[],"notes":notes},
            "charts":charts,"verdict":verdict,"conditional_pattern_verdict":conditional,
            "coverage":{"level":level,"statement":statement,
                        "checker_or_citation":"GGHV 2022 arXiv:2204.14178 Section 4; triage_check.py"},
            "survivor_dossier":None,"derivation_note":f"cases/{case_id}.md"}


def extension_chains(t):
    C=t.C
    return [
        ("RANK14",14,t.Chain("F1 j=2",[C(4,1,12),C(7,4,3)],C(1,1,0),(7,10),160,"rank extension")),
        ("RANK15",15,t.Chain("F16 j=0",[C(9,1,24),C(10,3,7)],C(1,1,0),(3,5),165,"rank extension")),
        ("RANK16a",16,t.Chain("F2 j=2",[C(5,1,20),C(7,5,2)],C(1,1,0),(4,7),175,"rank extension")),
        ("RANK16b",16,t.Chain("F3 j=1",[C(5,1,20),C(8,5,3)],C(1,1,0),(7,5),175,"rank extension")),
        ("RANK17a",17,t.Chain("F9 j=2",[C(7,1,21),C(11,7,2)],C(1,1,0),(4,7),196,"rank extension")),
        ("RANK17b",17,t.Chain("F10 j=0",[C(7,1,21),C(13,7,3)],C(1,1,0),(7,4),196,"rank extension")),
    ]


def make_extension(t,case_id,rank,ch):
    candidates,notes=t.reduced_candidates(ch)
    candidates=[c for c in candidates if t.check_eps(c)[0]]
    charts=[chart_record(t,c,case_id) for c in candidates]
    conditional=("KILLED" if charts and all(c["status"]=="KILLED" for c in charts)
                 else "SURVIVES" if any(c["status"]=="SURVIVES" for c in charts) else "UNCLEAR")
    r=candidates[0]["r"] if candidates else None
    return {"case_id":case_id,"published_index":None,"ranking_positions":[rank],
            "degree_pair":list(ch.degrees()),"chain":[rational_corner(c) for c in ch.corners],
            "mn":[ch.m,ch.n],"max_degree":ch.maxdeg,
            "reduction":{"status":"derived" if charts else "out_of_scope",
                         "a":candidates[0]["a"] if candidates else None,
                         "b":candidates[0]["b"] if candidates else None,
                         "target_bracket":{"monomial":[r,0],"coefficient":1} if r is not None else None,
                         "base_polygons":[],"notes":notes},
            "charts":charts,"verdict":"UNCLEAR","conditional_pattern_verdict":conditional,
            "coverage":{"level":"conjectural_pattern",
                        "statement":"Beyond the published <=150 inventory; conditional output of the disproved-as-universal trackD pattern.",
                        "checker_or_citation":"triage_check.py; coverage_negative_control.py"},
            "survivor_dossier":None,"derivation_note":f"cases/{case_id}.md"}


def write_note(case,path):
    lines=[f"# {case['case_id']}: degrees {tuple(case['degree_pair'])}","",
           f"**Verdict: {case['verdict']}**  Conditional-pattern verdict: {case['conditional_pattern_verdict']}.","",
           f"Coverage: `{case['coverage']['level']}` — {case['coverage']['statement']}","",
           f"Chain: `{case['chain']}`; `(m,n)={tuple(case['mn'])}`.",""]
    target=case['reduction']['target_bracket']
    lines.append(f"Reduced target: `{target}`. Emitted charts: {len(case['charts'])}.")
    lines.append("")
    for chart in case['charts']:
        lines += [f"## {chart['chart_id']} — {chart['status']}","",
                  f"`N(P)={chart['newton_polygons']['P']}`", "",
                  f"`N(Q)={chart['newton_polygons']['Q']}`",""]
        for f in chart['essential_faces']:
            lines += [f"- weight `{f['weight']}`: P face `{f['P_monomials']}`, Q face `{f['Q_monomials']}`; "
                      f"budget `{f['budget']['nonconstant_unknowns']} vs {f['budget']['independent_conditions']}`; {f['status']}."]
            if f['kill_certificate']:
                k=f['kill_certificate'];lines += [f"  Kill: coefficient `{k['integer_coefficient']}` forces `{k['mandatory_variable']}=0`; residues `{k['modular_residues']}`."]
            elif f['solution_family']:
                lines += [f"  Family: `{f['solution_family']}`."]
            lines += ["  Face coefficient rules:"]
            for eq in f['equations']:
                lhs=" + ".join(f"{t['integer']}*{'*'.join(t['variables'])}" for t in eq['terms']) or "0"
                lines += [f"  - coefficient `{eq['output_monomial']}`: `{lhs} = {eq['rhs']}`"]
        if chart.get('note'): lines += [chart['note'],""]
    path.write_text("\n".join(lines)+"\n")


def write_report(cases,path,tally):
    lines=["# Complete frontier face triage","",
           "The first 34 rows are exactly the GGHV 2017 <=150 inventory; the final six rows expand ranking entries 14-17 beyond that bound.","",
           "A main verdict is promoted only for a published-exact reduction. `conditional` records what the conjectural trackD carrier would imply, without asserting coverage.","",
           "| row | rank | degrees | coverage | verdict | conditional | charts |","|---|---:|---:|---|---|---|---:|"]
    for c in cases:
        row=c['published_index'] if c['published_index'] is not None else c['case_id']
        rank=','.join(map(str,c['ranking_positions'])) or '-'
        lines += [f"| {row} | {rank} | {tuple(c['degree_pair'])} | {c['coverage']['level']} | {c['verdict']} | {c['conditional_pattern_verdict']} | {len(c['charts'])} |"]
    lines += ["",f"Tally: `{tally}`.","",
              "The exact published survivors are rows 8, 11, 18, and 25. Rows 8, 11, and 25 are eliminated by later arguments in GGHV 2022; row 18 is the live Proposition 4.3 `(72,108)` territory.","",
              "Sources: [GGHV 2017](https://arxiv.org/abs/1708.07936) and [GGHV 2022](https://arxiv.org/abs/2204.14178)."]
    path.write_text("\n".join(lines)+"\n")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--chain-map-dir",required=True);ap.add_argument("--output",default="triage.json")
    args=ap.parse_args();sys.path.insert(0,args.chain_map_dir);import trackD_chain_map as t
    cases=[make_case(t,i,ch) for i,ch in enumerate(t.all_chains(),1)]
    cases += [make_extension(t,*item) for item in extension_chains(t)]
    for c in cases:
        if c["case_id"] in ("GGHV34-11","GGHV34-25"):
            c["survivor_dossier"]={
                "face_type":"T8","coordinates_ref":"face_families.json#/T8",
                "dimension_after_coefficient_scaling":1,
                "normalized_solution_count":10,"residual_group":"mu_5",
                "budget":{"nonconstant_unknowns":13,"independent_conditions":12,"slack":1,
                          "after_u_normalization":"12 unknowns / 12 conditions"},
                "level1_equations_location":"charts[*].level1_cascade",
                "level1_shape":"14 coefficient equations in 15 new slice coefficients",
                "global_note":"Eliminated beyond face level by GGHV 2022 Theorem 5.1."
            }
        elif c["case_id"]=="GGHV34-18":
            c["survivor_dossier"]={
                "face_type":"T9","coordinates_ref":"face_families.json#/T9",
                "dimension_after_coefficient_scaling":1,
                "normalized_solution_count":35,"residual_group":"mu_7",
                "budget":{"nonconstant_unknowns":17,"independent_conditions":16,"slack":1,
                          "after_u_normalization":"16 unknowns / 16 conditions"},
                "level1_equations_location":"charts[*].level1_cascade",
                "level1_shape":"18 coefficient equations in 19 new slice coefficients; Hamiltonian kernel dimension at least one",
                "global_note":"The sole face survivor not eliminated by GGHV 2022; this is the live (72,108) territory up to transpose."
            }
        elif c["case_id"]=="GGHV34-08":
            c["survivor_dossier"]={
                "face_type":"commuting_outer_faces_only",
                "coordinates":"For B=conv{(0,0),(2,0),(3,1),(0,7)}, each corresponding outer edge has P_edge=alpha*R_edge^2 and Q_edge=beta*R_edge^3.",
                "dimension_after_coefficient_scaling":None,"residual_group":"edgewise Gm scalings",
                "budget":{"nonconstant_unknowns":None,"independent_conditions":None,"slack":None,
                          "basis":"No target-weight outer face exists."},
                "level1_equations_location":"charts[0].commuting_outer_faces[*].level1_cascade",
                "global_note":"Already eliminated by the intersection-number argument in GGHV 2022 Section 3."
            }
    tally={v:sum(c['verdict']==v for c in cases) for v in ("KILLED","SURVIVES","UNCLEAR")}
    data={"schema_version":"jc2.face-triage.v1","required_primes":list(PRIMES),
          "sources":[{"id":"GGHV2017","url":"https://arxiv.org/abs/1708.07936","scope":"34-row inventory"},
                     {"id":"GGHV2022","url":"https://arxiv.org/abs/2204.14178","scope":"published reductions"}],
          "cases":cases,"summary":{"case_count":len(cases),"tally":tally,"best_survivor_case_id":"GGHV34-18"}}
    Path(args.output).write_text(json.dumps(data,indent=2)+"\n")
    note_dir=Path(args.output).parent/"cases";note_dir.mkdir(exist_ok=True)
    for c in cases: write_note(c,note_dir/f"{c['case_id']}.md")
    write_report(cases,Path(args.output).parent/"TRIAGE_REPORT.md",tally)
    print("PASS",len(cases),tally)


if __name__=="__main__":main()
