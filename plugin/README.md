# ai-kitchen (plugin)

This directory is the Claude Code plugin. Everything outside it (scratch/, tools/, docs/) is part of the repo but not part of the plugin and never gets mirrored.

## Layout
- `.claude-plugin/plugin.json` — manifest
- `skills/<kebab-name>/SKILL.md` — skill definitions (all tagged `metadata.visibility: public`)
- `commands/` — slash commands
- `agents/` — subagents
- `hooks/` — hook configs
- `resources/` — shared resources for skills

## Mirror sync
All 12 skills have `metadata.visibility: public` in their frontmatter. A companion
development repo mirrors these into its private workspace; changes made there are
pulled here via `pull-public`. Edits in this public repo are allowed and flow back
via the same mechanism.

Validate the plugin with `claude plugin validate plugin/` from the repo root.

## Conventions for new skills
1. Draft in repo-root `scratch/<idea>/`.
2. When mature: `git mv scratch/<idea> plugin/skills/<idea>` from the repo root.
3. Add `metadata.visibility: public` to the frontmatter (REQUIRED for mirroring).
4. Validate: `name` is kebab-case, `description` has "when to use" + negative triggers, shell is Linux-safe.
5. Add 2 routing evals to `skill-routing.yaml` (max 2 per skill).
6. Test with `uv run python tools/route_eval.py skill-routing.yaml`.
7. Open a PR with the new skill.
