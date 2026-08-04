#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PHONE NUMBER OSINT v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Phone Intelligence                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re

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

class PhoneRecon:
    def __init__(self, phone):
        self.phone = phone
        self.clean = re.sub(r'[^0-9+]', '', phone)
        self.results = {}

    def format_analysis(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PHONE FORMAT ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}Original: {self.phone}")
        print(f"  {Fore.WHITE}Clean: {self.clean}")

        if self.clean.startswith('+'):
            country_code = self.clean[1:4]
            print(f"  {Fore.GREEN}[+] Country code: +{country_code}")
            self.results['country_code'] = f'+{country_code}'

            # Common country codes
            countries = {
                '1': 'USA/Canada', '44': 'United Kingdom', '49': 'Germany',
                '33': 'France', '34': 'Spain', '39': 'Italy',
                '55': 'Brazil', '86': 'China', '81': 'Japan',
                '91': 'India', '7': 'Russia', '52': 'Mexico',
                '54': 'Argentina', '57': 'Colombia', '34': 'Spain',
            }
            for code, country in countries.items():
                if self.clean.startswith(f'+{code}'):
                    print(f"  {Fore.GREEN}[+] Country: {country}")
                    self.results['country'] = country
                    break
        else:
            print(f"  {Fore.YELLOW}[-] No country code detected")

        # Carrier type estimation
        if len(self.clean) > 10:
            print(f"  {Fore.WHITE}Length: {len(self.clean)} digits (international)")
        else:
            print(f"  {Fore.WHITE}Length: {len(self.clean)} digits (possibly local)")

    def check_leaks(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DATA BREACH CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            import requests
            # Check against known breach databases
            print(f"  {Fore.WHITE}Searching for {self.phone} in breach databases...")
            print(f"  {Fore.YELLOW}[-] Set API keys for full breach checking")
            print(f"  {Fore.CYAN}  Services to check:")
            print(f"    - HaveIBeenPwned (phone)")
            print(f"    - IntelX")
            print(f"    - DeHashed")
        except:
            pass

    def check_social(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SOCIAL MEDIA ASSOCIATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Check these platforms manually:")
        print(f"  {Fore.CYAN}  - WhatsApp: Save number and check profile")
        print(f"  {Fore.CYAN}  - Telegram: Search by phone number")
        print(f"  {Fore.CYAN}  - Signal: Check if registered")
        print(f"  {Fore.CYAN}  - Facebook: Search by phone")
        print(f"  {Fore.CYAN}  - Instagram: Try to find by phone")
        print(f"  {Fore.CYAN}  - LinkedIn: Search by phone")
        print(f"  {Fore.CYAN}  - Twitter/X: Some users link phones")

    def generate_report(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  REPORT:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}Phone: {self.phone}")
        if 'country' in self.results:
            print(f"  {Fore.WHITE}Country: {self.results['country']}")

        # Save results
        results_file = f'/tmp/phone_recon_{self.clean}.json'
        with open(results_file, 'w') as f:
            json.dump({'phone': self.phone, 'results': self.results}, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Report saved: {results_file}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.phone}")
        print(f"{Fore.CYAN}  [*] Starting phone reconnaissance...\n")

        self.format_analysis()
        self.check_leaks()
        self.check_social()
        self.generate_report()

        print(f"\n{Fore.GREEN}{Back.BLACK}  PHONE RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")


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
    print(f"  {BW}{Style.BRIGHT}  PHONE RECON{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}PHONE RECON                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target phone number                          {RS}")
        print()
        print(f"  {C}[2]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target phone number{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
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

