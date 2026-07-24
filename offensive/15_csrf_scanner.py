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

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society CSRF Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()

    scanner = CSRFScanner(args.url)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting CSRF scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
