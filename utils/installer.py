#!/usr/bin/env python3

import sys
import wget
import os
import socket
import re
import platform
from urllib.request import urlopen
import tomli
import threading
import tomli_w
import subprocess

"""
Fabric packwiz server installer pack for packwiz-gui
"""
def opentoml(filename):
    """
    Open toml file. Returns dict.
    Args:
    filename; filename of file (with path) to open
    """
    with open(filename, "rb") as toml_file:
        return tomli.load(toml_file)

# Just a bunch of setup stuff
PLATFORM = None
SHELL = None
UNIXTYPE = None
ROOT = f"{os.getcwd()}/.."
PACKWIZ_BINARY = f"{ROOT}/bin/packwiz.exe" if platform.system() == "Windows" else f"{ROOT}/bin/packwiz"
INSTANCES_DIR = f"{ROOT}/instances/"
fabric_installer_version = None
fabric_loader_version = None
pack_name = None
minecraft_version = None
system_ram = None
SHELL = None

if platform.system() == "Windows":
    PLATFORM = "Win"
    UNIXTYPE = "Non-unix"
elif platform.system() == "Linux":
    PLATFORM = "Unix"
    UNIXTYPE = "Linux"
elif platform.system() == "Darwin":
    PLATFORM = "Unix"
    UNIXTYPE = "macOS"

if PLATFORM == "Win":
    os.system("title Fabric + packwiz installer script")

print("#######################################")
print("### FABRIC+PACKWIZ SERVER INSTALLER ###")
print("#######################################")

print("The below prompt will ask you some questions for the setup of the server. The value in [] is the recommended value, if you hit enter without specifying a version it will pass the recommended value.")

fabric_installer_version = input("Fabric installer version (NOT fabric loader) [0.10.2]: ")
if fabric_installer_version == "": 
    fabric_installer_version = "0.10.2"

pack_name = None
while pack_name in ("", None):
    pack_name = input("Pack name: ")
    if pack_name == "":
        print("Error: Please specify a pack name!")
    
minecraft_version = input("Minecraft version [1.18.1]: ")
if minecraft_version == "":
    minecraft_version = "1.18.1"

fabric_loader_version = input("Fabric loader version [0.12.12]: ")
if fabric_loader_version == "": 
    fabric_loader_version = "0.12.12"

system_ram = input("RAM to allocate to the minecraft server in MBs [4096]: ")
if system_ram == "":
    system_ram = "4096"

print("")
print("Data provided:")
print(f"Fabric installer version: {fabric_installer_version}")
print(f"Pack name: {pack_name}")
print(f"Minecraft version: {minecraft_version}")
print(f"Fabric loader version: {fabric_loader_version}")

pack_root = f"{INSTANCES_DIR}/{pack_name}"
server_root = f"{pack_root}/server/"
if not os.path.exists(f"{server_root}"):
    os.makedirs(f"{server_root}")
os.chdir(pack_root)
packwiz_serve_run = [PACKWIZ_BINARY, "serve"]
serve_thread  = threading.Thread(target=subprocess.run, args=(packwiz_serve_run,), daemon=True)
serve_thread.start()
os.chdir(server_root)
installer_jar_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_installer_version}/fabric-installer-{fabric_installer_version}.jar"
print(installer_jar_url)
wget.download(installer_jar_url, "fabric-installer.jar")
wget.download(f"https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar")
wget.download(f"https://github.com/packwiz/packwiz-installer/releases/download/v0.3.2/packwiz-installer.jar")

os.system(f"java -jar fabric-installer.jar server -mcversion {minecraft_version} -downloadMinecraft")
os.system(f"java -jar packwiz-installer-bootstrap.jar http://localhost:8080/pack.toml")
startshfile = f"java -Xms{str(int(system_ram) / 4)}M -Xmx{system_ram}M -jar fabric-server-launch.jar"
if PLATFORM == "Windows":
    with open("start.bat", "a", encoding="UTF-8") as f:
        f.write(startshfile)
elif PLATFORM == "Unix":
    with open("start.sh", "a", encoding="UTF-8") as f:
        f.write(startshfile)
sys.exit()
