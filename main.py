#!/bin/env python3
import PySimpleGUI as sg
import os
import platform
from subprocess import PIPE, Popen

root = os.getcwd()
sg.theme("DarkGrey9") 
right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT  # Add a touch of color
# All the stuff inside your window.
instances_list = ""
main_menu = [
                [sg.Text("")],
                [sg.Button("Create a new pack")],
                [sg.Text("")],
                [sg.Button("Open an existing pack")],
                [sg.Text("")]
                ]

pack_create = [
              [sg.Text("Pack name:"), sg.InputText()],
              [sg.Text("Author:"), sg.InputText()],
              [sg.Text("Pack Version:"), sg.InputText()],
              [sg.Text("Minecraft Version:"), sg.InputText()],
              [sg.Text("Modloader"), sg.Combo(["forge", "fabric"])],
              [sg.Text("Modloader Version:"), sg.InputText()],
              [sg.Button("Create")],
              [sg.Text("")],
              ]

pack_edit = [
            [sg.Text("Source:"), sg.Combo(["modrinth", "curseforge"])],
            [sg.Text("Mod ID: "), sg.InputText()],
            [sg.Button("Add Mod")],
            [sg.Text("")],
            ]

pack_list = [
            [sg.Text(instances_list)]
            ]


if platform.system() == 'Darwin' or 'Linux':
    linux = True
    windows = False
if platform.system() == 'Windows':
    windows = True
    linux = False
# Create the Window
window = sg.Window("Main Menu", main_menu)

if platform.system() == "Windows":
    packwiz = f"{root}\\bin\\packwiz.exe"
elif platform.system() == "Darwin" or "Linux":
    packwiz = f"{root}/bin/packwiz"
    os.system(f"chmod +x {packwiz}")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel": # if user closes window or clicks cancel
        break
    if event == "Create":

        name = values[0]
        author = values[1]
        pack_version = values[2]
        mc_version = values[3]
        modloader = values[4]
        modloader_version = values[5]

        os.mkdir(f"instances/{name}_pack")
        os.chdir(f"instances/{name}_pack")
        os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")
        
        window = sg.Window("Editing Pack", pack_edit)
            
    if event == "Add Mod":
        source_type = values[0]
        mod_url = values[1]
        os.chdir(f"{root}/instances/{name}")
        os.system(f"{packwiz} {source_type} install {mod_url}")
    
    if event == "Create a new pack":
        window = sg.Window("Creating a new pack", pack_create)
        
    if event == "Open an existing pack":
        if windows == True:
            command = f"cmd.exe dir"
            command2 = f""
        elif linux == True:
            command = f"ls"
            #command2 =  f"| awk {'print $9'}"
            command2 = f"| grep _pack"

        #status, output = commands.getstatusoutput(f"{command} {root}/instances")
        cmd = f"{command} {root}/instances/ {command2}"
        process = Popen(
        args=cmd,
        stdout=PIPE,
        stderr=PIPE,
        shell=True)
            
        instances_list = process.stdout.read()[:-6]
        pack_list = [
                    [sg.Text(instances_list.decode("utf-8"))]
                    ]
        print(process.stdout.read())
        window = sg.Window("Listing existing packs", pack_list)


window.close()
