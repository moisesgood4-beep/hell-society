#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HTTP HEADER SECURITY ANALYZER v2.0                              ║
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

class HeaderAnalyzer:
    def __init__(self, target):
        self.target = target
        self.vulns = []
        self.info = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def analyze(self):
        try:
            response = self.session.get(self.target, timeout=10)
            headers = dict(response.headers)

            print(f"{Fore.CYAN}  [*] Response Status: {response.status_code}")
            print(f"{Fore.CYAN}  [*] Response Time: {response.elapsed.total_seconds():.3f}s")
            print(f"{Fore.CYAN}  [*] Server: {headers.get('Server', 'Unknown')}\n")

            print(f"{Fore.CYAN}  {'═' * 60}")
            print(f"{Fore.CYAN}  ALL RESPONSE HEADERS:")
            print(f"{Fore.CYAN}  {'═' * 60}")
            for key, value in headers.items():
                print(f"  {Fore.WHITE}{key}: {Fore.YELLOW}{value}")

            print(f"\n{Fore.CYAN}  {'═' * 60}")
            print(f"{Fore.CYAN}  SECURITY ANALYSIS:")
            print(f"{Fore.CYAN}  {'═' * 60}\n")

            self._check_security_headers(headers)
            self._check_information_disclosure(headers)
            self._check_cookies(headers)

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}  [!] Error: {e}")

    def _check_security_headers(self, headers):
        security_checks = {
            'Strict-Transport-Security': {
                'check': lambda h: 'Strict-Transport-Security' in h,
                'msg': 'HSTS (HTTP Strict Transport Security) - MISSING',
                'severity': 'HIGH',
                'fix': 'Add: Strict-Transport-Security: max-age=31536000; includeSubDomains'
            },
            'X-Content-Type-Options': {
                'check': lambda h: h.get('X-Content-Type-Options') == 'nosniff',
                'msg': 'X-Content-Type-Options: nosniff - MISSING',
                'severity': 'MEDIUM',
                'fix': 'Add: X-Content-Type-Options: nosniff'
            },
            'X-Frame-Options': {
                'check': lambda h: 'X-Frame-Options' in h,
                'msg': 'X-Frame-Options - MISSING (Clickjacking risk)',
                'severity': 'MEDIUM',
                'fix': 'Add: X-Frame-Options: DENY or SAMEORIGIN'
            },
            'X-XSS-Protection': {
                'check': lambda h: h.get('X-XSS-Protection', '') == '1; mode=block',
                'msg': 'X-XSS-Protection: 1; mode=block - MISSING',
                'severity': 'LOW',
                'fix': 'Add: X-XSS-Protection: 1; mode=block'
            },
            'Content-Security-Policy': {
                'check': lambda h: 'Content-Security-Policy' in h,
                'msg': 'Content-Security-Policy - MISSING',
                'severity': 'HIGH',
                'fix': 'Add CSP header with restrictive policy'
            },
            'Referrer-Policy': {
                'check': lambda h: 'Referrer-Policy' in h,
                'msg': 'Referrer-Policy - MISSING',
                'severity': 'LOW',
                'fix': 'Add: Referrer-Policy: strict-origin-when-cross-origin'
            },
            'Permissions-Policy': {
                'check': lambda h: 'Permissions-Policy' in h,
                'msg': 'Permissions-Policy - MISSING',
                'severity': 'LOW',
                'fix': 'Add: Permissions-Policy: camera=(), microphone=(), geolocation=()'
            },
            'Cross-Origin-Embedder-Policy': {
                'check': lambda h: 'Cross-Origin-Embedder-Policy' in h,
                'msg': 'Cross-Origin-Embedder-Policy - MISSING',
                'severity': 'LOW',
                'fix': 'Add: Cross-Origin-Embedder-Policy: require-corp'
            },
            'Cross-Origin-Opener-Policy': {
                'check': lambda h: 'Cross-Origin-Opener-Policy' in h,
                'msg': 'Cross-Origin-Opener-Policy - MISSING',
                'severity': 'LOW',
                'fix': 'Add: Cross-Origin-Opener-Policy: same-origin'
            },
            'Cross-Origin-Resource-Policy': {
                'check': lambda h: 'Cross-Origin-Resource-Policy' in h,
                'msg': 'Cross-Origin-Resource-Policy - MISSING',
                'severity': 'LOW',
                'fix': 'Add: Cross-Origin-Resource-Policy: same-origin'
            },
        }

        for header, check_info in security_checks.items():
            if not check_info['check'](headers):
                severity_color = Fore.RED if check_info['severity'] == 'HIGH' else Fore.YELLOW if check_info['severity'] == 'MEDIUM' else Fore.CYAN
                print(f"  {Fore.RED}[VULN] {severity_color}{check_info['severity']} {Fore.WHITE}{check_info['msg']}")
                print(f"          {Fore.GREEN}{check_info['fix']}")
                self.vulns.append(check_info['msg'])

    def _check_information_disclosure(self, headers):
        info_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-AspNetMvc-Version', 'X-Varnish']

        for header in info_headers:
            if header in headers:
                print(f"  {Fore.YELLOW}[INFO] {header}: {Fore.WHITE}{headers[header]}")
                print(f"          {Fore.RED}Risk: Information Disclosure - Server technology exposed")
                self.info.append(f"{header}: {headers[header]}")

    def _check_cookies(self, headers):
        set_cookie = headers.get('Set-Cookie', '')
        if set_cookie:
            if 'httponly' not in set_cookie.lower():
                print(f"\n  {Fore.RED}[VULN] HIGH Cookie missing HttpOnly flag")
                print(f"          {Fore.GREEN}Fix: Add HttpOnly flag to cookies")
                self.vulns.append('Cookie missing HttpOnly')

            if 'secure' not in set_cookie.lower():
                print(f"  {Fore.RED}[VULN] HIGH Cookie missing Secure flag")
                print(f"          {Fore.GREEN}Fix: Add Secure flag to cookies")
                self.vulns.append('Cookie missing Secure')

    def print_summary(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Vulnerabilities Found: {len(self.vulns)}")
        print(f"  {Fore.YELLOW}[!] Info Disclosures: {len(self.info)}")

        if self.vulns:
            print(f"\n{Fore.RED}  Issues:")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        if self.info:
            print(f"\n{Fore.YELLOW}  Information Disclosures:")
            for i in self.info:
                print(f"    {Fore.YELLOW}• {i}")

        score = max(0, 100 - (len(self.vulns) * 10) - (len(self.info) * 3))
        print(f"\n  {Fore.CYAN}Security Score: {score}/100")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Header Analyzer')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()

    analyzer = HeaderAnalyzer(args.url)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Analyzing headers...\n")

    analyzer.analyze()
    analyzer.print_summary()

if __name__ == "__main__":
    main()
