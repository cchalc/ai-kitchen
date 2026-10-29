# Keeping uv.lock on public PyPI

uv records whatever index it resolved from. A developer's user-level uv config (for example a
corporate PyPI proxy as the default index) therefore leaks into `uv.lock`, and public CI and
cloners can't install. The fix keeps uv working the way each developer has it configured, and
keeps only the *committed lock* public.

**Don't** pin an index in `pyproject.toml` (it breaks plain `uv` on networks that only reach a
proxy), and **don't** export `UV_DEFAULT_INDEX` (`uv add` persists it into `pyproject.toml`).

## 1. Makefile: `lock` and `check-lock`

Add `lock check-lock` to `.PHONY` and make `lint` depend on the guard (`lint: check-lock`), so it
runs everywhere the gate runs:

```make
# uv works with whatever index your own uv config sets (e.g. a corporate PyPI proxy), but the
# committed uv.lock must reference only public PyPI so CI and cloners can install.
# Behind a proxy, put `export UV_FROZEN=1` in .envrc.local: syncs and runs then install from the
# lock without rewriting it. After `uv add <pkg>` (or editing pyproject.toml), run `make lock`.
PUBLIC_HOSTS = https://(pypi\.org|files\.pythonhosted\.org)

install:  ## Install dependencies, including dev
	uv sync --all-extras --all-groups

# Resolves through your configured index, then maps a PyPI proxy's URLs to the identical public
# files (proxies serve PyPI's own content-addressed /packages/... paths; hashes are unchanged).
lock:  ## Re-lock dependencies; the lock is rewritten to public PyPI URLs
	env -u UV_FROZEN uv lock
	sed -i.bak -E -e 's#registry = "https?://[^"]+"#registry = "https://pypi.org/simple"#g' \
	  -e 's#https?://[^/"]+/packages/#https://files.pythonhosted.org/packages/#g' uv.lock
	rm uv.lock.bak
	@$(MAKE) --no-print-directory check-lock

check-lock:  ## Fail if uv.lock references anything but public PyPI
	@bad=$$(grep -hoE 'https?://[^/"]+' uv.lock | grep -vxE '$(PUBLIC_HOSTS)' | sort -u); \
	if [ -n "$$bad" ]; then echo "non-public index hosts: $$bad (run make lock)" >&2; exit 1; fi
```

The rewrite works only for a proxy that serves PyPI's own content-addressed
`/packages/<hash>/...` paths, as most PyPI proxies do. Check one file's sha256 against
`files.pythonhosted.org` before trusting it. If the project ever adds a non-PyPI index,
revisit the `registry` rewrite.

## 2. Developers behind a proxy

In `.envrc.local` (gitignored), add `export UV_FROZEN=1`. `uv sync` / `uv run` then install from
the lock without rewriting it, and `uv add` only edits `pyproject.toml`. Run `make lock`
afterwards.

## 3. CI

In the lint job, after `make install`:

```yaml
      - run: uv lock --check   # uv.lock matches pyproject.toml
      - run: make lint         # includes check-lock: public PyPI hosts only
```

## Verify

```bash
make check-lock
UV_NO_CONFIG=1 uv lock --check --offline    # how CI sees it (no user uv config)
```
