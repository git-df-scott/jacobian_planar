# Rendered figures from arXiv:1901.04073v2 (Borisov)

`pdftotext` mangles these figures beyond use, so the pages were rendered at
200 dpi and read directly. They are the source of the chain transcription in
STATUS.md §2.2 and `../w1_L3_chain_identity.py`.

| file | page | figure |
|---|---|---|
| `borisov_fig10_p9_first_framework.png` | 9 | Fig. 10 — First Framework, with the (−5)…(−2) close-up |
| `borisov_fig31_p23_three_dessin.png` | 23 | Fig. 31 — Three-dessin Framework, same close-up |

Both close-ups give the identical 18 K̄ labels
`-5 -52 -47 -42 -37 -32 -27 -22 -39 -17 -12 -19 -26 -7 -9 -11 -13 -2`
and the identical target chain `-5 -4 -3 -2 -1 -2`.

A figure read is not a certificate, so the transcription is validated two ways in
`../w1_L3_chain_identity.py`: the campaign's C1 blowup test (contract to the bare
edge in 16 steps) and a forward reconstruction from `(-5,-2)`. A single misread
digit breaks that arithmetic.

Regenerate: `pdftoppm -f 9 -l 9 -r 200 -png borisov.pdf p09` (and `-f 23 -l 23`).
The PDF itself is not committed — it is Borisov's paper, freely available at
arXiv:1901.04073.
