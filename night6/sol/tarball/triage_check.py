#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
import jsonschema

ROOT=Path(__file__).parent
data=json.loads((ROOT/"triage.json").read_text())
schema=json.loads((ROOT/"triage.schema.json").read_text())
jsonschema.validate(data,schema)
print("PASS: JSON validates against frozen jc2.face-triage.v1 schema")

assert len(data["cases"])==40
assert [c["published_index"] for c in data["cases"][:34]]==list(range(1,35))
assert all(c["published_index"] is None for c in data["cases"][34:])
assert len({c["case_id"] for c in data["cases"]})==40
assert sorted((c["case_id"],c["ranking_positions"][0]) for c in data["cases"][34:])==[
    ("RANK14",14),("RANK15",15),("RANK16a",16),("RANK16b",16),("RANK17a",17),("RANK17b",17)]
print("PASS: complete 34-row inventory plus six ranked frontier extensions")


def recompute(P,Q,target):
    buckets={}
    for i,j in P:
        for k,l in Q:
            c=i*l-j*k
            if c:
                z=(i+k-1,j+l-1)
                buckets.setdefault(z,[]).append({"integer":c,"variables":[f"p_{i}_{j}",f"q_{k}_{l}"]})
    buckets.setdefault(tuple(target),[])
    return [{"output_monomial":list(z),"terms":buckets[z],"rhs":1 if z==tuple(target) else 0}
            for z in sorted(buckets)]


face_count=kill_count=0
level1_count=0
for case in data["cases"]:
    target=case["reduction"]["target_bracket"]
    if target is None: continue
    target=target["monomial"]
    for chart in case["charts"]:
        mandatory={f"p_{i}_{j}" for i,j in chart["newton_polygons"]["P"]}
        mandatory|={f"q_{i}_{j}" for i,j in chart["newton_polygons"]["Q"]}
        for face in chart["essential_faces"]:
            face_count+=1
            assert face["equations"]==recompute(face["P_monomials"],face["Q_monomials"],target)
            cert=face.get("kill_certificate")
            if cert:
                kill_count+=1
                c=cert["integer_coefficient"]
                assert c!=0
                assert cert["mandatory_variable"] in mandatory
                for p in data["required_primes"]:
                    assert cert["modular_residues"][str(p)]==c%p
                    assert c%p!=0
        level=chart.get("level1_cascade")
        if level:
            level1_count+=1
            for eq in level["equations"]:
                oi,oj=eq["output_monomial"]
                for term in eq["terms"]:
                    pv,qv=term["variables"]
                    _,i,j=pv.split("_"); _,k,l=qv.split("_")
                    i,j,k,l=map(int,(i,j,k,l))
                    assert [i+k-1,j+l-1]==[oi,oj]
                    assert term["integer"]==i*l-j*k
        for outer in chart.get("commuting_outer_faces",[]):
            assert all(e["rhs"]==0 for e in outer["top_equations"])
            level=outer.get("level1_cascade")
            if level:
                level1_count+=1
                for eq in level["equations"]:
                    oi,oj=eq["output_monomial"]
                    for term in eq["terms"]:
                        pv,qv=term["variables"]
                        _,i,j=pv.split("_"); _,k,l=qv.split("_")
                        i,j,k,l=map(int,(i,j,k,l))
                        assert [i+k-1,j+l-1]==[oi,oj]
                        assert term["integer"]==i*l-j*k
print(f"PASS: recomputed {face_count} face systems and {kill_count} nonzero kill certificates")
print(f"PASS: checked every monomial term in {level1_count} emitted level-one cascades")

case84=next(c for c in data["cases"] if c["published_index"]==14)
coeffs={f["kill_certificate"]["integer_coefficient"]
        for ch in case84["charts"] for f in ch["essential_faces"] if f.get("kill_certificate")}
assert coeffs=={-26,39}
assert len(case84["charts"])==14 and all(ch["status"]=="KILLED" for ch in case84["charts"])
assert case84["verdict"]=="UNCLEAR" and case84["conditional_pattern_verdict"]=="KILLED"
assert case84["coverage"]["level"]=="conjectural_pattern"
print("PASS: (84,126) has 14 conditional kills {-26,39} and is not promoted past its coverage gap")

exact={c["published_index"]:len(c["charts"]) for c in data["cases"] if c["coverage"]["level"]=="published_exact"}
assert exact=={8:1,11:3,18:2,25:1}
tally=Counter(c["verdict"] for c in data["cases"])
full_tally={v:tally[v] for v in ("KILLED","SURVIVES","UNCLEAR")}
assert full_tally==data["summary"]["tally"]
assert full_tally=={"KILLED":0,"SURVIVES":4,"UNCLEAR":36}
print("PASS: exact-coverage rows and final tally agree")

families=json.loads((ROOT/"face_families.json").read_text())
assert len(families)==9
for name,f in families.items():
    dp,dq=f["degrees"]
    assert f["top_identity"]==0
    assert f["residual_group"]==f"mu_{dp}"
    assert len(f["residual_equations"])==dp-1
print("PASS: nine survivor ODE coordinate dossiers have top cancellation and residual mu_deg(P)")
