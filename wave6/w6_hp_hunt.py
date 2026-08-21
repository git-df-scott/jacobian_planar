#!/usr/bin/env python3
"""HIGH-PRECISION char-0 hunt on the live (72,108) branch -- p108_525122.

The smallest realization system of the surviving pair (25 params, 140
conditions), in characteristic 0, attacked numerically at 50 digits of
precision (mpmath), which the 15-order coefficient span requires.  Nobody
has ever produced any char-0 evidence on these systems in either direction.

Gauss-Newton with complex variables at dps=50.  A converged point
(|F|^2 < 1e-60 at dps 50) = CANDIDATE on the (72,108) branch -> exact lift.
Persistent floor = first char-0 evidence for GGHV Cor 5.7.

Control: the same pipeline run on the known-EMPTY system w6_289012_0's
char-0 dump must floor (it is EMPTY mod p with nondegeneracy; a char-0
numerical 'solution' would flag a pipeline error -- OR a genuinely
degenerate char-0 point, which the mod-p run's saturation excluded; either
way a hit there is reported for inspection, not silently trusted).
"""
import sys, os, json, time, re
import mpmath as mp

mp.mp.dps = 50
ROOT = '/home/user/jacobian_planar'

def load_system(gens_path, nparams, extra_vars):
    txt = open(gens_path).read().strip().rstrip(',')
    txt = txt.replace('c(', 'c_').replace(')', '')
    gens = [g.strip() for g in txt.replace('\n', '').split(',') if g.strip()]
    vars_ = [f'c_{i}' for i in range(1, nparams + 1)] + extra_vars
    # compile each generator to a python expression evaluable with mpmath
    code = []
    for g in gens:
        e = g.replace('^', '**')
        code.append(compile(e, '<gen>', 'eval'))
    return code, vars_

def make_env(vars_, z):
    return {v: z[i] for i, v in enumerate(vars_)}

def residual(code, vars_, z):
    env = make