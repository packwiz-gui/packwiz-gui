import os

if not os.path.isfile(".setup"):
    import package_toml
    package_toml.setup()
    print("Setup complete.")
else:
    print("Setup already complete.")
    print("If you want to re-setup, delete .setup file.")