import unittest

import numpy as np

from gifted_masking.models import m0, m1


class M1Tests(unittest.TestCase):
    def test_disclosure_grid_includes_endpoints(self):
        grid = m1.disclosure_levels(5)
        self.assertEqual(grid[0], 0.0)
        self.assertEqual(grid[-1], 1.0)

    def test_expected_reward_matches_masking_at_zero_disclosure(self):
        reward = m1.expected_reward(0.0, p=0.4)
        mask, _ = m0.expected_rewards(0.4)
        self.assertAlmostEqual(float(reward), mask)

    def test_expected_reward_matches_authenticity_at_full_disclosure(self):
        reward = m1.expected_reward(1.0, p=0.4)
        _, authentic = m0.expected_rewards(0.4)
        self.assertAlmostEqual(float(reward), authentic)

    def test_higher_receptivity_increases_mean_disclosure(self):
        low = m1.simulate(0.2, n=200, horizon=900, seed=5).mean()
        high = m1.simulate(0.85, n=200, horizon=900, seed=6).mean()
        self.assertGreater(high, low)


if __name__ == "__main__":
    unittest.main()
