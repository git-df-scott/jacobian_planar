#!/usr/bin/env python3
"""SMALL falsification test of the prediction a_5 = 0 (lattice point (5,10)).

The 71-unknown raw test and the 69-unknown (u,z) test are both too large
(msolve exceeded 8 GB). This one uses ONLY the face, which is where the
prediction lives, and is 22 unknowns.

VERIFIED input (EDGE_GAP_FINDING.md, claim 2): on the (-2,1) face of the
open subcase-2 polygons the bracket's top component must VANISH, i.e. the
two face forms commute:

    [ faceP , faceQ ] = 0 ,
    faceP = sum_{k=0..8}  a_k x^k y^(2k)        (9 coefficients)
    faceQ = sum_{l=0..12} b_l x^l y^(2l)        (13 coefficients)

That is imposed directly here as polynomial equations -- NO assumption that
the face forms are powers of a common R. The descent independently
established a_1 = 0 and a_2 = 0. Question: is a_5 = 0 then forced?

Saturate by a_5 and test emptiness:
  EMPTY    -> a_5 = 0 is forced: the prediction is CONFIRMED independently.
  NONEMPTY -> a solution exists with a_5 != 0: the face analysis in
              EDGE_GAP_FINDING.md is REFUTED and must be retracted.

Non-degeneracy: a_0, a_8, b_0, b_12 are polygon vertices, so all nonzero.
"""
import subprocess, sys
import sympy as sp

x, y = sp.symbols("x y")
a = sp.symbols("a0:9"); b = sp.symbols("b0:13")
faceP = sum(a[k]*x**k*y**(2*k) for k in range(9))
faceQ = sum(b[l]*x**l*y**(2*l) for l in range(13))
br = sp.expand(sp.diff(faceP,x)*sp.diff(faceQ,y)
               - sp.diff(faceP,y)*sp.diff(faceQ,x))
eqs = [sp.expand(co) for _, co in sp.Poly(br, x, y).terms()]
print(f"commuting condition [faceP,faceQ] = 0 -> {len(eqs)} equations")

sub = {a[1]: 0, a[2]: 0}                 # what the descent established
eqs = [sp.expand(e.subs(sub)) for e in eqs]
eqs = [e for e in eqs if e != 0]
unk = [v for v in list(a)+list(b) if v not in sub]
s, w = sp.Symbol("s_sat"), sp.Symbol("w_nd")
eqs.append(sp.expand(a[5]*s - 1))                       # saturate: a_5 != 0
eqs.append(sp.expand(a[0]*a[8]*b[0]*b[12]*w - 1))       # vertices nonzero
unk += [s, w]
print(f"after imposing a_1=a_2=0 and saturating: {len(unk)} unknowns, "
      f"{len(eqs)} equations")

for char, fn in ((65521, "test_a5_face_p.ms"), (0, "test_a5_face_c0.ms")):
    out = []
    for g in eqs:
        pe = sp.Poly(g, *unk, domain="QQ")
        L = 1
        for c in pe.coeffs(): L = sp.ilcm(L, sp.Rational(c).q)
        out.append(str(sp.expand(g*L)).replace("**","^").replace(" ",""))
    open(fn,"w").write(",".join(str(v) for v in unk)+f"\n{char}\n"
                       + ",\n".join(out)+"\n")
    print("wrote", fn)

for fn, tag in (("test_a5_face_p.ms","mod 65521"), ("test_a5_face_c0.ms","char 0")):
    try:
        r = subprocess.run(["msolve","-f",fn], capture_output=True,
                           text=True, timeout=900)
        o = (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        print(f"{tag}: TIMEOUT"); continue
    v = ("EMPTY" if o.startswith("[-1]") else
         ("NONEMPTY" if o.startswith("[") else "NO-OUTPUT"))
    print(f"\n{tag}: {v}   {o[:70]}")
    if v == "EMPTY":
        print("  -> a_5 = 0 IS forced. Prediction CONFIRMED independently.")
    elif v == "NONEMPTY":
        print("  -> a solution exists with a_5 != 0.")
        print("     THE FACE ANALYSIS IS REFUTED and must be retracted.")
