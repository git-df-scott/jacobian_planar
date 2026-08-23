"""INSTRUMENT VERIFICATION for the (9,24) sub-case (3) attack.

The ladder reports a residual ||F||.  That number is worthless unless it really
measures  [P,Q] - x.  So: take the parameters, build P and Q as EXPLICIT
polynomials, compute the bracket P_x Q_y - P_y Q_x directly, and compare with x.

Three checks:
  1. CONTROL: a pair we know satisfies [P,Q]=x  ->  bracket residual must be 0.
  2. Does the direct bracket residual track the ladder's ||F||?
  3. At the best point found, what is the ACTUAL bracket error?
"""
import numpy as np, sys, sympy as sp
sys.argv=['x']
import case924 as C

x,y=sp.symbols('x y')

def build_PQ(t):
    A,B,r,ptr=C.run(t)
    P=0; Q=0
    for i in range(C.MX+1):
        for c,e in zip(A[i],C.AR[i]):
            if abs(c)>0: P+= complex(c)*x**i*y**e
    for k in range(C.MQ+1):
        for c,e in zip(B[k],C.BR[k]):
            if abs(c)>0: Q+= complex(c)*x**k*y**e
    return sp.expand(P),sp.expand(Q),A,B,r

def bracket_error(P,Q):
    J=sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x))
    D=sp.expand(J-x)
    if D==0: return 0.0,0.0,0
    pj=sp.Poly(D,x,y)
    coeffs=[abs(complex(c)) for c in pj.coeffs()]
    # scale: size of the bracket's own terms
    pJ=sp.Poly(J,x,y) if J!=0 else None
    scale=max([abs(complex(c)) for c in pJ.coeffs()]) if pJ else 1.0
    return max(coeffs), max(coeffs)/(scale+1e-300), len(coeffs)

print("=== CHECK 1: control -- a pair that genuinely satisfies [P,Q] = x ===")
Pc, Qc = y, x*y - sp.Rational(0)  # {y, xy} = y_x*(xy)_y - y_y*(xy)_x = 0 - 1*y = -y
Pc, Qc = -x, y                      # {-x,y} = -1
for (p_,q_,lab) in [(x, y, "P=x, Q=y  -> bracket 1"),
                    (y, -x, "P=y, Q=-x -> bracket 1"),
                    (x*y, y, "P=xy, Q=y -> bracket y")]:
    J=sp.expand(sp.diff(p_,x)*sp.diff(q_,y)-sp.diff(p_,y)*sp.diff(q_,x))
    print(f"   {lab:28s}: computed bracket = {J}")
# an exact [P,Q] = x pair:  P = x^2/2, Q = y  -> P_x Q_y = x
print(f"   P=x^2/2, Q=y: bracket = {sp.expand(sp.diff(x**2/2,x)*sp.diff(y,y))}  (must be x)")
err,rel,n=bracket_error(x**2/2, y)
print(f"   -> bracket_error on that exact pair: abs={err:.3e} rel={rel:.3e}  (must be 0)")

print("\n=== CHECK 2/3: the ladder's points ===")
rng=np.random.default_rng(5)
best=(1e99,None)
for trial in range(40):
    x0=rng.normal(size=34)
    from scipy.optimize import least_squares
    try: s=least_squares(C.resid,x0,method='lm',max_nfev=30000)
    except Exception: continue
    r=C.resid(s.x); val=float(np.linalg.norm(r[:-8]))
    if val<best[0]: best=(val,s.x.copy())
print(f"best ladder residual over 40 trials: ||F|| = {best[0]:.6e}")
t=best[1][:17]+1j*best[1][17:]
P,Q,A,B,r=build_PQ(t)
err,rel,n=bracket_error(P,Q)
print(f"\nDIRECT bracket check on that point:")
print(f"   max |coefficient of ([P,Q] - x)|  = {err:.6e}")
print(f"   relative to the bracket's own scale = {rel:.6e}")
print(f"   number of nonzero error coefficients = {n}")
print(f"   vertices: p_18_6={abs(A[6][-1]):.3e}  p_16_6={abs(A[6][0]):.3e}")
print(f"             q_27_9={abs(B[9][-1]):.3e}  q_24_9={abs(B[9][0]):.3e}")
print("\nIf the direct bracket error is NOT tiny, the ladder residual is not")
print("measuring [P,Q]-x and every number reported from it is meaningless.")
