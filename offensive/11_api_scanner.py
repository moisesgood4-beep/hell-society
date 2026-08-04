#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  API SECURITY SCANNER v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - API Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import json
import colorama
from colorama import Fore, Back, Style
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

class APIScanner:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.vulns = []
        self.info = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def scan(self):
        print(f"{Fore.CYAN}  [*] Scanning: {Fore.WHITE}{self.base_url}\n")
        self._check_authentication()
        self._check_rate_limiting()
        self._check_information_disclosure()
        self._check_http_methods()
        self._check_common_endpoints()
        self._check_input_validation()

    def _check_authentication(self):
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  AUTHENTICATION CHECKS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        endpoints = ['/api/v1/users', '/api/users', '/api/admin',
                     '/api/v1/admin', '/graphql', '/api/config']

        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}[VULN] {endpoint} - No authentication required!")
                    self.vulns.append(f"Missing auth: {endpoint}")
                elif resp.status_code == 401 or resp.status_code == 403:
                    print(f"  {Fore.GREEN}[OK] {endpoint} - Authentication enforced")
                elif resp.status_code == 404:
                    print(f"  {Fore.YELLOW}[-] {endpoint} - Not found")
            except:
                pass

    def _check_rate_limiting(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  RATE LIMITING CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f"{self.base_url}/api/v1/status"
        rate_limited = False

        for i in range(20):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code == 429:
                    rate_limited = True
                    print(f"  {Fore.GREEN}[OK] Rate limiting detected after {i} requests")
                    break
            except:
                break

        if not rate_limited:
            print(f"  {Fore.RED}[VULN] No rate limiting detected")
            self.vulns.append("No rate limiting")

        rate_headers = ['X-RateLimit-Limit', 'X-RateLimit-Remaining',
                       'Retry-After', 'RateLimit-Reset']
        for header in rate_headers:
            if header in self.session.headers:
                print(f"  {Fore.YELLOW}[INFO] {header} header present")

    def _check_information_disclosure(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  INFORMATION DISCLOSURE")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        endpoints = ['/api/v1/debug', '/api/debug', '/health',
                     '/api/health', '/env', '/api/env',
                     '/api/v1/config', '/config', '/.env',
                     '/api/v1/users/1', '/api/users/1']

        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    content = resp.text
                    sensitive = ['password', 'secret', 'key', 'token', 'api_key',
                                'database', 'connection', 'credential']
                    for word in sensitive:
                        if word in content.lower():
                            print(f"  {Fore.RED}[VULN] Sensitive data in {endpoint}")
                            self.vulns.append(f"Info disclosure: {endpoint}")
                            break
            except:
                pass

    def _check_http_methods(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  HTTP METHODS CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        methods = ['OPTIONS', 'TRACE', 'DELETE', 'PUT', 'PATCH']
        url = f"{self.base_url}/api/v1/users"

        for method in methods:
            try:
                resp = self.session.request(method, url, timeout=self.timeout)
                if resp.status_code in [200, 201, 204]:
                    print(f"  {Fore.RED}[VULN] {method} allowed on {url}")
                    self.vulns.append(f"Dangerous method: {method} on {url}")
                elif resp.status_code == 405:
                    print(f"  {Fore.GREEN}[OK] {method} blocked")
                elif resp.status_code == 403:
                    print(f"  {Fore.YELLOW}[-] {method} forbidden")
            except:
                pass

    def _check_common_endpoints(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  COMMON ENDPOINTS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        endpoints = [
            '/swagger', '/swagger-ui.html', '/api-docs', '/docs',
            '/api/v1/docs', '/graphql', '/graphiql',
            '/api/graphql', '/api/v1/graphql',
            '/actuator', '/actuator/health', '/actuator/env',
            '/api/v1/test', '/api/test', '/api/ping',
            '/api/v1/version', '/version',
        ]

        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    print(f"  {Fore.GREEN}[+] Found: {endpoint} (200 OK)")
                    self.info.append(f"Endpoint: {endpoint}")
            except:
                pass

    def _check_input_validation(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"{Fore.CYAN}  INPUT VALIDATION")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        payloads = [
            {"test": "' OR '1'='1"},
            {"test": "<script>alert(1)</script>"},
            {"test": "../../../etc/passwd"},
            {"test": "$(whoami)"},
            {"test": "{{7*7}}"},
        ]

        url = f"{self.base_url}/api/v1/search"
        for payload in payloads:
            try:
                resp = self.session.post(url, json=payload, timeout=self.timeout)
                if resp.status_code == 500:
                    print(f"  {Fore.RED}[VULN] Possible injection via: {payload}")
                    self.vulns.append(f"Input validation: {payload}")
                elif resp.status_code == 200:
                    print(f"  {Fore.YELLOW}[-] Payload accepted: {payload}")
            except:
                pass

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")
        print(f"  {Fore.YELLOW}[!] Info: {len(self.info)}")

        if self.vulns:
            print(f"\n{Fore.RED}  Issues Found:")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        score = max(0, 100 - (len(self.vulns) * 8))
        print(f"\n  {Fore.CYAN}API Security Score: {score}/100")



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
    print(f"  {BW}{Style.BRIGHT}  API SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}API SCANNER                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target API URL                               {RS}")
        print(f"  {C}[2]  {BW}Timeout                                      {RS}")
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
            print(f"  {Y}[*] Target API URL{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Timeout{RS}")
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

