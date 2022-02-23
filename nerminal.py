# ---------------Module/Package--------------- #
import os
import sys
from library import *
# ---------------- Function ------------------ #

while True:
    title()
    clear()
    command = input(">>").lower()
    if command in ['cls', 'clear', 'clean']:
        clear()
    elif command in ['password', 'generator', 'pg', 'pwdg', 'pwg', 'password generator']:
        password_genrator()
    elif command in ['google', 'drive', 'gd']:
        google_drive()
    elif command in ['guessing', 'guess', 'game', 'gg']:
        guessing_game()
    elif command in ['hide', 'hifi', 'hi-fi', 'hi', 'hf']:
        hifi()
    elif command in ['img', 'pic', 'picture', 'jpg', 'png', 'webp', 'gif', 'image', 'photo', 'image convert', 'image converter']:
        from library import image_converter
    elif command == 'help':
        clear()
        with open('help.txt', 'r') as file:
            message = file.read()
            print(message)
            print()
            print()
            pause()
    elif command in ['exit', 'close', 'quite', 'leave']:
        sys.exit()
    else:
        clear()
        title('Terminal by Limon®')
        print("Invalid command!")
        pause()
