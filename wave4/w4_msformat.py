"""
An msolve-input SANITISER and VALIDATOR, and the reason it exists.

TWO SILENT LIES IN msolve 0.10.1, found by minimal reproduction while auditing
this session's own generated inputs.  Both make msolve return a confident wrong
answer on a well-formed-looking file, with exit code 0.

L1  A CONSTANT GENERATOR WHOSE TERMS SUM TO A MULTIPLE OF THE CHARACTERISTIC IS
    READ AS NONZERO, and the system is declared EMPTY.

        a,b / 1000003 / "2 + 1000001," "a*b + 1000002," "a + 1000002"
        -> [-1]   (EMPTY)                    but 2 + 1000001 = 1000003 = 0,
                                             and a = b = 1 solves the rest.
        Writing the same generator as the single token "0" gives the correct
        non-empty answer.  Writing it as the single token "1000003" produces a
        ZERO-BYTE OUTPUT FILE.

L2  REPEATED MONOMIALS INSIDE ONE POLYNOMIAL ARE NOT COMBINED.

        "a + a + 1000001"   is solved as if it were   "a + 1000001"   (a = 2),
        while "2*a + 1000001" gives a = 1.  Two spellings of the same
        polynomial, two different answers, no diagnostic.

Consequence for this campaign: any generator produced by ADDING a term to an
existing polynomial -- which is exactly what a planted-mutant control does --
can silently acquire a duplicate monomial or a second constant, and msolve will
then answer a different question.  A planted control that comes back EMPTY is
the visible symptom; a real system that comes back EMPTY for the same reason is
the invisible one.

Every .ms file written by wave4/, symslice/ and gghv_audit/ is passed through
`sanitize_lines` (which folds duplicates and constants and reduces mod p) and
then through `validate` (which re-reads the file and fails loudly on any
duplicate monomial, any repeated constant, or any coefficient outside [0,p)).
"""

import re
import sys
from collections import defaultdict
from fractions import Fraction

# A term of an msolve polynomial: an optional sign, an optional rational
# coefficient, and any number of var^exp factors joined by '*'.
_SPLIT = re.compile(r"(?=[+-])")


def _terms(s):
    """Split a polynomial into signed terms, tolerating '+'/'-' with or without
    surrounding spaces, which is how the campaign's own .ms files are written."""
    s = s.strip().rstrip(",")
    if not s:
        raise ValueError("empty polynomial")
    out, buf, depth = [], "", 0
    for i, ch in enumerate(s):
        if ch in "+-" and buf.strip() and not buf.rstrip().endswith(("*", "^", "/", "+", "-")):
            out.append(buf)
            buf = ch if ch == "-" else ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf)
    return [t.strip() for t in out if t.strip()]


def _term(raw):
    """(Fraction coefficient, sorted tuple of variable letters with repeats)."""
    coef = Fraction(1)
    factors = []
    raw = raw.replace(" ", "")
    neg = raw.startswith("-")
    if raw[0] in "+-":
        raw = raw[1:]
    if not raw:
        raise ValueError("empty term")
    for tok in raw.split("*"):
        if re.fullmatch(r"\d+(/\d+)?", tok):
            coef *= Fraction(tok)
        elif re.fullmatch(r"[A-Za-z_]\w*\^\d+", tok):
            nm, e = tok.split("^")
            factors.extend([nm] * int(e))
        elif re.fullmatch(r"[A-Za-z_]\w*", tok):
            factors.append(tok)
        else:
            raise ValueError(f"unparsable token {tok!r} in term {raw!r}")
    if neg:
        coef = -coef
    return coef, tuple(sorted(factors))


def parse_poly(s, p):
    """{monomial: coefficient mod p} for one msolve polynomial string."""
    out = defaultdict(Fraction)
    for raw in _terms(s):
        c, m = _term(raw)
        out[m] += c
    red = {}
    for m, c in out.items():
        if p:
            v = (int(c.numerator) % p) * pow(int(c.denominator) % p, p - 2, p) % p
        else:
            v = c
        red[m] = v
    return red


def render(d):
    parts = []
    for mono in sorted(d, key=lambda m: (len(m), m)):
        c = d[mono]
        if c == 0:
            continue
        parts.append("*".join([str(c)] + _pow(mono)) if mono else str(c))
    return " + ".join(parts) if parts else "0"


def _pow(mono):
    out, i = [], 0
    while i < len(mono):
        j = i
        while j < len(mono) and mono[j] == mono[i]:
            j += 1
        out.append(mono[i] if j - i == 1 else f"{mono[i]}^{j - i}")
        i = j
    return out


def sanitize_lines(lines, p):
    return [render(parse_poly(L, p)) for L in lines]


def validate(path):
    """Re-read a written .ms file and report exactly the two hazards above.

    Reported: a monomial occurring more than once inside one generator (L2),
    more than one constant term (a special case of L2 that triggers L1), and --
    only when the characteristic is positive -- a written coefficient that is a
    nonzero multiple of the characteristic.
    """
    txt = open(path).read().rstrip()
    rows = txt.split("\n")
    if len(rows) < 3:
        raise SystemExit(f"{path}: fewer than 3 lines")
    p = int(rows[1].strip())
    problems = []
    body = " ".join(r.strip() for r in rows[2:]).split(",")
    for k, L in enumerate(body):
        L = L.strip()
        if not L:
            problems.append((k, "empty generator"))
            continue
        seen = defaultdict(int)
        for raw in _terms(L):
            try:
                c, m = _term(raw)
            except ValueError as e:
                problems.append((k, str(e)))
                continue
            seen[m] += 1
            if p and c.denominator == 1 and c.numerator and c.numerator % p == 0:
                problems.append((k, f"coefficient {c} is a nonzero multiple of "
                                    f"the characteristic (msolve silent lie L1)"))
        for m, c in seen.items():
            if c > 1:
                what = "constant term" if not m else f"monomial {m}"
                problems.append((k, f"{what} repeated {c} times "
                                    f"(msolve silent lie L2)"))
    return problems


if __name__ == "__main__":
    P = 1000003
    ok = True
    cases = [("a + a + 1000001", {("a",): 2, (): 1000001}),
             ("2*a + 1000001", {("a",): 2, (): 1000001}),
             ("2 + 1000001", {(): 0}),
             ("3*x^2*y + 999999*x^2*y", {("x", "x", "y"): 1000002})]
    print("=" * 74)
    print("SANITISER SELF-TEST")
    print("=" * 74)
    for s, want in cases:
        got = {k: v for k, v in parse_poly(s, P).items()}
        good = got == want
        ok &= good
        print(f"    [{'PASS' if good else 'FAIL'}] {s!r} -> {got}")
    # NEGATIVE control: the sanitiser must REJECT garbage
    bad = False
    try:
        parse_poly("a $ b", P)
    except ValueError:
        bad = True
    print(f"    [{'PASS' if bad else 'FAIL'}] NEGATIVE: unparsable input is rejected")
    ok &= bad
    # NEGATIVE control: validate() must FIND a planted duplicate
    open("/tmp/_ms_validate_probe.ms", "w").write(
        "a,b\n1000003\na + a + 1000001,\n2 + 1000001\n")
    probs = validate("/tmp/_ms_validate_probe.ms")
    found = (any("monomial" in m and "repeated" in m for _, m in probs)
             and any("constant term" in m and "repeated" in m for _, m in probs))
    print(f"    [{'PASS' if found else 'FAIL'}] NEGATIVE: validate() finds a "
          f"planted duplicate monomial and a double constant: {probs}")
    ok &= found
    open("/tmp/_ms_validate_clean.ms", "w").write(
        "a,b\n1000003\n" + ",\n".join(sanitize_lines(
            ["a + a + 1000001", "2 + 1000001"], P)) + "\n")
    probs2 = validate("/tmp/_ms_validate_clean.ms")
    print(f"    [{'PASS' if not probs2 else 'FAIL'}] the sanitised version is clean: "
          f"{probs2}")
    ok &= not probs2
    print("=" * 74)
    sys.exit(0 if ok else 1)
