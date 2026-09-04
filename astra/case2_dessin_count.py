"""Enumerate the five rooted plane trees in the case-(2) completeness proof.

The reduction of arbitrary admissible dessins to these trees is a mathematical
argument in ASTRA_2_CASE2_EXACT_DESCENT.md. This program checks the finite
enumeration, passports, transitivity, and inequivalence of its representatives.
No computer enumeration substitutes for that reduction argument.
"""
from functools import lru_cache


@lru_cache(None)
def binary_trees(n):
    if n == 0:
        return (None,)
    return tuple((left, right) for k in range(n)
                 for left in binary_trees(k)
                 for right in binary_trees(n - 1 - k))


def dessin(tree):
    black, white = [], []

    def visit(node):
        parent = len(black)
        black.extend((parent + 1, parent + 2, parent))
        white.extend((parent, parent + 1, parent + 2))
        if node is None:
            white[parent + 1], white[parent + 2] = parent + 2, parent + 1
        else:
            for offset, child in enumerate(node, 1):
                child_parent = visit(child)
                white[parent + offset] = child_parent
                white[child_parent] = parent + offset
        return parent

    assert visit(tree) == 0
    return black, white


def cycles(p):
    seen, out = set(), []
    for start in range(len(p)):
        if start in seen:
            continue
        cycle, x = [], start
        while x not in seen:
            seen.add(x)
            cycle.append(x)
            x = p[x]
        assert x == start
        out.append(cycle)
    return out


def canonical(b, w):
    # The unique white fixed point is a canonical root. Traverse using the
    # two named permutations: simultaneous conjugation cannot alter this code.
    root, = [i for i in range(len(w)) if w[i] == i]
    order, labels = [root], {root: 0}
    for x in order:
        for y in (b[x], w[x]):
            if y not in labels:
                labels[y] = len(order)
                order.append(y)
    assert len(order) == len(b), 'nontransitive dessin'
    return tuple((labels[b[x]], labels[w[x]]) for x in order)


def verify():
    trees = binary_trees(3)
    assert len(trees) == 5
    codes, records = set(), []
    for tree in trees:
        b, w = dessin(tree)
        face = [b[w[x]] for x in range(len(b))]
        passport = [sorted(map(len, cycles(p))) for p in (b, w, face)]
        assert passport == [[3]*7, [1]+[2]*10, [1]*4+[17]]
        assert sum(len(cycles(p)) for p in (b, w, face)) - len(b) == 2
        codes.add(canonical(b, w))
        records.append({'tree': tree, 'black': b, 'white': w,
                        'passport': passport})
    assert len(codes) == 5
    return records


if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2))
    print('CASE2 DESSIN ENUMERATION: PASS (5 inequivalent representatives)')
