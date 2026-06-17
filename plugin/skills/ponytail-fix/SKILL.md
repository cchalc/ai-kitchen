---
name: ponytail-fix
description: >
  Run a project's check gate (lint + typecheck + tests), triage every failure
  by root cause, and apply the laziest correct fix for each — then re-verify
  the gate is green. Fixes real bugs; suppresses only confirmed false positives
  with a reason. Use when the user says "fix the lint errors", "make the check
  pass", "fix the build", "clear the type errors", or "get CI green". Do NOT
  use to add features, refactor working code, reformat untouched files, or when
  the user only wants a list of problems (that's a review, not a fix).
---

Fix everything the gate reports, smallest correct diff per error. Root cause
over symptom, reuse over rewrite. Suppress only false positives, with a reason;
never silence a real bug.

## Find the gate

There is no universal command. Detect it, then run all layers — a green
linter over a red typecheck is not done. Common sources:

- `package.json` scripts: `check`, `lint`, `typecheck`, `test`, `test:unit`.
- `Makefile` targets: `make lint`, `make check`, `make test`.
- `pyproject.toml` / `noxfile.py` / `tox.ini`: `ruff`, `mypy`/`pyright`, `pytest`.
- Pre-commit config: `.pre-commit-config.yaml` (`pre-commit run --all-files`).
- CI file (`.github/workflows/*.yml`): read what CI actually runs — that IS
  the gate.

If nothing is obvious, ask which command must pass rather than guess.

## Loop

1. **Collect.** Run every gate layer. Group failures by rule/code, then by
   root cause — not by file. One missing generated file or one stale type can
   spray many errors across many files. Find the source, not the symptoms.
2. **Auto-fix first.** Use the tool's own fixer before hand-editing:
   `ruff check --fix`, `biome check --write`, `eslint --fix`, `gofmt -w`.
   Re-run, re-collect.
3. **Triage what's left** into: false positive · shared root cause · real bug.
4. **Fix by category** (below), lowest-effort correct fix each.
5. **Re-verify.** Re-run the full gate. Repeat until every layer is green.

## Fix by category

- **Missing generated file** (a `Cannot find module` / import error plus a
  cascade of downstream type errors) → regenerate it, don't hand-edit. Find the
  generator (codegen script, build step, framework plugin) and run it.
- **Stale code vs. schema/model** (`X is missing` where X exists in the source
  of truth but a consumer doesn't produce it) → fix the consumer to match the
  source, not the type annotation. The drift is the bug.
- **Unused import / variable** → confirm one occurrence (`grep -c NAME file`),
  then delete. If it was meant to be used, that's a real bug — wire it up.
- **Unsafe null/None access flagged by the checker** → narrow at the source
  (type guard, early return, `is not None` filter) so downstream access is
  provably safe. Prefer narrowing over assertion casts.
- **Rule fires on framework code the linter can't see through** (a control that
  renders as something else, a re-export, a decorator) → likely a false
  positive; suppress inline with a reason after confirming behavior is correct.
- **Test-runner globals undefined in typecheck** → add the runner's types to
  the type config (e.g. `vitest/globals`, pytest plugins) rather than importing
  them everywhere.
- **Broken assertion** (calls a method the object lacks, computes a value then
  never asserts on it) → real bug. Rewrite to assert the actual condition.

## Suppression rule

Suppress ONLY confirmed false positives, always with a reason comment in the
tool's own format (`# noqa: RULE — why`, `// biome-ignore lint/RULE: why`,
`# type: ignore[code]  # why`). Never suppress a real bug. If unsure whether
it's a false positive, fix the code instead.

## Output

Per fixed cluster, one line: `<rule/code>: <root cause> → <fix>`. End with the
gate result, e.g. `lint ✓ · types ✓ · tests N passed`. If a layer was left
untouched, say why in one line (e.g. slow integration suite not in the gate).

## Boundaries

Fixes the gate, nothing else. No refactors, no new features, no reformatting
untouched code. If a fix needs a design decision or changes product behavior,
stop and ask rather than guess. Pairs with ponytail (build style) and
ponytail-review (list-only). "stop ponytail-fix" / "normal mode": revert.
