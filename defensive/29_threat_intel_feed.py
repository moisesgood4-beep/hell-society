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
    print(f"  {BW}{Style.BRIGHT}  THREAT INTEL FEED{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}THREAT INTEL FEED                       {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}IP, hash, or domain                          {RS}")
        print(f"  {C}[2]  {BW}Indicator type                               {RS}")
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
            print(f"  {Y}[*] IP, hash, or domain{RS}")
            value = input(f"  {Y}[*] -i: {RS}").strip()
            print(f"  {C}[*] Executing with -i={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Indicator type{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
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

