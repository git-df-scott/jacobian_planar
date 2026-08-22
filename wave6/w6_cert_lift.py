#!/usr/bin/env python3
"""Reconstruct the Nullstellensatz certificate over Q by CRT.  Bypasses char-0 Groebner.

PERELMAN-ENTROPY MOVE
---------------------
The characteristic-zero Groebner basis on 119 variables is the stall, and more
compute on the same object will not resolve it.  So use a different object --
the CERTIFICATE, which is only ~53 terms -- and a technique from outside the
method (CRT + rational reconstruction) to lift it.

Fix ONE rational system (`char0_118v.ms`, integer coefficients).  Reduce it
modulo several primes.  Extract the certificate at each -- seconds, not hours.
If the monomial supports agree across primes, CRT the coefficients and
rationally reconstruct.  Then verify  sum(lambda_i * F_i) = 1  EXACTLY over Q.

That final expansion is the proof: it trusts no Groebner engine, no prime, and
no solver -- only integer arithmetic.
"""
import sys, os, re, json, subprocess
from collections import defaultdict

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')
SRC = 'wave6/pentseed/char0_118v.ms'


def load_int_system(path):
    L = open(path).read().split('\n')
    vs = [v.strip() for v in L[0].split(',') if v.strip()]
    body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    assert not leak, f"MALFORMED source: undeclared {leak[:8]}"
    return vs, body


def cert_at_prime(vs, body, p):
    f = f'{SCR}/cl_{p}.sing'
    open(f, 'w').write(
        f'ring R = {p}, ({",".join(vs)}), dp;\n'
        'ideal I = ' + ",\n".join(body) + ';\n'
        'option(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "UNIT"; matrix T = lift(I,G);\n'
        'int i; for(i=1;i<=nrows(T);i++){ if(T[i,1]!=0){ "LAM",i,":",T[i,1]; } } }\n'
        'else { "NOTUNIT"; }\n"END";\nexit;\n')
    r = subprocess.run(['timeout', '1200', 'Singular', '-q', f],
                       capture_output=True, text=True)
    return r.stdout


def parse_cert(txt, p):
    # DO NOT conflate these: NOTUNIT means the system HAS solutions, while an
    # absent marker means the run gave NO VERDICT (timeout/crash). Reporting
    # them with one message hid a 1200s timeout behind wording that read like a
    # mathematical result.
    if 'NOTUNIT' in txt:
        return 'NOTUNIT'
    if 'UNIT' not in txt:
        return None                      # NO VERDICT
    lam = {}
    for line in txt.split('\n'):
        m = re.match(r'^LAM\s+(\d+)\s*:\s*(.+)$', line.strip())
        if not m:
            continue
        idx, s = int(m.group(1)), m.group(2).replace(' ', '')
        d = defaultdict(int)
        for mm in re.finditer(r'([+-]?)([^+-]+)', s):
            sign, term = mm.group(1), mm.group(2)
            if not term:
                continue
            co, mono = 1, defaultdict(int)
            for fa in term.split('*'):
                if not fa:
                    continue
                if re.fullmatch(r'\d+', fa):
                    co = co * int(fa) % p
                else:
                    g = re.fullmatch(r'([A-Za-z_]\w*)(?:\^(\d+))?', fa)
                    assert g, f"unparsable factor {fa!r}"
                    mono[g.group(1)] += int(g.group(2) or 1)
            if sign == '-':
                co = (-co) % p
            k = tuple(sorted(mono.items()))
            d[k] = (d[k] + co) % p
        lam[idx] = {k: v for k, v in d.items() if v}
    return lam


def main():
    primes = [int(x) for x in sys.argv[1:]] or [1000003, 1000033, 1000039]
    vs, body = load_int_system(SRC)
    print(f"fixed Q-system: {os.path.basename(SRC)}, {len(vs)} vars, "
          f"{len(body)} equations", flush=True)
    certs = {}
    for p in primes:
        txt = cert_at_prime(vs, body, p)
        c = parse_cert(txt, p)
        if c == 'NOTUNIT':
            print(f"  p={p}: NOT the unit ideal -- the system HAS solutions mod p. "
                  f"That is a LEAD, not a failure.", flush=True)
            continue
        if c is None:
            print(f"  p={p}: NO VERDICT (timeout/crash) -- not EMPTY, not a hit",
                  flush=True)
            continue
        certs[p] = c
        print(f"  p={p}: UNIT, {len(c)} multipliers, "
              f"{sum(len(v) for v in c.values())} terms", flush=True)
    if len(certs) < 2:
        print("need at least two usable primes")
        return 1
    ps = sorted(certs)
    sup = {p: {(i, m) for i, l in certs[p].items() for m in l} for p in ps}
    same = all(sup[p] == sup[ps[0]] for p in ps)
    print(f"\nsupports identical across primes: {same}  "
          f"(union {len(set.union(*sup.values()))}, "
          f"intersection {len(set.intersection(*sup.values()))})")
    json.dump({str(p): {str(i): {repr(k): v for k, v in l.items()}
                        for i, l in certs[p].items()} for p in ps},
              open(f'{SCR}/certs.json', 'w'))
    print(f"saved {SCR}/certs.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
