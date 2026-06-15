import unittest

import numpy as np

from gifted_masking.models import m4


class M4Tests(unittest.TestCase):
    def test_update_receptivity_respects_bounds(self):
        p_t = np.array([0.95, 0.05, 0.50])
        authentic = np.array([True, True, False])
        accepted = np.array([True, False, False])
        updated = m4.update_receptivity(
            p_t,
            authentic,
            accepted,
            km=0.5,
            ka=0.5,
            kr=0.5,
            p_min=0.05,
            p_max=0.95,
        )
        self.assertTrue(np.all(updated >= 0.05))
        self.assertTrue(np.all(updated <= 0.95))

    def test_simulation_clips_initial_receptivity(self):
        _, final_p, _ = m4.simulate(1.2, 0.001, n=64, horizon=200, seed=11)
        self.assertTrue(np.all(final_p <= 0.95))

    def test_higher_entrenchment_increases_mask_rate(self):
        low = m4.simulate(0.45, 0.0, n=180, horizon=1000, seed=12)[0].mean()
        high = m4.simulate(0.45, 0.003, n=180, horizon=1000, seed=13)[0].mean()
        self.assertGreater(high, low)

    def test_hysteresis_experiment_returns_matched_paths(self):
        result = m4.hysteresis_experiment(0.45, np.linspace(0.0, 0.003, 5), n=96, horizon=200, seed=14)
        self.assertEqual(result["mask_up"].shape, (5,))
        self.assertEqual(result["mask_down"].shape, (5,))
        self.assertEqual(result["p_up"].shape, (5,))
        self.assertEqual(result["p_down"].shape, (5,))


if __name__ == "__main__":
    unittest.main()
