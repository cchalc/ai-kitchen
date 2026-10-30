---
name: project-startup
description: >
  Use when starting a new project repo, or bootstrapping an empty or near-empty one,
  end to end: wire the dev-standards plugins, the agent config (CLAUDE.md, living docs),
  and an out-of-source uv venv FIRST, then scaffold from a template (or a minimal uv
  layout) and add CI and a README. Triggers on "set up this new repo", "bootstrap a
  project", "start a new project", "project startup", "scaffold this repo with our dev
  standards", "new repo from the template". Do NOT use for one piece on its own in an
  established repo: CI only (that's setup-ci), README only (writing-readmes), ignore
  rules only (gitignore), or committing (committing-work).
metadata:
  visibility: public
---

# Project startup

Turns an empty or near-empty repo into a working project, in a fixed order. **Standards come
before the template**, so the template lands in a repo that already has its agent config and
conventions, and the scaffold is merged in rather than overwriting them. Each phase is its own
commit, so the history shows standards → scaffold → CI/docs.

Files to copy or fill in are in `references/`. `scripts/merge_scaffold.py` does the merge.
`references/profiles.md` defines the two profile kinds.

## 0. Gather (ask, don't guess)

- **Repo path** and **project name**: kebab-case. The package is underscored and the
  distribution hyphenated.
- **Standards profile**: built-in `public`, or a `standards-*.yaml` from
  `${PROJECT_STARTUP_PROFILES:-~/.agents/project-startup}/`. List the dir and offer what's
  there.
- **Template profile**: built-in `none` (minimal uv layout), or a `template-*.yaml` from
  the same dir.
- **Shape**, if the template offers several (e.g. app / jobs / both / neither). Every later
  step depends on it.
- **Is the repo public?** Check with `gh repo view <owner>/<repo> --json visibility`, using
  the gh account that owns it (`GH_TOKEN=$(gh auth token --user <owner>)` when several are
  logged in). A 404 from the wrong account is not "public". If it is public and the
  standards profile has `visibility: org`, warn: outside cloners can't install an org-only
  marketplace. Offer the `public` profile. If a template is internal, say that scaffolding
  it into a public repo publishes it, and get an explicit yes.

## 1. Preflight

- Clean working tree, on the default branch and up to date.
- `git`, `gh`, `uv`, `direnv` and `make` are present. Install missing tools with the
  machine's existing package manager. Never use Homebrew, and never `pip install` outside a
  venv.
- Commit signing is configured (committing-work). If not, ask the user to set it up. Don't
  commit unsigned.
- Create the branch per committing-work: `<username>/<issue-id>-project-setup`, or
  `<username>/project-setup` with no issue.

## 2. Dev standards — commit 1

Write these, filling `{{…}}` from the profiles:

| File | From |
|---|---|
| `.claude/settings.json` | `extraKnownMarketplaces.<marketplace.name>` = `{"source": {"source": "github", "repo": <marketplace.repo>}}`; `enabledPlugins` = each of `plugins` → `true` |
| `CLAUDE.md` | `references/CLAUDE.md.tmpl` (skill table from the profile's `skills` map) |
| `checkpoint.md`, `tasks.md`, `lessons.md` | `references/living-docs.md` |
| `.envrc` | `references/envrc`: one venv per checkout at `~/.virtualenvs/<dir name>` |
| `.gitignore` | append `references/gitignore-additions`. If an existing rule ignores `.envrc` itself, remove it, because the `.envrc` is committed |
| `.github/pull_request_template.md` | `references/github/pull_request_template.md` |
| `CHANGELOG.md` | changelog skill: Keep a Changelog with an `## [Unreleased]` section |

If a `CLAUDE.md` already exists, merge into it rather than replacing it. Per the gitignore
skill, files from tools only *you* use (editor dirs, personal agent state) go in
`.git/info/exclude` or your global ignore, not the project `.gitignore`.

Commit (committing-work): e.g. `Add dev standards and agent config`, with a Problem/Solution
body.

## 3. Scaffold — commit 2

**Template with a `command`:**
1. `dest=$(mktemp -d)`, then run `command` with `{name}`/`{dest}` substituted and `env` set.
   It must write only under `dest`.
2. Apply the chosen shape's `delete` list **inside the temp copy**, before merging, so
   pruning can never touch a file the repo already had.
3. Dry run, then apply:
   ```bash
   python <skill>/scripts/merge_scaffold.py "$dest/<name>" <repo>
   python <skill>/scripts/merge_scaffold.py "$dest/<name>" <repo> --apply
   ```
   Standards-owned paths (`CLAUDE.md`, `.claude/`, `.envrc`, living docs, `CHANGELOG.md`, the
   PR template) are KEEP and never written. `.gitignore` rules are appended, and a bare
   `# Title` README is replaced. Any other CONFLICT means nothing is written. Resolve it in
   the temp copy or by hand, then re-run.
4. Review any `.gitignore` APPEND block, and drop rules that are redundant with the existing
   ones, personal (OS or editor files go to the global ignore), or for pruned paths.
5. If the template brought its own `CLAUDE.md` (often just "see AGENTS.md"), it was skipped.
   Point the repo's CLAUDE.md at `AGENTS.md` instead.
6. Apply the shape's `notes` (edits to the Makefile, pyproject, workflows, and so on). If you
   removed a dependency extra, re-lock (`uv lock`).
7. Check that no placeholders are left (e.g. `grep -rn 'project_name\|project-name' .`), and
   list any remaining `SETUP` markers for the user rather than inventing values (no hosts,
   service principals, or IDs).

**Template `none`:** write `references/minimal-layout.md` straight into the repo.

Commit: e.g. `Scaffold project from <template> template`.

## 4. Environment

`direnv allow`, then the profile's `gate.install` (e.g. `make install`). If the pinned
Python is missing, run `uv python install <version>`. Verify:

```bash
uv run python -c 'import sys; print(sys.executable)'   # must be under ~/.virtualenvs/<dir name>/
```

**The lockfile must be installable by CI and by anyone who clones the repo.** uv records whatever
index it resolved from, and a developer's user-level uv config (a private PyPI mirror, for
example) leaks into `uv.lock`:

```bash
grep -o 'https://[^/"]*' uv.lock | sort | uniq -c   # expect only pypi.org + files.pythonhosted.org
```

If anything else shows up, add the `lock` and `check-lock` targets from
`references/lockfile.md`. Leave the index to each developer's own uv config: don't pin one in
`pyproject.toml`, and don't export `UV_DEFAULT_INDEX`. Behind a proxy, set `UV_FROZEN=1` in
`.envrc.local`, then run `make lock`. Verify the way CI will see it:
`make check-lock && UV_NO_CONFIG=1 uv lock --check --offline`.

## 5. CI, README and license — commit 3 (license as its own commit)

- **CI** (setup-ci): `references/github/check.yml`, with the targets switched to the
  profile's `gate`, and action versions matched to the ones the template's workflows already
  pin. Keep any dependabot/freshness workflows the template shipped. If the
  template points at a CI component the repo can't reach (e.g. internal and the repo is
  public), use this workflow instead and say so. `check.yml` has separate lint, test (with
  coverage), whitespace and offline link-check jobs, per setup-ci.
- **README** (writing-readmes): a Standard Readme with title, a description under 120
  characters, Install (`direnv allow && make install`), Usage, Contributing (→ CLAUDE.md and
  the standards skills) and License. Remove the template's own "how to start a project from
  this template" sections from README/AGENTS.md, as such templates ask. Run
  `git grep '\[//\]:'` and expect nothing back.
- Set the repo host's description to the README one-liner
  (`gh repo edit --description "…"`), as writing-readmes asks.
- **License** (license-choice). Every public repo needs one, so ask which license. If a
  template was scaffolded, read *its* license first. Template-derived files keep the
  template's license, which you can't relicense. A typical layout:
  - your license (e.g. MIT) as `LICENSE`
  - the template's text in `LICENSES/LicenseRef-<Name>.txt`
  - a `NOTICE` that lists the derived files
  - an SPDX header plus a "modified" note in each derived file that can take comments
- Add an `Added` entry to the `CHANGELOG.md` `Unreleased` section.

## 6. Gate and hand-off

- Make the standards plugins active here: `claude plugin install <plugin> --scope project`
  for each one in the profile that `claude plugin list` doesn't show as enabled. (The install
  may reorder keys in `.claude/settings.json`; revert that no-op diff.)
- Run `gate.lint` and `gate.test` until green. Use ponytail-fix for red: fix root causes,
  and don't suppress.
- Update `checkpoint.md` and `tasks.md`, then amend or fix up into the right commit.
- **Stop.** Report what was created, the remaining `SETUP` items, and anything you skipped.
  Push and open the PR only when the user says so, following pull-requests.

## Failure modes this prevents

- Scaffolding first and bolting standards on after, which loses the template's or your own
  config to overwrites.
- An in-tree `.venv`, or a shared venv across worktrees.
- A public repo pointing at an org-only marketplace or CI component.
- A `uv.lock` that pins a private mirror, so CI can't install.
- A public repo with no license, or template code silently relicensed.
- Template placeholders or "how to use this template" text left in the finished repo.
- One giant unsigned commit.
