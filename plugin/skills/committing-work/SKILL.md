---
name: committing-work
description: >
  Use when naming a branch for an issue, writing a commit message, or staging
  and committing changes — the user/issue-id branch-name scheme, Problem/Solution
  commit bodies, signed commits, and fixup→autosquash during review. Load it
  before looking the issue up: the naming scheme comes from here. Triggers on
  "what should I name the branch for issue #N", "what should the branch be
  called", "create a branch for this issue", "draft a commit message", "commit
  these changes", "make a fixup commit", "git commit". Do NOT use to
  open, fill, or merge a pull request (that's pull-requests) or to review someone
  else's code (that's reviewing-prs).
metadata:
  visibility: public
---

# Committing work

Use whenever you are about to create a branch for new work, stage changes, or
write a commit message.

## Branch naming

Mark yourself as working on the issue first — assign yourself (or move it to
"In Progress" if the tracker uses that). It's the easiest step to forget once
you're into the work.

Issue branches: `<username>/<issue-id>-<brief-description>`

- `<username>` — your git host username.
- `<issue-id>` — GitHub issues: `#` + number (e.g. `#228`). Other trackers: the
  tracker's key (e.g. `proj-322`). More than one issue or person: concatenate
  IDs with dashes.
- `<brief-description>` — lowercase and dashes; brief but clear enough that the
  topic is obvious without looking the issue up.

Example: `alice/#228-add-yellow-button`.

Branch off the target branch (usually `main` or `master`). Check the repo's docs
for its branching model before assuming — some repos keep a separate
release/production branch that only release work touches.

> **jj:** start the change with `jj new <target>`; name a bookmark with
> `jj bookmark create <name> -r @`.

## Commit message format

Subject line:

- Prefix with issue IDs in square brackets: `[#453]`. Omit if the repo is public
  and the issue lives in a private tracker.
- Start with an uppercase letter, imperative mood ("Switch from X to Y", not
  "Switched"), ≤50 chars (hard limit 72), no trailing period.

Body (mandatory):

- One blank line after the subject.
- `Problem:` paragraph — what is wrong / what needs to change.
- `Solution:` paragraph — how this commit addresses it.
- Any extra context after that. Wrap at 72 chars (hard limit 80).

Sign commits (`git commit -S`, or enable signing by default). If signing isn't
configured locally, ask the user to configure it — don't commit unsigned.

> **jj:** set the message with `jj describe -m "..."` (or `jj commit -m` to also
> start a fresh change). Signing is configured in jj's own config.

### Example

```
[#453] Switch from avada-kedavra to expelliarmus

Problem: the `avada-kedavra` library we use to kill unwanted process
instances tears programmers' souls apart, and there is currently no
mitigation.

Solution: use the simpler `expelliarmus` library, which blocks process
instances from performing any effects, and garbage-collect blocked
processes with the `kill` syscall.
```

## Commit hygiene

- Each commit is a minimal, accurate answer to exactly one identified problem.
- A commit should not fix a problem introduced by an earlier commit in the same
  PR — clean that up before merging.
- Ordinary pushes use plain `git push`. Force-push only after rewriting history,
  with `--force-with-lease`, never `-f`.
- After `git mv`, editing the moved file's contents does not re-stage it —
  `git add` the path again, or the commit captures only the bare rename.

> **jj:** history rewriting is first-class — `jj squash`, `jj split`, `jj rebase`
> edit any commit with no force-push dance; `jj git push` syncs. There is no
> staging step: the working copy is itself a commit.

## During PR review

The clean-history rules above apply to commits that will be merged. During a
PR's review phase, write fixes as **separate** commits (don't amend), pushed
as-is. Before merging, squash them into their targets:

```
git commit --fixup=<sha-being-fixed>
git rebase -i --autosquash <target>
```

> **jj:** fold a fix into an earlier change directly with
> `jj squash --into <change>` — no fixup markers needed.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
