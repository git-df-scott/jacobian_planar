"""ITEM 3 -- the verdict-change log for the above-125 queue.

Compares h2/h2_state.json (this session, 900 s per prime) against the campaign's
own campaign/audit_tracks/trackD_twoprime_state.json (90 s per prime) and emits
every change, in particular every TIMEOUT -> EMPTY / LIVE.  A target whose
verdict did not change is listed as UNCHANGED with its budget, so "no change"
is visible rather than silent.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OLD = os.path.join(ROOT, "campaign", "audit_tracks", "trackD_twoprime_state.json")
NEW = os.path.join(HERE, "h2_state.json")

old = json.load(open(OLD))
new = json.load(open(NEW))
rows = []
for tag, rec in sorted(new.items()):
    o = old.get(tag)
    ov = o["verdict"] if o else None
    nv = rec["verdict"]
    ob = (o or {}).get("budget")
    nb = rec.get("budget")
    if o is None:
        kind = "NEW"
    elif ov != nv:
        kind = f"CHANGED {ov} -> {nv}"
    else:
        kind = f"UNCHANGED {nv}"
    rows.append({"tag": tag, "kind": kind, "old_verdict": ov, "new_verdict": nv,
                 "old_budget": ob, "new_budget": nb, "max": rec.get("max"),
                 "params": rec.get("params"),
                 "per_prime": rec.get("per_prime")})
counts = collections.Counter(r["kind"].split()[0] for r in rows)
changed = [r for r in rows if r["kind"].startswith("CHANGED")]
live = [r for r in rows if r["new_verdict"] in ("LIVE", "DISAGREE")]
print("=" * 78)
print("ITEM 3 -- above-125 queue: verdict changes at the 900 s cap")
print("=" * 78)
print(f"  campaign state: {len(old)} targets;  this session: {len(new)} targets")
print(f"  {dict(counts)}")
print(f"  verdicts now: "
      f"{dict(collections.Counter(r['new_verdict'] for r in rows))}")
print(f"  TIMEOUT -> decided: "
      f"{[ (r['tag'][:48], r['kind']) for r in changed if r['old_verdict']=='TIMEOUT' ]}")
print(f"  LIVE or DISAGREE: {len(live)}")
for r in live:
    print(f"    *** {r['new_verdict']}  {r['tag']}  max={r['max']}  "
          f"CANDIDATE-UNVERIFIED protocol applies")
json.dump({"counts": dict(counts), "rows": rows},
          open(os.path.join(HERE, "h2_changelog.json"), "w"), indent=1)
print("=" * 78)
