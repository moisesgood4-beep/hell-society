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

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}   ██████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗     {Fore.RED}║
║{Fore.CYAN}  ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║     {Fore.RED}║
║{Fore.CYAN}  ██║      ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║     {Fore.RED}║
║{Fore.CYAN}  ██║       ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║     {Fore.RED}║
║{Fore.CYAN}  ╚██████╗   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║     {Fore.RED}║
║{Fore.CYAN}   ╚═════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝     {Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - CVE Vulnerability Checker v2.0                     {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

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

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society CVE Checker')
    parser.add_argument('--cve', help='Check specific CVE (e.g., CVE-2021-44228)')
    parser.add_argument('--package', help='Check package vulnerabilities')
    parser.add_argument('--version', help='Package version')
    args = parser.parse_args()

    checker = CVEChecker()

    if args.cve:
        checker.check_cve(args.cve)
    elif args.package:
        checker.check_package(args.package, args.version)
    else:
        print(f"  {Fore.YELLOW}Usage:")
        print(f"  {Fore.CYAN}  --cve CVE-2021-44228")
        print(f"  {Fore.CYAN}  --package openssl --version 1.1.1")

if __name__ == "__main__":
    main()
