---
name: setup-ci
description: >
  Use when bootstrapping CI for a repo, adding a GitHub Actions workflow, creating
  a `.gitlab-ci.yml`, choosing which checks to run, or wiring branch protection to
  required checks. Triggers on "set up CI", "add a workflow", "create
  .gitlab-ci.yml", "configure CI for this repo", "common CI checks", "require
  status checks". Do NOT use to write the tests themselves (that's code-testing).
metadata:
  visibility: public
---

# Setting up CI/CD

Long-lived branches (`main`, sometimes a separate release branch) must stay in a
good state, so CI is mandatory for any non-trivial repo. The same pipeline often
doubles as CD (deploys/releases triggered by a push to a specific branch).

## Pick the service

- GitHub repos → GitHub Actions, config in `.github/workflows/*.yml`.
- GitLab repos → GitLab CI, config in `.gitlab-ci.yml`.

Both run on hosted runners by default; self-hosted runners are an option when you
need more power or specific tooling.

## Common checks (apply everywhere)

Regardless of language or build system:

- Build all code and run the test suite (see code-testing); produce a coverage
  report.
- Lint / format check for the project's languages (e.g. `ruff`, `eslint`,
  `gofmt -l`).
- `shellcheck` on any shell scripts.
- No trailing whitespace / missing final newline (e.g. via pre-commit).
- Broken-link check for docs (e.g. `lychee` or `xrefcheck`).
- `reuse lint` if the repo follows REUSE (see reuse-headers).

Keep each check as a distinct job so a failure points at the cause.

## A minimal GitHub Actions workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make check   # build + lint + test
```

Replace `make check` with the project's real gate, and pin action versions to a
tag.

## Branch protection

After CI exists, protect the long-lived branch and require the checks:

- GitHub: enable "Require status checks to pass before merging" and select the
  workflow jobs. Set via the web UI or `gh api`.
- GitLab: enable "Pipelines must succeed" in Settings → Merge requests.

Setting these usually needs admin rights on the repo.

## Watching a run

Use `gh pr checks <number> --watch` to follow a run live. Don't pipe a one-shot
`gh pr checks` through another command (e.g. `| tail`) to judge pass/fail — the
exit code you read becomes that command's, not the checks', so a failing run can
look green.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
