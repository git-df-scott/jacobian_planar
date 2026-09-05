#!/usr/bin/env python3
"""The sharpened question for the (72,108) family.

The campaign's extract system asks: is there a P with the reduced (72,108)
Newton polygon and a Q *in the prescribed windows* with {P,Q} = x^2?

This asks the strictly wider question: is there such a P and ANY strip-type Q
at all, with deg_T g_sigma bounded only by a generous N?  An EMPTY here is a
much stronger statement than the campaign target being empty.

mu=2, (rmax,smax)=(2,3), tops=(m,m,m) is the 2:3 ray; m=8 is (72,108).
"""
import sys
import general2

BUDGET = int(sys.argv[1]) if len(sys.argv) > 1 else 900
for m in (2, 3, 4, 5, 6, 7, 8):
    N = 2 * m + 2
    print(f"--- 2:3 ray, tops=({m},{m},{m}), N={N}  [m=8 is the (72,108) polygon]", flush=True)
    general2.run(2, 2, 3, 2, [m, m, m], N, 32003, BUDGET)
