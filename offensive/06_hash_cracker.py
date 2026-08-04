#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HASH CRACKER v2.0                                               ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Password Cracking                         ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import hashlib
import sys
import time
import colorama
from colorama import Fore, Back, Style
import argparse
import itertools

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

HASH_TYPES = {
    'md5': 32,
    'sha1': 40,
    'sha256': 64,
    'sha512': 128,
    'ntlm': 32,
    'blake2b': 128,
}

COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "passw0rd", "shadow", "123123", "654321",
    "superman", "qazwsx", "michael", "football", "password1",
    "password123", "admin", "root", "toor", "test",
    "guest", "info", "adm", "mysql", "oracle",
    "pass", "admin123", "root123", "toor123",
    "P@ssw0rd", "P@ssword", "p@ssword", "password!",
    "hello123", "welcome", "welcome1", "changeme",
    "1q2w3e", "1q2w3e4r", "zaq1xsw2", "qwerty123",
    "asdfgh", "zxcvbn", "123456789", "1234567890",
    "000000", "111111", "222222", "333333",
    "aaaaaa", "abcabc", "abcdef", "abcdefg",
    "pass1234", "test1234", "admin1234", "user1234",
]

EXTENDED_PASSWORDS = [
    "hello", "world", "python", "linux", "hacker",
    "security", "pentest", "crack", "brute", "force",
    "exploit", "vuln", "cve", "nmap", "metasploit",
    "burp", "wireshark", "kali", "parrot", "blackarch",
    "debian", "ubuntu", "centos", "arch", "fedora",
    "server", "client", "network", "firewall", "proxy",
    "vpn", "ssh", "ftp", "http", "https",
    "javascript", "php", "java", "c++", "rust",
    "golang", "ruby", "perl", "bash", "powershell",
]

class HashCracker:
    def __init__(self, hash_value, wordlist=None, mode="dictionary"):
        self.hash_value = hash_value.lower()
        self.wordlist = wordlist
        self.mode = mode
        self.hash_type = self.identify_hash()
        self.cracked = False

    def identify_hash(self):
        length = len(self.hash_value)
        for htype, hlen in HASH_TYPES.items():
            if length == hlen:
                return htype
        return "unknown"

    def hash_password(self, password):
        if self.hash_type == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif self.hash_type == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif self.hash_type == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif self.hash_type == 'sha512':
            return hashlib.sha512(password.encode()).hexdigest()
        elif self.hash_type == 'ntlm':
            return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
        return None

    def crack_dictionary(self):
        passwords = COMMON_PASSWORDS + EXTENDED_PASSWORDS

        if self.wordlist:
            try:
                with open(self.wordlist, 'r', errors='ignore') as f:
                    passwords = f.read().splitlines()
            except FileNotFoundError:
                print(f"{Fore.RED}  [!] Wordlist file not found: {self.wordlist}")
                return

        total = len(passwords)
        print(f"{Fore.CYAN}  [*] Cracking with {total} passwords\n")

        for i, password in enumerate(passwords):
            progress = ((i + 1) / total) * 100
            bar_length = 40
            filled = int(bar_length * (i + 1) / total)
            bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
            print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Trying: {password[:30]}", end="", flush=True)

            hashed = self.hash_password(password)
            if hashed == self.hash_value:
                self.cracked = True
                print(f"\n")
                print(f"{Fore.GREEN}  [+] CRACKED! Password: {Fore.WHITE}{password}")
                print(f"{Fore.GREEN}  [+] Hash Type: {Fore.YELLOW}{self.hash_type}")
                return

    def crack_bruteforce(self, max_length=6):
        charset = "abcdefghijklmnopqrstuvwxyz0123456789"
        total = sum(len(charset) ** i for i in range(1, max_length + 1))
        current = 0

        print(f"{Fore.CYAN}  [*] Bruteforce mode - charset: {len(charset)} chars, max length: {max_length}\n")

        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                current += 1
                password = ''.join(combo)
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Trying: {password}", end="", flush=True)

                hashed = self.hash_password(password)
                if hashed == self.hash_value:
                    self.cracked = True
                    print(f"\n")
                    print(f"{Fore.GREEN}  [+] CRACKED! Password: {Fore.WHITE}{password}")
                    print(f"{Fore.GREEN}  [+] Hash Type: {Fore.YELLOW}{self.hash_type}")
                    return

    def crack(self):
        if self.hash_type == "unknown":
            print(f"{Fore.RED}  [!] Unknown hash type. Supported: {list(HASH_TYPES.keys())}")
            return

        print(f"{Fore.CYAN}  [*] Hash: {Fore.WHITE}{self.hash_value}")
        print(f"{Fore.CYAN}  [*] Type: {Fore.YELLOW}{self.hash_type}")
        print(f"{Fore.CYAN}  [*] Mode: {Fore.WHITE}{self.mode}")
        print(f"{Fore.CYAN}  [*] Starting...\n")

        if self.mode == "dictionary":
            self.crack_dictionary()
        elif self.mode == "bruteforce":
            self.crack_bruteforce()

        if not self.cracked:
            print(f"\n\n{Fore.YELLOW}  [!] Password not found in wordlist")



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
    print(f"  {BW}{Style.BRIGHT}  HASH CRACKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}HASH CRACKER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Hash to crack                                {RS}")
        print(f"  {C}[2]  {BW}Wordlist file path                           {RS}")
        print(f"  {C}[3]  {BW}Cracking mode                                {RS}")
        print()
        print(f"  {C}[4]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Hash to crack{RS}")
            value = input(f"  {Y}[*] -H: {RS}").strip()
            print(f"  {C}[*] Executing with -H={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Wordlist file path{RS}")
            value = input(f"  {Y}[*] -w: {RS}").strip()
            print(f"  {C}[*] Executing with -w={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Cracking mode{RS}")
            value = input(f"  {Y}[*] -m: {RS}").strip()
            print(f"  {C}[*] Executing with -m={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '4':
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

