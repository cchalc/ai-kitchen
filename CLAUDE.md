# ai-kitchen

Public mirror of shared open-source Claude Code skills. The canonical development
happens in a private companion repo; files here are written by its mirror tool
keyed on the frontmatter tag `metadata.visibility: public`. Skills tagged with
this visibility are shared across both repos.

## Repo layout
- `plugin/`   — Claude Code plugin (manifest + skills + commands + agents + hooks)
- `.agents/`  — shared agent config mirrored from the companion repo
- `scratch/`  — drafts; not mirrored back; rename to `plugin/skills/<name>` when ready
- `tools/`    — Python helpers; share the root uv venv
- `docs/`     — design specs (incl. `docs/superpowers/specs/`)

## Mirror workflow

Files here can be edited directly, and changes are pulled back into the companion
repo by its `pull-public` tool. If both sides have been edited on the same file,
the mirror tool refuses and asks for manual merge.

Skills tagged `metadata.visibility: public` in their frontmatter are the ones
that sync. Check existing skills for the pattern before adding a new one.

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
  triggers (Claude Code routing requires ≥95% accuracy).
- `skill-routing.yaml` evals: max 2 entries per skill (routing CI hard limit).
- Shell snippets must be Linux-compatible. Forbidden on Linux CI:
  `sed -i ''`, `base64 -i`, `stat -f`, `date -v`, `/Applications/...`.
- All skills MUST have `metadata.visibility: public` in frontmatter to be mirrored.

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

## Safety
- Don't commit credentials. `.gitignore` covers `.env*`; double-check.
- All public skills must pass validation: `claude plugin validate plugin/`.
