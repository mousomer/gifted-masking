import unittest

import numpy as np

from gifted_masking.models import m2


class M2Tests(unittest.TestCase):
    def test_neutral_authentic_acceptance_transitions_to_accepted(self):
        reward, state = m2.transition_step(
            np.array([m2.STATE_NEUTRAL]),
            np.array([1]),
            p=0.8,
            eta=0.1,
            outcome_uniform=np.array([0.1]),
            turnover_uniform=np.array([0.9]),
            escape_uniform=np.array([0.9]),
        )
        self.assertEqual(state[0], m2.STATE_ACCEPTED)
        self.assertAlmostEqual(reward[0], 1.6)

    def test_stigmatized_masking_keeps_state_without_escape(self):
        reward, state = m2.transition_step(
            np.array([m2.STATE_STIGMATIZED]),
            np.array([0]),
            p=0.8,
            eta=0.1,
            outcome_uniform=np.array([0.1]),
            turnover_uniform=np.array([0.9]),
            escape_uniform=np.array([0.9]),
        )
        self.assertEqual(state[0], m2.STATE_STIGMATIZED)
        self.assertAlmostEqual(reward[0], 0.25)

    def test_higher_escape_rate_reduces_mean_mask_rate(self):
        low = m2.simulate(0.55, 0.0, n=160, horizon=1000, seed=7).mean()
        high = m2.simulate(0.55, 0.2, n=160, horizon=1000, seed=8).mean()
        self.assertGreater(low, high)


if __name__ == "__main__":
    unittest.main()
