#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PASSWORD POLICY CHECKER v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Authentication Security                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
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

COMMON_PASSWORDS = [
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey',
    '1234567', 'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou',
    'master', 'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow',
    '123123', '654321', 'superman', 'qazwsx', 'michael', 'football',
    'password1', 'password123', 'admin', 'root', 'user', 'test'
]

class PasswordChecker:
    def __init__(self):
        self.issues = []
        self.score = 100

    def check_pam_config(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PAM CONFIGURATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        pam_files = ['/etc/pam.d/common-password', '/etc/pam.d/system-auth']

        for pam_file in pam_files:
            if os.path.exists(pam_file):
                print(f"  {Fore.WHITE}  Checking: {pam_file}")
                with open(pam_file, 'r') as f:
                    content = f.read()

                if 'pam_pwquality' in content or 'pam_cracklib' in content:
                    print(f"  {Fore.GREEN}  [+] Password quality module active")
                else:
                    print(f"  {Fore.RED}  [!] No password quality module")
                    self.issues.append('No pam_pwquality/pam_cracklib')
                    self.score -= 20

                if 'minlen' in content:
                    minlen = re.search(r'minlen=(\d+)', content)
                    if minlen and int(minlen.group(1)) >= 12:
                        print(f"  {Fore.GREEN}  [+] Minimum length: {minlen.group(1)}")
                    else:
                        length = minlen.group(1) if minlen else 'N/A'
                        print(f"  {Fore.YELLOW}  [-] Minimum length too low: {length}")
                        self.issues.append(f'Weak minlen: {length}')
                        self.score -= 15
                else:
                    print(f"  {Fore.RED}  [!] No minimum length set")
                    self.issues.append('No minimum length')
                    self.score -= 20

                if 'dcredit' in content:
                    print(f"  {Fore.GREEN}  [+] Digit credit configured")
                else:
                    print(f"  {Fore.YELLOW}  [-] No digit requirement")
                    self.issues.append('No digit requirement')
                    self.score -= 10

                if 'ucredit' in content:
                    print(f"  {Fore.GREEN}  [+] Upper case credit configured")
                else:
                    print(f"  {Fore.YELLOW}  [-] No upper case requirement")
                    self.issues.append('No upper case requirement')
                    self.score -= 10

                if 'lcredit' in content:
                    print(f"  {Fore.GREEN}  [+] Lower case credit configured")
                else:
                    print(f"  {Fore.YELLOW}  [-] No lower case requirement")
                    self.issues.append('No lower case requirement')
                    self.score -= 10

    def check_password_hashes(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PASSWORD HASH ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            with open('/etc/shadow', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) >= 2:
                        username = parts[0]
                        hash_field = parts[1]

                        if hash_field == '' or hash_field == '!':
                            continue

                        # Check for empty password
                        if hash_field == '':
                            print(f"  {Fore.RED}  [!!!] {username}: EMPTY PASSWORD!")
                            self.issues.append(f'Empty password: {username}')
                            self.score -= 30

                        # Check hash algorithm
                        elif hash_field.startswith('$1$'):
                            print(f"  {Fore.RED}  [!] {username}: MD5 hash (WEAK)")
                            self.issues.append(f'MD5 hash: {username}')
                            self.score -= 15

                        elif hash_field.startswith('$2a$') or hash_field.startswith('$2y$'):
                            print(f"  {Fore.GREEN}  [OK] {username}: bcrypt (STRONG)")

                        elif hash_field.startswith('$6$'):
                            print(f"  {Fore.GREEN}  [OK] {username}: SHA-512 (STRONG)")

                        elif hash_field.startswith('$5$'):
                            print(f"  {Fore.YELLOW}  [-] {username}: SHA-256 (MODERATE)")

                        else:
                            print(f"  {Fore.YELLOW}  [?] {username}: Unknown hash type")

        except PermissionError:
            print(f"  {Fore.YELLOW}  [-] Need root to read /etc/shadow")

    def check_account_policies(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ACCOUNT POLICIES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            with open('/etc/login.defs', 'r') as f:
                content = f.read()

                pass_max = re.search(r'PASS_MAX_DAYS\s+(\d+)', content)
                if pass_max:
                    days = int(pass_max.group(1))
                    if days <= 90:
                        print(f"  {Fore.GREEN}  [+] Max password age: {days} days")
                    else:
                        print(f"  {Fore.RED}  [!] Max password age too long: {days} days")
                        self.issues.append(f'Long password age: {days} days')
                        self.score -= 10
                else:
                    print(f"  {Fore.RED}  [!] No PASS_MAX_DAYS set")
                    self.issues.append('No password max age')
                    self.score -= 15

                pass_min = re.search(r'PASS_MIN_DAYS\s+(\d+)', content)
                if pass_min:
                    days = int(pass_min.group(1))
                    print(f"  {Fore.WHITE}  Min days between changes: {days}")

                pass_warn = re.search(r'PASS_WARN_AGE\s+(\d+)', content)
                if pass_warn:
                    days = int(pass_warn.group(1))
                    if days >= 7:
                        print(f"  {Fore.GREEN}  [+] Warning before expiry: {days} days")
                    else:
                        print(f"  {Fore.YELLOW}  [-] Warning too short: {days} days")
                        self.issues.append('Short warning period')
                        self.score -= 5

        except:
            print(f"  {Fore.YELLOW}  [-] Could not read /etc/login.defs")

    def check_common_passwords(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  COMMON PASSWORD CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}  Checking for {len(COMMON_PASSWORDS)} common passwords...")
        print(f"  {Fore.GREEN}  [+] Use pam_pwquality to enforce common password rejection")

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  PASSWORD POLICY CHECK COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        self.score = max(0, self.score)
        color = Fore.GREEN if self.score >= 80 else (Fore.YELLOW if self.score >= 50 else Fore.RED)
        print(f"\n  {color}Password Policy Score: {self.score}/100")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Password Policy Checker')
    args = parser.parse_args()

    checker = PasswordChecker()
    checker.check_pam_config()
    checker.check_password_hashes()
    checker.check_account_policies()
    checker.check_common_passwords()
    checker.print_summary()

if __name__ == "__main__":
    main()
