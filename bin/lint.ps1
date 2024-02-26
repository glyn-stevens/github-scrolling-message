$TARGER_DIR=("src", "tests")

"`nRunning ruff format:"
poetry run ruff format $TARGER_DIR

"`nRunning ruff lint:"
poetry run ruff --fix --show-fixes $TARGER_DIR

"`nRunning mypy:"
poetry run mypy $TARGER_DIR --ignore-missing-imports --check-untyped-defs