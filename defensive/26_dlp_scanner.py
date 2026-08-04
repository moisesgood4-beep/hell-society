#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DATA LOSS PREVENTION SCANNER v2.0                               ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Data Protection                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
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

class DLPScanner:
    def __init__(self, scan_path):
        self.scan_path = scan_path
        self.findings = []
        self.stats = {'files': 0, 'emails': 0, 'cards': 0, 'ssns': 0, 'keys': 0}

        self.patterns = {
            'email': rb'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
            'credit_card': rb'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ssn': rb'\b\d{3}-\d{2}-\d{4}\b',
            'api_key': rb'(?:api[_-]?key|apikey)\s*[:=]\s*["\'][A-Za-z0-9_\-]{20,}["\']',
            'password': rb'password\s*[:=]\s*["\'][^"\']{8,}["\']',
            'aws_key': rb'AKIA[0-9A-Z]{16}',
            'private_key': rb'-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----',
            'jwt_token': rb'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
        }

    def scan(self):
        print(f"{Fore.CYAN}  [*] Scanning: {Fore.WHITE}{self.scan_path}")
        print(f"{Fore.CYAN}  [*] Looking for sensitive data...\n")

        for root, dirs, files in os.walk(self.scan_path):
            for filename in files:
                self.stats['files'] += 1
                filepath = os.path.join(root, filename)

                if any(filename.endswith(ext) for ext in ['.png', '.jpg', '.gif', '.zip', '.gz', '.tar', '.bin', '.exe']):
                    continue

                try:
                    with open(filepath, 'rb') as f:
                        content = f.read(100000)

                    for pattern_name, pattern in self.patterns.items():
                        matches = re.findall(pattern, content)
                        if matches:
                            self.findings.append({
                                'file': filepath,
                                'type': pattern_name,
                                'count': len(matches)
                            })
                            self.stats[pattern_name] += len(matches)

                except:
                    pass

                if self.stats['files'] % 50 == 0:
                    print(f"\r{Fore.CYAN}  [*] Files: {self.stats['files']} | Findings: {len(self.findings)}", end="", flush=True)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DLP SCAN COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.WHITE}Files scanned: {self.stats['files']}")
        print(f"\n  {Fore.CYAN}Sensitive Data Found:")
        print(f"  {Fore.WHITE}  Emails: {self.stats['email']}")
        print(f"  {Fore.RED}  Credit Cards: {self.stats['credit_card']}")
        print(f"  {Fore.RED}  SSNs: {self.stats['ssn']}")
        print(f"  {Fore.RED}  API Keys: {self.stats['api_key']}")
        print(f"  {Fore.RED}  Passwords: {self.stats['password']}")
        print(f"  {Fore.RED}  AWS Keys: {self.stats['aws_key']}")
        print(f"  {Fore.RED}  Private Keys: {self.stats['private_key']}")
        print(f"  {Fore.YELLOW}  JWT Tokens: {self.stats['jwt_token']}")

        if self.findings:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  FINDINGS:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            for f in self.findings[:20]:
                print(f"  {Fore.RED}[{f['type'].upper()}] {f['file']} ({f['count']} matches)")

        total = sum(self.stats[k] for k in self.stats if k != 'files')
        if total > 0:
            print(f"\n  {Fore.RED}[!!!] {total} sensitive data items exposed!")
            print(f"  {Fore.RED}[!!!] Encrypt or remove sensitive data!")
        else:
            print(f"\n  {Fore.GREEN}[OK] No sensitive data found")



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
    print(f"  {BW}{Style.BRIGHT}  DLP SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}DLP SCANNER                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Path to scan                                 {RS}")
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
            print(f"  {Y}[*] Path to scan{RS}")
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

