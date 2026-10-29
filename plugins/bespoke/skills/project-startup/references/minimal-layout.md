# Minimal layout (template `none`)

Use when no template profile is chosen. `{{pkg}}` is the project name with `-` → `_`;
`{{dist}}` is the hyphenated name.

```
pyproject.toml
.python-version          # 3.12
Makefile
src/{{pkg}}/__init__.py
tests/test_smoke.py
```

`pyproject.toml`:

```toml
[project]
name = "{{dist}}"
version = "0.1.0"
description = "{{one-line description}}"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest>=8", "pyright>=1.1.400", "ruff>=0.9"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{{pkg}}"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q --strict-markers --strict-config"

[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.12"
```

`Makefile` (recipes are tab-indented):

```make
.DEFAULT_GOAL := help
.PHONY: help install lint format test

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "  %-10s %s\n", $$1, $$2}'

install:  ## Install dependencies, including dev
	uv sync --all-groups

lint:  ## Check formatting, lint, and types
	uv run ruff format --check .
	uv run ruff check .
	uv run pyright

format:  ## Fix formatting and auto-fixable lint
	uv run ruff format .
	uv run ruff check --fix .

test:  ## Run the tests (no credentials needed)
	uv run pytest
```

`tests/test_smoke.py`:

```python
import {{pkg}}


def test_imports():
    assert {{pkg}}.__name__ == "{{pkg}}"
```
