// Claude answers a question by writing Python that runs in a LumiBox sandbox (tool use + code interpreter).
//   export ANTHROPIC_API_KEY=...
//   node code-interpreter-claude.mjs "What is the 100th prime number?"
import Anthropic from "@anthropic-ai/sdk"
import { Sandbox } from "@e2b/code-interpreter"

const MODEL = process.env.ANTHROPIC_MODEL ?? "claude-haiku-5-5"

const tools = [
  {
    name: "run_python",
    description: "Run Python code in a Jupyter kernel and return its output. State is kept between calls.",
    input_schema: {
      type: "object",
      properties: { code: { type: "string", description: "The Python code to run" } },
      required: ["code"],
    },
  },
]

// The sandbox side of the tool: what the model gets back.
export async function runPython(sandbox, code) {
  const execution = await sandbox.runCode(code)
  let out = execution.logs.stdout.join("") + execution.logs.stderr.join("")
  if (execution.text) out += execution.text
  if (execution.error) out += `${execution.error.name}: ${execution.error.value}\n${execution.error.traceback}`
  return out || "(no output)"
}

export async function ask(question, sandbox, client = new Anthropic()) {
  const messages = [{ role: "user", content: question }]
  for (;;) {
    const response = await client.messages.create({ model: MODEL, max_tokens: 2048, tools, messages })
    messages.push({ role: "assistant", content: response.content })
    if (response.stop_reason !== "tool_use") {
      return response.content.filter((b) => b.type === "text").map((b) => b.text).join("")
    }
    const results = []
    for (const block of response.content) {
      if (block.type === "tool_use") {
        results.push({ type: "tool_result", tool_use_id: block.id, content: await runPython(sandbox, block.input.code) })
      }
    }
    messages.push({ role: "user", content: results })
  }
}

if (import.meta.main) {
  const sandbox = await Sandbox.create({ timeoutMs: 300_000 }) // the public template code-interpreter-v1
  try {
    console.log(await ask(process.argv[2] ?? "What is the 100th prime number? Compute it.", sandbox))
  } finally {
    await sandbox.kill()
  }
}
