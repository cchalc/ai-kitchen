# ai-kitchen

Open-source developer-workflow skills for Claude Code. This is a **public mirror** of shared skills — canonical development happens in a private companion repo, and files here are written by its mirror tool. Skills tagged `metadata.visibility: public` sync bidirectionally.

## 12 Shared Skills

All 12 skills focus on developer workflow: commit discipline, PR review, changelog hygiene, licensing, testing, and CI setup. Each includes explicit negative triggers and routing evals to ensure accurate Claude Code skill routing.

## Quickstart

```bash
# 1. Clone
git clone git@github.com:cchalc/ai-kitchen.git

# 2. Enter the directory and approve direnv
cd ai-kitchen
direnv allow

# 3. devenv loads a Nix-pinned Python 3.11 shell + uv, and runs `uv sync`
#    on first entry. The venv lives at ~/.virtualenvs/ai-kitchen.
```

If you don't have devenv, the `.envrc` falls back to bare direnv + uv (you'll need both installed and a Python 3.11+ on PATH).

## Repo layout

| Path | What it holds |
|---|---|
| `plugin/` | Claude Code plugin manifest + 12 shared skills + commands + agents. |
| `plugin/skills/<name>/SKILL.md` | Individual skill definitions, all tagged `metadata.visibility: public`. |
| `.agents/` | Shared agent config mirrored from the companion repo. |
| `skill-routing.yaml` | Routing evals (max 2 per skill); run with `uv run python tools/route_eval.py`. |
| `tools/` | Python helpers using the root uv venv. |
| `docs/` | Design specs under `docs/superpowers/`. |
| `scratch/` | Drafts. Not mirrored. Promote by `git mv` into `plugin/skills/`. |

## Mirror workflow

This repo is a one-way read + one-way write mirror:
- **Read from here** → companion repo imports via `pull-public` (merges with `metadata.visibility: public`)
- **Write here** → allowed; `pull-public` detects and rejects both-sides-edited conflicts

If you see a conflict, the instructions are in the companion repo's error message.

## Living docs

- [`CLAUDE.md`](./CLAUDE.md) — session bootstrap for Claude
- [`architecture.md`](./architecture.md) — design rationale
- [`tasks.md`](./tasks.md) — rolling work list
- [`lessons.md`](./lessons.md) — append-only learnings
- [`checkpoint.md`](./checkpoint.md) — "where I left off"

## Validation

```bash
# Validate the plugin and all skills
claude plugin validate plugin/

# Test skill routing (run from repo root)
uv run python tools/route_eval.py skill-routing.yaml
```

## VCS

`jj` is the primary VCS, colocated with git for GitHub interop. Worktrees via `wt` (worktrunk). All worktrees share one venv at `~/.virtualenvs/ai-kitchen`.

## License

Open source under the [MIT License](./LICENSE). The vendored `plugin/skills/frontend-design`
skill retains its own upstream license ([Apache-2.0](./plugin/skills/frontend-design/LICENSE.txt),
from [anthropics/skills](https://github.com/anthropics/skills)).
