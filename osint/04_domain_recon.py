#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DOMAIN INTELLIGENCE v2.0                                        ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Domain Intelligence                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import subprocess
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import socket

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

class DomainRecon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}

    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return result.stdout.strip()
        except:
            return ''

    def check_dns(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DNS RECORDS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
        for rtype in record_types:
            result = self.run_cmd(f"dig +short {self.domain} {rtype}")
            if result:
                print(f"  {Fore.GREEN}[+] {rtype}: {result[:100]}")
                self.results.setdefault('dns', {})[rtype] = result.split('\n')
            else:
                print(f"  {Fore.YELLOW}[-] {rtype}: None")

    def check_whois(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WHOIS INFORMATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        result = self.run_cmd(f"whois {self.domain}")
        if result:
            lines = result.split('\n')
            for line in lines[:30]:
                if line.strip():
                    print(f"  {Fore.WHITE}  {line.strip()}")
            self.results['whois'] = True
        else:
            print(f"  {Fore.YELLOW}[-] Whois not available")
            self.results['whois'] = False

    def check_technology(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TECHNOLOGY STACK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            import requests
            resp = requests.get(f"https://{self.domain}", timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 HellSociety/2.0'
            })

            print(f"  {Fore.WHITE}Status: {resp.status_code}")
            print(f"  {Fore.WHITE}Server: {resp.headers.get('Server', 'Unknown')}")
            print(f"  {Fore.WHITE}Powered-By: {resp.headers.get('X-Powered-By', 'Unknown')}")

            # Detect technologies
            content = resp.text
            techs = []

            if 'wordpress' in content.lower() or '/wp-content/' in content:
                techs.append('WordPress')
                print(f"  {Fore.GREEN}[+] WordPress detected")

            if 'jquery' in content.lower():
                techs.append('jQuery')
                print(f"  {Fore.GREEN}[+] jQuery detected")

            if 'react' in content.lower() or 'react-dom' in content.lower():
                techs.append('React')
                print(f"  {Fore.GREEN}[+] React detected")

            if 'angular' in content.lower():
                techs.append('Angular')
                print(f"  {Fore.GREEN}[+] Angular detected")

            if 'laravel' in content.lower() or 'xsrf-token' in resp.headers.get('Set-Cookie', '').lower():
                techs.append('Laravel')
                print(f"  {Fore.GREEN}[+] Laravel detected")

            if 'php' in resp.headers.get('X-Powered-By', '').lower():
                techs.append('PHP')
                print(f"  {Fore.GREEN}[+] PHP detected")

            if 'asp.net' in resp.headers.get('X-Powered-By', '').lower():
                techs.append('ASP.NET')
                print(f"  {Fore.GREEN}[+] ASP.NET detected")

            self.results['technologies'] = techs

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_subdomains(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUBDOMAIN CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        common_subs = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
                      'staging', 'blog', 'shop', 'cdn', 'static', 'app',
                      'dashboard', 'portal', 'panel', 'db', 'sql', 'vpn']

        found = []
        for sub in common_subs:
            full = f"{sub}.{self.domain}"
            try:
                ip = socket.gethostbyname(full)
                print(f"  {Fore.GREEN}[+] {full} -> {ip}")
                found.append({'subdomain': full, 'ip': ip})
            except:
                pass

        self.results['subdomains'] = found
        print(f"\n  {Fore.WHITE}Subdomains found: {len(found)}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.domain}")
        print(f"{Fore.CYAN}  [*] Starting domain intelligence...\n")

        self.check_dns()
        self.check_whois()
        self.check_technology()
        self.check_subdomains()

        results_file = f'/tmp/domain_recon_{self.domain}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

        print(f"\n{Fore.GREEN}{Back.BLACK}  DOMAIN INTELLIGENCE COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Domain Recon')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()

    recon = DomainRecon(args.domain)
    recon.run()
