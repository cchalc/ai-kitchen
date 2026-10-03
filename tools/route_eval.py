"""Headless skill-routing eval for Claude Code plugins.

`claude plugin eval` may fail in sandboxed environments where the credential
cache is unreachable. This runs each prompt through `claude -p` against the real
environment and scores the first Skill call.

Usage: uv run python tools/route_eval.py skill-routing.yaml [more.yaml ...]
"""
import json
import pathlib
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import yaml

PLUGIN = pathlib.Path(__file__).resolve().parent.parent / "plugin"
PLUGIN_NAME = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["name"]


def run(case, repo):
    p = subprocess.run(
        ["claude", "-p", case["prompt"], "--plugin-dir", str(PLUGIN),
         "--output-format", "stream-json", "--verbose", "--max-turns", "6",
         "--disallowedTools", "Bash", "Write", "Edit", "NotebookEdit", "Agent"],
        cwd=repo, capture_output=True, text=True, timeout=240,
    )
    skills = []
    for line in p.stdout.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "assistant":
            skills += [c["input"].get("skill") for c in m["message"]["content"]
                       if c.get("type") == "tool_use" and c["name"] == "Skill"]
    got = skills[0] if skills else None
    # Require the plugin prefix: a bare name may be a same-named built-in skill.
    return case, got, got == PLUGIN_NAME + ":" + case["expect"]


def main():
    cases = [c for f in sys.argv[1:] for c in yaml.safe_load(open(f))["evals"]]
    with tempfile.TemporaryDirectory() as repo:
        # A throwaway repo with a staged change, so git-flavoured prompts have context.
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        pathlib.Path(repo, "app.py").write_text("print('hi')\n")
        subprocess.run(["git", "add", "app.py"], cwd=repo, check=True)
        with ThreadPoolExecutor(4) as ex:
            results = list(ex.map(lambda c: run(c, repo), cases))
    for case, got, ok in results:
        print(f"{'PASS' if ok else 'FAIL'} {case['expect']:16} got={got!s:30} | {case['prompt']}")
    n = sum(ok for *_, ok in results)
    print(f"\n{n}/{len(results)} routed correctly ({100 * n / len(results):.0f}%)")
    sys.exit(0 if n == len(results) else 1)


if __name__ == "__main__":
    main()
