---
name: package-management
description: On this machine, tooling installs must never use Homebrew. Use the package managers already present (nix, uv, npm, pipx, direct downloads), and prefer the project's out-of-source uv virtualenv for Python. Applies to any task that installs, upgrades, or runs a CLI tool or Python dependency.
metadata:
  format: https://www.agentbehavior.dev/
  sources:
    - ~/.claude/CLAUDE.md (Package Management)
    - ~/Projects/Databricks/CLAUDE.md (uv environment activation)
---

# Package management

**Intent:** Homebrew is a strict, non-negotiable no on this machine — it is not
on PATH by design and must not be added. Every install, upgrade, or tool run
has to route through a package manager that is already present. For Python,
dependencies belong in the project's out-of-source uv virtualenv so the working
tree stays clean and the venv survives `git clean`.

**Evidence:** Before installing or running a tool, inspect what is actually
available:
- nix profile: `~/.nix-profile/bin/` (direnv, devenv, node, java, flyctl, …).
- `uv` for Python projects; `npm` for Node; `pipx` or a `curl`-based installer
  for standalone CLIs; direct downloads as a last resort.
- Whether a uv venv is active: `echo $UV_PROJECT_ENVIRONMENT` (projects set it
  to `~/.virtualenvs/<project-name>` via a per-project `.envrc` that direnv
  loads), `echo $DIRENV_DIR`, and `uv run python -c 'import sys; print(sys.executable)'`
  (the path must resolve under `~/.virtualenvs/`).

**Decision:** Choose a non-brew manager that fits the tool. For Python work,
decide to operate inside the project's uv venv rather than any system or global
interpreter. If direnv has not loaded the env, decide to run `direnv allow`
from the project root (and `uv sync` if the venv does not yet exist) before
installing anything.

**Execution:**
- Python deps: `uv add <pkg>`; run code with `uv run <cmd>` or
  `$UV_PROJECT_ENVIRONMENT/bin/<tool>`. Never activate the venv shell-style and
  never `pip install` outside the venv.
- Other tools: install via nix, npm, pipx, or a direct download.
- Keep nix-config changes minimal and never run `home-manager switch` as part
  of incidental work.

**Recovery:** When a skill, plugin, or setup script instructs a brew command,
override it: use an alternative manager already on the system, or skip the step
and report it as unavailable. Do not run `brew` as a fallback, do not source
`brew shellenv`, and do not suggest brew to the user even as an option. If no
non-brew path exists, stop and say so rather than reaching for brew.

**Failure modes:** Running any `brew` subcommand (`install`, `upgrade`, `tap`,
`cask`, …); sourcing `brew shellenv` or adding brew to PATH; recommending brew
as a fallback; `pip install` into a system/global interpreter instead of the uv
venv; activating a venv shell-style when `uv run` would do; adding incidental
packages to nix-config.
