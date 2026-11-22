// Create a sandbox, run a command, write and read a file, serve a port.
//   node quickstart.mjs
import { Sandbox } from "e2b"

export async function main() {
  const sandbox = await Sandbox.create("base", { timeoutMs: 300_000 }) // ends by itself after 5 minutes
  try {
    const result = await sandbox.commands.run("python3 -c 'print(6 * 7)'")
    console.log(result.stdout.trim()) // 42

    await sandbox.files.write("/home/user/hello.txt", "hello from LumiBox\n")
    console.log((await sandbox.files.read("/home/user/hello.txt")).trim())

    await sandbox.commands.run("python3 -m http.server 8000", { background: true, cwd: "/home/user" })
    console.log(`serving at https://${sandbox.getHost(8000)}/hello.txt`)
  } finally {
    await sandbox.kill()
  }
}

if (import.meta.main) await main()
