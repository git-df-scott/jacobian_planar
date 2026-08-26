#!/usr/bin/env python3
"""Exact collision-first Hamiltonian incidence over finite fields.

Normalize a hypothetical collision to a=(0,0), b=(1,0), F(a)=F(b)=0.
For fixed P, the equations [P,Q]=1, Q(a)=Q(b)=0 are linear in the
coefficients of Q.  This module constructs and solves that complete linear
system without a reduced Laurent model or a reverse-lift step.

A modular solution is only CANDIDATE-UNVERIFIED.  It must lie on a component
that lifts to characteristic zero and then pass exact complex-number-field
Jacobian and collision checks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

Monomial = Tuple[int, int]
Polynomial = Dict[Monomial, int]


def bracket(P: Polynomial, Q: Polynomial, prime: int) -> Polynomial:
    out: Polynomial = {}
    for (i, j), a in P.items():
        for (k, ell), b in Q.items():
            multiplier = i*ell-j*k
            if not multiplier:
                continue
            target = (i+k-1, j+ell-1)
            out[target] = (out.get(target, 0)+multiplier*a*b) % prime
    return {monomial: value for monomial, value in out.items() if value % prime}


def value_at(polynomial: Polynomial, point: Tuple[int, int], prime: int) -> int:
    x, y = point
    return sum(coefficient*pow(x, i, prime)*pow(y, j, prime)
               for (i, j), coefficient in polynomial.items()) % prime


def rref(matrix: Sequence[Sequence[int]], prime: int):
    a = [[int(value) % prime for value in row] for row in matrix]
    if not a:
        return a, []
    rows, columns = len(a), len(a[0])
    pivots = []
    row = 0
    for column in range(columns):
        pivot = next((r for r in range(row, rows) if a[r][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inverse = pow(a[row][column], prime-2, prime)
        a[row] = [value*inverse % prime for value in a[row]]
        for r in range(rows):
            if r == row or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [(x-factor*y) % prime for x, y in zip(a[r], a[row])]
        pivots.append(column)
        row += 1
        if row == rows:
            break
    return a, pivots


def solve_affine(matrix: Sequence[Sequence[int]], rhs: Sequence[int], prime: int):
    """Return one solution and a nullspace basis, or None if inconsistent."""
    augmented = [list(row)+[value] for row, value in zip(matrix, rhs)]
    rr, pivots_all = rref(augmented, prime)
    columns = len(matrix[0])
    if any(all(value % prime == 0 for value in row[:columns])
           and row[columns] % prime for row in rr):
        return None
    pivots = [column for column in pivots_all if column < columns]
    free = [column for column in range(columns) if column not in pivots]
    particular = [0]*columns
    for row, pivot in enumerate(pivots):
        particular[pivot] = rr[row][columns] % prime
    nullspace = []
    for free_column in free:
        vector = [0]*columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rr[row][free_column] % prime
        nullspace.append(vector)
    return particular, nullspace, len(pivots)


def weighted_triangle(x_degree: int, y_degree: int) -> List[Monomial]:
    """All lattice points in i/x_degree + j/y_degree <= 1."""
    return [(i, j) for j in range(y_degree+1)
            for i in range(x_degree+1)
            if y_degree*i+x_degree*j <= x_degree*y_degree]


def collision_polynomial(support: Sequence[Monomial], values: Sequence[int],
                         prime: int) -> Polynomial:
    """Decode free values into P with P(0,0)=P(1,0)=0.

    The constant coefficient is zero.  The largest positive-x bottom-row
    coefficient is the pivot enforcing the second equality.
    """
    support = list(support)
    if (0, 0) not in support:
        raise ValueError("support must contain (0,0)")
    bottom = sorted(i for i, j in support if j == 0 and i > 0)
    if not bottom:
        raise ValueError("support needs a positive-x bottom monomial")
    pivot = (bottom[-1], 0)
    free = [monomial for monomial in support if monomial not in ((0, 0), pivot)]
    if len(values) != len(free):
        raise ValueError(f"expected {len(free)} free coefficients")
    polynomial = {monomial: value % prime for monomial, value in zip(free, values)}
    polynomial[pivot] = -sum(polynomial.get((i, 0), 0) for i in bottom[:-1]) % prime
    return {monomial: value for monomial, value in polynomial.items() if value}


@dataclass
class Incidence:
    p_support: List[Monomial]
    q_support: List[Monomial]
    targets: List[Monomial]

    @classmethod
    def create(cls, p_support: Iterable[Monomial], q_support: Iterable[Monomial]):
        ps = sorted(set(p_support))
        qs = sorted(set(q_support))
        targets = {(0, 0)}
        for i, j in ps:
            for k, ell in qs:
                if i*ell-j*k:
                    targets.add((i+k-1, j+ell-1))
        return cls(ps, qs, sorted(targets))

    def system(self, P: Polynomial, prime: int):
        """Matrix for [P,Q]=1 plus Q(0,0)=Q(1,0)=0."""
        target_index = {monomial: row for row, monomial in enumerate(self.targets)}
        matrix = [[0]*len(self.q_support) for _ in range(len(self.targets)+2)]
        rhs = [0]*(len(self.targets)+2)
        rhs[target_index[(0, 0)]] = 1
        for column, (k, ell) in enumerate(self.q_support):
            for (i, j), coefficient in P.items():
                multiplier = i*ell-j*k
                if multiplier:
                    row = target_index[(i+k-1, j+ell-1)]
                    matrix[row][column] = (
                        matrix[row][column]+multiplier*coefficient) % prime
            # Q(0,0)=0 and Q(1,0)=0.
            matrix[-2][column] = int((k, ell) == (0, 0))
            matrix[-1][column] = int(ell == 0)
        return matrix, rhs

    def solve(self, P: Polynomial, prime: int):
        matrix, rhs = self.system(P, prime)
        answer = solve_affine(matrix, rhs, prime)
        if answer is None:
            return None
        particular, kernel, rank = answer
        Q = {monomial: particular[index] for index, monomial in enumerate(self.q_support)
             if particular[index] % prime}
        return Q, kernel, rank

    def verify(self, P: Polynomial, Q: Polynomial, prime: int):
        expected = {(0, 0): 1 % prime}
        return {
            "P_collision": value_at(P, (0, 0), prime) == value_at(P, (1, 0), prime) == 0,
            "Q_collision": value_at(Q, (0, 0), prime) == value_at(Q, (1, 0), prime) == 0,
            "jacobian": bracket(P, Q, prime) == expected,
        }


def controls():
    prime = 101
    support = weighted_triangle(2, 2)
    incidence = Incidence.create(support, support)

    # Independent tensor check on a dense pair.
    P = {(0, 0): 3, (1, 0): 5, (0, 1): 7, (2, 0): 11, (1, 1): 13}
    Q = {(0, 0): 17, (1, 0): 19, (0, 1): 23, (0, 2): 29, (1, 1): 31}
    matrix, _ = incidence.system(P, prime)
    q_vector = [Q.get(monomial, 0) for monomial in incidence.q_support]
    product = [sum(a*b for a, b in zip(row, q_vector)) % prime for row in matrix]
    direct = bracket(P, Q, prime)
    expected = [direct.get(target, 0) for target in incidence.targets]
    assert product[:-2] == expected

    # Known Keller automorphism: passes [x,y]=1, fails the forced P collision.
    keller_P, keller_Q = {(1, 0): 1}, {(0, 1): 1}
    check = incidence.verify(keller_P, keller_Q, prime)
    assert check == {"P_collision": False, "Q_collision": True, "jacobian": True}
    solved = incidence.solve(keller_P, prime)
    assert solved is not None
    solved_Q, _, _ = solved
    assert incidence.verify(keller_P, solved_Q, prime)["jacobian"]

    # A genuine colliding pair: passes both collision rows but its Jacobian is
    # visibly nonconstant, ensuring the gates cannot be conflated.
    colliding_P = {(1, 0): -1 % prime, (2, 0): 1, (0, 1): 1}
    colliding_Q = {(1, 0): -1 % prime, (2, 0): 1, (0, 1): 2}
    check = incidence.verify(colliding_P, colliding_Q, prime)
    assert check == {"P_collision": True, "Q_collision": True, "jacobian": False}

    decoded = collision_polynomial(support, list(range(1, len(support)-1)), prime)
    assert value_at(decoded, (0, 0), prime) == value_at(decoded, (1, 0), prime) == 0
    return True


if __name__ == "__main__":
    controls()
    print("COLLISION-FIRST INCIDENCE CONTROLS: PASS")
