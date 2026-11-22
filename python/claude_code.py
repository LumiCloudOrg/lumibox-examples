"""Run Claude Code inside a sandbox: the agent edits files and runs commands there, never on your machine.

    export ANTHROPIC_API_KEY=...
    python claude_code.py "Write fizzbuzz.py with tests and run them"
"""
import json
import os
import shlex
import sys

from e2b import Sandbox

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")


def install(sandbox: Sandbox) -> str:
    """Installs the Claude Code CLI (the base template has Node.js); about 20 seconds. Returns its version."""
    sandbox.commands.run("sudo npm install -g @anthropic-ai/claude-code", timeout=300)
    return sandbox.commands.run("claude --version").stdout.strip()


def run(sandbox: Sandbox, task: str, api_key: str) -> dict:
    """Runs one task headless (claude -p) in /home/user/work and returns its JSON result."""
    sandbox.commands.run("mkdir -p /home/user/work")
    result = sandbox.commands.run(
        f"claude -p {shlex.quote(task)} --model {MODEL} --output-format json --permission-mode acceptEdits --allowedTools 'Bash Edit Write Read'",
        cwd="/home/user/work",
        envs={"ANTHROPIC_API_KEY": api_key},
        timeout=600,
    )
    return json.loads(result.stdout)


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Write fizzbuzz.py with a pytest test file, then run the tests."
    with Sandbox.create("base", timeout=900) as sandbox:
        print("Claude Code", install(sandbox))
        print(run(sandbox, task, os.environ["ANTHROPIC_API_KEY"]).get("result"))
        print(sandbox.commands.run("ls -la /home/user/work").stdout)
