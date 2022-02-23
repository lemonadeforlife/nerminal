# ---------------Module/Package--------------- #
import os
import sys
import random
from .cli_func import *
# ---------------- Function ------------------ #


def guessing_game():
    title('Guessing Game')
    clear()
    count_guess = 0
    print()
    low = int(input("Enter the low range number --> "))
    high = int(input("Enter the high range number --> "))
    clear()
    if low > high:
        print("Invalid range! Try again")
        guessing_game()
    else:
        store = random.randrange(low, high)
        print("""===========Welcome to the Guessing game===========

        * exit = To exit the game
        * s = To surrender
        * help = for game rules
        * If you guess higher than the secret number it will tell you to \
'GUESS LOW!'
        * if you guess lower than the secret number it will tell you to \
'GUESS HIGH!'
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
                pause()
                break
            elif str(guess) == 'quite' or guess == 'exit':
                break
            elif str(guess) == 'help':
                print("""===========Welcome to the Guessing game===========

                        * exit = To exit the game
                        * s = To surrender
                        * help = for game rules
                        * If you guess higher than the secret number it will \
tell you to 'GUESS LOW!'
                        * if you guess lower than the secret number it will \
tell you to  'GUESS HIGH!'
                        * And you will get 20 attempts to guss the game! So \
good luck!
                        """)
                print()
                print()
            elif count_guess == 20:
                print(
                    f"You attempt has expired! So the number was {store}. Good\
 luck for next time!")
                print()
                pause()
                break
            elif int(guess) > store:
                print("GUESS LOW!")
            elif int(guess) < store:
                print("GUESS HIGH!")
            elif int(guess) == store:
                print(f"""Congratulation! You have won the game! It took \
{count_guess} attempts.""")
                print()
                pause()
                clear()
                break


if __name__ == '__main__':
    print("It won't run this way :(")
