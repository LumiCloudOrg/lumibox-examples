"""The examples' sandbox side, against a real LumiBox (E2B_DOMAIN, E2B_API_KEY). Models are replaced by fakes that
return a fixed tool call, so no model key is needed.

    pytest -v test_examples.py
"""
import asyncio
import json
from types import SimpleNamespace as NS

import pytest
from e2b import Sandbox
from e2b_code_interpreter import Sandbox as CodeSandbox

import claude_code
import code_interpreter_claude
import code_interpreter_openai
import parallel_eval
import browser_playwright

CODE = "import math\nprint(sum(1 for n in range(2, 1000) if all(n % d for d in range(2, math.isqrt(n) + 1))))"


def test_quickstart(capsys):
    import quickstart

    quickstart.main()
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "42" and out[1] == "hello from LumiBox"


def test_pause_resume(capsys):
    import pause_resume

    pause_resume.main()
    out = capsys.readouterr().out
    assert "state before pause" in out and "sleep still running: yes" in out


class FakeClaude:
    """Asks for one run_python call, then answers with what it got back."""

    def __init__(self):
        self.messages = NS(create=self.create)
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        if self.calls == 1:
            return NS(stop_reason="tool_use", content=[NS(type="tool_use", id="t1", name="run_python", input={"code": CODE})])
        result = kw["messages"][-1]["content"][0]
        assert result["type"] == "tool_result" and result["tool_use_id"] == "t1"
        return NS(stop_reason="end_turn", content=[NS(type="text", text=result["content"].strip())])


class FakeOpenAI:
    def __init__(self):
        self.responses = NS(create=self.create)
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        if self.calls == 1:
            call = NS(type="function_call", call_id="c1", name="run_python", arguments=json.dumps({"code": CODE}))
            return NS(output=[call], output_text="")
        out = kw["input"][-1]
        assert out["type"] == "function_call_output" and out["call_id"] == "c1"
        return NS(output=[NS(type="message")], output_text=out["output"].strip())


@pytest.fixture(scope="module")
def code_sandbox():
    with CodeSandbox.create(timeout=300) as s:
        yield s


def test_run_python_output_and_errors(code_sandbox):
    assert code_interpreter_claude.run_python(code_sandbox, "x = 41\nprint(x + 1)").strip() == "42"
    assert code_interpreter_claude.run_python(code_sandbox, "x * 2").strip() == "82"  # state is kept
    assert "ZeroDivisionError" in code_interpreter_claude.run_python(code_sandbox, "1 / 0")


def test_claude_tool_loop(code_sandbox):
    assert code_interpreter_claude.ask("how many primes below 1000?", code_sandbox, FakeClaude()) == "168"


def test_openai_tool_loop(code_sandbox):
    assert code_interpreter_openai.ask("how many primes below 1000?", code_sandbox, FakeOpenAI()) == "168"


def test_claude_code_installs():
    with Sandbox.create("base", timeout=600) as s:
        assert "Claude Code" in claude_code.install(s)


def test_parallel_eval(capsys):
    results = asyncio.run(parallel_eval.main())
    assert results == {"correct": True, "off_by_one": False, "crashes": False, "loops_forever": False}


def test_browser(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with Sandbox.create("browser", timeout=300) as s:
        assert browser_playwright.title_of(s, "https://example.com") == "Example Domain"
    assert (tmp_path / "page.png").stat().st_size > 1000


def test_desktop():
    from e2b_desktop import Sandbox as Desktop

    d = Desktop.create(timeout=300)
    try:
        assert d.screenshot()[:8] == b"\x89PNG\r\n\x1a\n"
        d.stream.start()
        assert d.stream.get_url().startswith("https://")
    finally:
        d.kill()


def test_package_managers():
    """npm and pip in the base template install from their registries (whatever the template points them at)."""
    with Sandbox.create("base", timeout=300) as s:
        s.commands.run("cd /tmp && npm install --no-audit --no-fund express", timeout=180)
        s.commands.run("pip install --user six", timeout=180)
        assert s.commands.run("python3 -c 'import six; print(six.__version__)'").stdout.strip()
        assert s.commands.run("node -e \"require('/tmp/node_modules/express'); console.log('ok')\"").stdout.strip() == "ok"
