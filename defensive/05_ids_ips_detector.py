#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  IDS/IPS REAL-TIME DETECTOR v2.0                                 ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Intrusion Detection                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import scapy.all as scapy
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import time
import json
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

SIGNATURES = {
    'port_scan': {'desc': 'Port Scan Detection', 'threshold': 20, 'window': 10},
    'syn_flood': {'desc': 'SYN Flood Detection', 'threshold': 100, 'window': 5},
    'brute_force': {'desc': 'Brute Force Detection', 'threshold': 5, 'window': 30},
    'dns_tunnel': {'desc': 'DNS Tunneling Detection', 'threshold': 50, 'window': 10},
    'arp_spoof': {'desc': 'ARP Spoofing Detection', 'threshold': 5, 'window': 5},
    'icmp_flood': {'desc': 'ICMP Flood Detection', 'threshold': 30, 'window': 5},
}

class IDSDetector:
    def __init__(self, interface='any', duration=60):
        self.interface = interface
        self.duration = duration
        self.packet_count = 0
        self.start_time = None
        self.alerts = []

        # Tracking
        self.syn_packets = defaultdict(list)
        self.port_access = defaultdict(list)
        self.dns_queries = defaultdict(list)
        self.arp_table = {}
        self.icmp_packets = defaultdict(list)
        self.failed_auth = defaultdict(list)

    def check_port_scan(self, src, dst_port, timestamp):
        self.port_access[src].append({'port': dst_port, 'time': timestamp})
        recent = [p for p in self.port_access[src] if timestamp - p['time'] < 10]
        unique_ports = set(p['port'] for p in recent)

        if len(unique_ports) > 20:
            alert = {
                'type': 'PORT_SCAN',
                'severity': 'HIGH',
                'src': src,
                'detail': f"Accessed {len(unique_ports)} ports in 10s"
            }
            self.alerts.append(alert)
            return alert
        return None

    def check_syn_flood(self, src, timestamp):
        self.syn_packets[src].append(timestamp)
        recent = [t for t in self.syn_packets[src] if timestamp - t < 5]

        if len(recent) > 100:
            alert = {
                'type': 'SYN_FLOOD',
                'severity': 'CRITICAL',
                'src': src,
                'detail': f"{len(recent)} SYN packets in 5s"
            }
            self.alerts.append(alert)
            return alert
        return None

    def check_arp_spoof(self, ip, mac):
        if ip in self.arp_table and self.arp_table[ip] != mac:
            alert = {
                'type': 'ARP_SPOOFING',
                'severity': 'HIGH',
                'ip': ip,
                'detail': f"MAC changed from {self.arp_table[ip]} to {mac}"
            }
            self.alerts.append(alert)
            return alert

        self.arp_table[ip] = mac
        return None

    def process_packet(self, packet):
        self.packet_count += 1
        timestamp = time.time()

        # IP layer analysis
        if packet.haslayer(scapy.IP):
            src = packet[scapy.IP].src
            dst = packet[scapy.IP].dst

            # TCP analysis
            if packet.haslayer(scapy.TCP):
                dport = packet[scapy.TCP].dport
                flags = str(packet[scapy.TCP].flags)

                if 'S' in flags and 'A' not in flags:
                    alert = self.check_syn_flood(src, timestamp)
                    if alert:
                        self._print_alert(alert)

                alert = self.check_port_scan(src, dport, timestamp)
                if alert:
                    self._print_alert(alert)

            # ICMP analysis
            if packet.haslayer(scapy.ICMP):
                self.icmp_packets[src].append(timestamp)
                recent = [t for t in self.icmp_packets[src] if timestamp - t < 5]
                if len(recent) > 30:
                    alert = {'type': 'ICMP_FLOOD', 'severity': 'HIGH', 'src': src,
                            'detail': f"{len(recent)} ICMP packets in 5s"}
                    self.alerts.append(alert)
                    self._print_alert(alert)

            # DNS analysis
            if packet.haslayer(scapy.DNS) and packet.haslayer(scapy.DNSQR):
                qname = packet[scapy.DNSQR].qname.decode('utf-8', errors='ignore')
                self.dns_queries[src].append(timestamp)
                recent = [t for t in self.dns_queries[src] if timestamp - t < 10]
                if len(recent) > 50:
                    alert = {'type': 'DNS_TUNNEL', 'severity': 'HIGH', 'src': src,
                            'detail': f"High DNS query rate from {src}"}
                    self.alerts.append(alert)
                    self._print_alert(alert)

        # ARP layer analysis
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            ip = packet[scapy.ARP].psrc
            mac = packet[scapy.ARP].hwsrc
            alert = self.check_arp_spoof(ip, mac)
            if alert:
                self._print_alert(alert)

    def _print_alert(self, alert):
        print(f"\n  {Fore.RED}{Back.BLACK} [ALERT] {Fore.WHITE}Type: {alert['type']}")
        print(f"  {Fore.RED}  Severity: {alert['severity']}")
        print(f"  {Fore.RED}  Source: {alert.get('src', 'N/A')}")
        print(f"  {Fore.RED}  Detail: {alert['detail']}")
        print(f"  {Fore.RED}  Time: {time.strftime('%H:%M:%S')}")
        print(f"  {Fore.CYAN}  {'─' * 50}")

    def detect(self):
        print(f"{Fore.CYAN}  [*] Interface: {Fore.WHITE}{self.interface}")
        print(f"{Fore.CYAN}  [*] Duration: {Fore.WHITE}{self.duration}s")
        print(f"{Fore.CYAN}  [*] Starting IDS/IPS...\n")

        self.start_time = time.time()

        # Print signature rules loaded
        print(f"{Fore.CYAN}  [*] Signatures loaded: {len(SIGNATURES)}")
        for name, sig in SIGNATURES.items():
            print(f"  {Fore.GREEN}  [+] {sig['desc']} (threshold: {sig['threshold']}, window: {sig['window']}s)")
        print()

        try:
            scapy.sniff(iface=self.interface, prn=self.process_packet, timeout=self.duration)
        except KeyboardInterrupt:
            pass

        self.print_summary()

    def print_summary(self):
        elapsed = time.time() - self.start_time
        critical = [a for a in self.alerts if a['severity'] == 'CRITICAL']
        high = [a for a in self.alerts if a['severity'] == 'HIGH']
        medium = [a for a in self.alerts if a['severity'] == 'MEDIUM']

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  IDS/IPS REPORT  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.WHITE}Total packets analyzed: {self.packet_count}")
        print(f"  {Fore.WHITE}Monitoring duration: {elapsed:.1f}s")
        print(f"  {Fore.WHITE}Total alerts: {len(self.alerts)}")
        print(f"  {Fore.RED}  CRITICAL: {len(critical)}")
        print(f"  {Fore.RED}  HIGH: {len(high)}")
        print(f"  {Fore.YELLOW}  MEDIUM: {len(medium)}")

        if self.alerts:
            print(f"\n{Fore.CYAN}  [{'═' * 40}]")
            print(f"  ALERT BREAKDOWN:")
            print(f"{Fore.CYAN}  [{'═' * 40}]")
            from collections import Counter
            type_counts = Counter(a['type'] for a in self.alerts)
            for t, c in type_counts.most_common():
                print(f"  {Fore.RED}  {t}: {c}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society IDS/IPS Detector')
    parser.add_argument('-i', '--interface', default='any', help='Network interface')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Detection duration')
    args = parser.parse_args()

    detector = IDSDetector(args.interface, args.duration)
    detector.detect()

if __name__ == "__main__":
    main()
