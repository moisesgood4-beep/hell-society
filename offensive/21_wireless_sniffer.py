#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WIRELESS NETWORK SNIFFER v2.0                                   ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Network Security                          ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import scapy.all as scapy
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

class WirelessSniffer:
    def __init__(self, interface='wlan0', duration=30):
        self.interface = interface
        self.duration = duration
        self.clients = defaultdict(set)
        self.aps = set()
        self.packets_count = 0

    def process_packet(self, packet):
        self.packets_count += 1

        if packet.haslayer(scapy.Dot11):
            dot11 = packet[scapy.Dot11]

            if dot11.type == 0 and dot11.subtype == 8:
                bssid = dot11.addr2
                ssid = dot11[scapy.Dot11Elt].info.decode('utf-8', errors='ignore')
                if ssid:
                    self.aps.add((bssid, ssid))
                    print(f"  {Fore.GREEN}[AP] {Fore.WHITE}{ssid:<30} {Fore.CYAN}BSSID: {bssid}")

            elif dot11.type == 0 and dot11.subtype == 0:
                bssid = dot11.addr1
                client = dot11.addr2
                if bssid != 'ff:ff:ff:ff:ff:ff':
                    self.clients[bssid].add(client)
                    print(f"  {Fore.YELLOW}[CLIENT] {Fore.WHITE}{client} -> {Fore.CYAN}BSSID: {bssid}")

        if packet.haslayer(scapy.Raw):
            raw = packet[scapy.Raw].load
            try:
                decoded = raw.decode('utf-8', errors='ignore')
                if any(kw in decoded.lower() for kw in ['password', 'login', 'auth', 'token']):
                    print(f"  {Fore.RED}[SENSITIVE] Possible credentials in packet #{self.packets_count}")
                    print(f"           {Fore.WHITE}{decoded[:100]}")
            except:
                pass

    def sniff(self):
        print(f"{Fore.CYAN}  [*] Interface: {Fore.WHITE}{self.interface}")
        print(f"{Fore.CYAN}  [*] Duration: {Fore.WHITE}{self.duration}s")
        print(f"{Fore.CYAN}  [*] Starting wireless sniff...\n")

        start_time = time.time()
        while time.time() - start_time < self.duration:
            elapsed = time.time() - start_time
            remaining = self.duration - elapsed
            progress = (elapsed / self.duration) * 100

            bar_length = 40
            filled = int(bar_length * elapsed / self.duration)
            bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)

            print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% | Packets: {self.packets_count} | APs: {len(self.aps)} | Clients: {sum(len(v) for v in self.clients.values())} | Remaining: {remaining:.0f}s", end="", flush=True)

            scapy.sniff(iface=self.interface, count=1, timeout=1, prn=self.process_packet)

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  SNIFF COMPLETE - {self.packets_count} PACKETS CAPTURED  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n{Fore.CYAN}  ACCESS POINTS FOUND: {len(self.aps)}")
        for bssid, ssid in self.aps:
            print(f"  {Fore.GREEN}  [+] {Fore.WHITE}{ssid} {Fore.CYAN}({bssid})")

        print(f"\n{Fore.CYAN}  CLIENTS PER AP:")
        for bssid, clients in self.clients.items():
            print(f"  {Fore.YELLOW}  AP: {bssid}")
            for client in clients:
                print(f"    {Fore.WHITE}  • {client}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Wireless Sniffer')
    parser.add_argument('-i', '--interface', default='wlan0', help='Network interface')
    parser.add_argument('-d', '--duration', type=int, default=30, help='Sniff duration in seconds')
    args = parser.parse_args()

    sniffer = WirelessSniffer(args.interface, args.duration)
    sniffer.sniff()

if __name__ == "__main__":
    main()
