#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DATA BREACH FINDER v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Data Breach Intelligence                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re
import hashlib
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

class BreachFinder:
    def __init__(self, target, target_type='email'):
        self.target = target
        self.target_type = target_type
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })

    def check_haveibeenpwned(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  HAVEIBEENPWNED CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f'https://haveibeenpwned.com/unifiedsearch/{self.target}'
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                breaches = data.get('Breaches', [])
                pastes = data.get('Pastes', [])

                print(f"  {Fore.GREEN}[+] Found in {len(breaches)} breaches")

                for breach in breaches:
                    print(f"\n  {Fore.RED}  Breach: {breach.get('Name')}")
                    print(f"  {Fore.WHITE}    Domain: {breach.get('Domain')}")
                    print(f"    Data: {', '.join(breach.get('DataClasses', []))}")
                    print(f"    Date: {breach.get('BreachDate')}")
                    print(f"    PwnCount: {breach.get('PwnCount')}")

                if pastes:
                    print(f"\n  {Fore.YELLOW}[+] Found in {len(pastes)} pastes")
                    for paste in pastes[:5]:
                        print(f"    {Fore.WHITE}• {paste.get('Source')}: {paste.get('Title')}")

                self.results['hibp'] = {
                    'breaches': [b.get('Name') for b in breaches],
                    'pastes': len(pastes),
                    'total_breaches': len(breaches)
                }
            elif resp.status_code == 404:
                print(f"  {Fore.GREEN}[OK] Not found in any breach")
            else:
                print(f"  {Fore.YELLOW}[-] Status: {resp.status_code}")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_dehashed(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DEHASHED SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Search URL:")
        print(f"  {Fore.CYAN}  https://dehashed.com/search?query={self.target}")
        print(f"\n  {Fore.WHITE}  [*] For full results, use DeHashed premium")
        print(f"  {Fore.WHITE}  [*] Free tier shows limited results")

    def search_intelx(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  INTELLIGENCE X SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Search URL:")
        print(f"  {Fore.CYAN}  https://intelx.io/?s={self.target}")
        print(f"\n  {Fore.WHITE}  [*] IntelX indexes dark web breaches, leaks, etc.")
        print(f"  {Fore.WHITE}  [*] Free search available for limited results")

    def search_leakcheck(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  LEAKCHECK SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f'https://leakcheck.io/api/public?query={self.target}'
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    found = data.get('found', 0)
                    print(f"  {Fore.GREEN}[+] Found in {found} breaches")

                    sources = data.get('sources', [])
                    for source in sources[:10]:
                        print(f"    {Fore.RED}  • {source.get('name', 'Unknown')} ({source.get('date', '')})")
                        lines = source.get('lines', 0)
                        if lines:
                            print(f"      {Fore.WHITE}    Entries: {lines}")

                    self.results['leakcheck'] = {'found': found, 'sources': len(sources)}
                else:
                    print(f"  {Fore.GREEN}[OK] Not found in leaks")
            else:
                print(f"  {Fore.YELLOW}[-] Status: {resp.status_code}")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def search_snusbase(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SNUSBASE SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Search URL:")
        print(f"  {Fore.CYAN}  https://www.snusbase.com/")
        print(f"\n  {Fore.WHITE}  [*] Search for: {self.target}")
        print(f"  {Fore.WHITE}  [*] Snusbase indexes multiple breach databases")

    def search_scylla(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SCYLLA.SH SEARCH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Search URL:")
        print(f"  {Fore.CYAN}  https://scylla.sh/search?q=email:{self.target}")
        print(f"\n  {Fore.WHITE}  [*] Scylla provides real-time breach data")

    def check_password_in_leaks(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PASSWORD HASH CHECK (HIBP API):")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if self.target_type == 'password':
            # SHA1 hash of password
            sha1 = hashlib.sha1(self.target.encode()).hexdigest().upper()
            prefix = sha1[:5]
            suffix = sha1[5:]

            url = f'https://api.pwnedpasswords.com/range/{prefix}'
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    matches = re.findall(rf'{suffix}:(\d+)', resp.text)
                    if matches:
                        count = matches[0]
                        print(f"  {Fore.RED}[!!!] Password found in {count} breaches!")
                        self.results['password_breached'] = True
                        self.results['password_count'] = count
                    else:
                        print(f"  {Fore.GREEN}[OK] Password not found in known breaches")
                else:
                    print(f"  {Fore.YELLOW}[-] Could not check")
            except Exception as e:
                print(f"  {Fore.RED}[!] Error: {e}")

    def generate_breach_report(self):
        print(f"\n\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BREACH REPORT:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Target: {self.target}")
        print(f"  {Fore.WHITE}  Type: {self.target_type}")
        print(f"  {Fore.WHITE}  Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        if 'hibp' in self.results:
            print(f"\n  {Fore.RED}  Breaches found: {self.results['hibp'].get('total_breaches', 0)}")

        print(f"\n  {Fore.CYAN}  Services to check:")
        print(f"    • https://haveibeenpwned.com/")
        print(f"    • https://dehashed.com/")
        print(f"    • https://intelx.io/")
        print(f"    • https://leakcheck.io/")
        print(f"    • https://scylla.sh/")
        print(f"    • https://snusbase.com/")
        print(f"    • https://breachdirectory.org/")
        print(f"    • https://www.spycloud.com/")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Type: {Fore.WHITE}{self.target_type}")
        print(f"{Fore.CYAN}  [*] Starting breach search...\n")

        if self.target_type == 'password':
            self.check_password_in_leaks()
        else:
            self.check_haveibeenpwned()
            self.check_dehashed()
            self.search_intelx()
            self.search_leakcheck()
            self.search_snusbase()
            self.search_scylla()

        self.generate_breach_report()

        # Save results
        with open(f'/tmp/breach_results_{self.target}.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/breach_results_{self.target}.json")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  BREACH SEARCH COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Data Breach Finder')
    parser.add_argument('-t', '--target', required=True, help='Target (email, username, or password)')
    parser.add_argument('-type', '--type', choices=['email', 'username', 'password', 'domain'],
                       default='email', help='Target type')
    args = parser.parse_args()

    finder = BreachFinder(args.target, args.type)
    finder.run()
