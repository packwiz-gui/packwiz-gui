import sys
import wget
import os
import socket
import re
from platform import system
from urllib.request import urlopen

"""
Fabric packwiz server installer pack for packwiz-gui
"""

def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

# Just a bunch of setup stuff
PLATFORM = None
SHELL = None
UNIXTYPE = None
ROOT = os.getcwd()
PACKWIZ_BINARY = None
INSTANCES_DIR = f'{ROOT}/../instances/'
fabric_installer_version = None
fabric_loader_version = None
pack_name = None
minecraft_version = None
system_ram = None
ip_addr = getPublicIp()




if system() == 'Windows':
    PLATFORM = 'Win'
    UNIXTYPE = 'Non-unix'
    PACKWIZ_BINARY = f'{ROOT}/bin/packwiz.exe'
elif system() == 'Linux':
    PLATFORM = 'Unix'
    UNIXTYPE = 'Linux'
    PACKWIZ_BINARY = f'{ROOT}/bin/packwiz'
elif system() == 'Darwin':
    PLATFORM = 'Unix'
    UNIXTYPE = 'macOS'
    PACKWIZ_BINARY = f'{ROOT}/bin/packwiz'

if PLATFORM == 'Win':
    os.system('title Fabric + packwiz installer script')

print("#######################################")
print("### FABRIC+PACKWIZ SERVER INSTALLER ###")
print("#######################################")

print("The below prompt will ask you some questions for the setup of the server. The value in [] is the recommended value, if you hit enter without specifying a version it will pass the recommended value.")

fabric_installer_version = input("Fabric installer version (NOT fabric loader) [0.10.2]: ")
if fabric_installer_version is None: 
    fabric_installer_version = '0.10.2'

pack_name = input("Pack name: ")
if pack_name is None:
    print('ERROR: Please specify a pack name')
    pack_name = input('Pack name: ')
    
minecraft_version = input("Minecraft version [1.18.1]: ")
if minecraft_version is None:
    minecraft_version = '1.18.1'

fabric_loader_version = input("Fabric loader version [0.12.12]: ")
if fabric_loader_version is None: 
    fabric_loader_version = '0.10.2'

system_ram = input('RAM to allocate to the minecraft server in MBs [4096]: ')
if system_ram is None:
    system_ram = 4096



print('Data provided:')
print(f'Fabric installer version: {fabric_installer_version}')
print(f'Pack name: {pack_name}')
print(f'Minecraft version: {minecraft_version}')
print(f'Fabric loader version: {fabric_loader_version}')



#*if prompt_return_code != 0:
#    confirmation = input("An error occured while running the prompt. Would you like to try again? [Y/n] ")
#    if confirmation == 'n' or 'N':
#        exit()
#    else:
#        prompt()
pack_root = f'{INSTANCES_DIR}/{pack_name}'
server_root = f'{pack_root}/server/'
if not os.path.exists(f'{server_root}'):
    os.makedirs(f'{server_root}')
os.chdir(pack_root)
os.system(f'{PACKWIZ_BINARY} serve')
os.chdir(server_root)
wget.download(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_installer_version}/fabric-installer-{fabric_installer_version}.jar", 'fabric-installer.jar')
wget.download(f'https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar')
wget.download(f'https://github.com/packwiz/packwiz-installer/releases/download/v0.3.2/packwiz-installer.jar')
os.system(f'java -jar installer.jar server -mcversion {minecraft_version} -downloadMinecraft')
startshfile = f"""
java -jar packwiz-installer.bootstrap.jar http://{ip_addr}:8080/pack.toml
java -Xmx{system_ram} -jar fabric-server-launch.jar
"""
if PLATFORM == 'Windows':
    with open("start.bat", "a", encoding="UTF-8") as f:
        f.write(startshfile)
elif PLATFORM == 'Unix':
    with open("start.sh", "a", encoding="UTF-8") as f:
        f.write(startshfile)
