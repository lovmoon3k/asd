from threading import Thread
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import sys
import shutil
from urllib.parse import urlparse

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

web_URL = input("Enter gallery URL: ")



while True:
    code = input("Enter gallery code: ")
    try:
        int(code)
    except:
        print("Please provide a valid code...")
        print()
        continue

    web_Main_r = requests.get(web_URL)
    
    if web_Main_r.status_code == 200:
        print()
    else:
        print("URL not valid or site offline CODE - " + str(web_Main_r.status_code) + " - ")
        exit()

    soup = BeautifulSoup(web_Main_r.text, 'html.parser')
    
    galTitle = str(soup.find('h1'))
    galTitle = galTitle.replace('<h1>','')
    galTitle = galTitle.replace('</h1>','')
    print("Gallery: " + galTitle)

    tTotal = 0
    while soup.find('img', id='show' + str(tTotal)):
        tTotal = tTotal + 1
    else:
        print("Images found: " + str(tTotal))
    
    
    galFolder = os.path.exists("galleries")
    picsFolder = os.path.exists("galleries/" + galTitle)

    if galFolder != True:
        os.makedirs('galleries')
        print("Gallery folder created")
    else:
        print()

    if picsFolder:
        print("Gallery already exists.")
        exit()
    else:
        os.makedirs('galleries/' + galTitle)
        


    for picsIndex in range(tTotal):
        try:
            webPic = requests.get(f'https://asiansister.com/viewImg.php?code={code}&id=' + str(picsIndex))
            soup = BeautifulSoup(webPic.text, 'html.parser')
            imgURLget = soup.find('meta', property='og:image')
            imgURLfinal = "https://asiansister.com/" + str(imgURLget["content"])
            picD = requests.get(imgURLfinal)
            picNameGet = urlparse(imgURLfinal)
            picName = os.path.basename(picNameGet.path)

            with open('galleries/' + galTitle + '/' + str(picName), 'wb') as pic:
                pic.write(picD.content)
            print("Image " + str(picsIndex) + " OK!")
        except Exception as e:
            print("Error pic " + str(picsIndex) + " FAILURE: " + str(e))
            input("Press any key to close.")
            exit()

    print("SUCCESS!!! Gallery Downloaded!")
    input("Press any key to close.")
    exit()
    

    

