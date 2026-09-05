"""Char-0 Singular exports for Operation 108.

Reuses trackD_extract.build_singular verbatim and patches exactly two
char-dependent artifacts: the ring characteristic (P -> 0) and the modular
inverses (pow(k+1, P-2, P) -> 1/(k+1), and the rhs sign -1 == P-1 -> -1).
Everything else (recurrence, support conditions, vertex saturation,
facstd verdict) is untouched, so the char-0 system is THE same system the
mod-p queue runs — the campaign's standing requirement that char-0 and
mod-p verdicts come from one construction.

Emits:
  deg108_case1_char0.sing   (8,28)(3,2) subcase (1) pentagons   [OPEN]
  deg108_case2_char0.sing   (8,28)(3,2) subcase (2) quadrilaterals [OPEN]
  deg108_927_char0.sing     (9,27) shape, [P,Q]=x  [control: killed by
                             GGHV 2204.14178 Thm 5.1/Cor 5.7 - must be EMPTY]
"""
import re

import trackB1_shapes as SH
import trackD_extract as EX


def to_char0(src):
    out = []
    for line in src.splitlines():
        m = re.match(r"^ring R = \d+, (.*)$", line)
        if m:
            out.append(f"ring R = 0, {m.group(1)}")
            continue
        m = re.match(r"^poly Q(\d+) = \((.*)\) \* w \* (\d+);$", line)
        if m:
            k1 = int(m.group(1))
            out.append(f"poly Q{k1} = ({m.group(2)}) * w / {k1};")
            continue
        m = re.match(rf"^poly Rr0 = (\d+)\*x\^(\d+);$", line)
        if m:
            c = int(m.group(1))
            c0 = 1 if c == 1 else -1          # P-1 mod P encodes -1
            out.append(f"poly Rr0 = ({c0})*x^{m.group(2)};")
            continue
        out.append(line)
    return "\n".join(out)


def main():
    jobs = [(SH.SHAPES[0], "deg108_case1_char0.sing"),
            (SH.SHAPES[1], "deg108_case2_char0.sing"),
            (SH.SHAPES[2], "deg108_927_char0.sing")]
    for sh, fn in jobs:
        src, info = EX.build_singular(sh.NA, sh.NB, sh.rhs[0][0],
                                      name=fn.split(".")[0])
        assert src is not None, f"{sh.name}: OUT OF SCOPE?!"
        src0 = to_char0(src)
        # sanity: no residual mod-p constants in Q-row definitions
        assert not re.search(r"\* w \* \d{2,};", src0)
        assert "ring R = 0," in src0
        open(fn, "w").write(src0)
        print(f"{fn}: params={info['nparams']} jmax={info['jmax']} "
              f"driver_is_P={info['driver_is_P']}")


if __name__ == "__main__":
    main()
