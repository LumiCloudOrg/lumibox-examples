"""Score several candidate solutions at once, each in its own sandbox: the pattern of agent evals and RL rollouts.

    python parallel_eval.py
"""
import asyncio

from e2b import AsyncSandbox

# Candidates a model might have written for: def add(a, b)
CANDIDATES = {
    "correct": "def add(a, b):\n    return a + b\n",
    "off_by_one": "def add(a, b):\n    return a + b + 1\n",
    "crashes": "def add(a, b):\n    return a + undefined_name\n",
    "loops_forever": "def add(a, b):\n    while True:\n        pass\n",
}

TESTS = """
from solution import add
assert add(1, 2) == 3
assert add(-1, 1) == 0
print("passed")
"""


async def score(name: str, code: str) -> tuple[str, bool]:
    sandbox = await AsyncSandbox.create("base", timeout=120)
    try:
        await sandbox.files.write("/home/user/solution.py", code)
        await sandbox.files.write("/home/user/test_solution.py", TESTS)
        try:
            result = await sandbox.commands.run("python3 test_solution.py", cwd="/home/user", timeout=10)
            return name, result.stdout.strip() == "passed"
        except Exception:  # a non-zero exit or the timeout
            return name, False
    finally:
        await sandbox.kill()


async def main(candidates: dict[str, str] = CANDIDATES) -> dict[str, bool]:
    results = dict(await asyncio.gather(*(score(n, c) for n, c in candidates.items())))
    for name, passed in results.items():
        print(f"{name:15} {'pass' if passed else 'fail'}")
    return results


if __name__ == "__main__":
    asyncio.run(main())
