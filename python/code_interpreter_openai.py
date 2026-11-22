"""An OpenAI model answers a question by writing Python that runs in a LumiBox sandbox (function calling, Responses API).

    export OPENAI_API_KEY=...
    python code_interpreter_openai.py "What is the 100th prime number?"
"""
import json
import os
import sys

from e2b_code_interpreter import Sandbox
from openai import OpenAI

from code_interpreter_claude import run_python

MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.5")

TOOLS = [
    {
        "type": "function",
        "name": "run_python",
        "description": "Run Python code in a Jupyter kernel and return its output. State is kept between calls.",
        "parameters": {
            "type": "object",
            "properties": {"code": {"type": "string", "description": "The Python code to run"}},
            "required": ["code"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def ask(question: str, sandbox: Sandbox, client=None) -> str:
    client = client or OpenAI()
    items = [{"role": "user", "content": question}]
    while True:
        response = client.responses.create(model=MODEL, tools=TOOLS, input=items)
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text
        items += response.output
        for call in calls:
            code = json.loads(call.arguments)["code"]
            items.append({"type": "function_call_output", "call_id": call.call_id, "output": run_python(sandbox, code)})


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the 100th prime number? Compute it."
    with Sandbox.create(timeout=300) as sandbox:
        print(ask(question, sandbox))
