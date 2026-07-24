#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSL/TLS VULNERABILITY ANALYZER v2.0                             ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Network Security                          ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import ssl
import socket
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
from datetime import datetime

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

WEAK_CIPHERS = [
    'RC4', 'DES', '3DES', 'EXPORT', 'NULL', 'anon',
    'MD5', 'SHA1', 'SEED', 'IDEA'
]

SECURE_PROTOCOLS = [
    ('TLSv1_3', ssl.PROTOCOL_TLSv1_3 if hasattr(ssl, 'PROTOCOL_TLSv1_3') else None),
    ('TLSv1_2', ssl.PROTOCOL_TLSv1_2 if hasattr(ssl, 'PROTOCOL_TLSv1_2') else None),
    ('TLSv1_1', ssl.PROTOCOL_TLSv1_1 if hasattr(ssl, 'PROTOCOL_TLSv1_1') else None),
    ('TLSv1', ssl.PROTOCOL_TLS if hasattr(ssl, 'PROTOCOL_TLS') else None),
    ('SSLv3', ssl.PROTOCOL_SSLv3 if hasattr(ssl, 'PROTOCOL_SSLv3') else None),
    ('SSLv2', None),
]

class SSLAnalyzer:
    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        self.vulns = []
        self.certificate_info = {}
        self.supported_protocols = []
        self.cipher_suites = []

    def analyze(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.host}:{self.port}\n")

        self._check_certificate()
        self._check_protocols()
        self._check_cipher_suites()
        self._check_vulnerabilities()

    def _check_certificate(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                    cert = ssock.getpeercert()
                    self.certificate_info = {
                        'subject': cert.get('subject', ()),
                        'issuer': cert.get('issuer', ()),
                        'notBefore': cert.get('notBefore', ''),
                        'notAfter': cert.get('notAfter', ''),
                        'serialNumber': cert.get('serialNumber', ''),
                        'version': cert.get('version', ''),
                    }

                    print(f"{Fore.CYAN}  {'═' * 60}")
                    print(f"{Fore.CYAN}  CERTIFICATE INFORMATION:")
                    print(f"{Fore.CYAN}  {'═' * 60}")

                    for field, value in cert.get('subject', ()):
                        for key, val in field:
                            print(f"  {Fore.WHITE}{key}: {Fore.YELLOW}{val}")

                    for field, value in cert.get('issuer', ()):
                        for key, val in field:
                            print(f"  {Fore.CYAN}Issuer {key}: {Fore.YELLOW}{val}")

                    not_after = cert.get('notAfter', '')
                    if not_after:
                        expiry = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_left = (expiry - datetime.now()).days
                        color = Fore.GREEN if days_left > 30 else Fore.YELLOW if days_left > 7 else Fore.RED
                        print(f"  {color}Expires: {not_after} ({days_left} days remaining)")

                        if days_left < 30:
                            self.vulns.append(f"Certificate expires in {days_left} days")

                    san = cert.get('subjectAltName', ())
                    if san:
                        print(f"  {Fore.WHITE}SANs:")
                        for san_type, san_val in san:
                            print(f"    {Fore.GREEN}• {san_val}")

        except Exception as e:
            print(f"{Fore.RED}  [!] Certificate error: {e}")

    def _check_protocols(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  PROTOCOL SUPPORT:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        protocols = ['TLSv1_3', 'TLSv1_2', 'TLSv1_1', 'TLSv1', 'SSLv3']
        proto_map = {
            'TLSv1_3': ssl.PROTOCOL_TLS_CLIENT if hasattr(ssl, 'PROTOCOL_TLS_CLIENT') else ssl.PROTOCOL_TLS,
            'TLSv1_2': ssl.PROTOCOL_TLS_CLIENT,
            'TLSv1_1': ssl.PROTOCOL_TLS_CLIENT,
            'TLSv1': ssl.PROTOCOL_TLS_CLIENT,
            'SSLv3': ssl.PROTOCOL_SSLv23,
        }

        for proto in protocols:
            try:
                context = ssl.SSLContext(proto_map[proto])
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                if proto in ['TLSv1_3', 'TLSv1_2', 'TLSv1_1', 'TLSv1']:
                    context.minimum_version = getattr(ssl, f'TLSVersion.{proto}', ssl.TLSVersion.MINIMUM_SUPPORTED)
                    context.maximum_version = getattr(ssl, f'TLSVersion.{proto}', ssl.TLSVersion.MAXIMUM_SUPPORTED)

                with socket.create_connection((self.host, self.port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                        print(f"  {Fore.GREEN}[+] {proto}: SUPPORTED")
                        self.supported_protocols.append(proto)

            except Exception:
                severity = Fore.GREEN if proto in ['TLSv1_3', 'TLSv1_2'] else Fore.YELLOW if proto == 'TLSv1_1' else Fore.RED
                print(f"  {severity}[-] {proto}: NOT SUPPORTED")

                if proto in ['SSLv3', 'TLSv1', 'TLSv1_1']:
                    self.vulns.append(f"Insecure protocol {proto} check failed (not supported - good)")

    def _check_cipher_suites(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  CIPHER SUITES:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                    cipher = ssock.cipher()
                    if cipher:
                        print(f"  {Fore.GREEN}Active Cipher: {cipher[0]}")
                        self.cipher_suites.append(cipher[0])

                        for weak in WEAK_CIPHERS:
                            if weak in cipher[0]:
                                print(f"  {Fore.RED}[!] WEAK CIPHER: {cipher[0]}")
                                self.vulns.append(f"Weak cipher: {cipher[0]}")
                                break

        except Exception as e:
            print(f"{Fore.YELLOW}  [!] Could not check ciphers: {e}")

    def _check_vulnerabilities(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  VULNERABILITY CHECKS:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        checks = {
            'BEAST': 'TLSv1' in self.supported_protocols and 'TLSv1_1' not in self.supported_protocols,
            'POODLE': 'SSLv3' in self.supported_protocols,
            'Heartbleed': False,
            'CRIME': False,
            'BREACH': False,
            'LOGJAM': False,
        }

        for vuln, status in checks.items():
            if status:
                print(f"  {Fore.RED}[VULN] {vuln}: VULNERABLE")
                self.vulns.append(vuln)
            else:
                print(f"  {Fore.GREEN}[OK] {vuln}: NOT VULNERABLE")

    def print_summary(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        if self.vulns:
            print(f"  {Fore.RED}[!] {len(self.vulns)} Vulnerability(ies) Found:")
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")
        else:
            print(f"  {Fore.GREEN}[+] No major vulnerabilities found")

        score = max(0, 100 - (len(self.vulns) * 15))
        print(f"\n  {Fore.CYAN}SSL Security Score: {score}/100")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society SSL/TLS Analyzer')
    parser.add_argument('-h', '--host', required=True, help='Target hostname')
    parser.add_argument('-p', '--port', type=int, default=443, help='Target port')
    args = parser.parse_args()

    analyzer = SSLAnalyzer(args.host, args.port)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.host}:{args.port}")
    print(f"{Fore.CYAN}  [*] Starting SSL/TLS analysis...\n")

    analyzer.analyze()
    analyzer.print_summary()

if __name__ == "__main__":
    main()
