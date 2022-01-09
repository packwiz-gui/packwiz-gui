#!/usr/bin/env python3

"""
Fabric packwiz server installer pack for packwiz-gui
"""

import os
import platform
import threading
import subprocess
import http.server
import socketserver
import tomli
import wget

def opentoml(filename):
    """
    Open toml file. Returns dict.
    Args:
    filename: filename of file (with path) to open
    """
    with open(filename, "rb") as toml_file:
        return tomli.load(toml_file)

def main():
    # Just a bunch of setup stuff
    root = f"{os.getcwd()}"
    while not os.path.isfile(f"{root}/packwiz_gui.py"):
        os.chdir("..")
        root = os.getcwd()
    instances = f"{root}/instances"
    fabric_installer_version = None
    fabric_loader_version = None
    pack_name = None
    minecraft_version = None
    system_ram = None

    if platform.system() == "Windows":
        osys = "Win"
        os.system("title Fabric + packwiz installer script")
    else:
        osys = "Unix"

    print("#######################################")
    print("### FABRIC+PACKWIZ SERVER INSTALLER ###")
    print("#######################################")

    print("The below prompt will ask you some questions for the setup of the server. The value in [] is the recommended value, if you hit enter without specifying a version it will pass the recommended value.")

    while pack_name in ("", None) or not os.path.isfile(f"{instances}/{pack_name}/pack.toml"):
        pack_name = input("Pack name: ")
        if pack_name == "":
            print("Error: Please specify a pack name!")
        elif not os.path.isfile(f"{instances}/{pack_name}/pack.toml"):
            print("Error: please enter a valid pack!")

    fabric_installer_version = input("Fabric installer version (NOT fabric loader) [0.10.2]: ")
    if fabric_installer_version == "":
        fabric_installer_version = "0.10.2"

    system_ram = input("RAM to allocate to the minecraft server in MBs [4096]: ")
    if system_ram == "":
        system_ram = "4096"

    pack_toml = opentoml(f"{instances}/{pack_name}/pack.toml")

    minecraft_version = pack_toml["versions"]["minecraft"]

    print("")
    print("Data provided:")
    print(f"Pack name: {pack_name}")
    print(f"Fabric installer version: {fabric_installer_version}")
    print(f"RAM to allocate: {system_ram}")
    print("")

    pack_root = f"{instances}/{pack_name}"
    server_root = f"{pack_root}/server"
    if not os.path.exists(f"{server_root}"):
        os.makedirs(f"{server_root}")

    def runserver():
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=pack_root, **kwargs)
        with socketserver.TCPServer(("", 8080), Handler) as httpd:
            httpd.serve_forever()
    serve_thread  = threading.Thread(target=runserver)
    serve_thread.setDaemon(True)
    serve_thread.start()

    os.chdir(server_root)

    wget.download(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_installer_version}/fabric-installer-{fabric_installer_version}.jar", 'fabric-installer.jar')
    wget.download("https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar")
    subprocess.run(["java", "-jar", "fabric-installer.jar", "server", "-mcversion", minecraft_version, "-downloadMinecraft"], check=True)
    subprocess.run(["java", "-jar", "packwiz-installer-bootstrap.jar", "http://localhost:8080/pack.toml"], check=True)

    startshfile = f"java -Xms{str(int(int(system_ram) / 4))}M -Xmx{system_ram}M -jar fabric-server-launch.jar"
    with open("start.bat", "a", encoding="UTF-8") as startscript:
        startscript.write(startshfile)
    with open("start.sh", "a", encoding="UTF-8") as startscript:
        startscript.write(startshfile)
    if osys == "Unix":
        subprocess.run(["chmod", "+x", "start.sh"], check=True)

if __name__ == "__main__":
    main()
