# packwiz-gui


## Build Instructions

1. Clone the repo: `git clone https://github.com/ExoPlant/packwiz-gui`. Keep in mind you need git for this.
2. Download the [packwiz](https://github.com/comp500/packwiz/) binary for the OS you're using it for and put it 
in the `bin` folder (created when you start packwiz-gui).
3. Install `PySimpleGUI` using pip3: `pip3 install PySimpleGUI`.
4. Run the `packwiz_gui.py` file using `python` on Windows or `python3` on Unix-based OSes (On Linux if you have 
python3 you can double-click to start it, though it's not recommended).
5. Enjoy!

Linux and Mac users: If you want packwiz-gui to integrate with your Linux Qt/KDE theme or MacOS, run 
`patch packwiz_gui.py unix-qt-patch.patch -o packwiz_gui_qt.py` and use the new `packwiz-gui-qt.py` file.
Also, install `PySimpleGUIQt` using `pip3 install PySimpleGUIQt`.
