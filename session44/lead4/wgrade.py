#!/usr/bin/env python3
"""Weight-graded descent for  [P,Q] = x^r  with prescribed Newton polygons.

WHY THIS EXISTS
---------------
The y-adic descent (walk_ideal / trackD_extract) eliminates Q by a row
recursion and then grinds one y-row at a time in ALL of the driver's
coefficients at once.  It rediscovers the shape's structure slowly.

This module grades BOTH polynomials by a weight w(i,j) = u*i + v*j chosen
along a common edge direction of the two polygons.  Writing

    P = sum_alpha P^(alpha),   Q = sum_beta Q^(beta)      (w-homogeneous parts)

the identity [P,Q] = x^r splits into one equation per w-level:

    E_S :  sum_{alpha+beta = S} [P^(alpha), Q^(beta)]  =  x^r  or  0.

Two facts make this a much better descent than the y-adic one:

  * each w-level of a polygon is a set of COLLINEAR lattice points, so
    P^(alpha) = (monomial) * h_alpha(t) for the primitive monomial t along
    the level lines -- every level equation is an identity of polynomials
    in ONE variable, and its coefficient equations are triangular;
  * the EXTREME level equation involves only the two extreme faces.  When
    the right-hand side x^r sits at that extreme level (which is exactly
    the situation for the open (72,108) subcase 2) that equation is a
    small, self-contained, NON-vacuous system in the two face forms alone.
    It is a necessary condition, so if it has no non-degenerate solution
    the whole shape is EMPTY -- decided before any other coefficient is
    ever touched.

The walk is sound and loses no solutions: within a level the coefficient
equations are processed in order and an unknown is eliminated only when its
coefficient is a NONZERO RATIONAL; every other equation is kept verbatim as
a condition.  No truncation: the graded system is the complete set of
coefficient equations of [P,Q] - x^r.

CAVEATS THAT MUST TRAVEL WITH ANY VERDICT
  * gauge fixing sets designated non-vanishing coefficients to 1; a slice
    of a torus orbit, legitimate over an algebraically closed field.
  * EMPTY means: no (P,Q) with these Newton polygons and this bracket.
    A surviving component is NOT a counterexample until it is lifted to
    honest polynomials in the original coordinates and its Jacobian is
    verified to be a nonzero constant exactly.
"""
import argparse
import json
import math
import os
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction

import sympy as sp

from trackB1_polygon import hull_rows


# ---------------------------------------------------------------- polygons
def lattice(verts):
    R = hull_rows([tuple(p) for p in verts])
    return [(i, j) for j in sorted(R) for i in range(R[j][0], R[j][1] + 1)]


def hull_vertices(verts):
    pts = sorted(set(tuple(p) for p in verts))
    if len(pts) <= 2:
        return pts

    def cr(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def edge_dirs(verts):
    V = hull_vertices(verts)
    out = []
    for k in range(len(V)):
        a, b = V[k], V[(k + 1) % len(V)]
        d = (b[0]-a[0], b[1]-a[1])
        g = math.gcd(abs(d[0]), abs(d[1]))
        if g:
            out.append((d[0]//g, d[1]//g))
    return out


def weight_candidates(NP, NQ):
    """primitive weights (u,v) whose level lines run along an edge direction
    shared by both polygons."""
    dP, dQ = edge_dirs(NP), edge_dirs(NQ)
    cands = []
    for d in dP:
        if d in dQ or (-d[0], -d[1]) in dQ:
            u, v = d[1], -d[0]
            g = math.gcd(abs(u), abs(v))
            u, v = u//g, v//g
            if (u, v) not in cands and (-u, -v) not in cands:
                cands.append((u, v))
    return cands


# ---------------------------------------------------------------- the walk
class Walk:
    def __init__(self, NP, NQ, r, weight, sign=1, gauge=None, verbose=True):
        self.NP, self.NQ, self.r = NP, NQ, r
        self.u, self.v = weight
        self.sign = sign
        self.verbose = verbose
        self.LP, self.LQ = lattice(NP), lattice(NQ)
        self.a = {p: sp.Symbol(f"a_{p[0]}_{p[1]}") for p in self.LP}
        self.b = {p: sp.Symbol(f"b_{p[0]}_{p[1]}") for p in self.LQ}
        self.assign = {}
        self.conds = []
        self.free = []
        self.gauge = list(gauge or [])
        # direction along the level lines, and the coordinate along it
        g = math.gcd(abs(self.u), abs(self.v))
        self.d = (-self.v // g, self.u // g)
        for p, val in self.gauge:
            key = tuple(p)
            if key in self.a:
                self.assign[self.a[key]] = sp.Integer(val)
            else:
                raise SystemExit(f"gauge point {p} not in N(P)")

    def w(self, p):
        return self.u*p[0] + self.v*p[1]

    def tcoord(self, p):
        return p[0]*self.d[0] + p[1]*self.d[1]

    def build(self):
        """all coefficient equations of [P,Q] - sign*x^r, grouped by w-level"""
        eq = defaultdict(lambda: sp.Integer(0))
        for p in self.LP:
            for q in self.LQ:
                c = p[0]*q[1] - p[1]*q[0]
                if c:
                    eq[(p[0]+q[0]-1, p[1]+q[1]-1)] += c*self.a[p]*self.b[q]
        eq[(self.r, 0)] -= self.sign
        lev = defaultdict(list)
        for m, e in eq.items():
            if e != 0:
                lev[self.w(m)].append((self.tcoord(m), m, e))
        for L in lev:
            lev[L].sort()
        return lev

    def run(self, order=None):
        lev = self.build()
        Ls = sorted(lev)
        if order == "down":
            Ls = Ls[::-1]
        if self.verbose:
            print(f"  weight w(i,j) = {self.u}*i + {self.v}*j ; "
                  f"{len(self.LP)}+{len(self.LQ)} coefficients ; "
                  f"{sum(len(v) for v in lev.values())} equations "
                  f"in {len(Ls)} w-levels", flush=True)
        for L in Ls:
            solved = ncond = 0
            for _, m, e in lev[L]:
                e = sp.expand(e.subs(self.assign))
                if e == 0:
                    continue
                pivot = None
                for s in sorted(e.free_symbols, key=self.pivkey):
                    c = e.coeff(s, 1)
                    if c.is_number and c != 0 and sp.degree(e, s) == 1:
                        pivot = (s, sp.expand(-(e - c*s)/c))
                        break
                if pivot:
                    s, val = pivot
                    self.assign[s] = val
                    for k in list(self.assign):
                        self.assign[k] = sp.expand(
                            sp.sympify(self.assign[k]).subs({s: val}))
                    solved += 1
                else:
                    self.conds.append(e)
                    ncond += 1
            if self.verbose:
                print(f"    level {L:4d}: {len(lev[L]):4d} eqs -> "
                      f"{solved:4d} eliminated, {ncond:4d} conditions "
                      f"(total {len(self.conds)})", flush=True)
        return self.conds

    def pivkey(self, s):
        """triangular preference: eliminate Q-coefficients first, highest
        position along the level line first."""
        nm = str(s).split("_")
        p = (int(nm[1]), int(nm[2]))
        return (0 if nm[0] == "b" else 1, -self.tcoord(p), str(s))

    def unassigned(self):
        allsym = set(self.a.values()) | set(self.b.values())
        used = set()
        for p in self.LP:
            for q in self.LQ:
                if p[0]*q[1] - p[1]*q[0]:
                    used |= {self.a[p], self.b[q]}
        return sorted((allsym & used) - set(self.assign), key=str)


# ------------------------------------------------------------- the verdict
def singular_verdict(conds, syms, nondeg, char=0, timeout=900, tag="wg",
                     scratch="_scratch_wg"):
    os.makedirs(scratch, exist_ok=True)
    names = {s: f"v({k+1})" for k, s in enumerate(syms)}

    def cv(e):
        e = sp.expand(e)
        s = str(e)
        for sym in sorted(syms, key=lambda z: -len(str(z))):
            s = s.replace(str(sym), names[sym])
        return s
    L = [f"ring R = {char}, (v(1..{len(syms)}), zz), dp;"]
    if conds:
        L.append("ideal I = " + ",\n  ".join(cv(c) for c in conds) + ";")
    else:
        L.append("ideal I = 0;")
    if nondeg:
        L.append("poly nd = " + " * ".join(cv(n) for n in nondeg) + ";")
        L.append("I = I + ideal(zz*nd - 1);")
    L.append("int t0 = timer;")
    L.append("list LL = facstd(I);")
    L.append('"time: " + string(timer - t0);')
    L.append('"components: " + string(size(LL));')
    L.append("int ii; int alive = 0; int dmax = -1;")
    L.append("for (ii = 1; ii <= size(LL); ii++) {")
    L.append("  ideal Gi = std(LL[ii]);")
    L.append("  if (size(Gi) != 1 || Gi[1] != 1) { alive = alive + 1;")
    L.append("    if (dim(Gi) > dmax) { dmax = dim(Gi); }")
    L.append('    "  live component " + string(ii) + ": dim " + string(dim(Gi))'
             ' + (dim(Gi)==0 ? ", vdim " + string(vdim(Gi)) : ""); }')
    L.append("}")
    L.append('if (alive == 0) { "VERDICT: EMPTY"; } else '
             '{ "VERDICT: " + string(alive) + " live component(s), max dim " '
             '+ string(dmax); }')
    L.append("quit;")
    fn = os.path.join(scratch, f"{tag}_{char}.sing")
    open(fn, "w").write("\n".join(L))
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        return pr.stdout.strip(), fn
    except subprocess.TimeoutExpired:
        return f"TIMEOUT after {timeout}s", fn
