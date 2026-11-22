# LumiBox examples

[中文](README.zh-CN.md)

Runnable examples for [LumiBox](https://lumicloud.ai), sandboxes for AI agents in Singapore. LumiBox serves the E2B API: the examples use E2B's own SDKs, and the same code runs on LumiBox with two environment variables.

```sh
export E2B_DOMAIN=lumicloud.dev
export E2B_API_KEY=<your LumiBox key>   # console.lumicloud.ai → Sandbox → API keys
```

Code that already runs on E2B needs no other change. See [Migrating from E2B](https://lumicloud.ai/docs/migrate-from-e2b).

## Examples

| Example | Python | JavaScript | Template |
|---|---|---|---|
| Run a command, write a file, serve a port | [quickstart.py](python/quickstart.py) | [quickstart.mjs](js/quickstart.mjs) | `base` |
| Pause and resume with memory and processes kept | [pause_resume.py](python/pause_resume.py) | | `base` |
| Claude tool use with a code interpreter | [code_interpreter_claude.py](python/code_interpreter_claude.py) | [code-interpreter-claude.mjs](js/code-interpreter-claude.mjs) | `code-interpreter-v1` |
| OpenAI function calling with a code interpreter | [code_interpreter_openai.py](python/code_interpreter_openai.py) | | `code-interpreter-v1` |
| Claude Code inside a sandbox | [claude_code.py](python/claude_code.py) | | `base` |
| Headless Chromium with Playwright over CDP | [browser_playwright.py](python/browser_playwright.py) | [browser-playwright.mjs](js/browser-playwright.mjs) | `browser` |
| Linux desktop for computer use | [desktop.py](python/desktop.py) | | `desktop` |
| Parallel evaluation, one sandbox per candidate | [parallel_eval.py](python/parallel_eval.py) | [parallel-eval.mjs](js/parallel-eval.mjs) | `base` |

All templates above are public: every account can use them by name.

## Running

Python 3.10 or later:

```sh
cd python
pip install -r requirements.txt
python quickstart.py
```

Node.js 24 or later:

```sh
cd js
npm install
node quickstart.mjs
```

The examples that call a model also need `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`. The model is set with `ANTHROPIC_MODEL` (default `claude-haiku-5-5`) or `OPENAI_MODEL` (default `gpt-5.5`).

## Tests

`python/test_examples.py` and `js/test.mjs` run every example's sandbox side against LumiBox. The model is replaced by a fake that returns a fixed tool call, so the tests need only `E2B_DOMAIN` and `E2B_API_KEY`. They run against LumiBox production every day.

```sh
cd python && pytest -v test_examples.py
cd js && npm test
```

## Notes

- One region: Singapore. Prices are in Singapore dollars, charged by the second from a prepaid balance: [pricing](https://lumicloud.ai/#pricing).
- LumiBox is a service of LUMI CLOUD PTE. LTD. and is not affiliated with E2B. E2B's SDKs are used under their Apache-2.0 license.

## License

MIT
