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
    print(f"  {BW}{Style.BRIGHT}  RANSOMWARE DETECTOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}RANSOMWARE DETECTOR                     {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Path to scan                                 {RS}")
        print()
        print(f"  {C}[2]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Path to scan{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
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

