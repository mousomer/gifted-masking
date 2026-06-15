from __future__ import annotations

import argparse
from pathlib import Path

from gifted_masking.experiments.robustness import write_suite
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
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
