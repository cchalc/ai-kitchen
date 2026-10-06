# Tasks

Rolling work list. Updated each session.

## In Progress

None. Public mirror is stable and complete.

## Next

- [ ] Companion repo runs `pull-public` to import the 12 shared skills.
- [ ] Monitor for mirror conflicts (both-sides edits); resolve via the companion repo's workflow.
- [ ] Consider adding a `Makefile` or `justfile` for repeated workflows if patterns stabilize.

## Backlog

- [ ] Decide whether `.claude/settings.local.json` is worth seeding (permissions, hooks).
- [ ] Add pre-commit hooks (ruff, isort) once `tools/` has real Python in it.
- [ ] Extend routing to cover disambiguating related skills (e.g., pull-requests vs reviewing-prs edge cases).

## Done (2026-10-05)

- [x] Scrubbed internal Databricks references from all docs and skills.
- [x] Tagged all 12 skills with `metadata.visibility: public`.
- [x] Updated route_eval.py to read plugin name from config.
- [x] Added routing evals for frontend-design and ponytail-fix.
- [x] Reframed docs (CLAUDE.md, README.md, architecture.md, plugin/README.md) for public mirror role.

## Done (2026-10-05, earlier)

- [x] Ported 10 serokell-derived developer skills; renamed to avoid built-in clashes.
- [x] Added frontend-design (vendored, Apache-2.0) and ponytail-fix.
- [x] Initial repo setup.
