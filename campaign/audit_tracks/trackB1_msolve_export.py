#!/usr/bin/env python3
"""Export a Track-B1 / Track-A system to msolve input format.

msolve (https://msolve.lip6.fr, F4 over F_p) is a far stronger engine than
Singular's std on the shapes this campaign produces; P3 authorizes installing
it, and T5's "lottery ticket" on the full pentagon system is exactly the kind
of run it exists for.

Input format:
    var1,var2,...,varn
    <characteristic>
    poly1,
    poly2,
    ...
    polyk

Nonvanishing side conditions are imposed by Rabinowitsch: one fresh variable
w_sat and the generator  w_sat*(prod of the nonzero conditions) - 1. That is
the same saturation the Singular pipeline uses, so verdicts are comparable:
an empty variety here means no point WITH the side conditions nonzero, which
is the case-(1) question.

Usage:
    trackB1_msolve_export.py SYSTEM.json OUT.ms [CHAR] [--no-sat]
"""
import json, sys


def mono_str(mono):
    parts = []
    for var, e in mono:
        parts.append(var if e == 1 else "%s^%d" % (var, e))
    return "*".join(parts) if parts else "1"


def poly_str(terms, char):
    """terms: [[monomial, [num, den]], ...] -> msolve polynomial string.

    Denominators are cleared into the field: over F_char a rational c = n/d is
    n * d^(char-2). msolve accepts integer coefficients only.
    """
    out = []
    for mono, (num, den) in terms:
        c = num % char if den == 1 else (num * pow(den, char - 2, char)) % char
        if c == 0:
            continue
        out.append("%d*%s" % (c, mono_str(mono)))
    return " + ".join(out) if out else "0"


def export(sys_path, out_path, char=65521, saturate=True):
    d = json.load(open(sys_path))
    variables = list(d["variables"])
    nz = list(d.get("nonzero", []))
    nz_exprs = list(d.get("nonzero_exprs", []))
    polys = [poly_str(e["terms"], char) for e in d["equations"]]
    polys = [p for p in polys if p != "0"]
    if saturate and (nz or nz_exprs):
        assert not nz_exprs, ("string-form nonzero_exprs not supported by this "
                             "exporter; use the structured system")
        variables = variables + ["w_sat"]
        prod = "*".join(nz)
        polys.append("w_sat*%s - 1" % prod)
    with open(out_path, "w") as fh:
        fh.write(",".join(variables) + "\n")
        fh.write("%d\n" % char)
        fh.write(",\n".join(polys) + "\n")
    print("msolve export: %s -> %s  (%d vars, %d polys, char %d, sat=%s)"
          % (sys_path, out_path, len(variables), len(polys), char, saturate))
    print("content_hash of source system: %s" % d.get("content_hash"))
    return out_path


if __name__ == "__main__":
    a = sys.argv[1:]
    export(a[0], a[1],
           int(a[2]) if len(a) > 2 and not a[2].startswith("--") else 65521,
           "--no-sat" not in a)
