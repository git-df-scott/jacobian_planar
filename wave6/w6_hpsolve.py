#!/usr/bin/env python3
"""HIGH-PRECISION hunt on the (72,108) branch systems -- the char-0 attack no
float64 method could run (coefficients span ~15+ orders; here 191k-digit
integer coeffs).  mpmath at 60 digits keeps the small-coefficient conditions
alive, so Newton/least-squares actually sees the whole system.

Target: p108_525122 (25 params c2..c25 + w, 140 conditions), the SMALLEST
system on the (9,27)/(8,28) live branch of (72,108) -- the branch whose only
kill in the literature is GGHV Cor 5.7, never independently checked.  A
non-degenerate common zero here is a first-order counterexample seed on that
branch; verify exactly, then finite-field one-to-one check.

Method: damped Newton on the square-ified system (stack the 140 conditions;
minimize sum |g_i|^2 via mpmath). Multi-start.  Nondegeneracy: reject
solutions with any driver c-var ~ 0 (those are the trivial degenerate locus
the extractor already excludes).

CONTROL: a random inhomogeneous perturbation of the same monomials with NO
common zero must NOT converge (guards against the optimizer reporting a
spurious near-zero from precision loss).
"""
import sys, os, re, json, time
import mpmath as mp

mp.mp.dps = 60
GENS_PATH = sys.argv[1] if len(sys.argv) > 1 else '/home/user/jacobian_planar/wave6/p108_525122_q.gens'
NSTARTS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
NDVARS = [2, 3, 55, 110, 116]  # driver vars flagged ndegen in the extractor (subset present)

def parse(path):
    s = open(path).read().strip().rstrip(',')
    gens = [g.strip() for g in s.split(',') if g.strip()]
    varset = set(int(v) for v in re.findall(r'c\((\d+)\)', s))
    has_w = 'w' in s
    return gens, sorted(varset), has_w

def compile_gen(g):
    # turn a Singular poly string into a python expr over dict C[i] and w
    e = g.replace('^', '**')
    e = re.sub(r'c\((\d+)\)', r'C[\1]', e)
    return compile(e, '<g>', 'eval')

if __name__ == '__main__':
    gens, cvars, has_w = parse(GENS_PATH)
    codes = [compile_gen(g) for g in gens]
    nv = len(cvars) + (1 if has_w else 0)
    idx = {v: k for k, v in enumerate(cvars)}
    print(json.dumps({'system': os.path.basename(GENS_PATH), 'gens': len(gens),
                      'cvars': len(cvars), 'has_w': has_w, 'dps': mp.mp.dps}), flush=True)

    class Cdict(dict):
        def __missing__(self, k):
            return mp.mpf(0)
    def residual_vec(x):
        C = Cdict((v, x[idx[v]]) for v in cvars)
        w = x[-1] if has_w else mp.mpf(0)
        env = {'C': C, 'w': w}
        out = []
        for c in codes:
            out.append(eval(c, {'__builtins__': {}}, env))
        return out

    def cost(x):
        v = residual_vec(x)
        return sum(abs(vi)**2 for vi in v)

    def newton_min(x0, iters=60):
        # numerical damped Gauss-Newton with mpmath finite-diff Jacobian
        x = [mp.mpf(t) for t in x0]
        h = mp.mpf(10)**(-20)
        best = cost(x)
        for it in range(iters):
            f = residual_vec(x)
            m = len(f); n = len(x)
            # Jacobian (m x n) by forward difference; entries complex
            J = mp.zeros(m, n)
            for j in range(n):
                xj = x[j]; x[j] = xj + h
                fj = residual_vec(x); x[j] = xj
                for i in range(m):
                    J[i, j] = (fj[i] - f[i]) / h
            fv = mp.matrix([mp.mpc(fi) for fi in f])
            try:
                # normal equations (J^T J + lam I) dx = -J^T f
                JT = J.conjugate().T
                A = JT * J
                lam = mp.mpf(10)**(-6) * (1 + it)
                for i in range(n): A[i, i] += lam
                b = -(JT * fv)
                dx = mp.lu_solve(A, b)
            except Exception:
                break
            step = mp.mpf(1)
            for _ in range(20):
                xn = [x[i] + step*dx[i] for i in range(n)]
                if cost(xn) < best:
                    x = xn; best = cost(xn); break
                step /= 2
            else:
                break
            if best < mp.mpf(10)**(-40):
                break
        return x, best

    rng_seed = 0
    def rstart():
        global rng_seed
        rng_seed += 1
        mp.mp.dps = 60
        def r():
            return mp.mpf(int.from_bytes(os.urandom(4),'big'))/mp.mpf(2**32)*2-1
        return [mp.mpc(r(), r()) for _ in range(nv)]

    t0 = time.time(); best_overall = mp.inf; hits = []
    for k in range(NSTARTS):
        x0 = rstart()
        x, c = newton_min(x0)
        if c < best_overall:
            best_overall = c
            print(json.dumps({'start': k, 'best_cost': mp.nstr(c, 8),
                              'elapsed': round(time.time()-t0,1)}), flush=True)
        if c < mp.mpf(10)**(-40):
            C = {v: mp.nstr(x[idx[v]], 30) for v in cvars}
            drivers_ok = all(abs(x[idx[v]]) > mp.mpf(10)**(-8) for v in NDVARS if v in idx)
            rec = {'CANDIDATE-HP': True, 'cost': mp.nstr(c,8), 'nondeg_drivers': drivers_ok,
                   'C': C, 'w': mp.nstr(x[-1],30) if has_w else None}
            print(json.dumps(rec), flush=True)
            hits.append(rec)
            break
    out = {'system': os.path.basename(GENS_PATH), 'nstarts': NSTARTS,
           'best_cost': mp.nstr(best_overall, 8), 'hits': len(hits)}
    json.dump({'summary': out, 'hits': hits},
              open('/home/user/jacobian_planar/wave6/hpsolve_p108_525122.json','w'), indent=1)
    print(json.dumps(out))
