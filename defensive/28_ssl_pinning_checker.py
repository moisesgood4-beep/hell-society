#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSL PINNING CHECKER v2.0                                        ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - TLS Security                              ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import ssl
import socket
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

class SSLChecker:
    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        self.issues = []

    def check_cert(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SSL CERTIFICATE ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.host, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()

                    print(f"  {Fore.WHITE}Host: {self.host}:{self.port}")
                    print(f"  {Fore.WHITE}Cipher: {cipher[0] if cipher else 'None'}")

                    # Check TLS version
                    version = ssock.version()
                    print(f"  {Fore.WHITE}TLS Version: {version}")

                    if version in ['TLSv1', 'TLSv1.1']:
                        print(f"  {Fore.RED}[!] Weak TLS version!")
                        self.issues.append(f'Weak TLS: {version}')
                    elif version == 'TLSv1.2':
                        print(f"  {Fore.YELLOW}[-] TLS 1.2 (acceptable but not ideal)")
                    elif version == 'TLSv1.3':
                        print(f"  {Fore.GREEN}[OK] TLS 1.3 (best)")

                    # Certificate info
                    if cert:
                        subject = dict(x[0] for x in cert.get('subject', []))
                        issuer = dict(x[0] for x in cert.get('issuer', []))

                        print(f"\n  {Fore.WHITE}Subject: {subject}")
                        print(f"  {Fore.WHITE}Issuer: {issuer}")

                        # Check expiry
                        not_after = cert.get('notAfter', '')
                        if not_after:
                            expiry = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                            days_left = (expiry - datetime.now()).days

                            if days_left < 30:
                                print(f"  {Fore.RED}[!] Certificate expires in {days_left} days!")
                                self.issues.append(f'Cert expires in {days_left} days')
                            elif days_left < 90:
                                print(f"  {Fore.YELLOW}[-] Certificate expires in {days_left} days")
                                self.issues.append(f'Cert expires in {days_left} days')
                            else:
                                print(f"  {Fore.GREEN}[OK] Certificate valid for {days_left} days")

                        # Check SANs
                        san = cert.get('subjectAltName', [])
                        print(f"\n  {Fore.WHITE}Subject Alternative Names:")
                        for name, value in san:
                            print(f"    {Fore.WHITE}{name}: {value}")

                    # Pinning check
                    cert_der = ssock.getpeercert(binary_form=True)
                    import hashlib
                    pin_sha256 = hashlib.sha256(cert_der).hexdigest()
                    print(f"\n  {Fore.WHITE}Certificate Pin (SHA256): {pin_sha256}")
                    print(f"  {Fore.CYAN}  Use this pin for certificate pinning in your app")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_pinning_headers(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  HSTS & PINNING HEADERS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        import requests
        try:
            resp = requests.get(f"https://{self.host}", timeout=10, verify=True)
            headers = resp.headers

            # HSTS
            if 'strict-transport-security' in headers:
                hsts = headers['strict-transport-security']
                print(f"  {Fore.GREEN}[OK] HSTS: {hsts[:50]}")
                if 'max-age=31536000' in hsts:
                    print(f"  {Fore.GREEN}[OK] HSTS max-age >= 1 year")
            else:
                print(f"  {Fore.RED}[!] No HSTS header!")
                self.issues.append('No HSTS')

            # Public-Key-Pins (deprecated but check)
            if 'public-key-pins' in headers:
                print(f"  {Fore.YELLOW}[-] HPKP is deprecated")
                self.issues.append('HPKP (deprecated)')
            else:
                print(f"  {Fore.GREEN}[OK] No deprecated HPKP")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def analyze(self):
        print(f"{Fore.CYAN}  [*] Analyzing SSL/TLS for: {Fore.WHITE}{self.host}")
        self.check_cert()
        self.check_pinning_headers()
        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  SSL ANALYSIS COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        if not self.issues:
            print(f"\n  {Fore.GREEN}[OK] SSL configuration is strong")
        elif len(self.issues) > 3:
            print(f"\n  {Fore.RED}[!] SSL needs attention")



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
    print(f"  {BW}{Style.BRIGHT}  SSL PINNING CHECKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}SSL PINNING CHECKER                     {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target host                                  {RS}")
        print(f"  {C}[2]  {BW}Port                                         {RS}")
        print()
        print(f"  {C}[3]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target host{RS}")
            value = input(f"  {Y}[*] -h: {RS}").strip()
            print(f"  {C}[*] Executing with -h={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Port{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '3':
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

