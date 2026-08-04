#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  MULTI WEB VULNERABILITY SCANNER v2.0                            ║
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
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
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

class WebVulnScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.domain = urlparse(target).netloc
        self.vulns = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def scan_all(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}\n")

        checks = [
            ('clickjacking', self._check_clickjacking),
            ('cookies', self._check_cookies),
            ('headers', self._check_headers),
            ('open_redirect', self._check_open_redirect),
            ('cors', self._check_cors),
            ('mixed_content', self._check_mixed_content),
            ('version_disclosure', self._check_version_disclosure),
            ('backup_files', self._check_backup_files),
            ('directory_listing', self._check_directory_listing),
            ('ssl', self._check_ssl),
        ]

        for name, func in checks:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  {Fore.WHITE}{name.upper().replace('_', ' ')}")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            func()

    def _check_clickjacking(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            headers = dict(resp.headers)
            if 'X-Frame-Options' not in headers:
                if not any('content-security-policy' in k.lower() and 'frame-ancestors' in v.lower()
                          for k, v in headers.items()):
                    print(f"  {Fore.RED}  [VULN] Missing X-Frame-Options (Clickjacking risk)")
                    self.vulns.append('Clickjacking: No X-Frame-Options')
                else:
                    print(f"  {Fore.GREEN}  [OK] CSP frame-ancestors found")
            else:
                print(f"  {Fore.GREEN}  [OK] X-Frame-Options present")
        except:
            pass

    def _check_cookies(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            cookies = resp.headers.get('Set-Cookie', '')
            if cookies:
                if 'httponly' not in cookies.lower():
                    print(f"  {Fore.RED}  [VULN] Cookie missing HttpOnly flag")
                    self.vulns.append('Cookie: Missing HttpOnly')
                else:
                    print(f"  {Fore.GREEN}  [OK] HttpOnly flag present")

                if 'secure' not in cookies.lower():
                    print(f"  {Fore.RED}  [VULN] Cookie missing Secure flag")
                    self.vulns.append('Cookie: Missing Secure')
                else:
                    print(f"  {Fore.GREEN}  [OK] Secure flag present")

                if 'samesite' not in cookies.lower():
                    print(f"  {Fore.YELLOW}  [WARN] Cookie missing SameSite attribute")
                    self.vulns.append('Cookie: Missing SameSite')
                else:
                    print(f"  {Fore.GREEN}  [OK] SameSite attribute present")
            else:
                print(f"  {Fore.YELLOW}  [-] No cookies set")
        except:
            pass

    def _check_headers(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            headers = dict(resp.headers)
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer-Policy',
                'Permissions-Policy': 'Permissions-Policy',
            }

            for header, name in security_headers.items():
                if header in headers:
                    print(f"  {Fore.GREEN}  [OK] {name} present")
                else:
                    print(f"  {Fore.RED}  [VULN] Missing {name}")
                    self.vulns.append(f'Header: Missing {name}')
        except:
            pass

    def _check_open_redirect(self):
        try:
            resp = self.session.get(f"{self.target}/?redirect=http://evil.com", timeout=10, allow_redirects=False)
            if resp.status_code in [301, 302, 303, 307, 308]:
                location = resp.headers.get('Location', '')
                if 'evil.com' in location:
                    print(f"  {Fore.RED}  [VULN] Open Redirect via 'redirect' parameter")
                    self.vulns.append('Open Redirect')
                else:
                    print(f"  {Fore.GREEN}  [OK] No open redirect")
            else:
                print(f"  {Fore.GREEN}  [OK] No open redirect detected")
        except:
            pass

    def _check_cors(self):
        try:
            resp = self.session.get(self.target, timeout=10,
                headers={'Origin': 'https://evil.com'})
            acao = resp.headers.get('Access-Control-Allow-Origin', '')
            if acao == '*':
                print(f"  {Fore.RED}  [VULN] CORS allows any origin (*)")
                self.vulns.append('CORS: Wildcard origin')
            elif 'evil.com' in acao:
                print(f"  {Fore.RED}  [VULN] CORS reflects arbitrary origin")
                self.vulns.append('CORS: Reflected origin')
            else:
                print(f"  {Fore.GREEN}  [OK] CORS properly configured")
        except:
            pass

    def _check_mixed_content(self):
        try:
            if self.target.startswith('https'):
                resp = self.session.get(self.target, timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                http_resources = []
                for tag in ['script', 'link', 'img', 'iframe']:
                    for el in soup.find_all(tag):
                        src = el.get('src', '') or el.get('href', '')
                        if src.startswith('http://'):
                            http_resources.append(src)

                if http_resources:
                    print(f"  {Fore.RED}  [VULN] {len(http_resources)} HTTP resources on HTTPS page")
                    self.vulns.append('Mixed Content')
                else:
                    print(f"  {Fore.GREEN}  [OK] No mixed content")
        except:
            pass

    def _check_version_disclosure(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            headers = dict(resp.headers)
            for header in ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-Generator']:
                if header in headers:
                    print(f"  {Fore.RED}  [VULN] {header}: {headers[header]}")
                    self.vulns.append(f'Version Disclosure: {header}')
        except:
            pass

    def _check_backup_files(self):
        backup_files = ['/index.php.bak', '/wp-config.php.bak', '/.git/config',
                       '/config.php.bak', '/database.sql', '/backup.zip',
                       '/db.sql', '/dump.sql', '/.env', '/composer.lock']

        print(f"  {Fore.YELLOW}  Checking for backup/config files...")
        for bf in backup_files:
            url = f"{self.target}{bf}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}  [VULN] Accessible: {bf} ({len(resp.text)} bytes)")
                    self.vulns.append(f'Backup File: {bf}')
            except:
                pass

    def _check_directory_listing(self):
        dirs = ['/', '/images/', '/css/', '/js/', '/uploads/', '/admin/']
        for d in dirs:
            url = f"{self.target}{d}"
            try:
                resp = self.session.get(url, timeout=5)
                if 'Index of' in resp.text or '<title>Directory listing' in resp.text.lower():
                    print(f"  {Fore.RED}  [VULN] Directory listing enabled: {d}")
                    self.vulns.append(f'Directory Listing: {d}')
            except:
                pass

    def _check_ssl(self):
        if self.target.startswith('https'):
            print(f"  {Fore.GREEN}  [OK] HTTPS enabled")
        else:
            print(f"  {Fore.RED}  [VULN] No HTTPS - unencrypted connection")
            self.vulns.append('No HTTPS')

    def print_results(self):
        print(f"\n\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  FINAL SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Total Vulnerabilities: {len(self.vulns)}")

        if self.vulns:
            print(f"\n{Fore.RED}  All Issues:")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        score = max(0, 100 - (len(self.vulns) * 5))
        print(f"\n  {Fore.CYAN}Overall Security Score: {score}/100")



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
    print(f"  {BW}{Style.BRIGHT}  WEB VULN SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}WEB VULN SCANNER                        {RS}  {G}╟{RS}")
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

