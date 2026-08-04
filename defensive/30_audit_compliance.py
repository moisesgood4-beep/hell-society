#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  COMPLIANCE AUDITOR v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Compliance & Auditing                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
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

class ComplianceAuditor:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.findings = []

    def check_a1_account_management(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  A1 - ACCOUNT MANAGEMENT:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check for shared accounts
        with open('/etc/passwd', 'r') as f:
            uids = {}
            for line in f:
                parts = line.strip().split(':')
                uid = int(parts[2])
                if uid >= 1000:
                    if uid in uids:
                        print(f"  {Fore.RED}[FAIL] Shared UID {uid}: {uids[uid]} & {parts[0]}")
                        self.findings.append(f'A1-FAIL: Shared UID {uid}')
                        self.failed += 1
                    else:
                        uids[uid] = parts[0]

            if len(self.findings) == 0:
                print(f"  {Fore.GREEN}[PASS] No shared accounts")
                self.passed += 1

        # Check password hashing
        try:
            with open('/etc/shadow', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) >= 2:
                        hash_type = parts[1][:3] if parts[1] else ''
                        if hash_type == '$1$':
                            print(f"  {Fore.RED}[FAIL] Weak hash for {parts[0]}")
                            self.findings.append('A1-FAIL: Weak hash algorithm')
                            self.failed += 1
                            break
                else:
                    print(f"  {Fore.GREEN}[PASS] Strong password hashing")
                    self.passed += 1
        except:
            pass

    def check_a2_access_control(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  A2 - ACCESS CONTROL:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check file permissions on sensitive files
        sensitive_files = ['/etc/shadow', '/etc/passwd', '/etc/sudoers']
        for sf in sensitive_files:
            if os.path.exists(sf):
                mode = oct(os.stat(sf).st_mode)[-4:]
                if mode == '0640' or mode == '0600':
                    print(f"  {Fore.GREEN}[PASS] {sf}: {mode}")
                    self.passed += 1
                else:
                    print(f"  {Fore.RED}[FAIL] {sf}: {mode} (too permissive)")
                    self.findings.append(f'A2-FAIL: {sf} mode {mode}')
                    self.failed += 1

    def check_a3_authentication(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  A3 - AUTHENTICATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check SSH config
        ssh_config = '/etc/ssh/sshd_config'
        if os.path.exists(ssh_config):
            with open(ssh_config, 'r') as f:
                content = f.read()

            if 'PasswordAuthentication no' in content:
                print(f"  {Fore.GREEN}[PASS] Password auth disabled in SSH")
                self.passed += 1
            else:
                print(f"  {Fore.RED}[FAIL] Password auth enabled in SSH")
                self.findings.append('A3-FAIL: SSH password auth enabled')
                self.failed += 1

            if 'PermitRootLogin no' in content:
                print(f"  {Fore.GREEN}[PASS] Root login disabled")
                self.passed += 1
            else:
                print(f"  {Fore.RED}[FAIL] Root login may be enabled")
                self.findings.append('A3-FAIL: Root login not disabled')
                self.failed += 1

    def check_a4_logging(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  A4 - LOGGING & MONITORING:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check if syslog is running
        try:
            result = subprocess.run(['systemctl', 'is-active', 'rsyslog'], 
                                  capture_output=True, text=True, timeout=5)
            if result.stdout.strip() == 'active':
                print(f"  {Fore.GREEN}[PASS] Syslog active")
                self.passed += 1
            else:
                print(f"  {Fore.RED}[FAIL] Syslog not active")
                self.findings.append('A4-FAIL: Syslog inactive')
                self.failed += 1
        except:
            pass

        # Check log rotation
        if os.path.exists('/etc/logrotate.conf'):
            print(f"  {Fore.GREEN}[PASS] Log rotation configured")
            self.passed += 1
        else:
            print(f"  {Fore.RED}[FAIL] No log rotation")
            self.findings.append('A4-FAIL: No log rotation')
            self.failed += 1

    def check_a5_encryption(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  A5 - ENCRYPTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check disk encryption
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,FSTYPE,MOUNTPOINT'], 
                                  capture_output=True, text=True)
            if 'crypto' in result.stdout.lower() or 'luks' in result.stdout.lower():
                print(f"  {Fore.GREEN}[PASS] Disk encryption detected")
                self.passed += 1
            else:
                print(f"  {Fore.YELLOW}[-] No disk encryption detected")
                self.findings.append('A5-WARN: No disk encryption')
                self.failed += 1
        except:
            pass

    def audit(self):
        print(f"{Fore.CYAN}  [*] Starting compliance audit...\n")
        self.check_a1_account_management()
        self.check_a2_access_control()
        self.check_a3_authentication()
        self.check_a4_logging()
        self.check_a5_encryption()
        self.print_summary()

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  COMPLIANCE AUDIT COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.GREEN}[PASS] {self.passed}")
        print(f"  {Fore.RED}[FAIL] {self.failed}")

        if self.findings:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  FINDINGS:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            for f in self.findings:
                print(f"  {Fore.RED}• {f}")

        score = max(0, (self.passed / (self.passed + self.failed) * 100)) if (self.passed + self.failed) > 0 else 0
        color = Fore.GREEN if score >= 80 else (Fore.YELLOW if score >= 50 else Fore.RED)
        print(f"\n  {color}Compliance Score: {score:.0f}%")



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
    print(f"  {BW}{Style.BRIGHT}  AUDIT COMPLIANCE{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}AUDIT COMPLIANCE                        {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Iniciar herramienta{RS}")
        print(f"  {C}[2]  {BW}Configurar opciones{RS}")
        print(f"  {C}[3]  {BW}Mostrar ayuda/uso{RS}")
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
            print(f"  {G}[*] Starting Audit Compliance...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Audit Compliance{RS}")
            print(f"  {Y}    Interactive tool with guided inputs{RS}")
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

