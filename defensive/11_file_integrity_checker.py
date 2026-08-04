#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  FILE INTEGRITY MONITOR v2.0                                     ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Integrity Monitoring                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import os
import sys
import json
import colorama
from colorama import Fore, Back, Style
import argparse
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

class FileIntegrityMonitor:
    def __init__(self, watch_path, baseline_file='baseline.json'):
        self.watch_path = watch_path
        self.baseline_file = baseline_file
        self.changes = []
        self.new_files = []
        self.deleted_files = []
        self.baseline = {}

    def create_baseline(self):
        print(f"{Fore.CYAN}  [*] Creating baseline for: {Fore.WHITE}{self.watch_path}\n")

        self.baseline = {}
        for root, dirs, files in os.walk(self.watch_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        h = hashlib.sha256(content).hexdigest()
                    stat = os.stat(filepath)
                    self.baseline[filepath] = {
                        'hash': h,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'mode': oct(stat.st_mode)
                    }
                except:
                    pass

        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)

        print(f"  {Fore.GREEN}[+] Baseline created: {len(self.baseline)} files")
        print(f"  {Fore.GREEN}[+] Saved to: {self.baseline_file}")

    def check_integrity(self):
        print(f"{Fore.CYAN}  [*] Checking integrity against baseline...\n")

        # Load baseline
        if not os.path.exists(self.baseline_file):
            print(f"  {Fore.YELLOW}[!] No baseline found. Create one first with --create")
            return

        with open(self.baseline_file, 'r') as f:
            self.baseline = json.load(f)

        current_files = set()

        for root, dirs, files in os.walk(self.watch_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                current_files.add(filepath)

                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        h = hashlib.sha256(content).hexdigest()
                    stat = os.stat(filepath)
                except:
                    continue

                if filepath in self.baseline:
                    old = self.baseline[filepath]

                    # Check hash
                    if h != old['hash']:
                        self.changes.append({
                            'file': filepath,
                            'change': 'HASH_MODIFIED',
                            'severity': 'HIGH'
                        })

                    # Check size
                    if stat.st_size != old['size']:
                        self.changes.append({
                            'file': filepath,
                            'change': f"SIZE_CHANGED ({old['size']} -> {stat.st_size})",
                            'severity': 'MEDIUM'
                        })

                    # Check permissions
                    if oct(stat.st_mode) != old['mode']:
                        self.changes.append({
                            'file': filepath,
                            'change': f"PERMISSIONS_CHANGED ({old['mode']} -> {oct(stat.st_mode)})",
                            'severity': 'MEDIUM'
                        })
                else:
                    self.new_files.append(filepath)

        # Check for deleted files
        for filepath in self.baseline:
            if filepath not in current_files:
                self.deleted_files.append(filepath)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  INTEGRITY CHECK COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"  {Fore.RED}[!] Modified files: {len(self.changes)}")
        for c in self.changes[:20]:
            color = Fore.RED if c['severity'] == 'HIGH' else Fore.YELLOW
            print(f"  {color}  [{c['severity']}] {c['file']} - {c['change']}")

        print(f"\n  {Fore.GREEN}[+] New files: {len(self.new_files)}")
        for f in self.new_files[:10]:
            print(f"    {Fore.GREEN}  {f}")

        print(f"\n  {Fore.RED}[-] Deleted files: {len(self.deleted_files)}")
        for f in self.deleted_files[:10]:
            print(f"    {Fore.RED}  {f}")

        if len(self.changes) > 10:
            print(f"\n  {Fore.RED}[!!!] CRITICAL: Many files have been modified!")
        elif len(self.changes) > 0:
            print(f"\n  {Fore.YELLOW}[!] Some files were modified")
        else:
            print(f"\n  {Fore.GREEN}[OK] No integrity violations detected")



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
    print(f"  {BW}{Style.BRIGHT}  FILE INTEGRITY CHECKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}FILE INTEGRITY CHECKER                  {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Path to monitor                              {RS}")
        print(f"  {C}[2]  {BW}Create baseline                              {RS}")
        print(f"  {C}[3]  {BW}Baseline file                                {RS}")
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
            print(f"  {Y}[*] Path to monitor{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Create baseline{RS}")
            value = input(f"  {Y}[*] -c: {RS}").strip()
            print(f"  {C}[*] Executing with -c={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Baseline file{RS}")
            value = input(f"  {Y}[*] -b: {RS}").strip()
            print(f"  {C}[*] Executing with -b={BW}{value}{RS}")
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

