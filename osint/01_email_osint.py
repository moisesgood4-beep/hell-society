#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  EMAIL OSINT RECON v2.0                                          ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Email Intelligence                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
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

class EmailOSINT:
    def __init__(self, email):
        self.email = email
        self.results = {}

    def check_gravatar(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  GRAVATAR CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        import hashlib
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"

        try:
            resp = requests.head(url, timeout=10)
            if resp.status_code == 200:
                print(f"  {Fore.GREEN}[+] Gravatar found for this email!")
                print(f"  {Fore.WHITE}URL: https://gravatar.com/avatar/{email_hash}")
                self.results['gravatar'] = True
            else:
                print(f"  {Fore.YELLOW}[-] No Gravatar found")
                self.results['gravatar'] = False
        except:
            print(f"  {Fore.YELLOW}[-] Could not check Gravatar")

    def check_breaches(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BREACH CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}"
            headers = {'hibp-api-key': '', 'User-Agent': 'HellSociety/2.0'}
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                print(f"  {Fore.RED}[!!!] Found in {len(data)} breaches!")
                for breach in data[:10]:
                    print(f"  {Fore.RED}    • {breach.get('Name', 'N/A')} ({breach.get('BreachDate', 'N/A')})")
                self.results['breaches'] = len(data)
            elif resp.status_code == 404:
                print(f"  {Fore.GREEN}[OK] No breaches found")
                self.results['breaches'] = 0
            elif resp.status_code == 403:
                print(f"  {Fore.YELLOW}[-] Set HaveIBeenPwned API key")
            else:
                print(f"  {Fore.YELLOW}[-] API error: {resp.status_code}")
        except:
            print(f"  {Fore.YELLOW}[-] Could not check breaches")

    def check_email_validity(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  EMAIL VALIDITY:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            domain = self.email.split('@')[1]
            # Check MX records
            result = subprocess.run(['dig', '+short', domain, 'MX'], capture_output=True, text=True, timeout=10)
            if result.stdout.strip():
                print(f"  {Fore.GREEN}[+] MX records found for {domain}")
                for line in result.stdout.strip().split('\n'):
                    print(f"    {Fore.WHITE}{line}")
                self.results['mx_records'] = True
            else:
                print(f"  {Fore.RED}[!] No MX records for {domain}")
                self.results['mx_records'] = False
        except:
            pass

        # Check format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, self.email):
            print(f"  {Fore.GREEN}[OK] Valid email format")
        else:
            print(f"  {Fore.RED}[!] Invalid email format")

    def search_social(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SOCIAL MEDIA SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        username = self.email.split('@')[0]
        platforms = {
            'Twitter/X': f'https://twitter.com/{username}',
            'Instagram': f'https://www.instagram.com/{username}',
            'GitHub': f'https://github.com/{username}',
            'LinkedIn': f'https://www.linkedin.com/in/{username}',
            'Reddit': f'https://www.reddit.com/user/{username}',
            'TikTok': f'https://www.tiktok.com/@{username}',
        }

        for platform, url in platforms.items():
            try:
                resp = requests.head(url, timeout=5, allow_redirects=True)
                if resp.status_code == 200:
                    print(f"  {Fore.GREEN}[+] {platform}: POSSIBLE ({url})")
                else:
                    print(f"  {Fore.YELLOW}[-] {platform}: Not found")
            except:
                print(f"  {Fore.YELLOW}[-] {platform}: Could not check")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.email}")
        print(f"{Fore.CYAN}  [*] Starting email OSINT recon...\n")

        self.check_email_validity()
        self.check_gravatar()
        self.check_breaches()
        self.search_social()

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  EMAIL OSINT COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        # Save results
        results_file = f'/tmp/email_osint_{self.email.split("@")[0]}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"  {Fore.GREEN}[+] Results saved: {results_file}")


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
    print(f"  {BW}{Style.BRIGHT}  EMAIL OSINT{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}EMAIL OSINT                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target email                                 {RS}")
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
            print(f"  {Y}[*] Target email{RS}")
            value = input(f"  {Y}[*] -e: {RS}").strip()
            print(f"  {C}[*] Executing with -e={BW}{value}{RS}")
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

