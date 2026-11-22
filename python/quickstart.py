"""Create a sandbox, run a command, upload and read a file, serve a port.

    python quickstart.py
"""
from e2b import Sandbox


def main():
    with Sandbox.create("base", timeout=300) as sandbox:  # ends by itself after 300 seconds
        print(sandbox.commands.run("python3 -c 'print(6 * 7)'").stdout.strip())  # 42

        sandbox.files.write("/home/user/hello.txt", "hello from LumiBox\n")
        print(sandbox.files.read("/home/user/hello.txt").strip())

        sandbox.commands.run("python3 -m http.server 8000", background=True, cwd="/home/user")
        print("serving at https://" + sandbox.get_host(8000) + "/hello.txt")


if __name__ == "__main__":
    main()
