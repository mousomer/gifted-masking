.PHONY: bootstrap verify robustness legacy-figures

bootstrap:
	./scripts/bootstrap_venv.sh

verify:
	./scripts/verify.sh

robustness:
	. .venv/bin/activate && python -m gifted_masking.cli robustness --output-dir results

legacy-figures:
	. .venv/bin/activate && python -m gifted_masking.cli legacy-figures --output-dir results/figures
