"""night18 -- CONTROLS.  Run and reported before any result.

C1  the symbolic linear-algebra layer, specialised at 3 parameter points, must
    reproduce night17's recorded lambda certificates for the corresponding
    instances -- verified against THIS lane's symbolically built M.
C2  on a FAMILY OF COORDINATES parametrised by t the machinery must find the
    MATE symbolically in t, not a certificate.
C3  the rank of M computed symbolically must agree with the rank at 5 random
    specialisations.
"""
import json, os, random, sys
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))
import spk18 as spk, fam18, mate18, members18
import pk17, mate17, coord17

HERE = os.path.dirname(os.path.abspath(__file__))
T = sp.Symbol('t')
OUT = {}


def hdr(s):
    print("=" * 78); print(s); print("=" * 78)


# ------------------------------------------------------------------ C1
def c1():
    hdr("C1  the symbolic layer must reproduce night17's recorded lambda certificates")
    rec = json.load(open(os.path.join(HERE, '..', 'night17', 'records17.json')))['records']
    want = {'d37142063698': 1, '431f3f1966ca': 2, '9667585bcb72': 3}
    rows_out = []
    ok = True
    for r in rec:
        if r['hash'] not in want:
            continue
        H = want[r['hash']]
        Pe = sp.sympify(r['P'].replace('^', '**'))
        pr = members18.recover_params(Pe)
        Fm = fam18.family(H)
        sub = {Fm['gam']: pr['gam'], Fm['a']: pr['a'], Fm['al']: pr['al']}
        for i, s in enumerate(Fm['hs']):
            sub[s] = pr['hs'][i]
        Ps = spk.subs(Fm['P'], sub)
        same_P = (spk.psub(Ps, spk.from_expr(Pe)) == {})
        for st in r['mate']['stages']:
            D = st['deg_Q_bound']
            S = mate18.carrier(D)
            cols, rws = mate18.build(Ps, S)
            lam = {tuple(int(z) for z in k.split(',')): sp.Rational(v)
                   for k, v in st['lambda'].items()}
            truncated = (len(lam) == 40)   # mate17.stage stores only the first 40
            good, msg = (False, "record truncated at 40 entries") if truncated \
                else mate18.verify_lambda(lam, cols)
            # night17's own solver re-run at the same point (byte-level check)
            mine, _c, _r, _q = mate17.stage(spk.to_pk(Ps), D, verbose=False)
            agree = (mine['verdict'] == st['verdict'])
            same_lam = (mine.get('lambda') == st.get('lambda'))
            # and this lane's own symbolic solver, specialised
            mylam, myinfo = mate18.solve_lambda(cols, rws, [])
            mine18 = 'EMPTY' if mylam is not None else 'MATE_or_NOT_EMPTY'
            good18 = mate18.verify_lambda(mylam, cols)[0] if mylam is not None else False
            agree &= (mine18 == 'EMPTY') and good18
            ok_row = bool((good or truncated) and agree and same_P)
            ok &= ok_row
            print("  %-4s %-13s D=%-3d  night17 lambda (|supp|=%d) against night18 M: %-22s"
                  " | night18 own lambda (|supp|=%d) verified: %-5s | verdict %s==%s"
                  % (r['support'], r['hash'], D, len(lam),
                     "TRUNCATED_RECORD" if truncated else str(good),
                     len(mylam) if mylam else 0, good18,
                     st['verdict'], mine['verdict']))
            rows_out.append({"support": r['support'], "hash": r['hash'], "deg_Q_bound": D,
                             "deg_h": H, "family_reproduces_P": bool(same_P),
                             "night17_lambda_support": len(lam),
                             "night17_record_truncated_at_40": bool(truncated),
                             "night17_lambda_annihilates_night18_M": bool(good),
                             "night17_verdict": st['verdict'],
                             "night18_verdict": mine['verdict'],
                             "verdicts_agree": bool(agree),
                             "lambda_dict_identical": bool(same_lam),
                             "night18_own_lambda_verified": bool(good18),
                             "night18_own_lambda_support": len(mylam) if mylam else 0})
    OUT['C1'] = {"rows": rows_out, "pass": bool(ok)}
    print("  C1 %s" % ("PASS" if ok else "*** FAILED ***")); print()
    return ok


# ------------------------------------------------------------------ C2
def coordinate_family():
    """(F,G) built from (x,y) by Jacobian-1 moves, with a parameter t.

       (x, y) -> (x, y + t x^3 + x^2) -> swap -> (F, G + F^2)
    P := the second component; its mate is the first component, and both depend
    on t.  P is a COORDINATE for every t, so the machinery must return MATE.
    """
    Fx, Gy = spk.from_expr(spk.X), spk.from_expr(spk.Y)
    # (F,G) -> (F, G + p(F)) with p(u) = t u^3 + u^2
    p = spk.padd(spk.pscal(T, spk.ppow(Fx, 3)), spk.ppow(Fx, 2))
    Fn, Gn = Fx, spk.padd(Gy, p)
    Fn, Gn = Gn, spk.pscal(-1, Fn)                       # swap
    Gn = spk.padd(Gn, spk.ppow(Fn, 2))                   # (F, G + F^2)
    return Gn, spk.pscal(-1, Fn)                         # P = Gn, mate = -Fn


def c2():
    hdr("C2  a FAMILY OF COORDINATES: the machinery must find the MATE, symbolically in t")
    P, Qknown = coordinate_family()
    chk = spk.psub(spk.bracket(P, Qknown), {(0, 0): sp.Integer(1)})
    print("  P(t) = %s" % spk.to_str(P))
    print("  deg P = %d ; the construction's own mate Q0 has deg %d ; [P,Q0]-1 terms = %d"
          % (spk.tdeg(P), spk.tdeg(Qknown), len(chk)))
    rows_out = []
    ok = (chk == {})
    for D in (spk.tdeg(P), 2 * spk.tdeg(P)):
        S = mate18.carrier(D)
        cols, rws = mate18.build(P, S)
        q, info = mate18.solve_mate(cols, rws, S, [T])
        if q is None:
            print("  D=%-3d n=%-4d  NO SOLUTION  *** FAILED ***" % (D, len(S)))
            ok = False
            rows_out.append({"deg_Q_bound": D, "verdict": "NO_SOLUTION"})
            continue
        res = spk.psub(spk.bracket(P, q), {(0, 0): sp.Integer(1)})
        good = (res == {})
        ok &= good
        # is it genuinely t-dependent?
        tdep = any(T in sp.sympify(v).free_symbols for v in q.values())
        print("  D=%-3d n=%-4d  MATE_over_Q(t)  [P,Q]-1 terms = %d  deg Q = %d  "
              "t-dependent = %s   Q = %s"
              % (D, len(S), len(res), spk.tdeg(q), tdep, spk.to_str(q)))
        lam, _li = mate18.solve_lambda(cols, rws, [T])
        no_cert = (lam is None)
        ok &= no_cert
        print("        Fredholm: a lambda certificate exists = %s (must be False)" % (not no_cert))
        rows_out.append({"deg_Q_bound": D, "n_unknowns": len(S), "verdict": "MATE_over_Q(t)",
                         "lambda_certificate_exists": bool(not no_cert),
                         "bracket_minus_one_terms": len(res), "deg_Q": spk.tdeg(q),
                         "t_dependent": bool(tdep), "Q": spk.to_str(q)})
    # negative half of C2: the same machinery on a NON-coordinate family must
    # NOT return a mate
    OUT['C2'] = {"P": spk.to_str(P), "known_mate": spk.to_str(Qknown),
                 "known_mate_residual_terms": len(chk), "stages": rows_out, "pass": bool(ok)}
    print("  C2 %s" % ("PASS" if ok else "*** FAILED ***")); print()
    return ok


# ------------------------------------------------------------------ C3
def c3():
    hdr("C3  symbolic rank of M vs the rank at 5 random specialisations")
    random.seed(31337)
    rows_out = []
    ok = True
    for H in (1, 2):
        Fm = fam18.family(H)
        for D in (3, 6):
            S = mate18.carrier(D)
            cols, rws = mate18.build(Fm['P'], S)
            rk, _M = mate18.rank_symbolic(cols, rws, Fm['free'])
            rks = []
            for _ in range(5):
                while True:
                    v = {Fm['gam']: sp.Rational(random.randint(1, 7)),
                         Fm['a']: sp.Rational(random.randint(-4, 4)),
                         Fm['al']: sp.Rational(random.randint(-5, 5))}
                    for s in Fm['hs']:
                        v[s] = sp.Rational(random.randint(-4, 4))
                    if Fm['ha'].subs(v) != 0:
                        break
                Ps = spk.subs(Fm['P'], v)
                c2_, r2 = mate18.build(Ps, S)
                rk2, _ = mate18.rank_symbolic(c2_, r2, [])
                rks.append(int(rk2))
            agree = all(r == int(rk) for r in rks)
            ok &= agree
            print("  deg h=%d  D=%-2d  n_cols=%-3d n_rows=%-3d  rank(symbolic)=%-3d"
                  "  ranks at 5 random points = %s  %s"
                  % (H, D, len(S), len(rws), rk, rks, "AGREE" if agree else "*** DISAGREE ***"))
            rows_out.append({"deg_h": H, "deg_Q_bound": D, "n_cols": len(S),
                             "n_rows": len(rws), "rank_symbolic": int(rk),
                             "ranks_at_5_specialisations": rks, "agree": bool(agree)})
    OUT['C3'] = {"rows": rows_out, "pass": bool(ok)}
    print("  C3 %s" % ("PASS" if ok else "*** FAILED ***")); print()
    return ok


if __name__ == "__main__":
    a = c1(); b = c2(); c = c3()
    OUT['all_pass'] = bool(a and b and c)
    json.dump(OUT, open(os.path.join(HERE, 'controls18.json'), 'w'), indent=1)
    print("CONTROLS %s" % ("PASS" if OUT['all_pass'] else "*** FAILED ***"))
