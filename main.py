import PySimpleGUI as sg
import os
import platform
import subprocess

root = os.getcwd()
sg.theme('DarkGrey9')   # Add a touch of color
# All the stuff inside your window.
new_pack_layout = [  [sg.Text('Pack name:'), sg.InputText()],
            [sg.Text('Author:'), sg.InputText()],
            [sg.Text('Pack Version:'), sg.InputText()],
            [sg.Text('Minecraft Version:'), sg.InputText()],
            [sg.Text('Modloader (\'forge\' or \'fabric\'):'), sg.InputText()],
            [sg.Text('Modloader Version:'), sg.InputText()],
            [sg.Button("Create")]]
pack_layout = [  [sg.Text('Pack name:'), sg.InputText()],
            [sg.Text('Author:'), sg.InputText()],
            [sg.Text('Pack Version:'), sg.InputText()],
            [sg.Text('Minecraft Version:'), sg.InputText()],
            [sg.Text('Modloader (\'forge\' or \'fabric\'):'), sg.InputText()],
            [sg.Text('Modloader Version:'), sg.InputText()],
            [sg.Button("Create")]]

# Create the Window
window = sg.Window('New Packwiz Pack', new_pack_layout)

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return ""
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Create':
        #os.mkdir('instances/{}', str(values[0]))
        #os.chdir('instances/{}', str(values[0]))
        if linux_distribution() == '':
            if platform.system() == 'Windows':
                name = values[0]
                author = values[1]
                pack_version = values[2]
                mc_version = values[3]
                modloader = values[4]
                modloader_version = values[5]

                os.mkdir("instances/" + name)
                os.chdir("instances/" + name)
                #subprocess.Popen('\"bin\packwiz\"', 'init', '--name', values[0], '--author', values[1], '--version', values["2"], '--mc-version', values["3"], '--modloader', "fabric", '--fabric--version', values["5"], 'instances/', values["Pack name:"])
                #os.system('\"bin\packwiz init\" --name "{}" --author "{}" --version "{}" --mc-version "{}" --modloader "{}" --{}-version "{}"', name, author, pack_version, mc_version, modloader, modloader, modloader_version)
                os.system(root + "/bin/packwiz init " + '--name ' + name + ' --author ' + author + ' --version ' + pack_version + ' --mc-version ' + mc_version + ' --modloader ' + modloader + ' --' + modloader + '-version ' + modloader_version)
            if platform.system() == 'Darwin':
                #os.system('\"bin\packwiz init\" --name "{}" --author "{}" --version "{}" --mc-version "{}" --modloader "{}" --{}-version "{}"', str(values[0]), str(values[1]), str(values[2]), str(values[3]), str(values[4]), str(values[4]), str(values[5]))
                print("macOS")
    os.chdir('../..')
            

window.close()