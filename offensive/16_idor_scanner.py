#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  IDOR VULNERABILITY SCANNER v2.0                                 ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - API/Web Pentesting                        ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import colorama
from colorama import Fore, Back, Style
from urllib.parse import urlparse, urlunparse
import argparse
import re

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗        {Fore.MAGENTA}║
║{Fore.CYAN}  ██║████╗  ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝        {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██╔██╗ ██║█████╗  ██║     ██║   ██║██║  ██║█████╗          {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║╚██╗██║██╔══╝  ██║     ██║   ██║██║  ██║██╔══╝          {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║ ╚████║███████╗╚██████╗╚██████╔╝██████╔╝███████╗        {Fore.MAGENTA}║
║{Fore.CYAN}  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝        {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - IDOR Scanner v2.0                                    {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores NO se hacen responsables del mal uso.
"""

class IDORScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.vulns = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def scan(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}\n")
        print(f"{Fore.CYAN}  [*] Testing for Insecure Direct Object References...\n")

        self._test_numeric_ids()
        self._test_uuid_manipulation()
        self._test_filename_based()
        self._test_api_endpoints()

    def _test_numeric_ids(self):
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        print(f"  NUMERIC ID MANIPULATION")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        parsed = urlparse(self.target)
        path = parsed.path

        id_patterns = re.findall(r'/(\d+)', path)
        if not id_patterns:
            print(f"  {Fore.YELLOW}  [!] No numeric IDs found in URL path")
            return

        for id_val in id_patterns:
            original_id = int(id_val)
            test_ids = [original_id + 1, original_id - 1, original_id + 10,
                       original_id * 2, 1, 0]

            for test_id in test_ids:
                test_path = path.replace(f'/{id_val}', f'/{test_id}')
                test_url = urlunparse((parsed.scheme, parsed.netloc, test_path,
                                       parsed.params, parsed.query, parsed.fragment))
                try:
                    resp = self.session.get(test_url, timeout=10)
                    if resp.status_code == 200:
                        if len(resp.text) > 100:
                            print(f"  {Fore.RED}[VULN] ID {test_id} accessible (replaced {original_id})")
                            self.vulns.append(f"Numeric IDOR: {test_url}")
                except:
                    pass

    def _test_uuid_manipulation(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  UUID PARAMETER MANIPULATION")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        from urllib.parse import parse_qs
        params = parse_qs(urlparse(self.target).query)

        for param, values in params.items():
            for val in values:
                if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', val, re.I):
                    print(f"  {Fore.GREEN}[+] UUID found in param: {param}")
                    print(f"  {Fore.YELLOW}  Testing predictable UUIDs...")

                    test_uuids = [
                        '00000000-0000-0000-0000-000000000001',
                        '00000000-0000-0000-0000-000000000002',
                        val[:20] + '000000000001',
                    ]

                    for test_uuid in test_uuids:
                        test_url = self.target.replace(val, test_uuid)
                        try:
                            resp = self.session.get(test_url, timeout=10)
                            if resp.status_code == 200 and len(resp.text) > 100:
                                print(f"  {Fore.RED}[VULN] UUID {test_uuid} accessible")
                                self.vulns.append(f"UUID IDOR: {test_uuid}")
                        except:
                            pass

    def _test_filename_based(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  FILENAME-BASED IDOR")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        parsed = urlparse(self.target)
        path_parts = parsed.path.split('/')
        last_part = path_parts[-1] if path_parts else ''

        if '.' in last_part:
            name, ext = last_part.rsplit('.', 1)
            test_names = [f"{name}_admin.{ext}", f"admin_{name}.{ext}",
                         f"{name}_priv.{ext}", f"root.{ext}"]

            for test_name in test_names:
                test_path = '/'.join(path_parts[:-1]) + '/' + test_name
                test_url = urlunparse((parsed.scheme, parsed.netloc, test_path,
                                       parsed.params, parsed.query, parsed.fragment))
                try:
                    resp = self.session.get(test_url, timeout=10)
                    if resp.status_code == 200:
                        print(f"  {Fore.RED}[VULN] File accessible: {test_name}")
                        self.vulns.append(f"File IDOR: {test_name}")
                except:
                    pass

    def _test_api_endpoints(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  API ENDPOINT IDOR")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        api_paths = ['/api/v1/users', '/api/users', '/api/v1/orders',
                     '/api/orders', '/api/v1/accounts', '/api/accounts']

        base = f"{urlparse(self.target).scheme}://{urlparse(self.target).netloc}"

        for path in api_paths:
            url = f"{base}{path}"
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if isinstance(data, (list, dict)) and len(str(data)) > 50:
                            print(f"  {Fore.RED}[VULN] Data exposed: {path}")
                            self.vulns.append(f"API IDOR: {path}")
                    except:
                        pass
            except:
                pass

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")

        if self.vulns:
            print(f"\n{Fore.RED}  Issues:")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        score = max(0, 100 - (len(self.vulns) * 20))
        print(f"\n  {Fore.CYAN}IDOR Security Score: {score}/100")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society IDOR Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()

    scanner = IDORScanner(args.url)
    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
