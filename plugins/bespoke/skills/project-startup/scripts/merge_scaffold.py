#!/usr/bin/env python3
"""Merge a scaffolded project directory into an existing repo without clobbering it.

Template scaffolders usually refuse a non-empty target, but project-startup lays down the
dev standards (CLAUDE.md, .claude/, .envrc, living docs) BEFORE the template. So the
template is scaffolded into a temp dir and merged in with this script:

    python merge_scaffold.py SCAFFOLD_DIR REPO_DIR            # dry run: print the plan
    python merge_scaffold.py SCAFFOLD_DIR REPO_DIR --apply    # write it

Per file in the scaffold:
  ADD      not in the repo yet → copied
  SAME     identical bytes already in the repo → nothing to do
  KEEP     a standards-owned path (see PROTECTED, extend with --protect) → never written
  APPEND   .gitignore → the scaffold's missing lines are appended under a marker comment
  REPLACE  README.md whose repo copy is only a bare `# Title` stub → replaced
  CONFLICT anything else that differs → nothing is written; resolve and re-run

All-or-nothing: if any CONFLICT exists, --apply writes nothing and exits 1. Resolve a
conflict by editing/deleting the file in the (temp) scaffold dir, or merging it by hand
into the repo, then re-run. Symlinks anywhere in the scaffold are refused (exit 2): the
scaffold is untrusted data, and nothing from it is executed. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Paths the dev standards own. A directory entry (trailing "/") covers everything under it.
PROTECTED = (
    ".git/",
    ".claude/",
    "CLAUDE.md",
    ".envrc",
    ".envrc.local",
    "checkpoint.md",
    "tasks.md",
    "lessons.md",
    "CHANGELOG.md",
    ".github/pull_request_template.md",
)
GITIGNORE_MARKER = "# --- merged from scaffold ---"
STUB_README = re.compile(r"\A\s*#[^\n]*\s*\Z")


class MergeError(Exception):
    """User-facing error: printed without a traceback, exit code 2."""


def is_protected(rel: str, protected: tuple[str, ...]) -> bool:
    for p in protected:
        if p.endswith("/"):
            if rel == p[:-1] or rel.startswith(p):
                return True
        elif rel == p:
            return True
    return False


def gitignore_additions(scaffold_text: str, repo_text: str) -> list[str]:
    """Scaffold rule lines the repo .gitignore lacks (comments/blanks are not rules)."""
    have = {ln.strip() for ln in repo_text.splitlines()}
    out = []
    for ln in scaffold_text.splitlines():
        s = ln.strip()
        if s and not s.startswith("#") and s not in have and s not in out:
            out.append(s)
    return out


def plan(scaffold: Path, repo: Path, protected: tuple[str, ...]) -> list[tuple[str, str]]:
    """[(action, relpath)] for every file in the scaffold, sorted by path."""
    links = [p for p in scaffold.rglob("*") if p.is_symlink()]
    if links:
        names = ", ".join(str(p.relative_to(scaffold)) for p in links)
        raise MergeError(f"refusing symlinks in scaffold: {names}")
    actions = []
    for src in sorted(p for p in scaffold.rglob("*") if p.is_file()):
        rel = src.relative_to(scaffold).as_posix()
        dst = repo / rel
        if is_protected(rel, protected):
            actions.append(("KEEP", rel))
        elif not dst.exists():
            actions.append(("ADD", rel))
        elif dst.is_dir():
            actions.append(("CONFLICT", rel))
        elif src.read_bytes() == dst.read_bytes():
            actions.append(("SAME", rel))
        elif src.name == ".gitignore":
            extra = gitignore_additions(_text(src), _text(dst))
            actions.append(("APPEND" if extra else "SAME", rel))
        elif rel == "README.md" and STUB_README.match(_text(dst)):
            actions.append(("REPLACE", rel))
        else:
            actions.append(("CONFLICT", rel))
    return actions


def apply(scaffold: Path, repo: Path, actions: list[tuple[str, str]]) -> None:
    for action, rel in actions:
        src, dst = scaffold / rel, repo / rel
        if action in ("ADD", "REPLACE"):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        elif action == "APPEND":
            current = _text(dst)
            extra = gitignore_additions(_text(src), current)
            sep = "" if current.endswith("\n") or not current else "\n"
            dst.write_text(current + sep + "\n" + GITIGNORE_MARKER + "\n" + "\n".join(extra) + "\n")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("scaffold", type=Path, help="scaffolded project dir (e.g. in a temp dir)")
    p.add_argument("repo", type=Path, help="existing repo to merge into")
    p.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    p.add_argument(
        "--protect", action="append", default=[], metavar="PATH",
        help="extra standards-owned path to never write (dir: trailing '/'); repeatable",
    )
    args = p.parse_args(argv)
    try:
        scaffold, repo = args.scaffold.resolve(), args.repo.resolve()
        for d in (scaffold, repo):
            if not d.is_dir():
                raise MergeError(f"{d} is not a directory")
        if scaffold == repo:
            raise MergeError("scaffold and repo are the same directory")
        actions = plan(scaffold, repo, PROTECTED + tuple(args.protect))
    except MergeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for action, rel in actions:
        if action != "SAME":
            print(f"{action:8} {rel}")
    counts = {a: sum(1 for x, _ in actions if x == a) for a, _ in actions}
    print("summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if counts.get("CONFLICT"):
        print("conflicts: nothing written. Resolve them and re-run.", file=sys.stderr)
        return 1
    if args.apply:
        apply(scaffold, repo, actions)
        print("applied.")
    else:
        print("dry run: re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
