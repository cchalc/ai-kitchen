# ai-kitchen Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the `ai-kitchen` repo as a hybrid Vibe plugin + scratchpad with jj-colocated VCS, devenv+uv Python tooling, and living documentation — ready for first skill drafting and eventual `/vibe-publish-plugin` publishing.

**Architecture:** Plugin lives in a `plugin/` subdirectory with the canonical Vibe layout (`.claude-plugin/plugin.json`, `skills/`, `commands/`, `agents/`, `hooks/`, `resources/`). The repo root holds Python tooling (uv via devenv with direnv-only fallback), four living-doc markdown files at root, scratch and tools sibling directories, and formal design specs under `docs/superpowers/`.

**Tech Stack:** jj (colocated with git), worktrunk (`wt`), direnv, devenv (Nix), uv, Python 3.11.

**Working directory:** `/Users/christopher.chalcraft/Projects/Databricks/ai-kitchen`

---

### Task 1: Initialize jj colocated with git

**Files:**
- Create: `.jj/` (managed by jj)

- [ ] **Step 1: Run jj colocate from inside the repo**

```bash
cd /Users/christopher.chalcraft/Projects/Databricks/ai-kitchen
jj git init --colocate
```

Expected: `Done importing changes from the underlying Git repo` (or silent success).

- [ ] **Step 2: Verify jj is tracking the repo**

```bash
jj log -r 'all()' --limit 5
```
Expected: At least one commit shown (the initial commit from `git clone`). Working copy `@` should be on a child of that initial commit.

- [ ] **Step 3: Verify git still works**

```bash
git status
```
Expected: Normal git output. The design spec at `docs/superpowers/specs/2026-05-26-ai-kitchen-design.md` should appear as untracked.

---

### Task 2: Commit the existing design spec

**Files:**
- Already exists: `docs/superpowers/specs/2026-05-26-ai-kitchen-design.md`

- [ ] **Step 1: Describe the current working copy with a message**

```bash
jj describe -m "docs: add design spec for ai-kitchen setup"
```
Expected: jj shows the new description applied to `@`.

- [ ] **Step 2: Verify the design spec is part of the change**

```bash
jj diff --summary
```
Expected: One line — `A docs/superpowers/specs/2026-05-26-ai-kitchen-design.md`. The implementation plan (this file) should ALSO show as added — that's fine; it's the next addition to the same change. (If you want them split into two commits, run `jj split` and select files; otherwise keep them together as "docs: bootstrap design + plan".)

- [ ] **Step 3: Start a new working change for Task 3 onwards**

```bash
jj new -m "feat: plugin scaffold"
```
Expected: `@` advances to a new empty working change with the message prefilled.

---

### Task 3: Plugin scaffold

**Files:**
- Create: `plugin/.claude-plugin/plugin.json`
- Create: `plugin/README.md`
- Create: `plugin/skills/.gitkeep`
- Create: `plugin/commands/.gitkeep`
- Create: `plugin/agents/.gitkeep`
- Create: `plugin/hooks/.gitkeep`
- Create: `plugin/resources/.gitkeep`

- [ ] **Step 1: Create the plugin directory tree**

```bash
mkdir -p plugin/.claude-plugin plugin/skills plugin/commands plugin/agents plugin/hooks plugin/resources
touch plugin/skills/.gitkeep plugin/commands/.gitkeep plugin/agents/.gitkeep plugin/hooks/.gitkeep plugin/resources/.gitkeep
```

- [ ] **Step 2: Write `plugin/.claude-plugin/plugin.json`**

```json
{
  "name": "ai-kitchen",
  "description": "Personal Databricks Field Engineering skills and tools — incubator for work that may eventually be published to the vibe marketplace.",
  "version": "0.1.0",
  "author": {
    "name": "Christopher Chalcraft",
    "email": "chris.chalcraft@gmail.com"
  },
  "skills": "./skills/",
  "commands": "./commands/",
  "agents": "./agents/"
}
```

- [ ] **Step 3: Write `plugin/README.md`**

```markdown
# ai-kitchen (plugin)

This directory IS the Vibe plugin. Everything outside it (scratch/, tools/, docs/) is part of the repo but not part of the plugin and never gets published.

## Layout
- `.claude-plugin/plugin.json` — manifest
- `skills/<kebab-name>/SKILL.md` — skill definitions
- `commands/` — slash commands
- `agents/` — subagents
- `hooks/` — hook configs
- `resources/` — shared resources for skills

## Publishing
From this directory, run `/vibe-publish-plugin`. It auto-detects `.claude-plugin/plugin.json` and walks you through dupe-check, validation, and PR creation against `databricks/vibe`.

## Adding a skill
1. Draft in repo-root `scratch/<idea>/`.
2. When mature: `git mv scratch/<idea> plugin/skills/<idea>` from the repo root.
3. Validate description has "when to use" + negative triggers, kebab-case `name`, Linux-safe shell.
4. `cd plugin && /vibe-publish-plugin`.
```

- [ ] **Step 4: Verify plugin.json is valid JSON**

```bash
python3 -c "import json; json.load(open('plugin/.claude-plugin/plugin.json'))"
```
Expected: No output, exit code 0. (Any output means a parse error — fix it.)

- [ ] **Step 5: Verify the directory shape matches Vibe expectations**

```bash
ls -la plugin/
ls -la plugin/.claude-plugin/
```
Expected: `plugin/` contains `.claude-plugin/`, `README.md`, `skills/`, `commands/`, `agents/`, `hooks/`, `resources/`. Each subdir contains `.gitkeep`. `plugin/.claude-plugin/` contains `plugin.json`.

- [ ] **Step 6: Continue the working change (no commit yet — Task 4 also belongs in this change)**

No command needed. The working copy keeps accumulating until `jj new` is called.

---

### Task 4: Append .gitignore entries

**Files:**
- Modify: `.gitignore` (append-only)

- [ ] **Step 1: Append the new entries**

Append the following block to the END of `.gitignore`:

```
# devenv
.devenv/

# direnv
.envrc.local

# editor state
.idea/
.vscode/
```

- [ ] **Step 2: Verify the append**

```bash
tail -10 .gitignore
```
Expected: The last lines show the appended block. The original Python entries (`__pycache__/`, `build/`, etc.) are still present above.

- [ ] **Step 3: Describe the current change and start a new one for Task 5**

```bash
jj describe -m "feat: plugin scaffold + gitignore updates"
jj new -m "feat: Python tooling (devenv + uv)"
```

---

### Task 5: Python tooling (pyproject.toml, devenv, .envrc)

**Files:**
- Create: `pyproject.toml`
- Create: `devenv.nix`
- Create: `devenv.yaml`
- Create: `.envrc`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "ai-kitchen"
version = "0.1.0"
description = "Personal Databricks FE skills and tools (incubator)"
requires-python = ">=3.11"
dependencies = []

[tool.uv]
package = false
```

- [ ] **Step 2: Write `devenv.nix`**

```nix
{ pkgs, ... }: {
  languages.python.enable = true;
  languages.python.package = pkgs.python311;
  languages.python.uv.enable = true;

  enterShell = ''
    export UV_PROJECT_ENVIRONMENT="$HOME/.virtualenvs/ai-kitchen"
    if [ ! -d "$UV_PROJECT_ENVIRONMENT" ]; then
      uv sync
    fi
  '';
}
```

- [ ] **Step 3: Write `devenv.yaml`**

```yaml
inputs:
  nixpkgs:
    url: github:cachix/devenv-nixpkgs/rolling
```

- [ ] **Step 4: Write `.envrc`**

```sh
# Path 1 (preferred): devenv — Nix-reproducible shell with uv inside.
if has devenv && [ -f devenv.nix ]; then
  use devenv
  return
fi

# Path 2 (fallback): plain direnv + uv per the cchalc gist.
# Requires: direnv + uv on PATH.
export UV_PROJECT_ENVIRONMENT="$HOME/.virtualenvs/ai-kitchen"
```

- [ ] **Step 5: Verify TOML and YAML parse**

```bash
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
python3 -c "import yaml; yaml.safe_load(open('devenv.yaml'))" 2>&1 || echo "(yaml not in stdlib — skip; visual check)"
```
Expected: TOML loads silently. YAML check may fall back to visual — just confirm the file looks right.

- [ ] **Step 6: Verify `.envrc` syntax (do NOT `direnv allow` yet — we want a clean commit first)**

```bash
bash -n .envrc
```
Expected: No output, exit code 0.

- [ ] **Step 7: Describe and advance**

```bash
jj describe -m "feat: Python tooling (devenv + uv) with direnv fallback"
jj new -m "docs: living documentation"
```

---

### Task 6: Living documentation (CLAUDE.md + 4 root docs)

**Files:**
- Create: `CLAUDE.md`
- Create: `README.md`
- Create: `architecture.md`
- Create: `tasks.md`
- Create: `lessons.md`
- Create: `checkpoint.md`

- [ ] **Step 1: Write `CLAUDE.md`**

```markdown
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
```

- [ ] **Step 2: Write `README.md`**

```markdown
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

Personal / internal. Not for redistribution.
```

- [ ] **Step 3: Write `architecture.md`**

```markdown
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
```

- [ ] **Step 4: Write `tasks.md`**

```markdown
# Tasks

Rolling work list. Updated each session.

## In Progress

_(none)_

## Next

- [ ] Draft a first skill in `scratch/` to validate the promotion workflow end-to-end.
- [ ] Try `/vibe-publish-plugin` against `plugin/` as a dry-run sanity check.

## Backlog

- [ ] Decide whether `.claude/settings.local.json` is worth seeding (permissions, hooks).
- [ ] Consider adding a `Makefile` or `justfile` for repeated workflows once they stabilize.
- [ ] Add pre-commit hooks (ruff) once `tools/` has real Python in it.

## Done (recent)

- [x] Initial repo setup (Task 1–9 of `docs/superpowers/plans/2026-05-26-ai-kitchen-setup.md`).
```

- [ ] **Step 5: Write `lessons.md`**

```markdown
# Lessons

Append-only log of non-obvious things learned while working in this repo. Newest entries on top. Format:

```
### YYYY-MM-DD — short title

**What:** the surprise / learning.
**Why it matters:** how it changes future work.
**Tags:** #topic1 #topic2
```

---

### 2026-05-26 — `cchalc` SSH identity is distinct from `christopher-chalcraft_data` GitHub user

**What:** SSH key on this host authenticates to GitHub as `cchalc`, but the repo owner is `christopher-chalcraft_data`. Cloning with SSH failed with "Repository not found" because `cchalc` isn't a collaborator on the private repo.
**Why it matters:** Always check `ssh -T git@github.com` and `gh auth status` separately when cloning private repos. For this repo, use `gh repo clone` (HTTPS via gh token) or use the `christopher-chalcraft_data` account explicitly. Documented because the GitHub error message ("Repository not found") is generic for private + no-access, easy to misread as a typo.
**Tags:** #github #auth #onboarding

### 2026-05-26 — Vibe CI rejects skills without explicit negative triggers

**What:** `/vibe-publish-plugin` won't pass CI unless each skill `description` includes "NOT for X" exclusions for overlapping skills. Evals require ≥95% routing accuracy.
**Why it matters:** Write the negative triggers when drafting in `scratch/`, not as an afterthought before publishing. Saves a CI round-trip.
**Tags:** #publishing #ci #skill-design
```

- [ ] **Step 6: Write `checkpoint.md`**

```markdown
# Checkpoint

**Last session:** 2026-05-26 — initial repo setup.

**Current state:** Repo scaffolded per `docs/superpowers/plans/2026-05-26-ai-kitchen-setup.md`. devenv + uv + direnv all installed. jj colocated. No skills drafted yet.

**Next action:** Draft a first real skill in `scratch/` to validate the promotion workflow. Candidate: a small helper for [pick one when starting].

**Blockers:** None.
```

- [ ] **Step 7: Verify all files are readable and markdown-ish**

```bash
ls -la CLAUDE.md README.md architecture.md tasks.md lessons.md checkpoint.md
head -3 CLAUDE.md README.md architecture.md tasks.md lessons.md checkpoint.md
```
Expected: All six files exist; each starts with a `#` heading line.

- [ ] **Step 8: Describe and advance**

```bash
jj describe -m "docs: CLAUDE.md, README, and four living-doc files"
jj new -m "feat: scratch + tools stubs"
```

---

### Task 7: Scratch and tools stubs

**Files:**
- Create: `scratch/README.md`
- Create: `tools/README.md`

- [ ] **Step 1: Create the directories**

```bash
mkdir -p scratch tools
```

- [ ] **Step 2: Write `scratch/README.md`**

```markdown
# scratch/

WIP / drafts. **Nothing here is published.**

## Conventions

- One subdirectory per idea: `scratch/<kebab-name>/`.
- A skill draft looks like `scratch/<name>/SKILL.md` with at least a `name` and `description` in frontmatter — but you can be sloppy here. The point of `scratch/` is to think out loud.
- When the skill is mature: `git mv scratch/<name> plugin/skills/<name>` (from the repo root). jj in colocated mode tracks the rename.

## What "mature" means

Before promoting:
- [ ] Frontmatter `name` is kebab-case.
- [ ] Frontmatter `description` has "when to use" *and* explicit negative triggers (`NOT for X` exclusions).
- [ ] Shell snippets are Linux-safe (no `sed -i ''`, `base64 -i`, `stat -f`, `date -v`, `/Applications/...`).
- [ ] No more than 2 evals planned per skill in `skill-routing.yaml`.

## Don't run `/vibe-publish-plugin` from here

It walks the CWD looking for `.claude-plugin/plugin.json`. There isn't one here on purpose. Run it from `plugin/` after promoting.
```

- [ ] **Step 3: Write `tools/README.md`**

```markdown
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
```

- [ ] **Step 4: Verify**

```bash
ls scratch/ tools/
```
Expected: Each contains `README.md`.

- [ ] **Step 5: Describe and advance**

```bash
jj describe -m "docs: scratch and tools stubs with conventions"
jj new -m "chore: activate devenv + initial venv"
```

---

### Task 8: Activate the dev environment

This step actually loads devenv and creates the venv. It's a separate task because it modifies the user's direnv state.

- [ ] **Step 1: Allow direnv to load `.envrc` in this directory**

```bash
direnv allow
```
Expected: `direnv: loading .envrc` followed by devenv output ("Building shell..." etc.) and eventually a `direnv: export +UV_PROJECT_ENVIRONMENT ...` line. First run may take 30–120 seconds while Nix fetches packages.

- [ ] **Step 2: Verify Python comes from devenv (not the system python)**

```bash
which python
python --version
```
Expected: `python` resolves to a path inside `/nix/store/...` (devenv's python311). Version 3.11.x.

- [ ] **Step 3: Verify the venv was created**

```bash
ls -la ~/.virtualenvs/ai-kitchen/
```
Expected: Directory exists; contains `bin/`, `lib/`, `pyvenv.cfg`. (devenv's `enterShell` runs `uv sync` on first entry if the venv directory is missing.)

- [ ] **Step 4: Verify `uv` is available and sees the project**

```bash
uv --version
uv tree
```
Expected: `uv` prints its version. `uv tree` prints `ai-kitchen v0.1.0` with no dependencies (we haven't added any).

- [ ] **Step 5: Verify `uv.lock` was generated**

```bash
ls -la uv.lock
```
Expected: File exists. (If missing — devenv's `uv sync` should have created it. Re-run `uv sync` manually if needed.)

- [ ] **Step 6: Describe and start a new change for the push step**

```bash
jj describe -m "chore: activate devenv, generate uv.lock and devenv.lock"
jj new -m "chore: push to GitHub"
```

---

### Task 9: Push to GitHub

- [ ] **Step 1: Confirm what's about to be pushed**

```bash
jj log -r 'all()'
```
Expected: A chain of described commits from the initial git import through the changes from Tasks 2–8. Each commit has a meaningful description.

- [ ] **Step 2: Set the `main` bookmark to the latest committed change**

```bash
jj bookmark set main -r @-
```
Expected: jj confirms the bookmark moved to the latest committed change (`@-` is the parent of the current empty working copy).

- [ ] **Step 3: Push to GitHub**

```bash
jj git push --bookmark main
```
Expected: jj reports pushing `main` to `origin`. Output includes the commit IDs being pushed.

- [ ] **Step 4: Verify the push landed**

```bash
gh repo view cchalc/ai-kitchen --json defaultBranchRef -q '.defaultBranchRef.target.history.totalCount' 2>/dev/null || gh api repos/cchalc/ai-kitchen/commits --jq 'length'
```
Expected: A number ≥ 7 (initial commit + the new commits from this plan).

- [ ] **Step 5: Optional — final sanity check by browsing the repo**

```bash
gh repo view cchalc/ai-kitchen --web
```
Expected: Browser opens to the repo on GitHub. Visually confirm `plugin/`, `scratch/`, `tools/`, `docs/`, `CLAUDE.md`, `README.md` are all present.

---

## Post-plan validation checklist

After all tasks complete, verify the success criteria from the spec:

- [ ] `cd /Users/christopher.chalcraft/Projects/Databricks/ai-kitchen` triggers direnv → devenv shell.
- [ ] `which python` returns a `/nix/store/...` path (Python 3.11).
- [ ] `which uv` resolves (devenv-provided).
- [ ] `uv tree` runs without error.
- [ ] `jj log` shows the new commits with descriptive messages.
- [ ] `git log --oneline` shows the same commits (colocated).
- [ ] `ls plugin/` shows the canonical Vibe plugin layout.
- [ ] `cat plugin/.claude-plugin/plugin.json | python3 -c 'import json,sys; json.load(sys.stdin)'` succeeds.
- [ ] GitHub remote has all the new files.

---

## Notes for the implementer

- This plan is sequential. Tasks 1–9 must run in order because each task assumes the prior task's state.
- All `jj describe` / `jj new` boundaries are chosen to group logically-related file changes. If you'd rather collapse them into a single commit, run `jj squash` after Task 8.
- If devenv's first build hangs or fails (Task 8 Step 1), check `~/.cache/nix/`. The fallback path (bare direnv + uv) is the next thing to try — temporarily comment out the `use devenv` branch in `.envrc` and re-run `direnv allow`.
- If `jj git push` (Task 9 Step 3) fails with permission errors, the auth mismatch from `lessons.md` is biting — gh CLI is authenticated as `christopher-chalcraft_data` but jj uses git's SSH, which authenticates as `cchalc`. Either: (a) push via `gh` somehow, (b) add `cchalc` as a collaborator on the repo, or (c) configure SSH multi-identity. Repo is private and owned by `christopher-chalcraft_data`, so option (b) is simplest.
