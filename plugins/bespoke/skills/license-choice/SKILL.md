---
name: license-choice
description: >
  Use when picking a license for a project, adding a LICENSE file, setting up a
  proprietary repository, or handling copyright on customer / derived work.
  Triggers on "pick a license", "what license should we use", "add LICENSE file",
  "set up a proprietary repo", "MIT or Apache", "MPL or GPL", "who owns the
  copyright". Do NOT use for per-file SPDX headers in each source file (that's
  reuse-headers).
metadata:
  visibility: public
---

# Choosing a license

Pick deliberately — the license governs how others may use the code and is hard
to change once contributors have submitted work under it. If the project is paid
for by a client, the client usually has the final say and often owns the
copyright.

## Common open-source choices

- **MIT / BSD-2/3-Clause** — maximally permissive; use for the widest adoption
  when you don't need patent or copyleft terms.
- **Apache-2.0** — permissive like MIT but adds an explicit patent grant and
  contribution terms. Prefer it where patent clarity matters.
- **MPL-2.0** — weak (file-level) copyleft: changes to MPL files stay open, but
  the code can be combined with proprietary code. A good default for a library
  you want kept open without blocking commercial use.
- **GPL-3.0-or-later** — strong copyleft; derivative works must also be GPL.
  Discourages embedding in closed products.
- **AGPL-3.0-or-later** — like GPL but also triggers on network/service use; the
  main defence when the value is in running the software as a service.

Match whatever the surrounding ecosystem expects (e.g. the dominant license in
your language community) unless there's a reason to diverge.

## Proprietary (closed-source) projects

When the source isn't meant to be freely used by anyone:

1. Create `LICENSES/LicenseRef-Proprietary.txt`:

   ```
   © <year> <holder>, all rights reserved.
   ```

2. Use `LicenseRef-Proprietary` as the `SPDX-License-Identifier` in per-file
   headers (see reuse-headers).

## Files in the repo

Whichever license you pick:

- Put the primary license as `LICENSE` at the repo root — GitHub and GitLab
  treat this file specially.
- If the project follows REUSE, also add the text at `LICENSES/<SPDX-ID>.txt`
  (download via `reuse download <SPDX-ID>`) and add per-file SPDX headers (see
  reuse-headers).

## Copyright holder

- Customer-funded work: copyright belongs to the customer unless the contract
  says otherwise; use their name in `SPDX-FileCopyrightText`, and have an
  authorised representative confirm the license (e.g. by approving the PR that
  adds it).
- Internal project: copyright belongs to your organisation (or to you).

## Derived work from third-party code

- Cleanly separable generic helpers: split into their own repo under the new
  owner so they aren't encumbered by the third party's license.
- Code closely tied to the original: copyright stays with the original owner —
  negotiate terms with them.
- If asked to use third-party code under terms that don't allow it, refuse and
  say so clearly.

## See also

- reuse-headers — per-file SPDX header conventions.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
