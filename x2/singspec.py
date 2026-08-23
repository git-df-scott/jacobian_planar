"""Parse a campaign `extract_*.sing` system into a pure-Python spec.

Returns: nparams, Pd (list of {xexp: sympy expr}), Rr (list of {xexp: coeff}),
         windows (list, index k>=1 -> (lo,hi) or None meaning "all must vanish"),
         nd (list of param indices required nonzero), char.
"""
import re
import sympy as sp


def parse(path):
    txt = open(path).read()
    m = re.search(r'ring R = (\d+), \(c\(1\.\.(\d+)\)', txt)
    char, n = int(m.group(1)), int(m.group(2))
    c = sp.symbols(f'c1:{n+1}')

    def parse_poly(s):
        s = s.strip().rstrip(';')
        if s == '0':
            return {}
        out = {}
        for term in s.split('+'):
            term = term.strip()
            mm = re.match(r'^(?:c\((\d+)\)\*)?(\d+)?\*?x\^(\d+)$', term)
            if mm is None:
                mm2 = re.match(r'^(\d+)\*x\^(\d+)$', term)
                if mm2:
                    coef = sp.Integer(int(mm2.group(1)))
                    e = int(mm2.group(2))
                    out[e] = out.get(e, 0) + coef
                    continue
                raise ValueError(term)
            ci, num, e = mm.group(1), mm.group(2), int(mm.group(3))
            coef = sp.Integer(1)
            if ci:
                coef *= c[int(ci) - 1]
            if num:
                coef *= sp.Integer(int(num))
            out[e] = out.get(e, 0) + coef
        return out

    Pd, Rr = [], []
    for name, store in (('Pd', Pd), ('Rr', Rr)):
        idx = 0
        while True:
            mm = re.search(rf'^poly {name}{idx} = (.*);$', txt, re.M)
            if not mm:
                break
            store.append(parse_poly(mm.group(1)))
            idx += 1

    # normalize the char-p integer coefficients of Rr to signed representatives
    for d in Rr:
        for e in list(d):
            v = d[e]
            if v.is_Integer and v > char // 2:
                d[e] = v - char

    # windows, in order of the "t = Qk;" blocks
    windows = {}
    for mm in re.finditer(
            r't = Q(\d+);\s*\n\s*cf = coeffs\(t, x\);\s*\n\s*for \(e = 1; e <= nrows\(cf\); e\+\+\) \{\s*\n\s*(?:if \(e-1 < (\d+) \|\| e-1 > (\d+)\) \{ )?I = I \+ ideal\(cf\[e, 1\]\);',
            txt):
        k = int(mm.group(1))
        if mm.group(2) is None:
            windows[k] = None
        else:
            windows[k] = (int(mm.group(2)), int(mm.group(3)))

    ndm = re.search(r'poly nd = (.*);', txt).group(1)
    nd = [int(z) for z in re.findall(r'c\((\d+)\)', ndm)]
    p10 = re.search(r'poly p10 = c\((\d+)\);', txt).group(1)
    return dict(char=char, n=n, c=c, Pd=Pd, Rr=Rr, windows=windows, nd=nd,
                p10=int(p10))
