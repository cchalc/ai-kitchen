# Checkpoint

**Last session:** 2026-10-05 — converted 12 developer skills to a public mirror
and scrubbed internal references. All skills tagged `metadata.visibility: public`.

**Current state:** 
- **12 shared skills in `plugin/skills/`:** `committing-work`, `reviewing-prs`,
  `pull-requests`, `changelog`, `writing-readmes`, `gitignore`, `license-choice`,
  `reuse-headers`, `code-testing`, `setup-ci`, `frontend-design`, `ponytail-fix`.
- **All metadata updated:** `metadata.visibility: public` in all SKILL.md files;
  `plugin.json` rewritten to describe public-facing skills; internal references
  removed.
- **route_eval.py generalized:** docstring updated, plugin name read from
  `plugin.json` instead of hardcoded.
- **Routing complete:** 16/16 evals (all 12 skills × 2 evals each) in
  `skill-routing.yaml`; validated with `tools/route_eval.py`.
- **Docs reframed:** CLAUDE.md, architecture.md, README.md, plugin/README.md
  now describe this as a public mirror; removed vibe-publish-plugin workflow.

**Next action:** Companion repo imports these via `pull-public`; vibe publishing
happens there if needed. This repo is now stable as the public source of truth.

**Blockers:** None.
