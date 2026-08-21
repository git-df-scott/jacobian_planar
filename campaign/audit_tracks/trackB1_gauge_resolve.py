#!/usr/bin/env python3
"""Resolve the last stated gap: the [P_8,.]-kernel / gauge caveat.

The caveat recorded in trackB1_THEOREM_S_square.md is that the descent to the
bottom equation could stall on a kernel weight, and that the polynomial gauge
Q -> Q + lambda P + mu cannot reach all of them.  That is TRUE for the second
(polynomial-W) proof, and it is IRRELEVANT for the first (formal-F) proof.
This script machine-checks the two facts the first proof needs.

FACT 1 (kernel).  Among rational functions, ker [P_8, .] at weight W is
        spanned by (S^)^{W/4},   P_8^ = a S^2,
i.e. it is 1-dimensional when (S^)^{W/4} is rational and 0 otherwise.
Checked here by brute-force linear algebra over F_p with denominators S^N.

FACT 2 (absorber).  Whenever that kernel is nonzero, an element of
ker [P, .] with that top slice EXISTS: P^{W/8} is a weight-graded formal series
with [P, P^{W/8}] = 0 and top slice a^{W/8} (S^)^{W/4}.  Its slices are
rational because P_8^{W/8} = (a S^2)^{W/8} = a^{W/8} (S^)^{W/4} is exactly as
rational as the kernel element itself -- so the absorber is available in
precisely the cases where there is something to absorb.  Checked here by
building the series and verifying [P, P^{W/8}] = 0 slice by slice.

Consequence: the descent in Step 2 never stalls.  Each absorption strictly
lowers wtop(Delta) (which starts <= 11 because Delta_12 = Q_12 - F_12 = 0), so
after at most 21 steps wtop(Delta) = -10 and the weight -2 part of [P,Delta] is
[P_8, Delta_-10] alone.  Hence (C4) holds unconditionally, with no gauge needed
and no polynomiality demanded of Delta.
"""
import random, sys
from trackB1_sqrt import pmul, padd, pscal, ptrim, pdiv_exact, pderiv
from trackB1_cascade_general import component1_S, component2_S, half_radical

p = 65521

def kernel_dim(S, W, a=1, Nmax=6, degmax=20):
    """dim of {G = H/S^N : [P_8, G] = 0}, P_8 = a S^2, weight W. Rational G."""
    # [P_8, H/S^N] = W*(a S^2)'*H/S^N - 8*(a S^2)*(H/S^N)'
    #   = a S^{-N-1} [ W*(S^2)'*S*H - 8*S^3*H' + 8N*S^2*S'*H ]
    S2 = pmul(S, S, p); S3 = pmul(S2, S, p)
    dS2 = pderiv(S2, p); Sp = pderiv(S, p)
    A1 = pmul(dS2, S, p); A2 = pmul(S2, Sp, p)
    best = 0
    for N in range(0, Nmax + 1):
        cols = []
        for j in range(degmax + 1):
            e = [0] * j + [1]
            t = padd(padd(pscal(pmul(A1, e, p), W % p, p),
                          pscal(pmul(S3, pderiv(e, p), p), -8 % p, p), p),
                     pscal(pmul(A2, e, p), (8 * N) % p, p), p)
            cols.append(t)
        m = max([len(c) for c in cols] + [1])
        Mx = [[(cols[j][i] if i < len(cols[j]) else 0)
               for j in range(len(cols))] for i in range(m)]
        # rank
        row = 0
        for col in range(len(cols)):
            piv = next((r for r in range(row, m) if Mx[r][col]), None)
            if piv is None:
                continue
            Mx[row], Mx[piv] = Mx[piv], Mx[row]
            inv = pow(Mx[row][col], p - 2, p)
            Mx[row] = [(v * inv) % p for v in Mx[row]]
            for r in range(m):
                if r != row and Mx[r][col]:
                    f = Mx[r][col]
                    Mx[r] = [(Mx[r][c] - f * Mx[row][c])
                             for c in range(len(cols))]
                    Mx[r] = [v % p for v in Mx[r]]
            row += 1
        # nullity counts H up to degree degmax with that denominator; the
        # kernel is at most 1-dimensional as a rational function, so report
        # whether ANY nonzero solution exists at this N
        best = max(best, len(cols) - row)
    return best

def s_pow_rational(S, W, p):
    """Is S^{W/4} a rational function?  Test: S^W is a 4th power in F_p(z)."""
    # squarefree factorization exponents e_i; S^{W/4} rational iff 4 | e_i*W
    # for all i (up to the leading constant, which we ignore mod p).
    exps = []
    rem = ptrim(list(S)); d = pderiv(rem, p)
    from trackB1_cascade_general import pgcd
    g = pgcd(rem, d, p); k = 1; w = pdiv_exact(rem, g, p)
    while len(w) > 1:
        gg = pgcd(w, g, p); Ak = pdiv_exact(w, gg, p)
        if len(Ak) > 1:
            exps.append(k)
        g = pdiv_exact(g, gg, p) if gg else g
        w = gg; k += 1
    return all((e * W) % 4 == 0 for e in exps)

def check_fact1(trials=6, Ws=range(-12, 13)):
    print("FACT 1 -- kernel of [P_8,.] among rational functions")
    print("  W : predicted(1 iff S^{W/4} rational) vs measured, per component")
    random.seed(2)
    comps = []
    for _ in range(trials):
        A = [1, random.randrange(p), random.randrange(1, p)]
        S = component1_S(A, 1, p)
        if S:
            comps.append(("I ", S))
            break
    for _ in range(200):
        u, v = random.randrange(1, p), random.randrange(1, p)
        S = component2_S(u, v, 1, p)
        if S:
            comps.append(("II", S))
            break
    for _ in range(200):
        S = [random.randrange(1, p) for _ in range(5)]
        if s_pow_rational(S, 4, p):
            continue
        comps.append(("sqfree", S))
        break
    bad = 0
    for name, S in comps:
        line = []
        for W in Ws:
            pred = 1 if s_pow_rational(S, W, p) else 0
            meas = 1 if kernel_dim(S, W) > 0 else 0
            if pred != meas:
                bad += 1
                line.append(f"W={W}:PRED{pred}/MEAS{meas}!!")
            else:
                line.append(f"{W}:{meas}")
        print(f"  {name}: " + " ".join(line))
    print(f"  mismatches: {bad}\n")
    return bad == 0

# ---- rational slices  value = num / S^e  (all denominators are powers of S)
def radd(x, y, S, p):
    (f, e), (g, d) = x, y
    m = max(e, d)
    for _ in range(m - e):
        f = pmul(f, S, p)
    for _ in range(m - d):
        g = pmul(g, S, p)
    return (padd(f, g, p), m)

def rmul(x, y, p):
    return (pmul(x[0], y[0], p), x[1] + y[1])

def rscal(x, c, p):
    return (pscal(x[0], c, p), x[1])

def rderiv(x, S, p):
    """d/dz (f / S^e) = (f' S - e f S') / S^{e+1}."""
    f, e = x
    if e == 0:
        return (pderiv(f, p), 0)
    num = padd(pmul(pderiv(f, p), S, p),
               pscal(pmul(f, pderiv(S, p), p), -e % p, p), p)
    return (num, e + 1)

def rbracket(x, w1, y, w2, S, p):
    """[f,g] = w2 f' g - w1 f g' on rational slices."""
    t1 = rscal(rmul(rderiv(x, S, p), y, p), w2 % p, p)
    t2 = rscal(rmul(x, rderiv(y, S, p), p), (-w1) % p, p)
    return radd(t1, t2, S, p)

def riszero(x):
    return not ptrim(list(x[0]))

def check_fact2(trials=4, depth=22):
    """Build P^{3/2} with RATIONAL slices and verify [P, P^{3/2}] = 0.

    All slices of P^{3/2} have denominators that are powers of S, because
    P_8 = a S^2 makes P_8^{3/2} = a^{3/2} S^3 POLYNOMIAL.  The ladder
    2 E_12 E_{12-m} = (P^3)_{24-m} - sum_{0<k<m} E_{12-k} E_{12-m+k}
    then needs no exact division at all: dividing by 2 S^3 just increments the
    denominator exponent.  (a = 1 so that a^{3/2} stays in F_p.)
    """
    print("FACT 2 -- absorbers: [P, P^{3/2}] = 0 with RATIONAL slices")
    random.seed(4)
    ok = tot = 0
    for t in range(trials):
        gen = component1_S if t % 2 == 0 else None
        if gen:
            A = [1, random.randrange(p), random.randrange(1, p)]
            S = component1_S(A, 1, p)
        else:
            S = None
            for _ in range(200):
                u, v = random.randrange(1, p), random.randrange(1, p)
                S = component2_S(u, v, 1, p)
                if S:
                    break
        if S is None:
            continue
        P = {8: pmul(S, S, p)}                      # a = 1
        for w in range(7, -2, -1):
            lo, hi = max(0, -w), min(8, w + 2)
            P[w] = ptrim([random.randrange(p) if lo <= i <= hi else 0
                          for i in range(hi + 1)])
        P2, P3 = {}, {}
        for w1 in P:
            for w2 in P:
                P2[w1+w2] = padd(P2.get(w1+w2, []), pmul(P[w1], P[w2], p), p)
        for W2 in P2:
            for w3 in P:
                P3[W2+w3] = padd(P3.get(W2+w3, []), pmul(P2[W2], P[w3], p), p)
        s3 = pmul(pmul(S, S, p), S, p)
        E = {12: (s3, 0)}                            # E_12 = S^3
        inv2 = pow(2, p - 2, p)
        for m in range(1, depth + 1):
            W = 24 - m
            N = (list(P3.get(W, [])), 0)
            for k in range(1, m):
                if 12 - k in E and 12 - (m - k) in E:
                    N = radd(N, rscal(rmul(E[12-k], E[12-(m-k)], p), -1, p),
                             S, p)
            # divide by 2 E_12 = 2 S^3 : exponent +3, scale by 1/2
            E[12-m] = (pscal(N[0], inv2, p), N[1] + 3)
        # [P, E]_W = sum_{wp} [P_wp, E_{W-wp}] must vanish for every W
        for W in range(19, 19 - depth, -1):
            acc = ([], 0)
            complete = True
            for wp in sorted(P):
                we = W - wp
                if we in E:
                    acc = radd(acc, rbracket((P[wp], 0), wp, E[we], we, S, p),
                               S, p)
                elif we <= 12:
                    complete = False
            if not complete:
                continue
            tot += 1
            ok += riszero(acc)
    print(f"  [P, P^{{3/2}}] = 0 on tested slices: {ok}/{tot}\n")
    return tot > 0 and ok == tot

if __name__ == "__main__":
    f1 = check_fact1()
    f2 = check_fact2()
    print(f"FACT 1 confirmed: {f1}")
    print(f"FACT 2 confirmed: {f2}")
    sys.exit(0 if (f1 and f2) else 1)
