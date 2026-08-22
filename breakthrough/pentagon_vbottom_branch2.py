#!/usr/bin/env python3
"""Exact audit of the 45 v-bottom equations against w-descent branch 2.

This does not perform a costly expanded substitution.  It proves the stronger
coefficient identity: the coefficient of ``r^n`` at v-level ``V`` is exactly
the coefficient on w-level ``L=n-V`` of the original Jacobian equation.
Consequently every equation with L >= 15 is already zero on the reconstructed
level-15 branch, independently of its parametrization.
"""

from collections import Counter


def p_ok(j, i):
    return 0 <= i <= 8 and 0 <= j <= 16 and max(0, j-8) <= i <= min(8, j//2+1)


def q_ok(j, k):
    if not 0 <= k <= 12:
        return False
    lo = (k+1)//2 if k <= 2 else 2*k-3
    return lo <= j <= 12+k


def name(letter, j, i):
    return f"{letter}_{j}_{i}"


def vbottom_conditions():
    """Return (V, r-degree, sparse coefficient dictionary)."""
    out = []
    for V in range(-20, -11):
        coefficients = {}
        for d in range(-8, 3):
            e = V+1-d
            if not -12 <= e <= 3:
                continue
            for i in range(9):
                jp = 2*i-d
                if not p_ok(jp, i):
                    continue
                for k in range(13):
                    jq = 2*k-e
                    if not q_ok(jq, k):
                        continue
                    scalar = d*k-e*i
                    if scalar:
                        n = i+k-1
                        term = (name("p", jp, i), name("q", jq, k))
                        coefficients.setdefault(n, {})[term] = scalar
        out.extend((V, n, terms) for n, terms in sorted(coefficients.items()) if terms)
    assert len(out) == 45
    return out


def check_regrading_identity(V, n, terms):
    """Check every monomial and scalar against the w-ladder formula."""
    L = n-V
    for (pn, qn), scalar in terms.items():
        _, jp, i = pn.split("_")
        _, jq, k = qn.split("_")
        jp, i, jq, k = map(int, (jp, i, jq, k))
        a, b = jp-i, jq-k
        # w formula b*h_a'*g_b-a*h_a*g_b' has coefficient b*i-a*k.
        assert a+b == L
        assert scalar == b*i-a*k
    return L


def format_equation(terms):
    chunks = []
    for (pn, qn), scalar in sorted(terms.items()):
        sign = "+" if scalar > 0 else "-"
        magnitude = abs(scalar)
        body = f"{'' if magnitude == 1 else str(magnitude)+'*'}{pn}*{qn}"
        chunks.append((sign, body))
    first_sign, first = chunks[0]
    text = ("-" if first_sign == "-" else "") + first
    return text + "".join(f" {sign} {body}" for sign, body in chunks[1:])


def main():
    equations = vbottom_conditions()
    levels = [check_regrading_identity(*equation) for equation in equations]
    counts = Counter(levels)
    assert counts == {20: 9, 19: 8, 18: 7, 17: 6, 16: 5,
                      15: 4, 14: 3, 13: 2, 12: 1}

    discharged = [equation for equation, L in zip(equations, levels) if L >= 15]
    pending = [equation for equation, L in zip(equations, levels) if L < 15]
    assert len(discharged) == 39
    assert len(pending) == 6

    print("45 v-bottom equations reduced against branch 2 through w-level 15")
    print("  39 identities: coefficients of already-solved w-levels 15..20")
    print("  6 pending equations: coefficients of not-yet-descended levels 12..14")
    for V, n, terms in pending:
        print(f"  V={V}, r^{n}, w={n-V}: {format_equation(terms)} = 0")

    deepest = equations[0]
    assert deepest[0:2] == (-20, 0)
    assert check_regrading_identity(*deepest) == 20
    print("PASS: deepest scaling law is exactly the r^0 coefficient of w-level 20")


if __name__ == "__main__":
    main()
