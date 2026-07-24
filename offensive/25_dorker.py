#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  GOOGLE DORKER v2.0                                              ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Reconnaissance                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import time
import random
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

DORKS = {
    'login_pages': [
        'inurl:login site:{target}',
        'inurl:signin site:{target}',
        'inurl:auth site:{target}',
        'inurl:admin site:{target}',
        '"login" "password" site:{target}',
    ],
    'sensitive_files': [
        'filetype:sql site:{target}',
        'filetype:log site:{target}',
        'filetype:env site:{target}',
        'filetype:bak site:{target}',
        'filetype:conf site:{target}',
        'filetype:ini site:{target}',
        'filetype:db site:{target}',
    ],
    'config_files': [
        'filetype:xml "password" site:{target}',
        'filetype:yaml site:{target}',
        'filetype:json "api_key" site:{target}',
        '"db_password" site:{target}',
        '"api_secret" site:{target}',
    ],
    'open_directories': [
        'intitle:"index of" site:{target}',
        'intitle:"index of /" "parent directory" site:{target}',
        '"directory listing for" site:{target}',
    ],
    'exposed_cams': [
        'inurl:/view.shtml site:{target}',
        '"webcamXP" site:{target}',
        '"Network Camera NetworkCamera" site:{target}',
    ],
    'credentials': [
        '"password" filetype:txt site:{target}',
        '"username" "password" filetype:log site:{target}',
        'intext:"password" filetype:csv site:{target}',
    ],
    'vulnerabilities': [
        'inurl:"id=" site:{target}',
        'inurl:"page=" site:{target}',
        'inurl:"cat=" site:{target}',
        'inurl:"file=" site:{target}',
        'inurl:"dir=" site:{target}',
    ],
    'technology': [
        '"powered by WordPress" site:{target}',
        '"powered by Joomla" site:{target}',
        '"powered by Drupal" site:{target}',
        '"X-Powered-By" site:{target}',
    ],
}

class GoogleDorker:
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 HellSociety/2.0'
        })

    def search(self, dork, max_results=5):
        try:
            query = dork.replace('{target}', self.target)
            url = f"https://www.google.com/search?q={query}"
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q=') and 'google' not in href.split('q=')[1].split('&')[0]:
                    link = href.split('q=')[1].split('&')[0]
                    if self.target in link:
                        links.append(link)
                        if len(links) >= max_results:
                            break

            return links
        except:
            return []

    def scan_all(self):
        total_categories = len(DORKS)
        total_dorks = sum(len(v) for v in DORKS.values())
        current = 0

        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Total dorks: {total_dorks} in {total_categories} categories\n")

        for category, dorks in DORKS.items():
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  {Fore.WHITE}{category.upper().replace('_', ' ')}")
            print(f"{Fore.CYAN}  [{'═' * 40}]")

            category_results = []
            for dork in dorks:
                current += 1
                progress = (current / total_dorks) * 100
                print(f"\n  {Fore.YELLOW}[{current}/{total_dorks}] {dork[:60]}")

                links = self.search(dork)
                if links:
                    for link in links:
                        category_results.append(link)
                        print(f"    {Fore.GREEN}• {Fore.WHITE}{link[:80]}")

                time.sleep(random.uniform(1, 3))

            self.results[category] = category_results

        self.print_results()

    def print_results(self):
        total_results = sum(len(v) for v in self.results.values())
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DORKING COMPLETE - {total_results} RESULTS FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for category, results in self.results.items():
            if results:
                print(f"\n  {Fore.CYAN}{category.upper().replace('_', ' ')}: {len(results)} results")
                for r in results[:5]:
                    print(f"    {Fore.WHITE}• {r[:70]}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Google Dorker')
    parser.add_argument('-t', '--target', required=True, help='Target domain (e.g., example.com)')
    args = parser.parse_args()

    dorker = GoogleDorker(args.target)
    dorker.scan_all()

if __name__ == "__main__":
    main()
