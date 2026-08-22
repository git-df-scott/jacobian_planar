#!/usr/bin/env python3
"""INDEPENDENT verification of the Nullstellensatz certificate.

PERELMAN DISCIPLINE
-------------------
The certificate was produced by Singular and "verified" by Singular. That is the
same process checking its own output, and it does not count. This script takes
ONLY the raw certificate data out of Singular -- the multiplier polynomials as
text -- and re-expands

        sum_i  lambda_i * F_i

from scratch, using this file's own parser and its own modular polynomial
arithmetic, then checks the result is exactly 1. Nothing here calls Singular,
msolve, or sympy; if it agrees, two independently built implementations agree.

It also re-derives the equations from the .ms file itself rather than trusting
any intermediate, so a corrupted or mis-ordered intermediate would show up as a
mismatch rather than passing silently.

Usage:  python3 w6_verify_cert.py SYSTEM.ms CERT.txt
"""
import sys, re
from collections import defaultdict


def parse_poly(s, p):
    """Parse a Singular polynomial into {monomial: coefficient} mod p.

    Deliberately written independently of w6_chain_modp.parse_ms so that a bug
    in one parser cannot hide itself in the other."""
    s = s.replace(' ', '')
    out = defaultdict(int)
    # split into signed terms, keeping the sign with the term
    for m in re.finditer(r'([+-]?)([^+-]+)', s):
        sign, term = m.group(1), m.group(2)
        if not term:
            continue
        coef, mono = 1, defaultdict(int)
        for f in term.split('*'):
            if not f:
                continue
            if re.fullmatch(r'\d+', f):
                coef = coef * int(f) % p
            else:
                mm = re.fullmatch(r'([A-Za-z_]\w*)(?:\^(\d+))?', f)
                assert mm, f"unparsable factor {f!r} in {term!r}"
                mono[mm.group(1)] += int(mm.group(2) or 1)
        if sign == '-':
            coef = (-coef) % p
        key = tuple(sorted(mono.items()))
        out[key] = (out[key] + coef) % p
    return {k: v for k, v in out.items() if v}


def mul(a, b, p):
    out = defaultdict(int)
    for ma, ca in a.items():
        for mb, cb in b.items():
            d = defaultdict(int)
            for v, e in ma:
                d[v] += e
            for v, e in mb:
                d[v] += e
            out[tuple(sorted(d.items()))] = (out[tuple(sorted(d.items()))] + ca * cb) % p
    return {k: v for k, v in out.items() if v}


def main():
    sysf, certf = sys.argv[1], sys.argv[2]
    L = open(sysf).read().split('\n')
    p = int(L[1].strip())
    body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    eqs = [parse_poly(b, p) for b in body]
    print(f"system: {sysf.split('/')[-1]}, {len(eqs)} equations, p = {p}")

    lam = {}
    for line in open(certf):
        m = re.match(r'^LAM\s+(\d+)\s*:\s*(.+)$', line.strip())
        if m:
            lam[int(m.group(1))] = parse_poly(m.group(2), p)
    nterms = sum(len(v) for v in lam.values())
    print(f"certificate: {len(lam)} nonzero multipliers, {nterms} terms total")
    assert lam, "no certificate lines parsed"

    total = {}
    for i, l in lam.items():
        assert 1 <= i <= len(eqs), f"multiplier index {i} out of range"
        prod = mul(l, eqs[i - 1], p)
        for k, v in prod.items():
            total[k] = (total.get(k, 0) + v) % p
    total = {k: v for k, v in total.items() if v}

    print(f"expanded sum has {len(total)} surviving term(s)")
    ok = (total == {(): 1})
    if not ok and total:
        bad = sorted(total.items(), key=lambda kv: -len(kv[0]))[:3]
        print(f"  residue sample: {bad}")
    print()
    print("INDEPENDENT VERDICT:", "PASS -- sum(lambda_i * F_i) == 1 exactly, "
          "re-derived with a separate parser and separate arithmetic"
          if ok else "FAIL -- the identity does NOT hold")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
