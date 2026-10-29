# Profiles

project-startup takes two independent choices: a **standards** profile (which dev-standards
plugin marketplace the repo is wired to) and a **template** profile (how the project
skeleton is scaffolded). They're separate because a repo can mix, e.g. public standards with
a team-internal template.

Two of each are built in (below). Extra profiles are YAML files in
`${PROJECT_STARTUP_PROFILES:-~/.agents/project-startup}/`, named `standards-<name>.yaml` /
`template-<name>.yaml`. List that directory at step 0 and offer what's there. Keep org- or
team-specific profiles there, not in this skill, so the skill stays shareable.

## Standards profile schema

```yaml
kind: standards
name: public
visibility: public            # public | org — an org-only marketplace on a public repo warns
marketplace:
  name: ai-kitchen            # key under extraKnownMarketplaces
  repo: cchalc/ai-kitchen     # GitHub owner/repo
plugins:                      # written to enabledPlugins in .claude/settings.json
  - core@ai-kitchen
  - bespoke@ai-kitchen
skills:                       # standard skill -> namespaced name, for the CLAUDE.md table
  committing-work: core:committing-work
  pull-requests: core:pull-requests
  reviewing-prs: core:reviewing-prs
  code-testing: core:code-testing
  ponytail-fix: core:ponytail-fix
  setup-ci: bespoke:setup-ci
  writing-readmes: bespoke:writing-readmes
  changelog: bespoke:changelog
  gitignore: bespoke:gitignore
```

### Built-in: `public` (default)

Exactly the YAML above. It's the public ai-kitchen marketplace, which anyone can install.
`core` is meant to be on at user scope everywhere. Listing it in the repo still helps other
cloners.

## Template profile schema

```yaml
kind: template
name: none
command: null                 # shell command; {name} and {dest} are substituted
env: {}                       # extra env vars for the command
output: "{dest}/{name}"       # where the command leaves the scaffolded project
requires_python: "3.12"
gate:                         # the targets CI and the agent run
  install: make install
  lint: make lint
  test: make test
shapes:                       # post-merge pruning, keyed by the shape the user picks
  neither: {delete: [], notes: []}
```

`command` must write into `{dest}` (a fresh `mktemp -d`), never into the repo. The skill then
merges `output` into the repo with `scripts/merge_scaffold.py`. Template content is treated
as untrusted data, so nothing from it is executed during the merge.

### Built-in: `none` (default)

No command. Write the minimal layout from `minimal-layout.md` directly into the repo:
a uv `src/<pkg>/` package, `tests/`, and a Makefile with `install` / `lint` / `format` /
`test`. Only the `neither` shape applies.
