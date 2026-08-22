#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / L3 -- step 1: is the (-5)...(-2) chain of the Three-dessin
Framework the SAME as the First Framework's?

WHY THIS IS THE FIRST L3 QUESTION.  L3 is boundary rigidity: the Taylor pins
that force g = alpha*U*(U-1)^8 with no free moduli.  The campaign derives g from
the Y-side chart (Session 27), whose inputs are exactly (i) the (-5)...(-2)
chain and (ii) the (-5)- and (-2)-curve Belyi maps.  If all three inputs are
unchanged, L3's derivation has nothing to re-derive.  If the chain differs, L3
must be rebuilt from scratch and the conditional kill is in genuine doubt.

SOURCE.  Read off Borisov arXiv:1901.04073v2 by rendering the PDF pages at
200 dpi and reading the figures directly (pdftotext mangles them):
  Fig. 10, p.9   -- First Framework, close-up of the (-5)...(-2) map
  Fig. 31, p.23  -- Three-dessin Framework, close-up of the (-5)...(-2) map

A FIGURE READ IS NOT A CERTIFICATE, so the labels are then put through the
campaign's own C1 test (d23_phase1_chaindata.py): a valid iterated-blowup chain
must reduce to the bare edge (-5,-2) by repeatedly deleting a curve whose label
equals the sum of its two neighbours'.  A single misread digit breaks that
arithmetic, so passing C1 validates the transcription.
"""
import sys
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

# ---- transcriptions, read from the rendered figures ----------------------
FF = [-5, -52, -47, -42, -37, -32, -27, -22, -39, -17, -12, -19, -26,
      -7, -9, -11, -13, -2]                       # Fig. 10,  p.9
TD = [-5, -52, -47, -42, -37, -32, -27, -22, -39, -17, -12, -19, -26,
      -7, -9, -11, -13, -2]                       # Fig. 31,  p.23
FF_TARGET = [-5, -4, -3, -2, -1, -2]              # Y-side chain, Fig. 10
TD_TARGET = [-5, -4, -3, -2, -1, -2]              # Y-side chain, Fig. 31

print("="*78)
print("L3 step 1 -- THE (-5)...(-2) CHAIN, FIRST vs THREE-DESSIN FRAMEWORK")
print("="*78)

def c1_reduce(labels):
    """Campaign C1: repeatedly delete an interior curve whose label equals the
    sum of its two neighbours (i.e. contract a (-1)-curve). A genuine
    iterated-blowup chain reduces to its two endpoints."""
    ch = list(labels); order = []
    changed = True
    while changed and len(ch) > 2:
        changed = False
        for i in range(1, len(ch)-1):
            if ch[i] == ch[i-1] + ch[i+1]:
                order.append(ch.pop(i)); changed = True; break
    return ch, order

for name, ch in (("First Framework", FF), ("Three-dessin Framework", TD)):
    red, order = c1_reduce(ch)
    check(f"{name}: chain is a valid iterated blowup (C1 reduces to the bare "
          f"edge)", red == [-5, -2], "CERTIFIED",
          f"{len(ch)} labels -> {red}; contracted {len(order)} curves")

check("the two transcriptions are IDENTICAL, label for label",
      FF == TD, "CERTIFIED", f"{len(FF)} labels, exact match")
check("the Y-side (target) chains are identical too",
      FF_TARGET == TD_TARGET, "CERTIFIED", f"{FF_TARGET}")

# ---- forward reconstruction: build the chain by blowups, confirm it is THE one
print("\n  Forward check -- rebuild the chain from the bare edge by blowups:")
def blow(ch, i):
    """insert the sum of neighbours i,i+1 between them (one blowup)"""
    return ch[:i+1] + [ch[i] + ch[i+1]] + ch[i+1:]
seq = [-5, -2]
# the construction order forced by the labels: first the (-5)/(-2) corner (-7),
# then the (-5)-side arithmetic run, then the (-2)-side run, then the three
# interior curves -39, -19, -26.
seq = blow(seq, 0)                                   # -7
for _ in range(9):                                   # -12,-17,...,-52
    seq = blow(seq, 0)
i7 = seq.index(-7)
for _ in range(3):                                   # -9,-11,-13
    seq = blow(seq, len(seq)-2)
i22, i17 = seq.index(-22), seq.index(-17)
seq = blow(seq, i22)                                 # -39 between -22 and -17
i12, i7b = seq.index(-12), seq.index(-7)
seq = blow(seq, i12)                                 # -19 between -12 and -7
i19 = seq.index(-19)
seq = blow(seq, i19)                                 # -26 between -19 and -7
check("the transcribed chain is reproduced exactly by an explicit blowup "
      "sequence from the edge (-5,-2)", seq == FF, "CERTIFIED",
      f"rebuilt {len(seq)} labels; match = {seq == FF}")
if seq != FF:
    print(f"      rebuilt : {seq}")
    print(f"      figure  : {FF}")

print(f"""
  READING.  {len(FF)} curves, endpoints (-5) and (-2), 16 interior.  The
  arithmetic run -7,-12,-17,-22,-27,-32,-37,-42,-47,-52 is repeated blowup
  against the (-5)-curve; -9,-11,-13 against the (-2)-curve; -39, -19, -26 are
  the three interior corner blowups.  Both frameworks carry it verbatim.
""")
print("="*78)
if FAIL:
    print("L3 step 1 FAILED:", FAIL); sys.exit(1)
print("""L3 step 1 RESULT.  The (-5)...(-2) chain -- the chain that carries the
degree-13 map and fixes the chain degree D -- is IDENTICAL in the First and
Three-dessin Frameworks, source and target, and both transcriptions are
validated by the campaign's own C1 blowup test.

Together with Borisov's statement (source-verified) that the (-5)- and
(-2)-curve Belyi maps are the SAME as the First Framework's, ALL THREE inputs
to the Session-27 Y-side chart are unchanged.

This is evidence, NOT a certificate, that L3 transfers: the inputs match, but
the rigidity DERIVATION has not been re-run on the three-dessin boundary, where
the (-1)/type-3 region genuinely differs.  Status stays CONDITIONAL.""")
print("="*78)
