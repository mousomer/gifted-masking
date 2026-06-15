import unittest

import numpy as np

from gifted_masking.models import m0, m1, m2, m3, m4


class DeterminismTests(unittest.TestCase):
    def test_m0_seed_is_deterministic(self):
        first = m0.simulate(0.6, n=64, horizon=300, seed=101)
        second = m0.simulate(0.6, n=64, horizon=300, seed=101)
        np.testing.assert_allclose(first, second)

    def test_m1_seed_is_deterministic(self):
        first = m1.simulate(0.6, n=64, horizon=300, seed=102)
        second = m1.simulate(0.6, n=64, horizon=300, seed=102)
        np.testing.assert_allclose(first, second)

    def test_m2_seed_is_deterministic(self):
        first = m2.simulate(0.6, 0.05, n=64, horizon=300, seed=103)
        second = m2.simulate(0.6, 0.05, n=64, horizon=300, seed=103)
        np.testing.assert_allclose(first, second)

    def test_m3_seed_is_deterministic(self):
        first = m3.simulate(4, n=64, horizon=300, seed=104)[1]
        second = m3.simulate(4, n=64, horizon=300, seed=104)[1]
        np.testing.assert_allclose(first, second)

    def test_m4_seed_is_deterministic(self):
        first = m4.simulate(0.45, 0.001, n=64, horizon=300, seed=105)[0]
        second = m4.simulate(0.45, 0.001, n=64, horizon=300, seed=105)[0]
        np.testing.assert_allclose(first, second)


if __name__ == "__main__":
    unittest.main()
