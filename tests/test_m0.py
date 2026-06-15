import unittest

import numpy as np

from gifted_masking.models import m0


class M0Tests(unittest.TestCase):
    def test_expected_rewards_match_reference_values(self):
        mask, authentic = m0.expected_rewards(0.5, b=1.0, a=0.6, c=0.25, r=2.0)
        self.assertAlmostEqual(mask, 0.75)
        self.assertAlmostEqual(authentic, 0.1)

    def test_objective_gap_zero_at_reference_threshold(self):
        gap = m0.expected_gap(2.15 / 3.0, 1.0, 0.6, 0.25, 2.0)
        self.assertAlmostEqual(gap, 0.0, places=7)

    def test_lambda_one_matches_baseline_subjective_curve(self):
        p_value = 0.5
        self.assertAlmostEqual(m0.subjective_indifference_r(p_value, 1.0), 0.7)

    def test_higher_receptivity_reduces_mean_mask_rate(self):
        low = m0.simulate(0.2, n=200, horizon=900, seed=1).mean()
        high = m0.simulate(0.85, n=200, horizon=900, seed=2).mean()
        self.assertGreater(low, high)

    def test_higher_loss_aversion_increases_mask_rate_near_boundary(self):
        low_lam = m0.simulate(0.65, lam=0.5, n=200, horizon=900, seed=3).mean()
        high_lam = m0.simulate(0.65, lam=2.5, n=200, horizon=900, seed=4).mean()
        self.assertGreater(high_lam, low_lam)


if __name__ == "__main__":
    unittest.main()
