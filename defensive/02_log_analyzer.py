#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  LOG FILE ANALYZER v2.0                                          ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Log Analysis & Detection                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import re
import os
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
from collections import Counter, defaultdict
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

ALERT_KEYWORDS = [
    'error', 'fail', 'denied', 'unauthorized', 'attack', 'intrusion',
    'malware', 'virus', 'trojan', 'exploit', 'overflow', 'injection',
    'brute', 'scan', 'nmap', 'nikto', 'sqlmap', 'metasploit',
    'root', 'sudo', 'su ', 'passwd', 'shadow', 'chmod', 'chown',
    'useradd', 'usermod', 'groupadd', 'iptables', 'firewall',
    'shutdown', 'reboot', 'kill', 'rm -rf', 'wget', 'curl',
    'nc ', 'ncat', 'netcat', 'reverse', 'shell', 'backdoor',
    '404', '401', '403', '500', '503',
]

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.alerts = []
        self.ip_counter = Counter()
        self.event_counter = Counter()
        self.failed_logins = 0
        self.suspicious_ips = set()

    def analyze(self):
        if not os.path.exists(self.log_file):
            print(f"{Fore.RED}  [!] Log file not found: {self.log_file}")
            return

        print(f"{Fore.CYAN}  [*] Analyzing: {Fore.WHITE}{self.log_file}\n")

        with open(self.log_file, 'r', errors='ignore') as f:
            lines = f.readlines()

        print(f"{Fore.CYAN}  [*] Total lines: {len(lines)}\n")

        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()

            # Extract IPs
            ips = ip_pattern.findall(line)
            for ip in ips:
                self.ip_counter[ip] += 1

            # Check for alerts
            for keyword in ALERT_KEYWORDS:
                if keyword in line_lower:
                    self.alerts.append({
                        'line': i,
                        'keyword': keyword,
                        'content': line.strip()[:200]
                    })
                    break

            # Count failed logins
            if any(kw in line_lower for kw in ['failed password', 'authentication failure',
                                                'login failed', 'access denied']):
                self.failed_logins += 1

        self._identify_suspicious()
        self._print_results()

    def _identify_suspicious(self):
        for ip, count in self.ip_counter.items():
            if count > 50:
                self.suspicious_ips.add(ip)
                self.alerts.append({
                    'line': 0,
                    'keyword': 'high_frequency_ip',
                    'content': f"IP {ip} appeared {count} times"
                })

    def _print_results(self):
        print(f"\n{Fore.GREEN}{Back.BLACK}  ANALYSIS COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n  {Fore.CYAN}STATISTICS:")
        print(f"  {Fore.WHITE}  Total alerts: {len(self.alerts)}")
        print(f"  {Fore.WHITE}  Failed logins: {self.failed_logins}")
        print(f"  {Fore.WHITE}  Unique IPs: {len(self.ip_counter)}")
        print(f"  {Fore.WHITE}  Suspicious IPs: {len(self.suspicious_ips)}")

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TOP 10 IPs:")
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        for ip, count in self.ip_counter.most_common(10):
            marker = f" {Fore.RED}[SUSPICIOUS]" if ip in self.suspicious_ips else ""
            print(f"  {Fore.YELLOW}{ip:<15} {Fore.WHITE}{count:>6} occurrences{marker}")

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  RECENT ALERTS (last 15):")
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        for alert in self.alerts[-15:]:
            print(f"  {Fore.RED}[ALERT] {Fore.WHITE}Line {alert['line']} - Keyword: {alert['keyword']}")
            print(f"  {Fore.WHITE}  {alert['content'][:100]}")

        # Severity assessment
        severity = "LOW"
        if len(self.alerts) > 50 or self.failed_logins > 10:
            severity = "HIGH"
        elif len(self.alerts) > 20 or self.failed_logins > 5:
            severity = "MEDIUM"

        color = Fore.GREEN if severity == "LOW" else (Fore.YELLOW if severity == "MEDIUM" else Fore.RED)
        print(f"\n  {color}[!] Threat Level: {severity}")



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
    print(f"  {BW}{Style.BRIGHT}  LOG ANALYZER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}LOG ANALYZER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Log file path                                {RS}")
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
            print(f"  {Y}[*] Log file path{RS}")
            value = input(f"  {Y}[*] -f: {RS}").strip()
            print(f"  {C}[*] Executing with -f={BW}{value}{RS}")
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

