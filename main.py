# PyStegano - Steganographie Tool to hide your Passphrases in Files
#
# Creation:    09.10.2019
# Last Update: 09.10.2019
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

class PyStegano():

    def __init__(self):

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
                   \/            \/           \/_____/     \/     \/        
           
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
            # Return
            if choice == '1':
                raw_txt = str(input(self.time_hm + Fore.GREEN + " [+] Wrote down your passphrase » "))
                print(Style.RESET_ALL)
                write_txt = "$- " + raw_txt + " -$"
                return 'write', write_txt
            if choice == '2':
                return 'read', None
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
                    read_txt = sub("\$- ", "", row)
                    read_txt = sub(" -\$", "", read_txt)
            finally:
                f.close()
                return read_txt

    def write(self, *, write_txt):
        with open(self.path, encoding="ISO-8859-1", mode="a+") as f:

            f.write(write_txt)

            try:
                byte = f.read(1)
                str = ""
                while byte != "":
                    str = str + byte
                    byte = f.read(1)
                print(str)
            finally:
                f.close()
                return True

    def run(self):
        self.out()
        op_mode, write_txt = self.input()
        if op_mode == 'write':
            _true = self.write(write_txt=write_txt)
            if _true: print(self.time_hm + Fore.GREEN + " [+] Passphrase Succesfully saved")
            else: print(self.time_hm + Fore.RED + " [-] ERROR: Passphrase not saved")
        elif op_mode == 'read':
            read_txt = self.read()
            print(self.time_hm + Fore.GREEN + " [+] Sucessfully read Passphrase ↓")
            print(Style.RESET_ALL)
            print(read_txt)


# TO BE CONTINUED ...

stegano = PyStegano()
stegano.run()
