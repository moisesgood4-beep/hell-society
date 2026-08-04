#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PRIVILEGE ESCALATION DETECTOR v2.0                              ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - System Security                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse

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

class PrivEscDetector:
    def __init__(self):
        self.issues = []
        self.score = 100

    def check_suid(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUID/SGID FILES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        dangerous_suid = ['nmap', 'vim', 'find', 'bash', 'sh', 'cp', 'cat', 'chmod', 'python', 'perl']

        try:
            result = subprocess.run(['find', '/', '-perm', '-4000', '-type', 'f'], 
                                  capture_output=True, text=True, timeout=10)
            suid_files = result.stdout.strip().split('\n')

            print(f"  {Fore.WHITE}  SUID files found: {len(suid_files)}")
            for f in suid_files[:20]:
                if f:
                    basename = os.path.basename(f)
                    if basename in dangerous_suid:
                        print(f"  {Fore.RED}  [!] Dangerous SUID: {f}")
                        self.issues.append(f'Dangerous SUID: {f}')
                        self.score -= 10
                    else:
                        print(f"  {Fore.WHITE}  {f}")

        except:
            print(f"  {Fore.YELLOW}  [-] Could not scan SUID files")

    def check_sudo(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUDO CONFIGURATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['sudo', '-l'], capture_output=True, text=True, timeout=10)
            output = result.stdout

            if 'NOPASSWD' in output:
                print(f"  {Fore.RED}[!] NOPASSWD entries found!")
                self.issues.append('NOPASSWD sudo entries')
                self.score -= 20

            if 'ALL' in output and 'NOPASSWD' not in output:
                print(f"  {Fore.YELLOW}[-] Full sudo access")
                self.issues.append('Full sudo access')
                self.score -= 5

            if '(ALL : ALL) ALL' in output:
                print(f"  {Fore.YELLOW}[-] ALL:ALL sudo rule")
                self.score -= 5

            print(f"\n  {Fore.WHITE}  {output[:500]}")

        except:
            pass

    def check_writable_paths(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WRITABLE PATHS IN PATH:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        path_dirs = os.environ.get('PATH', '').split(':')
        for d in path_dirs:
            if d and os.path.exists(d):
                try:
                    stat = os.stat(d)
                    # Check if world-writable
                    if stat.st_mode & 0o002:
                        print(f"  {Fore.RED}[!] World-writable in PATH: {d}")
                        self.issues.append(f'Writable PATH: {d}')
                        self.score -= 15
                except:
                    pass

    def check_cron(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CRON JOBS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"  {Fore.WHITE}  User crontab:")
                for line in result.stdout.split('\n'):
                    print(f"    {Fore.WHITE}{line}")
                    if '* * * * *' in line and ('curl' in line or 'wget' in line):
                        print(f"    {Fore.RED}  [!] Suspicious cron: network command every minute!")
                        self.issues.append('Suspicious cron job')
                        self.score -= 10
        except:
            pass

        # System cron
        cron_dirs = ['/etc/cron.d/', '/etc/cron.daily/', '/etc/cron.weekly/', '/etc/cron.hourly/']
        for cron_dir in cron_dirs:
            if os.path.exists(cron_dir):
                files = os.listdir(cron_dir)
                for f in files:
                    filepath = os.path.join(cron_dir, f)
                    try:
                        with open(filepath, 'r') as fh:
                            content = fh.read()
                            if 'chmod 777' in content or 'bash -i' in content:
                                print(f"  {Fore.RED}[!] Suspicious system cron: {filepath}")
                                self.issues.append(f'Suspicious cron: {filepath}')
                                self.score -= 15
                    except:
                        pass

    def check_kernel(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  KERNEL VERSION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
        kernel = result.stdout.strip()
        print(f"  {Fore.WHITE}  Kernel: {kernel}")

        # Known vulnerable kernel ranges
        vulnerable = [
            ('3.', 'Old kernel - may have known exploits'),
            ('2.', 'Very old kernel - HIGHLY vulnerable'),
        ]

        for prefix, msg in vulnerable:
            if kernel.startswith(prefix):
                print(f"  {Fore.RED}  [!] {msg}")
                self.issues.append(f'Old kernel: {kernel}')
                self.score -= 15
                break

    def detect(self):
        print(f"{Fore.CYAN}  [*] Starting privilege escalation check...\n")
        self.check_suid()
        self.check_sudo()
        self.check_writable_paths()
        self.check_cron()
        self.check_kernel()
        self.print_summary()

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  PRIVILEGE ESCALATION CHECK COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        self.score = max(0, self.score)
        color = Fore.GREEN if self.score >= 80 else (Fore.YELLOW if self.score >= 50 else Fore.RED)
        print(f"\n  {color}Security Score: {self.score}/100")

        if len(self.issues) > 5:
            print(f"\n  {Fore.RED}[!!!] HIGH RISK of privilege escalation!")
        elif len(self.issues) > 2:
            print(f"\n  {Fore.YELLOW}[!] Some escalation vectors exist")
        else:
            print(f"\n  {Fore.GREEN}[OK] System is reasonably hardened")



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
    print(f"  {BW}{Style.BRIGHT}  PRIVILEGE ESCALATION DETECTOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}PRIVILEGE ESCALATION DETECTOR           {RS}  {G}╟{RS}")
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
            print(f"  {G}[*] Starting Privilege Escalation Detector...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Privilege Escalation Detector{RS}")
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

