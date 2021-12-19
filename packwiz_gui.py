#!/bin/env python3

import os
import platform
import sys
import logging
import webbrowser
import shutil
import getopt
import toml

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:qhvgb", ["theme=", "qt", "help", "verbose", "debug", "git", "bin"])
except getopt.GetoptError:
    print("Error: Unknown flag.\nUse --help to see available commands.")
    sys.exit()

THEMESET = ""
QTSET = False
LOGLEVEL = 15
GITSET = False
BINARY = False

for opt, arg in opts:
    if opt in ("--theme", "-t"):
        THEMESET = arg
    if opt in ("-q", "--qt"):
        QTSET = True
    if opt in ("-h", "--help"):
        print("")
        print("  -t, --theme, <theme>:              - Pick a custom theme.")
        print("  -q, --qt:                          - Use Qt instead of tkinter. Requires PySimpleGUIQt.")
        print("  -h, --help:                        - This help message.")
        print("  -v, --verbose, --debug:            - More verbose logging.")
        print("  -b, --bin:                         - Run in binary mode. If you run this script without this flag as a binary, it will crash.")
        print("                                       This may cause unknown bugs.")
        print("")
        sys.exit()
    if opt in ("-v", "--verbose", "--debug"):
        LOGLEVEL = 10
    if opt in ("-g", "--git"):
        GITSET = True
    if opt in ("-b", "--bin"):
        BINARY = True

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

if not BINARY:
    root = sys.path[0]
else:
    root = os.getcwd()

logging_file_handler = logging.FileHandler(filename=f"{root}/log.txt")
logging_stdout_handler = logging.StreamHandler(sys.stdout)
logging_handlers = [logging_file_handler, logging_stdout_handler]
logging.basicConfig(handlers=logging_handlers, level=LOGLEVEL)

logging.debug(msg=f"root dir is {root}")

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
else:
    logging.debug(msg=f"packwiz binary is {packwiz}")

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
                    os.mkdir("mods")
                    if GITSET:
                        os.system("git init")
                        os.system("git add .")
                        os.system(f"git commit -m \"Create pack {name}\"")
                    os.chdir(root)

                    if pack_create_command != 0:
                        logging.error(msg=f"There was an error creating the pack \"{name}\"!")
                        logging.debug(msg=f"error code {pack_create_command}")
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

            if pack_list_event == "Open" and not PACK_EDIT_WINDOW_ACTIVE:
                name = pack_list_values[0]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    if os.path.isfile(f"{pack_root}/pack.toml"):
                        os.chdir(pack_root)
                        pack_toml = toml.load("pack.toml")
                        pack_edit = [
                                    [sg.Text("Source:"), sg.Combo(["modrinth", "curseforge"])],
                                    [sg.Text("Mod ID: "), sg.InputText()],
                                    [sg.Text("")],
                                    [sg.Button("Add Mod")],
                                    [sg.Button("Remove Mod")],
                                    [sg.Button("View Installed Mods")],
                                    [sg.Button("Export to CF pack")],
                                    [sg.Button("Refresh pack")],
                                    [sg.Text("")],
                                    [sg.Text("Pack name:"), sg.InputText(pack_toml["name"])],
                                    [sg.Text("Warning: if you change the pack name, you may need to change the instance folder name yourself.")],
                                    [sg.Text("Author:"), sg.InputText(pack_toml["author"])],
                                    [sg.Text("Pack Version:"), sg.InputText(pack_toml["version"])],
                                    [sg.Text("Minecraft Version:"), sg.InputText(pack_toml["versions"]["minecraft"])],
                                    [sg.Text("Changing modloader is currently unsupported")],
                                    [sg.Button("Change")],
                                    [sg.Button("Close")],
                                    [sg.Text("")],
                                    ]
                        pack_list_window.Close()
                        PACK_LIST_WINDOW_ACTIVE = False
                        pack_edit_window = sg.Window("Editing Pack", pack_edit)
                        PACK_EDIT_WINDOW_ACTIVE = True

                        # Editing Packs

                        while True:
                            pack_edit_event, pack_edit_values = pack_edit_window.read()
                            source = pack_edit_values[0]
                            mod = pack_edit_values[1]
                            # Editing window Close check
                            if pack_edit_event in (sg.WIN_CLOSED, "Close"):
                                pack_edit_window.Close()
                                PACK_EDIT_WINDOW_ACTIVE = False
                                main_menu_window.UnHide()
                                MAIN_MENU_WINDOW_ACTIVE = True
                                break

                            if pack_edit_event == "Add Mod":
                                os.chdir(pack_root)
                                mod_add_command = os.system(f"{packwiz} {source} install {mod}")
                                if mod_add_command != 0:
                                    logging.error(msg=f"There was an error adding mod \"{mod}\" from source \"{source}\"!")
                                    logging.debug(msg=f"error code {mod_add_command}")
                                else:
                                    logging.info(msg=f"Successfully added mod \"{mod}\" from source \"{source}\".")
                                    if GITSET:
                                        os.system("git add .")
                                        os.system(f"git commit -m \"Added {mod}\"")

                            if pack_edit_event == "Remove Mod":
                                os.chdir(f"{pack_root}")
                                mod_remove_command = os.system(f"{packwiz} remove {mod}")
                                if mod_remove_command != 0:
                                    logging.error(msg=f"There was an error removing mod \"{mod}\"!")
                                    logging.debug(msg=f"{mod_remove_command}")
                                else:
                                    logging.info(msg=f"Mod \"{mod}\" successfully removed.")
                                    if GITSET:
                                        os.system("git add .")
                                        os.system(f"git commit -m \"Removed {mod}\"")

                            if pack_edit_event == "View Installed Mods" and not MOD_LIST_WINDOW_ACTIVE:
                                mods_list = ""
                                for n in os.listdir(f"{pack_root}/mods"):
                                    mods_list = mods_list + n + "\n"
                                mod_list = [
                                           [sg.Text(mods_list)],
                                           [sg.Button("Close")]
                                           ]

                                mod_list_window = sg.Window("Listing installed mods", mod_list)
                                MOD_LIST_WINDOW_ACTIVE = True
                                mod_list_event, mod_list_values = mod_list_window.read()
                                mod_list_window.Close()
                                MOD_LIST_WINDOW_ACTIVE = False

                            if pack_edit_event == "Export to CF pack":
                                pack_export_command = os.system(f"{packwiz} cf export")
                                if pack_export_command != 0:
                                    logging.error(msg=f"There was an error exporting the pack \"{name}\"!")
                                    logging.debug(msg=f"error code {pack_export_command}")
                                else:
                                    logging.info(msg=f"Pack \"{name}\" successfully exported.")
                                    if GITSET:
                                        os.system("git add .")
                                        os.system(f"git commit -m \"Exported pack {name}\"")
                                    if platform.system() == "Windows":
                                        os.startfile(pack_root)
                                    elif platform.system() == "Darwin":
                                        os.system(f"open {pack_root}")
                                    else:
                                        os.system(f"xdg-open {pack_root}")

                            if pack_edit_event == "Refresh pack":
                                packwiz_refresh = os.system(f"{packwiz} refresh")
                                if packwiz_refresh != 0:
                                    logging.error(msg="There was an error refreshing the pack!")
                                    logging.debug(msg=f"error code {packwiz_refresh}")
                                else:
                                    logging.info(msg="Successfully refreshed pack.")


                            if pack_edit_event == "Change":
                                pack_toml["name"] = pack_edit_values[2]
                                pack_toml["author"] = pack_edit_values[3]
                                pack_toml["version"] = pack_edit_values[4]
                                pack_toml["versions"]["minecraft"] = pack_edit_values[5]
                                pack_toml_handler = open("pack.toml", "w+")
                                toml.dump(pack_toml, pack_toml_handler)
                                pack_toml_handler.close()
                                packwiz_refresh = os.system(f"{packwiz} refresh")
                                if GITSET:
                                    os.system("git add .")
                                    os.system(f"git commit -m \"Modify pack details\"")
                                if packwiz_refresh != 0:
                                    logging.error(msg="There was an error changing the pack details!")
                                    logging.debug(msg=f"error code {packwiz_refresh}")
                                else:
                                    logging.info(msg="Successfully changed pack details. Please change the instance folder name yourself if you have modified the name.")

                    else:
                        logging.warning(msg=f"The pack \"{name}\" does not exist!")
                else:
                    logging.warning(msg=f"The pack \"{name}\" does not exist!")

            if pack_list_event == "Delete" and not PACK_DELETE_WINDOW_ACTIVE:
                name = pack_list_values[0]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    if os.path.isfile(f"{pack_root}/pack.toml"):
                        pack_delete = [
                                      [sg.Text("WARNING: THIS WILL DELETE ALL OF THIS PACK'S DATA.")],
                                      [sg.Text("ONLY PRESS YES IF YOU UNDERSTAND THIS. ARE YOU SURE?")],
                                      [sg.Text("")],
                                      [sg.Button("Yes"), sg.Button("No")]
                                      ]
                        pack_list_window.Close()
                        PACK_LIST_WINDOW_ACTIVE = False
                        pack_delete_window = sg.Window("Are you sure?", pack_delete)
                        PACK_DELETE_WINDOW_ACTIVE = True

                        # Deleting pack

                        while True:
                            pack_delete_event, pack_delete_values = pack_delete_window.read()
                            # Existing modify window Close check
                            if pack_delete_event in (sg.WIN_CLOSED, "No"):
                                pack_delete_window.Close()
                                PACK_DELETE_WINDOW_ACTIVE = False
                                main_menu_window.UnHide()
                                MAIN_MENU_WINDOW_ACTIVE = True
                                break

                            if pack_delete_event == "Yes":
                                os.chdir(root)
                                shutil.rmtree(f"{pack_root}")
                                logging.info(msg=f"Pack {name} deleted.")

                                pack_delete_window.Close()
                                PACK_DELETE_WINDOW_ACTIVE = False
                                main_menu_window.UnHide()
                                MAIN_MENU_WINDOW_ACTIVE = True
                                break
                    else:
                        logging.warning(msg=f"The pack \"{name}\" does not exist!")
                else:
                    logging.warning(msg=f"The pack \"{name}\" does not exist!")

    if main_menu_event == "Download packwiz":
        if platform.system() == "Windows":
            webbrowser.get("windows-default").open("https://github.com/comp500/packwiz/#installation")
        else:
            webbrowser.open("https://github.com/comp500/packwiz/#installation")
