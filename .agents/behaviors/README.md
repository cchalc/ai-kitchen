# Agent behaviors

This repo adopts the [agentbehavior.dev](https://www.agentbehavior.dev/) format: each
behavior is a Markdown spec at `.agents/behaviors/<name>/BEHAVIOR.md` describing conduct an
agent is expected to follow across repeated interactions. Specs use YAML frontmatter
(`name`, `description`, optional `metadata`) followed by bold-label sections — **Intent**,
**Evidence**, **Decision**, **Execution**, **Recovery**, and **Failure modes**.

Agents working in this repo should read the relevant `BEHAVIOR.md` before acting on anything
it governs, and treat it as a binding operating rule rather than a suggestion.

## Behaviors

- `package-management` — never use Homebrew; install via the package managers already present
  (nix, uv, npm, pipx, direct downloads) and keep Python dependencies in the project's
  out-of-source uv virtualenv.

<!-- This file is generated from a template and mirrored into this public repo. Edit the
     source in the authoring repo, not here. -->
