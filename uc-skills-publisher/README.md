# Publish Agent Skills to Unity Catalog

A tool for publishing agent skills (Genie, Claude Code, Copilot) into Unity Catalog as securable assets, enabling teams to share custom skills across coding agents with fine-grained access control.

## Overview

Skills are Unity Catalog securables under the `/api/2.1/unity-catalog/skills` endpoint, backed by files in a `Skills/` volume. This publisher creates skills from a local git source directory and uploads them to UC via REST, making them available for consumption by agents across your workspace.

**Why this approach instead of bundles?** Databricks bundles (DAB) have no `skills` resource type — the REST API is the only producer path for UC securable skills.

## Two ways to publish

| Method | Use case | Scope | MCP impact |
|--------|----------|-------|-----------|
| **Unity Gateway MCP** (`ug skills` tool) | Single skill, interactive authoring | One skill at a time | Changes MCP scope (may prune other servers) |
| **REST Publisher** (this tool) | Batch sync from git, CI/scheduled jobs | Multiple skills at once | None — runs locally, no MCP involvement |

This publisher implements the **REST method** for bulk sync and CI workflows. For single-skill interactive authoring, use the official `ug skills create_skill` / `update_skill` MCP commands.

## Prerequisites

- **Databricks CLI ≥ 1.11.0** — check with `databricks --version`
- **Python 3.12+** and **uv** — check with `python3 --version` and `uv --version`
- **Unity Catalog** enabled on your workspace
- **Profile configured** in `~/.databrickscfg` with OAuth access to your workspace
- **Catalog and schema** created in your target metastore (or permissions to create them)

### Verify your setup

```bash
# Check Databricks CLI and profile
databricks auth describe --profile <your-profile>

# Check Python and uv
python3 --version  # should be 3.12+
uv --version

# Verify catalog/schema access
databricks catalogs get --profile <your-profile> <catalog>
databricks schemas get --profile <your-profile> <catalog>.<schema>
```

## Quick start

### Dry run (preview, no changes)

```bash
uv run --with pyyaml python publish_skills_to_uc.py \
  --profile <your-profile> \
  --catalog <catalog> \
  --schema <schema> \
  --dry-run
```

### Publish to UC (creates or updates skills)

```bash
uv run --with pyyaml python publish_skills_to_uc.py \
  --profile <your-profile> \
  --catalog <catalog> \
  --schema <schema>
```

### What it does

1. **Discovers** skills: scans `skills/<skill-name>/SKILL.md` for valid skills
2. **Validates**: checks skill names, descriptions (≤1024 bytes), YAML frontmatter
3. **Creates/updates**: three REST calls per skill:
   - `POST /api/2.1/unity-catalog/skills` — create or check existence
   - `PUT /api/2.0/fs/files/Skills/...` — upload all files from the skill directory
   - `POST /api/2.1/unity-catalog/skills/.../finalize` — finalize and register
4. **Reports**: shows created, updated, and errored skills

## Skill directory layout

Each skill lives in its own subdirectory under `skills/`:

```
skills/
├── my-skill-1/
│   ├── SKILL.md                 # Frontmatter: name, description, metadata
│   ├── references.md            # (optional) additional docs, links
│   └── ... (any files)
└── my-skill-2/
    ├── SKILL.md
    └── ...
```

### SKILL.md frontmatter

```yaml
---
name: my-skill-1                  # must match directory name
description: |
  What this skill does (when to use it).
  
  When NOT to use this skill (negative triggers).
metadata:
  compatible-agents: [genie, claude-code, codex]
---
# Markdown content (skill guide, examples, etc.)
```

**Constraints:**
- `name:` must exactly match the directory name (lowercase alphanumerics and hyphens)
- `description:` must be ≤1024 bytes (include clear use cases and negative triggers)
- All skill files are uploaded to UC and available to consumers

## Grants: sharing skills with your team

Skills are private to the owner until granted. To share with consuming principals (users, service principals, groups), grant these UC permissions:

```sql
GRANT USE CATALOG ON CATALOG <catalog> TO <principal>;
GRANT USE SCHEMA ON SCHEMA <catalog>.<schema> TO <principal>;
GRANT READ VOLUME ON VOLUME <catalog>.<schema>.Skills TO <principal>;
```

Example:

```sql
-- Share with a user group
GRANT USE CATALOG ON CATALOG my-catalog TO `data-team@company.com`;
GRANT USE SCHEMA ON SCHEMA my-catalog.agent_skills TO `data-team@company.com`;
GRANT READ VOLUME ON VOLUME my-catalog.agent_skills.Skills TO `data-team@company.com`;

-- Share with a service principal
GRANT USE CATALOG ON CATALOG my-catalog TO `service-principal-name`;
GRANT USE SCHEMA ON SCHEMA my-catalog.agent_skills TO `service-principal-name`;
GRANT READ VOLUME ON VOLUME my-catalog.agent_skills.Skills TO `service-principal-name`;
```

## Consuming skills: agents using published skills

Once published and granted, consuming agents use Unity Gateway to download and consume skills:

```bash
# List available skills in a schema
ug skills list

# Download a single skill
ug skills add --names <catalog>.<schema>.<skill-name> --via download

# Download all skills from a schema
ug skills add --location <catalog>.<schema> --via download

# Remove a skill
ug skills remove --names <catalog>.<schema>.<skill-name>
```

**Note:** Use `--via download` to keep your MCP configuration intact. The `--via mcp` option will modify MCP scope and may trigger `ug configure` (which prunes other MCP servers).

## Gotchas and limitations

1. **`--via mcp` prunes other MCP servers**: `ug skills add --via mcp` calls `ug configure` internally, which prunes your `~/.claude.json` to the single target workspace. Avoid it unless you're intentionally reconfiguring. Use `--via download` instead.

2. **UC skills are workspace-specific**: Unity Catalog skills live in a single workspace's metastore. To publish the same skills to multiple workspaces or metastores, re-run this publisher with a different `--profile` and target catalog/schema.

3. **Description size limit**: `description:` in your `SKILL.md` frontmatter must be ≤1024 bytes after UTF-8 encoding. Violations are caught at publish time.

4. **Skill name constraints**: skill directory names must be lowercase alphanumerics with optional inner hyphens (e.g., `my-skill-1`, `data-validator`, `api-checker`). Names must be unique within the schema.

5. **Cross-metastore replication**: if you have multiple metastores (e.g., AWS and Azure), publish separately to each:
   ```bash
   # AWS metastore
   uv run --with pyyaml python publish_skills_to_uc.py \
     --profile aws-workspace --catalog catalog-aws --schema skills

   # Azure metastore
   uv run --with pyyaml python publish_skills_to_uc.py \
     --profile azure-workspace --catalog catalog-azure --schema skills
   ```

## CLI reference

```bash
uv run --with pyyaml python publish_skills_to_uc.py [OPTIONS]

Options:
  --profile PROFILE           Databricks CLI profile (required)
  --catalog CATALOG           Target catalog (required)
  --schema SCHEMA             Target schema (required)
  --skills-root PATH          Root directory containing skill subdirs (default: ./skills)
  --dry-run                   Preview only; do not publish
  --help                      Show this message
```

## Troubleshooting

### "catalog not found / not granted"

Ensure the catalog exists and your profile has access:

```bash
databricks catalogs get --profile <your-profile> <catalog>
```

Create the catalog if needed:

```bash
databricks catalogs create --profile <your-profile> --name <catalog>
```

### "schema ... MISSING"

The schema will be auto-created on publish (non-dry-run). For dry-run, create it first:

```bash
databricks schemas create --profile <your-profile> \
  --name <schema> --catalog <catalog>
```

### "description X bytes > 1024"

Trim the `description:` field in your `SKILL.md` frontmatter to ≤1024 bytes.

### "frontmatter name '...' != dir '...'"

The `name:` field in `SKILL.md` must exactly match the directory name. Fix it and retry.

### "name collision (already from ...)"

Two skill directories have the same name. Skill names must be unique within a schema. Rename one and retry.

## Example workflow

```bash
# 1. Create a skill directory
mkdir -p skills/my-validator
cat > skills/my-validator/SKILL.md << 'EOF'
---
name: my-validator
description: |
  Validates data schemas and catches common formatting errors.
  
  Best for: CSV validation, schema checking, type inference
  Not for: Real-time streaming validation, large multi-TB datasets
metadata:
  compatible-agents: [genie, claude-code]
---
# Validator Skill

This skill...
EOF

# 2. Add more files (optional)
cp my-reference.md skills/my-validator/references.md

# 3. Dry run
uv run --with pyyaml python publish_skills_to_uc.py \
  --profile my-profile --catalog my-catalog --schema skills --dry-run

# 4. Publish
uv run --with pyyaml python publish_skills_to_uc.py \
  --profile my-profile --catalog my-catalog --schema skills

# 5. Grant access
databricks sql --profile my-profile << 'EOF'
GRANT USE CATALOG ON CATALOG my-catalog TO `team@company.com`;
GRANT USE SCHEMA ON SCHEMA my-catalog.skills TO `team@company.com`;
GRANT READ VOLUME ON VOLUME my-catalog.skills.Skills TO `team@company.com`;
EOF

# 6. Consume in an agent
ug skills add --location my-catalog.skills --via download
```

## For CI/automation

Add to your CI pipeline (e.g., GitHub Actions, Databricks Workflows):

```bash
#!/bin/bash
set -e

# Publish skills from main branch to production schema
uv run --with pyyaml python publish_skills_to_uc.py \
  --profile prod-workspace \
  --catalog prod-catalog \
  --schema prod-skills
```

Ensure your CI environment has:
- Databricks CLI configured with the target profile
- Python 3.12+ and uv installed
- Read access to the git repository

## See also

- [Unity Catalog securables](https://docs.databricks.com/en/security/auth-and-access-management/catalog-api/index.html)
- [Unity Gateway documentation](https://github.com/databricks/unity-gateway)
- [Databricks CLI profiles](https://docs.databricks.com/en/dev-tools/cli/profiles.html)
