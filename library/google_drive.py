# ---------------Module/Package--------------- #
import os
import sys
import pyperclip
import re
from .cli_func import *
# ---------------- Function ------------------ #


def google_drive():
    title('Google Drive Download Link Converter')
    clear()
    data = input("Enter your google drive link or exit --> ")
    if data in ['exit', 'back']:
        pass
    else:
        pattern_google_auth = re.compile(
            r'(https://|www\.|https://www\.)?drive\.google\.com(/file/d/|/uc\?id=|/drive/folders).+(/view\?usp='
            r'sharing|&export=download|/view)?(.*)?')
        matches_auth = pattern_google_auth.match(data)
        if matches_auth:
            patter_google_url_download = re.compile(
                r'(https://|www\.|https://www\.)?drive\.google\.com/uc\?id=.+&export=download')
            matches_download = patter_google_url_download.match(data)
            if matches_download:
                print("""It's a download link of Google Drive!
        Enjoy! :) """)
                pause()
            else:
                data = data.replace('file/d/', 'uc?id=')
                data = data.replace('/view?usp=sharing', '&export=download')
                data = data.replace('/view', '&export=download')
                print('\n'*2)
                pyperclip.copy(data)
                print("Download link has been copied to your clipboard")
                pause()
        else:
            print("""Error Link!
    Make sure your link is in this Format:
 https://drive.google.com/file/d/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/view? \
usp=sharing""")
            pause()
            google_drive()


if __name__ == '__main__':
    print("It won't run this way :(")
