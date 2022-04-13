import os
import subprocess as sp
import sys as python

import toml

def read_toml(filename):
    """
    Reads toml file and returns dict.
    Args:
    filename: filename of toml file to read.
    """
    if filename == "app.toml":
        try:
            return toml.load(filename)
        except toml.TomlDecodeError:
            raise InvalidAppMetaData("Invalid app.toml file.")
    return toml.load(filename)


# Custom exceptions
class NoAppMetaData(Exception):
    """
    Raised when no metadata is found.
    """
    pass

class InvalidAppMetaData(Exception):
    """
    Raised when metadata is invalid.
    """
    pass

class data:
    if os.path.isfile("app.toml"):
        app_toml = read_toml("app.toml")
    else:
        raise NoAppMetaData("app.toml not found.")
    version = app_toml["app"]["version"]
    title = app_toml["app"]["title"]
    name = title
    description = app_toml["app"]["description"]
    authors = app_toml["app"]["authors"]
    license = app_toml["app"]["license"]
    git_repo = app_toml["app"]["git_repo"]
    website = app_toml["app"]["website"]


def pip_install(package):
    """
    Installs package using pip.
    Args:
    package: package to install.
    """
    sp.call(["pip", "install", package])
app_toml = read_toml("app.toml")
app = app_toml["app"]
dependencies = app_toml["dependencies"]
def setup():
    if os.path.exists("requirements.txt"):
        # Remove old requirements.txt
        print("Removing requirements.txt")
        os.remove("requirements.txt")
    print("Writing requirements.txt...")
    for dependency in dependencies:
        # Write requirements.txt
   
        with open("requirements.txt", "a") as req:
            req.write(dependency + "\n")
    # Install requirements.txt
    print("Installing requirements.txt...")
    sp.call(["pip", "install", "-r", "requirements.txt"])
    # Delete requirements.txt
    print("Removing requirements.txt")
    os.remove("requirements.txt")
    # Add blank .setup file
    print("Creating .setup file...")
    with open(".setup", "w") as setup:
        setup.write("")