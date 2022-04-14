import sys
import colorama
from colorama import Fore
import os
import random
import string

# get full path of log dir
logs = sys.path[0] + '/logs' if os.path.isdir(sys.path[0] + '/logs') else os.getcwd() + '/logs'
if not os.path.isdir(f"{logs}"):
    os.mkdir(f"{logs}")
if os.path.isfile(f"{logs}/latest.log"):
    id = random.choices(string.ascii_uppercase + string.digits, k=11)
    os.rename(f"{logs}/latest.log", f"{logs}/{''.join(id)}.log.old")

def err(msg = ''):
    if msg != '':
        print(Fore.RED + '[ERR] ' + msg + Fore.WHITE)
        with open(f"{logs}/latest.log", "a") as log:
            log.write(f"[ERR] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty")   
def inf(msg = ''):
    if msg != '':
        print(Fore.WHITE + '[INF] ' + msg + Fore.WHITE)
        with open(f"{logs}/latest.log", "a") as log:
            log.write(f"[INF] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def dbg(msg = '', send = False):
    if msg != '': 
        print(Fore.LIGHTBLACK_EX + '[DBG] ' + msg + Fore.WHITE)
        with open(f"{logs}/latest.log", "a") as log:
            log.write(f"[DBG] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def wrn(msg = ''):
    if msg != '': 
        print(Fore.LIGHTYELLOW_EX + '[WRN] ' + msg + Fore.WHITE)
        with open(f"{logs}/latest.log", "a") as log:
            log.write(f"[WRN] {msg} \n")
    else:
        err("INTERNAL ERROR: msg parameter is empty")