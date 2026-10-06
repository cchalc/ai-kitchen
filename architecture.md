# Architecture

This document explains *why* the repo is shaped the way it is. For *what's where*, see [`README.md`](./README.md). For Claude session bootstrap, see [`CLAUDE.md`](./CLAUDE.md). For the full design spec, see [`docs/superpowers/specs/2026-05-26-ai-kitchen-design.md`](./docs/superpowers/specs/2026-05-26-ai-kitchen-design.md).

## Public Mirror Role

This repo is a **public mirror** of shared Claude Code skills. Canonical development happens in a private companion repo (`ai-kitchen-dbx`). Files here are written by the companion repo's mirror tool, keyed on the frontmatter tag `metadata.visibility: public`. Skills tagged with this visibility sync bidirectionally between repos.

The mirror keeps the public and private development synchronized while allowing the private repo to hold additional closed-source work.

## Top-level shape: plugin in a subdir

The repo is a *hybrid* — a Claude Code plugin with shared skills AND Python tooling for skill development and routing validation. The plugin lives in `plugin/`; everything else lives next to it.

**Why not plugin at root?**  Mixes plugin metadata (`.claude-plugin/plugin.json`) with Python metadata (`pyproject.toml`, `devenv.nix`) and scratch work at the same level. Blurs "what gets published/mirrored" vs. "what doesn't."

**Why not multiple plugins?**  Premature. There's one plugin today. If a second arrives, restructure then.

**Trade-off accepted:** Plugin validation and skill routing testing must be run from `plugin/` or the repo root (one `cd`). Acceptable in exchange for the clean boundary.

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

## Routing validation

Skills use `tools/route_eval.py` for routing validation. It runs each prompt through headless `claude -p --plugin-dir ./plugin` in a throwaway git repo and scores the first `Skill` call against all available skills (300+), requiring the plugin-qualified prefix (`ai-kitchen:skillname`) to disambiguate from built-in skills with identical names (e.g. `code-review`).

Each skill gets exactly 2 routing evals in `skill-routing.yaml` (vibe CI hard limit). This validates that the skill is routed correctly without false negatives or positives.

## Rejected alternatives

| Considered | Why rejected |
|---|---|
| Plugin at root | Blurs mirror/non-mirror boundary. |
| Multiple plugins per repo | Premature for one plugin. |
| Plain git as primary | jj's history-rewriting story is materially better for skill iteration. |
| Per-worktree venvs (gist verbatim) | Slow worktree switches; deps rarely diverge per-branch in a skills repo. |
| Homebrew for any dependency | Forbidden (see `~/.agents/behaviors/package-management/BEHAVIOR.md`). |
| Pre-commit hooks (ruff/black) | Defer until Python in `tools/` grows beyond trivial. |
| `claude plugin eval` for routing | Sandbox isolation prevents credential access; use headless `claude -p` instead. |
