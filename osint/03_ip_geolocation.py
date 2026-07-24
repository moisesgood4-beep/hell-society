#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  IP GEOLOCATION & RECON v2.0                                     ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - IP Intelligence                               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗███╗   ██╗███████╗████████╗ ██████╗██╗  ██╗███████╗██████╗      {Fore.MAGENTA}║
║{Fore.CYAN}  ██║████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗     {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██╔██╗ ██║███████╗   ██║   ██║     ███████║█████╗  ██████╔╝     {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║╚██╗██║╚════██║   ██║   ██║     ██╔══██║██╔══╝  ██╔═══╝      {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║ ╚████║███████║   ██║   ╚██████╗██║  ██║███████╗██║          {Fore.MAGENTA}║
║{Fore.CYAN}  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝          {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - IP Geolocation & Recon v2.0                      {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

class IPRecon:
    def __init__(self, ip):
        self.ip = ip
        self.data = {}

    def geolocate(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  GEOLOCATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = requests.get(f'https://ip-api.com/json/{self.ip}', timeout=10)
            data = resp.json()

            if data.get('status') == 'success':
                print(f"  {Fore.WHITE}IP: {data.get('query')}")
                print(f"  {Fore.WHITE}Country: {data.get('country')} ({data.get('countryCode')})")
                print(f"  {Fore.WHITE}Region: {data.get('regionName')}")
                print(f"  {Fore.WHITE}City: {data.get('city')}")
                print(f"  {Fore.WHITE}ZIP: {data.get('zip')}")
                print(f"  {Fore.WHITE}Lat/Lon: {data.get('lat')}, {data.get('lon')}")
                print(f"  {Fore.WHITE}Timezone: {data.get('timezone')}")
                print(f"  {Fore.WHITE}ISP: {data.get('isp')}")
                print(f"  {Fore.WHITE}Org: {data.get('org')}")
                print(f"  {Fore.WHITE}AS: {data.get('as')}")
                self.data = data
            else:
                print(f"  {Fore.RED}[!] Error: {data.get('message')}")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_ports(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SHODAN-STYLE PORT CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            # Check common ports
            import socket
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995,
                          3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]

            open_ports = []
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"  {Fore.GREEN}[+] Port {port}: OPEN")
                else:
                    print(f"  {Fore.WHITE}  Port {port}: closed")
                sock.close()

            self.data['open_ports'] = open_ports

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def reverse_dns(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  REVERSE DNS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            import socket
            hostname = socket.gethostbyaddr(self.ip)
            print(f"  {Fore.GREEN}[+] Reverse DNS: {hostname[0]}")
            self.data['hostname'] = hostname[0]
        except:
            print(f"  {Fore.YELLOW}[-] No reverse DNS record")

    def check_blacklists(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  BLACKLIST CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        dnsbl_list = [
            'dnsbl.sorbs.net',
            'bl.spamcop.net',
            'zen.spamhaus.org',
            'b.barracudacentral.org',
            'dnsbl-1.uceprotect.net',
        ]

        import socket
        # Reverse IP for DNSBL
        octets = self.ip.split('.')
        reversed_ip = f"{octets[3]}.{octets[2]}.{octets[1]}.{octets[0]}"

        for dnsbl in dnsbl_list:
            query = f"{reversed_ip}.{dnsbl}"
            try:
                result = socket.gethostbyname(query)
                print(f"  {Fore.RED}[!] {dnsbl}: LISTED")
                self.data.setdefault('blacklisted', []).append(dnsbl)
            except:
                print(f"  {Fore.GREEN}[OK] {dnsbl}: Clean")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target IP: {Fore.WHITE}{self.ip}")
        print(f"{Fore.CYAN}  [*] Starting IP reconnaissance...\n")

        self.geolocate()
        self.check_ports()
        self.reverse_dns()
        self.check_blacklists()

        # Save results
        results_file = f'/tmp/ip_recon_{self.ip}.json'
        with open(results_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

        print(f"\n{Fore.GREEN}{Back.BLACK}  IP RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society IP Recon')
    parser.add_argument('-i', '--ip', required=True, help='Target IP address')
    args = parser.parse_args()

    recon = IPRecon(args.ip)
    recon.run()
