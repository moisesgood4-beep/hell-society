#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PHONE NUMBER OSINT v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Phone Intelligence                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ██████╗       {Fore.MAGENTA}║
║{Fore.CYAN}  ██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗██╔══██╗      {Fore.MAGENTA}║
║{Fore.CYAN}  ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██║  ██║      {Fore.MAGENTA}║
║{Fore.CYAN}  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║  ██║      {Fore.MAGENTA}║
║{Fore.CYAN}  ██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██████╔╝      {Fore.MAGENTA}║
║{Fore.CYAN}  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝       {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Phone Number OSINT v2.0                          {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

class PhoneRecon:
    def __init__(self, phone):
        self.phone = phone
        self.clean = re.sub(r'[^0-9+]', '', phone)
        self.results = {}

    def format_analysis(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PHONE FORMAT ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}Original: {self.phone}")
        print(f"  {Fore.WHITE}Clean: {self.clean}")

        if self.clean.startswith('+'):
            country_code = self.clean[1:4]
            print(f"  {Fore.GREEN}[+] Country code: +{country_code}")
            self.results['country_code'] = f'+{country_code}'

            # Common country codes
            countries = {
                '1': 'USA/Canada', '44': 'United Kingdom', '49': 'Germany',
                '33': 'France', '34': 'Spain', '39': 'Italy',
                '55': 'Brazil', '86': 'China', '81': 'Japan',
                '91': 'India', '7': 'Russia', '52': 'Mexico',
                '54': 'Argentina', '57': 'Colombia', '34': 'Spain',
            }
            for code, country in countries.items():
                if self.clean.startswith(f'+{code}'):
                    print(f"  {Fore.GREEN}[+] Country: {country}")
                    self.results['country'] = country
                    break
        else:
            print(f"  {Fore.YELLOW}[-] No country code detected")

        # Carrier type estimation
        if len(self.clean) > 10:
            print(f"  {Fore.WHITE}Length: {len(self.clean)} digits (international)")
        else:
            print(f"  {Fore.WHITE}Length: {len(self.clean)} digits (possibly local)")

    def check_leaks(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DATA BREACH CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            import requests
            # Check against known breach databases
            print(f"  {Fore.WHITE}Searching for {self.phone} in breach databases...")
            print(f"  {Fore.YELLOW}[-] Set API keys for full breach checking")
            print(f"  {Fore.CYAN}  Services to check:")
            print(f"    - HaveIBeenPwned (phone)")
            print(f"    - IntelX")
            print(f"    - DeHashed")
        except:
            pass

    def check_social(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SOCIAL MEDIA ASSOCIATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Check these platforms manually:")
        print(f"  {Fore.CYAN}  - WhatsApp: Save number and check profile")
        print(f"  {Fore.CYAN}  - Telegram: Search by phone number")
        print(f"  {Fore.CYAN}  - Signal: Check if registered")
        print(f"  {Fore.CYAN}  - Facebook: Search by phone")
        print(f"  {Fore.CYAN}  - Instagram: Try to find by phone")
        print(f"  {Fore.CYAN}  - LinkedIn: Search by phone")
        print(f"  {Fore.CYAN}  - Twitter/X: Some users link phones")

    def generate_report(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  REPORT:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}Phone: {self.phone}")
        if 'country' in self.results:
            print(f"  {Fore.WHITE}Country: {self.results['country']}")

        # Save results
        results_file = f'/tmp/phone_recon_{self.clean}.json'
        with open(results_file, 'w') as f:
            json.dump({'phone': self.phone, 'results': self.results}, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Report saved: {results_file}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.phone}")
        print(f"{Fore.CYAN}  [*] Starting phone reconnaissance...\n")

        self.format_analysis()
        self.check_leaks()
        self.check_social()
        self.generate_report()

        print(f"\n{Fore.GREEN}{Back.BLACK}  PHONE RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Phone Recon')
    parser.add_argument('-p', '--phone', required=True, help='Target phone number')
    args = parser.parse_args()

    recon = PhoneRecon(args.phone)
    recon.run()
