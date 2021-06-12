# ---------------Module/Package--------------- #
import os
import pyperclip
import re
# ---------------- Function ------------------ #


def pause():
    os.system('pause')


def cls():
    os.system('cls')


def password_genrator():
    os.system('color a')
    os.system('Title Password Generator by Limon®')
    cls()
    import random

    character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%=-"
    while True:
        password_length = int(input("Password Length >> "))
        password_count = int(input("How many password do you want >> "))
        for num in range(0, password_count):
            num += 1
            password = ""
            for length in range(0, password_length):
                password_character = random.choice(character)
                password += password_character
            print(f"Here is your password no. {num} >> ", password)
            print()
        input("Press 'Enter' key to exit the Password Generator...")
        cls()
        break


def guessing_game():
    os.system('color f0')
    os.system('Title Guessing Game by Limon®')
    cls()
    import random

    count_guess = 0
    print()
    low = int(input("Enter the low range number --> "))
    high = int(input("Enter the high range number --> "))
    cls()
    if low > high:
        print("Invalid range! Try again")
        guessing_game()
    else:
        store = random.randrange(low, high)
        print("""===========Welcome to the Guessing game===========

        * exit = To exit the game
        * s = To surrender
        * help = for game rules
        * If you guess higher than the secret number it will tell you to 'GUESS LOW!'
        * if you guess lower than the secret number it will tell you to  'GUESS HIGH!'
        * And you will get 20 attempts to guss the game! So good luck!
        """)
        print()
        print()
        while True:
            guess = input("Guess -->").lower()
            count_guess += 1
            if str(guess) == 's':
                print(f"Okay! No problem. The number was {store}")
                print()
                input("Press Enter key to exit the game...")
                break
            elif str(guess) == 'quite' or guess == 'exit':
                break
            elif str(guess) == 'help':
                print("""===========Welcome to the Guessing game===========

                        * exit = To exit the game
                        * s = To surrender
                        * help = for game rules
                        * If you guess higher than the secret number it will tell you to 'GUESS LOW!'
                        * if you guess lower than the secret number it will tell you to  'GUESS HIGH!'
                        * And you will get 20 attempts to guss the game! So good luck!
                        """)
                print()
                print()
            elif count_guess == 20:
                print(
                    f"You attempt has expired! So the number was {store}. Good luck for next time!")
                print()
                input("Press Enter key to exit the game....")
                break
            elif int(guess) > store:
                print("GUESS LOW!")
            elif int(guess) < store:
                print("GUESS HIGH!")
            elif int(guess) == store:
                print(f"""Congratulation! You have won the game! It took {count_guess} attempts.""")
                print()
                input("Press Enter key to exit the game...")
                cls()
                break


def google_drive():
    os.system('color a')
    os.system('Title Google Drive Download Link Generator by Limon®')
    cls()
    data = input("Enter your google drive link or exit --> ")
    if data == 'exit' or data == 'back':
        pass
    else:
        pattern_google_auth = re.compile(
            r'(https://)?drive\.google\.com(/file/d/|/uc\?id=).+(/view\?usp=sharing|&export=download|/view).*')
        matches_auth = pattern_google_auth.match(data)
        if matches_auth:
            patter_google_url_download = re.compile(
                r'(https://)?drive\.google\.com/uc\?id=.+&export=download')
            matches_download = patter_google_url_download.match(data)
            if matches_download:
                print("""It's a download link of Google Drive!
        Enjoy! :) """)
                pause()
            else:
                data = data.replace('file/d/', 'uc?id=')
                data = data.replace('/view?usp=sharing', '&export=download')
                data = data.replace('/view', '&export=download')
                print()
                print()
                pyperclip.copy(data)
                print("Download link has been copied to your clipboard")
                pause()
        else:
            print("""Error Link!
    Make sure your link is in this Format:
 https://drive.google.com/file/d/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/view?usp=sharing""")
            pause()
            google_drive()


def hifi():
    os.system('Title Hi-Fi')
    os.system('color 09')
    messege_menu = """
                                    ------------------------------------------
                                             [1] Hide File or Folder
                                             [2] Show File or Folder
                                             [0] Exit
                                    ------------------------------------------


    """

    def hidef():
        cls()
        path = input("Drag your file or folder here >>")
        os.system(f'Attrib +h +s +r {path}')
        print("Done!")
        print()
        pause()
        cls()
        name = input('Enter the Path Text File name >> ')
        with open(f'{name}.txt', 'w') as text:
            text.write(f"Path = {path}\n \nCopy the text and fill on the show option to unhide")

    def showf():
        cls()
        path = input("Paste your path here >> ")
        os.system(f"Attrib -h -s -r {path}")
        print("Done!")
        pause()

    while True:
        cls()
        print(messege_menu)
        menu = input(">>")
        if int(menu) == 1:
            hidef()
        elif int(menu) == 2:
            showf()
        elif int(menu) == 0:
            break
        elif int(menu) == -1:
            print("Invalid command!")
        else:
            print("Invalid command!")


while True:
    os.system('color 07')
    os.system('Title Terminal by Limon®')
    cls()
    command = input(">>").lower()
    if command == 'cls' or command == 'clear' or command == 'clean':
        cls()
    elif command.find('password') != -1 or command.find('generator') != -1 or command == 'pg' or command == 'pwdg' or command == 'pwg':
        password_genrator()
    elif command.find('google') != -1 or command.find('drive') != -1 or command == 'gd':
        google_drive()
    elif command.find('guessing') != -1 or command.find('guess') != -1 or command == 'game' or command == 'gg':
        guessing_game()
    elif command.find('hide') != -1 or command == 'hifi' or command == 'hi-fi' or command == 'hi' or command == 'hf':
        hifi()
    elif command == 'help':
        cls()
        with open('help.txt', 'r') as file:
            message = file.read()
            print(message)
            print()
            print()
            pause()
    elif command == 'exit' or command == 'close' or command == 'quite' or command == 'leave':
        exit()
    else:
        cls()
        os.system("color 4")
        os.system('Title Terminal by Limon®')
        print("Invalid command!")
        pause()
