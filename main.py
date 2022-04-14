from email.policy import default
import os
import platform
import sys
import dearpygui.dearpygui as dpg
import dearpygui as dpgcore
import toml
import logger
import tomli_w
import tomli
import subprocess as sp
from package_toml import data
global pack_name
def dumptoml(filename, var):
    """
    Takes in dict and filename. Dumps dict to file as toml.
    Args:
    filename: filename of file (with path) to dump to
    var: dict to dump from
    """
    with open(filename, "wb") as toml_file:
        return tomli_w.dump(var, toml_file)
root = sys.path[0] if os.path.isdir(sys.path[0]) else os.getcwd()
if platform.system() == "Windows":
    root = sys.path[0] if os.path.isdir(sys.path[0]) else os.getcwd()
    instances = f"{root}\\instances"
    packwiz = f"{root}\\bin\\packwiz.exe"
else:
    root = sys.path[0] if os.path.isdir(sys.path[0]) else os.getcwd()
    instances = f"{root}/instances"
    packwiz = f"{root}/bin/packwiz"

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

if not os.path.isdir("bin"):
    logger.err("Bin folder not found! Please create bin folder and place the packwiz executable in it.")
    sys.exit()
else:
    if not os.path.isfile(packwiz):
        logger.err("Packwiz executable not found! Please place the packwiz executable in bin folder.")
        sys.exit()
if not os.path.isdir(instances):
    logger.wrn("Instances folder not found! Creating instances folder.")
    os.mkdir(instances)

def save_callback():
    print("Saving...")

    
    

def dumptoml(filename, var):
    """
    Takes in dict and filename. Dumps dict to file as toml.
    Args:
    filename: filename of file (with path) to dump to
    var: dict to dump from
    """
    with open(filename, "wb") as toml_file:
        return tomli_w.dump(var, toml_file)

if os.path.isfile(f"{root}/config.toml"):
    with open(f"{root}/config.toml", "rb") as toml_file:
        config = tomli.load(toml_file)
else:
    logger.wrn("config.toml not found. Creating config.toml...")
    createconfig(f"{root}/config.toml")
    with open(f"{root}/config.toml", "rb") as toml_file:
        config = tomli.load(toml_file)
if config["debug_mode"] == "true" or config["debug_mode"] == "True" or config["debug_mode"] == "TRUE" or config["debug_mode"] == True:
    debug_mode = True
    logger.dbg("Debug mode enabled.", debug_mode)
elif config["debug_mode"] == "false" or config["debug_mode"] == "False" or config["debug_mode"] == "FALSE" or config["debug_mode"] == True:
    debug_mode = False
else:
    logger.err("Invalid debug mode in config.toml. Force crashing.")
    raise ValueError("Invalid debug_mode value.")

def create_pack_callback(sender, app_data):
    if platform.system() == "Windows":
        logger.inf("Creating pack...")
        #sp.call(["./bin/packwiz.exe", 
        #"init", 
        #"--name", dpg.get_value("pack_name"), 
        #"--version", dpg.get_value("pack_version"), 
        #"--author", dpg.get_value("pack_author"),
        #"--mcversion", dpg.get_value("pack_mc_version"),
        #"--modloader", dpg.get_value("pack_modloader"),
        #f"--{dpg.get_value('pack_modloader')}-version", dpg.get_value("pack_modloader_version")
        #], shell=True)
        # Convert above to os.system()
        if os.path.isdir(f"{instances}/{dpg.get_value('pack_name')}"):
            logger.err(f"Pack with name {dpg.get_value('pack_name')} already exists!")
        else:
            os.mkdir(f"{instances}/{dpg.get_value('pack_name')}")
            os.chdir(f"{instances}/{dpg.get_value('pack_name')}")
            os.system("..\\..\\bin\packwiz.exe init --name " + dpg.get_value("pack_name") + " --version " + dpg.get_value("pack_version") + " --author " + dpg.get_value("pack_author") + " --mc-version " + dpg.get_value("pack_mc_version") + " --modloader " + dpg.get_value("pack_modloader") + " --" + dpg.get_value("pack_modloader") + "-version " + dpg.get_value("pack_modloader_version"))
        #logger.dbg(dpg.get_item_user_data(29), debug_mode)
        logger.dbg(str(app_data), debug_mode)
       
    

def create_new_pack_callback():
    logger.dbg("Opening create new pack window", debug_mode)
    with dpg.window(label="Create A New Pack", width=400, height=300):
        
        dpg.add_input_text(tag="pack_name", label="Pack Name", tracked=True, default_value="testing123")
        dpg.add_input_text(tag="pack_version", label="Pack Version")
        dpg.add_input_text(tag="pack_author", label="Pack Author")
        dpg.add_input_text(tag="pack_mc_version", label="Minecraft Version")
        dpg.add_listbox(tag="pack_modloader", label="Modloader", items=["forge", "fabric"])
        dpg.add_input_text(tag="pack_modloader_version", label="Modloader Version")

        dpg.add_button(tag="create_pack", label="Create Pack", callback=create_pack_callback)
        dpg.add_button(tag="cancel", label="Cancel", callback=dpg.close_window)


def load_pack_callback():
    print("Loading package...")
    dpg.show_window("load_pack")

def settings_callback():
    print("Settings...")
    dpg.show_window("settings")




dpg.create_context()

dpg.create_viewport(title="Packwiz GUI")

dpg.setup_dearpygui()



with dpg.window(label="Main Menu", width=300, height=300, tag="main_menu"):

    dpg.add_text("packwiz-gui v{}".format(data.version))

    dpg.add_button(label="Save", callback=save_callback)

    dpg.add_button(label="Create a new pack", callback=create_new_pack_callback)

    dpg.add_button(label="Load a pack", callback=load_pack_callback)

    dpg.add_button(label="Settings", callback=settings_callback)

    dpg.add_button(label="Exit", callback=sys.exit)



dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()