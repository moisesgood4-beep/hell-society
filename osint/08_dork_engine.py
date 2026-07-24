#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  GOOGLE DORKING ENGINE v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Search Engine Intelligence                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import time

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

class DorkEngine:
    def __init__(self, target):
        self.target = target
        self.results = []
        self.dorks = [
            # Sensitive files
            f'site:{target} filetype:env',
            f'site:{target} filetype:sql',
            f'site:{target} filetype:log',
            f'site:{target} filetype:conf',
            f'site:{target} filetype:xml',
            f'site:{target} filetype:json',
            f'site:{target} filetype:txt intext:password',

            # Admin panels
            f'site:{target} inurl:admin',
            f'site:{target} inurl:login',
            f'site:{target} inurl:phpmyadmin',
            f'site:{target} inurl:cpanel',
            f'site:{target} inurl:wp-admin',
            f'site:{target} inurl:administrator',

            # Sensitive info
            f'site:{target} intext:"index of"',
            f'site:{target} intext:"parent directory"',
            f'site:{target} intext:"database error"',
            f'site:{target} intext:"stack trace"',
            f'site:{target} intext:"syntax error"',

            # Exposed services
            f'site:{target} inurl:swagger',
            f'site:{target} inurl:graphql',
            f'site:{target} inurl:api',
            f'site:{target} inurl:dashboard',
            f'site:{target} intitle:"test"',

            # Credentials
            f'site:{target} ext:txt intext:"password"',
            f'site:{target} ext:log intext:"password"',
            f'site:{target} ext:env intext:"DB_PASSWORD"',
            f'site:{target} ext:env intext:"API_KEY"',
            f'site:{target} ext:env intext:"SECRET"',
        ]

    def search_dork(self, dork):
        try:
            # Use a simple search approach
            url = f"https://www.google.com/search?q={dork}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
                'Accept': 'text/html,application/xhtml+xml'
            }
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 200:
                return {'dork': dork, 'status': 'available', 'results_count': 'check manually'}
            else:
                return {'dork': dork, 'status': f'error_{resp.status_code}'}
        except:
            return {'dork': dork, 'status': 'failed'}

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Total dorks: {Fore.WHITE}{len(self.dorks)}")
        print(f"{Fore.CYAN}  [*] Generating dork list...\n")

        print(f"  {Fore.CYAN}{'═' * 60}")
        print(f"  GENERATED DORK QUERIES:")
        print(f"  {Fore.CYAN}{'═' * 60}\n")

        for i, dork in enumerate(self.dorks, 1):
            print(f"  {Fore.WHITE}[{i:02d}] {dork}")

        # Categorize
        categories = {
            'Sensitive Files': [d for d in self.dorks if 'filetype' in d],
            'Admin Panels': [d for d in self.dorks if 'inurl:admin' in d or 'inurl:login' in d or 'inurl:wp-admin' in d or 'inurl:cpanel' in d or 'inurl:phpmyadmin' in d],
            'Directory Listing': [d for d in self.dorks if 'index of' in d or 'parent directory' in d],
            'Error Messages': [d for d in self.dorks if 'error' in d or 'trace' in d or 'syntax' in d],
            'Exposed Services': [d for d in self.dorks if 'swagger' in d or 'graphql' in d or 'api' in d],
            'Credentials': [d for d in self.dorks if 'password' in d or 'API_KEY' in d or 'SECRET' in d or 'DB_PASSWORD' in d],
        }

        print(f"\n\n  {Fore.CYAN}{'═' * 60}")
        print(f"  DORK CATEGORIES:")
        print(f"  {Fore.CYAN}{'═' * 60}")

        for cat, dorks in categories.items():
            print(f"\n  {Fore.RED}[{cat}]")
            for d in dorks:
                print(f"    {Fore.WHITE}{d}")

        # Generate search URLs
        print(f"\n\n  {Fore.CYAN}{'═' * 60}")
        print(f"  SEARCH URLS (copy & paste):")
        print(f"  {Fore.CYAN}{'═' * 60}\n")

        for i, dork in enumerate(self.dorks, 1):
            encoded = dork.replace(' ', '+')
            url = f"https://www.google.com/search?q={encoded}"
            print(f"  {Fore.WHITE}[{i:02d}] {url}")

        # Save dork list
        results = {
            'target': self.target,
            'dorks': self.dorks,
            'categories': {k: v for k, v in categories.items()},
            'total': len(self.dorks)
        }
        results_file = f'/tmp/dorks_{self.target}.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Dorks saved: {results_file}")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DORK GENERATION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.YELLOW}[i] Copy the URLs above and run them in your browser")
        print(f"  {Fore.YELLOW}[i] Check results for sensitive data exposure")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Dork Engine')
    parser.add_argument('-t', '--target', required=True, help='Target domain')
    args = parser.parse_args()

    engine = DorkEngine(args.target)
    engine.run()
