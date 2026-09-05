#!/usr/bin/env python3
"""Replay only the new strike's exact certificates and retained controls."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
scripts=['verify_69_noncube.py','derive_69_resonance.py','verify_69_inputs_and_controls.py']
results=[]
for script in scripts:
    result=subprocess.run([sys.executable,str(HERE/script)],capture_output=True,text=True)
    print(result.stdout,end='')
    if result.returncode:
        print(result.stderr,file=sys.stderr)
        raise SystemExit(result.returncode)
    results.append({'script':script,'exit_code':result.returncode,'output':result.stdout.splitlines()})
files=sorted(path for path in HERE.iterdir() if path.is_file() and path.name!='verification_summary.json')
summary={'status':'PASS','scope':'Exact identities and controls; mathematical scope as in Astra 8 report',
         'counterexample_found':False,'full_collision_route_closed':False,
         'single_irreducible_gap_proved':False,'degree_15_fully_closed':False,
         'noncube_69_obstruction_certificate':'PASS','results':results,
         'file_sha256':{path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in files}}
(HERE/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
