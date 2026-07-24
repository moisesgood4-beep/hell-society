#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - WiFi Network Scanner & Analyzer                ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, subprocess, struct, socket
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

BANNER=f"""{BR}
██╗    ██╗██╗     ██╗      ██████╗  █████╗ ████████╗███████╗
██║    ██║██║     ██║     ██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
██║ █╗ ██║██║     ██║     ██║   ██║███████║   ██║   ███████╗
██║███╗██║██║     ██║     ██║   ██║██╔══██║   ██║   ╚════██║
╚███╔███╔╝███████╗███████╗╚██████╔╝██║  ██║   ██║   ███████║
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
{Y}  Created by: HELL SOCIETY{RS}
"""

class WiFiScanner:
    def __init__(self):
        self.networks = []
        self.results = {}

    def scan_linux(self):
        print(f"\n{G}[+] Method 1: Linux WiFi Scan (iwlist/nmcli){RS}")
        # Try nmcli
        try:
            result = subprocess.run(['nmcli', '-t', '-f', 'SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY', 'device', 'wifi', 'list'],
                                   capture_output=True, text=True, timeout=15)
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                print(f"  {G}[✓] Found {len(lines)} networks via nmcli")
                for line in lines[:20]:
                    parts = line.split(':')
                    if len(parts) >= 6:
                        ssid, bssid, chan, freq, signal, security = parts[:6]
                        print(f"  {C}  SSID: {W}{ssid[:20]:20} | {Y}CH: {chan} | {M}Sig: {signal}dBm | {R}Sec: {security}")
                        self.networks.append({'ssid': ssid, 'bssid': bssid, 'chan': chan, 'signal': signal, 'security': security})
                self.results['linux_wifi'] = self.networks
                return
        except FileNotFoundError:
            pass

        # Try iwlist
        try:
            result = subprocess.run(['sudo', 'iwlist', 'scan'], capture_output=True, text=True, timeout=15)
            if result.stdout:
                cells = re.findall(r'Cell \d+ - Address: ([0-9A-Fa-f:]+)\n.*?ESSID:"([^"]*)"\n.*?Quality=([^\s]+)\n.*?Signal level=(-?\d+)',
                                  result.stdout, re.DOTALL)
                print(f"  {G}[✓] Found {len(cells)} networks via iwlist")
                for addr, ssid, quality, signal in cells[:20]:
                    print(f"  {C}  SSID: {W}{ssid[:20]:20} | {Y}BSSID: {addr} | {M}Signal: {signal}dBm")
                    self.networks.append({'ssid': ssid, 'bssid': addr, 'signal': signal})
                self.results['iwlist'] = self.networks
        except FileNotFoundError:
            print(f"  {R}[!] Neither nmcli nor iwlist available")

    def scan_termux(self):
        print(f"\n{G}[+] Method 2: Termux WiFi Scan{RS}")
        # In Termux, use termux-wifi-scaninfo
        try:
            result = subprocess.run(['termux-wifi-scaninfo'], capture_output=True, text=True, timeout=15)
            if result.stdout.strip():
                import json as j
                data = j.loads(result.stdout)
                if isinstance(data, list):
                    print(f"  {G}[✓] Found {len(data)} networks")
                    for net in data[:20]:
                        ssid = net.get('SSID', 'Hidden')
                        bssid = net.get('BSSID', 'N/A')
                        signal = net.get('RSSI', 'N/A')
                        print(f"  {C}  SSID: {W}{ssid[:20]:20} | {Y}BSSID: {bssid} | {M}RSSI: {signal}")
                    self.results['termux_wifi'] = data[:20]
                else:
                    print(f"  {Y}[i] Data: {result.stdout[:100]}")
            else:
                print(f"  {Y}[!] termux-wifi-scaninfo returned empty")
                print(f"  {Y}[i] Grant location permission in Termux settings")
        except FileNotFoundError:
            print(f"  {R}[!] termux-wifi-scaninfo not available")
            print(f"  {Y}[i] Install: pkg install termux-api")

    def wifi_analyzer(self):
        print(f"\n{G}[+] Method 3: Network Analysis{RS}")
        for net in self.networks:
            ssid = net.get('ssid', 'Unknown')
            security = net.get('security', net.get('WPA', 'Unknown'))

            # Detect weak security
            if 'Open' in security or not security:
                print(f"  {BR}[⚠] {ssid}: OPEN NETWORK (No security!){RS}")
            elif 'WEP' in security:
                print(f"  {R}[⚠] {ssid}: WEP (Crackable in minutes){RS}")
            elif 'WPA' in security:
                print(f"  {Y}[~] {ssid}: WPA/WPA2 (Moderate security){RS}")
            elif 'WPA3' in security:
                print(f"  {G}[✓] {ssid}: WPA3 (Strong security){RS}")

    def mac_analysis(self):
        print(f"\n{G}[+] Method 4: MAC Address Analysis (OUI Lookup){RS}")
        for net in self.networks:
            bssid = net.get('bssid', '')
            if bssid:
                oui = bssid[:8].replace(':', '')
                print(f"  {C}  BSSID: {bssid} → OUI: {oui}")
                # Try OUI lookup
                try:
                    r = requests.get(f"https://api.macvendors.com/{oui}", timeout=5)
                    if r.status_code == 200:
                        vendor = r.text
                        print(f"  {Y}    Vendor: {vendor}")
                except:
                    print(f"  {Y}    Vendor: Unknown")
                time.sleep(1)

    def deauth_warning(self):
        print(f"\n{G}[+] Method 5: Deauthentication Analysis{RS}")
        print(f"  {Y}[i] Networks vulnerable to deauth attack:")
        print(f"  {Y}[i] Use: aireplay-ng --deauth 10 -a <BSSID> wlan0mon")
        print(f"  {Y}[i] Requires monitor mode: airmon-ng start wlan0")
        for net in self.networks:
            security = net.get('security', '')
            if 'Open' not in security and security:
                print(f"  {R}  - {net.get('ssid','?')}: Can attempt deauth to capture handshake")

    def save_results(self):
        outfile = "wifi_scan_results.json"
        with open(outfile, 'w') as f:
            json.dump({'networks': self.networks, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{Y}[~]{'─'*50}{RS}")

        self.scan_linux()
        self.scan_termux()
        self.wifi_analyzer()
        self.mac_analysis()
        self.deauth_warning()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - WiFi Scanner Complete         ║")
        print(f"{BR}║  Networks found: {len(self.networks):20}    ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    scanner = WiFiScanner()
    scanner.run_all()

if __name__ == "__main__":
    main()
