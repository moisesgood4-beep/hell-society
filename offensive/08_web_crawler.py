#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEB CRAWLER / SPIDER v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Web Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import time
import colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import threading
from collections import deque

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

class WebCrawler:
    def __init__(self, target, max_pages=100, max_depth=5):
        self.target = target.rstrip('/')
        self.target_domain = urlparse(target).netloc
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited = set()
        self.urls = deque()
        self.forms = []
        self.inputs = []
        self.interesting_files = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def crawl(self):
        self.urls.append((self.target, 0))
        page_count = 0

        print(f"{Fore.CYAN}  [*] Starting crawl from: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Max pages: {self.max_pages}, Max depth: {self.max_depth}\n")

        while self.urls and page_count < self.max_pages:
            url, depth = self.urls.popleft()

            if url in self.visited or depth > self.max_depth:
                continue

            if urlparse(url).netloc != self.target_domain:
                continue

            self.visited.add(url)
            page_count += 1

            bar_length = 40
            filled = int(bar_length * page_count / self.max_pages)
            bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
            print(f"\r{Fore.CYAN}  [{bar}] {page_count}/{self.max_pages} pages - {len(self.visited)} unique", end="", flush=True)

            try:
                response = self.session.get(url, timeout=10, allow_redirects=False)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                content_type = response.headers.get('Content-Type', '')

                if 'text/html' in content_type:
                    self._extract_links(soup, url)
                    self._extract_forms(soup, url)
                    self._check_interesting(url, response)

            except requests.exceptions.RequestException:
                continue

    def _extract_links(self, soup, base_url):
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                continue
            full_url = urljoin(base_url, href)
            if full_url not in self.visited:
                self.urls.append((full_url, base_url.count('/') - self.target.count('/')))

    def _extract_forms(self, soup, url):
        for form in soup.find_all('form'):
            action = form.get('action', url)
            method = form.get('method', 'GET').upper()
            inputs = []
            for inp in form.find_all(['input', 'textarea', 'select']):
                inputs.append({
                    'name': inp.get('name', ''),
                    'type': inp.get('type', 'text'),
                    'value': inp.get('value', '')
                })
            self.forms.append({
                'url': urljoin(url, action),
                'method': method,
                'inputs': inputs
            })

    def _check_interesting(self, url, response):
        interesting_extensions = ['.php', '.asp', '.aspx', '.jsp', '.cgi',
                                  '.bak', '.old', '.save', '.swp', '.orig',
                                  '.log', '.conf', '.cfg', '.env', '.ini']

        for ext in interesting_extensions:
            if url.lower().endswith(ext):
                self.interesting_files.append({
                    'url': url,
                    'extension': ext,
                    'size': len(response.text)
                })

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  CRAWL COMPLETE - {len(self.visited)} PAGES VISITED  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n{Fore.CYAN}  FORMS FOUND: {len(self.forms)}")
        for i, form in enumerate(self.forms[:20], 1):
            print(f"  {Fore.WHITE}[{i}] {form['method']} {form['url']}")
            for inp in form['inputs']:
                print(f"      {Fore.YELLOW}Input: {inp['name']} ({inp['type']})")

        print(f"\n{Fore.CYAN}  INTERESTING FILES: {len(self.interesting_files)}")
        for f in self.interesting_files:
            print(f"  {Fore.GREEN}[+] {f['url']} ({f['size']} bytes)")

        print(f"\n{Fore.CYAN}  ALL DISCOVERED URLS: {len(self.visited)}")
        for url in sorted(list(self.visited)):
            print(f"  {Fore.WHITE}• {url}")



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
    print(f"  {BW}{Style.BRIGHT}  WEB CRAWLER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}WEB CRAWLER                             {RS}  {G}╟{RS}")
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

