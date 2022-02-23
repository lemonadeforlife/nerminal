# ---------------Module/Package--------------- #
import os
import sys
import random
from .cli_func import *
# ---------------- Function ------------------ #


def password_genrator():
    title('Password Generator')
    clear()

    character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\
!@#%=-"
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
        pause()
        clear()
        break


if __name__ == '__main__':
    print("It won't run this way :(")
