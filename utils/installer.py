#!/usr/bin/env python3

"""
Fabric packwiz server installer pack for packwiz-gui
"""

import os
import sys
import platform
import threading
import subprocess
import http.server
import socketserver
import requests
import tomli

def opentoml(filename):
    """
    Open toml file. Returns dict.
    Args:
    filename: filename of file (with path) to open
    """
    with open(filename, "rb") as toml_file:
        return tomli.load(toml_file)

def continueorno():
    while True:
        useraccept = input("Continue? (Y/n) ")
        if useraccept in ("y", ""):
            return "y"
        elif useraccept == "n":
            sys.exit(1)
        else:
            print("Error: Invalid input!")

def main():
    # Just a bunch of setup stuff
    root = os.getcwd()
    while not os.path.isfile(f"{root}/packwiz_gui.py"):
        os.chdir("..")
        root = os.getcwd()
    instances = f"{root}/instances"

    if platform.system() == "Windows":
        osys = "Win"
        os.system("title Fabric + packwiz installer script")
    else:
        osys = "Unix"

    print("")
    print("#######################################")
    print("### FABRIC+PACKWIZ SERVER INSTALLER ###")
    print("#######################################")
    print("")
    print("The below prompt will ask you some questions for the setup of the server. The value in [] is the recommended value.")
    print("If you hit enter without specifying a version it will pass the recommended value.")
    print("Warning: this script only works for fabric.")
    print("")
    continueorno()

    pack_name = ""
    while pack_name == "" or not os.path.isfile(f"{instances}/{pack_name}/pack.toml"):
        pack_name = input("Pack name: ")
        if pack_name == "":
            print("Error: Please specify a pack name!")
        elif not os.path.isfile(f"{instances}/{pack_name}/pack.toml"):
            print("Error: please enter a valid pack!")

    while True:
        system_ram = input("RAM to allocate to the minecraft server in MBs [4096]: ")
        if system_ram == "":
            system_ram = "4096"
            break
        try:
            int(system_ram)
            break
        except ValueError:
            print("Error: Ram must be a number (No K/M/G at the end either)!")

    pack_toml = opentoml(f"{instances}/{pack_name}/pack.toml")

    minecraft_version = pack_toml["versions"]["minecraft"]
    fabric_version = pack_toml["versions"]["fabric"]

    # Print all the data provided (plus data from pack.toml)

    print("")
    print("Data provided:")
    print(f"Pack name: {pack_name}")
    print(f"RAM to allocate: {system_ram}")
    print(f"Minecraft version: {minecraft_version}")
    print("")
    continueorno()

    pack_root = f"{instances}/{pack_name}"
    server_root = f"{pack_root}/server"
    if not os.path.exists(f"{server_root}"):
        os.makedirs(f"{server_root}")

    # Just running a serve_forever so that packwiz-installer can download files. packwiz serve doesn't work for whatever reason meh
        
    def runserver():
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=pack_root, **kwargs)
        with socketserver.TCPServer(("", 8080), Handler) as httpd:
            httpd.serve_forever()
    serve_thread  = threading.Thread(target=runserver)
    serve_thread.setDaemon(True)
    serve_thread.start()

    # Start installing server stuff in pack_root/server

    os.chdir(server_root)
    with open("fabric-installer.jar", "wb") as loader_installer:
        loader_installer_url = requests.get("https://meta.fabricmc.net/v2/versions/installer").json()[0]["url"]
        loader_installer.write(requests.get(loader_installer_url).content)
    with open("packwiz-installer-bootstrap.jar", "wb") as packwiz_bootstrap:
        packwiz_bootstrap.write(
                                requests.get(
                                            "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar").content)
    subprocess.run(["java", "-jar", "fabric-installer.jar", "server", "-mcversion", minecraft_version, "-loader", fabric_version, "-downloadMinecraft"], check=True)
    subprocess.run(["java", "-jar", "packwiz-installer-bootstrap.jar", "http://localhost:8080/pack.toml"], check=True)
    os.remove("fabric-installer.jar")

    # Create start.sh/start.bat file

    startshfile = f"java -Xms{str(int(int(system_ram) / 4))}M -Xmx{system_ram}M -jar fabric-server-launch.jar nogui"
    with open("start.bat", "a", encoding="UTF-8") as startscript:
        startscript.write(startshfile)
    with open("start.sh", "a", encoding="UTF-8") as startscript:
        startscript.write(startshfile)
    if osys == "Unix":
        subprocess.run(["chmod", "+x", "start.sh"], check=False)

    print("")
    print(f"Done! Server created in {server_root}!")
    print("Use start.bat (Windows) or start.sh (Linux/MacOS) to start the server.")
    print("Make sure to agree to the EULA in eula.txt.")
    print("You do need to run it through a command prompt.")

if __name__ == "__main__":
    main()
