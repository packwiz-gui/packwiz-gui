import os
import tomli
import tomli_w

def main(root, pack_root=None, opentoml=None, dumptoml=None):
    def datafix():
        pwgui_toml = opentoml("pwgui.toml")
        if pwgui_toml["version"] == "1.2.0":
            # Do stuff
            pwgui_toml["version"] = "1.3.0"
        if pwgui_toml["version"] == "1.3.0":
            # Do stuff
            pass
        dumptoml("pwgui.toml", pwgui_toml)
    if pack_root == None:
        for each in os.listdir(f"{root}/instances"):
            os.chdir(f"{root}/instances/{each}")
            datafix()
    else:
        os.chdir(pack_root)
        datafix()
