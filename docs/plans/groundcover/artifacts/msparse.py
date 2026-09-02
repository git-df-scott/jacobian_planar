"""Parser for msolve .ms files -> (vars, char, [gen_dict]) with exact Fraction coeffs.
Generator representation: dict {frozen-sorted-tuple((var,exp),...): Fraction coeff}
"""
import re, sys
from fractions import Fraction

def read_ms(path):
    raw = open(path).read()
    lines = raw.split("\n")
    varline = lines[0].strip()
    charline = lines[1].strip()
    variables = [v.strip() for v in varline.split(",") if v.strip()]
    ch = int(charline)
    body = "\n".join(lines[2:])
    # generators separated by commas that terminate a line (msolve style);
    # be robust: strip newlines only where the preceding char is an operator
    gens = []
    cur = []
    for ln in body.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if s.endswith(","):
            cur.append(s[:-1]); gens.append("".join(cur)); cur = []
        else:
            cur.append(s)
    if cur:
        last = "".join(cur)
        last = last.rstrip(":;").strip()
        if last:
            gens.append(last)
    return variables, ch, gens

TOKEN = re.compile(r'([+-]?)([^+-]+)')

def parse_poly(s, varset):
    s = s.replace(" ", "").replace("\n", "")
    assert "(" not in s and ")" not in s, "parenthesised input not supported"
    out = {}
    i = 0
    n = len(s)
    while i < n:
        sign = 1
        if s[i] == '+':
            i += 1
        elif s[i] == '-':
            sign = -1; i += 1
        j = i
        while j < n and s[j] not in '+-':
            j += 1
        term = s[i:j]
        i = j
        if not term:
            continue
        coeff = Fraction(sign)
        mono = {}
        for fac in term.split('*'):
            if not fac:
                continue
            if '^' in fac:
                b, e = fac.split('^'); e = int(e)
            else:
                b, e = fac, 1
            if re.fullmatch(r'\d+', b):
                coeff *= Fraction(int(b))**e
            elif re.fullmatch(r'\d+/\d+', b):
                coeff *= Fraction(b)**e
            else:
                assert b in varset, "unknown symbol %r in term %r" % (b, term)
                mono[b] = mono.get(b, 0) + e
        key = tuple(sorted(mono.items()))
        out[key] = out.get(key, Fraction(0)) + coeff
        if out[key] == 0:
            del out[key]
    return out

def load(path):
    variables, ch, gens = read_ms(path)
    vs = set(variables)
    polys = [parse_poly(g, vs) for g in gens]
    return variables, ch, polys
