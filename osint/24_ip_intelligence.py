#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - IP Intelligence & Tracking                     ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests, socket
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

BANNER=f"""{BR}
██╗███╗   ██╗██╗   ██╗████████╗███████╗██████╗
██║████╗  ██║██║   ██║╚══██╔══╝██╔════╝██╔══██╗
██║██╔██╗ ██║██║   ██║   ██║   █████╗  ██████╔╝
██║██║╚██╗██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
██║██║ ╚████║╚██████╔╝   ██║   ███████╗██║  ██║
╚═╝╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
{Y}  Created by: HELL SOCIETY{RS}
"""

class IPIntelligence:
    def __init__(self, ip):
        self.ip = ip
        self.results = {}

    def geolocation(self):
        print(f"\n{G}[+] Method 1: IP Geolocation{RS}")
        try:
            r = requests.get(f"http://ip-api.com/json/{self.ip}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                fields = ['country', 'regionName', 'city', 'zip', 'lat', 'lon', 'timezone', 'isp', 'org', 'as']
                for f in fields:
                    val = data.get(f, 'N/A')
                    print(f"  {C}[{f}] {W}{val}")
                self.results['geo'] = data
                print(f"\n  {Y}[i] Google Maps: https://www.google.com/maps?q={data.get('lat','')},{data.get('lon','')}")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def shodan_lookup(self):
        print(f"\n{G}[+] Method 2: Shodan Intelligence{RS}")
        print(f"  {Y}[i] Shodan: https://www.shodan.io/host/{self.ip}")
        try:
            r = requests.get(f"https://internetdb.shodan.io/{self.ip}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {G}[✓] Ports: {data.get('ports', [])}")
                print(f"  {G}[✓] Vulns: {data.get('vulns', [])}")
                print(f"  {G}[✓] Tags: {data.get('tags', [])}")
                self.results['shodan'] = data
            else:
                print(f"  {Y}[!] No Shodan data")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def dns_recon(self):
        print(f"\n{G}[+] Method 3: DNS Reverse Lookup{RS}")
        try:
            hostname, _, _ = socket.gethostbyaddr(self.ip)
            print(f"  {G}[✓] Hostname: {hostname}")
            self.results['hostname'] = hostname
        except socket.herror:
            print(f"  {Y}[!] No reverse DNS")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def port_scan(self):
        print(f"\n{G}[+] Method 4: Quick Port Scan{RS}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 993, 995,
                       1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        open_ports = []
        print(f"  {Y}[i] Scanning {len(common_ports)} common ports...")
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"  {G}[OPEN] Port {port}")
                else:
                    print(f"  {R}[CLOSED] Port {port}")
            except:
                print(f"  {R}[CLOSED] Port {port}")
            finally:
                sock.close()
        self.results['ports'] = open_ports

    def ssl_cert(self):
        print(f"\n{G}[+] Method 5: SSL Certificate Analysis{RS}")
        try:
            import ssl, ssl
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.ip) as ssock:
                ssock.connect((self.ip, 443))
                cert = ssock.getpeercert()
                print(f"  {G}[✓] Certificate found")
                print(f"  {C}  Subject: {cert.get('subject', 'N/A')}")
                print(f"  {C}  Issuer: {cert.get('issuer', 'N/A')}")
                print(f"  {C}  Version: {cert.get('version', 'N/A')}")
                self.results['ssl'] = str(cert)
        except Exception as e:
            print(f"  {Y}[!] No SSL on port 443 or error: {e}")

    def threat_intel(self):
        print(f"\n{G}[+] Method 6: Threat Intelligence{RS}")
        services = [
            ('AbuseIPDB', f"https://www.abuseipdb.com/check/{self.ip}"),
            ('VirusTotal', f"https://www.virustotal.com/gui/ip-address/{self.ip}"),
            ('ThreatCrowd', f"https://threatcrowd.org/ip.php?ip={self.ip}"),
            ('AlienVault', f"https://otx.alienvault.com/indicator/ip/{self.ip}"),
            ('IPVoid', f"https://www.ipvoid.com/ip-blacklist-check/{self.ip}"),
            ('Cisco Talos', f"https://talosintelligence.com/reputation_center/lookup?search={self.ip}"),
        ]
        for name, url in services:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['threat_intel'] = services

    def save_results(self):
        outfile = f"ip_intel_{self.ip}.json"
        with open(outfile, 'w') as f:
            json.dump({'ip': self.ip, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target IP: {W}{self.ip}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.geolocation()
        self.shodan_lookup()
        self.dns_recon()
        self.port_scan()
        self.ssl_cert()
        self.threat_intel()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - IP Intelligence Complete      ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='Target IP address')
    args = parser.parse_args()
    intel = IPIntelligence(args.target)
    intel.run_all()

if __name__ == "__main__":
    main()
