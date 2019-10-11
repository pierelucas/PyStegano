# PyStegano - Steganographie Tool to hide encrypted Textpassages in Files
#
# Creation:    09.10.2019
# Last Update: 10.10.2019
#
#
# MIT License
#
# Copyright (c) 2019 by PiereLucas
# https://github.com/pierelucas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
# Modules
#
import os, sys, subprocess, time
from re import findall, sub
from colorama import Fore, Style
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import hashlib

class PyStegano():

    def __init__(self, salt='SlTKeYOpHygTYkP3'):

        # Time
        self.lt = time.localtime()
        self.time_hm = time.strftime(Fore.GREEN + "%H:%M" + Style.RESET_ALL, self.lt)

        # Banner
        self.banner_txt = """
        __________         _________ __                                     
        \______   \___.__./   _____//  |_  ____   _________    ____   ____  
         |     ___<   |  |\_____  \\   __\/ __ \ / ___\__  \  /    \ /  _ \ 
         |    |    \___  |/        \|  | \  ___// /_/  > __ \|   |  (  <_> )
         |____|    / ____/_______  /|__|  \___  >___  (____  /___|  /\____/ 
           v.1.2   \/            \/           \/_____/     \/     \/        
           
                    Coded by PiereLucas | github.com/pierelucas
                             [+] FUCK YOU INTERPOL [+]
           """

        self.menu_txt = """
                    [1] Write
                    [2] Read
                    [Else] Exit
                    """

        # Path
        self.path = None

        # Enc Dec
        self.salt = salt
        self.enc_dec_meth0 = 'utf-8'
        self.message = None
        self.ciphertext = None

    def out(self):

        subprocess.call("clear", shell=True)
        print(Fore.CYAN + self.banner_txt)
        print(Fore.RED + self.menu_txt)
        print(Style.RESET_ALL)

    def input(self):

        # Make Choice
        while True:
            choice = str(input(self.time_hm + Fore.GREEN + " [+] Which option Number » "))
            print(Style.RESET_ALL)
            # Path
            while True:
                self.path = str(input(self.time_hm + Fore.GREEN + " [+] File Path » "))
                print(Style.RESET_ALL)
                if os.path.isfile(self.path): break
                else:
                    print(self.time_hm + Fore.RED + " [-] File is not readable")
                    print(Style.RESET_ALL)
                    continue
            # Passphrase for encryption
            while True:
                key = str(input(self.time_hm + Fore.GREEN + " [+] Wrote down your Passphrase for Encryption (min. 8) » "))
                print(Style.RESET_ALL)
                key_check = str(input(self.time_hm + Fore.GREEN + " [+] Wrote down AGAIN your Passphrase for Encryption (min. 8) » "))
                print(Style.RESET_ALL)
                if key == key_check:
                    if len(key) >= 8: break
                    else: continue
                else: continue
            # Return
            if choice == '1':
                message = str(input(self.time_hm + Fore.GREEN + " [+] Wrote down your hidden Textpassage » "))
                print(Style.RESET_ALL)
                return 'write', message, key
            if choice == '2':
                return 'read', None, key
            else:
                sys.exit(0)

    def read(self):

        with open(self.path, encoding="ISO-8859-1", mode="r") as f:

            try:
                byte = f.read(1)
                str = ""
                while byte != "":
                    str = str + byte
                    byte = f.read(1)
                raw_find = findall("\$- .* -\$", str)
                for row in raw_find:
                    ciphertext = sub("\$- ", "", row)
                    ciphertext = sub(" -\$", "", ciphertext)
                    return ciphertext
            finally:
                f.close()

    def write(self, *, ciphertext):

        ciphertext = "$- " + ciphertext + " -$"

        with open(self.path, encoding="ISO-8859-1", mode="a+") as f:

            f.write(ciphertext)

            try:
                byte = f.read(1)
                str = ""
                while byte != "":
                    str = str + byte
                    byte = f.read(1)
                print(str)
                return True
            finally:
                f.close()

    def enc(self, *, key, message):

        key = hashlib.sha256(str.encode(key))
        try:
            iv = self.salt
            aes_obj = AES.new(key.digest(), AES.MODE_CFB, iv)
            hx_enc = aes_obj.encrypt(message)
            ciphertext = b64encode(hx_enc).decode(self.enc_dec_meth0)
            return ciphertext
        except: print("Error")

    def dec(self, *, key, ciphertext):

        key = hashlib.sha256(str.encode(key))
        try:
            iv = self.salt
            aes_obj = AES.new(key.digest(), AES.MODE_CFB, iv)
            tmp = b64decode(ciphertext.encode(self.enc_dec_meth0))
            hx_dec = aes_obj.decrypt(tmp)
            message = hx_dec.decode(self.enc_dec_meth0)
            return message
        except: print("Error")

    def run(self):

        self.out()
        op_mode, message, key = self.input()
        if op_mode == 'write':
            self.ciphertext = self.enc(key=key, message=message)
            _true = self.write(ciphertext=self.ciphertext)
            if _true: print(self.time_hm + Fore.GREEN + " [+] Textpassage succesfully encrypted and saved")
            else: print(self.time_hm + Fore.RED + " [-] ERROR: Textpassage not saved")
        elif op_mode == 'read':
            ciphertext = self.read()
            message = self.dec(key=key, ciphertext=ciphertext)
            print(self.time_hm + Fore.GREEN + " [+] Sucessfully decrypt and read textpassage ↓")
            print(Style.RESET_ALL)
            print(message)


# TO BE CONTINUED ...

stegano = PyStegano()
stegano.run()
