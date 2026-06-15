import unittest

import numpy as np

from gifted_masking.core import softmax_probabilities, subjective_value


class CoreTests(unittest.TestCase):
    def test_softmax_rejects_nonpositive_temperature(self):
        with self.assertRaises(ValueError):
            softmax_probabilities(np.array([[1.0, 2.0]]), 0.0)

    def test_subjective_value_only_scales_negative_rewards(self):
        rewards = np.array([-2.0, -0.1, 0.0, 1.5])
        values = subjective_value(rewards, 2.5)
        np.testing.assert_allclose(values, np.array([-5.0, -0.25, 0.0, 1.5]))


if __name__ == "__main__":
    unittest.main()
