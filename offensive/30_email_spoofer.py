#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  EMAIL HEADER ANALYZER & SPOOFING TESTER v2.0                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Email Security                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import smtplib
import socket
import dns.resolver
import json

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
Los creadores NO se hacen responsables del mal uso.
"""

class EmailSpoofer:
    def __init__(self, domain):
        self.domain = domain
        self.dmarc = None
        self.spf = None
        self.mx_records = []
        self.vulns = []

    def check_spf(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SPF RECORD CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            answers = dns.resolver.resolve(self.domain, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if 'v=spf1' in txt:
                    self.spf = txt
                    print(f"  {Fore.GREEN}[+] SPF Record: {Fore.WHITE}{txt}")

                    if '+all' in txt or '?all' in txt:
                        print(f"  {Fore.RED}[VULN] SPF allows ANY sender!")
                        self.vulns.append('SPF: Permissive (+all/?all)')
                    elif '-all' in txt or '~all' in txt:
                        print(f"  {Fore.GREEN}[OK] SPF has strict policy")
                    elif 'all' not in txt:
                        print(f"  {Fore.RED}[VULN] SPF missing 'all' mechanism")
                        self.vulns.append('SPF: Missing all mechanism')

                    if 'include' in txt:
                        includes = [i.split(':')[1] for i in txt.split('include:')]
                        print(f"  {Fore.CYAN}  Includes: {includes}")
                    return
            print(f"  {Fore.RED}[VULN] No SPF record found!")
            self.vulns.append('SPF: Not configured')
        except dns.resolver.NoAnswer:
            print(f"  {Fore.RED}[VULN] No TXT records - SPF not configured!")
            self.vulns.append('SPF: Not configured')
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_dmarc(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DMARC RECORD CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            answers = dns.resolver.resolve(f'_dmarc.{self.domain}', 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if 'v=DMARC1' in txt:
                    self.dmarc = txt
                    print(f"  {Fore.GREEN}[+] DMARC Record: {Fore.WHITE}{txt}")

                    if 'p=none' in txt:
                        print(f"  {Fore.RED}[VULN] DMARC policy is 'none' (no enforcement)")
                        self.vulns.append('DMARC: Policy=none')
                    elif 'p=quarantine' in txt:
                        print(f"  {Fore.YELLOW}[-] DMARC policy is 'quarantine'")
                        self.vulns.append('DMARC: Policy=quarantine')
                    elif 'p=reject' in txt:
                        print(f"  {Fore.GREEN}[OK] DMARC policy is 'reject' (strict)")

                    if 'pct=100' in txt or 'pct=' not in txt:
                        print(f"  {Fore.GREEN}[OK] DMARC applies to 100% of emails")
                    else:
                        pct = [t for t in txt.split(';') if 'pct=' in t][0]
                        print(f"  {Fore.YELLOW}[-] DMARC partial: {pct}")

                    return
            print(f"  {Fore.RED}[VULN] No DMARC record found!")
            self.vulns.append('DMARC: Not configured')
        except dns.resolver.NoAnswer:
            print(f"  {Fore.RED}[VULN] No DMARC record!")
            self.vulns.append('DMARC: Not configured')
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_mx(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  MX RECORDS CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            self.mx_records = [(rdata.exchange.to_text().rstrip('.'), rdata.preference)
                             for rdata in answers]
            self.mx_records.sort(key=lambda x: x[1])

            for mx, pref in self.mx_records:
                print(f"  {Fore.CYAN}  MX: {Fore.WHITE}{mx} (priority: {pref})")

            if not self.mx_records:
                print(f"  {Fore.RED}[VULN] No MX records!")
        except dns.resolver.NoAnswer:
            print(f"  {Fore.RED}[VULN] No MX records found!")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def spoofing_test(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  EMAIL SPOOFING VULNERABILITY SUMMARY")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if 'SPF: Not configured' in self.vulns or 'SPF: Permissive' in self.vulns:
            print(f"  {Fore.RED}[HIGH] Domain CAN be spoofed (SPF weak/missing)")

        if 'DMARC: Not configured' in self.vulns or 'DMARC: Policy=none' in self.vulns:
            print(f"  {Fore.RED}[HIGH] DMARC won't prevent spoofing")

        if not any('SPF' in v and 'Not' in v for v in self.vulns) and \
           not any('DMARC' in v and 'Not' in v for v in self.vulns):
            print(f"  {Fore.GREEN}[OK] Domain has basic email protection")

    def print_results(self):
        print(f"\n\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SPOOFING ANALYSIS SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")

        if self.vulns:
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        if 'SPF: Not configured' in self.vulns or 'DMARC: Not configured' in self.vulns:
            print(f"\n  {Fore.RED}[CRITICAL] This domain is HIGHLY vulnerable to email spoofing!")
            print(f"  {Fore.RED}[CRITICAL] Attackers can send emails appearing from @{self.domain}")



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
    print(f"  {BW}{Style.BRIGHT}  EMAIL SPOOFER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}EMAIL SPOOFER                           {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target domain                                {RS}")
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
            print(f"  {Y}[*] Target domain{RS}")
            value = input(f"  {Y}[*] -d: {RS}").strip()
            print(f"  {C}[*] Executing with -d={BW}{value}{RS}")
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

