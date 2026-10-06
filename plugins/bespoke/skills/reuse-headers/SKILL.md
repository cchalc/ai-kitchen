---
name: reuse-headers
description: >
  Use when adding SPDX license headers to source files, fixing a `reuse lint`
  failure, copying third-party code into the repo, or annotating files in bulk.
  Triggers on "add SPDX header", "REUSE lint failing", "add license header to this
  file", "reuse annotate", "missing copyright header", "SPDX-FileCopyrightText".
  Do NOT use for choosing which license the project uses (that's license-choice).
metadata:
  visibility: public
---

# REUSE / SPDX headers

For repos that follow the [REUSE](https://reuse.software) Practices, `reuse lint`
must pass on every commit. Repo-wide license registration lives in `REUSE.toml`;
per-file headers cover everything not blanket-covered there. (If the repo still
has the older `.reuse/dep5`, migrate with `reuse convert-dep5`, then delete it.)

## Header on every new source file

Two required lines, in a comment in the file's language:

```
SPDX-FileCopyrightText: <year> <copyright holder> <<URL>>
SPDX-License-Identifier: <SPDX-ID>
```

Place it at the very top, below the shebang if there is one. The identifier
should match the project's license — check `LICENSE` / `LICENSES/` before
guessing (see license-choice for new projects).

## Comment style by file type

Copyright holder and license below are placeholders — use the project's.

Shell / Python / YAML / Makefile / Dockerfile:

```
# SPDX-FileCopyrightText: 2026 Example Org <https://example.org>
#
# SPDX-License-Identifier: MIT
```

C / Java / TypeScript:

```
// SPDX-FileCopyrightText: 2026 Example Org <https://example.org>
//
// SPDX-License-Identifier: MIT
```

Markdown with YAML frontmatter (e.g. a Claude Code `SKILL.md`): put the SPDX lines
as YAML comments inside the frontmatter, since the frontmatter must come first:

```
---
# SPDX-FileCopyrightText: 2026 Example Org <https://example.org>
# SPDX-License-Identifier: MIT
name: ...
---
```

## Bulk annotation

```
reuse annotate --copyright 'Example Org <https://example.org>' \
               --license 'MIT' \
               --style python \
               path/to/file.py
```

`--style` matches the language (`python`, `c`, `shell`, `xml-document`, ...);
`reuse annotate --help` lists them.

## Copying third-party code

- Preserve the file's existing SPDX header — don't overwrite the original
  copyright.
- If its license differs from the project's, add the license text at
  `LICENSES/<SPDX-ID>.txt`.
- If the header inlines the entire license text, move that to `LICENSES/` and
  leave only the short `SPDX-License-Identifier` in the header.
- If you copy only a fragment, add a comment stating where it came from, the
  owner, and the license. Prefer copying whole files over inlining fragments.
- The same rules apply to docs, not just code.

## Files that can't carry a header

Binary or generated files, or formats without comments: register them in
`REUSE.toml` via an `[[annotations]]` entry with `path`,
`SPDX-FileCopyrightText`, and `SPDX-License-Identifier`. Don't invent comment
syntax. Generated files (lockfiles, build output) only appear after a
build/generate step, so a `reuse lint` that passed before they existed doesn't
cover them — annotate them when they show up.

## Verifying

Re-run `reuse lint` after any command that adds new files, not just once.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
