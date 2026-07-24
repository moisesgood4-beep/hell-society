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

BANNER = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗      █████╗ ██╗   ██╗███████╗ ██████╗ ██╗  ██╗███████╗██╗      {Fore.BLUE}║
║{Fore.CYAN}  ██║     ██╔══██╗██║   ██║██╔════╝██╔═══██╗██║ ██╔╝██╔════╝██║      {Fore.BLUE}║
║{Fore.CYAN}  ██║     ███████║██║   ██║███████╗██║   ██║█████╔╝ █████╗  ██║      {Fore.BLUE}║
║{Fore.CYAN}  ██║     ██╔══██║╚██╗ ██╔╝╚════██║██║   ██║██╔═██╗ ██╔══╝  ██║      {Fore.BLUE}║
║{Fore.CYAN}  ███████╗██║  ██║ ╚████╔╝ ███████║╚██████╔╝██║  ██╗███████╗███████╗ {Fore.BLUE}║
║{Fore.CYAN}  ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ {Fore.BLUE}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Log File Analyzer v2.0                               {Fore.BLUE}║
╚══════════════════════════════════════════════════════════════════╝
"""

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

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Log Analyzer')
    parser.add_argument('-f', '--file', required=True, help='Log file path')
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.file)
    analyzer.analyze()

if __name__ == "__main__":
    main()
