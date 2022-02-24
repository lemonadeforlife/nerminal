# ---------------Module/Package--------------- #
from PIL import Image
from .cli_func import *
# -------------------------------------------- #
title('Image Converter')
loop = True
while loop:
    clear()
    message = f"1.jpeg\n2.jpg\n3.png"
    print(message)
    try:
        choice = input('Convert to? ')
        if choice == 'jpeg' or choice == '1':
            loop = False
            format = 'jpeg'
        elif choice == 'jpg' or choice == '2':
            loop = False
            format = 'jpg'
        elif choice == 'png' or choice == '3':
            loop = False
            format = 'png'
        elif int(choice) == 1:
            loop = False
            format = 'jpeg'
        elif int(choice) == 2:
            loop = False
            format = 'jpg'
        elif int(choice) == 3:
            loop = False
            format = 'png'
        else:
            clear()
            print(
                f'You were command was:{choice}!\n Which is an invalid command')
            pause()
    except Exception as e:
        clear()
        print(f'Your error was: {e}')
        pause()

img = input('Drag or Enter image path>').strip()

img = img.replace("'", '')
pic = Image.open(img)
if img.rfind('.') != -1:
    x = img.rfind('.')
else:
    print('Invalid file!')
img_path = img[:x+1]
file_format = f'{img_path}{format}'
pic.save(file_format)
print('Successfully converted the file!')
pause()

if __name__ == '__main__':
    print("It won't work this way")
else:
    pass
