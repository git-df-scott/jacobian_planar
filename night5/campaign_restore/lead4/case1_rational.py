#!/usr/bin/env python3
"""Characteristic-zero run of the reduced 6-variable essential-face system."""
import subprocess, sys
from case1_points import reduced_eqs_modp, to_msolve
k = 3
m, n = 2*k+1, 3*k+1
eqs, unk = reduced_eqs_modp(m, n, 0)
fn = "_scratch_case1/case1_red_k3_QQ.ms"
to_msolve(eqs, unk, 0, fn)
out = fn.replace(".ms", ".res")
pr = subprocess.run(["msolve", "-f", fn, "-o", out, "-P", "2"],
                    capture_output=True, text=True, timeout=20000)
print(pr.stdout[-1500:], pr.stderr[-800:])
print(open(out).read()[:1500])
