# Architecture

This document explains *why* the repo is shaped the way it is. For *what's where*, see [`README.md`](./README.md). For Claude session bootstrap, see [`CLAUDE.md`](./CLAUDE.md). For the full design spec, see [`docs/superpowers/specs/2026-05-26-ai-kitchen-design.md`](./docs/superpowers/specs/2026-05-26-ai-kitchen-design.md).

## Top-level shape: plugin in a subdir (Approach C)

The repo is a *hybrid* — a publishable Claude Code plugin AND a personal scratchpad with Python tooling. The plugin lives in `plugin/`; everything else lives next to it.

**Why not Approach A (plugin at root)?**  Mixes plugin metadata (`.claude-plugin/plugin.json`) with Python metadata (`pyproject.toml`, `devenv.nix`) and scratch work at the same level. Blurs "what gets published" vs. "what doesn't."

**Why not Approach B (marketplace with multiple plugins)?**  Premature. There's one plugin today. If a second arrives, restructure then.

**Trade-off accepted:** `/vibe-publish-plugin` must be run from `plugin/` (one `cd`). Acceptable in exchange for the clean boundary.

## VCS: jj colocated with git

`jj` is the primary local interface; `git` exists only because GitHub speaks git. `jj git init --colocate` enables both in the same checkout. Why jj as primary:
- First-class working-copy commits (no separate "stage" + "commit" dance).
- Trivial history rewriting (`jj squash`, `jj split`, `jj rebase`).
- `.gitignore` is honored — no separate `.jjignore` needed.

## Python: devenv + uv (dual path)

`devenv.nix` is preferred (Nix-pinned Python 3.11 + uv, reproducible across machines). `.envrc` falls back to bare `direnv + uv` if devenv isn't installed. Both paths point the venv at `~/.virtualenvs/ai-kitchen` — a hardcoded path so `wt` worktrees share one venv instead of multiplying.

**Why hardcode the venv path?** The gist's `$(basename "$PWD")` pattern multiplies venvs across worktrees (one per branch). For a skills repo where deps barely change, one shared venv is faster and simpler. Cost: renaming the repo dir requires editing one line in `.envrc` and `devenv.nix`.

## Living docs at root, not under `docs/`

Four files at root (`tasks.md`, `lessons.md`, `architecture.md`, `checkpoint.md`) are *living* — Claude updates them during real work. They surface in `ls`. Formal, dated design specs live deeper under `docs/superpowers/specs/` because they're stable historical records.

## Rejected alternatives

| Considered | Why rejected |
|---|---|
| Approach A (plugin at root) | Blurs publish/non-publish boundary. |
| Approach B (marketplace + multiple plugins) | Premature for one author with one plugin. |
| Plain git as primary | jj's history-rewriting story is materially better for skill iteration. |
| Per-worktree venvs (gist verbatim) | Slow worktree switches; deps rarely diverge per-branch in a skills repo. |
| Homebrew for any dependency | Globally forbidden on this host (see `~/.claude/CLAUDE.md`). |
| Pre-commit hooks (ruff/black) | Defer until Python in `tools/` grows beyond trivial. |
