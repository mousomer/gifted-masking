import copy
import csv
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from gifted_masking.experiments.e06 import (
    RAW_FIELDS, STANDARD_CELL_FIELDS, STANDARD_LOOP_FIELDS, STANDARD_SEEDS,
    GO_BINDING_FIELDS, STANDARD_COMMAND, STANDARD_CONFIG_RELATIVE, SEALED_SMOKE_MANIFEST_RELATIVE,
    derive_segment_seed, derive_tables, derive_e06_standard_tables, expected_rows,
    expected_learner_steps, iter_e06_family_specs, e06_seed_map_key, invert_transition,
    load_e06_config, loop_area, nondecreasing_pava, run_e06_experiment, replay_segment_parity,
    paired_student_t_effect, derive_bootstrap_seed, bootstrap_paired_transition_width,
    validate_e06_raw, validate_e06_derived, validate_e06_raw_csv_streaming,
    validate_e06_standard_derived, validate_e06_standard_go_binding,
    e06_standard_readiness_projection, validate_e06_gzip_member, GZIP_SETTINGS,
    load_e06_standard_compression_fixture, authenticate_e06_standard_compression_fixture,
    validate_e06_post_seal_git_drift, E06ResourceGuard, STANDARD_COMPRESSION_FIXTURE_RELATIVE,
)
from gifted_masking.experiments.e06 import _canon, _expected_raw_rows, _open_deterministic_gzip_csv, _parse_e06_go_binding, _read_e06_csv, _standard_cells_from_family, _standard_figure
from gifted_masking.experiments.e06 import (
    EXPECTED_FOCUSED_COMMANDS, EXPECTED_USER_FULL_COMMAND, FOCUSED_EVIDENCE_ORDER,
    SCIENTIFIC_OUTPUT_NAMES, build_e06_full_verification_evidence,
    record_e06_preverification, seal_e06_verification,
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

    def test_standard_cardinality_order_seed_keys_and_readiness(self):
        config = load_e06_config(STANDARD)
        specs = list(iter_e06_family_specs(config))
        self.assertEqual(expected_rows(config), 52000)
        self.assertEqual(expected_learner_steps(config), 913000000)
        self.assertEqual(len(specs), 130)
        self.assertEqual((specs[0][0], specs[0][1]["id"], specs[0][2]), (STANDARD_SEEDS[0], "S00", "inherited_loop"))
        self.assertEqual((specs[-1][0], specs[-1][1]["id"], specs[-1][2]), (STANDARD_SEEDS[-1], "S08", "km_disabled_reversal_only"))
        keys = [e06_seed_map_key(master, scenario["id"], path) for master, scenario, path in specs]
        self.assertEqual(len(keys), len(set(keys)))
        projection = e06_standard_readiness_projection(ROOT / SEALED_SMOKE_MANIFEST_RELATIVE, ROOT)
        self.assertTrue(projection["within_strict_review_limits"])
        self.assertTrue(projection["within_formal_limits"])
        self.assertLessEqual(projection["raw_mib"], projection["strict_review_limits"]["raw_mib"])
        self.assertLessEqual(projection["raw_mib"], projection["formal_execution_limits"]["raw_mib"])
        self.assertIn("streaming_replay", projection["components_seconds"])
        self.assertEqual(projection["compression_fixture"]["rows"], 52000)
        self.assertGreater(projection["logical_raw_size_bound"]["bound_mib"], projection["raw_mib"])

    def test_compression_fixture_record_is_current_and_adversarially_bound(self):
        config = load_e06_config(STANDARD); canonical = ROOT / STANDARD_COMPRESSION_FIXTURE_RELATIVE
        record = load_e06_standard_compression_fixture(canonical, ROOT, config)
        self.assertEqual(record["status"], "passed"); self.assertTrue(record["within_limits"])
        mutations = {
            "source": ("source_fingerprint_sha256", "0"*64),
            "rows": ("rows", 51999),
            "scientific": ("scientific", True),
            "compressed_size": ("compressed_raw_mib", 1.0),
            "logical_size": ("logical_raw_mib", 1.0),
            "total_size": ("stored_total_bound_mib", 1.0),
            "status": ("status", "failed"),
            "within": ("within_limits", False),
        }
        for name,(field,value) in mutations.items():
            altered=copy.deepcopy(record);altered[field]=value
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/"fixture.json";path.write_text(json.dumps(altered))
                self.assertFalse(load_e06_standard_compression_fixture(path,ROOT,config)["within_limits"])
        altered=copy.deepcopy(record);altered["fingerprint"]["settings"]["mtime"]=1
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"fixture.json";path.write_text(json.dumps(altered))
            self.assertFalse(load_e06_standard_compression_fixture(path,ROOT,config)["within_limits"])

    def test_standard_go_binding_is_exact_and_fails_closed(self):
        smoke_path = ROOT / SEALED_SMOKE_MANIFEST_RELATIVE
        smoke = json.loads(smoke_path.read_text())
        config = load_e06_config(STANDARD)
        source_fingerprint = smoke["source_fingerprint_sha256"]
        binding = dict(zip(GO_BINDING_FIELDS, (
            "GO_STANDARD", "E06", STANDARD_CONFIG_RELATIVE,
            hashlib.sha256(_canon(config).encode()).hexdigest(), source_fingerprint,
            SEALED_SMOKE_MANIFEST_RELATIVE, hashlib.sha256(smoke_path.read_bytes()).hexdigest(),
            "projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md",
            hashlib.sha256((ROOT / "projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md").read_bytes()).hexdigest(),
            STANDARD_COMMAND, "REFUSED",
        ), strict=True))
        block = "```e06-go-binding\n" + json.dumps(binding, separators=(",", ":")) + "\n```"
        self.assertEqual(_parse_e06_go_binding(block), binding)
        report=ROOT / "results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md"
        synthetic_sealed={"verification":{"status":"passed","seal_state":"external_evidence_verified"},"source_fingerprint_sha256":source_fingerprint,"git":{"dirty_paths":[]},"outputs":{"report":{"path":str(report),"sha256":hashlib.sha256(report.read_bytes()).hexdigest()}}}
        with mock.patch("gifted_masking.experiments.e06._source_fingerprint", return_value=source_fingerprint), mock.patch("gifted_masking.experiments.e06._strict_json", return_value=synthetic_sealed), mock.patch("gifted_masking.experiments.e06._git_porcelain_inventory", return_value={"dirty_paths":[]}):
            validate_e06_standard_go_binding(binding, STANDARD, ROOT)
            for field in GO_BINDING_FIELDS:
                altered = dict(binding); altered[field] = "foreign"
                with self.subTest(field=field):
                    with self.assertRaises(PermissionError): validate_e06_standard_go_binding(altered, STANDARD, ROOT)
        with self.assertRaises(PermissionError): _parse_e06_go_binding(block + "\n" + block)
        with self.assertRaises(ValueError): _parse_e06_go_binding('```e06-go-binding\n{"decision":"GO_STANDARD","decision":"GO_STANDARD"}\n```')

    def test_streaming_raw_replay_accepts_exact_smoke_and_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = run_e06_experiment(SMOKE, Path(tmp))
            replay = validate_e06_raw_csv_streaming(out["raw"], self.config)
            self.assertEqual((replay["rows"], replay["families"], replay["peak_retained_packed_rows"]), (320, 5, 64))
            raw = _expected_raw_rows(self.config); standard_cells = []
            for offset in range(0, len(raw), self.config["n"]):
                standard_cells.extend(_standard_cells_from_family(raw[offset:offset + self.config["n"]], self.config))
            cells_path = Path(tmp) / "standard_cells.csv"
            with cells_path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=STANDARD_CELL_FIELDS); writer.writeheader(); writer.writerows(standard_cells)
            self.assertEqual(validate_e06_raw_csv_streaming(out["raw"], self.config, cells_path=cells_path)["families"], 5)
            altered_cells = copy.deepcopy(standard_cells); altered_cells[0]["p_end_q50"] += .01
            with cells_path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=STANDARD_CELL_FIELDS); writer.writeheader(); writer.writerows(altered_cells)
            with self.assertRaises(ValueError): validate_e06_raw_csv_streaming(out["raw"], self.config, cells_path=cells_path)
            rows = _read_e06_csv(out["raw"], RAW_FIELDS); rows[0]["child_id"] = "1"
            corrupt = Path(tmp) / "corrupt.csv"
            with corrupt.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS); writer.writeheader(); writer.writerows(rows)
            with self.assertRaises(ValueError): validate_e06_raw_csv_streaming(corrupt, self.config)

    def test_deterministic_gzip_is_canonical_and_streaming_rejects_container_corruption(self):
        rows = _expected_raw_rows(self.config)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); paths = [root / "a.csv.gz", root / "b.csv.gz"]
            logical = []
            for path in paths:
                raw_handle, gzip_handle, compressed, logical_writer = _open_deterministic_gzip_csv(path)
                try:
                    writer = csv.DictWriter(logical_writer, fieldnames=RAW_FIELDS); writer.writeheader(); writer.writerows(rows)
                finally:
                    gzip_handle.close(); raw_handle.close()
                logical.append((logical_writer.bytes, logical_writer.hexdigest()))
                fingerprint = validate_e06_gzip_member(path)
                self.assertEqual(fingerprint["settings"], GZIP_SETTINGS)
                self.assertEqual((fingerprint["logical_csv_bytes"], fingerprint["logical_csv_sha256"]), logical[-1])
                self.assertEqual(validate_e06_raw_csv_streaming(path, self.config)["rows"], 320)
            self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())
            self.assertEqual(logical[0], logical[1])

            malformed = root / "malformed.gz"; malformed.write_bytes(b"not gzip")
            with self.assertRaises(ValueError): validate_e06_gzip_member(malformed)
            trailing = root / "trailing.gz"; trailing.write_bytes(paths[0].read_bytes() + b"foreign")
            with self.assertRaises(ValueError): validate_e06_gzip_member(trailing)
            concatenated = root / "concatenated.gz"; concatenated.write_bytes(paths[0].read_bytes() + paths[1].read_bytes())
            with self.assertRaises(ValueError): validate_e06_gzip_member(concatenated)
            wrong_header = root / "wrong_header.gz"; payload = bytearray(paths[0].read_bytes()); payload[4] = 1; wrong_header.write_bytes(payload)
            with self.assertRaises(ValueError): validate_e06_gzip_member(wrong_header)

    def test_resource_guard_stops_before_over_limit_write_and_bootstrap_completion(self):
        ticks = iter((0., 0., 2.))
        guard = E06ResourceGuard(clock=lambda: next(ticks), rss_source=lambda: 1., limits={"seconds": 1.})
        guard.check("synthetic setup")
        with self.assertRaisesRegex(RuntimeError, "phase=synthetic phase: seconds"):
            guard.check("synthetic phase")
        byte_guard = E06ResourceGuard(clock=lambda: 0., rss_source=lambda: 1., limits={"logical_raw_mib": 0.})
        with self.assertRaisesRegex(RuntimeError, "logical_raw_mib"):
            byte_guard.check("logical synthetic", logical_bytes=1)
        rss_guard = E06ResourceGuard(clock=lambda: 0., rss_source=lambda: 2., limits={"rss_mib": 1.})
        with self.assertRaisesRegex(RuntimeError, "rss_mib"):
            rss_guard.check("RSS synthetic")

    def test_post_seal_git_drift_requires_content_match(self):
        report = ROOT / "results/reports/frontiers_m4_path_diagnostics_v1_smoke_report.md"
        checkpoint = ROOT / "projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md"
        baseline = {"status":" M","path":"already-untracked.txt","bytes":3,"sha256":"a" * 64}
        smoke = {"git":{"dirty_paths":[baseline]},"outputs":{"report":{"path":str(report),"sha256":hashlib.sha256(report.read_bytes()).hexdigest()}}}
        binding = {"review_checkpoint_path":"projects/frontiers_article/checkpoints/E06_COMPRESSION_SOL_REVIEW.md","review_checkpoint_sha256":hashlib.sha256(checkpoint.read_bytes()).hexdigest()}
        with mock.patch("gifted_masking.experiments.e06._git_porcelain_inventory", return_value={"dirty_paths":[dict(baseline)]}):
            validate_e06_post_seal_git_drift(smoke, binding, ROOT)
        changed = dict(baseline); changed["sha256"]="b" * 64
        with mock.patch("gifted_masking.experiments.e06._git_porcelain_inventory", return_value={"dirty_paths":[changed]}):
            with self.assertRaises(PermissionError): validate_e06_post_seal_git_drift(smoke, binding, ROOT)

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

    def test_standard_derived_package_uses_master_inference_and_rejects_mutation(self):
        config = load_e06_config(STANDARD)
        cells = []; xs = [float(x) for x in config["km_values"]]
        for master_index, master in enumerate(STANDARD_SEEDS):
            jitter = master_index * .001
            for scenario in config["scenarios"]:
                for path in scenario["path_types"]:
                    directions = ("cold",) if path == "cold_start" else ("up", "down")
                    gap = {"inherited_loop":.08,"reversal_only":.02,"km_disabled_inherited_loop":.01,"km_disabled_reversal_only":.005}.get(path, 0.)
                    for direction in directions:
                        for km in xs:
                            if direction == "cold": mask = .15 + 170*km + jitter; p_end = .8 - 60*km - jitter
                            else:
                                slope = 10 if path.startswith("km_disabled_") else 190
                                mask = .12 + slope*km + jitter + (gap if direction == "down" else 0.)
                                p_end = .86 - 90*km - jitter - (gap/2 if direction == "down" else 0.)
                            mask = min(.99,max(.01,mask)); p_end = min(.94,max(.06,p_end)); n = int(config["n"])
                            payload = [config["run_id"],"E06","standard",scenario["id"],path,direction,km,master,n,mask,.01,p_end,.01,.4,.5,100,100,70,30,0,p_end-.02,p_end,p_end+.02]
                            cells.append(dict(zip(STANDARD_CELL_FIELDS,payload,strict=True)))
        paths, loops, transitions, effects = derive_e06_standard_tables(cells, config)
        validate_e06_standard_derived(cells, paths, loops, transitions, effects, config)
        pooled_loops = [row for row in loops if row["master_seed"] == "pooled"]
        self.assertTrue(pooled_loops)
        self.assertTrue(all(row["n_master"] == 5 and row["ci_low"] != "" and row["ci_high"] != "" for row in pooled_loops))
        pooled_transitions = [row for row in transitions if row["master_seed"] == "pooled"]
        self.assertTrue(pooled_transitions)
        self.assertTrue(all(row["bootstrap_replicates"] == 10000 for row in pooled_transitions))
        self.assertTrue(any(row["decision_eligible"] == "True" for row in pooled_transitions))
        self.assertTrue(any(row["decision_eligible"] == "False" and row["ci_low"] == "" and row["ci_high"] == "" for row in pooled_transitions))
        summaries = [row for row in effects if row["level"] == "five_master_summary"]
        self.assertTrue(summaries)
        with tempfile.TemporaryDirectory() as tmp:
            figure = Path(tmp) / "standard.png"; _standard_figure(figure, cells, paths, loops, transitions)
            self.assertGreater(figure.stat().st_size, 0)
        altered = copy.deepcopy(effects); altered[-1]["estimate"] = float(altered[-1]["estimate"]) + .01
        with self.assertRaises(ValueError): validate_e06_standard_derived(cells, paths, loops, transitions, altered, config)

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

    def test_raw_validator_rejects_complete_frozen_contract_in_memory_and_csv(self):
        """Named review mutations must fail at both supported raw boundaries."""
        material = _expected_raw_rows(self.config)

        def changed(field, value, row_index=0):
            result = copy.deepcopy(material)
            result[row_index][field] = value
            return result

        inherited = next(i for i,row in enumerate(material) if row["path_type"] == "inherited_loop")
        disabled = next(i for i,row in enumerate(material) if row["path_type"] == "km_disabled_reversal_only")
        seed_map = json.loads(material[0]["policy_environment_seed_map_json"])
        nested_seed_map = copy.deepcopy(seed_map); nested_seed_map[0]["seed"] += 1
        cases = [
            ("scenario_role", changed("scenario_role", "foreign")),
            ("matched_family_id", changed("matched_family_id", "foreign")),
            ("seed_map", changed("policy_environment_seed_map_json", "[]")),
            ("seed_map_member", changed("policy_environment_seed_map_json", json.dumps(nested_seed_map, separators=(",", ":")))),
            ("child_seed", changed("child_seed", "foreign")), ("rng_unit", changed("rng_unit", "foreign")),
            ("declared_n", changed("n", 63)), ("window_start", changed("final_window_start", 95)), ("window_end", changed("final_window_end", 118)),
            ("ka", changed("ka", 0.11)), ("km_mode", changed("km_mode", "disabled")),
            ("nominal_grid", changed("nominal_km_values_json", "[0.0,0.001,0.002,0.003,0.005]")), ("alpha", changed("alpha", 0.2)),
            ("traversal_direction", changed("traversal_direction_json", "[\"down\",\"up\",\"up\",\"up\",\"up\",\"down\",\"down\",\"down\",\"down\",\"down\"]", inherited)),
            ("traversal_nominal", changed("traversal_nominal_km_json", "[0.004,0.001,0.002,0.003,0.004,0.004,0.003,0.002,0.001,0.0]", inherited)),
            ("traversal_actual", changed("traversal_actual_km_json", "[0.001,0.001,0.002,0.003,0.004,0.004,0.003,0.002,0.001,0.0]", inherited)),
            ("inherited_auth_q", changed("q_auth_start_json", "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", inherited)),
            ("inherited_mask_q", changed("q_mask_start_json", "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", inherited)),
            ("disabled_reversal_p", changed("p_start_json", "[0.5,0.45,0.45,0.45,0.45,0.45,0.45,0.45,0.45,0.45]", disabled)),
            ("disabled_reversal_q_mask", changed("q_mask_start_json", "[0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", disabled)),
            ("disabled_reversal_q_auth", changed("q_auth_start_json", "[0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", disabled)),
            ("wrong_array_length", changed("mask_rate_json", "[0.0]")), ("wrong_json_type", changed("mask_count_json", "{\"count\":1}")),
            ("duplicate_json_key", changed("policy_environment_seed_map_json", "[{\"direction\":\"up\",\"direction\":\"down\"}]")), ("nan", changed("final_p", float("nan"))), ("infinity", changed("final_p", float("inf"))),
        ]
        cases.extend([
            ("missing_row", material[:-1]), ("duplicate_row", material + [copy.deepcopy(material[0])]),
            ("reordered_row", [material[1], material[0], *material[2:]]),
            ("foreign_row", changed("scenario_id", "foreign")),
        ])
        for name, bad in cases:
            with self.subTest(boundary="materialized", mutation=name):
                with self.assertRaises(ValueError):
                    validate_e06_raw(bad, self.config)
            with self.subTest(boundary="parsed_csv", mutation=name):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "raw.csv"
                    with path.open("w", newline="") as handle:
                        writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS)
                        writer.writeheader(); writer.writerows(bad)
                    with self.assertRaises(ValueError):
                        validate_e06_raw(_read_e06_csv(path, RAW_FIELDS), self.config)

    def test_derived_boundary_rejects_raw_identity_seed_parameter_traversal_reset_and_both_q(self):
        raw = _expected_raw_rows(self.config)
        tables = derive_tables(raw, self.config)
        corruptions = {
            "identity": ("matched_family_id", "foreign", 0), "seed": ("policy_environment_seed_map_json", "[]", 0),
            "parameter": ("alpha", 0.2, 0), "traversal": ("traversal_direction_json", "[\"cold\"]", 0),
            "reset": ("p_start_json", "[0.5,0.45,0.45,0.45,0.45,0.45,0.45,0.45,0.45,0.45]", next(i for i,r in enumerate(raw) if r["path_type"] == "km_disabled_reversal_only")),
            "mask_q": ("q_mask_start_json", "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", next(i for i,r in enumerate(raw) if r["path_type"] == "inherited_loop")),
            "auth_q": ("q_auth_start_json", "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", next(i for i,r in enumerate(raw) if r["path_type"] == "inherited_loop")),
        }
        for name,(field,value,index) in corruptions.items():
            bad = copy.deepcopy(raw); bad[index][field] = value
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    validate_e06_derived(bad, *tables, self.config)

    def test_external_seal_reconstructs_evidence_and_rejects_all_required_corruption(self):
        """Synthetic only: every acceptance/rejection case seals a temporary package."""
        def digest(path):
            return hashlib.sha256(path.read_bytes()).hexdigest()

        def full_log():
            return (
                "Verification Python: /Users/omer/workspace/venvs/venv314/bin/python\n"
                "Ran 113 tests in 128.937s\n\nOK\n"
                "Ran 1 test in 1.937s\n\nOK\n"
                "Ran 1 test in 1.956s\n\nOK\n"
                "Ran 2 tests in 3.861s\n\nOK\n"
            )

        def focused_evidence(root):
            records=[]
            for index,name in enumerate(FOCUSED_EVIDENCE_ORDER, start=1):
                path=root/f"focused_{name}.log"; command=EXPECTED_FOCUSED_COMMANDS[name]
                path.write_text(f"command={command}\nRan {index} tests in {index}.250s\n\nOK\nexit_code=0\n")
                records.append({"name":name,"command":command,"log_path":str(path),"log_sha256":digest(path),"exit_code":0,"test_count":index,"runtime_seconds":float(f"{index}.250"),"passed":True})
            return {"status":"passed","records":records}

        def deterministic_evidence(first, second):
            def run_record(out):
                manifest=json.loads(out["manifest"].read_text())
                return {"manifest_path":str(out["manifest"]),"report_path":str(out["report"]),"scientific_artifacts":{name:manifest["scientific_artifacts"][name] for name in SCIENTIFIC_OUTPUT_NAMES}}
            return {"status":"passed","runs":[run_record(first),run_record(second)],"scientific_byte_comparison":"passed","normalized_manifest_report":"passed","normalization_rules":["manifest.timing", "manifest.timestamps", "manifest.git", "manifest.standard_projection", "manifest.qualification_projection", "manifest.command output-root only", "manifest.outputs.*.path output-root only", "manifest.outputs.report bytes/sha256", "manifest.output_hashes.report", "report item 9 runtime/projection", "report item 10 qualification projection"]}

        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            # These three fresh roots are intentionally independent of the canonical package.
            first=run_e06_experiment(SMOKE,root/"fresh_a")
            second=run_e06_experiment(SMOKE,root/"fresh_b")
            out=run_e06_experiment(SMOKE,root/"package")
            focused=focused_evidence(root); deterministic=deterministic_evidence(first,second)
            record_e06_preverification(out,focused,deterministic)
            log=root/"verify.log"; exit_record=root/"verify.exit"
            log.write_text(full_log()); exit_record.write_text("verification_exit_code=0\n")
            evidence=build_e06_full_verification_evidence(log,exit_record)
            pending_manifest=out["manifest"].read_bytes(); pending_report=out["report"].read_bytes()
            pending_raw=out["raw"].read_bytes()
            pending_focused={Path(record["log_path"]):Path(record["log_path"]).read_bytes() for record in focused["records"]}

            seal_e06_verification(out,evidence)
            sealed=json.loads(out["manifest"].read_text())
            self.assertEqual(sealed["verification"]["status"],"passed")
            self.assertIn("external-seal status `passed`",out["report"].read_text())
            with self.assertRaises(ValueError):
                seal_e06_verification(out,evidence)

            def restore():
                out["manifest"].write_bytes(pending_manifest); out["report"].write_bytes(pending_report)
                out["raw"].write_bytes(pending_raw)
                for path,payload in pending_focused.items(): path.write_bytes(payload)
                log.write_text(full_log()); exit_record.write_text("verification_exit_code=0\n")

            def rejected(name, mutate):
                with self.subTest(corruption=name):
                    restore(); altered=copy.deepcopy(evidence); mutate(altered)
                    with self.assertRaises(ValueError):
                        seal_e06_verification(out,altered)

            rejected("altered_verification_log",lambda _: log.write_text(full_log()+"foreign evidence\n"))
            rejected("altered_exit_record",lambda value: (exit_record.write_text("verification_exit_code=00\n"),value.__setitem__("exit_sha256",digest(exit_record))))
            rejected("wrong_command",lambda value: value.__setitem__("command","./scripts/verify.sh"))
            for deceptive in ("verification_exit_code=1\n","verification_exit_code=01\n","verification_exit_code=00\n","verification_exit_code=0\nforeign\n"):
                rejected(f"deceptive_exit_{deceptive!r}",lambda value,text=deceptive: (exit_record.write_text(text),value.__setitem__("exit_sha256",digest(exit_record))))
            rejected("caller_count_mismatch",lambda value: value.__setitem__("test_count",118))
            rejected("caller_runtime_mismatch",lambda value: value.__setitem__("runtime_seconds",1.0))
            rejected("incomplete_suite_log",lambda value: (log.write_text(full_log().rsplit("Ran 2 tests",1)[0]),value.__setitem__("log_sha256",digest(log))))
            rejected("failed_suite_log",lambda value: (log.write_text(full_log()+"FAILED (failures=1)\n"),value.__setitem__("log_sha256",digest(log))))

            def stale_source(_):
                source=ROOT/"src/gifted_masking/experiments/e06.py"; original=source.stat().st_mtime
                os.utime(source,(original,log.stat().st_mtime+60))
                self.addCleanup(lambda: os.utime(source,(original,original)))
            rejected("stale_source_evidence",stale_source)
            os.utime(ROOT/"src/gifted_masking/experiments/e06.py",None)
            # Recreate evidence after the freshness test because the source timestamp is now newer.
            log.write_text(full_log()); exit_record.write_text("verification_exit_code=0\n"); evidence=build_e06_full_verification_evidence(log,exit_record)
            pending_manifest=out["manifest"].read_bytes(); pending_report=out["report"].read_bytes()

            def manifest_mutation(field, value):
                manifest=json.loads(out["manifest"].read_text()); manifest[field]=value; out["manifest"].write_text(json.dumps(manifest,indent=2)+"\n")
            rejected("source_fingerprint_drift",lambda _: manifest_mutation("source_fingerprint_sha256","0"*64))
            rejected("config_drift",lambda _: manifest_mutation("config_sha256","0"*64))
            rejected("approval_drift",lambda _: (lambda m: (m["authorization"].__setitem__("approval_sha256","0"*64),out["manifest"].write_text(json.dumps(m,indent=2)+"\n")))(json.loads(out["manifest"].read_text())))
            for key in ("head","branch","porcelain_sha256"):
                rejected(f"git_{key}_drift",lambda _,key=key: (lambda m: (m["git"].__setitem__(key,"foreign"),out["manifest"].write_text(json.dumps(m,indent=2)+"\n")))(json.loads(out["manifest"].read_text())))
            rejected("dirty_state_hash_drift",lambda _: (lambda m: (m["git"].__setitem__("dirty",not m["git"]["dirty"]),out["manifest"].write_text(json.dumps(m,indent=2)+"\n")))(json.loads(out["manifest"].read_text())))
            rejected("changed_scientific_artifact",lambda _: out["raw"].write_bytes(out["raw"].read_bytes()+b"drift\n"))
            rejected("missing_focused_evidence",lambda _: manifest_mutation("focused_verification",{"status":"pending_external_focused_logs"}))
            rejected("altered_focused_log",lambda _: Path(focused["records"][0]["log_path"]).write_text("altered\n"))
            rejected("missing_deterministic_evidence",lambda _: manifest_mutation("deterministic_regeneration",{"status":"pending_external_fresh_runs"}))
            rejected("normalized_scientific_mismatch",lambda _: (lambda m: (m["deterministic_regeneration"]["runs"][1]["scientific_artifacts"]["raw"].__setitem__("sha256","0"*64),out["manifest"].write_text(json.dumps(m,indent=2)+"\n")))(json.loads(out["manifest"].read_text())))
            rejected("inconsistent_pending_state",lambda _: (lambda m: (m["verification"].__setitem__("seal_state","external_evidence_verified"),out["manifest"].write_text(json.dumps(m,indent=2)+"\n")))(json.loads(out["manifest"].read_text())))

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
