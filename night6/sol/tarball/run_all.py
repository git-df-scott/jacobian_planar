#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run(*args):
    print("+",*args,flush=True)
    subprocess.run([sys.executable,*args],check=True)


module_dir=("." if Path("trackD_chain_map.py").exists()
            else "../campaign_session44/session44/lead4")
run("coverage_negative_control.py","--chain-map-dir",module_dir)
run("triage_generate.py","--chain-map-dir",module_dir,"--output","triage.json")
run("face_families.py")
run("face_hurwitz_general.py","--case1-module-dir",module_dir)
run("triage_check.py")
print("PASS: complete frontier triage verification")
