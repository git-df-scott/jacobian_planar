#!/usr/bin/env python3
"""End-to-end decision of the minimal-width mu=2 strip target at parameter m
and characteristic p:

  stage 1  E1 (leading level, f2 only) -> lex triangular set in F1..F_{m-1}
  stage 1b factor the eliminant in F_{m-1}
  stage 2  for each irreducible factor, adjoin the lower levels over
           F_p[a]/(factor) and test for emptiness with B_top invertible.

Reports the RAW Singular verdict lines.  dim = -1 / GB = 1  means EMPTY.
"""
import re, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = int(sys.argv[1]); P = int(sys.argv[2])
BUDGET = int(sys.argv[3]) if len(sys.argv) > 3 else 1800

BODY = r'''
proc cf(poly p, int k) { matrix M = coeffs(p, T); if (k+1 > nrows(M)) { return(poly(0)); } return(M[k+1,1]); }
proc addall(poly p) { matrix M = coeffs(p,T); int k; ideal J; for (k=1; k<=nrows(M); k++) { J = J + ideal(M[k,1]); } return(J); }
int i; int n; poly cur; poly d;
poly f2 = T; for (i=1; i<=nF; i++) { f2 = f2 + FF(i)*T^(i+1); }
poly f1 = 0; for (i=0; i<=nA-1; i++) { f1 = f1 + A(i)*T^(i+1); }
poly f0 = 0; for (i=0; i<=nB-1; i++) { f0 = f0 + B(i)*T^i; }
poly g3 = 0;
for (n=0; n<=dg-2; n++) { cur = 2*f2*diff(g3,T) - 3*diff(f2,T)*g3 - T^2; d = -cf(cur,n+2)/(1+2*n); g3 = g3 + d*T^(n+2); }
ideal E1 = simplify(addall(2*f2*diff(g3,T) - 3*diff(f2,T)*g3 - T^2),2);
poly src4 = f1*diff(g3,T) - 3*diff(f1,T)*g3;
poly g2 = 0;
for (n=0; n<=dg-2; n++) { cur = 2*f2*diff(g2,T) - 2*diff(f2,T)*g2 + src4; d = -cf(cur,n+2)/(2+2*n); g2 = g2 + d*T^(n+2); }
poly R4 = 2*f2*diff(g2,T) - 2*diff(f2,T)*g2 + src4;
poly src3 = f1*diff(g2,T) - 2*diff(f1,T)*g2 - 3*diff(f0,T)*g3;
poly g1 = 0;
for (n=0; n<=dg-1; n++) { cur = 2*f2*diff(g1,T) - diff(f2,T)*g1 + src3; d = -cf(cur,n+1)/(1+2*n); g1 = g1 + d*T^(n+1); }
poly R3 = 2*f2*diff(g1,T) - diff(f2,T)*g1 + src3;
poly src2 = f1*diff(g1,T) - diff(f1,T)*g1 - 2*diff(f0,T)*g2;
poly g0 = 0;
for (n=0; n<=dg-1; n++) { cur = 2*f2*diff(g0,T) + src2; d = -cf(cur,n+1)/(2+2*n); g0 = g0 + d*T^(n+1); }
ideal REST = simplify(addall(2*f2*diff(g0,T) + src2) + addall(R3) + addall(R4)
                      + addall(f1*diff(g0,T) - diff(f0,T)*g1), 2);
'''


def run(script, tag, budget):
    path = os.path.join(HERE, f'_{tag}.sing')
    open(path, 'w').write(script)
    try:
        r = subprocess.run(['Singular', '-q', path], capture_output=True,
                           text=True, timeout=budget)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    return '\n'.join(l for l in r.stdout.splitlines()
                     if l.strip() and 'redefining' not in l and not l.startswith('//'))


nF, nA, nB, dg = M - 1, M, M + 1, 3 * M // 2

s1 = f'''LIB "triang.lib";
int nF = {nF}; int nA = {nA}; int nB = {nB}; int dg = {dg};
ring R0 = {P}, (FF(1..nF), A(0..nA-1), B(0..nB-1), T), dp;
{BODY}
"m={M} p={P} degP={3*M} degQ={9*M//2} unknowns={nF+nA+nB} E1conds=" + string(size(E1)) + " lower=" + string(size(REST));
ring R1 = {P}, (FF(1..nF)), dp;
ideal E1 = imap(R0,E1) + ideal(FF(nF)-1);
option(redSB); ideal J = std(E1);
"E1dim " + string(dim(J));
if (dim(J)==0) {{ "E1vdim " + string(vdim(J)); }}
ring R1l = {P}, (FF(1..nF)), lp;
ideal J = fglm(R1, J);
int k;
for (k=1; k<=size(J); k++) {{ "TRI " + string(J[k]); }}
quit;
'''
out1 = run(s1, f'p1_m{M}_p{P}', BUDGET)
print(out1, flush=True)
tri = [l[4:] for l in out1.splitlines() if l.startswith('TRI ')]
if not tri:
    sys.exit(0)
# eliminant = the generator involving only FF(nF-1)  (lex: last variable block)
elim = [t for t in tri if re.fullmatch(r'[^,]*', t) and f'FF({nF-1})' in t
        and not any(f'FF({j})' in t for j in range(1, nF - 1))]
print("eliminant:", elim[0][:120] if elim else "NONE", flush=True)

s_fac = f'''ring R = {P}, FF({nF-1}), dp;
poly h = {elim[0]};
list L = factorize(h); int i;
for (i=1; i<=size(L[1]); i++) {{ if (deg(L[1][i])>0) {{ "FAC " + string(deg(L[1][i])) + " " + string(L[1][i]); }} }}
quit;
'''
outf = run(s_fac, f'fac_m{M}_p{P}', 600)
facs = [l[4:].split(' ', 1) for l in outf.splitlines() if l.startswith('FAC ')]
print(f"{len(facs)} irreducible factors, degrees {[int(d) for d,_ in facs]}", flush=True)

subs = [t for t in tri if t not in elim]
for idx, (deg, fac) in enumerate(facs):
    fac_a = fac.replace(f'FF({nF-1})', 'a')
    setf = []
    for t in subs:
        mm = re.match(rf'FF\((\d+)\)(.*)', t)
        j = int(mm.group(1))
        rest = mm.group(2).replace(f'FF({nF-1})', 'a')
        setf.append(f'number v{j} = -({rest});')     # t = FF(j) + rest = 0
    setf.append(f'number v{nF} = 1;')
    fl = ",".join(f'number(v{j})' for j in range(1, nF + 1))
    s2 = f'''int nF = {nF}; int nA = {nA}; int nB = {nB}; int dg = {dg};
ring R0 = ({P}, a), (A(0..nA-1), B(0..nB-1), T), dp;
minpoly = {fac_a};
{chr(10).join(setf)}
list FVl = {fl};
proc cf(poly p, int k) {{ matrix M = coeffs(p, T); if (k+1 > nrows(M)) {{ return(poly(0)); }} return(M[k+1,1]); }}
proc addall(poly p) {{ matrix M = coeffs(p,T); int k; ideal J; for (k=1; k<=nrows(M); k++) {{ J = J + ideal(M[k,1]); }} return(J); }}
int i; int n; poly cur; poly d;
poly f2 = T; for (i=1; i<=nF; i++) {{ f2 = f2 + FVl[i]*T^(i+1); }}
poly f1 = 0; for (i=0; i<=nA-1; i++) {{ f1 = f1 + A(i)*T^(i+1); }}
poly f0 = 0; for (i=0; i<=nB-1; i++) {{ f0 = f0 + B(i)*T^i; }}
poly g3 = 0;
for (n=0; n<=dg-2; n++) {{ cur = 2*f2*diff(g3,T) - 3*diff(f2,T)*g3 - T^2; d = -cf(cur,n+2)/(1+2*n); g3 = g3 + d*T^(n+2); }}
"E1residualcount " + string(size(simplify(addall(2*f2*diff(g3,T) - 3*diff(f2,T)*g3 - T^2),2)));
poly src4 = f1*diff(g3,T) - 3*diff(f1,T)*g3;
poly g2 = 0;
for (n=0; n<=dg-2; n++) {{ cur = 2*f2*diff(g2,T) - 2*diff(f2,T)*g2 + src4; d = -cf(cur,n+2)/(2+2*n); g2 = g2 + d*T^(n+2); }}
poly R4 = 2*f2*diff(g2,T) - 2*diff(f2,T)*g2 + src4;
poly src3 = f1*diff(g2,T) - 2*diff(f1,T)*g2 - 3*diff(f0,T)*g3;
poly g1 = 0;
for (n=0; n<=dg-1; n++) {{ cur = 2*f2*diff(g1,T) - diff(f2,T)*g1 + src3; d = -cf(cur,n+1)/(1+2*n); g1 = g1 + d*T^(n+1); }}
poly R3 = 2*f2*diff(g1,T) - diff(f2,T)*g1 + src3;
poly src2 = f1*diff(g1,T) - diff(f1,T)*g1 - 2*diff(f0,T)*g2;
poly g0 = 0;
for (n=0; n<=dg-1; n++) {{ cur = 2*f2*diff(g0,T) + src2; d = -cf(cur,n+1)/(2+2*n); g0 = g0 + d*T^(n+1); }}
ideal REST = simplify(addall(2*f2*diff(g0,T) + src2) + addall(R3) + addall(R4)
                      + addall(f1*diff(g0,T) - diff(f0,T)*g1), 2);
ring RF = ({P}, a), (A(0..nA-1), B(0..nB-1), U), dp;
minpoly = {fac_a};
ideal I = imap(R0,REST) + ideal(U*B(nB-1)-1);
ideal G = std(I);
"VERDICT dim " + string(dim(G)) + " GB1 " + string(G[1]);
quit;
'''
    res = run(s2, f'st_m{M}_p{P}_{idx}', BUDGET)
    print(f"[factor {idx} deg {deg}] {res}", flush=True)
