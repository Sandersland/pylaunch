import tkinter as tk
import sys

from pylaunch.roku.remote.controller import Controller
from pylaunch.roku import Roku


def main():
    args = sys.argv[1:]
    if args[0] == "init":
        sys.stdout.write("Initializing roku controller\n")
        c = Controller()
        c.run()
    elif args[0] == "discover":
        sys.stdout.write("Discovering devices...\n")
        devices = Roku.discover()
        sys.stdout.write("\n".join([repr(d) for d in devices]) + "\n")


if __name__ == "__main__":
    main()
