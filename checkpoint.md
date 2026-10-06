# Checkpoint

**Last session:** 2026-10-06. Split the shared skills into tier plugins and made
the repo an installable marketplace.

**Current state:**
- **Two tier plugins**, listed in `.claude-plugin/marketplace.json` (marketplace `ai-kitchen`):
  - `plugins/core/`: committing-work, pull-requests, reviewing-prs, code-testing,
    ponytail-fix. Installed here at **user scope** (`core@ai-kitchen`), so it's on everywhere.
  - `plugins/bespoke/`: changelog, writing-readmes, setup-ci, license-choice,
    reuse-headers, gitignore, frontend-design. Not enabled anywhere; enable per project.
- Paths match the private companion repo exactly, and its two-way mirror keeps
  them in sync. Every skill is tagged `metadata.visibility: public`.
- `tools/route_eval.py` loads every marketplace plugin and expects `<plugin>:<skill>`.
  Single runs are noisy: re-run failures before trusting a drop.

**Next action:** Nothing here. The companion repo still has to merge its stacked
PRs, then install its `ops` tier in the SSA dirs and publish to vibe.

**Open issues:** `ponytail-fix` never routes in evals (the model runs the linter
directly). "Get it ready for review" flips between pull-requests and committing-work.

**Blockers:** None.
