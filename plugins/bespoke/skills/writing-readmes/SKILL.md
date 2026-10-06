---
name: writing-readmes
description: >
  Use when writing or fixing a README following the Standard Readme spec, picking
  the required sections, writing the one-line short description, or setting up
  per-component READMEs in a multi-package repo. Triggers on "write a README",
  "fix the README", "Standard Readme", "short description for readme", "README per
  package", "README required sections". Do NOT use for CHANGELOG entries (that's
  changelog), choosing a license (that's license-choice), or a demo-walkthrough
  README produced by a demo-building workflow.
metadata:
  visibility: public
---

# README.md

Every non-trivial repo should have a README that complies with the
[Standard Readme](https://github.com/RichardLitt/standard-readme) spec, which
distinguishes **required** sections from **optional** ones.

## Required sections (in spec order)

- **Title** — a single `# Name` heading.
- **Short description** — one line, **<120 characters**, right after the title.
  Should match the package-manager `description` field and the repo's host
  description.
- **Install** — how to install / build.
- **Usage** — how to use it; CLI examples; the most common operations.
- **Contributing** — link to `CONTRIBUTING.md` if present, or inline guidance.
  For branch naming / commit format / PR process, pull from the conventions the
  repo actually uses (see committing-work, pull-requests) — don't restate a
  workflow model from memory; repo-specific rules differ.
- **License** — SPDX identifier and a link to `LICENSE`.

## Optional sections (when applicable, between short-description and license)

Banner, Badges (start with just a license badge), Long description, Table of
contents (add it if the README exceeds ~100 raw `.md` lines), Security,
Background, API / CLI, Maintainers, Thanks.

## Multi-component repos

If the repo has multiple independent components in subdirectories, each
component's directory should also contain its own Standard-Readme-compliant
README. "Independent component" is a judgement call.

## Forks

If the repo is a fork, explain **why** the fork exists at the very top of the
README — otherwise nobody will know whether it's still needed months later.

## Pitfall: template leftovers

When customising a README from a template, strip every `[//]: # (...)`
meta-comment. Verify with:

```
git grep '\[//\]:'
```

That should return nothing in a finished README.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
