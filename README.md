# packwiz-gui


## Build Instructions

1. Clone the repo `git clone https://github.com/ExoPlant/packwiz-gui/`
2. Download the [packwiz](https://github.com/comp500/packwiz/) binary for the OS you're building for and put it in the `bin` folder. If it's Windows, it should be named `packwiz.exe`. If you downloaded the macOS or Linux binary, it should be `packwiz`.
3. Install `PySimpleGUI` using pip3: `pip3 install PySimpleGUI`.
4. Run the `main.py` file using `python` on Windows or `python3` on another OS (On Linux if you have python3 you can double-click).
5. Enjoy!

Linux and Mac users: If you want packwiz-gui to integrate with your Linux Qt/KDE theme or MacOS, apply `unix-qt-patch.patch` to the script using `patch packwiz-gui.py unix-qt-patch.patch -o packwiz-gui-qt.py` and use the new `packwiz-gui-qt.py` file.
Also install `PySimpleGUIQt` using `pip3 install PySimpleGUIQt`.
