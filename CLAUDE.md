# ai-kitchen

Personal incubator for Databricks Field Engineering skills and tools.
Mature work graduates to the official vibe marketplace via
`/vibe-publish-plugin`. Anything in `scratch/` is WIP and not for general use.

## Repo layout
- `plugin/`   — publishable Vibe plugin (canonical layout)
- `scratch/`  — drafts; not published; rename to `plugin/skills/<name>` when ready
- `tools/`    — Python helpers; share the root uv venv
- `docs/`     — design specs (incl. `docs/superpowers/specs/`)

## Living docs (read these in order at session start)
1. `checkpoint.md` — where I left off
2. `tasks.md` — in-progress + next
3. `lessons.md` — append-only learnings (consult when stuck)
4. `architecture.md` — why things are shaped this way

At session end: overwrite `checkpoint.md` with current state.
On surprises: append a dated entry to `lessons.md`.

## Conventions
- Skills live under `plugin/skills/<kebab-name>/SKILL.md`.
- Skill `description` MUST include "when to use" + explicit negative
  triggers (vibe CI requires ≥95% routing accuracy).
- `skill-routing.yaml` evals: max 2 entries per skill (vibe CI hard limit).
- Shell snippets must be Linux-compatible. Forbidden on Linux CI:
  `sed -i ''`, `base64 -i`, `stat -f`, `date -v`, `/Applications/...`.

## VCS
- `jj` is the primary local VCS; colocated with git.
- `git` exists for GitHub interop only. Use `jj git push` to publish.
- `wt` (worktrunk) for parallel skill work. Default config; no `.config/wt.toml`.

## Python
- Single venv at `~/.virtualenvs/ai-kitchen` (shared across worktrees).
- `direnv allow` once; the shell auto-loads the env on `cd`.
- Two entry paths supported: `devenv.nix` (preferred) or plain `uv` fallback.
- `uv add <pkg>` to add deps. `uv run python tools/x.py` to run scripts.
- Footnote: if you rename the repo dir, update the hardcoded path in
  `.envrc` and `devenv.nix` (`enterShell`).

## Promotion workflow
1. Draft in `scratch/<idea>/`.
2. Validate skill: kebab-case `name`, "when to use" + negative triggers
   in `description`, Linux-safe shell.
3. `git mv scratch/<idea> plugin/skills/<idea>` (jj sees the rename).
4. `cd plugin && /vibe-publish-plugin` — auto-detects, dupe-checks,
   validates, opens PR to `databricks/vibe`.

## Safety
- Never run `/vibe-publish-plugin` from `scratch/` — it's intentionally
  outside the plugin and won't be detected.
- Don't commit credentials. `.gitignore` covers `.env*`; double-check.
