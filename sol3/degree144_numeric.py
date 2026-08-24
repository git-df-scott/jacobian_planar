#!/usr/bin/env python3
"""Complex numerical reconnaissance on the full degree-144 quadrilaterals.

This is deliberately not a verdict machine.  It fixes all nonzero driver
vertices and the two nontrivial generated vertices to unit magnitude, preventing
the ubiquitous collapse to (x,x^2*y), and minimizes every support violation in
the exact y-adic recurrence.  A small residual is printed only as
CANDIDATE-UNVERIFIED and must be replayed exactly.
"""
import argparse
import numpy as np
from scipy.optimize import least_squares
from degree8_jet import lattice
from lift_x4 import reverse


CASES = [
    ("P-drives", [(0,0),(1,0),(12,9),(12,12)],
     [(0,0),(2,1),(16,12),(16,16)], 1),
    ("Q-drives", [(0,0),(1,0),(16,12),(16,16)],
     [(0,0),(2,1),(12,9),(12,12)], -1),
]


def rows(poly):
    d = {}
    for i, j in lattice(poly):
        d.setdefault(j, []).append(i)
    return {j: (min(v), max(v)) for j, v in d.items()}


def add(a, b, scale=1):
    z = np.zeros(max(len(a), len(b)), dtype=complex)
    z[:len(a)] += a
    z[:len(b)] += scale*b
    while len(z) and abs(z[-1]) == 0:
        z = z[:-1]
    return z


def mul(a, b):
    return np.convolve(a, b) if len(a) and len(b) else np.zeros(0, complex)


def deriv(a):
    return np.arange(1, len(a))*a[1:] if len(a) > 1 else np.zeros(0, complex)


class Search:
    def __init__(self, name, DV, OV, sign, pin_other=True, lift_chart=None):
        self.name, self.DR, self.OR, self.sign = name, rows(DV), rows(OV), sign
        allm = [(i,j) for i,j in lattice(DV)]
        self.fixed = {(0,0): 0, (1,0): 1}
        for v in DV:
            if v not in ((0,0),(1,0)):
                self.fixed[v] = 1
        self.var = [m for m in allm if m not in self.fixed]
        self.ov = [v for v in OV if v not in ((0,0),(2,1))]
        self.Dsupp, self.Osupp = lattice(DV), lattice(OV)
        self.pin_other = pin_other
        self.lift_chart = lift_chart
        self.lift_exps = []
        if lift_chart:
            for supp in (self.Dsupp, self.Osupp):
                ex=set()
                for m in supp:
                    ex |= {e for e in reverse({m:1},*lift_chart) if min(e)<0}
                self.lift_exps.append(sorted(ex))
        self.jmax = max(max(self.DR), max(self.OR))+2
        deg={0:-1,1:2}
        for kk in range(1,self.jmax+1):
            ds=[]
            for aa in range(kk+1):
                b=kk-aa
                if aa+1 in self.DR and deg.get(b,-1)>=0:
                    ds.append(self.DR[aa+1][1]+deg[b]-1)
                if aa>=1 and aa in self.DR and deg.get(b+1,-1)>=0:
                    ds.append(self.DR[aa][1]-1+deg[b+1])
            deg[kk+1]=max(ds,default=-1)
        self.badpos=[]
        for j in range(1,self.jmax+1):
            lohi=self.OR.get(j)
            self.badpos += [(i,j) for i in range(deg.get(j,-1)+1)
                            if lohi is None or not (lohi[0]<=i<=lohi[1])]

    def decode(self, z):
        c = dict(self.fixed)
        for m, v in zip(self.var, z): c[m] = v
        D = {}
        for (i,j), v in c.items():
            if j not in D: D[j] = np.zeros(self.DR[j][1]+1, complex)
            D[j][i] = v
        return D

    def solve_other(self, z):
        D = self.decode(z)
        R = {0: np.array([0,0,self.sign], complex)}
        O = {0: np.zeros(0,complex), 1: R[0].copy()}
        for k in range(1, self.jmax+1):
            acc = R.get(k, np.zeros(0,complex)).copy()
            for aa in range(k+1):
                b = k-aa
                if aa+1 in D and b in O:
                    acc = add(acc, mul(D[aa+1], deriv(O[b])), aa+1)
                if aa >= 1 and aa in D and b+1 in O:
                    acc = add(acc, mul(deriv(D[aa]), O[b+1]), -(b+1))
            O[k+1] = acc/(k+1)
        return D,O

    def evaluate(self, z):
        D,O = self.solve_other(z)
        bad = []
        for i,j in self.badpos:
            q=O.get(j,np.zeros(0,complex))
            bad.append(q[i] if i<len(q) else 0)
        # Vertex normalization blocks the degenerate zero-edge attractor.
        if self.pin_other:
            for i,j in self.ov:
                q = O.get(j, np.zeros(0,complex))
                bad.append((q[i] if i < len(q) else 0)-1)
        if self.lift_chart:
            for rows_, supp, exps in ((D,self.Dsupp,self.lift_exps[0]),
                                      (O,self.Osupp,self.lift_exps[1])):
                poly={(i,j): rows_.get(j,np.zeros(0,complex))[i]
                      for i,j in supp if i < len(rows_.get(j,()))}
                rr=reverse(poly,*self.lift_chart)
                bad += [rr.get(e,0) for e in exps]
        return np.asarray(bad)

    def other_vertices(self, z):
        # Re-run with temporary pins and read the final entries, whose residual
        # is coefficient-1.
        old=self.pin_other; self.pin_other=True
        vals=self.evaluate(z)[-len(self.ov):]+1
        self.pin_other=old
        return vals

    def residual(self, x):
        n = len(self.var); z = x[:n]+1j*x[n:]
        r = self.evaluate(z)
        return np.r_[r.real, r.imag]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--trials',type=int,default=8)
    ap.add_argument('--nfev',type=int,default=4000)
    ap.add_argument('--free-other-vertices', action='store_true')
    ap.add_argument('--real-start', action='store_true')
    ap.add_argument('--real-only', action='store_true')
    ap.add_argument('--case', choices=['P-drives','Q-drives'])
    ap.add_argument('--lift-chart', help='comma-separated lambda2,lambda3,lambda4')
    ap.add_argument('--free-lambdas', action='store_true',
                    help='optimize lambda2,lambda3 with lambda4 normalized to 1')
    ns=ap.parse_args()
    rng=np.random.default_rng(144)
    chart=tuple(map(complex,ns.lift_chart.split(','))) if ns.lift_chart else None
    if ns.free_lambdas: chart=(1,1,1)
    for data in CASES:
        if ns.case and data[0] != ns.case: continue
        S=Search(*data,pin_other=not ns.free_other_vertices,lift_chart=chart); best=1e300; bestz=None
        print(S.name, 'complex variables',len(S.var),'residuals',len(S.evaluate(np.zeros(len(S.var)))))
        for t in range(ns.trials):
            if ns.real_only:
                extra=2 if ns.free_lambdas else 0
                x=rng.normal(scale=.15,size=len(S.var)+extra)
                if ns.free_lambdas: x[-2:]=rng.normal(size=2)
                def fun(q):
                    if ns.free_lambdas: S.lift_chart=(complex(q[-2]),complex(q[-1]),1)
                    return S.evaluate(q[:len(S.var)].astype(complex)).real
                zz=least_squares(fun,x,max_nfev=ns.nfev,xtol=1e-12,ftol=1e-12,gtol=1e-12)
                cand=zz.x[:len(S.var)].astype(complex); val=np.linalg.norm(fun(zz.x))
                if ns.free_lambdas: print('    lambdas',zz.x[-2],zz.x[-1],1,flush=True)
            else:
                x=rng.normal(scale=.15,size=2*len(S.var))
                if ns.real_start: x[len(S.var):]=0
                zz=least_squares(S.residual,x,max_nfev=ns.nfev,xtol=1e-12,ftol=1e-12,gtol=1e-12)
                n=len(S.var); cand=zz.x[:n]+1j*zz.x[n:]
                val=np.linalg.norm(S.residual(zz.x))
            if val<best: best=val; bestz=cand.copy()
            print(' ',t,'norm',f'{val:.6e}',flush=True)
        tag='CANDIDATE-UNVERIFIED' if best < 1e-9 else 'NO NUMERICAL HIT'
        msg=[tag,S.name,'best',f'{best:.12e}']
        if bestz is not None:
            vv=S.other_vertices(bestz)
            msg += ['other-vertex-magnitudes',str([float(abs(x)) for x in vv])]
            np.savez(f"sol3_{S.name.replace('-','_')}.npz", z=bestz,
                     variables=np.array(S.var), vertices=vv)
        print(*msg)


if __name__ == '__main__': main()
