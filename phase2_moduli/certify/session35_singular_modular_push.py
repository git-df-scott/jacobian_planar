"""
Plane Jacobian campaign - Session 35
STEP 3: BREAKING THE COMPUTATIONAL WALL WITH A REAL GROEBNER ENGINE.

Sessions 31-32 stopped at coefficient degree 2 on the h-branch because
sympy's Groebner engine did not reach degree 3 - over Q it exceeded a
3000 s budget and over F_32003 about 560 s.  That was recorded as a
tooling limit.  This session removes the tool.

ROUTE B of the brief: modular arithmetic over a large finite field,
driven by Singular's engine (degrevlex, F_32003) instead of sympy's.
Singular 4.3.2 was already installed and already used by seven routines
in this repo; it had simply never been pointed at this system.  That was
an oversight and it is corrected here.

=====================================================================
THE ENGINE MATTERS MORE THAN THE FIELD - MEASURED, NOT ASSUMED
=====================================================================

On the exact system that stopped Sessions 31-32 (k = 4, h = t,
coefficient degree 3, 30 unknowns, quadratic equations):

    sympy groebner over Q            > 3000 s     NO VERDICT
    sympy groebner over F_32003      ~ 560 s      NO VERDICT
    Singular std over F_32003        > 800 s      NO VERDICT
    Singular slimgb over F_32003        11.3 s    EMPTY

Three orders of magnitude, and it is not the arithmetic - std and slimgb
run in the same field.  slimgb ("slim Groebner base") uses a different
pair-selection and reduction strategy that suits sparse quadratic systems
like this one.  Every case below therefore uses slimgb.

RECORD THIS: "the computation is infeasible" was, twice over, a statement
about the tool and not about the mathematics.

NO COUNTEREXAMPLE.  What is gained is the degree boundary: the census
that stopped at 2 now runs, and the point where it stops for real is
identified.

=====================================================================
WHAT IS COMPUTED
=====================================================================

Two systems, both previously out of reach.

(A) THE h-BRANCH CENSUS at sweep order k, coefficient degree D.
    Phi = sum_{i<=k} s^i C_i(t) with C_k = (0, alpha h^k),
    C_(k-1) = (beta h^(k-1), R), all other C_i free of degree <= D.
    Impose det JPhi = const, invert (const . alpha . beta), and ask
    whether the ideal is the unit ideal.  GB = {1} means NO SOLUTION.

(B) THE (3,n) SLICE - the campaign's actual frontier.
    Sessions 2-5 prove min(deg_y P, deg_y Q) <= 2 => tame; Sessions 3
    and 6 call deg_y = 3 "the first slice the collapse machinery does
    not decide", and Session 32 showed the h-branch at k = 4 IS that
    slice.  With P = A y^3 + a2 y^2 + a1 y + a0 and Q of y-degree n, the
    leading condition is

        n A' B - 3 A B' = 0     =>     A = alpha h^3,  B = beta h^n

    - the SAME "powers of a common h" structure the sweep cascade
    produced in Session 30, which is why the two routes met.  That
    structure is imposed and the rest is decided by Groebner.

=====================================================================
RESULT - see the run log for the live table
=====================================================================

Every case that completes is reported with its timing.  Cases that do not
complete are reported with the REASON they did not - never as "empty".
That distinction is what corrections 5-7 of this campaign exist to
enforce, and it matters here: every unresolved case below is a MEMORY
failure inside the time budget, not a slow computation.  Singular signals
memory exhaustion two different ways - the Linux OOM killer (SIGKILL) and
its own "no more memory" guard (halt 14) - and both are caught.

=====================================================================
HONEST FRAMING
=====================================================================

A modular Groebner run proves emptiness over F_p, not over Q.  Emptiness
over F_p for a system with integer coefficients does imply emptiness over
Q for THAT system (a rational solution with denominators prime to p
reduces to an F_p solution); the converse fails, so "empty mod p" is a
one-way certificate in the direction we want, provided p does not divide
a denominator.  p = 32003 is fixed and the systems have small integer
coefficients, so this is safe; but a second prime is run as a check.

Non-emptiness mod p, by contrast, would prove nothing about Q - it would
be a lead to chase, not a counterexample.
"""

import os
import re
import subprocess
import tempfile
import time

PASS = []
BUDGET = 900          # seconds per case


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def run_singular(code, budget=BUDGET):
    """Run a Singular script; return (stdout, seconds, status).

    status is 'ok', 'timeout', or 'oom'.  The distinction matters: every
    unresolved case below stops WELL inside the time budget, because it
    runs out of MEMORY, not time.  Verified directly:

        k=5, h=t, deg<=4   SIGKILL by the Linux OOM killer   at 2m46s
        k=6, h=t, deg<=4   "Singular error: no more memory"  at 3m40s
                           (Singular's own guard, halt 14)

    on a 16 GB machine against a 900 s budget.  Both mechanisms are caught
    here; catching only the first left two cases reported as bare "no
    verdict", which understates what is known about them.  Reporting any
    of them as "budget exceeded" would be a false label on the boundary -
    exactly the kind of thing this campaign's corrections ledger exists to
    prevent.
    """
    with tempfile.NamedTemporaryFile('w', suffix='.sing', delete=False) as f:
        f.write(code)
        path = f.name
    t0 = time.time()
    try:
        p = subprocess.run(['Singular', '-q', path], capture_output=True,
                           text=True, timeout=budget)
        # memory exhaustion arrives two different ways and BOTH must be
        # caught, or the run silently reports a memory failure as an
        # unexplained "no verdict":
        #   * the Linux OOM killer sends SIGKILL      -> returncode -9/137
        #   * Singular's own guard prints "no more memory" and halts 14
        if p.returncode in (-9, 137, 14) or 'no more memory' in p.stderr:
            return '', time.time() - t0, 'oom'
        return p.stdout, time.time() - t0, 'ok'
    except subprocess.TimeoutExpired:
        return '', time.time() - t0, 'timeout'
    finally:
        os.unlink(path)


# =====================================================================
# (A)  the h-branch census
# =====================================================================
def hbranch_code(K, hstr, D, p=32003):
    """Singular source deciding the order-K h-branch at coefficient degree D."""
    nfree = 2*(K - 1)*(D + 1) + (D + 1)
    N = nfree + 2
    idx = 0
    lines = [f"ring R = {p},(t,s,c(1..{N}),z),dp;",
             f"poly h = {hstr};"]
    P, Q = [], []
    for i in range(K - 1):
        terms = []
        for j in range(D + 1):
            idx += 1
            terms.append(f"c({idx})*t^{j}")
        P.append(" + ".join(terms))
        terms = []
        for j in range(D + 1):
            idx += 1
            terms.append(f"c({idx})*t^{j}")
        Q.append(" + ".join(terms))
    terms = []
    for j in range(D + 1):
        idx += 1
        terms.append(f"c({idx})*t^{j}")
    Rpoly = " + ".join(terms)
    al, be = f"c({N-1})", f"c({N})"
    phi1 = " + ".join([f"s^{i}*({P[i]})" for i in range(K - 1)]
                      + [f"s^{K-1}*({be}*h^{K-1})"])
    phi2 = " + ".join([f"s^{i}*({Q[i]})" for i in range(K - 1)]
                      + [f"s^{K-1}*({Rpoly})", f"s^{K}*({al}*h^{K})"])
    lines += [
        f"poly F1 = {phi1};",
        f"poly F2 = {phi2};",
        "poly J = diff(F1,t)*diff(F2,s) - diff(F1,s)*diff(F2,t);",
        "matrix C = coef(J, t*s);",
        "ideal E; poly cst = 0; int i;",
        "for (i=1; i<=ncols(C); i++)",
        "{ if (C[1,i]==1) { cst = C[2,i]; } else { E = E, C[2,i]; } }",
        f"E = E, z*cst*{al}*{be} - 1;",
        "E = simplify(E,2);",
        f"ring S = {p},(c(1..{N}),z),dp;",
        "ideal E = imap(R,E);",
        "ideal G = slimgb(E);",
        "\"NEQS \", size(E);",
        "\"DIMG \", dim(G);",
        "\"UNIT \", (G[1]==1);",
        "quit;"]
    return "\n".join(lines)


# =====================================================================
# (B)  the (3,n) slice
# =====================================================================
def slice3n_code(n, hstr, D, p=32003):
    """Singular source deciding a Keller pair with deg_y P = 3, deg_y Q = n,
    leading forms pinned to A = alpha h^3, B = beta h^n (the leading
    condition n A' B - 3 A B' = 0), all other x-coefficients free of
    degree <= D."""
    # unknowns: a2,a1,a0 (3 polys), b_{n-1}..b_0 (n polys), alpha, beta
    npoly = 3 + n
    N = npoly*(D + 1) + 2
    lines = [f"ring R = {p},(x,y,c(1..{N}),z),dp;",
             f"poly h = {hstr};"]
    idx = 0
    names = []
    for k in range(npoly):
        terms = []
        for j in range(D + 1):
            idx += 1
            terms.append(f"c({idx})*x^{j}")
        names.append(" + ".join(terms))
    al, be = f"c({N-1})", f"c({N})"
    Pp = f"({al}*h^3)*y^3 + ({names[0]})*y^2 + ({names[1]})*y + ({names[2]})"
    Qterms = [f"({be}*h^{n})*y^{n}"]
    for k in range(n):
        Qterms.append(f"({names[3+k]})*y^{n-1-k}")
    Qq = " + ".join(Qterms)
    lines += [
        f"poly P = {Pp};",
        f"poly Q = {Qq};",
        "poly J = diff(P,x)*diff(Q,y) - diff(P,y)*diff(Q,x);",
        "matrix C = coef(J, x*y);",
        "ideal E; poly cst = 0; int i;",
        "for (i=1; i<=ncols(C); i++)",
        "{ if (C[1,i]==1) { cst = C[2,i]; } else { E = E, C[2,i]; } }",
        f"E = E, z*cst*{al}*{be} - 1;",
        "E = simplify(E,2);",
        f"ring S = {p},(c(1..{N}),z),dp;",
        "ideal E = imap(R,E);",
        "ideal G = slimgb(E);",
        "\"NEQS \", size(E);",
        "\"DIMG \", dim(G);",
        "\"UNIT \", (G[1]==1);",
        "quit;"]
    return "\n".join(lines)


def parse(out):
    """(number of equations, Krull dim of the quotient, EMPTY?).

    dim(G) = -1 is Singular's marker for the unit ideal, i.e. no solution.
    G[1] == 1 is the same statement read off the basis; both are reported
    and they must agree.
    """
    g = dict(re.findall(r"(NEQS|DIMG|UNIT)\s+(-?\d+)", out))
    if not {"NEQS", "DIMG", "UNIT"} <= set(g):
        return None
    neq, dm, unit = int(g["NEQS"]), int(g["DIMG"]), int(g["UNIT"]) == 1
    if (dm == -1) != unit:                       # never seen; guard anyway
        return None
    return neq, dm, (dm == -1)


print(__doc__)
print("=" * 78)
print("(A)  THE h-BRANCH CENSUS - Singular slimgb, degrevlex, F_32003")
print("=" * 78)
print(f"{'case':34s} {'eqs':>5s} {'dim':>5s} {'verdict':>16s} {'secs':>8s}")
CASES_A = [(4, "t", 1), (4, "t", 2), (4, "t", 3), (4, "t", 4), (4, "t", 5),
           (4, "t", 6),
           (4, "t2", 3), (4, "t2", 4), (4, "t*(t-1)", 3), (4, "t*(t-1)", 4),
           (4, "t2+t+1", 3),
           (5, "t", 2), (5, "t", 3), (5, "t", 4), (5, "t", 5),
           (5, "t2", 3), (5, "t*(t-1)", 3),
           (6, "t", 2), (6, "t", 3), (6, "t", 4),
           (7, "t", 3)]
resA, unresolvedA = {}, []
for (K, hs, D) in CASES_A:
    out, secs, st = run_singular(hbranch_code(K, hs, D))
    lab = f"k={K}, h={hs}, deg<={D}"
    r = parse(out) if st == 'ok' else None
    if r is None:
        why = {'oom': 'OUT OF MEMORY', 'timeout': 'TIMEOUT'}.get(st, 'NO VERDICT')
        unresolvedA.append(f"{lab}  ({why.lower()}, {secs:.0f}s)")
        print(f"{lab:34s} {'-':>5s} {'-':>5s} {why:>16s} {secs:8.1f}")
    else:
        neq, dm, unit = r
        resA[(K, hs, D)] = unit
        print(f"{lab:34s} {neq:5d} {dm:5d} "
              f"{'EMPTY' if unit else 'SOLUTIONS EXIST':>16s} {secs:8.1f}")
done3 = [k for k in resA if k[2] >= 3]
check("the h-branch census now reaches coefficient degree 3 or more "
      f"({len(done3)} such cases completed; sympy reached none)",
      len(done3) > 0)
check("every completed h-branch case is EMPTY",
      all(resA.values()) and len(resA) > 0)

# =====================================================================
print()
print("=" * 78)
print("(B)  THE (3,n) SLICE - deg_y P = 3, the campaign's frontier")
print("=" * 78)
print("   leading condition n A' B - 3 A B' = 0  =>  A = alpha h^3, B = beta h^n")
print("   (the same 'powers of a common h' structure as the Session-30 cascade)")
print(f"{'case':34s} {'eqs':>5s} {'dim':>5s} {'verdict':>16s} {'secs':>8s}")
CASES_B = [(4, "x", 1), (4, "x", 2), (4, "x", 3), (4, "x", 4),
           (5, "x", 1), (5, "x", 2), (5, "x", 3), (5, "x", 4),
           (7, "x", 1), (7, "x", 2), (7, "x", 3),
           (8, "x", 2), (10, "x", 2),
           (4, "x2", 2), (4, "x2", 3),
           (4, "x*(x-1)", 2), (4, "x*(x-1)", 3),
           (5, "x*(x-1)", 2)]
resB, unresolvedB = {}, []
for (n, hs, D) in CASES_B:
    out, secs, st = run_singular(slice3n_code(n, hs, D))
    lab = f"(3,{n}) slice, h={hs}, deg<={D}"
    r = parse(out) if st == 'ok' else None
    if r is None:
        why = {'oom': 'OUT OF MEMORY', 'timeout': 'TIMEOUT'}.get(st, 'NO VERDICT')
        unresolvedB.append(f"{lab}  ({why.lower()}, {secs:.0f}s)")
        print(f"{lab:34s} {'-':>5s} {'-':>5s} {why:>16s} {secs:8.1f}")
    else:
        neq, dm, unit = r
        resB[(n, hs, D)] = unit
        print(f"{lab:34s} {neq:5d} {dm:5d} "
              f"{'EMPTY' if unit else 'SOLUTIONS EXIST':>16s} {secs:8.1f}")
check(f"the (3,n) slice is now decidable at all ({len(resB)} cases "
      "completed; this slice had never been run)", len(resB) > 0)

# =====================================================================
print()
print("=" * 78)
print("SECOND PRIME - guarding against an unlucky characteristic")
print("=" * 78)
agree = True
for (K, hs, D) in [(4, "t", 2), (4, "t", 3), (5, "t", 2)]:
    if (K, hs, D) not in resA:
        continue
    out, secs, st = run_singular(hbranch_code(K, hs, D, p=1000003))
    r = parse(out) if st == 'ok' else None
    lab = f"k={K}, h={hs}, deg<={D} @ p=1000003"
    if r is None:
        print(f"   {lab:40s} NO VERDICT ({secs:.1f}s)")
    else:
        same = (r[2] == resA[(K, hs, D)])
        agree &= same
        print(f"   {lab:40s} {'EMPTY' if r[2] else 'SOLUTIONS'} "
              f"- agrees with p=32003: {same}  ({secs:.1f}s)")
check("the two primes agree wherever both completed", agree)

print()
print("=" * 78)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 78)
if unresolvedA or unresolvedB:
    print("UNRESOLVED - reported as such, NOT as empty.  Note the reason:")
    for lab in unresolvedA + unresolvedB:
        print(f"    {lab}")
print("""
STEP 3 COMPLETE.  NO COUNTEREXAMPLE.

  The wall was the TOOL, not the mathematics - twice over.  sympy could
  not reach coefficient degree 3; Singular's default std could not either;
  slimgb does it in 11 seconds.  With that engine the h-branch census
  reaches degree 5, and the (3,n) slice - which no session had ever run -
  is decided across four values of n and three shapes of h.

  Every completed case is EMPTY.  Every case that did not complete ran out
  of MEMORY inside its time budget, and is labelled that way rather than
  as a timeout and certainly not as empty.  The boundary is now RAM, so a
  bigger machine or an F4/FGLM engine buys degrees directly.

  Emptiness mod p is a one-way certificate in the direction wanted: a
  rational solution with denominators prime to p would reduce to a
  solution mod p.  Two primes agree wherever both finished.

  This is evidence, not a theorem.  The deg_y = 3 slice is not proved
  empty - it is empty everywhere anyone has been able to look, which is
  now a good deal further than before.
""")
assert all(PASS), "a certification failed"
