---
name: pull-requests
description: >
  Use when opening a PR or MR, drafting a PR description, filling the PR template,
  requesting reviewers, or merging a PR. Triggers on "open a PR", "create a pull
  request", "make an MR", "write PR description", "fill the PR template", "request
  review", "merge this PR", "tick the checkboxes". Do NOT use to write commit
  messages (that's committing-work) or to review someone else's PR (that's
  reviewing-prs).
metadata:
  visibility: public
---

# Pull requests and merge requests

Use when opening, updating, or merging a PR (GitHub) or MR (GitLab).

## Title

Scheme: `[ISSUE-ID] Brief description`. Omit `[ISSUE-ID]` if the repo is public
and the issue lives in a private tracker. The brief description should be
understandable on its own.

## Description

Never leave it empty.

- If the repo provides a template (`.github/pull_request_template.md` or
  `.gitlab/merge_request_templates/`), fill every section.
- Describe what changed **and why**.
- Link related issues: `Fixes #N` / `Resolves #N` auto-close them on merge
  (GitHub/GitLab). For an external tracker, paste the full issue URL prefixed
  with `Resolves`.

## Checkboxes (if the template has them)

- Tick every checkbox you can substantiate.
- **If a checkbox is irrelevant to this PR, still tick it** — that signals you
  considered the item and judged it irrelevant. The only acceptable unticked box
  is one you justify (e.g. in a comment).

What common conditional sections mean and what backs ticking them:

- **Tests** — fires when the PR adds functionality or fixes a bug. New
  functionality: add covering tests. Bugfix: add a regression test that would
  have caught it (see code-testing).
- **Documentation** — fires when behaviour visible to users or other code
  changes. Update the README and in-code docs.
- **Public contracts** — fires on public API/protocol changes. Follow the
  project's semver/deprecation policy, add a changelog entry (see changelog), and
  a migration note for breaking changes.
- **Release** — fires on release PRs. Bump the version, tag `vX.Y.Z`, publish to
  the registry.
- **Style (mandatory)** — never irrelevant. Confirm commit-policy and code-style
  compliance.
- **Agent (conditional)** — fires whenever a coding agent opened the PR. Confirm
  you followed the project's skills and instruction files.

## Scope

- One PR per issue; don't bundle unrelated work. Exception: trivial in-place
  fixes (typo, formatting) in a file you're already editing.
- Aim for ≤~500 additions+deletions. If larger, first consider whether the issue
  can be split.

## Reviewers

- Request the project's expected number of reviewers (often 2). If unsure, check
  `CODEOWNERS` and recent merged PRs, or ask. Prefer people who touched this code
  or are likely interested.
- Codeowners may be auto-requested; check the final reviewer list after opening.

## During review

- Make requested changes in **separate** commits — don't amend during review. Use
  `git commit --fixup=<sha>` (see committing-work).
- Don't force-push during review, except to rebase onto a newer target branch
  (`--force-with-lease`, never `-f`).
- Sync with the target branch by **rebasing** onto it, not merging it in.
- Don't mark a reviewer's comment resolved — that's their call.
- If reviewers are silent ~3 working days, ping them explicitly.

> **jj:** rebase onto the updated target with `jj rebase -d <target>`; push with
> `jj git push`. No force-push flags needed.

## Merging

- Default to a **merge commit**. Don't "Squash and merge" unless the PR has
  exactly one commit. Don't "Rebase and merge" by default.
- Before merging, ensure the history satisfies the commit policy
  (committing-work). The author usually cleans history first.
- Merging **someone else's** PR: confirm they're fine with it and don't want to
  polish history first (you can skip asking only for trivial one-liners).
- After merging, close the linked issue if `Fixes #N` didn't auto-close it.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
