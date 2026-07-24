#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEB APPLICATION DEFENSE SCANNER v2.0                            ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Web App Security Assessment               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import requests
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import json

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

class WebAppDefender:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.vulns = []
        self.ok = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 HellSociety/2.0',
            'Accept': '*/*'
        })

    def check_security_headers(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SECURITY HEADERS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        required_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'X-XSS-Protection': 'XSS filter',
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'Referrer-Policy': 'Referrer control',
            'Permissions-Policy': 'Feature policy',
        }

        try:
            resp = self.session.get(self.target, timeout=10)
            headers = resp.headers

            for header, purpose in required_headers.items():
                if header in headers:
                    print(f"  {Fore.GREEN}[OK] {header}: {headers[header][:50]}")
                    self.ok.append(header)
                else:
                    print(f"  {Fore.RED}[MISSING] {header} - {purpose}")
                    self.vulns.append(f'Missing: {header}')

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_cookies(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  COOKIE SECURITY:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = self.session.get(self.target, timeout=10)
            cookies = resp.cookies

            for cookie in cookies:
                flags = []
                if cookie.secure:
                    flags.append('Secure')
                if cookie.has_nonstandard_attr('HttpOnly'):
                    flags.append('HttpOnly')
                if cookie.has_nonstandard_attr('SameSite'):
                    flags.append('SameSite')

                if not cookie.secure:
                    print(f"  {Fore.RED}[!] {cookie.name}: Missing Secure flag")
                    self.vulns.append(f'Insecure cookie: {cookie.name}')

                if not cookie.has_nonstandard_attr('HttpOnly'):
                    print(f"  {Fore.YELLOW}[-] {cookie.name}: Missing HttpOnly")
                    self.vulns.append(f'No HttpOnly: {cookie.name}')

            if not cookies:
                print(f"  {Fore.GREEN}[OK] No cookies set")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_http_methods(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  HTTP METHODS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        dangerous_methods = ['TRACE', 'DELETE', 'PUT', 'OPTIONS', 'PATCH']

        for method in dangerous_methods:
            try:
                resp = self.session.request(method, self.target, timeout=5)
                if resp.status_code not in [403, 405, 501]:
                    print(f"  {Fore.RED}[!] {method} method allowed (status: {resp.status_code})")
                    self.vulns.append(f'{method} method allowed')
                else:
                    print(f"  {Fore.GREEN}[OK] {method} blocked ({resp.status_code})")
            except:
                print(f"  {Fore.GREEN}[OK] {method} not available")

    def check_directory_listing(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DIRECTORY LISTING:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        dirs = ['/images/', '/uploads/', '/files/', '/assets/', '/css/', '/js/']

        for d in dirs:
            try:
                resp = self.session.get(f"{self.target}{d}", timeout=5)
                if resp.status_code == 200 and 'Index of' in resp.text:
                    print(f"  {Fore.RED}[!] Directory listing: {d}")
                    self.vulns.append(f'Dir listing: {d}')
                elif resp.status_code == 403:
                    print(f"  {Fore.GREEN}[OK] {d} protected")
            except:
                pass

    def check_ssl(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SSL/TLS CONFIG:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if self.target.startswith('https://'):
            print(f"  {Fore.GREEN}[OK] HTTPS enabled")
            self.ok.append('HTTPS')
        else:
            print(f"  {Fore.RED}[!!!] HTTPS NOT enabled!")
            self.vulns.append('No HTTPS')

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  WEB APP SECURITY CHECK COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")
        for v in self.vulns:
            print(f"    {Fore.RED}• {v}")

        print(f"\n  {Fore.GREEN}[OK] Passed: {len(self.ok)}")
        for o in self.ok:
            print(f"    {Fore.GREEN}• {o}")

        score = max(0, 100 - (len(self.vulns) * 7))
        color = Fore.GREEN if score >= 80 else (Fore.YELLOW if score >= 50 else Fore.RED)
        print(f"\n  {color}Web App Security Score: {score}/100")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Web App Defender')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()

    scanner = WebAppDefender(args.url)
    scanner.check_security_headers()
    scanner.check_cookies()
    scanner.check_http_methods()
    scanner.check_directory_listing()
    scanner.check_ssl()
    scanner.print_summary()

if __name__ == "__main__":
    main()
