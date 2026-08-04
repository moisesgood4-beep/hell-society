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
    print(f"  {BW}{Style.BRIGHT}  WIRELESS SNIFFER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}WIRELESS SNIFFER                        {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Network interface                            {RS}")
        print(f"  {C}[2]  {BW}Sniff duration in seconds                    {RS}")
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
            print(f"  {Y}[*] Sniff duration in seconds{RS}")
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

