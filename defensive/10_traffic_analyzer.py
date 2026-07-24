#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  TRAFFIC ANOMALY DETECTOR v2.0                                   ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Traffic Analysis                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import time
import json
from collections import defaultdict

colorama.init(autoreset=True)

BANNER = f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗      █████╗  ██████╗██╗  {Fore.YELLOW}║
║{Fore.CYAN}  ╚══██╔══╝██║╚██╗██╔╝╚══██╔══╝██╔═══██╗██║     ██╔══██╗██╔════╝██║  {Fore.YELLOW}║
║{Fore.CYAN}     ██║   ██║ ╚███╔╝    ██║   ██║   ██║██║     ███████║██║     ██║  {Fore.YELLOW}║
║{Fore.CYAN}     ██║   ██║ ██╔██╗    ██║   ██║   ██║██║     ██╔══██║██║     ██║  {Fore.YELLOW}║
║{Fore.CYAN}     ██║   ██║██╔╝ ██╗   ██║   ╚██████╔╝███████╗██║  ██║╚██████╗███████{Fore.YELLOW}║
║{Fore.CYAN}     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════{Fore.YELLOW}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.RED}  HELL SOCIETY - Traffic Anomaly Detector v2.0                        {Fore.YELLOW}║
╚══════════════════════════════════════════════════════════════════╝
"""

class TrafficAnalyzer:
    def __init__(self, interface='any', duration=30):
        self.interface = interface
        self.duration = duration
        self.stats = defaultdict(lambda: defaultdict(int))
        self.anomalies = []
        self.start_time = None

    def collect_data(self):
        print(f"{Fore.CYAN}  [*] Interface: {Fore.WHITE}{self.interface}")
        print(f"{Fore.CYAN}  [*] Duration: {Fore.WHITE}{self.duration}s")
        print(f"{Fore.CYAN}  [*] Collecting traffic data...\n")

        self.start_time = time.time()

        # Collect network statistics
        try:
            result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
            print(f"  {Fore.GREEN}[+] Listening ports captured")
        except:
            pass

        try:
            result = subprocess.run(['ss', '-tunap'], capture_output=True, text=True)
            lines = result.stdout.split('\n')

            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 5:
                    state = parts[0]
                    local = parts[3] if len(parts) > 3 else ''
                    remote = parts[4] if len(parts) > 4 else ''

                    if 'ESTAB' in state:
                        if ':' in remote:
                            remote_ip = remote.rsplit(':', 1)[0]
                            self.stats['established'][remote_ip] += 1

                    elif 'TIME-WAIT' in state:
                        if ':' in remote:
                            remote_ip = remote.rsplit(':', 1)[0]
                            self.stats['time_wait'][remote_ip] += 1

                    elif 'SYN-SENT' in state or 'SYN-RECV' in state:
                        if ':' in remote:
                            remote_ip = remote.rsplit(':', 1)[0]
                            self.stats['syn'][remote_ip] += 1

        except:
            pass

        # Check for high connection counts
        for ip, count in self.stats['syn'].items():
            if count > 50:
                self.anomalies.append({
                    'type': 'SYN_FLOOD',
                    'ip': ip,
                    'count': count,
                    'severity': 'CRITICAL'
                })

        for ip, count in self.stats['established'].items():
            if count > 100:
                self.anomalies.append({
                    'type': 'HIGH_CONNECTIONS',
                    'ip': ip,
                    'count': count,
                    'severity': 'HIGH'
                })

    def analyze_ports(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PORT ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
            lines = result.stdout.split('\n')[1:]

            unexpected_ports = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 4:
                    addr = parts[3]
                    port = int(addr.rsplit(':', 1)[1]) if addr.rsplit(':', 1)[1].isdigit() else 0

                    if port > 1024 and port not in [3000, 5000, 8000, 8080, 8443, 9000, 3306, 5432, 6379, 27017]:
                        unexpected_ports.append(port)

            if unexpected_ports:
                print(f"  {Fore.YELLOW}[!] Unexpected ports: {unexpected_ports}")
                self.anomalies.append({
                    'type': 'UNEXPECTED_PORTS',
                    'ports': unexpected_ports,
                    'severity': 'MEDIUM'
                })
            else:
                print(f"  {Fore.GREEN}[OK] No unexpected ports")

        except:
            pass

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  ANALYSIS COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n  {Fore.WHITE}Established connections: {sum(self.stats['established'].values())}")
        print(f"  {Fore.WHITE}TIME-WAIT: {sum(self.stats['time_wait'].values())}")
        print(f"  {Fore.WHITE}SYN pending: {sum(self.stats['syn'].values())}")

        print(f"\n  {Fore.RED}[!] Anomalies detected: {len(self.anomalies)}")
        for a in self.anomalies:
            severity_color = Fore.RED if a['severity'] == 'CRITICAL' else (Fore.YELLOW if a['severity'] == 'MEDIUM' else Fore.RED)
            print(f"  {severity_color}[{a['severity']}] {a['type']}: {a}")

        if len(self.anomalies) > 5:
            print(f"\n  {Fore.RED}[!!!] Network requires IMMEDIATE investigation!")
        elif len(self.anomalies) > 2:
            print(f"\n  {Fore.YELLOW}[!] Some anomalies need review")
        else:
            print(f"\n  {Fore.GREEN}[OK] Network appears normal")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Traffic Analyzer')
    parser.add_argument('-i', '--interface', default='any', help='Network interface')
    parser.add_argument('-d', '--duration', type=int, default=30, help='Analysis duration')
    args = parser.parse_args()

    analyzer = TrafficAnalyzer(args.interface, args.duration)
    analyzer.collect_data()
    analyzer.analyze_ports()
    analyzer.print_results()

if __name__ == "__main__":
    main()
