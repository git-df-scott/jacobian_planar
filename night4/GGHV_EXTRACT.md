# night4 GGHV_EXTRACT — extraction notes

Companion to `night4/gghv_cases.json`. Records what was read, how, and anything
that could not be read cleanly. Transcription only; no inference, no gap-filling.

## Source

| item | value |
|---|---|
| arXiv id | 1708.07936 (v1) |
| title | Some algorithms related to the Jacobian Conjecture |
| authors | Guccione, Jorge A.; Guccione, Juan J.; Horruitiner, Rodrigo; Valqui, Christian |
| arXiv date | 2017/08/26 |
| primary source used | `https://arxiv.org/e-print/1708.07936` — the original LaTeX source, single file `Some_algorithms_related_to_the_Jacobian_Conjecture_26_de_agosto_de_2017.tex` (115826 bytes) |
| cross-check source | `https://arxiv.org/pdf/1708.07936` (404296 bytes, 29 pages), text layer decompressed directly |

Both fetches returned HTTP 200. Working from the LaTeX source rather than from
rendered text means the table entries are the authors' own characters, not an OCR
or layout reconstruction. No PDF text-extraction library is installed on this
container; the PDF text layer was decompressed with `zlib` only to confirm printed
page numbers and to cross-check the tables as typeset.

## What was extracted

Section 6 of the printed paper, verbatim title
`Possible counterexamples with $\max(\deg(P),\deg(Q))\le 150$`, beginning on
printed page 27. The paper states there are 34 such cases; 34 were extracted,
across four tables:

| table | page | rows | columns as printed |
|---|---|---|---|
| 1 | 27 | 13 | Family, (m,n), max{deg(P),deg(Q)} |
| 2 | 27 | 9 | A_0, A_1, (m,n), max{deg(P),deg(Q)} |
| 3 | 28 | 11 | A_0, A_1, A_2, (m,n), max{deg(P),deg(Q)} |
| 4 | 28 | 1 | A_0, A_1, A_2, A_3, (m,n), max{deg(P),deg(Q)} |

13 + 9 + 11 + 1 = 34, matching the count stated in the paper's own text.

Also transcribed, as a clearly separated reference block, the two family tables of
Section 5 (`Admissible complete chains with $v_{11}(A_0)\le 35$`), both on printed
page 25: 17 length-1 families (F_1–F_17) and 7 length-2 families (F_18–F_24), with
their A_0, A_0', A_1, A_1', A_2, k, m, n columns.

Printed page numbers were read off the running headers in the PDF text layer, which
carry the folio; PDF page index and printed folio coincide throughout.

## Verification performed

The finished `gghv_cases.json` was re-parsed and compared field by field against the
raw LaTeX table rows (source lines 1802–1814, 1828–1836, 1848–1858, 1869 for the
case tables; 1678–1694 and 1709–1715 for the family tables). **Result: 0
mismatches across all 34 case rows and all 24 family rows**, covering every chain
entry, every (m,n), every max-degree value, and the red/star markers.

## Entries flagged `"ambiguous": true`

**None.** Every table entry in the source was legible without judgement calls.
Working from the authors' LaTeX rather than a rendered page is why; there was no
point at which a character or a cell boundary had to be guessed.

## Items recorded as printed but worth a human eye

These are **not** ambiguities — the source text is unambiguous — but they are places
where the printed value may surprise a reader, so they are transcribed exactly and
called out rather than silently normalized.

1. **No per-case degree pair is printed anywhere.** The tables print
   `max{deg(P),deg(Q)}` and `(m,n)`, never a `(deg P, deg Q)` pair. Every case
   carries `"deg_pair_printed": false`. No degree pair was computed or inferred.
2. **Table 1 prints no chain data.** Its 13 rows give only a family label, an
   `(m,n)`, and a max degree. The chains for those families live in the Section 5
   reference tables on page 25. The two were deliberately **not** merged: doing so
   would require substituting a value of the family parameter `j`, which is
   inference. Each table-1 case carries `"chain": null` plus a note saying where the
   family's chain is printed.
3. **`(12/4,5)`** — table 3, last row, the A_2 entry. Printed with the fraction
   `12/4`, not in lowest terms (the other entries in these tables are reduced).
   Transcribed exactly; not reduced, not corrected. Flagged in that case's `notes`.
4. **Two different corner notations between sections.** The Section 5 family tables
   print corners with the macro `\wrs`, which typesets as `≀`; the Section 6 case
   tables print corners with a plain `/`. Per the source's own definition (Sec. 2:
   "we will write $a\wrs l$ instead of $(a,l)$", and the geometric realization of
   `(a≀l, b)` is the point `(a/l, b)`), the two notations denote the same kind of
   object. Both are transcribed exactly as each table prints them; no notation was
   unified. `≀` is used in the JSON where the source uses `\wrs`.
5. **Red-marked rows.** Six table-1 rows are printed in red, meaning per the
   caption "possible counterexamples with max(deg(P),deg(Q)) <= 100". Colour is not
   recoverable from the PDF text layer, so the `red_in_source` flags are taken from
   the `\color{red}` markers in the LaTeX. The count is 6, which matches the
   paper's own prose ("Five of them correspond to the six cases found by Moh… The
   sixth red case, marked with a star, corresponds to F_22").
6. **The starred row.** `F_22 (2,3)*` carries a literal asterisk, independently
   visible in the PDF text layer as `F22(2,3)*96`. Recorded as
   `"star_in_source": true`.
7. **Symmetry caveat printed by the authors.** Both sections state: "We only list
   the cases satisfying equality (3.17). The other cases (satisfying (3.18)) can be
   obtained by swapping m with n." The swapped cases are therefore *not* present in
   the tables and are *not* present in the JSON. Recorded verbatim in the JSON's
   `source.text_note_verbatim`.

## Vocabulary note

The campaign's standing rule bars a certain word from files I author. The paper's
own section title and several of its sentences contain it. Because this task's
fidelity rule is absolute and this file is to serve as ground truth for an external
check, the published title and quoted sentences are reproduced verbatim in
`gghv_cases.json` rather than paraphrased. Every occurrence in that file is inside a
field whose name ends in `_verbatim` or is the quoted title of a published section;
none of it is my own characterization of anything.

## Not done, deliberately

- No degree pairs computed from `(m,n)` or from the chains.
- No family parameter `j` resolved, so no table-1 chain reconstructed.
- No fraction reduced, no notation normalized, no apparent irregularity corrected.
- Nothing extracted from any source other than the two arXiv fetches above; no
  table was reconstructed from memory.
