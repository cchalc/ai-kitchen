"""Publish agent skills to Unity Catalog as securable assets.

Reads skills from a local directory structure (skills/<skill-name>/SKILL.md) and
publishes them to a Unity Catalog schema via the REST API. Handles creation,
updates, and validation locally — no bundle, no job, no notebook required.

The producer recipe (three REST calls per skill):
  1. POST /api/2.1/unity-catalog/skills?parent=schemas/<cat>.<schema>&skill_id=<leaf>
  2. PUT  /api/2.0/fs/files/Skills/<cat>/<schema>/<leaf>/<relpath>   (one per file)
  3. POST /api/2.1/unity-catalog/skills/<cat>.<schema>.<leaf>/finalize

Finalize reads the uploaded SKILL.md frontmatter: `name:` must equal the skill's
directory name and `description:` must be <= 1024 bytes.

Usage:
  uv run --with pyyaml python publish_skills_to_uc.py \\
      --profile <profile> --catalog <catalog> --schema <schema> --dry-run
  # then drop --dry-run to publish.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import AlreadyExists, NotFound

SKILLS_API = "/api/2.1/unity-catalog/skills"
FILES_API = "/api/2.0/fs/files"
# Skill leaf: lowercase alphanumerics with inner hyphens, up to 64 chars.
SKILL_LEAF_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        return {}
    body = text.lstrip()[3:]
    end = body.find("\n---")
    block = body if end == -1 else body[:end]
    try:
        return yaml.safe_load(block) or {}
    except yaml.YAMLError:
        return {}


def discover(skills_root: Path):
    """Yield (leaf, dir) for each valid skill; collect skips."""
    winners: dict[str, Path] = {}
    skips: list[tuple[str, str]] = []  # (leaf, reason)

    if not skills_root.is_dir():
        print(f"ERROR: skills root not found: {skills_root}", file=sys.stderr)
        return winners, skips

    for skill_dir in sorted(d for d in skills_root.iterdir() if d.is_dir()):
        leaf = skill_dir.name
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            skips.append((leaf, "no SKILL.md"))
            continue
        if not SKILL_LEAF_PATTERN.match(leaf):
            skips.append((leaf, f"invalid leaf name (fails {SKILL_LEAF_PATTERN.pattern})"))
            continue
        fm = parse_frontmatter(md)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != leaf:
            skips.append((leaf, f"frontmatter name '{name}' != dir '{leaf}'"))
            continue
        if len(str(desc).encode("utf-8")) > 1024:
            skips.append((leaf, f"description {len(str(desc).encode())} bytes > 1024"))
            continue
        if leaf in winners:
            skips.append((leaf, f"name collision (already discovered)"))
            continue
        winners[leaf] = skill_dir

    return winners, skips


def read_bundle(skill_dir: Path) -> dict[str, bytes]:
    return {
        str(f.relative_to(skill_dir)): f.read_bytes()
        for f in sorted(skill_dir.rglob("*"))
        if f.is_file()
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", default="DEFAULT", help="Databricks CLI profile (default: DEFAULT)")
    ap.add_argument("--catalog", required=True, help="Target catalog (required)")
    ap.add_argument("--schema", required=True, help="Target schema (required)")
    ap.add_argument(
        "--skills-root",
        default="skills",
        help="Path to skills directory (default: ./skills)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Preview only; do not publish")
    args = ap.parse_args()

    catalog, schema = args.catalog, args.schema
    skills_root = Path(args.skills_root).resolve()

    w = WorkspaceClient(profile=args.profile)
    api = w.api_client

    print(f"profile   {args.profile}")
    print(f"target    {catalog}.{schema}")
    print(f"root      {skills_root}\n")

    winners, skips = discover(skills_root)
    print(f"Discovered {len(winners)} publishable skill(s), {len(skips)} skipped.")
    for leaf, reason in skips:
        print(f"  SKIP   {leaf}: {reason}")
    for leaf, d in sorted(winners.items()):
        print(f"  PUBLISH {leaf}  ({len(read_bundle(d))} file(s))")

    if args.dry_run:
        # Verify the schema/catalog reachability read-only, then stop.
        try:
            w.catalogs.get(catalog)
            try:
                w.schemas.get(f"{catalog}.{schema}")
                print(f"\nschema {catalog}.{schema} exists")
            except NotFound:
                print(f"\nschema {catalog}.{schema} MISSING — would be created on real run")
        except NotFound:
            print(f"\nERROR: catalog {catalog} not found / not granted", file=sys.stderr)
        print("--- dry run: nothing published ---")
        return

    # Ensure schema exists.
    w.catalogs.get(catalog)
    try:
        w.schemas.get(f"{catalog}.{schema}")
    except NotFound:
        w.schemas.create(name=schema, catalog_name=catalog)
        print(f"created schema {catalog}.{schema}")

    created = updated = errored = 0
    for leaf, skill_dir in sorted(winners.items()):
        try:
            try:
                api.do("POST", SKILLS_API, query={"parent": f"schemas/{catalog}.{schema}", "skill_id": leaf}, body={})
                action = "created"
            except AlreadyExists:
                action = "updated"
            for rel, content in read_bundle(skill_dir).items():
                api.do(
                    "PUT",
                    f"{FILES_API}/Skills/{catalog}/{schema}/{leaf}/{rel}",
                    headers={"Content-Type": "application/octet-stream"},
                    data=content,
                )
            api.do("POST", f"{SKILLS_API}/{catalog}.{schema}.{leaf}/finalize")
            created += action == "created"
            updated += action == "updated"
            print(f"  {action:8} {leaf}")
        except Exception as e:  # noqa: BLE001 - contain per-skill failures
            errored += 1
            print(f"  {'error':8} {leaf}: {e}")

    print(f"\n{created} created, {updated} updated, {errored} errored.")
    if errored:
        raise SystemExit(f"{errored} skill(s) failed to publish")


if __name__ == "__main__":
    main()
