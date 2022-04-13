#!/bin/env python3

"""
packwiz-gui. If you don't know what this is, what are you doing here?
Anyway, docstring to make linter stfu :)
"""

import os
import platform
import sys
import subprocess
import logging
import webbrowser
import shutil
import tomli
import tomli_w


def runcmd(cmd, shell=False, check=False):
    """
    Run command.
    Args:
    cmd: Command to run. Array with value for each arg, unless shell is True or there's only 1 arg (binary to run).
    shell (opt, False): Whether to run command in a shell.
    check (opt, False): Whether to throw exception if fail.
    """
    return subprocess.run(cmd, shell=shell, check=check)

def opentoml(filename):
    """
    Open toml file. Returns dict.
    Args:
    filename: filename of file (with path) to open.
    """
    with open(filename, "rb") as toml_file:
        return tomli.load(toml_file)

def dumptoml(filename, var):
    """
    Takes in dict and filename. Dumps dict to file as toml.
    Args:
    filename: filename of file (with path) to dump to
    var: dict to dump from
    """
    with open(filename, "wb") as toml_file:
        return tomli_w.dump(var, toml_file)

def createsettings(filename):
    """
    Create settings.
    Args:
    filename: filename of settings toml file.
    """
    settings = {
        "backend": "qt",
        "tktheme": "DarkGrey9",
        "qttheme": "SystemDefaultForReal",
        "usegit": False
    }
    dumptoml(filename, settings)

VERSION_NUMBER = '1.1.2'

def main():
    """
    Main function. Mostly using this docstring to make linter stfu
    """

    root = sys.path[0] if os.path.isdir(sys.path[0]) else os.getcwd()

    logging_file_handler = logging.FileHandler(filename=f"{root}/log.txt")
    logging_stdout_handler = logging.StreamHandler(sys.stdout)
    logging_handlers = [logging_file_handler, logging_stdout_handler]
    logging.basicConfig(handlers=logging_handlers, level=10)

    def log(msg, logtype):
        if logtype == "debug":
            logging.debug(msg=msg)
        elif logtype == "info":
            logging.info(msg=msg)
        elif logtype == "warning":
            logging.warning(msg=msg)
        elif logtype == "warningsg":
            logging.warning(msg=msg)
            sg.popup_ok_cancel(msg)
        elif logtype == "error":
            logging.error(msg=msg)
        elif logtype == "errorsg":
            print(msg)
            sg.popup_error(msg)
        elif logtype == "critical":
            logging.critical(msg=msg)
        elif logtype == "criticalsg":
            logging.critical(msg=msg)
            sg.popup_error(msg)
        elif logtype == "print":
            print(msg)
        elif logtype == "printerror":
            print(msg)
            sg.popup_error(msg)
        elif logtype == "printsg":
            print(msg)
            sg.popup(msg)
        else:
            raise ValueError("Wrong or no type provided!")

    if not os.path.isfile(f"{root}/settings.toml"):
        createsettings(f"{root}/settings.toml")
    settings = opentoml(f"{root}/settings.toml")
    valid_backends = ["tk", "qt"]
    if settings["backend"] in valid_backends:
        if settings["backend"] == "qt":
            import PySimpleGUIQt as sg
            sg.theme(settings["qttheme"])
        elif settings["backend"] == "tk":
            import PySimpleGUI as sg
            sg.theme(settings["tktheme"])
        current_backend = settings["backend"]
    else:
        log("Error: backend invalid in settings file", "critical")
    usegit = settings["usegit"]
    log(f"root dir is {root}", "debug")
    if platform.system() == "Windows":
        packwiz = f"{root}\\bin\\packwiz.exe"
    else:
        packwiz = f"{root}/bin/packwiz"
        runcmd(["chmod", "+x", packwiz])
    if not os.path.isdir(f"{root}/instances"):
        os.mkdir(f"{root}/instances")
        log("No instances folder, creating...", "warning")
    if not os.path.isdir(f"{root}/bin"):
        os.mkdir(f"{root}/bin")
        log("No bin folder, creating...", "warning")
    if not os.path.isfile(packwiz):
        log("Packwiz does not exist! Please download packwiz and put it in the bin folder!", "criticalsg")
    else:
        log(f"packwiz binary is {packwiz}", "debug")
    main_menu = [
        [sg.T("")],
        [sg.B("Create a new pack")],
        [sg.T("")],
        [sg.B("Modify pack")],
        [sg.T("")],
        [sg.B("Import an existing pack")],
        [sg.T("")],
        [sg.B("Download packwiz")],
        [sg.T("")],
        [sg.B("Settings")],
        [sg.T("")],
        [sg.B("Close packwiz-gui")],
        [sg.T(f"packwiz-gui {VERSION_NUMBER}", font=(sg.DEFAULT_FONT[0], 8, "italic"))]
    ]
    main_menu_window = sg.Window("Main Menu", main_menu)
    while True:
        main_menu_event, main_menu_values = main_menu_window.read()
        if main_menu_event in (sg.WIN_CLOSED, "Close packwiz-gui"):
            main_menu_window.close()
            break
        if main_menu_event == "Create a new pack":
            pack_create = [
                [sg.T("Pack name:"), sg.In(key="name")],
                [sg.T("Author:"), sg.In(key="author")],
                [sg.T("Pack Version:"), sg.In(key="version")],
                [sg.T("Minecraft Version:"), sg.In(key="minecraftversion")],
                [sg.T("Modloader:"), sg.Drop(["forge", "fabric", "liteloader"], key="modloader")],
                [sg.T("Modloader Version:"), sg.In(key="modloaderversion")],
                [sg.B("Create"), sg.B("Close")],
                [sg.T("")],
            ]
            main_menu_window.hide()
            pack_create_window = sg.Window("Create new pack", pack_create)
            pack_create_event, pack_create_values = pack_create_window.read()
            if pack_create_event == "Create":
                name = pack_create_values["name"].replace("*", "_").replace("\\", "_").replace("/", "_").replace("(", "_").replace(")", "_").replace("\"", "_")
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    log(f"The pack \"{name}\" already exists!", "printerror")
                else:
                    author = pack_create_values["author"]
                    pack_version = pack_create_values["version"]
                    mc_version = pack_create_values["minecraftversion"]
                    modloader = pack_create_values["modloader"]
                    modloader_version = pack_create_values["modloaderversion"]
                    for val in [author, pack_version, mc_version, modloader, modloader_version]:
                        if val == "":
                            log("Error: you must fill in all the details!", "errorsg")
                        else:
                            os.mkdir(pack_root)
                            os.chdir(pack_root)
                            pack_create_command = runcmd([packwiz, "init", "--name", name, "--author", author, "--version", pack_version, "--mc-version", mc_version, "--modloader", modloader, f"--{modloader}-version", modloader_version])
                            with open(f"{pack_root}/.packwizignore", "w", encoding="UTF-8") as pwignore:
                                pwignore.write("*.zip\n*.mrpack\n.git/**\n.gitattributes\n.gitignore\n*.jar\nserver/**\n")
                            with open(f"{pack_root}/.gitattributes", "w", encoding="UTF-8") as gitattrib:
                                gitattrib.write("* -text\n")
                            with open(f"{pack_root}/.gitignore", "w", encoding="UTF-8") as gitignore:
                                gitignore.write("*.zip\n*.mrpack\n")
                            os.mkdir("mods")
                            if usegit:
                                runcmd(["git", "init"])
                                runcmd(["git", "add", "."])
                                runcmd(["git", "commit", "-m", f"\"Create pack {name}\""])
                            os.chdir(root)
                            if pack_create_command.returncode != 0:
                                log(f"There was an error creating the pack \"{name}\"!", "printerror")
                                log(f"error code {pack_create_command}", "debug")
                                shutil.rmtree(pack_root)
                            else:
                                log(f"Pack \"{name}\" created.", "printsg")
                        break
            pack_create_window.close()
            main_menu_window.UnHide()
        if main_menu_event == "Import an existing pack":
            pack_import = [
                [sg.T("Pack name:"), sg.In()],
                [sg.In(), sg.FileBrowse(file_types=(('Curseforge packs', '*.zip'),))],
                [sg.B("Import"), sg.B("Cancel")],
            ]
            main_menu_window.hide()
            pack_import_window = sg.Window("Import pack", pack_import)
            pack_import_event, pack_import_values = pack_import_window.read()
            if pack_import_event == "Import":
                name = pack_import_values[0]
                pack_root = f"{root}/instances/{name}"
                if os.path.isdir(pack_root):
                    log("Error: pack already exists!", "errorsg")
                else:
                    if pack_import_values[1] == "":
                        log("Error: path must not be empty!", "errorsg")
                    else:
                        os.mkdir(pack_root)
                        os.chdir(pack_root)
                        pack_import_command = runcmd([packwiz, "cf", "import", pack_import_values[1]])
                        if pack_import_command.returncode != 0:
                            log(f"Error while importing pack {name}!", "errorsg")
                        else:
                            log("Successfully imported pack.", "printsg")
                        pack_toml = opentoml(f"{pack_root}/pack.toml")
                        pack_toml["name"] = name
                        pack_toml["author"] = "Unknown"
                        pack_toml["version"] = "1.0.0"
                        dumptoml(f"{pack_root}/pack.toml", pack_toml)
            pack_import_window.close()
            main_menu_window.UnHide()
        if main_menu_event == "Modify pack":
            instances_list = ""
            for instance in os.listdir(f"{root}/instances"):
                instances_list = instances_list + instance + "\n"
            pack_list = [
                [sg.T("Packs:")],
                [sg.T(instances_list)],
                [sg.T("Pack Name:"), sg.In(key="packname")],
                [sg.B("Open")],
                [sg.B("Close")],
                [sg.B("Delete", button_color="red")],
            ]
            main_menu_window.hide()
            pack_list_window = sg.Window("Listing existing packs", pack_list)
            pack_list_event, pack_list_values = pack_list_window.read()
            pack_list_window.close()
            if pack_list_event == "Open":
                name = pack_list_values["packname"]
                pack_root = f"{root}/instances/{name}"
                if not os.path.isfile(f"{pack_root}/pack.toml"):
                    log(f"The pack \"{name}\" does not exist!", "printerror")
                else:
                    os.chdir(pack_root)
                    pack_toml = opentoml(f"{pack_root}/pack.toml")
                    pack_edit = [
                        [sg.T("Source:"), sg.Drop(["modrinth", "curseforge"], key="source")],
                        [sg.T("Mod: "), sg.In(key="mod")],
                        [sg.T("")],
                        [sg.B("Add Mod")],
                        [sg.B("Remove Mod")],
                        [sg.B("View Installed Mods")],
                        [sg.B("Export to Modrinth pack")],
                        [sg.B("Export to Curseforge pack")],
                        [sg.B("Refresh pack")],
                        [sg.B("Update all mods")],
                        [sg.B("Update mod")],
                        [sg.T("")],
                        [sg.T("Pack name:"), sg.In(pack_toml["name"], key="name")],
                        [sg.T(
                            "Warning: if you change the pack name, you may need to change the instance folder name yourself.")],
                        [sg.T("Author:"), sg.In(pack_toml["author"], key="author")],
                        [sg.T("Pack Version:"), sg.In(pack_toml["version"], key="version")],
                        [sg.T("Minecraft Version:"), sg.In(pack_toml["versions"]["minecraft"], key="minecraftversion")],
                        [sg.T("Changing modloader is currently unsupported.")],
                        [sg.B("Change")],
                        [sg.B("Close")],
                        [sg.T("")],
                    ]
                    pack_edit_window = sg.Window("Edit Pack", pack_edit)
                    while True:
                        pack_edit_event, pack_edit_values = pack_edit_window.read()
                        source = pack_edit_values["source"]
                        mod = pack_edit_values["mod"]
                        if pack_edit_event in (sg.WIN_CLOSED, "Close"):
                            pack_edit_window.close()
                            break
                        if pack_edit_event == "Add Mod":
                            os.chdir(pack_root)
                            mod_add_command = runcmd([packwiz, source, "install", mod])
                            if mod_add_command.returncode != 0:
                                log(f"There was an error adding mod \"{mod}\" from source \"{source}\"!", "printerror")
                                log(f"error code {mod_add_command}", "debug")
                            else:
                                log(f"Successfully added mod \"{mod}\" from source \"{source}\".", "printsg")
                                if usegit:
                                    runcmd(["git", "add", "."])
                                    runcmd(["git", "commit", "-m", f"\"Add {mod}\""])
                        if pack_edit_event == "Remove Mod":
                            os.chdir(f"{pack_root}")
                            mod_remove_command = runcmd([packwiz, "remove", mod])
                            if mod_remove_command.returncode != 0:
                                log(f"There was an error removing mod \"{mod}\"!", "printerror")
                                log(f"error code {mod_remove_command}", "debug")
                            else:
                                log(f"Mod \"{mod}\" successfully removed.", "printsg")
                                if usegit:
                                    runcmd(["git", "add", "."])
                                    runcmd(["git", "commit", "-m", f"\"Remove {mod}\""])
                        if pack_edit_event == "View Installed Mods":
                            mods_list = ""
                            for mod in os.listdir(f"{pack_root}/mods"):
                                mods_list = mods_list + mod[::-1].replace("lmot.", "", 1)[::-1] + "\n"
                            sg.popup(mods_list, title="Installed mods")
                        if pack_edit_event == "Export to Curseforge pack":
                            pack_export_command = runcmd([packwiz, "cf", "export"])
                            if pack_export_command.returncode != 0:
                                log(f"There was an error exporting the pack \"{name}\"!", "printerror")
                                log(f"error code {pack_export_command}", "debug")
                            else:
                                log(f"Pack \"{name}\" successfully exported.", "printsg")
                                if platform.system() == "Windows":
                                    os.startfile(pack_root)
                                elif platform.system() == "Darwin":
                                    runcmd(["open", pack_root])
                                else:
                                    runcmd(["xdg-open", pack_root])
                        if pack_edit_event == "Export to Modrinth pack":
                            pack_export_command = runcmd([packwiz, "mr", "export"])
                            if pack_export_command.returncode != 0:
                                log(f"There was an error exporting the pack \"{name}\"!", "printerror")
                                log(f"error code {pack_export_command}", "debug")
                            else:
                                log(f"Pack \"{name}\" successfully exported.", "printsg")
                                if platform.system() == "Windows":
                                    os.startfile(pack_root)
                                elif platform.system() == "Darwin":
                                    runcmd(["open", pack_root])
                                else:
                                    runcmd(["xdg-open", pack_root])
                        if pack_edit_event == "Refresh pack":
                            packwiz_refresh_command = runcmd([packwiz, "refresh"])
                            if packwiz_refresh_command.returncode != 0:
                                log("There was an error refreshing the pack!", "printerror")
                                log(f"error code {packwiz_refresh_command}", "debug")
                            else:
                                log("Successfully refreshed pack.", "printsg")
                            if usegit:
                                runcmd(["git", "add", "."])
                                runcmd(["git", "commit", "-m", f"\"Refresh pack {name}\""])
                        if pack_edit_event == "Update all mods":
                            packwiz_update_all_command = runcmd([packwiz, "update", "-a"])
                            if packwiz_update_all_command.returncode != 0:
                                log("There was an error updating all mods!", "printerror")
                            else:
                                log("Updating all mods succeeded.", "printsg")
                            if usegit:
                                runcmd(["git", "add", "."])
                                runcmd(["git", "commit", "-m", "\"Update all mods\""])
                        if pack_edit_event == "Update mod":
                            packwiz_update_mod_command = runcmd([packwiz, "update", mod])
                            if packwiz_update_mod_command.returncode != 0:
                                log("There was an error updating your mod(s)!", "printerror")
                            else:
                                log("Updating your mod(s) succeeded.", "printsg")
                            if usegit:
                                runcmd(["git", "add", "."])
                                runcmd(["git", "commit", "-m", f"\"Update {mod}\""])
                        if pack_edit_event == "Change":
                            if pack_edit_values["name"] != pack_toml["name"]:
                                os.chdir(root)
                                name = pack_edit_values["name"]
                                os.rename(pack_root, f"{root}/instances/{name}")
                                pack_root = f"{root}/instances/{name}"
                                os.chdir(pack_root)
                            pack_toml["name"] = pack_edit_values["name"]
                            pack_toml["author"] = pack_edit_values["author"]
                            pack_toml["version"] = pack_edit_values["version"]
                            pack_toml["versions"]["minecraft"] = pack_edit_values["minecraftversion"]
                            dumptoml(f"{pack_root}/pack.toml", pack_toml)
                            packwiz_refresh_command = runcmd([packwiz, "refresh"])
                            if usegit:
                                runcmd(["git", "add", "."])
                                runcmd(["git", "commit", "-m", "\"Modify pack details\""])
                            if packwiz_refresh_command.returncode != 0:
                                log("There was an error changing the pack details!", "printerror")
                                log(f"error code {packwiz_refresh_command}", "debug")
                            else:
                                log("Successfully changed pack details. Please change the instance folder name yourself if you have modified the name.", "printsg")
            if pack_list_event == "Delete":
                name = pack_list_values["packname"]
                pack_root = f"{root}/instances/{name}"
                if not os.path.isfile(f"{pack_root}/pack.toml"):
                    log(f"The pack \"{name}\" does not exist!", "printerror")
                else:
                    pack_delete_event = sg.popup_yes_no("WARNING: THIS WILL DELETE ALL OF THIS PACK'S DATA."
                                                        "\nONLY PRESS YES IF YOU UNDERSTAND THIS. ARE YOU SURE?", title="Are you sure?")
                    if pack_delete_event == "Yes":
                        os.chdir(root)
                        shutil.rmtree(f"{pack_root}")
                        log(f"Pack {name} deleted.", "printsg")
            main_menu_window.UnHide()
        if main_menu_event == "Settings":
            modify_settings = [
                [sg.T("Backend:"), sg.Drop(["tk", "qt"], key="backend", default_value=current_backend)],
                [sg.Drop(sg.theme_list(), key="theme", default_value=settings[f"{current_backend}theme"])],
                [sg.CB("Use git", key="git", default=settings["usegit"])],
                [sg.B("Reset settings")],
                [sg.B("Ok")]
            ]
            main_menu_window.hide()
            modify_settings_window = sg.Window("Modify settings", modify_settings)
            modify_settings_event, modify_settings_values = modify_settings_window.read()
            if modify_settings_event == "Reset settings":
                if os.path.isfile(f"{root}/settings.toml"):
                    os.remove(f"{root}/settings.toml")
                createsettings(f"{root}/settings.toml")
                log("Successfully reset settings.", "printsg")
                sys.exit()
            elif modify_settings_event == "Ok":
                if modify_settings_values["backend"] in valid_backends and modify_settings_values["theme"] in sg.theme_list():
                    settings["usegit"] = modify_settings_values["git"]
                    usegit = modify_settings_values["git"]
                    dumptoml(f"{root}/settings.toml", settings)
                    if modify_settings_values["backend"] != settings["backend"] or modify_settings_values["theme"] != settings[f"{current_backend}theme"]:
                        settings["backend"] = modify_settings_values["backend"]
                        settings[f"{current_backend}theme"] = modify_settings_values["theme"]
                        dumptoml(f"{root}/settings.toml", settings)
                        log("Restart to see effect.", "printsg")
                        sys.exit()
                    else:
                        main_menu_window.UnHide()
                    modify_settings_window.close()
                else:
                    log("Invalid settings!", "printerror")
            modify_settings_window.close()
        if main_menu_event == "Download packwiz":
            if platform.system() == "Windows":
                webbrowser.get("windows-default").open("https://github.com/comp500/packwiz/#installation")
            else:
                webbrowser.open("https://github.com/comp500/packwiz/#installation")

if __name__ == "__main__":
    main()
