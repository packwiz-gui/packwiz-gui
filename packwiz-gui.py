#!/bin/env python3
import os
import platform
from subprocess import PIPE, Popen
import PySimpleGUI as sg
from shutil import rmtree

root = os.getcwd()
sg.theme("DarkGrey9") # Add a touch of color
#right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT
# All the stuff inside your window.
main_menu = [
            [sg.Text("")],
            [sg.Button("Create a new pack")],
            [sg.Text("")],
            [sg.Button("Open a pack")],
            [sg.Text("")],
            [sg.Button("Close packwiz-gui")]
            ]


if platform.system() == "Windows":
    packwiz = f"{root}\\bin\\packwiz.exe"
    OSYS = "windows"
elif platform.system() == "Darwin" or "Linux":
    packwiz = f"{root}/bin/packwiz"
    os.system(f"chmod +x {packwiz}")
    OSYS = "unix"

# Create the Window
window1 = sg.Window("Main Menu", main_menu)
WINDOW2_ACTIVE = False
WINDOW3_ACTIVE = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event1, values1 = window1.read()
    # Main menu close check
    if event1 in (sg.WIN_CLOSED, "Close packwiz-gui"):
        window1.close()
        break
    

    # EVENT1 - Main Menu

    if event1 == "Create a new pack" and not WINDOW2_ACTIVE:
        pack_create = [
                      [sg.Text("Pack name:"), sg.InputText()],
                      [sg.Text("Author:"), sg.InputText()],
                      [sg.Text("Pack Version:"), sg.InputText()],
                      [sg.Text("Minecraft Version:"), sg.InputText()],
                      [sg.Text("Modloader"), sg.Combo(["forge", "fabric"])],
                      [sg.Text("Modloader Version:"), sg.InputText()],
                      [sg.Button("Create")],
                      [sg.Button("Close")],
                      [sg.Text("")],
                      ]
        WINDOW2_ACTIVE = True
        window1.Hide()
        window2 = sg.Window("Creating a new pack", pack_create)
        
        # EVENT2 - Creating a new pack

        while True:
            event2, values2 = window2.read()
            # New pack window close check
            if event2 in (sg.WIN_CLOSED, "Close"):
                window2.close()
                WINDOW2_ACTIVE = False
                window1.UnHide()
                break

            if event2 == "Create":
                name = values2[0]
                author = values2[1]
                pack_version = values2[2]
                mc_version = values2[3]
                modloader = values2[4]
                modloader_version = values2[5]
                pack_root = f"{root}/instances/{name}_pack"
                os.mkdir(pack_root)
                os.chdir(pack_root)
                os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")
                window2.close()
                WINDOW2_ACTIVE = False
                window1.UnHide()
                break
    
    if event1 == "Open a pack" and not WINDOW3_ACTIVE:
        if OSYS == "windows":
            COMMAND = f"cmd.exe dir {root}/instances/"
        elif OSYS == "unix":
            COMMAND = f"ls {root}/instances/ | grep _pack"
        #status, output = commands.getstatusoutput(f"{COMMAND} {root}/instances")
        process = Popen(
        args=COMMAND,
        stdout=PIPE,
        stderr=PIPE,
        shell=True)

        instances_list = process.stdout.read().decode("utf-8")
        pack_list = [
                    [sg.Text(instances_list)],
                    [sg.Text("Pack Name to open: "), sg.InputText()],
                    [sg.Button("Open")], [sg.Button("Delete (WARNING: CANNOT BE UNDONE)")], [sg.Button("Close")]
                    ]
        WINDOW3_ACTIVE = True
        window1.Hide()
        window3 = sg.Window("Listing existing packs", pack_list)


        # EVENT3 - Open existing packs

        while True:
            event3, values3 = window3.read()
            # Existing modify window close check
            if event3 in (sg.WIN_CLOSED, "Close"):
                window3.close()
                WINDOW3_ACTIVE = False
                window1.UnHide()
                break

            WINDOW4_ACTIVE = False

            if event3 == "Delete (WARNING: CANNOT BE UNDONE)":
                name = values3[0]
                pack_root = f"{root}/instances/{name}_pack"
                rmtree(f"{pack_root}")
                print(f"Pack {name} deleted.")

            if event3 == "Open" and not WINDOW4_ACTIVE:
                name = values3[0]
                pack_root = f"{root}/instances/{name}_pack"
                os.chdir(pack_root)
                pack_edit = [
                            [sg.Text("Source:"), sg.Combo(["modrinth", "curseforge"])],
                            [sg.Text("Mod ID: "), sg.InputText()],
                            [sg.Text("")],
                            [sg.Button("Add Mod")],
                            [sg.Button("Remove Mod")],
                            [sg.Button("View Installed Mods")],
                            [sg.Button("Export to CF pack")],
                            [sg.Text("Pack zip ready in opened directory")],
                            [sg.Text("")],
                            [sg.Button("Close")],
                            ]
                WINDOW3_ACTIVE = False
                WINDOW4_ACTIVE = True
                window3.hide()
                window4 = sg.Window("Editing Pack", pack_edit)


                # EVENT4 - Editing Packs

                while True:
                    event4, values4 = window4.read()
                    # Editing window close check
                    if event4 in (sg.WIN_CLOSED, "Close"):
                        window4.close()
                        WINDOW4_ACTIVE = False
                        window3.UnHide()
                        WINDOW3_ACTIVE = True
                        break
                    if event4 == "Add Mod":
                        source_type = values4[0]
                        mod_url = "\"" + values4[1] + "\""
                        os.chdir(f"{root}/instances/{name}_pack")
                        os.system(f"{packwiz} {source_type} install {mod_url}")
                    WINDOW5_ACTIVE = False
                    if event4 == "View Installed Mods" and not WINDOW5_ACTIVE:
                        if OSYS == "windows":
                            COMMAND = "cmd.exe dir"
                        elif OSYS == "unix":
                            COMMAND = "ls"
                        cmd = f"{COMMAND} {pack_root}/mods"
                        process = Popen(
                            args=cmd,
                            stdout=PIPE,
                            stderr=PIPE,
                            shell=True)
                        mods_list = process.stdout.read().decode("utf-8")
                        list_installed_mods = [
                                              [sg.Text(mods_list)],
                                              [sg.Button("Close")]
                                              ]
                        window5 = sg.Window("Listing installed mods", list_installed_mods)
                        WINDOW4_ACTIVE = False
                        window4.Hide()
                        WINDOW5_ACTIVE = True

                        # EVENT5 - Mod listing

                        while True:
                            event5, values5 = window5.read()
                            # Mods list close check
                            if event5 in (sg.WIN_CLOSED, "Close"):
                                window5.close()
                                WINDOW5_ACTIVE = False
                                WINDOW4_ACTIVE = True
                                window4.UnHide()
                                break
                    if event4 == "Remove Mod":
                        mod_url = values4[1]
                        os.chdir(f"{pack_root}")
                        os.system(f"{packwiz} remove {mod_url}")
                    if event4 == "Export to CF pack":
                        os.system(f"{packwiz} cf export")
                        if platform.system() == "Windows":
                            os.system(f"explorer.exe {pack_root}")
                        elif platform.system() == "Darwin":
                            os.system(f"finder {pack_root}")
                        elif platform.system() == "Linux":
                            os.system(f"xdg-open {pack_root}")
