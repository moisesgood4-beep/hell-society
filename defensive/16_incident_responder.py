#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  INCIDENT RESPONSE TOOLKIT v2.0                                  ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Incident Response                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
import json
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

class IncidentResponder:
    def __init__(self, output_dir='/tmp/incident_response'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.evidence = []

    def collect_system_info(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SYSTEM INFORMATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        info = {}

        # OS info
        info['os'] = subprocess.run(['uname', '-a'], capture_output=True, text=True).stdout.strip()
        print(f"  {Fore.WHITE}OS: {info['os']}")

        # Uptime
        info['uptime'] = subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
        print(f"  {Fore.WHITE}Uptime: {info['uptime']}")

        # Hostname
        info['hostname'] = subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()
        print(f"  {Fore.WHITE}Hostname: {info['hostname']}")

        # Users logged in
        info['users'] = subprocess.run(['who'], capture_output=True, text=True).stdout.strip()
        print(f"  {Fore.WHITE}Logged in: {info['users']}")

        filepath = os.path.join(self.output_dir, 'system_info.json')
        with open(filepath, 'w') as f:
            json.dump(info, f, indent=2)
        print(f"  {Fore.GREEN}[+] Saved to: {filepath}")

    def collect_network_state(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  NETWORK STATE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Connections
        connections = subprocess.run(['ss', '-tunap'], capture_output=True, text=True).stdout
        filepath = os.path.join(self.output_dir, 'network_connections.txt')
        with open(filepath, 'w') as f:
            f.write(connections)
        print(f"  {Fore.GREEN}[+] Connections saved: {filepath}")
        print(f"  {Fore.WHITE}  Active connections: {len(connections.split(chr(10)))}")

        # ARP table
        arp = subprocess.run(['arp', '-a'], capture_output=True, text=True).stdout
        filepath = os.path.join(self.output_dir, 'arp_table.txt')
        with open(filepath, 'w') as f:
            f.write(arp)
        print(f"  {Fore.GREEN}[+] ARP table saved")

        # Routing
        routes = subprocess.run(['ip', 'route'], capture_output=True, text=True).stdout
        filepath = os.path.join(self.output_dir, 'routing_table.txt')
        with open(filepath, 'w') as f:
            f.write(routes)
        print(f"  {Fore.GREEN}[+] Routing table saved")

    def collect_processes(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PROCESS ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        processes = subprocess.run(['ps', 'aux', '--sort=-%cpu'], capture_output=True, text=True).stdout
        filepath = os.path.join(self.output_dir, 'processes.txt')
        with open(filepath, 'w') as f:
            f.write(processes)
        print(f"  {Fore.GREEN}[+] Processes saved: {filepath}")

        # Check for suspicious processes
        suspicious = ['ncat', 'nc ', 'meterpreter', 'cobalt', 'mimikatz', 'hashcat']
        for proc in processes.split('\n'):
            for sus in suspicious:
                if sus in proc.lower():
                    print(f"  {Fore.RED}[!!!] SUSPICIOUS: {proc.strip()}")
                    self.evidence.append(proc.strip())

    def collect_logs(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  LOG COLLECTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        log_files = [
            '/var/log/auth.log',
            '/var/log/syslog',
            '/var/log/messages',
            '/var/log/secure',
            '/var/log/kern.log',
            '/var/log/dmesg',
            '/var/log/lastlog',
        ]

        for log_file in log_files:
            if os.path.exists(log_file):
                dest = os.path.join(self.output_dir, os.path.basename(log_file))
                subprocess.run(['cp', log_file, dest])
                print(f"  {Fore.GREEN}[+] Collected: {log_file}")

    def collect_users(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  USER ACCOUNTS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check /etc/passwd
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    uid = int(parts[2])
                    if uid == 0 and parts[0] != 'root':
                        print(f"  {Fore.RED}[!!!] Another UID 0 user: {parts[0]}")
                        self.evidence.append(f'UID0: {parts[0]}')
                    if '/bin/bash' in line or '/bin/sh' in line:
                        print(f"  {Fore.YELLOW}  [-] Shell access: {parts[0]}")

        # Check sudoers
        try:
            sudoers = subprocess.run(['cat', '/etc/sudoers'], capture_output=True, text=True).stdout
            if 'NOPASSWD' in sudoers:
                print(f"  {Fore.RED}[!!!] NOPASSWD in sudoers!")
                self.evidence.append('NOPASSWD in sudoers')
        except:
            pass

    def generate_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'evidence_count': len(self.evidence),
            'evidence': self.evidence,
            'output_dir': self.output_dir,
        }

        filepath = os.path.join(self.output_dir, 'incident_report.json')
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Report saved: {filepath}")

    def respond(self):
        print(f"{Fore.CYAN}  [*] Incident Response initiated...")
        print(f"{Fore.CYAN}  [*] Output: {Fore.WHITE}{self.output_dir}\n")

        self.collect_system_info()
        self.collect_network_state()
        self.collect_processes()
        self.collect_logs()
        self.collect_users()
        self.generate_report()

        print(f"\n{Fore.GREEN}[OK] Incident response data collected successfully!")
        if self.evidence:
            print(f"{Fore.RED}[!] Evidence items: {len(self.evidence)}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Incident Response')
    parser.add_argument('-o', '--output', default='/tmp/incident_response', help='Output directory')
    parser.add_argument('--full', action='store_true', help='Full collection')
    args = parser.parse_args()

    responder = IncidentResponder(args.output)
    responder.respond()

if __name__ == "__main__":
    main()
