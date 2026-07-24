#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  RANSOMWARE DETECTOR v2.0                                        ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Ransomware Protection                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import hashlib
import re

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗ ██╗   ██╗███████╗██╗      ██████╗ ██╗    ██╗███████╗    {Fore.RED}║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔════╝██║     ██╔═══██╗██║    ██║██╔════╝    {Fore.RED}║
║{Fore.CYAN}  ██████╔╝██║   ██║█████╗  ██║     ██║   ██║██║ █╗ ██║█████╗      {Fore.RED}║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔══╝  ██║     ██║   ██║██║███╗██║██╔══╝      {Fore.RED}║
║{Fore.CYAN}  ██║  ██║╚██████╔╝███████╗███████╗╚██████╔╝╚███╔███╔╝███████╗    {Fore.RED}║
║{Fore.CYAN}  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝    {Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Ransomware Detector v2.0                           {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

class RansomwareDetector:
    def __init__(self, watch_path):
        self.watch_path = watch_path
        self.alerts = []
        self.stats = {'scanned': 0, 'encrypted': 0, 'ransom_notes': 0}

        self.ransom_extensions = [
            '.locked', '.encrypted', '.crypto', '.crypt', '.ryuk',
            '.wannacry', '.zeus', '.locky', '.petya', '.notpetya',
            '.cerber', '.tesla', '.samsung', '.odin', '.ecc',
            '.aaa', '.ccc', '.vvv', '.xxx', '.ttt',
        ]

        self.ransom_patterns = [
            rb'your files.*encrypted',
            rb'pay.*bitcoin',
            rb'ransom.*note',
            rb'decrypt.*payment',
            rb'bitcoin.*address',
            rb'tor.*link',
            rb'HOW TO DECRYPT',
            rb'READ ME',
            rb'README',
            rb'!DECRYPT!',
            rb'!recover!',
        ]

    def scan(self):
        print(f"{Fore.CYAN}  [*] Scanning: {Fore.WHITE}{self.watch_path}")
        print(f"{Fore.CYAN}  [*] Looking for ransomware indicators...\n")

        for root, dirs, files in os.walk(self.watch_path):
            for filename in files:
                self.stats['scanned'] += 1
                filepath = os.path.join(root, filename)

                # Check extension
                _, ext = os.path.splitext(filename)
                if ext.lower() in self.ransom_extensions:
                    self.alerts.append({
                        'type': 'RANSOM_EXTENSION',
                        'file': filepath,
                        'severity': 'CRITICAL'
                    })
                    self.stats['encrypted'] += 1

                # Check ransom note filenames
                if any(note in filename.upper() for note in ['README', 'HOW TO', 'DECRYPT', 'RECOVER']):
                    self.alerts.append({
                        'type': 'RANSOM_NOTE',
                        'file': filepath,
                        'severity': 'CRITICAL'
                    })
                    self.stats['ransom_notes'] += 1

                # Check content patterns
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read(5000)
                        for pattern in self.ransom_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                self.alerts.append({
                                    'type': 'RANSOM_CONTENT',
                                    'file': filepath,
                                    'severity': 'CRITICAL',
                                    'detail': pattern.decode('utf-8', errors='ignore')
                                })
                                break
                except:
                    pass

                # Progress
                if self.stats['scanned'] % 100 == 0:
                    print(f"\r{Fore.CYAN}  [*] Scanned: {self.stats['scanned']} files | Alerts: {len(self.alerts)}", end="", flush=True)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  RANSOMWARE SCAN COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.WHITE}Files scanned: {self.stats['scanned']}")
        print(f"  {Fore.RED}Encrypted files: {self.stats['encrypted']}")
        print(f"  {Fore.RED}Ransom notes: {self.stats['ransom_notes']}")
        print(f"  {Fore.RED}Total alerts: {len(self.alerts)}")

        if self.alerts:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  ALERTS:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            for a in self.alerts[:20]:
                print(f"  {Fore.RED}[{a['type']}] {a['file']}")

        if len(self.alerts) > 0:
            print(f"\n  {Fore.RED}[!!!] RANSOMWARE INDICATORS DETECTED!")
            print(f"  {Fore.RED}[!!!] Isolate affected system immediately!")
            print(f"  {Fore.RED}[!!!] Do NOT pay ransom - contact authorities")
        else:
            print(f"\n  {Fore.GREEN}[OK] No ransomware indicators found")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Ransomware Detector')
    parser.add_argument('-p', '--path', required=True, help='Path to scan')
    args = parser.parse_args()

    detector = RansomwareDetector(args.path)
    detector.scan()

if __name__ == "__main__":
    main()
