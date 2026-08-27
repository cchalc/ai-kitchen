# Agent harness setup — omnigent + pi + devenv (generic)

The lean, reproducible essentials for setting up this repo's agent-harness environment on a
fresh machine. **Generic only** — no company servers, profiles, or gateways. (Company-specific
config lives in a separate private repo and layers on top of these defaults.)

## What's here

| File | Purpose |
|---|---|
| `.omnigent/config.yaml` | Per-project omnigent workstream override (harness/model) for this repo |
| `.pi/settings.json` | pi harness settings (retry policy) |
| `devenv.nix` + `.envrc` | Reproducible dev shell (Nix + uv), shared venv |

## Prerequisites (installed globally, e.g. via your system package manager / Nix)

- `omnigent` (the `omni` CLI) — the meta-harness
- `pi` — the coding-agent harness
- `devenv` + `direnv` — reproducible shell
- `uv` — Python env/deps

Keep global installs to binaries only. All per-project *runtime* config (harness, model,
database URIs, providers) belongs at the directory level — in `.omnigent/config.yaml` and
`.envrc` — not in your global machine config.

## omnigent — per-project workstream

`omni` merges `~/.omnigent/config.yaml` (global) with `<project>/.omnigent/config.yaml`
(this repo). The `harness` key deep-merges; `model` replaces. So this repo can pin its own
harness/model without changing anything global.

```bash
# from this repo root:
omni config list          # shows the effective config; the project overlay appears
                          # under this repo's .omnigent/config.yaml path
omni run --harness claude-sdk -p "hello"   # or just `omni run <agent-dir>`
```

`.omnigent/config.yaml` here sets `harness: claude-sdk` and leaves the model to the configured
provider's default. Edit it to pin a different harness or model for this project.

> Note: omnigent also auto-discovers `CLAUDE.md`/`AGENTS.md` from the working directory and the
> global `~/.claude/CLAUDE.md`, and stacks them on top of an agent's own instructions. Launching
> from a given directory inherits that directory's rules.

## pi — harness settings

`.pi/settings.json` carries a retry policy (no credentials — provider creds live outside the
repo). pi resolves skills from `~/.agents/skills` / `~/.claude/skills` (HOME-relative), so
skills are shared across harnesses without per-repo config.

## Dev shell — devenv + direnv + uv

```bash
direnv allow            # first time; auto-loads the shell on cd thereafter
```

`.envrc` prefers `devenv` (Nix-reproducible) and falls back to plain `direnv + uv`. The Python
env is a shared uv venv (see `devenv.nix` `enterShell`). `uv sync` runs on first entry.

## Reproduce on a fresh machine

1. Install the prerequisites globally (binaries only).
2. Clone this repo; `direnv allow` to build the dev shell.
3. Configure your provider once (`omni setup`) — that populates the *global* `~/.omnigent`;
   this repo's `.omnigent/config.yaml` then overlays the harness/model choice.
4. `omni config list` from the repo root to confirm the overlay resolves.
