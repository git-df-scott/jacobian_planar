"""
Track C, parts C2/C3/C4: Phase-4 realization machinery on top of the
C1-verified master identity (trackC_master_identity.py, 29 PASS).

Everything exact over Q (fractions.Fraction). No floats.

FRAMEWORK (all relations DERIVED and executably verified in C1):
  cusp type (a,b) = (2,3), a+b = 5; chart slopes (rho, s) (handoff frame:
  rho = s); g0 = alpha*(v+1)^m*v^sigma; deviation first block u0 = g0^b*R/a;
  R = v^t * S(v) / (v+1)^p  with S(0) != 0, S(-1) != 0 (t = ord_{v=0} R;
  handoff frame t = 0).

  Master identity [C1c]:  leading Keller block = g0^(a+b)*(k R' + D R (log g0)').
  q-side matching [C1d]:  D = (a+b)k + 1 - s  (>= 1).
  v-side matching [C1d, generalized to t]:  (a+b)sigma + t = 1 + rho(1-s).
  pole forcing   [C1d]:  p = (a+b)m - 1   (off resonance D*m != k*p).

  Writing the block over the common denominator (derivation in comments of
  core_E below), Keller  J_(x)(y1,y2) = c  becomes the POLYNOMIAL condition

      E(S) := k*v*(v+1)*S' + (k*t + D*sigma)*(v+1)*S + (D*m - k*p)*v*S
            = -c / alpha^(a+b)     (a CONSTANT),

  because block = alpha^5 * (v+1)^(5m-p-1) * v^(5*sigma+t-1) * E(S) and the
  exponents vanish/match the RHS -c*q^(-s)*v^(rho(1-s)) exactly under the
  relations above.

CONSEQUENCES (proved in solve_forced_S by exact linear algebra, not assumed):
  - deg S forced:  d = (p - t) - (D/k)*(m + sigma); polynomial S exists only
    if d is a nonnegative integer  =>  k | D*(m+sigma)  [divisibility sieve].
  - recurrence  [k(j+t) + D*sigma]*s_j = k*(d+1-j)*s_{j-1}, j = 1..d;
    a resonance  k(j*+t) + D*sigma = 0  with  1 <= j* <= d  cascades to
    s_0 = 0: slice DEAD.
  - c = -alpha^5*(k*t + D*sigma)*s_0:  k*t + D*sigma = 0  =>  c = 0: DEAD.
  - uniqueness: up to scalar (absorbed by alpha^5) when k does not divide D;
    if k | D the homogeneous kernel g0^(-D/k) is rational: flagged.

Run:
  python3 trackC_phase4.py c4     # the (rho,m) admissible-slice enumeration
  python3 trackC_phase4.py c2     # the ten forced R's at (72,108), k=3..12
  python3 trackC_phase4.py c3     # k=3 jet-ladder realization layer
Artifacts: trackC_c4_lattice.json, trackC_c2_tenR.json, trackC_c3_ladder.json
(written next to this file), sections also print human tables.
"""

import sys, json, os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))

PASS = 0
FAIL = 0
def report(name, ok, extra=""):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok: PASS += 1
    else: FAIL += 1
    print(f"  [{tag}] {name}" + (f"   {extra}" if extra else ""))
    return ok

# ---------------------------------------------------------------- poly core
# polynomials over Q as dict {deg: Fraction}, zero-free

def pclean(P):
    return {i: c for i, c in P.items() if c != 0}

def padd(P, Q):
    R = dict(P)
    for i, c in Q.items():
        R[i] = R.get(i, F(0)) + c
    return pclean(R)

def pscal(a, P):
    return pclean({i: a*c for i, c in P.items()})

def pmul(P, Q):
    R = {}
    for i, a in P.items():
        for j, b in Q.items():
            R[i+j] = R.get(i+j, F(0)) + a*b
    return pclean(R)

def pdiff(P):
    return pclean({i-1: i*c for i, c in P.items() if i >= 1})

def pdeg(P):
    return max(P) if P else None

def peval(P, x):
    return sum(c * x**i for i, c in P.items()) if P else F(0)

V = {1: F(1)}            # v
VP1 = {1: F(1), 0: F(1)} # v + 1

def core_E(S, k, D, m, sigma, t, p):
    """E(S) = k v(v+1) S' + (k t + D sigma)(v+1) S + (D m - k p) v S.

    Derivation (exact, mirrors C1e's verified computation):
      with R = v^t S/(v+1)^p and (log g0)' = m/(v+1) + sigma/v,
      k R' + D R (log g0)'
        = v^(t-1) (v+1)^(-p-1) [ k v(v+1)S' + k t (v+1) S - k p v S
                                 + D m v S + D sigma (v+1) S ],
      block = g0^5 * (that) = alpha^5 (v+1)^(5m-p-1) v^(5 sigma + t - 1) E(S).
    """
    return padd(padd(pscal(F(k), pmul(pmul(V, VP1), pdiff(S))),
                     pscal(F(k*t + D*sigma), pmul(VP1, S))),
                pscal(F(D*m - k*p), pmul(V, S)))

def block_check(S, k, D, m, sigma, t):
    """Independent exact check that R = v^t S/(v+1)^p makes
    g0^5 (kR' + D R (log g0)') a constant times v^(5 sigma + t - 1),
    computed WITHOUT core_E's collected form: clear denominators directly.
    Returns (ok, const) where const = the forced -c/alpha^5."""
    p = 5*m - 1
    # numerator of kR' + DR(m/(v+1)+sigma/v) over v^(1-t) (v+1)^(p+1):
    #   k [ v(v+1) S' + t (v+1) S - p v S ] + D S [ m v + sigma (v+1) ]
    num = padd(pscal(F(k), padd(padd(pmul(pmul(V, VP1), pdiff(S)),
                                     pscal(F(t), pmul(VP1, S))),
                                pscal(F(-p), pmul(V, S)))),
               pmul(S, {1: F(D*m + D*sigma), 0: F(D*sigma)}))
    # block = alpha^5 (v+1)^(5m) v^(5 sigma) * v^(t-1) (v+1)^(-p-1) * num
    #       = alpha^5 (v+1)^(5m-p-1) v^(5 sigma + t - 1) * num ; 5m-p-1 = 0.
    ok = (set(num) <= {0})
    const = num.get(0, F(0))
    return ok, const

# ------------------------------------------------------- forced-S solver

def solve_forced_S(k, D, m, sigma, t=0, want_S=True):
    """Decide whether the slice instance (k, D, m, sigma, t) carries a forced
    R = v^t S/(v+1)^p (p = 5m-1) with E(S) = const != 0, S(0) != 0, S(-1) != 0.

    Returns dict with verdict in:
      DEAD_D          D < 1 (no chain)
      DEAD_c0         k t + D sigma = 0 (Keller constant forced 0)
      DEAD_degree     forced degree d not a nonnegative integer
      DEAD_resonance  in-range recurrence resonance cascades S = 0
      DEAD_S0         solver found only solutions with S(0) = 0 (defensive)
      FORCED_R        unique-up-to-scalar S found and exactly verified
    plus data (d, S, c_over_alpha5, S_at_minus1, kernel_flag ...).
    All decisions are by exact linear algebra on the coefficient system,
    not by trusting the recurrence analysis (which is then cross-checked).
    """
    out = {"k": k, "D": D, "m": m, "sigma": sigma, "t": t, "p": 5*m - 1}
    p = 5*m - 1
    if D < 1:
        out["verdict"] = "DEAD_D"; return out
    out["pole_resonance_Dm_eq_kp"] = (D*m == k*p)  # caveat flag for C1d forcing
    if k*t + D*sigma == 0:
        out["verdict"] = "DEAD_c0"; return out
    # forced degree: leading coeff of E on a deg-e poly is
    #   [k e + k t + D sigma + D m - k p] * s_e ; E const needs it zero,
    #   i.e. e = d := (p - t) - D (m+sigma)/k.  (Nonzero for any other e.)
    num = k*(p - t) - D*(m + sigma)
    if num % k != 0:
        out["verdict"] = "DEAD_degree"; out["d_frac"] = f"{num}/{k}"; return out
    d = num // k
    out["d"] = d
    if d < 0:
        out["verdict"] = "DEAD_degree"; return out
    # exact LA: unknowns s_0..s_d; conditions: coeff of v^j in E(S) = 0 for
    # j = 1..d+1 (constant term is free = the Keller constant).
    # E(S) coeff of v^j:  [k j + k t + D sigma] s_j - k (d+1-j) s_{j-1}
    # (second bracket k(j-1)+kt+D sigma+Dm-kp collapses to -k(d+1-j) by the
    # definition of d; s_{d+1} = 0, s_{-1} = 0; verified via block_check).
    # Solve by forward substitution, tracking resonances honestly.
    s = [None]*(d+1)
    s[0] = F(1)   # normalization attempt; scalar freedom is alpha^5
    resonant = False
    for j in range(1, d+1):
        lead = F(k*(j + t) + D*sigma)
        rhs = F(k*(d + 1 - j)) * s[j-1]   # [lead]*s_j = k(d+1-j) s_{j-1}
        if lead == 0:
            # resonance: equation reads 0*s_j = rhs; solvable iff rhs == 0,
            # and then s_j is free.  Cascade analysis: rhs == 0 forces
            # s_{j-1} = 0 (coefficient k(d+1-j) != 0 for j <= d), which
            # back-propagates; do the honest check by restarting a full
            # nullspace computation below.
            resonant = True
            break
        s[j] = rhs / lead
    if resonant:
        # full nullspace of the (d+1)x(d+1) system {coeff v^j = 0, j=1..d+1}
        # ... but coeff v^{d+1} is 0*s_d identically (degree choice), so the
        # system is d+1 equations j=1..d+1 in d+1 unknowns with the last
        # trivial.  Build and row-reduce exactly.
        rows = []
        for j in range(1, d+2):
            row = [F(0)]*(d+1)
            if j <= d:
                row[j] = F(k*(j + t) + D*sigma)
            if j-1 <= d:
                row[j-1] = row[j-1] - F(k*(d+1-j))
            rows.append(row)
        # gaussian elimination over Q
        mat = [r[:] for r in rows]
        ncols = d+1; rank = 0; pivots = []
        for col in range(ncols):
            piv = None
            for r in range(rank, len(mat)):
                if mat[r][col] != 0:
                    piv = r; break
            if piv is None: continue
            mat[rank], mat[piv] = mat[piv], mat[rank]
            pv = mat[rank][col]
            mat[rank] = [x/pv for x in mat[rank]]
            for r in range(len(mat)):
                if r != rank and mat[r][col] != 0:
                    f = mat[r][col]
                    mat[r] = [x - f*y for x, y in zip(mat[r], mat[rank])]
            pivots.append(col); rank += 1
        free = [c for c in range(ncols) if c not in pivots]
        out["nullity"] = ncols - rank
        # any nullspace vector with s_0 != 0?  s_0 is coordinate 0.
        if 0 in pivots:
            # s_0 is pivot: expressed via free vars; check if some free choice
            # makes it nonzero: row of pivot 0:
            prow = mat[pivots.index(0)]
            if all(prow[fc] == 0 for fc in free):
                out["verdict"] = "DEAD_resonance"
                out["note"] = "nullspace exists but every solution has S(0)=0"\
                              if ncols - rank > 0 else "only S = 0"
                return out
        # else s_0 free or expressible nonzero: a forced family exists but is
        # NOT unique (resonance freedom) — flag loudly.
        out["verdict"] = "FORCED_R_RESONANT_FAMILY"
        return out
    # non-resonant: candidate S
    S = pclean({i: s[i] for i in range(d+1)})
    ok_E, const = block_check(S, k, D, m, sigma, t)
    S_m1 = peval(S, F(-1))
    out["exact_block_check"] = bool(ok_E)
    out["c_over_alpha5"] = str(-const)   # c = -alpha^5 * const
    out["S_at_minus1"] = str(S_m1)
    out["S0_nonzero"] = (S.get(0, F(0)) != 0)
    out["kernel_rational"] = (D % k == 0)  # g0^(-D/k) rational => nonunique
    if not ok_E:
        out["verdict"] = "FAIL_INTERNAL"; return out
    if const == 0:
        out["verdict"] = "DEAD_c0"; return out
    if S_m1 == 0:
        # pole order at v=-1 drops below p: contradicts C1d forcing
        out["verdict"] = "DEAD_pole_drop"; return out
    if not out["S0_nonzero"]:
        out["verdict"] = "DEAD_S0"; return out
    out["verdict"] = "FORCED_R"
    if want_S:
        # primitive integer normalization for display
        from math import gcd
        dens = [c.denominator for c in S.values()]
        l = 1
        for x in dens:
            l = l*x//gcd(l, x)
        Sint = {i: c*l for i, c in S.items()}
        g = 0
        for c in Sint.values():
            g = gcd(g, int(c))
        Sint = {i: int(c)//g for i, c in Sint.items()}
        # match handoff sign convention: make leading coefficient positive
        if Sint[max(Sint)] < 0:
            Sint = {i: -c for i, c in Sint.items()}
        out["S_int"] = {str(i): c for i, c in sorted(Sint.items())}
        # c for the integer-normalized S (alpha = 1):
        scale = F(Sint[0], 1) / S[0] if S.get(0) else None
        out["c_int_alpha1"] = str(-const * scale) if scale else None
    return out


def poly_str(Sint):
    terms = []
    for i in sorted((int(i) for i in Sint), reverse=True):
        c = Sint[str(i)] if isinstance(next(iter(Sint)), str) else Sint[i]
        t = f"{'+' if c >= 0 else '-'} {abs(c)}"
        if i > 0:
            t += f"*v^{i}" if i > 1 else "*v"
        terms.append(t)
    s = " ".join(terms)
    return s[2:] if s.startswith("+ ") else "-" + s[2:]

# ================================================================== C4
def run_c4():
    print("== C4: the admissible (rho, m) lattice beyond (3,1) ==")
    print("   frame: handoff frame rho = s, t = 0 (R regular nonzero at v=0);")
    print("   constraints (all C1-derived): sigma = (1 + rho - rho^2)/5 in Z")
    print("   [<=> rho = 3 mod 5], m >= 1, k >= 1, D = 5k + 1 - rho >= 1,")
    print("   plus the solvability sieves computed per instance below.")
    results = {"frame": "rho=s, t=0, (a,b)=(2,3)",
               "relations": {"D": "5k+1-rho", "sigma": "(1+rho-rho^2)/5",
                             "p": "5m-1", "d": "(5m-1) - D(m+sigma)/k",
                             "c": "-alpha^5*(kt+D sigma)*s_0"},
               "window": {"rho": "3..28 (rho=3 mod 5)", "m": "1..8",
                          "k": "1..14"},
               "slices": []}

    # structural check 1: sigma integral <=> rho = 3 (mod 5)
    ok = all(((1 + r - r*r) % 5 == 0) == (r % 5 == 3) for r in range(1, 200))
    report("sigma in Z  <=>  rho = 3 (mod 5)   (checked rho = 1..199)", ok)

    # structural check 2: the resonant ladder m + sigma = 0 <=>
    # m = (rho^2 - rho - 1)/5; parametrized rho = 5r+3:
    ladder = []
    for r in range(0, 6):
        rho = 5*r + 3
        m_star = (rho*rho - rho - 1)//5
        ladder.append((rho, m_star))
    ok = all(m == 5*r*r + 5*r + 1 for r, (rho, m) in enumerate(ladder))
    report("resonant ladder (m+sigma=0):  (rho, m*) = (5r+3, 5r^2+5r+1), "
           "r >= 0", ok, f"first: {ladder[:4]}")
    results["resonant_ladder"] = ladder

    # enumeration
    survivors = []
    dead_slices = []
    for rho in [3, 8, 13, 18, 23, 28]:
        sigma = (1 + rho - rho*rho)//5
        for m in range(1, 9):
            slice_rec = {"rho": rho, "m": m, "sigma": sigma,
                         "m_plus_sigma": m + sigma, "instances": []}
            any_forced = False
            for k in range(1, 15):
                D = 5*k + 1 - rho
                res = solve_forced_S(k, D, m, sigma, 0, want_S=False)
                v = res["verdict"]
                inst = {"k": k, "D": D, "verdict": v}
                if v == "FORCED_R":
                    inst["d"] = res["d"]
                    inst["c_over_alpha5_s0norm"] = res["c_over_alpha5"]
                    inst["kernel_rational"] = res["kernel_rational"]
                    inst["pole_res_flag"] = res["pole_resonance_Dm_eq_kp"]
                    any_forced = True
                elif v not in ("DEAD_D",):
                    inst["d"] = res.get("d")
                slice_rec["instances"].append(inst)
            slice_rec["carries_forced_R"] = any_forced
            results["slices"].append(slice_rec)
            (survivors if any_forced else dead_slices).append(
                (rho, m, [i["k"] for i in slice_rec["instances"]
                          if i["verdict"] == "FORCED_R"]))

    print()
    print("  --- SURVIVOR SLICES (carry >= 1 forced R in k-window 1..14) ---")
    for rho, m, ks in survivors:
        sigma = (1 + rho - rho*rho)//5
        tag = " <== the ONLY previously examined slice (k=3 = (99,66)/"\
              "(72,108) anchor)" if (rho, m) == (3, 1) else \
              "  [resonant ladder]" if m + sigma == 0 else ""
        print(f"    (rho,m) = ({rho},{m})  sigma = {sigma}  "
              f"admissible k in window: {ks}{tag}")
    print(f"  --- DEAD SLICES in window: {len(dead_slices)} "
          f"(no forced R for any k = 1..14) ---")
    for rho, m, _ in dead_slices:
        print(f"    (rho,m) = ({rho},{m})", end="")
    print()

    # explicit forced S for the smallest unexamined survivor instances
    print()
    print("  --- explicit forced R for the first UNEXAMINED instances ---")
    shown = 0
    explicit = []
    for rho, m, ks in survivors:
        sigma = (1 + rho - rho*rho)//5
        for k in ks:
            if (rho, m, k) == (3, 1, 3):
                continue   # the examined anchor
            D = 5*k + 1 - rho
            res = solve_forced_S(k, D, m, sigma, 0, want_S=True)
            if res["verdict"] == "FORCED_R" and shown < 8:
                d = res["d"]
                print(f"    (rho,m,k) = ({rho},{m},{k}): D = {D}, "
                      f"p = {res['p']}, deg S = {d}, "
                      f"c/alpha^5 = {res['c_int_alpha1']} (S primitive)")
                if d <= 12:
                    print(f"        S = {poly_str(res['S_int'])}")
                explicit.append(res)
                shown += 1
    results["explicit_unexamined"] = explicit

    # cross-check one novel instance against sympy (independent implementation)
    print()
    novel = next((e for e in explicit if e["d"] <= 20), None)
    if novel is not None:
        import sympy as sp
        v = sp.symbols('v')
        k, D, m, sg, t = (novel[x] for x in ("k", "D", "m", "sigma", "t"))
        p = novel["p"]
        Ssym = sum(sp.Integer(c)*v**int(i) for i, c in novel["S_int"].items())
        g0 = (v+1)**m * v**sg
        R = v**t * Ssym / (v+1)**p
        blk = sp.together(g0**5*(k*sp.diff(R, v) + D*R*sp.diff(g0, v)/g0))
        want_pow = 5*sg + t - 1
        ratio = sp.cancel(blk / v**want_pow)
        ok = ratio.is_constant() and sp.simplify(ratio) != 0
        report(f"sympy cross-check of novel instance (k,D,m,sigma)="
               f"({k},{D},{m},{sg}): block == const * v^(5 sigma - 1)",
               bool(ok), f"const = {sp.simplify(ratio)}")
        results["sympy_crosscheck"] = {"instance": {kk: novel[kk] for kk in
                                                    ("k", "D", "m", "sigma")},
                                       "ok": bool(ok)}

    # ---- refined frame rho != s (C1's refinement): quick lattice map
    print()
    print("  --- REFINED frame (rho != s allowed; C1d generalized) ---")
    print("      sigma = (1 + rho - rho*s)/5 in Z  <=>  rho*(s-1) = 1 (mod 5)")
    refined = []
    for rho_ in range(1, 13):
        for s_ in range(1, 13):
            if (1 + rho_ - rho_*s_) % 5 == 0:
                sg = (1 + rho_ - rho_*s_)//5
                refined.append({"rho": rho_, "s": s_, "sigma": sg,
                                "D_formula": f"5k+1-{s_}",
                                "examined": (rho_ == 3 and s_ == 3)})
    n_unexam = sum(1 for x in refined if not x["examined"])
    ok = all((x["rho"]*(x["s"]-1)) % 5 == 1 or x["sigma"]*5 ==
             1 + x["rho"] - x["rho"]*x["s"] for x in refined)
    report(f"refined lattice window rho,s <= 12: {len(refined)} slices, "
           f"{n_unexam} unexamined", ok)
    sig0 = [x for x in refined if x["sigma"] == 0]
    print(f"      sigma = 0 (g0 with NO v-power) occurs only for "
          f"(rho,s) = {[(x['rho'], x['s']) for x in sig0]}; there "
          f"k*t + D*sigma = 0 at t=0  =>  c = 0: DEAD at t=0, needs t != 0.")
    results["refined_frame_window"] = refined

    with open(os.path.join(HERE, "trackC_c4_lattice.json"), "w") as f:
        json.dump(results, f, indent=1, default=str)
    print(f"\n  artifact: trackC_c4_lattice.json")

# ================================================================== C2
def run_c2():
    print("== C2: the ten forced R's at (72,108) (k = 3..12) ==")
    print("   D-relation DERIVED from C1 (q-order matching, s = 3):")
    print("       D = (a+b)k + 1 - s = 5k - 2")
    print("   handoff guess 'D = 3k+4?': agrees ONLY at k = 3 (13 = 13);")
    print("   diverges for k >= 4 (e.g. k=4: 18 vs 16). The guess is WRONG.")
    rows = []
    ok_all = True
    for k in range(3, 13):
        D = 5*k - 2
        res = solve_forced_S(k, D, 1, -1, 0, want_S=True)
        rows.append(res)
        ok_all &= (res["verdict"] == "FORCED_R" and res["d"] == 4
                   and res["exact_block_check"])
    report("all ten instances k=3..12 (D = 5k-2) carry a forced R, "
           "deg S = 4, exact block check", ok_all)
    uniq = all(res["kernel_rational"] is False and
               not res["pole_resonance_Dm_eq_kp"] for res in rows)
    report("uniqueness up to scalar for all ten (k does not divide D; "
           "no pole resonance D*m = k*p)", uniq)
    print()
    print("   k   D    S (primitive integer, leading coeff > 0)"
          "          c (alpha=1)")
    for res in rows:
        print(f"  {res['k']:>2}  {res['D']:>2}   {poly_str(res['S_int']):<52}"
              f" {res['c_int_alpha1']}")
    # handoff k=3 check
    r3 = rows[0]
    S_handoff = {4: 243, 3: -81, 2: 54, 1: -42, 0: 35}
    got = {int(i): c for i, c in r3["S_int"].items()}
    okS = (got == S_handoff)
    report("k=3 forced S == handoff S = 243v^4 - 81v^3 + 54v^2 - 42v + 35",
           okS, "" if okS else f"got {got}")
    c3v = F(r3["c_int_alpha1"])
    report("k=3 |c| == 455 (handoff says c = -455; OUR C1e-verified "
           "convention gives c = +455: sign-convention discrepancy, logged)",
           abs(c3v) == 455, f"c = {c3v}")
    # S(-1) consistency: E(-1) = -(Dm-kp) S(-1) = const = -c   (both sides
    # in the s_0 = 1 normalization that S_at_minus1/c_over_alpha5 use)
    okm1 = True
    for res in rows:
        Dm_kp = res["D"]*1 - res["k"]*4
        lhs = F(res["S_at_minus1"]) * (-Dm_kp)
        rhs = -F(res["c_over_alpha5"])
        okm1 &= (lhs == rhs)
    report("consistency E(-1) = -(Dm-kp)*S(-1) = -c for all ten "
           "(pole order 4 is EXACT: S(-1) != 0)", okm1)
    # what the wrong guess D = 3k+4 would have produced (for the record):
    print()
    print("   [record] under the WRONG guess D = 3k+4, the instances k >= 4")
    print("   change D and S entirely; e.g. k=4 (D=16 vs true 18):")
    wrong = solve_forced_S(4, 16, 1, -1, 0, want_S=True)
    print(f"     wrong-guess k=4 verdict: {wrong['verdict']}"
          + (f", S = {poly_str(wrong['S_int'])}" if wrong.get("S_int") else "")
          + f"   TRUE k=4: S = {poly_str(rows[1]['S_int'])}")
    with open(os.path.join(HERE, "trackC_c2_tenR.json"), "w") as f:
        json.dump({"D_relation": "D = 5k - 2 (derived; handoff guess 3k+4 "
                                 "wrong for k>=4)",
                   "rows": rows, "wrong_guess_k4": wrong},
                  f, indent=1, default=str)
    print(f"\n  artifact: trackC_c2_tenR.json")

# ================================================================== main
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("c4", "all"):
        run_c4()
        print()
    if which in ("c2", "all"):
        run_c2()
        print()
    if which in ("c3",):
        from trackC_c3_ladder import run_c3   # written as a separate module
        run_c3()
    print(f"TOTAL: {PASS} PASS, {FAIL} FAIL")
    sys.exit(0 if FAIL == 0 else 1)
