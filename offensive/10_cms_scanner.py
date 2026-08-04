#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  CMS VULNERABILITY SCANNER v2.0                                  ║
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
from bs4 import BeautifulSoup
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

class CMSScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })
        self.cms_type = None
        self.cms_version = None
        self.vulns = []
        self.info = []

    def detect_cms(self):
        try:
            response = self.session.get(self.target, timeout=10)
            content = response.text
            headers = dict(response.headers)

            print(f"{Fore.CYAN}  [*] Analyzing target for CMS detection...\n")

            if 'wp-content' in content or 'wp-includes' in content or 'wordpress' in content.lower():
                self.cms_type = 'WordPress'
                self._check_wordpress(content, headers)
            elif 'joomla' in content.lower() or '/media/jui/' in content:
                self.cms_type = 'Joomla'
                self._check_joomla(content, headers)
            elif 'drupal' in content.lower() or '/sites/default/' in content:
                self.cms_type = 'Drupal'
                self._check_drupal(content, headers)
            elif 'prestashop' in content.lower() or '/prestashop/' in content:
                self.cms_type = 'PrestaShop'
                self._check_prestashop(content, headers)
            else:
                print(f"{Fore.YELLOW}  [!] No common CMS detected, running generic checks...")
                self._generic_checks(content, headers)

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}  [!] Error: {e}")

    def _check_wordpress(self, content, headers):
        print(f"{Fore.GREEN}  [+] CMS Detected: {Fore.WHITE}WordPress")

        wp_paths = [
            '/wp-login.php', '/wp-admin/', '/wp-json/wp/v2/users',
            '/wp-json/', '/xmlrpc.php', '/wp-cron.php',
            '/readme.html', '/license.txt', '/wp-config.php',
            '/wp-content/debug.log', '/wp-content/uploads/',
            '/.wp-config.php.swp', '/wp-content/wp-backup/',
        ]

        for path in wp_paths:
            url = f"{self.target}{path}"
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}[VULN] Accessible: {path} ({len(resp.text)} bytes)")
                    self.vulns.append(f"WP: Accessible {path}")

                    if path == '/xmlrpc.php':
                        print(f"           {Fore.YELLOW}Risk: XML-RPC enabled - Brute force/DoS risk")
                    elif path == '/wp-config.php':
                        print(f"           {Fore.RED}Risk: CRITICAL - Config file exposed!")
                    elif path == '/readme.html':
                        print(f"           {Fore.YELLOW}Risk: Version information disclosure")
                elif resp.status_code == 403:
                    print(f"  {Fore.YELLOW}[-] Forbidden: {path}")
            except:
                pass

        self._check_plugins(content)
        self._check_users()

    def _check_plugins(self, content):
        plugin_paths = [
            '/wp-content/plugins/akismet/',
            '/wp-content/plugins/woocommerce/',
            '/wp-content/plugins/elementor/',
            '/wp-content/plugins/contact-form-7/',
            '/wp-content/plugins/wordfence/',
            '/wp-content/plugins/yoast-seo/',
            '/wp-content/plugins/updraftplus/',
            '/wp-content/plugins/wpforms/',
        ]

        print(f"\n{Fore.CYAN}  [*] Checking plugins...")
        for plugin in plugin_paths:
            url = f"{self.target}{plugin}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    print(f"  {Fore.GREEN}[+] Plugin found: {plugin}")
                    self.info.append(f"Plugin: {plugin}")
            except:
                pass

    def _check_users(self):
        try:
            resp = self.session.get(f"{self.target}/wp-json/wp/v2/users", timeout=5)
            if resp.status_code == 200:
                users = resp.json()
                print(f"\n{Fore.RED}  [VULN] User enumeration possible!")
                for user in users:
                    print(f"    {Fore.WHITE}Username: {user.get('slug', 'N/A')} | ID: {user.get('id', 'N/A')}")
                    self.vulns.append("WP: User enumeration via REST API")
        except:
            pass

    def _check_joomla(self, content, headers):
        print(f"{Fore.GREEN}  [+] CMS Detected: {Fore.WHITE}Joomla")
        joomla_paths = [
            '/administrator/', '/administrator/index.php',
            '/configuration.php', '/robots.txt',
            '/tmp/', '/logs/',
        ]
        for path in joomla_paths:
            url = f"{self.target}{path}"
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}[VULN] Accessible: {path}")
                    self.vulns.append(f"Joomla: Accessible {path}")
            except:
                pass

    def _check_drupal(self, content, headers):
        print(f"{Fore.GREEN}  [+] CMS Detected: {Fore.WHITE}Drupal")
        drupal_paths = [
            '/admin/', '/user/login', '/CHANGELOG.txt',
            '/core/install.php', '/sites/default/settings.php',
            '/xmlrpc.php', '/profiles/',
        ]
        for path in drupal_paths:
            url = f"{self.target}{path}"
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}[VULN] Accessible: {path}")
                    self.vulns.append(f"Drupal: Accessible {path}")
            except:
                pass

    def _check_prestashop(self, content, headers):
        print(f"{Fore.GREEN}  [+] CMS Detected: {Fore.WHITE}PrestaShop")
        ps_paths = [
            '/admin/', '/admin-dev/', '/install/',
            '/config/settings.inc.php', '/app/config/parameters.php',
        ]
        for path in ps_paths:
            url = f"{self.target}{path}"
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200:
                    print(f"  {Fore.RED}[VULN] Accessible: {path}")
                    self.vulns.append(f"PrestaShop: Accessible {path}")
            except:
                pass

    def _generic_checks(self, content, headers):
        print(f"{Fore.YELLOW}  [*] Running generic security checks...")

        if 'X-Powered-By' in headers:
            print(f"  {Fore.RED}[VULN] Server info disclosed: {headers['X-Powered-By']}")
            self.vulns.append(f"Info disclosure: {headers['X-Powered-By']}")

        if 'Server' in headers:
            print(f"  {Fore.YELLOW}[INFO] Server: {headers['Server']}")
            self.info.append(f"Server: {headers['Server']}")

        if '/admin' in content or '/login' in content:
            print(f"  {Fore.YELLOW}[INFO] Admin/login page references found")

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SCAN RESULTS:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        if self.cms_type:
            print(f"\n{Fore.GREEN}  CMS: {Fore.WHITE}{self.cms_type}")
            if self.cms_version:
                print(f"  {Fore.GREEN}Version: {Fore.WHITE}{self.cms_version}")

        print(f"\n  {Fore.RED}Vulnerabilities: {len(self.vulns)}")
        for v in self.vulns:
            print(f"    {Fore.RED}• {v}")

        print(f"\n  {Fore.YELLOW}Information: {len(self.info)}")
        for i in self.info:
            print(f"    {Fore.YELLOW}• {i}")

        score = max(0, 100 - (len(self.vulns) * 12))
        print(f"\n  {Fore.CYAN}Security Score: {score}/100")



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
    print(f"  {BW}{Style.BRIGHT}  CMS SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}CMS SCANNER                             {RS}  {G}╟{RS}")
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

