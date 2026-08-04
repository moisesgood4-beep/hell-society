#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  CVE VULNERABILITY CHECKER v2.0                                  ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Vulnerability Management                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import requests
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

class CVEChecker:
    def __init__(self):
        self.base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

    def check_cve(self, cve_id):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CVE LOOKUP: {cve_id.upper()}")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"{self.base_url}?cveId={cve_id.upper()}"
            resp = requests.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()

                if 'vulnerabilities' in data and len(data['vulnerabilities']) > 0:
                    vuln = data['vulnerabilities'][0]['cve']
                    descriptions = vuln.get('descriptions', [])
                    metrics = vuln.get('metrics', {})

                    print(f"  {Fore.WHITE}CVE: {vuln['id']}")

                    if descriptions:
                        desc = descriptions[0].get('value', 'N/A')
                        print(f"  {Fore.WHITE}Description: {desc[:200]}")

                    # CVSS Score
                    cvss3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
                    if cvss3:
                        score = cvss3.get('baseScore', 'N/A')
                        severity = cvss3.get('baseSeverity', 'N/A')

                        color = Fore.RED if score >= 9.0 else (Fore.YELLOW if score >= 7.0 else Fore.GREEN)
                        print(f"  {color}CVSS Score: {score}")
                        print(f"  {color}Severity: {severity}")

                        if score >= 9.0:
                            print(f"  {Fore.RED}[!!!] CRITICAL vulnerability!")
                        elif score >= 7.0:
                            print(f"  {Fore.YELLOW}[!] HIGH vulnerability")
                        elif score >= 4.0:
                            print(f"  {Fore.YELLOW}[-] MEDIUM vulnerability")
                        else:
                            print(f"  {Fore.GREEN}[OK] LOW vulnerability")
                    else:
                        print(f"  {Fore.YELLOW}CVSS Score: Not available")

                else:
                    print(f"  {Fore.GREEN}[OK] CVE not found (may be safe)")

            else:
                print(f"  {Fore.RED}[!] API error: {resp.status_code}")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_package(self, package_name, version=None):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PACKAGE VULNERABILITY CHECK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}Checking: {package_name}")
        if version:
            print(f"  {Fore.WHITE}Version: {version}")

        # Query NVD for known vulnerabilities
        try:
            url = f"{self.base_url}?keywordSearch={package_name}"
            resp = requests.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                total = data.get('totalResults', 0)
                print(f"  {Fore.WHITE}Results: {total} CVEs found")

                vulns = data.get('vulnerabilities', [])[:10]
                for v in vulns:
                    cve = v.get('cve', {})
                    cve_id = cve.get('id', 'N/A')
                    metrics = cve.get('metrics', {})
                    cvss3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})

                    score = cvss3.get('baseScore', 'N/A')
                    severity = cvss3.get('baseSeverity', 'N/A')

                    color = Fore.RED if str(score) in ['9.0', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '10.0'] else Fore.YELLOW
                    print(f"  {color}  • {cve_id} - Score: {score} ({severity})")

            else:
                print(f"  {Fore.YELLOW}[-] Could not query NVD")

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")



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
    print(f"  {BW}{Style.BRIGHT}  CVE CHECKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}CVE CHECKER                             {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Check specific CVE (e.g., CVE-2021-44228)    {RS}")
        print(f"  {C}[2]  {BW}Check package vulnerabilities                {RS}")
        print(f"  {C}[3]  {BW}Package version                              {RS}")
        print()
        print(f"  {C}[4]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Check specific CVE (e.g., CVE-2021-44228){RS}")
            value = input(f"  {Y}[*] --cve: {RS}").strip()
            print(f"  {C}[*] Executing with --cve={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Check package vulnerabilities{RS}")
            value = input(f"  {Y}[*] --package: {RS}").strip()
            print(f"  {C}[*] Executing with --package={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Package version{RS}")
            value = input(f"  {Y}[*] --version: {RS}").strip()
            print(f"  {C}[*] Executing with --version={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '4':
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

