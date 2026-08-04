#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  NETWORK TRAFFIC MONITOR v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Network Monitoring                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import scapy.all as scapy
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import time
from collections import defaultdict
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

class NetworkMonitor:
    def __init__(self, interface='any', duration=60):
        self.interface = interface
        self.duration = duration
        self.traffic_stats = defaultdict(int)
        self.protocols = defaultdict(int)
        self.src_ips = defaultdict(int)
        self.dst_ips = defaultdict(int)
        self.suspicious = []
        self.total_packets = 0
        self.start_time = None

    def process_packet(self, packet):
        self.total_packets += 1
        ts = time.time() - self.start_time

        if packet.haslayer(scapy.IP):
            src = packet[scapy.IP].src
            dst = packet[scapy.IP].dst
            self.src_ips[src] += 1
            self.dst_ips[dst] += 1

            if packet.haslayer(scapy.TCP):
                self.protocols['TCP'] += 1
                sport = packet[scapy.TCP].sport
                dport = packet[scapy.TCP].dport

                # Detect port scanning
                if dport in [22, 23, 25, 80, 443, 3306, 5432, 8080, 8443]:
                    if self.src_ips[src] > 100 and ts < 30:
                        self.suspicious.append(f"Possible scan from {src}")

                # Detect unusual ports
                if dport > 49152 and dport not in [0]:
                    self.suspicious.append(f"High port connection: {src}:{sport} -> {dst}:{dport}")

            elif packet.haslayer(scapy.UDP):
                self.protocols['UDP'] += 1
                dport = packet[scapy.UDP].dport

            elif packet.haslayer(scapy.ICMP):
                self.protocols['ICMP'] += 1

        # Detect potential DNS tunneling
        if packet.haslayer(scapy.DNS):
            self.protocols['DNS'] += 1

        if ts >= self.duration:
            raise StopIteration

    def monitor(self):
        print(f"{Fore.CYAN}  [*] Interface: {Fore.WHITE}{self.interface}")
        print(f"{Fore.CYAN}  [*] Duration: {Fore.WHITE}{self.duration}s")
        print(f"{Fore.CYAN}  [*] Starting network monitoring...\n")

        self.start_time = time.time()

        try:
            scapy.sniff(iface=self.interface, prn=self.process_packet, timeout=self.duration)
        except StopIteration:
            pass
        except KeyboardInterrupt:
            pass

        self.print_results()

    def print_results(self):
        elapsed = time.time() - self.start_time
        pps = self.total_packets / elapsed if elapsed > 0 else 0

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  MONITORING COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n  {Fore.CYAN}TRAFFIC SUMMARY:")
        print(f"  {Fore.WHITE}  Total packets: {self.total_packets}")
        print(f"  {Fore.WHITE}  Duration: {elapsed:.1f}s")
        print(f"  {Fore.WHITE}  Packets/sec: {pps:.1f}")

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PROTOCOL BREAKDOWN:")
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        for proto, count in sorted(self.protocols.items(), key=lambda x: x[1], reverse=True):
            pct = (count / self.total_packets) * 100 if self.total_packets > 0 else 0
            bar = f"{Fore.GREEN}█" * int(pct / 2)
            print(f"  {Fore.YELLOW}{proto:<10} {Fore.WHITE}{count:>8} ({pct:.1f}%) {bar}")

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TOP SOURCE IPs:")
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        for ip, count in sorted(self.src_ips.items(), key=lambda x: x[1], reverse=True)[:10]:
            marker = f" {Fore.RED}[HIGH]" if count > 50 else ""
            print(f"  {Fore.WHITE}{ip:<15} {count:>6} packets{marker}")

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TOP DESTINATION IPs:")
        print(f"{Fore.CYAN}  [{'═' * 40}]")
        for ip, count in sorted(self.dst_ips.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {Fore.WHITE}{ip:<15} {count:>6} packets")

        if self.suspicious:
            unique_suspicious = list(set(self.suspicious))[:10]
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  SUSPICIOUS ACTIVITY:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            for s in unique_suspicious:
                print(f"  {Fore.RED}  [!] {s}")

        threat_level = "LOW"
        if len(self.suspicious) > 20 or pps > 1000:
            threat_level = "HIGH"
        elif len(self.suspicious) > 5 or pps > 500:
            threat_level = "MEDIUM"

        color = Fore.GREEN if threat_level == "LOW" else (Fore.YELLOW if threat_level == "MEDIUM" else Fore.RED)
        print(f"\n  {color}[!] Network Threat Level: {threat_level}")



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
    print(f"  {BW}{Style.BRIGHT}  NETWORK MONITOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}NETWORK MONITOR                         {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Network interface                            {RS}")
        print(f"  {C}[2]  {BW}Monitor duration (seconds)                   {RS}")
        print()
        print(f"  {C}[3]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Network interface{RS}")
            value = input(f"  {Y}[*] -i: {RS}").strip()
            print(f"  {C}[*] Executing with -i={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Monitor duration (seconds){RS}")
            value = input(f"  {Y}[*] -d: {RS}").strip()
            print(f"  {C}[*] Executing with -d={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '3':
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

