#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HONEYPOT DETECTOR v2.0                                          ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Honeypot & Deception                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import socket
import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import time
from datetime import datetime

colorama.init(autoreset=True)

BANNER = f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗  ██╗ █████╗  ██████╗██╗  ██╗    ██╗  ██╗ █████╗ ███╗   ██╗     {Fore.YELLOW}║
║{Fore.CYAN}  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ██║  ██║██╔══██╗████╗  ██║     {Fore.YELLOW}║
║{Fore.CYAN}  ███████║███████║██║     █████╔╝     ███████║███████║██╔██╗ ██║     {Fore.YELLOW}║
║{Fore.CYAN}  ██╔══██║██╔══██║██║     ██╔═██╗     ██╔══██║██╔══██║██║╚██╗██║     {Fore.YELLOW}║
║{Fore.CYAN}  ██║  ██║██║  ██║╚██████╗██║  ██╗    ██║  ██║██║  ██║██║ ╚████║     {Fore.YELLOW}║
║{Fore.CYAN}  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝     {Fore.YELLOW}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.RED}  HELL SOCIETY - Honeypot Detector v2.0                               {Fore.YELLOW}║
╚══════════════════════════════════════════════════════════════════╝
"""

class Honeypot:
    def __init__(self, port=4444, log_file='/tmp/honeypot.log'):
        self.port = port
        self.log_file = log_file
        self.connections = []

    def start_ssh_honeypot(self):
        print(f"{Fore.CYAN}  [*] Starting SSH honeypot on port {self.port}...")
        print(f"{Fore.CYAN}  [*] Logging to: {self.log_file}\n")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)

        print(f"  {Fore.GREEN}[+] Honeypot listening on 0.0.0.0:{self.port}")
        print(f"  {Fore.GREEN}[+] Waiting for connections...\n")

        try:
            while True:
                client, addr = server.accept()
                timestamp = datetime.now().isoformat()

                print(f"  {Fore.RED}[ALERT] Connection from: {addr[0]}:{addr[1]}")

                self.connections.append({
                    'ip': addr[0],
                    'port': addr[1],
                    'time': timestamp
                })

                # Send fake banner
                banner = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
                client.send(banner)

                # Log
                log_entry = f"[{timestamp}] Connection from {addr[0]}:{addr[1]}\n"
                with open(self.log_file, 'a') as f:
                    f.write(log_entry)

                time.sleep(2)
                client.close()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}[!] Stopping honeypot...")
        finally:
            server.close()
            self.save_report()

    def save_report(self):
        report = {
            'total_connections': len(self.connections),
            'connections': self.connections,
            'unique_ips': list(set(c['ip'] for c in self.connections)),
        }

        report_file = '/tmp/honeypot_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n  {Fore.GREEN}[+] Report saved: {report_file}")
        print(f"  {Fore.GREEN}[+] Total connections: {len(self.connections)}")
        print(f"  {Fore.GREEN}[+] Unique IPs: {len(report['unique_ips'])}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Honeypot')
    parser.add_argument('-p', '--port', type=int, default=4444, help='Honeypot port')
    parser.add_argument('-l', '--log', default='/tmp/honeypot.log', help='Log file')
    args = parser.parse_args()

    honeypot = Honeypot(args.port, args.log)
    honeypot.start_ssh_honeypot()

if __name__ == "__main__":
    main()
