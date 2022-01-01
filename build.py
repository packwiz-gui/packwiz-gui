#!/usr/bin/env python3

import os
import platform
import sys
import getopt
import shutil

try:
    opts, args = getopt.getopt(sys.argv[1:], "r", ["pyinstaller", "cxfreeze", "remove"])
    if opts == []:
        raise getopt.GetoptError("")
except getopt.GetoptError:
    print("Usage:")
    print("      --pyinstaller:      Compile with pyinstaller")
    print("      --cxfreeze:         Compile with cx_freeze")
    print("  -r, --remove:           Cleanup build directories")
    sys.exit()

if os.path.isdir(sys.path[0]):
    root = sys.path[0]
else:
    root = os.getcwd()

def compile(builder):
    if not os.path.isdir(f"{root}/{builder}"):
        os.mkdir(f"{root}/{builder}")
    os.chdir(f"{root}/{builder}")
    if not os.path.isfile(f"{root}/packwiz_gui.py"):
        print("packwiz_gui not found, exiting")
        sys.exit()
    if platform.system() == "Windows":
        print(f"Warning: windows detected. Make sure you have {builder} installed.")
        command = os.system(f"{builder} {root}\packwiz_gui.py")
    else:
        command = os.system(f"{builder} {root}/packwiz_gui.py")
    if command == 0:
        print(f"Successfully compiled packwiz-gui using {builder}!")
    elif platform.system() != "Windows" and command == 32512:
        print(f"Error: you do not have {builder} installed.")
    else:
        print(f"Error: error detected, code {command}.")

for opt, arg in opts:
    if opt == "--pyinstaller":
        compile("pyinstaller")
    elif opt == "--cxfreeze":
        compile("cxfreeze")
    elif opt in ("-r", "--remove"):
        if os.path.isdir(f"{root}/pyinstaller"):
            shutil.rmtree(f"{root}/pyinstaller")
            print("Removed pyinstaller directory")
        if os.path.isdir(f"{root}/cxfreeze"):
            shutil.rmtree(f"{root}/cxfreeze")
            print("Removed cxfreeze directory")
