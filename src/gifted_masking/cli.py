from __future__ import annotations

import argparse
from pathlib import Path

from gifted_masking.experiments.robustness import write_suite
from gifted_masking.experiments.article import run_article_experiment
from gifted_masking.experiments.e02 import run_e02_experiment
from gifted_masking.experiments.e03 import run_e03_experiment
from gifted_masking.experiments.e04 import run_e04_experiment
from gifted_masking.experiments.e05 import run_e05_experiment
from gifted_masking.experiments.e06 import run_e06_experiment
from gifted_masking.plotting.legacy_figures import generate_all


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gifted_masking")
    subparsers = parser.add_subparsers(dest="command", required=True)

    robustness = subparsers.add_parser("robustness", help="Run robustness smoke checks.")
    robustness.add_argument("--output-dir", default="results", help="Directory for manifests, tables, and reports.")
    robustness.add_argument(
        "--suite",
        default="full",
        choices=["smoke", "full"],
        help="Robustness suite to execute.",
    )

    legacy = subparsers.add_parser("legacy-figures", help="Regenerate the legacy figure family with the modular package.")
    legacy.add_argument("--output-dir", default="results/figures", help="Directory for generated PNG files.")

    article = subparsers.add_parser("article-experiment", help="Run an approved config-driven article experiment.")
    article.add_argument("--config", required=True, help="Path to the approved article experiment JSON configuration.")
    article.add_argument("--output-dir", default="results", help="Directory for article experiment artifacts.")
    article.add_argument("--approval-record", help="Required GO_STANDARD approval record for a standard article experiment.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "robustness":
        outputs = write_suite(Path(args.output_dir), suite=args.suite)
        for key, value in outputs.items():
            print(f"{key}: {value}")
        return
    if args.command == "legacy-figures":
        outputs = generate_all(Path(args.output_dir))
        for value in outputs:
            print(value)
        return
    if args.command == "article-experiment":
        config_path = Path(args.config)
        # Each article experiment owns its own gate. Dispatching by the
        # explicit experiment identifier prevents one approval from becoming
        # authority to execute another experiment's standard work.
        import json
        experiment_id = json.loads(config_path.read_text()).get("experiment_id")
        runner = {"E01": run_article_experiment, "E02": run_e02_experiment, "E03": run_e03_experiment, "E04": run_e04_experiment, "E05": run_e05_experiment, "E06": run_e06_experiment}.get(experiment_id)
        if runner is None:
            raise ValueError(f"unknown article experiment identifier: {experiment_id!r}")
        outputs = runner(config_path, output_dir=Path(args.output_dir), approval_record=Path(args.approval_record) if args.approval_record else None)
        for key, value in outputs.items():
            print(f"{key}: {value}")
        return
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
