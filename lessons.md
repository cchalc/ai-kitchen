# Lessons

Append-only log of non-obvious things learned while working in this repo. Newest entries on top. Format:

```
### YYYY-MM-DD — short title

**What:** the surprise / learning.
**Why it matters:** how it changes future work.
**Tags:** #topic1 #topic2
```

---

### 2026-10-02 — `claude plugin eval` sandbox isolation; route-test with headless `claude -p`

**What:** `claude plugin eval` runs each case in a sandbox with a private `home/`. Claude authenticates via an `apiKeyHelper` whose credential cache lives in the real home dir; the eval sandbox's private `home/` can't reach it. The workaround is `tools/route_eval.py`: it runs each prompt through headless `claude -p --plugin-dir ./plugin` (Bash/Write/Edit/Agent disallowed) in a throwaway git repo and scores the first `Skill` call. Run `uv run python tools/route_eval.py skill-routing.yaml tools/route-heldout.yaml`. It tests against the real environment (300+ competing skills), which is the honest test.
**Why it matters:** Two traps when scoring: (1) a bare skill name that matches yours may be a **built-in** with the same name (Claude Code ships `code-review`), so require the plugin-qualified prefix; (2) context-free prompts in an empty repo make the model gather context instead of loading a skill, so phrase evals the way a user would in a real repo.
**Tags:** #evals #routing #auth #sandbox #testing

### 2026-10-02 — De-serokell-izing an external skills repo: four coupling categories to strip

**What:** Ported 10 of serokell-global's 15 skills. The reusable ones were coupled to serokell in four separable ways, and triaging by category (not per-skill) made the port fast: (1) **issue tracker** — YouTrack lifecycle/URLs → generalize to "GitHub `#N` / the tracker's key"; (2) **nix** — `nix flake init` templates, self-hosted nix runners, binary cache, flake-license caveats → drop or replace with hosted-runner equivalents; (3) **language** — Haskell/cabal/tasty examples → swap for language-agnostic guidance + Python/JS illustrations; (4) **org process** — metatemplates, `serokell/operations`, Notion, promo blurbs, "consult your manager" → drop entirely. Skills clustered cleanly: 6 near-verbatim ports (only tracker bits removed), 2 needing org/nix framing stripped (`license-choice`, `reuse-headers`), 2 needing real rewrites because philosophy was buried in Haskell/nix mechanics (`code-testing`, `setup-ci`). The 5 skipped skills were ≥75% one of those couplings. Serokell's content is CC0-1.0 (public domain), so no attribution is legally required — added a one-line courtesy `<!-- Adapted from … -->` comment anyway.

**Why it matters:** When adapting any external skill set, classify each coupling by category first; "how much survives" falls out of that, and whole skills are often all-or-nothing on a single category. Serokell's SKILL.md `description` fields are an excellent model (concrete trigger phrases) but **lack the explicit negative triggers vibe CI requires** — every port needed a "Do NOT use … (that's <sibling>)" clause added, cross-excluding the sibling it most overlaps (commit vs PR vs review; license vs SPDX headers; test-writing vs CI config).

**Tags:** #skills #porting #serokell #skill-design #routing #publishing

### 2026-07-19 — `wt` (worktrunk) + `jj` colocation for parallel agent work

**What:** Ran a ponytail (github.com/DietrichGebert/ponytail) over-engineering review across a TanStack/Electric app and split the fixes into 3 parallel `wt` worktrees. Key mechanics: `wt` drives **git** worktrees, not jj. For a jj-first repo, `jj git init --colocate` the main copy, then `wt switch --create <branch>` per stream, commit with plain `git` **inside** each worktree (jj isn't present there), `wt merge -y` back to main, and finally `jj git import` in main to pull the commits into jj. Parallel branches merged with zero conflicts because each touched a disjoint set of files. Two gotchas: (1) an interactive `commit-msg` hook doing `exec < /dev/tty` fails non-interactively — use `git commit --no-verify` for agent commits; (2) worktrees have no `node_modules`, so don't `pnpm install` N times — symlink or verify statically.

**Why it matters:** This is the repeatable recipe for fanning agent work out in parallel and folding it back into a jj history. Plan the split by **file boundaries, not features**, so merges stay conflict-free. Ponytail's scope is strictly over-engineering (dead code, single-caller wrappers, unused params, redundant memoization) — keep convention nits (e.g. `useState` bans) out of that pass so the review stays honest.

**Tags:** #jj #worktrunk #wt #parallel-agents #ponytail #workflow

### 2026-05-28 — First-time devenv activation has three setup gotchas

**What:** Activating `direnv allow` on a fresh host with `use devenv` in `.envrc` triggered three separate failures before the shell would load.
1. `~/.config/direnv/direnvrc` was empty — direnv's stdlib doesn't include `use_devenv`. Fix: `devenv direnvrc > ~/.config/direnv/direnvrc`. (This is a user-global change affecting all direnv projects.)
2. devenv evaluation failed with "Failed to get cachix caches" because the user wasn't in `trusted-users` in `/etc/nix/nix.conf`. Fix: set `cachix.enable = false;` in `devenv.nix`. Re-enable later if added to trusted-users.
3. devenv generates `.devenv.flake.nix` at the repo root each shell build. It was tracked by jj/git on first activation. Fix: add `.devenv.flake.nix` to `.gitignore` alongside `.devenv/`.
**Why it matters:** Future setups on new machines will hit the same three. Document them in the README's quickstart so others (and future-me) skip the dance. Future devenv versions may bundle the direnvrc stdlib — re-check when bumping.
**Tags:** #devenv #direnv #onboarding #nix

### 2026-05-26 — Multiple GitHub identities: SSH vs gh CLI can mismatch

**What:** When your git SSH key and your `gh` CLI authenticate as different GitHub accounts, a clone/push can fail with a generic "Repository not found" — which reads like a typo but is actually an access mismatch.
**Why it matters:** Check `ssh -T git@github.com` and `gh auth status` separately when a clone/push fails unexpectedly. Use `gh repo clone` (HTTPS via the gh token) to sidestep an SSH-identity mismatch, or configure SSH multi-identity.
**Tags:** #github #auth #onboarding

### 2026-05-26 — Vibe CI rejects skills without explicit negative triggers

**What:** `/vibe-publish-plugin` won't pass CI unless each skill `description` includes "NOT for X" exclusions for overlapping skills. Evals require ≥95% routing accuracy.
**Why it matters:** Write the negative triggers when drafting in `scratch/`, not as an afterthought before publishing. Saves a CI round-trip.
**Tags:** #publishing #ci #skill-design
