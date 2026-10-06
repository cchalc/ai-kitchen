---
name: code-testing
description: >
  Use when writing a regression test for a bug, adding tests, setting up CLI
  execution tests or coverage, or choosing the kind of test (unit / property /
  blackbox / acceptance) to write. Load it before reading the code: it sets the
  fail-before-fix / pass-after rule for bug tests. Triggers on "write a
  regression test for this bug", "add a test for this", "add test coverage",
  "test this CLI", "property-based test",
  "what kind of test should I write", "edge-case test". Do NOT use to configure
  the CI pipeline itself (that's setup-ci) or to review someone else's code
  (that's reviewing-prs).
metadata:
  visibility: public
---

# Code testing

Tests serve two qualities. **External quality** = how well the system meets its
functional requirements (what users see). **Internal quality** = how well it's
designed and how easily it can change (what developers feel). Different kinds of
tests serve them in different ratios.

## Mandatory rules

### Defect-driven testing

When you fix a bug, add a test that **fails before the fix and passes after**,
committed together. It documents the failure mode and covers a previously
untested path.

### Edge-case safety

While writing code, identify edge cases (empty inputs, boundary values, error
paths) and add a test for each — even one that passes trivially. The value is
the marker: it'll be there when someone later changes the code and will make them
notice the case.

### Execution tests for CLI tools

If the product ships a CLI (a binary the user invokes), the suite **must**
execute it through a normal shell-like invocation and validate every subcommand
and option as thoroughly as possible. This is the single most important kind of
test for a shipping CLI — it exercises the real surface the user touches. Spawn
the built binary as a subprocess (e.g. Python `subprocess`, Node
`child_process`), and assert on exit code, stdout, and stderr.

When tests run in an isolated build sandbox, the built binary may not be on
`PATH` — have the test resolve its path explicitly (e.g. via an env var the build
sets) rather than assuming a global install.

### Coverage in CI

- Produce a coverage report.
- Fail merges that reduce coverage.
- Exercise **every** executable file in the repo, including small scripts, so
  rarely-touched code can't rot silently.

## Vocabulary (use consistently)

**Level** — Acceptance (whole system, all components and interactions),
Integration (specific modules interacting), Unit (smallest component in
isolation). Higher levels give more external-quality feedback; lower levels more
internal.

**Interface use** — Edge-to-edge / end-to-end (inputs and outputs both through
the public interface, like a real user); Blackbox (end-to-end with no peeking at
internal state — pure external quality); Greybox (uses private interfaces to set
up or observe, but tests higher-level behaviour).

**Data generation** — Specific (known input → known output); Property / invariant
/ generative (random inputs, output checked against a predicate).

**Purpose** — Customer test (from user-facing specs; external quality); Developer
test (for developers' benefit; internal quality).

## Preferred strategies

- **Pure unit testing** of pure components — the biggest internal-quality lever.
  Prefer property-based testing (e.g. Hypothesis for Python, fast-check for JS);
  fall back to specific tests for edge cases the generators don't reliably hit.
  The mere existence of a unit test forces the surrounding code to be decoupled
  enough to test — a benefit beyond the assertions.
- **Functional blackbox testing** — highest-level customer tests for functional
  requirements; most important for external quality and independent of the tech
  stack.
- **Durability / load / stress / fuzzing** — highest-level blackbox tests for
  non-functional constraints (reliability, resilience, security). Valuable where
  the infrastructure exists; needs only instrumentation.

## Not prescribed here

Impure unit testing (mocking IO), functional greybox testing, and strict TDD are
all valuable but have no single mandated recipe — use judgement.

<!-- Adapted from serokell/claude-plugins (CC0-1.0). -->
