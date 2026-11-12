PY_M = python3 -m
UV_RUN = $(PY_M) uv run

install:
	uv sync

run:
	$(UV_RUN) python3 pac-man.py config.json

run_cheat_mode:
	$(UV_RUN) python3 pac-man.py config.json --cheat_mode

lint:
	@$(UV_RUN) $(PY_M) flake8 . --exclude=.venv
	@$(UV_RUN) mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

debug:
	@$(UV_RUN) $(PY_M) pdb pac-man.py config.json

clean:
	@$(PY_M) uv clean
	@rm -rf .mypy_cache
	rm -rf */__pycache__

.PHONY: install run clean lint lint-strict debug