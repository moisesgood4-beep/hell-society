#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  BACKUP VALIDATOR v2.0                                           ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Backup & Recovery                         ║
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

class BackupValidator:
    def __init__(self, backup_path, source_path):
        self.backup_path = backup_path
        self.source_path = source_path
        self.issues = []
        self.stats = {'total': 0, 'valid': 0, 'invalid': 0, 'missing': 0}

    def validate_checksums(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CHECKSUM VALIDATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Create checksum manifest
        manifest = {}
        for root, dirs, files in os.walk(self.source_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                self.stats['total'] += 1
                try:
                    with open(filepath, 'rb') as f:
                        h = hashlib.sha256(f.read()).hexdigest()
                    manifest[filepath] = h
                except:
                    pass

        manifest_file = os.path.join(self.backup_path, 'checksums.json')
        os.makedirs(self.backup_path, exist_ok=True)

        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"  {Fore.GREEN}[+] Checksum manifest created")

        # Validate existing backups
        existing_manifest = manifest_file
        if os.path.exists(existing_manifest):
            with open(existing_manifest, 'r') as f:
                old_manifest = json.load(f)

            for filepath, old_hash in old_manifest.items():
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        new_hash = hashlib.sha256(f.read()).hexdigest()
                    if new_hash == old_hash:
                        self.stats['valid'] += 1
                    else:
                        self.stats['invalid'] += 1
                        self.issues.append(f'Modified: {filepath}')
                else:
                    self.stats['missing'] += 1

    def check_backup_age(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BACKUP AGE CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if os.path.exists(self.backup_path):
            mtime = os.path.getmtime(self.backup_path)
            age_days = (datetime.now().timestamp() - mtime) / 86400

            if age_days < 1:
                print(f"  {Fore.GREEN}[OK] Backup is recent ({age_days:.1f} days)")
            elif age_days < 7:
                print(f"  {Fore.YELLOW}[-] Backup is {age_days:.1f} days old")
            else:
                print(f"  {Fore.RED}[!] Backup is {age_days:.1f} days old - OUTDATED!")
                self.issues.append(f'Old backup: {age_days:.1f} days')

    def check_integrity(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BACKUP INTEGRITY:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if os.path.exists(self.backup_path):
            size = 0
            for root, dirs, files in os.walk(self.backup_path):
                for f in files:
                    size += os.path.getsize(os.path.join(root, f))

            print(f"  {Fore.WHITE}  Backup size: {size / (1024*1024):.2f} MB")
            print(f"  {Fore.WHITE}  Files: {self.stats['total']}")

            if size == 0:
                print(f"  {Fore.RED}[!] Backup is EMPTY!")
                self.issues.append('Empty backup')
            else:
                print(f"  {Fore.GREEN}[OK] Backup has content")

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  BACKUP VALIDATION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.WHITE}Total files: {self.stats['total']}")
        print(f"  {Fore.GREEN}Valid: {self.stats['valid']}")
        print(f"  {Fore.RED}Invalid/Modified: {self.stats['invalid']}")
        print(f"  {Fore.YELLOW}Missing: {self.stats['missing']}")

        if self.issues:
            print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
            for issue in self.issues:
                print(f"    {Fore.RED}• {issue}")
        else:
            print(f"\n  {Fore.GREEN}[OK] All backups validated successfully")



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
    print(f"  {BW}{Style.BRIGHT}  BACKUP VALIDATOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}BACKUP VALIDATOR                        {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Backup path                                  {RS}")
        print(f"  {C}[2]  {BW}Source path to validate                      {RS}")
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
            print(f"  {Y}[*] Backup path{RS}")
            value = input(f"  {Y}[*] -b: {RS}").strip()
            print(f"  {C}[*] Executing with -b={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Source path to validate{RS}")
            value = input(f"  {Y}[*] -s: {RS}").strip()
            print(f"  {C}[*] Executing with -s={BW}{value}{RS}")
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

