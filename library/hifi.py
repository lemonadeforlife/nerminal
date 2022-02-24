# ---------------Module/Package--------------- #
import os
import sys
from .cli_func import *
# ---------------- Function ------------------ #
title('HiFi')


def hidef(path):
    clear()
    if sys.platform == 'win32':
        os.system(f'Attrib +h +s +r {path}')
    elif sys.platform == 'linux':
        if path.rfind("'") != -1:
            h_num = path.rfind("'")
            s_num = path.rfind("/")
            data1 = path[s_num+1:h_num]
            data2 = f'.{path[s_num+1:h_num]}'
            new_path = path.replace(data1, data2)
            os.system(f"mv {path} {new_path}")
        else:
            s_num = path.rfind("/")
            data1 = path[s_num+1:]
            data2 = f'.{path[s_num+1:]}'
            new_path = path.replace(data1, data2)
            os.system(f"mv {path} {new_path}")

    elif sys.platform == 'darwin':  # MAC OS
        pass  # I don't have any MAC sooooooo.....!!!!
    else:
        print("Sorry I don't what is happening...!")
    print("Done!")
    print()
    pause()
    clear()


def hifi():
    title('Hi-Fi')
    if sys.platform == 'win32' or sys.platform == 'linux':
        pass
    else:
        print("Doesn't support this feature on this OS!")
        pause()
        return None
    messege_menu = """------------------------------------------
            [1] Hide File or Folder
            [0] Exit
------------------------------------------"""

    while True:
        clear()
        print(messege_menu)
        menu = input(">>")
        if int(menu) == 1:
            path = input("Drag your file or folder here >>")
            hidef(path)
        elif int(menu) == 0:
            break
        elif int(menu) == -1:
            clear()
            print("Invalid command!")
            pause()
        else:
            clear()
            print("Invalid command!")
            pause()


if __name__ == '__main__':
    print("It won't run this way :(")
