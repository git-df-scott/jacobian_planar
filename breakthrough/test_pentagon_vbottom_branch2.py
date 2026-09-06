#!/usr/bin/env python3
"""Regression tests for the exact v/w coefficient audit."""

import unittest

from pentagon_vbottom_branch2 import check_regrading_identity, vbottom_conditions


class VBottomBranchTwoTests(unittest.TestCase):
    def setUp(self):
        self.equations = vbottom_conditions()

    def test_exact_count_and_w_distribution(self):
        levels = [check_regrading_identity(*equation) for equation in self.equations]
        self.assertEqual(len(levels), 45)
        self.assertEqual(
            {level: levels.count(level) for level in set(levels)},
            {12: 1, 13: 2, 14: 3, 15: 4, 16: 5,
             17: 6, 18: 7, 19: 8, 20: 9},
        )

    def test_deepest_equation_exactly(self):
        V, degree, terms = self.equations[0]
        self.assertEqual((V, degree), (-20, 0))
        self.assertEqual(
            terms,
            {("p_8_0", "q_13_1"): -8, ("p_9_1", "q_12_0"): 12},
        )
        self.assertEqual(check_regrading_identity(V, degree, terms), 20)

    def test_no_term_is_lost_by_sparse_aggregation(self):
        for _, _, terms in self.equations:
            self.assertTrue(terms)
            self.assertNotIn(0, terms.values())
            self.assertEqual(len(terms), len(set(terms)))


if __name__ == "__main__":
    unittest.main()
