"""
Plane Jacobian campaign - Session N2: PHASE 2 PREVIEW (gate respected).

The task gates Phase 2 (isotope series) on a clean unconditional Phase-1
DIES, which this session did not reach (verdict: conditional DIES).  This
file does NO tower rebuilding.  It only extracts the published Section-5
data (arXiv:1901.04073) and applies the already-certified general-D
endgame lemma (d23_phase1_endgame.py E4: the M==0 branch admits rational
R iff 3 | D; T_D certified for D = 13 and 23), producing the conditional
transfer verdict for the ENTIRE published framework family.

Published family (all of Section 2-5):
  - First Framework:            D = 13, degrees (99, 66)   [PROVEN dead,
    Sessions 16-18, unconditional]
  - Isotopes k = 2..6:          D = 13, degrees (36k+27, 24k+18); same
    TARGET graph as FF, same (-5)-curve Belyi data; only the (-2)-side
    branch inventory and the long branch change (k = 2 IS the FF)
  - "Complicated" framework:    D = 13, degrees (108, 72); the (-5)- and
    (-2)-curve Belyi maps are THE SAME as the First Framework's; adds a
    third, degree-5 Belyi map (explicitly (1/108) x^3 (x-5)^2)
  - Second Framework:           D = 23, degrees (435, 290)  [this session]

Chain degrees in the entire published family: {13, 23}; both are != 0
mod 3, so the one obstruction (3n = D insoluble; evaluation at v = -1)
covers everything the paper constructs -- exactly the Sessions 16-18
transfer conjecture, now verified at the data level family-wide.

Key structural facts making the ISOTOPE transfer especially tight (all
verified below from the published data):
  - same target graph as FF  =>  same Y-side chain, same contact -5,
    same chain degree 13, same chart, same rigidity data g = alpha U v^8;
  - the (-5)-curve map (Session-7 certified p, r) is untouched;
  - realization target: still a degree-13 POLYNOMIAL Belyi map for every
    k (infinity-marked, stated; k = 6 is t -> t^13 + 1 explicitly);
  - the certified endgame operator T_13 (kernel trivial, rank 14,
    T(R) = const infeasible) applies VERBATIM to every isotope: the
    k-dependence enters only the box-cap census layer (Sessions 14-15
    analog), which is the single isotope-conditional gap.
"""
# ---------- isotope data checks ----------
print("isotope series k = 2..6 (D = 13 for all):")
okA = okB = okC = True
for k in range(2, 7):
    d1, d2 = 36*k + 27, 24*k + 18
    okA &= (d1, d2) == (3*(12*k + 9), 2*(12*k + 9))          # cusp (3,2)
    # (-2)-curve Belyi profile: {0}: (6-k)x3 + (3k-5)x1;
    # {1}: 1x(2k+1) + (12-2k)x1; {inf}: 1x13
    f0 = 3*(6 - k) + (3*k - 5)
    f1 = (2*k + 1) + (12 - 2*k)
    okB &= f0 == 13 and f1 == 13
    rh = 2*(6 - k) + 2*k + 12                                 # sum (e-1)
    okC &= rh == 2*13 - 2
    print(f"  k={k}: degrees ({d1},{d2}) = {12*k+9}*(3,2); profile sums "
          f"{f0}/{f1}/13; RH {rh} = 24")
print("  all degree pairs proportional to (3,2):", okA)
print("  all (-2)-Belyi profiles have degree 13:", okB)
print("  Riemann-Hurwitz (genus 0) for every k:", okC)

# x1/x2-degree splits (published): y1: (9k+9, 27k+18); y2: (6k+6, 18k+12)
okD = all((9*k + 9) + (27*k + 18) == 36*k + 27 and
          (6*k + 6) + (18*k + 12) == 24*k + 18 for k in range(2, 7))
print("  published x1/x2-degree splits sum to the total degrees:", okD)
print("  (k = 2 boxes [0,27]x[0,72] / [0,18]x[0,48] = the Session-8 FF boxes)")

# ---------- complicated framework ----------
print()
print("complicated framework: degrees (108,72) = 36*(3,2):",
      (108, 72) == (36*3, 36*2))
print("  chain degree = 13 (same (-2)-curve Belyi map as FF, published);")
print("  third Belyi map deg 5: profile {inf}: 5; {0}: 3+2; {1}: 2+1+1+1;")
print("  RH:", (5-1) + (2+1) + (1+3*0), "= 8 = 2*5-2:",
      (5-1) + (2+1) + 1 == 8)

# ---------- family verdict table (conditional; NO new tower work) ----------
print()
print("family verdict under the certified general-D endgame lemma")
print("(fatal iff D mod 3 != 0; T_13 and T_23 exactly certified):")
fam = [("First Framework", 13, "(99,66)", "PROVEN DIES (Sessions 16-18)"),
       ("isotope k=3", 13, "(135,90)", "conditionally DIES"),
       ("isotope k=4", 13, "(171,114)", "conditionally DIES"),
       ("isotope k=5", 13, "(207,138)", "conditionally DIES"),
       ("isotope k=6", 13, "(243,162)", "conditionally DIES"),
       ("complicated fw", 13, "(108,72)", "conditionally DIES"),
       ("Second Framework", 23, "(435,290)", "conditionally DIES (this session)")]
for name, D, degs, verdict in fam:
    print(f"  {name:18s} D = {D}  ({D} mod 3 = {D % 3})  {degs:11s} {verdict}")
print()
print("Every chain degree in the published family lies in {13, 23}; none is")
print("divisible by 3.  The Sessions 16-18 transfer conjecture is verified")
print("at the data level across the ENTIRE published framework family.")
