import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from gifted_masking.experiments.e06 import (
    RAW_FIELDS, derive_segment_seed, derive_tables, expected_rows, invert_transition,
    load_e06_config, loop_area, nondecreasing_pava, run_e06_experiment, replay_segment_parity,
    paired_student_t_effect, derive_bootstrap_seed, bootstrap_paired_transition_width,
    validate_e06_raw, validate_e06_derived,
)

ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "configs/frontiers_article/e06_m4_paths_smoke.json"
STANDARD = ROOT / "configs/frontiers_article/e06_m4_paths_standard.json"
QUALIFICATION = ROOT / "configs/frontiers_article/e06_m4_hysteresis_qualification.json"


class E06Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_e06_config(SMOKE)

    def test_frozen_configs_and_dispatch_refusal(self):
        self.assertEqual(expected_rows(self.config), 320)
        self.assertFalse(load_e06_config(STANDARD)["approved_standard"])
        self.assertFalse(load_e06_config(QUALIFICATION)["approved_qualification"])
        with self.assertRaises(PermissionError):
            run_e06_experiment(STANDARD, ROOT / "results")
        with self.assertRaises(PermissionError):
            run_e06_experiment(QUALIFICATION, ROOT / "results")
        duplicate = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        duplicate.write('{"experiment_id":"E06","experiment_id":"E06"}')
        duplicate.close()
        with self.assertRaises(ValueError): load_e06_config(Path(duplicate.name))

    def test_seed_pairing_and_directional_isolation(self):
        up = derive_segment_seed(2026081699, "S00", "up", 2, .002)
        self.assertEqual(up, derive_segment_seed(2026081699, "S00", "up", 2, .002))
        self.assertNotEqual(up, derive_segment_seed(2026081699, "S00", "down", 2, .002))
        self.assertNotEqual(up, derive_segment_seed(2026081699, "S00", "cold", 2, .002))

    def test_local_replay_matches_maintained_m4_for_stochastic_cases(self):
        scenario = self.config["scenarios"][0]
        for seed, km in ((7, .0), (19, .002), (29, .004)):
            replay_segment_parity(np.full(8, .45), np.zeros((8, 2)), km, seed, self.config, scenario)
        # Non-integral 1/3 final window uses the maintained ceiling convention.
        altered = copy.deepcopy(self.config); altered["final_window_fraction"] = 1 / 3
        replay_segment_parity(np.linspace(.1, .9, 8), np.zeros((8, 2)), .001, 31, altered, scenario)

    def test_standard_only_inference_helpers_are_synthetic_and_seed_isolated(self):
        effect = paired_student_t_effect([1., 2., 3., 4., 5.])
        self.assertEqual(effect["df"], 4.0); self.assertLess(effect["ci_low"], effect["estimate"])
        self.assertNotEqual(derive_bootstrap_seed(1, "S00", "mask", .5), derive_bootstrap_seed(1, "S00", "p", .5))
        up = [[.1, .4, .6, .9] for _ in range(5)]; down = [[.1, .3, .5, .9] for _ in range(5)]
        boot = bootstrap_paired_transition_width(up, down, [0., .001, .002, .004], bootstrap_seed=3, scenario_id="S00", response="mask", target=.5)
        self.assertTrue(boot["estimable"]); self.assertEqual(boot["valid"], 10000)

    def test_loop_area_and_pava_transition_boundaries(self):
        signed, absolute = loop_area([0, .002, .004], [0, .2, .4], [.1, .3, .5])
        self.assertAlmostEqual(signed, .0004)
        self.assertAlmostEqual(absolute, .0004)
        np.testing.assert_allclose(nondecreasing_pava([.2, .7, .5]), [.2, .6, .6])
        point, status = invert_transition([0, .002, .004], [.1, .5, .9], .5)
        self.assertEqual(status, "valid"); self.assertAlmostEqual(point, .002)
        self.assertEqual(invert_transition([0, .004], [.1, .2], .5)[1], "no_crossing_below")
        self.assertEqual(invert_transition([0, .004], [.8, .9], .5)[1], "no_crossing_above")
        with self.assertRaises(ValueError): invert_transition([0, 0], [.2, .8], .5)
        with self.assertRaises(ValueError): loop_area([0, .004], [0, float("nan")], [0, .1])

    def test_smoke_packed_rows_reconstruct_and_reject_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = run_e06_experiment(SMOKE, Path(tmp))
            import csv
            with out["raw"].open() as handle: rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 320)
            self.assertTrue(all(list(row) == RAW_FIELDS for row in rows))
            validate_e06_raw(rows, self.config)
            cells, paths, loops, transitions, effects = derive_tables(rows, self.config)
            self.assertTrue(cells and paths and loops and transitions and effects)
            bad = copy.deepcopy(rows); bad[0]["mask_count_json"] = "[0]"
            with self.assertRaises(ValueError): validate_e06_raw(bad, self.config)
            inherited = next(row for row in rows if row["path_type"] == "inherited_loop")
            self.assertEqual(len(json.loads(inherited["mask_rate_json"])), 10)
            cold = next(row for row in rows if row["path_type"] == "cold_start")
            self.assertEqual(len(json.loads(cold["mask_rate_json"])), 5)

    def test_derived_validation_rejects_all_named_adversarial_mutations(self):
        """Every emitted E06 derived table is raw-grounded and fail-closed."""
        with tempfile.TemporaryDirectory() as tmp:
            out = run_e06_experiment(SMOKE, Path(tmp))
            with out["raw"].open(newline="") as handle:
                raw = list(csv.DictReader(handle))
            tables = {}
            for name in ("cells", "paths", "loops", "transitions", "effects"):
                with out[name].open(newline="") as handle:
                    tables[name] = list(csv.DictReader(handle))
            validate_e06_derived(raw, tables["cells"], tables["paths"], tables["loops"], tables["transitions"], tables["effects"], self.config)

            def reject(name, mutate):
                altered = copy.deepcopy(tables)
                mutate(altered)
                with self.assertRaises(ValueError, msg=name):
                    validate_e06_derived(raw, altered["cells"], altered["paths"], altered["loops"], altered["transitions"], altered["effects"], self.config)

            # Values and identities across every reconstruction family.
            reject("cell mean", lambda t: t["cells"][0].__setitem__("mean_mask_rate", "0.123"))
            reject("cell identity", lambda t: t["cells"][0].__setitem__("scenario_id", "foreign"))
            reject("path gap", lambda t: t["paths"][0].__setitem__("mask_down_minus_up", "0"))
            reject("aligned km", lambda t: t["paths"][0].__setitem__("km", "0.0005"))
            reject("loop signed", lambda t: t["loops"][0].__setitem__("signed_area", "0"))
            reject("loop absolute", lambda t: t["loops"][0].__setitem__("absolute_area", "0"))
            control_loop = next(i for i, row in enumerate(tables["loops"]) if row["control_excess_area"] != "")
            reject("control excess", lambda t: t["loops"][control_loop].__setitem__("control_excess_area", "0"))
            reject("transition estimate", lambda t: t["transitions"][0].__setitem__("ascending_km", "0.001"))
            reject("transition censoring", lambda t: t["transitions"][0].__setitem__("status", "valid"))
            reject("transition eligibility", lambda t: t["transitions"][0].__setitem__("decision_eligible", "True"))
            reject("effect estimate", lambda t: t["effects"][0].__setitem__("estimate", "0"))
            reject("effect identity", lambda t: t["effects"][0].__setitem__("effect_name", "foreign_effect"))

            # Identity/cardinality faults and nonfinite derived values must not
            # be made harmless by CSV parsing or a numeric coercion.
            reject("row order", lambda t: t["cells"].__setitem__(slice(0, 2), [t["cells"][1], t["cells"][0]]))
            reject("duplicate", lambda t: t["paths"].append(copy.deepcopy(t["paths"][0])))
            reject("missing", lambda t: t["loops"].pop())
            reject("foreign", lambda t: t["effects"].append({**t["effects"][0], "effect_name": "foreign"}))
            reject("nan", lambda t: t["cells"][0].__setitem__("mean_p_end", "nan"))
            reject("infinity", lambda t: t["cells"][0].__setitem__("mean_p_end", "inf"))


if __name__ == "__main__":
    unittest.main()
