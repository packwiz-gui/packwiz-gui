import PySimpleGUI as sg
import os
import platform

sg.theme('DarkGrey9')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Pack name:'), sg.InputText()],
            [sg.Text('Author:'), sg.InputText()],
            [sg.Text('Pack Version:'), sg.InputText()],
            [sg.Text('Minecraft Version:'), sg.InputText()],
            [sg.Text('Modloader (\'forge\' or \'fabric\'):'), sg.InputText()],
            [sg.Text('Modloader Version:'), sg.InputText()],
            [sg.Button("Create")]]

# Create the Window
window = sg.Window('New Packwiz Pack', layout)

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
        os.mkdir('instances/{}', str(values[0]))
        os.chdir('instances/{}', str(values[0]))
        if linux_distribution() == '':
            if platform.system() == 'Windows':
                os.system('\"bin\packwiz init\" --name "{}" --author "{}" --version "{}" --mc-version "{}" --modloader "{}" --{}-version "{}"', str(values[0]), str(values[1]), str(values[2]), str(values[3]), str(values[4]), str(values[4]), str(values[5]))
            if platform.system() == 'Darwin':
                os.system('\"bin\packwiz init\" --name "{}" --author "{}" --version "{}" --mc-version "{}" --modloader "{}" --{}-version "{}"', str(values[0]), str(values[1]), str(values[2]), str(values[3]), str(values[4]), str(values[4]), str(values[5]))
        else:
            os.system('bin/packwiz init')
    os.chdir('../..')
            

window.close()
