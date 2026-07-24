#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  ZERO-DAY INDICATOR DETECTOR v2.0                                ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Threat Detection                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
import re
import subprocess
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

class ZeroDayDetector:
    def __init__(self, target_path):
        self.target_path = target_path
        self.indicators = []
        self.stats = {'files_scanned': 0, 'suspicious': 0}

        self.suspicious_patterns = [
            # Obfuscation techniques
            rb'eval\s*\(\s*base64_decode',
            rb'eval\s*\(\s*gzinflate',
            rb'eval\s*\(\s*str_rot13',
            rb'base64_decode\s*\(\s*gzinflate',
            rb'eval\s*\(\s*["\']\s*[A-Za-z0-9+/=]{50,}',
            
            # Web shells
            rb'c99\s*shell',
            rb'r57\s*shell',
            rb'wso\s*shell',
            rb'backdoor\s*php',
            rb'p0wny\s*shell',
            
            # Suspicious functions
            rb'system\s*\(\s*\$_',
            rb'passthru\s*\(\s*\$_',
            rb'shell_exec\s*\(\s*\$_',
            rb'exec\s*\(\s*\$_POST',
            rb'popen\s*\(\s*\$_',
            rb'proc_open\s*\(\s*\$_',
            
            # Data exfiltration
            rb'file_get_contents\s*\(\s*["\']https?://',
            rb'curl_exec\s*\(\s*\$.*POST',
            rb'fopen\s*\(\s*["\']php://filter',
            rb'base64_encode\s*\(.*file_get_contents',
            
            # Persistence
            rb'file_put_contents\s*\(\s*["\'].*\.php',
            rb'chmod\s*\(\s*.*0777',
            rb'system\s*\(\s*["\']wget',
            rb'system\s*\(\s*["\']curl.*\|.*bash',
        ]

    def scan(self):
        print(f"{Fore.CYAN}  [*] Scanning: {Fore.WHITE}{self.target_path}")
        print(f"{Fore.CYAN}  [*] Looking for zero-day indicators...\n")

        for root, dirs, files in os.walk(self.target_path):
            for filename in files:
                self.stats['files_scanned'] += 1
                filepath = os.path.join(root, filename)

                # Skip binary files
                if any(filename.endswith(ext) for ext in ['.png', '.jpg', '.gif', '.zip', '.gz', '.tar']):
                    continue

                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()

                    for pattern in self.suspicious_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            self.indicators.append({
                                'file': filepath,
                                'pattern': pattern.decode('utf-8', errors='ignore'),
                                'count': len(matches)
                            })
                            self.stats['suspicious'] += 1

                except:
                    pass

                if self.stats['files_scanned'] % 50 == 0:
                    print(f"\r{Fore.CYAN}  [*] Files: {self.stats['files_scanned']} | Alerts: {len(self.indicators)}", end="", flush=True)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  ZERO-DAY SCAN COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.WHITE}Files scanned: {self.stats['files_scanned']}")
        print(f"  {Fore.RED}Suspicious indicators: {len(self.indicators)}")

        if self.indicators:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  INDICATORS FOUND:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            for ind in self.indicators[:15]:
                print(f"  {Fore.RED}[!] {ind['file']}")
                print(f"      Pattern: {ind['pattern']}")
                print(f"      Matches: {ind['count']}")
            print(f"\n  {Fore.RED}[!!!] POTENTIAL ZERO-DAY ACTIVITY DETECTED!")
            print(f"  {Fore.RED}[!!!] Investigate immediately!")
        else:
            print(f"\n  {Fore.GREEN}[OK] No zero-day indicators found")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Zero-Day Detector')
    parser.add_argument('-p', '--path', required=True, help='Path to scan')
    args = parser.parse_args()

    detector = ZeroDayDetector(args.path)
    detector.scan()

if __name__ == "__main__":
    main()
