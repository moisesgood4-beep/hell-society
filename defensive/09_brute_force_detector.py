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

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Brute Force Detector')
    parser.add_argument('-f', '--file', required=True, help='Log file (e.g., /var/log/auth.log)')
    parser.add_argument('-t', '--threshold', type=int, default=5, help='Failed attempts threshold')
    parser.add_argument('-d', '--duration', type=int, default=3600, help='Block duration (seconds)')
    args = parser.parse_args()

    detector = BruteForceDetector(args.file, args.threshold, args.duration)
    detector.analyze_logs()
    detector.generate_banlist()
    detector.print_summary()

if __name__ == "__main__":
    main()
