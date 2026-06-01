# Lessons

Append-only log of non-obvious things learned while working in this repo. Newest entries on top. Format:

```
### YYYY-MM-DD — short title

**What:** the surprise / learning.
**Why it matters:** how it changes future work.
**Tags:** #topic1 #topic2
```

---

### 2026-05-28 — First-time devenv activation has three setup gotchas

**What:** Activating `direnv allow` on a fresh host with `use devenv` in `.envrc` triggered three separate failures before the shell would load.
1. `~/.config/direnv/direnvrc` was empty — direnv's stdlib doesn't include `use_devenv`. Fix: `devenv direnvrc > ~/.config/direnv/direnvrc`. (This is a user-global change affecting all direnv projects.)
2. devenv evaluation failed with "Failed to get cachix caches" because the user wasn't in `trusted-users` in `/etc/nix/nix.conf`. Fix: set `cachix.enable = false;` in `devenv.nix`. Re-enable later if added to trusted-users.
3. devenv generates `.devenv.flake.nix` at the repo root each shell build. It was tracked by jj/git on first activation. Fix: add `.devenv.flake.nix` to `.gitignore` alongside `.devenv/`.
**Why it matters:** Future setups on new machines will hit the same three. Document them in the README's quickstart so others (and future-me) skip the dance. Future devenv versions may bundle the direnvrc stdlib — re-check when bumping.
**Tags:** #devenv #direnv #onboarding #nix

### 2026-05-26 — `cchalc` SSH identity is distinct from `christopher-chalcraft_data` GitHub user

**What:** SSH key on this host authenticates to GitHub as `cchalc`, but the repo owner is `christopher-chalcraft_data`. Cloning with SSH failed with "Repository not found" because `cchalc` isn't a collaborator on the private repo.
**Why it matters:** Always check `ssh -T git@github.com` and `gh auth status` separately when cloning private repos. For this repo, use `gh repo clone` (HTTPS via gh token) or use the `christopher-chalcraft_data` account explicitly. Documented because the GitHub error message ("Repository not found") is generic for private + no-access, easy to misread as a typo.
**Tags:** #github #auth #onboarding

### 2026-05-26 — Vibe CI rejects skills without explicit negative triggers

**What:** `/vibe-publish-plugin` won't pass CI unless each skill `description` includes "NOT for X" exclusions for overlapping skills. Evals require ≥95% routing accuracy.
**Why it matters:** Write the negative triggers when drafting in `scratch/`, not as an afterthought before publishing. Saves a CI round-trip.
**Tags:** #publishing #ci #skill-design
