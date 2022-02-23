import sys
import os
from getch import pause


def clear():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system('clear')


def title(name=None):
    if sys.platform == 'win32':
        if name == None:
            os.system(f"title Terminal by Limon®")
        else:
            os.system(f"title Terminal by Limon®: {name}")
    else:
        if name == None:
            sys.stdout.write(f"\x1b]2;Terminal by Limon®\x07")
        else:
            sys.stdout.write(f"\x1b]2;Terminal by Limon®: {name}\x07")
