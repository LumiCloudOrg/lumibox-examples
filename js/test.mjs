// The examples' sandbox side, against a real LumiBox (E2B_DOMAIN, E2B_API_KEY). The model is replaced by a fake that
// returns a fixed tool call, so no model key is needed.
//   npm test
import assert from "node:assert/strict"
import { mkdtempSync, statSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { test } from "node:test"
import { Sandbox as CodeSandbox } from "@e2b/code-interpreter"
import { Sandbox as Desktop } from "@e2b/desktop"
import { Sandbox } from "e2b"
import { titleOf } from "./browser-playwright.mjs"
import { ask, runPython } from "./code-interpreter-claude.mjs"
import { main as parallelEval } from "./parallel-eval.mjs"
import { main as quickstart } from "./quickstart.mjs"

const CODE = "import math\nprint(sum(1 for n in range(2, 1000) if all(n % d for d in range(2, math.isqrt(n) + 1))))"
const skipCodeInterpreter = process.env.SKIP_CODE_INTERPRETER === "1"

test("quickstart", async () => {
  await quickstart()
})

test("code interpreter and the Claude tool loop", { skip: skipCodeInterpreter }, async () => {
  const sandbox = await CodeSandbox.create({ timeoutMs: 300_000 })
  try {
    assert.equal((await runPython(sandbox, "x = 41\nprint(x + 1)")).trim(), "42")
    assert.match(await runPython(sandbox, "1 / 0"), /ZeroDivisionError/)
    let calls = 0
    const fake = {
      messages: {
        create: async ({ messages }) => {
          if (++calls === 1) {
            return { stop_reason: "tool_use", content: [{ type: "tool_use", id: "t1", name: "run_python", input: { code: CODE } }] }
          }
          const r = messages.at(-1).content[0]
          assert.equal(r.tool_use_id, "t1")
          return { stop_reason: "end_turn", content: [{ type: "text", text: r.content.trim() }] }
        },
      },
    }
    assert.equal(await ask("how many primes below 1000?", sandbox, fake), "168")
  } finally {
    await sandbox.kill()
  }
})

test("parallel eval", async () => {
  assert.deepEqual(await parallelEval(), { correct: true, off_by_one: false, crashes: false, loops_forever: false })
})

test("browser", async () => {
  const dir = mkdtempSync(join(tmpdir(), "lumibox-"))
  process.chdir(dir)
  const sandbox = await Sandbox.create("browser", { timeoutMs: 300_000 })
  try {
    assert.equal(await titleOf(sandbox, "https://example.com"), "Example Domain")
  } finally {
    await sandbox.kill()
  }
  assert.ok(statSync(join(dir, "page.png")).size > 1000)
})

test("desktop", async () => {
  const desktop = await Desktop.create({ timeoutMs: 300_000 })
  try {
    const png = await desktop.screenshot()
    assert.deepEqual([...png.slice(0, 4)], [0x89, 0x50, 0x4e, 0x47])
    await desktop.stream.start()
    assert.match(desktop.stream.getUrl(), /^https:\/\//)
  } finally {
    await desktop.kill()
  }
})
