#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  NETWORK SEGMENTATION AUDITOR v2.0                               ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Network Security                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import ipaddress

colorama.init(autoreset=True)

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.RED}  ██╗   ██╗███████╗██╗  ██╗███████╗██████╗ ███████╗ █████╗  ██████╗ {Fore.CYAN}║
║{Fore.RED}  ██║   ██║██╔════╝╚██╗██╔╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗{Fore.CYAN}║
║{Fore.RED}  ██║   ██║█████╗   ╚███╔╝ █████╗  ██████╔╝█████╗  ███████║██║   ██║{Fore.CYAN}║
║{Fore.RED}  ╚██╗ ██╔╝██╔══╝   ██╔██╗ ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██║██║   ██║{Fore.CYAN}║
║{Fore.RED}   ╚████╔╝ ███████╗██╔╝ ██╗███████╗██║     ███████╗██║  ██║╚██████╔╝{Fore.CYAN}║
║{Fore.RED}    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ {Fore.CYAN}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Network Segmentation Auditor v2.0                  {Fore.CYAN}║
╚══════════════════════════════════════════════════════════════════╝
"""

class NetworkAuditor:
    def __init__(self):
        self.issues = []
        self.interfaces = []

    def get_interfaces(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  NETWORK INTERFACES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            lines = result.stdout.split('\n')

            current_iface = ''
            for line in lines:
                line = line.strip()
                if line and line[0].isdigit():
                    parts = line.split(':')
                    if len(parts) >= 2:
                        current_iface = parts[1].strip().split('@')[0]
                        state = 'UP' if 'UP' in line else 'DOWN'
                        print(f"  {Fore.WHITE}Interface: {current_iface} [{state}]")
                        self.interfaces.append(current_iface)

                elif 'inet ' in line:
                    ip = line.split()[1].split('/')[0]
                    print(f"    {Fore.GREEN}  IP: {ip}")

        except:
            pass

    def check_subnets(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUBNET ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            routes = result.stdout.split('\n')

            subnets = set()
            for route in routes:
                if '/' in route:
                    parts = route.split()
                    if parts:
                        subnet = parts[0]
                        if '/' in subnet:
                            subnets.add(subnet)

            for subnet in subnets:
                print(f"  {Fore.WHITE}  Subnet: {subnet}")

                net = ipaddress.ip_network(subnet, strict=False)
                if net.num_addresses > 254:
                    print(f"  {Fore.YELLOW}  [-] Large subnet (>{net.num_addresses} hosts)")
                    self.issues.append(f'Large subnet: {subnet}')

        except:
            pass

    def check_vlans(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  VLAN CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['cat', '/proc/net/vlan/config'], capture_output=True, text=True)
            if 'VLAN' in result.stdout:
                print(f"  {Fore.GREEN}[OK] VLANs configured")
            else:
                print(f"  {Fore.YELLOW}[-] No VLANs detected")
                self.issues.append('No VLAN segmentation')
        except:
            print(f"  {Fore.YELLOW}[-] Could not check VLANs")

    def check_forwarding(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  IP FORWARDING:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'r') as f:
                value = f.read().strip()

            if value == '1':
                print(f"  {Fore.YELLOW}[-] IP forwarding ENABLED")
                self.issues.append('IP forwarding enabled')
            else:
                print(f"  {Fore.GREEN}[OK] IP forwarding disabled")

        except:
            pass

    def check_broadcast(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BROADCAST TRAFFIC:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['ss', '-nupa'], capture_output=True, text=True)
            udp_lines = [l for l in result.stdout.split('\n') if 'udp' in l.lower()]
            print(f"  {Fore.WHITE}  UDP connections: {len(udp_lines)}")

            if len(udp_lines) > 20:
                print(f"  {Fore.YELLOW}[-] High UDP traffic - check for broadcast storms")
                self.issues.append('High UDP traffic')

        except:
            pass

    def audit(self):
        print(f"{Fore.CYAN}  [*] Starting network segmentation audit...\n")
        self.get_interfaces()
        self.check_subnets()
        self.check_vlans()
        self.check_forwarding()
        self.check_broadcast()
        self.print_summary()

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  NETWORK AUDIT COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        if not self.issues:
            print(f"\n  {Fore.GREEN}[OK] Network segmentation is adequate")
        elif len(self.issues) > 3:
            print(f"\n  {Fore.RED}[!] Network needs segmentation improvements")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Network Auditor')
    args = parser.parse_args()

    auditor = NetworkAuditor()
    auditor.audit()

if __name__ == "__main__":
    main()
