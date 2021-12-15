#!/bin/env python3

import os
import platform
import sys
import logging
import webbrowser
from shutil import rmtree
from subprocess import PIPE, Popen
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:hv", ["theme=", "qt", "help", "verbose"])
except getopt.GetoptError:
    print("Error: Unknown flag.\nUse --help to see available commands.")
    sys.exit()

THEMESET = ""
QTSET = False
LOGLEVEL = 15

for opt, arg in opts:
    if opt == "--qt":
        QTSET = True
    if opt in ("--theme", "-t"):
        THEMESET = arg
    if opt in ("-h", "--help"):
        print("")
        print("  -t, --theme, <theme>:              Pick a custom theme.")
        print("      --qt:                          Use Qt instead of tkinter. Requires PySimpleGUIQt.")
        print("  -h, --help:                        This help message.")
        print("  -v, --verbose:                     More verbose logging.")
        print("")
        sys.exit()
    if opt in ("-v", "--verbose"):
        LOGLEVEL = 10

if QTSET:
    if platform.system() == "Windows":
        print("Error: Cannot use Qt on Windows")
        sys.exit()
    else:
        try:
            import PySimpleGUIQt as sg
        except ModuleNotFoundError:
            print("You must install PySimpleGUIQt!")
            sys.exit()
else:
    try:
        import PySimpleGUI as sg
    except ModuleNotFoundError:
        print("You must install PySimpleGUI!")
        sys.exit()


if THEMESET == "":
    if QTSET:
        sg.theme("SystemDefaultForReal")
    else:
        sg.theme("DarkGrey9")
else:
    sg.theme(THEMESET)

logging_file_handler = logging.FileHandler(filename='log.txt')
logging_stdout_handler = logging.StreamHandler(sys.stdout)
logging_handlers = [logging_file_handler, logging_stdout_handler]
logging.basicConfig(handlers=logging_handlers, level=LOGLEVEL)

root = os.getcwd()

if platform.system() == "Windows":
    packwiz = f"{root}\\bin\\packwiz.exe"
else:
    packwiz = f"{root}/bin/packwiz"
    os.system(f"chmod +x {packwiz}")

if not os.path.isdir(f"{root}/instances"):
    os.mkdir(f"{root}/instances")
    logging.warning(msg="No instances folder, creating...")
if not os.path.isdir(f"{root}/bin"):
    os.mkdir(f"{root}/bin")
    logging.warning(msg="No bin folder, creating...")
if not os.path.isfile(packwiz):
    logging.critical(msg="Packwiz does not exist! Please download packwiz and put it in the bin folder!")

PACK_CREATE_WINDOW_ACTIVE = False
PACK_LIST_WINDOW_ACTIVE = False
PACK_EDIT_WINDOW_ACTIVE = False
MOD_LIST_WINDOW_ACTIVE = False
PACK_DELETE_WINDOW_ACTIVE = False

# All the stuff inside your window.
main_menu = [
            [sg.Text("")],
            [sg.Button("Create a new pack")],
            [sg.Text("")],
            [sg.Button("Modify a pack")],
            [sg.Text("")],
            [sg.Button("Download packwiz")],
            [sg.Text("")],
            [sg.Button("Close packwiz-gui")]
            ]

# Create the Window
main_menu_window = sg.Window("Main Menu", main_menu)
MAIN_MENU_WINDOW_ACTIVE = True

# Event Loop to process "events" and get the "values" of the inputs
while True:
    main_menu_event, main_menu_values = main_menu_window.read()
    # Main menu Close check
    if main_menu_event in (sg.WIN_CLOSED, "Close packwiz-gui"):
        main_menu_window.Close()
        MAIN_MENU_WINDOW_ACTIVE = False
        break

    # Main Menu

    if main_menu_event == "Create a new pack" and not PACK_CREATE_WINDOW_ACTIVE:
        pack_create = [
                      [sg.Text("Pack name:"), sg.InputText()],
                      [sg.Text("Author:"), sg.InputText()],
                      [sg.Text("Pack Version:"), sg.InputText()],
                      [sg.Text("Minecraft Version:"), sg.InputText()],
                      [sg.Text("Modloader:"), sg.Combo(["forge", "fabric"])],
                      [sg.Text("Modloader Version:"), sg.InputText()],
                      [sg.Button("Create"), sg.Button("Close")],
                      [sg.Text("")],
                      ]

        main_menu_window.Hide()
        MAIN_MENU_WINDOW_ACTIVE = False
        pack_create_window = sg.Window("Creating a new pack", pack_create)
        PACK_CREATE_WINDOW_ACTIVE = True

        # Creating a new pack

        while True:
            pack_create_event, pack_create_values = pack_create_window.read()
            # New pack window Close check
            if pack_create_event in (sg.WIN_CLOSED, "Close"):
                pack_create_window.Close()
                PACK_CREATE_WINDOW_ACTIVE = False
                main_menu_window.UnHide()
                MAIN_MENU_WINDOW_ACTIVE = True
                break

            if pack_create_event == "Create":
                name = pack_create_values[0]
                pack_root = f"{root}/instances/{name}"
                if not os.path.isdir(pack_root):
                    author = pack_create_values[1]
                    pack_version = pack_create_values[2]
                    mc_version = pack_create_values[3]
                    modloader = pack_create_values[4]
                    modloader_version = pack_create_values[5]
                    os.mkdir(pack_root)
                    os.chdir(pack_root)
                    pack_create_command = os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")
                    os.system("echo *.zip >> .packwizignore")
                    os.system("echo .git/** >>.packwizignore")
                    os.system("git init")
                    os.system("git add .")
                    os.system(f"git commit -m \"Create pack {name}\"")
                    os.chdir(root)

                    if pack_create_command != 0:
                        logging.error(msg=f"There was an error creating the pack \"{name}\"!")
                        os.rmdir(pack_root)
                    else:
                        logging.info(msg=f"Pack \"{name}\" created.")

                    pack_create_window.Close()
                    PACK_CREATE_WINDOW_ACTIVE = False
                    main_menu_window.UnHide()
                    MAIN_MENU_WINDOW_ACTIVE = True
                    break
                else:
                    logging.warning(msg=f"The pack \"{name}\" already exists!")

    if main_menu_event == "Modify a pack" and not PACK_LIST_WINDOW_ACTIVE:
        instances_list = ""
        for n in os.listdir(f"{root}/instances"):
            instances_list = instances_list + n + "\n"
        pack_list = [
                    [sg.Text(instances_list)],
                    [sg.Text("Pack Name:"), sg.InputText()],
                    [sg.Button("Open")],
                    [sg.Button("Close")],
                    [sg.Button("Delete", button_color="red")],
                    ]

        main_menu_window.Hide()
        MAIN_MENU_WINDOW_ACTIVE = False
        pack_list_window = sg.Window("Listing existing packs", pack_list)
        PACK_LIST_WINDOW_ACTIVE = True

        # Open existing packs

        while True:
            pack_list_event, pack_list_values = pack_list_window.read()
            # Existing modify window Close check
            if pack_list_event in (sg.WIN_CLOSED, "Close"):
                pack_list_window.Close()
                PACK_LIST_WINDOW_ACTIVE = False
                main_menu_window.UnHide()
                MAIN_MENU_WINDOW_ACTIVE = True
                break

            if pack_list_event == "Delete" and not PACK_DELETE_WINDOW_ACTIVE:
                name = pack_list_values[0]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    if os.path.isfile(f"{pack_root}/pack.toml"):
                        delete_dialog = [
                                        [sg.Text("WARNING: THIS WILL DELETE ALL OF THIS PACK'S DATA.")],
                                        [sg.Text("ONLY PRESS YES IF YOU UNDERSTAND THIS. ARE YOU SURE?")],
                                        [sg.Text("")],
                                        [sg.Button("Yes"), sg.Button("No")]
                                        ]
                        pack_list_window.Hide()
                        PACK_LIST_WINDOW_ACTIVE = False
                        pack_delete_window = sg.Window("Are you sure?", delete_dialog)
                        PACK_DELETE_WINDOW_ACTIVE = True

                        # Deleting pack

                        while True:
                            pack_delete_event, pack_delete_values = pack_delete_window.read()
                            # Existing modify window Close check
                            if pack_delete_event in (sg.WIN_CLOSED, "No"):
                                pack_delete_window.Close()
                                PACK_DELETE_WINDOW_ACTIVE = False
                                pack_list_window.UnHide()
                                PACK_LIST_WINDOW_ACTIVE = True
                                break

                            if pack_delete_event == "Yes":
                                os.chdir(root)
                                rmtree(f"{pack_root}")
                                logging.info(msg=f"Pack {name} deleted.")

                                pack_delete_window.Close()
                                PACK_DELETE_WINDOW_ACTIVE = False
                                pack_list_window.Close()
                                PACK_LIST_WINDOW_ACTIVE = False
                                main_menu_window.UnHide()
                                MAIN_MENU_WINDOW_ACTIVE = True
                                break
                    else:
                        logging.warning(msg=f"The pack \"{name}\" does not exist!")
                else:
                    logging.warning(msg=f"The pack \"{name}\" does not exist!")

            if pack_list_event == "Open" and not PACK_EDIT_WINDOW_ACTIVE:
                name = pack_list_values[0]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    if os.path.isfile(f"{pack_root}/pack.toml"):
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
                        pack_list_window.Hide()
                        PACK_LIST_WINDOW_ACTIVE = False
                        pack_edit_window = sg.Window("Editing Pack", pack_edit)
                        PACK_EDIT_WINDOW_ACTIVE = True

                        # Editing Packs

                        while True:
                            pack_edit_event, pack_edit_values = pack_edit_window.read()
                            mod = pack_edit_values[1]
                            # Editing window Close check
                            if pack_edit_event in (sg.WIN_CLOSED, "Close"):
                                pack_edit_window.Close()
                                PACK_EDIT_WINDOW_ACTIVE = False
                                pack_list_window.UnHide()
                                PACK_LIST_WINDOW_ACTIVE = True
                                break

                            if pack_edit_event == "Add Mod":
                                source = pack_edit_values[0]
                                os.chdir(pack_root)
                                mod_add_command = os.system(f"{packwiz} {source} install {mod}")
                                if mod_add_command != 0:
                                    logging.error(msg=f"There was an error adding mod \"{mod}\" from source \"{source}\"!")
                                else:
                                    logging.info(msg=f"Successfully added mod \"{mod}\" from source \"{source}\".")

                            if pack_edit_event == "View Installed Mods" and not MOD_LIST_WINDOW_ACTIVE:
                                if platform.system() == "Windows":
                                    COMMAND = f"dir {pack_root}/mods"
                                else:
                                    COMMAND = f"ls {pack_root}/mods"
                                mods_list = Popen(args=COMMAND,
                                                  stdout=PIPE,
                                                  stderr=PIPE,
                                                  shell=True).stdout.read().decode("utf-8")
                                list_installed_mods = [
                                                      [sg.Text(mods_list)],
                                                      [sg.Button("Close")]
                                                      ]

                                mod_list_window = sg.Window("Listing installed mods", list_installed_mods)
                                MOD_LIST_WINDOW_ACTIVE = True
                                mod_list_event, mod_list_values = mod_list_window.read()
                                mod_list_window.Close()
                                MOD_LIST_WINDOW_ACTIVE = False

                            if pack_edit_event == "Remove Mod":
                                os.chdir(f"{pack_root}")
                                mod_remove_command = os.system(f"{packwiz} remove {mod}")
                                if mod_remove_command != 0:
                                    logging.error(msg=f"There was an error removing mod \"{mod}\"!")
                                else:
                                    logging.info(msg=f"Mod \"{mod}\" successfully removed.")

                            if pack_edit_event == "Export to CF pack":
                                pack_export_command = os.system(f"{packwiz} cf export")
                                if pack_export_command != 0:
                                    logging.error(msg=f"There was an error exporting the pack \"{name}\"!")
                                else:
                                    logging.info(msg=f"Pack \"{name}\" successfully exported.")
                                    if platform.system() == "Windows":
                                        os.startfile(pack_root)
                                    elif platform.system() == "Darwin":
                                        os.system(f"open {pack_root}")
                                    else:
                                        os.system(f"xdg-open {pack_root}")
                    else:
                        logging.warning(msg=f"The pack \"{name}\" does not exist!")
                else:
                    logging.warning(msg=f"The pack \"{name}\" does not exist!")

    if main_menu_event == "Download packwiz":
        if platform.system() == "Windows":
            webbrowser.get("windows-default").open("https://github.com/comp500/packwiz/#installation")
        else:
            webbrowser.open("https://github.com/comp500/packwiz/#installation")
