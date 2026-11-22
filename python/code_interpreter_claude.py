"""Claude answers a question by writing Python that runs in a LumiBox sandbox (tool use + code interpreter).

    export ANTHROPIC_API_KEY=...
    python code_interpreter_claude.py "What is the 100th prime number?"
"""
import os
import sys

import anthropic
from e2b_code_interpreter import Sandbox

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")

TOOLS = [
    {
        "name": "run_python",
        "description": "Run Python code in a Jupyter kernel and return its output. State is kept between calls.",
        "input_schema": {
            "type": "object",
            "properties": {"code": {"type": "string", "description": "The Python code to run"}},
            "required": ["code"],
        },
    }
]


def run_python(sandbox: Sandbox, code: str) -> str:
    """The sandbox side of the tool: what the model gets back."""
    execution = sandbox.run_code(code)
    out = "".join(execution.logs.stdout) + "".join(execution.logs.stderr)
    if execution.text:
        out += execution.text
    if execution.error:
        out += f"{execution.error.name}: {execution.error.value}\n{execution.error.traceback}"
    return out or "(no output)"


def ask(question: str, sandbox: Sandbox, client=None) -> str:
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(model=MODEL, max_tokens=2048, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return "".join(block.text for block in response.content if block.type == "text")
        results = [
            {"type": "tool_result", "tool_use_id": block.id, "content": run_python(sandbox, block.input["code"])}
            for block in response.content
            if block.type == "tool_use"
        ]
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the 100th prime number? Compute it."
    with Sandbox.create(timeout=300) as sandbox:  # the public template code-interpreter-v1
        print(ask(question, sandbox))
