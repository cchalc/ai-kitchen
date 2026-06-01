# scratch/

WIP / drafts. **Nothing here is published.**

## Conventions

- One subdirectory per idea: `scratch/<kebab-name>/`.
- A skill draft looks like `scratch/<name>/SKILL.md` with at least a `name` and `description` in frontmatter — but you can be sloppy here. The point of `scratch/` is to think out loud.
- When the skill is mature: `git mv scratch/<name> plugin/skills/<name>` (from the repo root). jj in colocated mode tracks the rename.

## What "mature" means

Before promoting:
- [ ] Frontmatter `name` is kebab-case.
- [ ] Frontmatter `description` has "when to use" *and* explicit negative triggers (`NOT for X` exclusions).
- [ ] Shell snippets are Linux-safe (no `sed -i ''`, `base64 -i`, `stat -f`, `date -v`, `/Applications/...`).
- [ ] No more than 2 evals planned per skill in `skill-routing.yaml`.

## Don't run `/vibe-publish-plugin` from here

It walks the CWD looking for `.claude-plugin/plugin.json`. There isn't one here on purpose. Run it from `plugin/` after promoting.
