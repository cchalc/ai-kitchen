# ai-kitchen (plugin)

This directory IS the Vibe plugin. Everything outside it (scratch/, tools/, docs/) is part of the repo but not part of the plugin and never gets published.

## Layout
- `.claude-plugin/plugin.json` — manifest
- `skills/<kebab-name>/SKILL.md` — skill definitions
- `commands/` — slash commands
- `agents/` — subagents
- `hooks/` — hook configs
- `resources/` — shared resources for skills

## Publishing
From this directory, run `/vibe-publish-plugin`. It auto-detects `.claude-plugin/plugin.json` and walks you through dupe-check, validation, and PR creation against `databricks/vibe`.

## Adding a skill
1. Draft in repo-root `scratch/<idea>/`.
2. When mature: `git mv scratch/<idea> plugin/skills/<idea>` from the repo root.
3. Validate description has "when to use" + negative triggers, kebab-case `name`, Linux-safe shell.
4. `cd plugin && /vibe-publish-plugin`.
