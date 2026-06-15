import unittest

import numpy as np

from gifted_masking.models import m3


class M3Tests(unittest.TestCase):
    def test_action_decoding_matches_flattened_layout(self):
        group, authentic = m3.decode_action(np.array([0, 1, 6, 7]))
        np.testing.assert_array_equal(group, np.array([0, 0, 3, 3]))
        np.testing.assert_array_equal(authentic, np.array([False, True, False, True]))

    def test_expected_reward_uses_bflpe_only_for_good_pond_acceptance(self):
        no_cost = m3.expected_reward_for_action(1, k_groups=4, bf=0.0)
        with_cost = m3.expected_reward_for_action(1, k_groups=4, bf=0.5)
        bad_group = m3.expected_reward_for_action(3, k_groups=4, bf=0.5)
        self.assertLess(float(with_cost), float(no_cost))
        self.assertAlmostEqual(float(bad_group), float(m3.expected_reward_for_action(3, k_groups=4, bf=0.0)))

    def test_more_groups_reduce_good_pond_settling_in_smoke_case(self):
        k1 = m3.simulate(1, n=180, horizon=1000, seed=9)[0].mean()
        k8 = m3.simulate(8, n=180, horizon=1000, seed=10)[0].mean()
        self.assertGreater(k1, k8)

    def test_hierarchical_formulation_runs_and_prefers_k1_over_k8(self):
        k1 = m3.simulate_hierarchical(1, n=180, horizon=1000, seed=11)[0].mean()
        k8 = m3.simulate_hierarchical(8, n=180, horizon=1000, seed=12)[0].mean()
        self.assertGreater(k1, k8)

    def test_global_mask_formulation_runs(self):
        settle, mask_rate, modal = m3.simulate_global_mask(4, n=96, horizon=500, seed=13)
        self.assertEqual(settle.shape, (96,))
        self.assertEqual(mask_rate.shape, (96,))
        self.assertEqual(modal.shape, (96,))

    def test_fixed_good_pond_runs(self):
        settle, mask_rate, modal = m3.simulate_fixed_good_pond(n=96, horizon=500, seed=14)
        self.assertEqual(settle.shape, (96,))
        self.assertEqual(mask_rate.shape, (96,))
        self.assertEqual(modal.shape, (96,))


if __name__ == "__main__":
    unittest.main()
