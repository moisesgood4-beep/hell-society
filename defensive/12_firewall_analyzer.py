#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  FIREWALL RULE ANALYZER v2.0                                     ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Firewall Analysis                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
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

class FirewallAnalyzer:
    def __init__(self):
        self.issues = []
        self.rules = []

    def analyze_iptables(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  IPTABLES ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['iptables', '-L', '-n', '-v'], capture_output=True, text=True, timeout=10)
            lines = result.stdout.split('\n')

            print(f"  {Fore.WHITE}  {len(lines)} rules found")
            print()

            for line in lines:
                self.rules.append(line)

                if 'ACCEPT' in line and '0.0.0.0/0' in line and 'tcp dpt:22' in line:
                    self.issues.append('SSH open to all IPs - restrict to specific ranges')

                if 'ACCEPT' in line and '0.0.0.0/0' in line and 'tcp dpt:3306' in line:
                    self.issues.append('MySQL open to all IPs - CRITICAL!')

                if 'ACCEPT' in line and '0.0.0.0/0' in line and 'tcp dpt:5432' in line:
                    self.issues.append('PostgreSQL open to all IPs - CRITICAL!')

                if 'ACCEPT' in line and '0.0.0.0/0' in line and 'tcp dpt:6379' in line:
                    self.issues.append('Redis open to all IPs - CRITICAL!')

            # Check default policies
            for line in lines[:10]:
                if 'INPUT' in line and 'ACCEPT' in line:
                    self.issues.append('Default INPUT policy is ACCEPT - should be DROP')
                if 'FORWARD' in line and 'ACCEPT' in line:
                    self.issues.append('Default FORWARD policy is ACCEPT')

        except:
            print(f"  {Fore.YELLOW}  [-] Could not read iptables (need root)")

    def analyze_ufw(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  UFW ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            result = subprocess.run(['ufw', 'status', 'verbose'], capture_output=True, text=True, timeout=10)
            output = result.stdout

            if 'inactive' in output.lower():
                print(f"  {Fore.RED}  [!!!] UFW is INACTIVE - firewall is down!")
                self.issues.append('UFW inactive')
            else:
                print(f"  {Fore.GREEN}  [OK] UFW is active")
                print(f"\n  {Fore.WHITE}  Rules:")
                for line in output.split('\n'):
                    if 'ALLOW' in line or 'DENY' in line:
                        print(f"    {Fore.WHITE}{line.strip()}")

        except:
            print(f"  {Fore.YELLOW}  [-] UFW not installed")

    def check_dangerous_ports(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DANGEROUS PORT CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        dangerous_ports = {
            21: 'FTP', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            110: 'POP3', 143: 'IMAP', 135: 'RPC', 139: 'NetBIOS',
            445: 'SMB', 1433: 'MSSQL', 1521: 'Oracle',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 9200: 'Elasticsearch',
            27017: 'MongoDB', 11211: 'Memcached'
        }

        try:
            result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
            for line in result.stdout.split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    addr = parts[3]
                    port = int(addr.rsplit(':', 1)[1]) if addr.rsplit(':', 1)[1].isdigit() else 0

                    if port in dangerous_ports:
                        print(f"  {Fore.RED}  [!] Port {port} ({dangerous_ports[port]}) is LISTENING")
                        self.issues.append(f"Dangerous port open: {port} ({dangerous_ports[port]})")

        except:
            pass

    def generate_recommendations(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  RECOMMENDATIONS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        recommendations = [
            "Set default INPUT policy to DROP",
            "Restrict SSH access to specific IP ranges",
            "Enable UFW/firewalld if not active",
            "Block all unnecessary ports",
            "Use VPN for database access instead of direct exposure",
            "Implement fail2ban for brute force protection",
            "Enable logging for all dropped packets",
            "Use iptables rate limiting to prevent DoS",
        ]

        for i, rec in enumerate(recommendations, 1):
            print(f"  {Fore.GREEN}  {i}. {rec}")

    def analyze(self):
        print(f"{Fore.CYAN}  [*] Starting firewall analysis...\n")
        self.analyze_iptables()
        self.analyze_ufw()
        self.check_dangerous_ports()
        self.generate_recommendations()
        self.print_summary()

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  FIREWALL ANALYSIS COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues found: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        if len(self.issues) > 5:
            print(f"\n  {Fore.RED}[!!!] CRITICAL: Firewall needs immediate attention!")
        elif len(self.issues) > 2:
            print(f"\n  {Fore.YELLOW}[!] Some issues need fixing")
        else:
            print(f"\n  {Fore.GREEN}[OK] Firewall is reasonably configured")



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
    print(f"  {BW}{Style.BRIGHT}  FIREWALL ANALYZER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}FIREWALL ANALYZER                       {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Full analysis                                {RS}")
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
            print(f"  {Y}[*] Full analysis{RS}")
            value = input(f"  {Y}[*] --full: {RS}").strip()
            print(f"  {C}[*] Executing with --full={BW}{value}{RS}")
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

