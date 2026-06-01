# tools/

Python helpers using the repo's root uv venv (at `~/.virtualenvs/ai-kitchen`).

## Conventions

- One file per tool: `tools/<name>.py` (or `tools/<name>/` for multi-file tools).
- Run via `uv run python tools/<name>.py` — uv resolves against `pyproject.toml`.
- Add deps with `uv add <pkg>` from the repo root. They land in `pyproject.toml` + `uv.lock`.
- Tools that aren't part of a published plugin live here. If a tool *becomes* part of a skill, it moves into `plugin/skills/<name>/` or `plugin/resources/`.

## What `tools/` is NOT for

- Production code (use a proper repo).
- One-off shell commands (just type them).
- Plugin assets (those go in `plugin/resources/`).
