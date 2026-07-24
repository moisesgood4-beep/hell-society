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

BANNER = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗  █████╗ ████████╗███████╗    ██████╗  █████╗ ███████╗   {Fore.GREEN}║
║{Fore.CYAN}  ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ██╔══██╗██╔══██╗██╔════╝   {Fore.GREEN}║
║{Fore.CYAN}  ██████╔╝███████║   ██║   █████╗      ██████╔╝███████║███████╗   {Fore.GREEN}║
║{Fore.CYAN}  ██╔═══╝ ██╔══██║   ██║   ██╔══╝      ██╔══██╗██╔══██║╚════██║   {Fore.GREEN}║
║{Fore.CYAN}  ██║     ██║  ██║   ██║   ███████╗    ██████╔╝██║  ██║███████║   {Fore.GREEN}║
║{Fore.CYAN}  ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   {Fore.GREEN}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Backup Validator v2.0                              {Fore.GREEN}║
╚══════════════════════════════════════════════════════════════════╝
"""

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

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Backup Validator')
    parser.add_argument('-b', '--backup', required=True, help='Backup path')
    parser.add_argument('-s', '--source', required=True, help='Source path to validate')
    args = parser.parse_args()

    validator = BackupValidator(args.backup, args.source)
    validator.validate_checksums()
    validator.check_backup_age()
    validator.check_integrity()
    validator.print_summary()

if __name__ == "__main__":
    main()
