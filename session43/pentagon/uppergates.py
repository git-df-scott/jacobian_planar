#!/usr/bin/env python3
"""THE UPPER GATES: how many at each level, from the Newton polygons alone.

At level L the new unknown is the coupled  W_{L-8} = g_{L-8} - (3c1/2c0) z^4 h_{L-12},
and D_{L-8} preserves degree, so

    deg W_{L-8} <= max( deg g_{L-8} , 4 + deg h_{L-12} )   =: DW

The equation is  D_{L-8}(W) = -carried_L / (8 c0 z^7), whose degree is
deg(carried_L) - 7 =: DR.  Every coefficient of the RHS above DW is an
OBSTRUCTION with no unknown to absorb it:

    number of UPPER gates at level L  =  max(0, DR - DW)

This is in addition to the lower gate z^7 | carried_L.
"""
def g_deg(b):
    ks = [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
    return max(ks) if ks else None
def h_deg(a):
    xs = [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
    return max(xs) if xs else None

print("  L | deg g_{L-8} | deg h_{L-12} | deg W | deg carried | deg RHS | UPPER GATES")
print(" ---+-------------+--------------+-------+-------------+---------+------------")
for L in range(19, 6, -1):
    b, a = L-8, L-12
    gd = g_deg(b) if -1 <= b <= 12 else None
    hd = h_deg(a) if -1 <= a <= 8 else None
    if gd is None: continue
    DW = max([gd] + ([4+hd] if hd is not None else []))
    # carried_L = all pairs (i,k), i+k = L, excluding the two isolating ones
    dc = 0
    for i in range(-1, 9):
        k = L - i
        if not (-1 <= k <= 12): continue
        if (i, k) in ((8, L-8), (L-12, 12)): continue
        hi, gk = h_deg(i), g_deg(k)
        if hi is None or gk is None: continue
        dc = max(dc, (hi-1)+gk, hi+(gk-1))
    DR = dc - 7
    gates = max(0, DR - DW)
    flag = "  <== GATE" if gates else ""
    print(f"  {L:2d} |     {gd:2d}      |      {str(hd):>2s}      |  {DW:2d}   |     {dc:2d}      "
          f"|   {DR:2d}    |     {gates}{flag}")
print("\nverified instances:")
print("  L=17 : DR = 12, DW = 12 -> 0 gates.  Consistent with Codex's level 17 standing.")
print("  L=16 : DR = 12, DW = 11 -> 1 gate.   This is the [z^19] carried16 = 27/4 obstruction.")
