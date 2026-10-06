---
name: changelog
description: >
  Use when adding a changelog entry, setting up CHANGES.md / CHANGELOG.md,
  documenting user-facing changes in a release, or writing a migration note for a
  breaking change. Triggers on "add to changelog", "CHANGES.md entry", "document
  this release", "release notes", "breaking change migration note", "what's new".
  Do NOT use for the project README (that's writing-readmes) or per-file license headers
  (that's reuse-headers).
metadata:
  visibility: public
---

# Changelog

## What to record

Only **user-visible** changes:

- CLI behaviour, API changes, output-format changes, new or changed config,
  dependency updates that affect users.
- A migration note for every breaking change, even within a major version.

Exclude internal-only changes (refactors with no behavioural impact).

## What each entry needs

- The version + date of the release it belongs to. Use a literal `Unreleased`
  heading for changes not yet shipped.
- One bullet per change, written from the **user's** perspective.
- A reference to the PR/issue.
- A clear marker and migration guidance for breaking changes.

## Format

Follow the changelog format already in the repo. For a new project, adopt
["Keep a Changelog"](https://keepachangelog.com):

- Categories: Added, Changed, Deprecated, Removed, Fixed, Security.
- Version headings `## [X.Y.Z] - YYYY-MM-DD`, with an `## [Unreleased]` section
  on top.

If the project's package manifest points at a specific changelog filename, keep
the file named to match it.

### Example

```markdown
## [Unreleased]

### Added
- `--json` output mode for the `export` command (#142).

### Changed
- **Breaking:** `--out` now requires a directory, not a file. Migration: pass
  the parent directory and the file is written inside it (#139).
```

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
