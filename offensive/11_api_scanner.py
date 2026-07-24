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

BANNER = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}     _    ____  ____ ___ ___   ____ _____ ____ _____ ____     {Fore.BLUE}║
║{Fore.CYAN}    / \\  | __ )| __ )_ _|_ _| / ___| ____/ ___|_   _/ ___|    {Fore.BLUE}║
║{Fore.CYAN}   / _ \\ |  _ \\|  _ \\| | | | | |  _|  _| \\___ \\ | | \\___ \\    {Fore.BLUE}║
║{Fore.CYAN}  / ___ \\| |_) | |_) | | | | | |_| | |___ ___) || |  ___) |   {Fore.BLUE}║
║{Fore.CYAN} /_/   \\_\\____/|____/___|___|  \\____|_____|____/ |_| |____/    {Fore.BLUE}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - API Security Scanner v2.0                              {Fore.BLUE}║
╚══════════════════════════════════════════════════════════════════╝
"""

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

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society API Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target API URL')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Timeout')
    args = parser.parse_args()

    scanner = APIScanner(args.url, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting API scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
