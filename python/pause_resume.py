"""Pause a sandbox and resume it later: memory, files and running processes are kept.
A paused sandbox is not charged for running, only for the storage of its snapshot.

    python pause_resume.py
"""
from e2b import Sandbox


def main():
    sandbox = Sandbox.create("base", timeout=300)
    sandbox.commands.run("echo 'state before pause' > /home/user/state.txt")
    sandbox.commands.run("sleep 3600", background=True)  # a process that keeps running
    sandbox_id = sandbox.sandbox_id
    sandbox.pause()
    print("paused", sandbox_id)

    sandbox = Sandbox.connect(sandbox_id, timeout=300)  # resumes it
    print(sandbox.files.read("/home/user/state.txt").strip())
    print("sleep still running:", sandbox.commands.run("pgrep -x sleep >/dev/null && echo yes || echo no").stdout.strip())
    sandbox.kill()


if __name__ == "__main__":
    main()
