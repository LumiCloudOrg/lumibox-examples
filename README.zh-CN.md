# LumiBox 示例

[English](README.md)

[LumiBox](https://lumicloud.ai) 的可运行示例。LumiBox 是位于新加坡的 AI agent 沙箱，提供 E2B 的 API：示例使用 E2B 官方 SDK，同一份代码设置两个环境变量即可在 LumiBox 上运行。

```sh
export E2B_DOMAIN=lumicloud.dev
export E2B_API_KEY=<LumiBox 密钥>   # console.lumicloud.ai → 沙箱 → API 密钥
```

已在 E2B 上运行的代码无需其他改动。见[从 E2B 迁移](https://lumicloud.ai/docs/migrate-from-e2b)。

## 示例

| 内容 | Python | JavaScript | 模板 |
|---|---|---|---|
| 运行命令、写文件、开放端口 | [quickstart.py](python/quickstart.py) | [quickstart.mjs](js/quickstart.mjs) | `base` |
| 暂停与恢复，保留内存和进程 | [pause_resume.py](python/pause_resume.py) | | `base` |
| Claude 工具调用 + 代码解释器 | [code_interpreter_claude.py](python/code_interpreter_claude.py) | [code-interpreter-claude.mjs](js/code-interpreter-claude.mjs) | `code-interpreter-v1` |
| OpenAI 函数调用 + 代码解释器 | [code_interpreter_openai.py](python/code_interpreter_openai.py) | | `code-interpreter-v1` |
| 在沙箱中运行 Claude Code | [claude_code.py](python/claude_code.py) | | `base` |
| 无头 Chromium，Playwright 经 CDP 控制 | [browser_playwright.py](python/browser_playwright.py) | [browser-playwright.mjs](js/browser-playwright.mjs) | `browser` |
| Linux 桌面，用于 computer use | [desktop.py](python/desktop.py) | | `desktop` |
| 并行评测，每个候选一个沙箱 | [parallel_eval.py](python/parallel_eval.py) | [parallel-eval.mjs](js/parallel-eval.mjs) | `base` |

以上模板均为公共模板，所有账户可直接按名称使用。

## 运行

Python 3.10 及以上：

```sh
cd python
pip install -r requirements.txt
python quickstart.py
```

Node.js 24 及以上：

```sh
cd js
npm install
node quickstart.mjs
```

调用模型的示例另需 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`。模型由 `ANTHROPIC_MODEL`（默认 `claude-haiku-5-5`）或 `OPENAI_MODEL`（默认 `gpt-5.5`）指定。

## 测试

`python/test_examples.py` 和 `js/test.mjs` 对 LumiBox 运行每个示例的沙箱部分。模型由返回固定工具调用的替身代替，测试只需 `E2B_DOMAIN` 和 `E2B_API_KEY`。测试每天在 LumiBox 生产环境运行。

```sh
cd python && pytest -v test_examples.py
cd js && npm test
```

## 说明

- 单一地区：新加坡。价格以美元计，从预付余额按秒扣费：[价格](https://lumicloud.ai/#pricing)。
- LumiBox 由 LUMI CLOUD PTE. LTD. 提供，与 E2B 公司无关。E2B SDK 依其 Apache-2.0 许可使用。

## 许可

MIT
