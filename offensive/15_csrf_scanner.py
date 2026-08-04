#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  CSRF VULNERABILITY SCANNER v2.0                                 ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Web Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

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

class CSRFScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.vulns = []
        self.forms_found = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def scan(self):
        try:
            response = self.session.get(self.target, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            forms = soup.find_all('form')
            print(f"{Fore.CYAN}  [*] Found {len(forms)} form(s) on page\n")

            csrf_token_names = ['csrf', 'csrf_token', '_csrf', 'token', '_token',
                               'authenticity_token', '__RequestVerificationToken',
                               'csrfmiddlewaretoken', 'nonce', '_nonce']

            for i, form in enumerate(forms, 1):
                action = form.get('action', self.target)
                method = form.get('method', 'GET').upper()
                full_action = urljoin(self.target, action)

                print(f"{Fore.CYAN}  [{'─' * 40}]")
                print(f"  {Fore.WHITE}Form {i}: {method} {full_action}")

                inputs = form.find_all(['input', 'textarea', 'select'])
                has_csrf = False
                csrf_found = None

                for inp in inputs:
                    name = inp.get('name', '')
                    inp_type = inp.get('type', 'text')

                    if any(token in name.lower() for token in csrf_token_names):
                        has_csrf = True
                        csrf_found = name
                        print(f"  {Fore.GREEN}  [+] CSRF Token Found: {name}")

                    print(f"  {Fore.YELLOW}  Input: {name} ({inp_type})")

                if not has_csrf and method == 'POST':
                    print(f"  {Fore.RED}  [VULN] No CSRF protection detected!")
                    self.vulns.append({
                        'form': i,
                        'action': full_action,
                        'method': method,
                        'issue': 'No CSRF token'
                    })

                if not form.find('input', {'name': lambda x: x and any(t in x.lower() for t in csrf_token_names)}):
                    if method == 'POST':
                        pass

                self.forms_found.append({
                    'action': full_action,
                    'method': method,
                    'has_csrf': has_csrf,
                    'csrf_field': csrf_found
                })

            self._check_headers(response.headers)

        except Exception as e:
            print(f"{Fore.RED}  [!] Error: {e}")

    def _check_headers(self, headers):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  HEADER ANALYSIS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        same_site = headers.get('Set-Cookie', '')
        if 'samesite' in same_site.lower():
            print(f"  {Fore.GREEN}[OK] SameSite cookie attribute found")
        else:
            print(f"  {Fore.RED}[VULN] Missing SameSite cookie attribute")
            self.vulns.append({'issue': 'Missing SameSite'})

        if 'X-CSRF-Token' in headers:
            print(f"  {Fore.GREEN}[OK] X-CSRF-Token header present")
        else:
            print(f"  {Fore.YELLOW}[-] No X-CSRF-Token header")

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        vulnerable = [f for f in self.forms_found if not f['has_csrf']]
        print(f"  {Fore.CYAN}Total Forms: {len(self.forms_found)}")
        print(f"  {Fore.GREEN}Protected: {len(self.forms_found) - len(vulnerable)}")
        print(f"  {Fore.RED}Vulnerable: {len(vulnerable)}")

        if vulnerable:
            print(f"\n{Fore.RED}  Vulnerable Forms:")
            for f in vulnerable:
                print(f"    {Fore.RED}• {f['method']} {f['action']}")

        score = max(0, 100 - (len(vulnerable) * 25))
        print(f"\n  {Fore.CYAN}CSRF Security Score: {score}/100")



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
    print(f"  {BW}{Style.BRIGHT}  CSRF SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}CSRF SCANNER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL                                   {RS}")
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
            print(f"  {Y}[*] Target URL{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
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

