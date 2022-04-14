import colorama
from colorama import Fore
import os
import random
import string

if not os.path.isdir("logs"):
    os.mkdir("logs")
if os.path.isfile("logs/latest.log"):
    id = random.choices(string.ascii_uppercase + string.digits, k=11)
    os.rename("logs/latest.log", f"logs/{''.join(id)}.log.old")

def err(msg = ''):
    if msg != '':
        print(Fore.RED + '[ERR] ' + msg + Fore.WHITE)
        with open("logs/latest.log", "a") as log:
            log.write(f"[ERR] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty")   
def inf(msg = ''):
    if msg != '':
        print(Fore.WHITE + '[INF] ' + msg + Fore.WHITE)
        with open("logs/latest.log", "a") as log:
            log.write(f"[INF] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def dbg(msg = '', send = False):
    if msg != '': 
        print(Fore.LIGHTBLACK_EX + '[DBG] ' + msg + Fore.WHITE)
        with open("logs/latest.log", "a") as log:
            log.write(f"[DBG] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def wrn(msg = ''):
    if msg != '': 
        print(Fore.LIGHTYELLOW_EX + '[WRN] ' + msg + Fore.WHITE)
        with open("logs/latest.log", "a") as log:
            log.write(f"[WRN] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty")