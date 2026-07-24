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

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Email Spoofing Tester')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()

    tester = EmailSpoofer(args.domain)

    print(f"{Fore.CYAN}  [*] Analyzing domain: {Fore.WHITE}{args.domain}\n")
    tester.check_spf()
    tester.check_dmarc()
    tester.check_mx()
    tester.spoofing_test()
    tester.print_results()

if __name__ == "__main__":
    main()
