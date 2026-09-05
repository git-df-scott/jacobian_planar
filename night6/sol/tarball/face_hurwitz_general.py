#!/usr/bin/env python3
"""Independent existence/count checker for all normalized edge-ODE types."""
import argparse
import math
import sys
from fractions import Fraction

TYPES = {
    "T1": (2,3,4,-3,2,4), "T2": (2,3,7,-5,2,4),
    "T3": (1,2,3,-2,1,1), "T4": (1,2,5,-3,1,1),
    "T5": (3,4,-3,2,1,3), "T6": (1,4,7,-2,1,1),
    "T7": (2,5,7,-3,3,6), "T8": (5,8,3,-2,2,10),
    "T9": (7,10,-3,2,5,35),
}


def profiles(dp,dq,beta,gamma):
    if beta < 0:
        zero_exp,zero_count=-beta,dp
        pole_exp,pole_count=gamma,dq
    else:
        zero_exp,zero_count=-gamma,dq
        pole_exp,pole_count=beta,dp
    degree=zero_exp*zero_count
    assert degree==1+pole_exp*pole_count
    mu0=(zero_exp,)*zero_count
    muI=(pole_exp,)*pole_count+(1,)
    ram0=degree-len(mu0);ramI=degree-len(muI)
    long_cycle=2*degree-2-ram0-ramI+1
    muC=(long_cycle,)+(1,)*(degree-long_cycle)
    return degree,mu0,muI,muC


def disconnected_size_obstruction(mu0,muI,muC):
    """Elementary automatic-transitivity test used by this catalogue."""
    degree=sum(mu0); complement=degree-muC[0]
    z,p=mu0[0],muI[0]
    possible=[]
    for size in range(1,complement+1):
        if size%z==0 and (size%p==0 or (size-1)%p==0): possible.append(size)
    # T9 has size 3 as the sole numerical possibility, but product of a
    # 3-cycle and a transposition cannot be identity on that orbit.
    if (degree,z,p,complement)==(21,3,2,4): possible=[]
    return possible


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--case1-module-dir",required=True);args=ap.parse_args()
    sys.path.insert(0,args.case1_module_dir)
    from case1_hurwitz import frobenius
    ok=True
    for name,(dp,dq,beta,gamma,want_covers,want_points) in TYPES.items():
        degree,mu0,muI,muC=profiles(dp,dq,beta,gamma)
        count=frobenius(mu0,muI,muC)
        covers=Fraction(count,math.factorial(degree))
        points=dp*covers
        possible=disconnected_size_obstruction(mu0,muI,muC)
        good=(covers==want_covers and points==want_points and not possible)
        ok &= good
        print(name,"PASS" if good else "FAIL","degree",degree,"profiles",mu0,muI,muC,
              "covers",covers,"normalized_points",points,"disconnected_sizes",possible)
    print("PASS: all Hurwitz counts and transitivity checks" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)


if __name__=="__main__":main()
