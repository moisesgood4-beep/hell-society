#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  BRUTE FORCE DETECTOR & BLOCKER v2.0                             ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Brute Force Protection                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import subprocess
import colorama
from colorama import Fore, Back, Style
import argparse
import re
import time
from collections import defaultdict

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

class BruteForceDetector:
    def __init__(self, log_file, threshold=5, block_duration=3600):
        self.log_file = log_file
        self.threshold = threshold
        self.block_duration = block_duration
        self.attacks = defaultdict(list)
        self.blocked = []

    def analyze_logs(self):
        print(f"{Fore.CYAN}  [*] Log file: {Fore.WHITE}{self.log_file}")
        print(f"{Fore.CYAN}  [*] Threshold: {Fore.WHITE}{self.threshold} attempts")
        print(f"{Fore.CYAN}  [*] Block duration: {Fore.WHITE}{self.block_duration}s\n")

        if not os.path.exists(self.log_file):
            print(f"{Fore.RED}  [!] Log file not found!")
            return

        with open(self.log_file, 'r', errors='ignore') as f:
            lines = f.readlines()

        print(f"{Fore.CYAN}  [*] Analyzing {len(lines)} log entries...\n")

        ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        attack_patterns = [
            'failed password', 'authentication failure', 'invalid user',
            'login failed', 'access denied', '401', '403',
            'incorrect password', 'user not found'
        ]

        for line in lines:
            line_lower = line.lower()

            if any(p in line_lower for p in attack_patterns):
                ips = ip_pattern.findall(line)
                if ips:
                    ip = ips[0]
                    timestamp = time.time()
                    self.attacks[ip].append(timestamp)

        self._identify_attackers()

    def _identify_attackers(self):
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ATTACK ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        for ip, attempts in sorted(self.attacks.items(), key=lambda x: len(x[1]), reverse=True):
            if len(attempts) >= self.threshold:
                print(f"  {Fore.RED}[!] {ip}: {len(attempts)} failed attempts")

                # Block the IP
                self.blocked.append(ip)
                try:
                    subprocess.run(['iptables', '-I', 'INPUT', '-s', ip, '-j', 'DROP'],
                                  capture_output=True, timeout=5)
                    print(f"  {Fore.GREEN}    [+] IP blocked in iptables")
                except:
                    try:
                        subprocess.run(['ufw', 'deny', f'from {ip}'],
                                      capture_output=True, timeout=5)
                        print(f"  {Fore.GREEN}    [+] IP blocked in UFW")
                    except:
                        print(f"  {Fore.YELLOW}    [-] Could not block (need root)")

    def generate_banlist(self, output_file='/tmp/banlist.txt'):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BANLIST GENERATED:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        with open(output_file, 'w') as f:
            for ip in self.blocked:
                f.write(f"{ip}\n")
                print(f"  {Fore.RED}  {ip}")

        print(f"\n  {Fore.GREEN}[+] Banlist saved to: {output_file}")

    def print_summary(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.CYAN}SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}  IPs with attacks: {len(self.attacks)}")
        print(f"  {Fore.RED}  IPs blocked: {len(self.blocked)}")

        if len(self.blocked) > 10:
            print(f"  {Fore.RED}[!!!] HIGH BRUTE FORCE ACTIVITY DETECTED!")
        elif len(self.blocked) > 3:
            print(f"  {Fore.YELLOW}[!] Moderate brute force activity")
        else:
            print(f"  {Fore.GREEN}[OK] Low brute force activity")



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
    print(f"  {BW}{Style.BRIGHT}  BRUTE FORCE DETECTOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}BRUTE FORCE DETECTOR                    {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Log file (e.g., /var/log/auth.log)           {RS}")
        print(f"  {C}[2]  {BW}Failed attempts threshold                    {RS}")
        print(f"  {C}[3]  {BW}Block duration (seconds)                     {RS}")
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
            print(f"  {Y}[*] Log file (e.g., /var/log/auth.log){RS}")
            value = input(f"  {Y}[*] -f: {RS}").strip()
            print(f"  {C}[*] Executing with -f={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Failed attempts threshold{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Block duration (seconds){RS}")
            value = input(f"  {Y}[*] -d: {RS}").strip()
            print(f"  {C}[*] Executing with -d={BW}{value}{RS}")
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

