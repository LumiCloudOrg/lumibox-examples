"""A Linux desktop in a sandbox (public template "desktop") for computer-use agents: screenshots, mouse,
keyboard and a live view in your browser. E2B's desktop SDK uses the template by default.

    pip install e2b-desktop
    python desktop.py
"""
import time

from e2b_desktop import Sandbox


def main():
    desktop = Sandbox.create(timeout=600)
    try:
        desktop.stream.start()
        print("watch it at", desktop.stream.get_url())
        desktop.launch("google-chrome")
        time.sleep(5)
        desktop.write("example.com\n")
        time.sleep(3)
        with open("desktop.png", "wb") as f:
            f.write(desktop.screenshot())
        print("screenshot in desktop.png")
        input("press Enter to end the sandbox ")
    finally:
        desktop.kill()


if __name__ == "__main__":
    main()
