#!/bin/env python3

import os
import platform
import sys
import logging
import getopt
import webbrowser
import shutil
import toml

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:qhdg", ["theme=", "qt", "help", "debug", "git"])
    except getopt.GetoptError:
        print("Error: Unknown flag.\nUse --help to see available commands.")
        sys.exit()

    theme = None
    qtset = False
    loglevel = 15
    gitset = False

    for opt, arg in opts:
        if opt in ("-t", "--theme"):
            theme = arg
        elif opt in ("-q", "--qt"):
            qtset = True
        elif opt in ("-h", "--help"):
            print("")
            print("  -t, --theme, <theme>:              - Picks a custom theme.")
            print("  -q, --qt:                          - Qt instead of tkinter. Requires PySimpleGUIQt.")
            print("  -h, --help:                        - This help message.")
            print("  -d, --debug:                       - Verbose logging.")
            print("  -g, --git:                         - Git support.")
            print("")
            sys.exit()
        elif opt in ("-d", "--debug"):
            loglevel = 10
        elif opt in ("-g", "--git"):
            gitset = True

    if qtset:
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
    if theme is None:
        if qtset:
            sg.theme("SystemDefaultForReal")
        else:
            sg.theme("DarkGrey9")
    else:
        sg.theme(theme)

    if os.path.isdir(sys.path[0]):
        root = sys.path[0]
    else:
        root = os.getcwd()

    logging_file_handler = logging.FileHandler(filename=f"{root}/log.txt")
    logging_stdout_handler = logging.StreamHandler(sys.stdout)
    logging_handlers = [logging_file_handler, logging_stdout_handler]
    logging.basicConfig(handlers=logging_handlers, level=loglevel)

    def log(msg, logtype):
        if logtype == "debug":
            logging.debug(msg=msg)
            return True
        elif logtype == "info":
            logging.info(msg=msg)
            return True
        elif logtype == "warning":
            logging.warning(msg=msg)
            return True
        elif logtype == "warningsg":
            logging.warning(msg=msg)
            sg.popup_ok_cancel(msg)
            return True
        elif logtype == "error":
            logging.error(msg=msg)
            return True
        elif logtype == "errorsg":
            logging.error(msg=msg)
            sg.popup_error(msg)
            return True
        elif logtype == "critical":
            logging.critical(msg=msg)
            return True
        elif logtype == "criticalsg":
            logging.critical(msg=msg)
            sg.popup_error(msg)
            return True
        else:
            raise ValueError("Wrong or no type provided!")

    log(f"root dir is {root}", "debug")
    if platform.system() == "Windows":
        packwiz = f"{root}\\bin\\packwiz.exe"
    else:
        packwiz = f"{root}/bin/packwiz"
        os.system(f"chmod +x {packwiz}")

    if not os.path.isdir(f"{root}/instances"):
        os.mkdir(f"{root}/instances")
        log("No instances folder, creating...", "warning")
    if not os.path.isdir(f"{root}/bin"):
        os.mkdir(f"{root}/bin")
        log( "No bin folder, creating...", "warning")
    if not os.path.isfile(packwiz):
        log("Packwiz does not exist! Please download packwiz and put it in the bin folder!", "criticalsg")
    else:
        log(f"packwiz binary is {packwiz}", "debug")

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

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        main_menu_event, main_menu_values = main_menu_window.read()
        # Main menu close check
        if main_menu_event in (sg.WIN_CLOSED, "Close packwiz-gui"):
            main_menu_window.close()
            break

        # Main Menu

        if main_menu_event == "Create a new pack":
            pack_create = [
                        [sg.Text("Pack name:"), sg.InputText(key="name")],
                        [sg.Text("Author:"), sg.InputText(key="author")],
                        [sg.Text("Pack Version:"), sg.InputText(key="version")],
                        [sg.Text("Minecraft Version:"), sg.InputText(key="minecraftversion")],
                        [sg.Text("Modloader:"), sg.Combo(["forge", "fabric"], key="modloader")],
                        [sg.Text("Modloader Version:"), sg.InputText(key="modloaderversion")],
                        [sg.Button("Create"), sg.Button("Close")],
                        [sg.Text("")],
                        ]
            main_menu_window.hide()
            pack_create_window = sg.Window("Creating a new pack", pack_create)

            # Creating a new pack

            pack_create_event, pack_create_values = pack_create_window.read()
            if pack_create_event == "Create":
                name = pack_create_values["name"]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    print(f"The pack \"{name}\" already exists!")
                else:
                    author = pack_create_values["author"]
                    pack_version = pack_create_values["version"]
                    mc_version = pack_create_values["minecraftversion"]
                    modloader = pack_create_values["modloader"]
                    modloader_version = pack_create_values["modloaderversion"]
                    os.mkdir(pack_root)
                    os.chdir(pack_root)
                    pack_create_command = os.system(f"{packwiz} init --name \"{name}\" --author \"{author}\" --version \"{pack_version}\" --mc-version \"{mc_version}\" --modloader \"{modloader}\" --{modloader}-version \"{modloader_version}\"")
                    with open(".packwizignore", "w", encoding="utf8") as pwignore:
                        pwignore.write("*.zip\n.git/**")
                    os.mkdir("mods")
                    if gitset:
                        os.system("git init")
                        os.system("git add .")
                        os.system(f"git commit -m \"Create pack {name}\"")
                    os.chdir(root)
                    if pack_create_command != 0:
                        print(f"There was an error creating the pack \"{name}\"!")
                        log(f"error code {pack_create_command}", "debug")
                        shutil.rmtree(pack_root)
                    else:
                        print(f"Pack \"{name}\" created.")
            pack_create_window.close()
            main_menu_window.UnHide()

        if main_menu_event == "Modify a pack":
            instances_list = ""
            for instance in os.listdir(f"{root}/instances"):
                instances_list = instances_list + instance + "\n"
            pack_list = [
                        [sg.Text("Packs:")],
                        [sg.Text(instances_list)],
                        [sg.Text("Pack Name:"), sg.InputText(key="packname")],
                        [sg.Button("Open")],
                        [sg.Button("Close")],
                        [sg.Button("Delete", button_color="red")],
                        ]
            main_menu_window.hide()
            pack_list_window = sg.Window("Listing existing packs", pack_list)

            # Open existing packs

            pack_list_event, pack_list_values = pack_list_window.read()
            pack_list_window.close()
            if pack_list_event == "Open":
                name = pack_list_values["packname"]
                pack_root = f"{root}/instances/{name}"
                if not os.path.isfile(f"{pack_root}/pack.toml"):
                    print(f"The pack \"{name}\" does not exist!")
                else:
                    os.chdir(pack_root)
                    pack_toml = toml.load("pack.toml")
                    pack_edit = [
                                [sg.Text("Source:"), sg.Combo(["modrinth", "curseforge"], key="source")],
                                [sg.Text("Mod: "), sg.InputText(key="mod")],
                                [sg.Text("")],
                                [sg.Button("Add Mod")],
                                [sg.Button("Remove Mod")],
                                [sg.Button("View Installed Mods")],
                                [sg.Button("Export to CF pack")],
                                [sg.Button("Refresh pack")],
                                [sg.Button("Update all mods")],
                                [sg.Button("Update mod")],
                                [sg.Text("")],
                                [sg.Text("Pack name:"), sg.InputText(pack_toml["name"], key="name")],
                                [sg.Text("Warning: if you change the pack name, you may need to change the instance folder name yourself.")],
                                [sg.Text("Author:"), sg.InputText(pack_toml["author"], key="author")],
                                [sg.Text("Pack Version:"), sg.InputText(pack_toml["version"], key="version")],
                                [sg.Text("Minecraft Version:"), sg.InputText(pack_toml["versions"]["minecraft"], key="minecraftversion")],
                                [sg.Text("Changing modloader is currently unsupported.")],
                                [sg.Button("Change")],
                                [sg.Button("Close")],
                                [sg.Text("")],
                                ]
                    pack_edit_window = sg.Window("Editing Pack", pack_edit)
                    # Editing Packs
                    while True:
                        pack_edit_event, pack_edit_values = pack_edit_window.read()
                        source = pack_edit_values["source"]
                        mod = pack_edit_values["mod"]
                        # Editing window close check
                        if pack_edit_event in (sg.WIN_CLOSED, "Close"):
                            pack_edit_window.close()
                            break
                        if pack_edit_event == "Add Mod":
                            os.chdir(pack_root)
                            mod_add_command = os.system(f"{packwiz} {source} install {mod}")
                            if mod_add_command != 0:
                                print(f"There was an error adding mod \"{mod}\" from source \"{source}\"!")
                                log(f"error code {mod_add_command}", "debug")
                            else:
                                print(f"Successfully added mod \"{mod}\" from source \"{source}\".")
                                if gitset:
                                    os.system("git add .")
                                    os.system(f"git commit -m \"Add {mod}\"")
                        if pack_edit_event == "Remove Mod":
                            os.chdir(f"{pack_root}")
                            mod_remove_command = os.system(f"{packwiz} remove {mod}")
                            if mod_remove_command != 0:
                                print(f"There was an error removing mod \"{mod}\"!")
                                log(f"error code {mod_remove_command}", "debug")
                            else:
                                print(f"Mod \"{mod}\" successfully removed.")
                                if gitset:
                                    os.system("git add .")
                                    os.system(f"git commit -m \"Remove {mod}\"")
                        if pack_edit_event == "View Installed Mods":
                            mods_list = ""
                            for mod in os.listdir(f"{pack_root}/mods"):
                                mods_list = mods_list + mod.replace(".toml", "", 1) + "\n"
                            sg.popup(mods_list, title="Installed mods")
                        if pack_edit_event == "Export to CF pack":
                            pack_export_command = os.system(f"{packwiz} cf export")
                            if pack_export_command != 0:
                                print(f"There was an error exporting the pack \"{name}\"!")
                                log(f"error code {pack_export_command}", "debug")
                            else:
                                print(f"Pack \"{name}\" successfully exported.")
                                if gitset:
                                    os.system("git add .")
                                    os.system(f"git commit -m \"Export pack {name}\"")
                                if platform.system() == "Windows":
                                    os.startfile(pack_root)
                                elif platform.system() == "Darwin":
                                    os.system(f"open {pack_root}")
                                else:
                                    os.system(f"xdg-open {pack_root}")
                        if pack_edit_event == "Refresh pack":
                            packwiz_refresh = os.system(f"{packwiz} refresh")
                            if packwiz_refresh != 0:
                                print("There was an error refreshing the pack!")
                                log(f"error code {packwiz_refresh}", "debug")
                            else:
                                print("Successfully refreshed pack.")
                            if gitset:
                                os.system("git add .")
                                os.system("git commit -m \"Refresh pack\"")
                        if pack_edit_event == "Update all mods":
                            packwiz_update_all = os.system(f"{packwiz} update -a")
                            if packwiz_update_all != 0:
                                print("There was an error updating all mods!")
                            else:
                                print("Updating all mods succeeded.")
                            if gitset:
                                os.system("git add .")
                                os.system("git commit -m \"Update all mods\"")
                        if pack_edit_event == "Update mod":
                            packwiz_update_mod = os.system(f"{packwiz} update {mod}")
                            if packwiz_update_mod != 0:
                                print("There was an error updating your mod(s)!")
                            else:
                                print("Updating your mod(s) succeeded.")
                            if gitset:
                                os.system("git add .")
                                os.system(f"git commit -m \"Update {mod}\"")
                        if pack_edit_event == "Change":
                            pack_toml["name"] = pack_edit_values["name"]
                            pack_toml["author"] = pack_edit_values["author"]
                            pack_toml["version"] = pack_edit_values["version"]
                            pack_toml["versions"]["minecraft"] = pack_edit_values["minecraftversion"]
                            with open("pack.toml", "w", encoding="utf8") as pack_toml_file:
                                toml.dump(pack_toml, pack_toml_file)
                            packwiz_refresh = os.system(f"{packwiz} refresh")
                            if gitset:
                                os.system("git add .")
                                os.system("git commit -m \"Modify pack details\"")
                            if packwiz_refresh != 0:
                                print("There was an error changing the pack details!")
                                log(f"error code {packwiz_refresh}", "debug")
                            else:
                                print("Successfully changed pack details. Please change the instance folder name yourself if you have modified the name.")

            if pack_list_event == "Delete":
                name = pack_list_values["packname"]
                pack_root = f"{root}/instances/{name}"
                if not os.path.isfile(f"{pack_root}/pack.toml"):
                    print(f"The pack \"{name}\" does not exist!")
                else:
                    pack_delete_event = sg.popup_yes_no("WARNING: THIS WILL DELETE ALL OF THIS PACK'S DATA."
                                                        "\nONLY PRESS YES IF YOU UNDERSTAND THIS. ARE YOU SURE?", title="Are you sure?")
                    if pack_delete_event == "Yes":
                        os.chdir(root)
                        shutil.rmtree(f"{pack_root}")
                        print(f"Pack {name} deleted.")
            main_menu_window.UnHide()

        if main_menu_event == "Download packwiz":
            if platform.system() == "Windows":
                webbrowser.get("windows-default").open("https://github.com/comp500/packwiz/#installation")
            else:
                webbrowser.open("https://github.com/comp500/packwiz/#installation")

if __name__ == "__main__":
    main()
