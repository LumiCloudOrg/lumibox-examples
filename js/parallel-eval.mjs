// Score several candidate solutions at once, each in its own sandbox: the pattern of agent evals and RL rollouts.
//   node parallel-eval.mjs
import { Sandbox } from "e2b"

// Candidates a model might have written for: def add(a, b)
export const candidates = {
  correct: "def add(a, b):\n    return a + b\n",
  off_by_one: "def add(a, b):\n    return a + b + 1\n",
  crashes: "def add(a, b):\n    return a + undefined_name\n",
  loops_forever: "def add(a, b):\n    while True:\n        pass\n",
}

const tests = `
from solution import add
assert add(1, 2) == 3
assert add(-1, 1) == 0
print("passed")
`

async function score(code) {
  const sandbox = await Sandbox.create("base", { timeoutMs: 120_000 })
  try {
    await sandbox.files.write("/home/user/solution.py", code)
    await sandbox.files.write("/home/user/test_solution.py", tests)
    try {
      const result = await sandbox.commands.run("python3 test_solution.py", { cwd: "/home/user", timeoutMs: 10_000 })
      return result.stdout.trim() === "passed"
    } catch {
      return false // a non-zero exit or the timeout
    }
  } finally {
    await sandbox.kill()
  }
}

export async function main() {
  const names = Object.keys(candidates)
  const passed = await Promise.all(names.map((n) => score(candidates[n])))
  const results = Object.fromEntries(names.map((n, i) => [n, passed[i]]))
  for (const [name, ok] of Object.entries(results)) console.log(name.padEnd(15), ok ? "pass" : "fail")
  return results
}

if (import.meta.main) await main()
