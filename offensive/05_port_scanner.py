#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  ADVANCED PORT SCANNER v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Network Reconnaissance                    ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import socket
import sys
import time
import colorama
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import struct

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

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt2", 9090: "Web-Console", 27017: "MongoDB",
    28017: "MongoDB-HTTP", 9200: "Elasticsearch", 9300: "ES-Transport",
    1099: "RMI", 4444: "Metasploit", 5555: "ADB",
    6667: "IRC", 8000: "HTTP-Dev", 8888: "Jupyter",
    11211: "Memcached", 5672: "RabbitMQ", 15672: "RabbitMQ-Mgmt",
    6443: "K8s-API", 2375: "Docker", 2376: "Docker-TLS",
}

class PortScanner:
    def __init__(self, target, start_port=1, end_port=10000, threads=100, timeout=1):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.timeout = timeout
        self.results = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                try:
                    banner = ""
                    sock.settimeout(0.5)
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                except:
                    banner = "No banner"
                sock.close()
                return {'port': port, 'status': 'OPEN', 'service': service, 'banner': banner}
            sock.close()
            return {'port': port, 'status': 'CLOSED', 'service': '', 'banner': ''}
        except Exception:
            return {'port': port, 'status': 'FILTERED', 'service': '', 'banner': ''}

    def scan(self):
        ports = range(self.start_port, self.end_port + 1)
        total = len(ports)
        print(f"{Fore.CYAN}  [*] Scanning {self.target} ports {self.start_port}-{self.end_port}")
        print(f"{Fore.CYAN}  [*] Using {self.threads} threads, {self.timeout}s timeout\n")

        completed = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.scan_port, port): port for port in ports}

            for future in as_completed(futures):
                completed += 1
                progress = (completed / total) * 100
                bar_length = 40
                filled = int(bar_length * completed / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Open: {len(self.results)}", end="", flush=True)

                result = future.result()
                if result['status'] == 'OPEN':
                    self.results.append(result)
                    banner_display = f" | Banner: {result['banner']}" if result['banner'] else ""
                    print(f"\n  {Fore.GREEN}[+] {Fore.WHITE}{result['port']}/{Fore.YELLOW}{result['service']} {Fore.CYAN}- OPEN{banner_display}")

    def print_results(self):
        if not self.results:
            print(f"\n\n{Fore.YELLOW}  [!] No open ports found")
            return

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  SCAN COMPLETE - {len(self.results)} OPEN PORTS FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        self.results.sort(key=lambda x: x['port'])
        print(f"\n{Fore.CYAN}  {'PORT':<10} {'SERVICE':<20} {'BANNER'}")
        print(f"{Fore.CYAN}  {'─' * 60}")
        for r in self.results:
            print(f"  {Fore.GREEN}{r['port']:<10} {Fore.YELLOW}{r['service']:<20} {Fore.WHITE}{r['banner']}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Port Scanner')
    parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    parser.add_argument('-p', '--ports', default='1-10000', help='Port range (e.g., 1-1000 or 80,443,8080)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('--timeout', type=int, default=1, help='Socket timeout')
    args = parser.parse_args()

    if '-' in args.ports:
        start, end = args.ports.split('-')
        start_port, end_port = int(start), int(end)
    else:
        ports_list = [int(p.strip()) for p in args.ports.split(',')]
        start_port, end_port = min(ports_list), max(ports_list)

    scanner = PortScanner(args.target, start_port, end_port, args.threads, args.timeout)
    print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{args.target}")
    print(f"{Fore.CYAN}  [*] Port Range: {Fore.WHITE}{start_port}-{end_port}")
    print(f"{Fore.CYAN}  [*] Starting scan...\n")

    scanner.scan()
    scanner.print_results()

if __name__ == "__main__":
    main()
