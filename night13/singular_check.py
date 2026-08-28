"""night13 -- independent verification in Singular (ring: Q, char 0).

Three checks, all in characteristic 0 with exact rational arithmetic, run by
an engine that shares no code with kit.py / prestratum.py:

  S1  [A*H^2, B*H^3] = 0 identically, with h2, h14, h29, h41, A, B all
      symbolic ring variables (this is control Ca done symbolically rather
      than at sampled integer values).
  S2  the degenerate carrier P = A*H^2 + a*x, Q = B*H^3 + b*y: the full
      bracket must equal a*b + A*b*(H^2)_x + a*B*(H^3)_y, and its
      coefficients at the three monomials 1, x^3 y^80, x^123 y^2 must be
      a*b, 4*A*b*h2^2 and 3*a*B*h41^3.
  S3  uniqueness of the two obstruction rows on the FULL greedy carrier:
      with random nonzero integer coefficients on all 96 P-lower and 256
      Q-lower monomials and on the top parameters, the coefficient of
      x^3 y^80 in the bracket must still be exactly 4*A*b_(0,1) and that of
      x^123 y^2 exactly 3*a_(1,0)*B*h41^3.  If any further pair of carrier
      monomials could reach either row, these equalities would fail.
"""

import json
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def gen():
    car = json.load(open(os.path.join(HERE, "carrier.json")))
    C_P = [tuple(m) for m in car["C_P"]]
    C_Q = [tuple(m) for m in car["C_Q"]]
    rng = random.Random(4242)
    aP = {m: rng.randrange(1, 40) * rng.choice([1, -1]) for m in C_P}
    bQ = {m: rng.randrange(1, 40) * rng.choice([1, -1]) for m in C_Q}
    h = [1, rng.randrange(2, 20), rng.randrange(2, 20), rng.randrange(2, 20)]
    A = rng.randrange(2, 20)
    B = rng.randrange(2, 20)

    L = []
    L.append('ring R = 0, (x,y,h2,h14,h29,h41,A,B,a,b), dp;')
    L.append('poly H = h2*x^2*y^40 + h14*x^14*y^28 + h29*x^29*y^13 '
             '+ h41*x^41*y;')
    L.append('poly P0 = A*H^2;  poly Q0 = B*H^3;')
    L.append('poly br0 = diff(P0,x)*diff(Q0,y) - diff(P0,y)*diff(Q0,x);')
    L.append('"S1 leading bracket is zero:", br0 == 0;')
    L.append('"S1 deg P0, deg Q0:", deg(P0), deg(Q0);')
    L.append('poly P1 = A*H^2 + a*x;  poly Q1 = B*H^3 + b*y;')
    L.append('poly br1 = diff(P1,x)*diff(Q1,y) - diff(P1,y)*diff(Q1,x);')
    L.append('poly pred = a*b + A*b*diff(H^2,x) + a*B*diff(H^3,y);')
    L.append('"S2 degenerate bracket equals independent expansion:", '
             'br1 - pred == 0;')
    L.append('proc getc(poly f, poly m) { matrix C = coef(f, xy); int i; '
             'for(i=1;i<=ncols(C);i++){ if(C[1,i]==m){ return(C[2,i]); } } '
             'return(0); }')
    L.append('"S2 coeff at 1        :", getc(br1, 1), " expected ", a*b;')
    L.append('"S2 coeff at x3y80    :", getc(br1, x^3*y^80), '
             '" expected ", 4*A*b*h2^2;')
    L.append('"S2 coeff at x123y2   :", getc(br1, x^123*y^2), '
             '" expected ", 3*a*B*h41^3;')
    L.append('"S2 all three match:", (getc(br1,1)-a*b==0) && '
             '(getc(br1,x^3*y^80)-4*A*b*h2^2==0) && '
             '(getc(br1,x^123*y^2)-3*a*B*h41^3==0);')

    # S3: the full carrier at explicit integers
    sub = ('h2=%d, h14=%d, h29=%d, h41=%d, A=%d, B=%d'
           % (h[0], h[1], h[2], h[3], A, B))
    L.append('ring R2 = 0, (x,y), dp;')
    L.append('poly H2 = %d*x^2*y^40 + %d*x^14*y^28 + %d*x^29*y^13 '
             '+ %d*x^41*y;' % tuple(h))
    L.append('poly P = %d*H2^2' % A
             + ''.join(' + (%d)*x^%d*y^%d' % (aP[m], m[0], m[1])
                       for m in C_P) + ';')
    L.append('poly Q = %d*H2^3' % B
             + ''.join(' + (%d)*x^%d*y^%d' % (bQ[m], m[0], m[1])
                       for m in C_Q) + ';')
    L.append('poly br = diff(P,x)*diff(Q,y) - diff(P,y)*diff(Q,x);')
    L.append('proc getc2(poly f, poly m) { matrix C = coef(f, xy); int i; '
             'for(i=1;i<=ncols(C);i++){ if(C[1,i]==m){ return(C[2,i]); } } '
             'return(0); }')
    L.append('"S3 params: %s";' % sub)
    L.append('"S3 deg P, deg Q:", deg(P), deg(Q);')
    L.append('"S3 coeff at x3y80  :", getc2(br, x^3*y^80), " expected ", %d;'
             % (4 * A * bQ[(0, 1)]))
    L.append('"S3 coeff at x123y2 :", getc2(br, x^123*y^2), " expected ", %d;'
             % (3 * aP[(1, 0)] * B * h[3] ** 3))
    L.append('"S3 coeff at 1      :", getc2(br, 1), " expected ", %d;'
             % (aP[(1, 0)] * bQ[(0, 1)]))
    L.append('"S3 all three match:", (getc2(br,x^3*y^80)==%d) && '
             '(getc2(br,x^123*y^2)==%d) && (getc2(br,1)==%d);'
             % (4 * A * bQ[(0, 1)], 3 * aP[(1, 0)] * B * h[3] ** 3,
                aP[(1, 0)] * bQ[(0, 1)]))
    L.append('exit;')
    path = os.path.join(HERE, "leading.sing")
    open(path, "w").write("\n".join(L) + "\n")
    return path


if __name__ == "__main__":
    p = gen()
    r = subprocess.run(["Singular", "-q", p], capture_output=True, text=True,
                       timeout=3600)
    out = r.stdout + r.stderr
    open(os.path.join(HERE, "singular_out.txt"), "w").write(out)
    print(out)
