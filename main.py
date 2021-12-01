#!/bin/env python3
import PySimpleGUI as sg
import os
import platform
import subprocess

root = os.getcwd()
sg.theme("DarkGrey9")   # Add a touch of color
# All the stuff inside your window.
main_menu = [
            [sg.Button("Create a new pack")],
            [sg.Button("Open an existing pack")]
            ]
pack_create = [
            [sg.Text("Pack name:"), sg.InputText()],
            [sg.Text("Author:"), sg.InputText()],
            [sg.Text("Pack Version:"), sg.InputText()],
            [sg.Text("Minecraft Version:"), sg.InputText()],
            [sg.Text("Modloader"), sg.Combo(["forge", "fabric"])],
            [sg.Text("Modloader Version:"), sg.InputText()],
            [sg.Button("Create")]
            ]

pack_edit = [
            [sg.Text("Source:"), sg.Combo(["modrinth", "curseforge"])],
            [sg.Text("Mod ID: "), sg.InputText()],
            [sg.Button("Add Mod")]
            ]

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

        os.mkdir(f"instances/{name}")
        os.chdir(f"instances/{name}")
        os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")

        window = sg.Window("Editing Pack", pack_edit)
            
    if event == "Add Mod":
        source_type = values[0]
        mod_url = values[1]
        os.chdir(f"{root}/instances/{name}")
        os.system(f"{packwiz} {source_type} install {mod_url}")
    if event == "Create a new pack":
        window.close()
        window = sg.Window("Creating a new pack", pack_create)

window.close()
