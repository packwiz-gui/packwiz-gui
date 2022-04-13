import os
import dearpygui.dearpygui as dpg
import toml
import logger
import tomli_w
import tomli
from package_toml import data

global debug_menu_active
def dumptoml(filename, var):
    """
    Takes in dict and filename. Dumps dict to file as toml.
    Args:
    filename: filename of file (with path) to dump to
    var: dict to dump from
    """
    with open(filename, "wb") as toml_file:
        return tomli_w.dump(var, toml_file)

def createconfig(filename):
    """
    Create settings.
    Args:
    filename: filename of settings toml file.
    """
    settings = {
        # Be careful. If you break something, delete the file and it will be recreated.
        "debug_mode": "false"
    }
    dumptoml(filename, settings)

def save_callback():
    print("Saving...")

def debug_menu():
    """
    Debug menu.
    """
    if not debug_menu_active:
        dpg.add_child_window(label="Debug", width=300, height=300, parent="main_menu")
        debug_menu_active = True
    else:
        dpg.remove_child_window(label="Debug")
        debug_menu_active = False

def dumptoml(filename, var):
    """
    Takes in dict and filename. Dumps dict to file as toml.
    Args:
    filename: filename of file (with path) to dump to
    var: dict to dump from
    """
    with open(filename, "wb") as toml_file:
        return tomli_w.dump(var, toml_file)

if os.path.isfile("config.toml"):
    with open("config.toml", "rb") as toml_file:
        config = tomli.load(toml_file)
else:
    logger.wrn("config.toml not found. Creating config.toml...")
    createconfig("config.toml")
    with open("config.toml", "rb") as toml_file:
        config = tomli.load(toml_file)
if config["debug_mode"] == "true" or config["debug_mode"] == "True" or config["debug_mode"] == "TRUE" or config["debug_mode"] == True:
    debug_mode = True
    logger.dbg("Debug mode enabled.", debug_mode)
elif config["debug_mode"] == "false" or config["debug_mode"] == "False" or config["debug_mode"] == "FALSE" or config["debug_mode"] == True:
    debug_mode = False
else:
    logger.err("Invalid debug mode in config.toml. Force crashing.")
    raise ValueError("Invalid debug_mode value.")



dpg.create_context()

dpg.create_viewport()

dpg.setup_dearpygui()



with dpg.window(label="Main Menu", width=300, height=300, tag="main_menu"):

    dpg.add_text("packwiz-gui v{}".format(data.version))

    dpg.add_button(label="Save", callback=save_callback)

    dpg.add_input_text(label="string")
    debug_menu_active = False
    if debug_mode == True:
        dpg.add_text("Debug mode is on.")
        debug_menu_active = False
        dpg.add_button(label="Debug menu", callback=debug_menu)

    dpg.add_slider_float(label="float")



dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()