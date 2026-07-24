#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  THREAT INTELLIGENCE FEED v2.0                                   ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Threat Intelligence                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
from datetime import datetime

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ████████╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗     ███████╗{Fore.RED}║
║{Fore.CYAN}  ╚══██╔══╝██╔═══██╗██╔══██╗██║   ██║██╔══██╗██║     ██║     ██╔════╝{Fore.RED}║
║{Fore.CYAN}     ██║   ██║   ██║██████╔╝██║   ██║███████║██║     ██║     ███████╗{Fore.RED}║
║{Fore.CYAN}     ██║   ██║   ██║██╔══██╗██║   ██║██╔══██║██║     ██║     ╚════██║{Fore.RED}║
║{Fore.CYAN}     ██║   ╚██████╔╝██║  ██║╚██████╔╝██║  ██║███████╗███████╗███████║{Fore.RED}║
║{Fore.CYAN}     ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝{Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Threat Intelligence Feed v2.0                      {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

class ThreatIntel:
    def __init__(self):
        self.threats = []

    def check_abuseipdb(self, ip):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ABUSEIPDB CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"https://api.abuseipdb.com/api/v2/check"
            headers = {'Key': '', 'Accept': 'application/json'}
            params = {'ipAddress': ip, 'maxAgeInDays': 90}
            resp = requests.get(url, headers=headers, params=params, timeout=10)

            if resp.status_code == 200:
                data = resp.json().get('data', {})
                print(f"  {Fore.WHITE}IP: {data.get('ipAddress', 'N/A')}")
                print(f"  {Fore.WHITE}Abuse Score: {data.get('abuseConfidenceScore', 'N/A')}")
                print(f"  {Fore.WHITE}Country: {data.get('countryCode', 'N/A')}")
                print(f"  {Fore.WHITE}Reports: {data.get('totalReports', 0)}")

                score = data.get('abuseConfidenceScore', 0)
                if score >= 80:
                    print(f"  {Fore.RED}[!!!] HIGHLY MALICIOUS!")
                elif score >= 40:
                    print(f"  {Fore.RED}[!] Malicious")
                elif score > 0:
                    print(f"  {Fore.YELLOW}[-] Some reports")
                else:
                    print(f"  {Fore.GREEN}[OK] Clean IP")
            else:
                print(f"  {Fore.YELLOW}[-] API error: {resp.status_code}")
                print(f"  {Fore.YELLOW}[-] Set your AbuseIPDB API key for full results")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_virustotal(self, ip_or_hash):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  VIRUSTOTAL CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            # Determine if IP or hash
            if all(c in '0123456789abcdefABCDEF' for c in ip_or_hash) and len(ip_or_hash) in [32, 64]:
                url = f"https://www.virustotal.com/api/v3/files/{ip_or_hash}"
                itype = 'file hash'
            else:
                url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_or_hash}"
                itype = 'IP address'

            headers = {'x-apikey': ''}
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 200:
                data = resp.json().get('data', {})
                attrs = data.get('attributes', {})
                print(f"  {Fore.WHITE}Type: {itype}")
                print(f"  {Fore.WHITE}Target: {ip_or_hash}")
                print(f"  {Fore.YELLOW}[-] Set VirusTotal API key for detailed results")
            elif resp.status_code == 404:
                print(f"  {Fore.GREEN}[OK] Not found in VirusTotal")
            else:
                print(f"  {Fore.YELLOW}[-] Set your VirusTotal API key")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_otx(self, indicator):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ALIENVAULT OTX CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"https://otx.alienvault.com/api/v1/indicators/general/{indicator}"
            resp = requests.get(url, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                print(f"  {Fore.WHITE}Indicator: {indicator}")
                print(f"  {Fore.WHITE}In pulses: {data.get('in_pulse', False)}")
                print(f"  {Fore.WHITE}Pulse count: {data.get('pulse_info', {}).get('count', 0)}")

                pulses = data.get('pulse_info', {}).get('pulses', [])
                for pulse in pulses[:5]:
                    print(f"    {Fore.YELLOW}• {pulse.get('name', 'N/A')}")
            else:
                print(f"  {Fore.YELLOW}[-] Not found or API error")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check(self, indicator, itype='ip'):
        print(f"{Fore.CYAN}  [*] Checking threat intel for: {Fore.WHITE}{indicator}")
        print(f"{Fore.CYAN}  [*] Type: {itype}\n")

        if itype == 'ip':
            self.check_abuseipdb(indicator)
            self.check_virustotal(indicator)
            self.check_otx(indicator)
        elif itype == 'hash':
            self.check_virustotal(indicator)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  THREAT INTELLIGENCE COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.YELLOW}[i] Set API keys for full results:")
        print(f"  {Fore.CYAN}  - AbuseIPDB: https://www.abuseipdb.com/api")
        print(f"  {Fore.CYAN}  - VirusTotal: https://www.virustotal.com/gui/my-apikey")
        print(f"  {Fore.CYAN}  - AlienVault OTX: https://otx.alienvault.com/api")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Threat Intelligence')
    parser.add_argument('-i', '--indicator', required=True, help='IP, hash, or domain')
    parser.add_argument('-t', '--type', choices=['ip', 'hash', 'domain'], default='ip', help='Indicator type')
    args = parser.parse_args()

    intel = ThreatIntel()
    intel.check(args.indicator, args.type)

if __name__ == "__main__":
    main()
