#!/usr/bin/env python3

"""
build.py is a simple script which can install dependencies or compile the script with pyinstaller/cxfreeze.
"""

import os
import platform
import sys
import getopt
import shutil

def main():
    """
    Main function.
    """

    python = "python" if platform.system() == "Windows" else "python3"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "r", ["deps", "deps-nobuild", "pyinstaller", "cxfreeze", "remove"])
        if opts == []:
            raise getopt.GetoptError("")
    except getopt.GetoptError:
        print("Usage:")
        print("      --deps:            Install all non-compiling related dependencies (dependencies required to run the script).")
        print("      --deps-nobuild:    Install required dependencies to start compiling or running the script.")
        print("      --pyinstaller:     Compile with pyinstaller. Stores in pyinstaller directory.")
        print("      --cxfreeze:        Compile with cx_freeze. Stores in cxfreeze firectory.")
        print("  -r, --remove:          Cleans up build directories")
        sys.exit(1)

    if len(opts) > 1:
        raise getopt.GetoptError("Cannot have more than 1 option.")

    root = f'{sys.path[0]}/..' if os.path.isdir(f'{sys.path[0]}/..') else f'{os.getcwd()}/..'

    def compilewith(builder):
        """
        Compile function. args: builder
        """
        if not os.path.isfile(f"{root}/packwiz_gui.py"):
            print("packwiz_gui not found, exiting")
            sys.exit(1)
        if not os.path.isdir(f"{root}/{builder}"):
            os.mkdir(f"{root}/{builder}")
        os.chdir(f"{root}/{builder}")
        if platform.system() == "Windows":
            print(f"Warning: windows detected. Make sure you have {builder} installed.")
            command = os.system(f"{builder} {root}\\packwiz_gui.py")
        else:
            command = os.system(f"{builder} {root}/packwiz_gui.py")
        if command == 0:
            print(f"Successfully compiled packwiz-gui using {builder}!")
        elif platform.system() != "Windows" and command == 32512:
            print(f"Error: you do not have {builder} installed.")
        else:
            print(f"Error: error detected, code {command}.")
        sys.exit(command)

    for opt, arg in opts:
        if opt == "--deps":
            os.system(f"{python} -m pip install -r {root}/requirements.txt")
        if opt == "--deps-nobuild":
            os.system(f"{python} -m pip install -r {root}/requirements-nobuild.txt")
        elif opt == "--pyinstaller":
            compilewith("pyinstaller")
        elif opt == "--cxfreeze":
            compilewith("cxfreeze")
        elif opt in ("-r", "--remove"):
            if os.path.isdir(f"{root}/pyinstaller"):
                shutil.rmtree(f"{root}/pyinstaller")
                print("Removed pyinstaller directory")
            if os.path.isdir(f"{root}/cxfreeze"):
                shutil.rmtree(f"{root}/cxfreeze")
                print("Removed cxfreeze directory")

if __name__ == "__main__":
    main()
