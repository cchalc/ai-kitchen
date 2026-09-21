# ai-kitchen

Personal incubator for Databricks Field Engineering skills and tools. Drafts live in `scratch/`; mature work moves to `plugin/`; finished pieces ship to the official Vibe marketplace via `/vibe-publish-plugin`.

## Quickstart

```bash
# 1. Clone (already done if you're reading this locally)
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
| `plugin/` | Publishable Vibe plugin (manifest + skills + commands + agents + hooks). |
| `scratch/` | Drafts. Not published. Promote by `git mv` into `plugin/skills/`. |
| `tools/` | Python helpers using the root uv venv. |
| `docs/` | Formal design specs under `docs/superpowers/`. |

## Living docs

- [`CLAUDE.md`](./CLAUDE.md) — session bootstrap for Claude
- [`architecture.md`](./architecture.md) — design rationale
- [`tasks.md`](./tasks.md) — rolling work list
- [`lessons.md`](./lessons.md) — append-only learnings
- [`checkpoint.md`](./checkpoint.md) — "where I left off"

## VCS

`jj` is the primary VCS, colocated with git for GitHub interop. Worktrees via `wt` (worktrunk). All worktrees share one venv at `~/.virtualenvs/ai-kitchen`.

## License

Open source under the [MIT License](./LICENSE). The vendored `plugin/skills/frontend-design`
skill retains its own upstream license ([Apache-2.0](./plugin/skills/frontend-design/LICENSE.txt),
from [anthropics/skills](https://github.com/anthropics/skills)).
