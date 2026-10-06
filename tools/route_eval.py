"""Headless skill-routing eval for Claude Code plugins.

`claude plugin eval` may fail in sandboxed environments where the credential
cache is unreachable. This runs each prompt through `claude -p` against the real
environment and scores the first Skill call.

Loads every plugin listed in the repo's .claude-plugin/marketplace.json, so each
case is scored against its skill's own plugin prefix (<plugin>:<skill>) with all
tiers competing. Run it before installing these plugins globally, or the installed
copies compete with the ones loaded here.

Usage: uv run python tools/route_eval.py skill-routing.yaml [more.yaml ...]
"""
import json
import pathlib
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKETPLACE = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
PLUGINS = [(ROOT / p["source"]).resolve() for p in MARKETPLACE["plugins"]]
# skill name -> "<plugin>:<skill>", the prefix a correct route must carry
EXPECTED = {
    skill.name: f"{json.loads((plugin / '.claude-plugin' / 'plugin.json').read_text())['name']}:{skill.name}"
    for plugin in PLUGINS
    for skill in sorted((plugin / "skills").glob("*/"))
}


def run(case, repo):
    try:
        stdout = subprocess.run(
            ["claude", "-p", case["prompt"],
             *[arg for plugin in PLUGINS for arg in ("--plugin-dir", str(plugin))],
             "--output-format", "stream-json", "--verbose", "--max-turns", "6",
             "--disallowedTools", "Bash", "Write", "Edit", "NotebookEdit", "Agent"],
            cwd=repo, capture_output=True, text=True, timeout=240,
        ).stdout
    except subprocess.TimeoutExpired as e:
        # Routing is decided in the first turns; score whatever was streamed.
        stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    skills = []
    for line in stdout.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "assistant":
            skills += [c["input"].get("skill") for c in m["message"]["content"]
                       if c.get("type") == "tool_use" and c["name"] == "Skill"]
    got = skills[0] if skills else None
    # Require the plugin prefix: a bare name may be a same-named built-in skill.
    return case, got, got == EXPECTED.get(case["expect"])


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
