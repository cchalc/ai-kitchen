# plugins/

Each directory here is one Claude Code plugin. Skills are grouped by how often
you need them, and the root `.claude-plugin/marketplace.json` lists the plugins.

| Plugin | Tier | Suggested scope |
|---|---|---|
| `core/` | Developer-workflow skills used all the time: committing-work, pull-requests, reviewing-prs, code-testing, ponytail-fix | user (everywhere) |
| `bespoke/` | Occasional, specialised: changelog, writing-readmes, setup-ci, license-choice, reuse-headers, gitignore, frontend-design | project, where needed |

Install:

```
claude plugin marketplace add cchalc/ai-kitchen
claude plugin install core@ai-kitchen --scope user
claude plugin install bespoke@ai-kitchen --scope project   # inside a repo that needs it
```

Files here are mirrored from a private companion repo, which uses the same
`plugins/<tier>/skills/<name>/` paths. Edits made directly here are pulled back
by that repo's `pull-public`.
