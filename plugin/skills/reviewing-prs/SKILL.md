---
name: reviewing-prs
description: >
  Use when acting as a reviewer on someone's pull request — choosing the verdict
  (approve vs request changes vs comment), leaving review comments on the PR,
  checking its commit history, and resolving conversations. Triggers on "should
  I approve or request changes", "approve this PR", "review this PR and leave
  comments", "review someone's PR", "resolve this conversation", "comment on
  their PR". Do NOT use for an automated bug scan of the local diff with no PR
  (that's the built-in code-review), to write your own commits (that's
  committing-work), or to open and fill out your own PR (that's pull-requests).
metadata:
  visibility: public
---

# Reviewing pull requests

Review has two goals: spreading knowledge (so the bus factor stays high) and
catching bugs before merge.

## When to review

- Start with PRs where your review was explicitly requested. On GitHub:
  `https://github.com/pulls/review-requested`.
- Within those, review **older PRs first** — they accumulate review debt. Don't
  cherry-pick by topic interest.
- It's the author's job to get their own changes merged; ping reviewers if they
  go silent. If your team expects reviewers to also pick up a couple of other
  open PRs to spread load, follow that convention.

## How to review

- **Ask questions liberally.** If a piece of code isn't obvious, ask — it's the
  author's job to explain, and yours to learn from it and keep quality high.
- Check the commit **history**, not just the diff. Each commit should satisfy
  the commit policy (one problem, Problem/Solution body, signed, no within-PR
  fixups left by merge time) — see committing-work.
- If the code is fine but the history is messy, **request changes** (not
  approve) and say so explicitly — otherwise the author may merge messy history.
- If a review was requested of you and shouldn't have been, remove yourself and
  request a more appropriate reviewer. If it wasn't requested but you want to
  review before merge, request a review from yourself.

## Verdict choice

Three verdicts: **approve**, **request changes**, **comment**.

- **approve** — confident it's mergeable as-is (or trusting the author to fix
  tiny nits after).
- **request changes** — you want changes before merge.
- **comment** — you genuinely have neither; e.g. raising a question you can't yet
  judge.

**GitHub quirk:** the API rejects a `REQUEST_CHANGES` review on your own PR. For
self-review, use `COMMENT` instead — all inline comments and the summary are
preserved.

**Agent quirk:** if you (a coding agent) authored the PR, delegate self-review to
a separate agent instance with no context from the authoring session — not inline
by the session that wrote the changes. A session that already knows why every
choice was made tends to rubber-stamp its own work; a fresh agent reviewing only
the diff and the relevant skills has no such bias and catches more.

## Comment hygiene

- When the issue **your** comment raised is addressed, you (the reviewer) resolve
  the conversation — not the author.
- You may resolve another reviewer's conversation only if you are 100% confident
  it's resolved.
- Each time you revisit the PR, resolve stale comments of yours that no longer
  apply.

## Last-reviewer shortcut

If you're the last requested reviewer, all remaining comments are minor and
indisputable, and they're quick to address: it's acceptable to make the fixes
yourself, push, and approve in one step.

## Merging

After all reviewers approve and CI is green, the PR is mergeable. Generally let
the author merge (they may want to polish history first). See pull-requests for
merge mode.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
