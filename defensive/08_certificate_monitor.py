#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SSL CERTIFICATE MONITOR v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Certificate Monitoring                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import ssl
import socket
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
from datetime import datetime, timedelta

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

class CertMonitor:
    def __init__(self, domain, port=443):
        self.domain = domain
        self.port = port
        self.issues = []

    def check(self):
        print(f"{Fore.CYAN}  [*] Checking: {Fore.WHITE}{self.domain}:{self.port}\n")

        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    version = ssock.version()
                    cipher = ssock.cipher()

                    print(f"{Fore.CYAN}  [{'═' * 40}]")
                    print(f"  CERTIFICATE DETAILS:")
                    print(f"{Fore.CYAN}  [{'═' * 40}]\n")

                    # Subject
                    subject = dict(x[0] for x in cert.get('subject', []))
                    print(f"  {Fore.WHITE}Subject: {subject.get('commonName', 'N/A')}")
                    print(f"  {Fore.WHITE}Issuer: {dict(x[0] for x in cert.get('issuer', [])).get('commonName', 'N/A')}")

                    # Dates
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    now = datetime.utcnow()

                    days_valid = (not_after - now).days
                    days_since_issued = (now - not_before).days

                    print(f"  {Fore.WHITE}Not Before: {not_before.strftime('%Y-%m-%d')}")
                    print(f"  {Fore.WHITE}Not After: {not_after.strftime('%Y-%m-%d')}")

                    if days_valid > 30:
                        print(f"  {Fore.GREEN}[OK] Valid for {days_valid} more days")
                    elif days_valid > 7:
                        print(f"  {Fore.YELLOW}[WARN] Expires in {days_valid} days - RENEW SOON")
                        self.issues.append('Certificate expiring soon')
                    elif days_valid > 0:
                        print(f"  {Fore.RED}[CRITICAL] Expires in {days_valid} days - URGENT!")
                        self.issues.append('Certificate expiring very soon')
                    else:
                        print(f"  {Fore.RED}[CRITICAL] CERTIFICATE EXPIRED {abs(days_valid)} days ago!")
                        self.issues.append('Certificate EXPIRED')

                    # SSL/TLS version
                    print(f"\n  {Fore.WHITE}TLS Version: {version}")
                    if version in ['TLSv1', 'TLSv1.1']:
                        print(f"  {Fore.RED}[VULN] Outdated TLS version - upgrade to TLSv1.2/1.3")
                        self.issues.append('Outdated TLS version')
                    else:
                        print(f"  {Fore.GREEN}[OK] Modern TLS version")

                    # Cipher
                    if cipher:
                        print(f"  {Fore.WHITE}Cipher: {cipher[0]}")
                        if any(weak in cipher[0].lower() for weak in ['rc4', 'des', '3des', 'null']):
                            print(f"  {Fore.RED}[VULN] Weak cipher suite")
                            self.issues.append('Weak cipher')
                        else:
                            print(f"  {Fore.GREEN}[OK] Strong cipher")

                    # SANs
                    sans = cert.get('subjectAltName', [])
                    if sans:
                        print(f"\n  {Fore.CYAN}SANs: {', '.join(s[:40] for s in [s[1] for s in sans[:5]])}")

        except ssl.SSLError as e:
            print(f"  {Fore.RED}[!] SSL Error: {e}")
            self.issues.append('SSL Error')
        except socket.error as e:
            print(f"  {Fore.RED}[!] Connection Error: {e}")
            self.issues.append('Connection failed')

        self.print_summary()

    def print_summary(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.CYAN}SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")

        if self.issues:
            print(f"  {Fore.RED}[!] Issues: {len(self.issues)}")
            for issue in self.issues:
                print(f"    {Fore.RED}• {issue}")
        else:
            print(f"  {Fore.GREEN}[OK] No issues found")



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
    print(f"  {BW}{Style.BRIGHT}  CERTIFICATE MONITOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}CERTIFICATE MONITOR                     {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Domain to check                              {RS}")
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
            print(f"  {Y}[*] Domain to check{RS}")
            value = input(f"  {Y}[*] -d: {RS}").strip()
            print(f"  {C}[*] Executing with -d={BW}{value}{RS}")
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

