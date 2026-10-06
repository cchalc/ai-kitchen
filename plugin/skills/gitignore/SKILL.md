---
name: gitignore
description: >
  Use when adding patterns to `.gitignore`, fixing imprecise ignore patterns, or
  deciding between project / global / local-only ignores. Triggers on "add to
  gitignore", "ignore these files", "fix gitignore", "what goes in gitignore",
  "global git ignore", "ignore build output", "editor files in gitignore". Do NOT
  use for per-file SPDX/license headers (that's reuse-headers) or CI config
  (that's setup-ci).
metadata:
  visibility: public
---

# .gitignore

## What goes in a project `.gitignore`

- Output of the **standard build tools** for the languages in the project (e.g.
  `__pycache__/`, `/dist/`, `/build/`, `node_modules/`).
- Anything else **every developer** on the project would produce and shouldn't
  commit.

If you'd only ignore something because of your editor, your OS, or a tool not
everyone uses — it does **not** belong here (see "Global ignore" below).

## Pattern precision

Make patterns as precise as possible.

- `/build/` — leading `/` anchors to the repo root; trailing `/` matches only
  directories (and their contents).
- `build` — matches `build` anywhere in the tree, as file or directory. Usually
  too broad.

Example for a Python project at the repo root:

```
# Packaging / build
/dist/
/build/
*.egg-info/

# Caches
__pycache__/
.pytest_cache/
.ruff_cache/

# In-tree virtualenv
/.venv/
```

For a Node project you'd instead ignore `node_modules/`, `/dist/`, `/coverage/`.

## Multi-component repos

If the repo has independent components in subdirectories (especially different
tech stacks), put each component's language-specific ignores in a `.gitignore`
**inside that component**, not the root.

## Global ignore (not in the repo)

Editor files, OS files, and personal-tool files go in your **global** ignore,
not the project `.gitignore`. Standard location: `~/.config/git/ignore` (or
`$XDG_CONFIG_HOME/git/ignore`). Create it if missing. Typical content:

```
# Tools
/tags

# macOS
.DS_Store

# Editors
.idea/
*.swp
```

## Local-only ignores

For project-and-user-specific scratch files you want ignored without committing
the rule or affecting other projects: use `.git/info/exclude` inside the repo.
It isn't synced.

> **jj** honours `.gitignore` (and the global and local-exclude files) directly —
> no separate `.jjignore` is needed.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
