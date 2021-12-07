#!/bin/env python3
import os
import platform
from subprocess import PIPE, Popen
from shutil import rmtree
import PySimpleGUI as sg

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
main_menu_window = sg.Window("Main Menu", main_menu)

MAIN_MENU_WINDOW_ACTIVE = True
PACK_CREATE_WINDOW_ACTIVE = False
PACK_LIST_WINDOW_ACTIVE = False
PACK_EDIT_WINDOW_ACTIVE = False
MOD_LIST_WINDOW_ACTIVE = False
PACK_DELETE_WINDOW_ACTIVE = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    main_menu_event, main_menu_values = main_menu_window.read()
    # Main menu close check
    if main_menu_event in (sg.WIN_CLOSED, "Close packwiz-gui"):
        main_menu_window.close()
        break


    # Main Menu

    if main_menu_event == "Create a new pack" and not PACK_CREATE_WINDOW_ACTIVE:
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
        PACK_CREATE_WINDOW_ACTIVE = True
        main_menu_window.Hide()
        MAIN_MENU_WINDOW_ACTIVE = False
        pack_create_window = sg.Window("Creating a new pack", pack_create)

        # Creating a new pack

        while True:
            pack_create_event, pack_create_values = pack_create_window.read()
            # New pack window close check
            if pack_create_event in (sg.WIN_CLOSED, "Close"):
                pack_create_window.close()
                PACK_CREATE_WINDOW_ACTIVE = False
                main_menu_window.UnHide()
                MAIN_MENU_WINDOW_ACTIVE = True

                break

            if pack_create_event == "Create":
                name = pack_create_values[0]
                author = pack_create_values[1]
                pack_version = pack_create_values[2]
                mc_version = pack_create_values[3]
                modloader = pack_create_values[4]
                modloader_version = pack_create_values[5]
                pack_root = f"{root}/instances/{name}_pack"
                os.mkdir(pack_root)
                os.chdir(pack_root)
                os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")
                os.chdir(root)

                pack_create_window.close()
                PACK_CREATE_WINDOW_ACTIVE = False
                main_menu_window.UnHide()
                MAIN_MENU_WINDOW_ACTIVE = True
                break

    if main_menu_event == "Open a pack" and not PACK_LIST_WINDOW_ACTIVE:
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
                    [sg.Button("Open")],
                    [sg.Button("Close")],
                    [sg.Button("Delete", button_color=("red"))],
                    ]
        PACK_LIST_WINDOW_ACTIVE = True
        main_menu_window.Hide()
        pack_list_window = sg.Window("Listing existing packs", pack_list)


        # EVENT3 - Open existing packs

        while True:
            pack_list_event, pack_list_values = pack_list_window.read()
            # Existing modify window close check
            if pack_list_event in (sg.WIN_CLOSED, "Close"):
                pack_list_window.close()
                PACK_LIST_WINDOW_ACTIVE = False
                main_menu_window.UnHide()
                break

            if pack_list_event == "Delete" and not PACK_DELETE_WINDOW_ACTIVE:
                name = pack_list_values[0]
                pack_root = f"{root}/instances/{name}_pack"
                delete_dialog = [
                                [sg.Text("WARNING: THIS WILL DELETE ALL OF THIS PACK'S DATA. ONLY PRESS YES IF YOU UNDERSTAND THIS. ARE YOU SURE?")],
                                [sg.Button("Yes"), sg.Button("No")]
                                ]
                pack_list_window.Hide()
                PACK_LIST_WINDOW_ACTIVE = False
                PACK_DELETE_WINDOW_ACTIVE = True
                pack_delete_window = sg.Window("Are you sure?", delete_dialog)

                while True:
                    pack_delete_event, pack_delete_values = pack_delete_window.read()
                    # Existing modify window close check
                    if pack_delete_event in (sg.WIN_CLOSED, "No"):
                        pack_delete_window.Close()
                        PACK_DELETE_WINDOW_ACTIVE = False
                        pack_list_window.UnHide()
                        PACK_DELETE_WINDOW_ACTIVE = True
                        break
                    if pack_delete_event == "Yes":
                        os.chdir(root)
                        rmtree(f"{pack_root}")
                        print(f"Pack {name} deleted.")

                        pack_delete_window.close()
                        PACK_DELETE_WINDOW_ACTIVE = False
                        pack_list_window.close()
                        PACK_DELETE_WINDOW_ACTIVE = False
                        main_menu_window.UnHide()
                        MAIN_MENU_WINDOW_ACTIVE = True
                        break

            if pack_list_event == "Open" and not PACK_EDIT_WINDOW_ACTIVE:
                name = pack_list_values[0]
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
                            [sg.Text("")],
                            [sg.Button("Close")],
                            ]
                PACK_LIST_WINDOW_ACTIVE = False
                PACK_EDIT_WINDOW_ACTIVE = True
                pack_list_window.hide()
                pack_edit_window = sg.Window("Editing Pack", pack_edit)


                # EVENT4 - Editing Packs

                while True:
                    pack_edit_event, pack_edit_values = pack_edit_window.read()
                    # Editing window close check
                    if pack_edit_event in (sg.WIN_CLOSED, "Close"):
                        pack_edit_window.close()
                        PACK_EDIT_WINDOW_ACTIVE = False
                        pack_list_window.UnHide()
                        PACK_LIST_WINDOW_ACTIVE = True
                        break
                    if pack_edit_event == "Add Mod":
                        source_type = pack_edit_values[0]
                        mod_url = "\"" + pack_edit_values[1] + "\""
                        os.chdir(f"{root}/instances/{name}_pack")
                        os.system(f"{packwiz} {source_type} install {mod_url}")
                    if pack_edit_event == "View Installed Mods" and not MOD_LIST_WINDOW_ACTIVE:
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
                        mod_list_window = sg.Window("Listing installed mods", list_installed_mods)
                        PACK_EDIT_WINDOW_ACTIVE = False
                        pack_edit_window.Hide()
                        MOD_LIST_WINDOW_ACTIVE = True

                        # EVENT5 - Mod listing

                        while True:
                            mod_list_event, mod_list_values = mod_list_window.read()
                            # Mods list close check
                            if mod_list_event in (sg.WIN_CLOSED, "Close"):
                                mod_list_window.close()
                                MOD_LIST_WINDOW_ACTIVE = False
                                PACK_EDIT_WINDOW_ACTIVE = True
                                pack_edit_window.UnHide()
                                break
                    if pack_edit_event == "Remove Mod":
                        mod_url = pack_edit_values[1]
                        os.chdir(f"{pack_root}")
                        os.system(f"{packwiz} remove {mod_url}")
                    if pack_edit_event == "Export to CF pack":
                        os.system(f"{packwiz} cf export")
                        if platform.system() == "Windows":
                            os.system(f"explorer.exe {pack_root}")
                        elif platform.system() == "Darwin":
                            os.system(f"finder {pack_root}")
                        elif platform.system() == "Linux":
                            os.system(f"xdg-open {pack_root}")
