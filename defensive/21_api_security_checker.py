#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  API SECURITY CHECKER v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - API Security Assessment                   ║
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

class APISecurityChecker:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.issues = []
        self.ok = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 HellSociety/2.0',
            'Accept': 'application/json'
        })

    def check_authentication(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  AUTHENTICATION CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        endpoints = ['/api/v1/users', '/api/users', '/api/v1/admin']

        for endpoint in endpoints:
            url = f"{self.target}{endpoint}"
            try:
                resp = self.session.get(url, timeout=10)

                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if isinstance(data, (list, dict)) and len(str(data)) > 50:
                            print(f"  {Fore.RED}[!] {endpoint} - Data exposed without auth!")
                            self.issues.append(f'No auth: {endpoint}')
                    except:
                        pass
                elif resp.status_code in [401, 403]:
                    print(f"  {Fore.GREEN}[OK] {endpoint} - Requires authentication")
                    self.ok.append(endpoint)
                else:
                    print(f"  {Fore.YELLOW}[-] {endpoint} - Status: {resp.status_code}")
            except:
                pass

    def check_rate_limiting(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  RATE LIMITING CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        url = f"{self.target}/api/v1/test"
        rate_limited = False

        for i in range(15):
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 429:
                    rate_limited = True
                    print(f"  {Fore.GREEN}[OK] Rate limiting active (blocked at request {i+1})")
                    self.ok.append('Rate limiting')
                    break
            except:
                pass

        if not rate_limited:
            print(f"  {Fore.RED}[!] No rate limiting detected")
            self.issues.append('No rate limiting')

    def check_cors(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CORS CONFIGURATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            headers = {'Origin': 'https://evil.com', 'Host': 'api.example.com'}
            resp = self.session.options(self.target, headers=headers, timeout=10)

            if 'Access-Control-Allow-Origin' in resp.headers:
                origin = resp.headers['Access-Control-Allow-Origin']
                if origin == '*':
                    print(f"  {Fore.RED}[!] CORS allows any origin (*)")
                    self.issues.append('CORS wildcard')
                elif 'evil.com' in origin:
                    print(f"  {Fore.RED}[!] CORS reflects attacker origin")
                    self.issues.append('CORS reflection')
                else:
                    print(f"  {Fore.GREEN}[OK] CORS properly configured: {origin}")
                    self.ok.append('CORS')
            else:
                print(f"  {Fore.GREEN}[OK] No CORS headers (restrictive)")
                self.ok.append('No CORS')

        except:
            pass

    def check_information_disclosure(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  INFORMATION DISCLOSURE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = self.session.get(f"{self.target}/api/v1/nonexistent", timeout=10)

            if resp.status_code == 500:
                if 'traceback' in resp.text.lower() or 'stack trace' in resp.text.lower():
                    print(f"  {Fore.RED}[!] Stack trace exposed in error response")
                    self.issues.append('Stack trace exposed')
                else:
                    print(f"  {Fore.GREEN}[OK] Clean error response")
                    self.ok.append('Error handling')

            # Check for debug mode
            if 'debug' in resp.headers.get('X-Powered-By', '').lower():
                print(f"  {Fore.RED}[!] Debug mode enabled")
                self.issues.append('Debug mode')

        except:
            pass

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  API SECURITY CHECK COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        print(f"\n  {Fore.GREEN}[OK] Passed: {len(self.ok)}")
        for o in self.ok:
            print(f"    {Fore.GREEN}• {o}")

        score = max(0, 100 - (len(self.issues) * 15))
        color = Fore.GREEN if score >= 80 else (Fore.YELLOW if score >= 50 else Fore.RED)
        print(f"\n  {color}API Security Score: {score}/100")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society API Security Checker')
    parser.add_argument('-u', '--url', required=True, help='API base URL')
    args = parser.parse_args()

    checker = APISecurityChecker(args.url)
    checker.check_authentication()
    checker.check_rate_limiting()
    checker.check_cors()
    checker.check_information_disclosure()
    checker.print_summary()

if __name__ == "__main__":
    main()
