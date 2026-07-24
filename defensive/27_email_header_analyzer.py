#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  EMAIL HEADER ANALYZER v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Email Security                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import re
import colorama
from colorama import Fore, Back, Style
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

class EmailAnalyzer:
    def __init__(self, email_file):
        self.email_file = email_file
        self.headers = {}
        self.alerts = []

    def parse_headers(self):
        print(f"{Fore.CYAN}  [*] Parsing email headers from: {Fore.WHITE}{self.email_file}\n")

        try:
            with open(self.email_file, 'r') as f:
                content = f.read()

            current_header = ''
            for line in content.split('\n'):
                if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                    key, value = line.split(':', 1)
                    self.headers[key.strip()] = value.strip()
                    current_header = key.strip()
                elif current_header and line.startswith((' ', '\t')):
                    self.headers[current_header] += ' ' + line.strip()

            print(f"  {Fore.GREEN}[+] Parsed {len(self.headers)} headers")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_spoofing(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SPOOFING CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        auth = self.headers.get('Authentication-Results', '')
        spf = self.headers.get('Received-SPF', auth)

        if 'spf=fail' in auth.lower() or 'spf=fail' in spf.lower():
            print(f"  {Fore.RED}[!] SPF FAIL - Possible spoofing")
            self.alerts.append('SPF Fail')
        elif 'spf=pass' in auth.lower() or 'spf=pass' in spf.lower():
            print(f"  {Fore.GREEN}[OK] SPF PASS")
        else:
            print(f"  {Fore.YELLOW}[-] SPF: Not clearly verified")
            self.alerts.append('SPF unclear')

        if 'dkim=fail' in auth.lower():
            print(f"  {Fore.RED}[!] DKIM FAIL")
            self.alerts.append('DKIM Fail')
        elif 'dkim=pass' in auth.lower():
            print(f"  {Fore.GREEN}[OK] DKIM PASS")

        if 'dmarc=fail' in auth.lower():
            print(f"  {Fore.RED}[!] DMARC FAIL")
            self.alerts.append('DMARC Fail')
        elif 'dmarc=pass' in auth.lower():
            print(f"  {Fore.GREEN}[OK] DMARC PASS")

    def check_traces(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  MESSAGE TRACE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        received = []
        for key, value in self.headers.items():
            if 'received' in key.lower():
                received.append(value)

        for i, r in enumerate(reversed(received), 1):
            print(f"  {Fore.WHITE}  Hop {i}: {r[:100]}")

    def check_suspicious_content(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUSPICIOUS CONTENT:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            with open(self.email_file, 'r') as f:
                content = f.read()

            # Check for urgency
            urgency_words = ['urgent', 'immediately', 'action required', 'verify', 'suspended']
            for word in urgency_words:
                if word in content.lower():
                    print(f"  {Fore.YELLOW}[-] Urgency keyword: '{word}'")

            # Check for shortened URLs
            urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
            for url in urls[:5]:
                if any(d in url for d in ['bit.ly', 'tinyurl', 't.co', 'goo.gl']):
                    print(f"  {Fore.RED}[!] Shortened URL: {url[:60]}")
                    self.alerts.append(f'Shortened URL: {url[:60]}')

        except:
            pass

    def analyze(self):
        print(f"{Fore.CYAN}  [*] Analyzing email: {Fore.WHITE}{self.email_file}\n")
        self.parse_headers()
        self.check_spoofing()
        self.check_traces()
        self.check_suspicious_content()
        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  EMAIL ANALYSIS COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        if self.alerts:
            print(f"\n  {Fore.RED}[!] Alerts: {len(self.alerts)}")
            for a in self.alerts:
                print(f"    {Fore.RED}• {a}")
            print(f"\n  {Fore.RED}[!!!] Email may be spoofed - verify sender!")
        else:
            print(f"\n  {Fore.GREEN}[OK] No spoofing indicators detected")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Email Header Analyzer')
    parser.add_argument('-f', '--file', required=True, help='Email file (.eml)')
    args = parser.parse_args()

    analyzer = EmailAnalyzer(args.file)
    analyzer.analyze()

if __name__ == "__main__":
    main()
