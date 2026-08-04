#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SOCIAL MEDIA SCRAPER v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Social Media Intelligence                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re
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

class SocialScraper:
    def __init__(self, username):
        self.username = username
        self.data = {}
        self.headers = {'User-Agent': 'Mozilla/5.0 HellSociety/2.0'}

    def check_twitter(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TWITTER/X INTELLIGENCE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"https://nitter.net/{self.username}"
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                print(f"  {Fore.GREEN}[+] Twitter profile accessible")
                self.data['twitter'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] Could not access Twitter profile")
                self.data['twitter'] = {'found': False}
        except:
            print(f"  {Fore.YELLOW}[-] Twitter check failed")

    def check_github(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  GITHUB INTELLIGENCE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = requests.get(f"https://api.github.com/users/{self.username}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  {Fore.GREEN}[+] GitHub profile found")
                print(f"  {Fore.WHITE}  Name: {data.get('name', 'N/A')}")
                print(f"  {Fore.WHITE}  Bio: {data.get('bio', 'N/A')}")
                print(f"  {Fore.WHITE}  Location: {data.get('location', 'N/A')}")
                print(f"  {Fore.WHITE}  Company: {data.get('company', 'N/A')}")
                print(f"  {Fore.WHITE}  Email: {data.get('email', 'N/A')}")
                print(f"  {Fore.WHITE}  Public repos: {data.get('public_repos', 0)}")
                print(f"  {Fore.WHITE}  Followers: {data.get('followers', 0)}")
                print(f"  {Fore.WHITE}  Created: {data.get('created_at', 'N/A')}")

                self.data['github'] = data
            else:
                print(f"  {Fore.YELLOW}[-] No GitHub profile")
                self.data['github'] = {'found': False}
        except:
            pass

    def check_linkedin(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  LINKEDIN INTELLIGENCE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f"https://www.linkedin.com/in/{self.username}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                print(f"  {Fore.GREEN}[+] LinkedIn profile accessible")
                self.data['linkedin'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] LinkedIn profile not accessible")
                self.data['linkedin'] = {'found': False}
        except:
            pass

    def check_instagram(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  INSTAGRAM INTELLIGENCE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f"https://www.instagram.com/{self.username}/"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                print(f"  {Fore.GREEN}[+] Instagram profile accessible")
                self.data['instagram'] = {'found': True, 'url': url}
            else:
                print(f"  {Fore.YELLOW}[-] Instagram not accessible")
                self.data['instagram'] = {'found': False}
        except:
            pass

    def check_reddit(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  REDDIT INTELLIGENCE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = requests.get(f"https://www.reddit.com/user/{self.username}/about.json",
                              headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get('data', {})
                print(f"  {Fore.GREEN}[+] Reddit profile found")
                print(f"  {Fore.WHITE}  Name: {data.get('subreddit', {}).get('display_name', 'N/A')}")
                print(f"  {Fore.WHITE}  Created: {data.get('created_utc', 'N/A')}")
                print(f"  {Fore.WHITE}  Karma: {data.get('total_karma', 'N/A')}")
                self.data['reddit'] = data
            else:
                print(f"  {Fore.YELLOW}[-] No Reddit profile")
                self.data['reddit'] = {'found': False}
        except:
            pass

    def generate_report(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  SOCIAL MEDIA RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        found_count = sum(1 for k, v in self.data.items() if isinstance(v, dict) and v.get('found'))
        print(f"\n  {Fore.GREEN}[+] Platforms with profiles: {found_count}")
        for k, v in self.data.items():
            if isinstance(v, dict) and v.get('found'):
                print(f"    {Fore.GREEN}• {k}: {v.get('url', 'Found')}")

        results_file = f'/tmp/social_recon_{self.username}.json'
        with open(results_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.username}")
        print(f"{Fore.CYAN}  [*] Starting social media reconnaissance...\n")

        self.check_github()
        self.check_linkedin()
        self.check_instagram()
        self.check_reddit()
        self.check_twitter()
        self.generate_report()


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
    print(f"  {BW}{Style.BRIGHT}  SOCIAL MEDIA SCRAPER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}SOCIAL MEDIA SCRAPER                    {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target username                              {RS}")
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
            print(f"  {Y}[*] Target username{RS}")
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

