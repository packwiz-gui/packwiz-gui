import colorama
from colorama import Fore

def err(msg = ''):
    if msg != '':
        print(Fore.RED + '[ERR] ' + msg + Fore.WHITE)
    else:
        err("INTERNAL ERROR: msg parameter is empty")   
def inf(msg = ''):
    if msg != '':
        print(Fore.WHITE + '[INF] ' + msg + Fore.WHITE)
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def dbg(msg = '', send = False):
    if msg != '': 
        print(Fore.LIGHTBLACK_EX + '[DBG] ' + msg + Fore.WHITE)
    else:
        err("INTERNAL ERROR: msg parameter is empty") 
def wrn(msg = ''):
    if msg != '': 
        print(Fore.LIGHTYELLOW_EX + '[WRN] ' + msg + Fore.WHITE)
    else:
        err("INTERNAL ERROR: msg parameter is empty")