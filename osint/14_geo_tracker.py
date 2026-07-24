#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  GEO TRACKER ADVANCED v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Geolocation & Tracking                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re
import time

colorama.init(autoreset=True)

BANNER = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}   ██████╗  █████╗ ██╗      ██████╗ ███████╗██████╗                {Fore.GREEN}║
║{Fore.CYAN}  ██╔════╝ ██╔══██╗██║     ██╔════╝ ██╔════╝██╔══██╗               {Fore.GREEN}║
║{Fore.CYAN}  ██║  ███╗███████║██║     ██║  ███╗█████╗  ██████╔╝               {Fore.GREEN}║
║{Fore.CYAN}  ██║   ██║██╔══██║██║     ██║   ██║██╔══╝  ██╔══██╗               {Fore.GREEN}║
║{Fore.CYAN}  ╚██████╔╝██║  ██║███████╗╚██████╔╝███████╗██║  ██║               {Fore.GREEN}║
║{Fore.CYAN}   ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝               {Fore.GREEN}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Geo Tracker Advanced v2.0                      {Fore.GREEN}║
╚══════════════════════════════════════════════════════════════════╝
"""

class GeoTracker:
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })

    def ip_geolocation(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  IP GEOLOCATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        ip = self.target

        # Validate IP format
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            print(f"  {Fore.YELLOW}[-] Not a valid IP address")
            return

        services = [
            ('IP-API', f'http://ip-api.com/json/{ip}'),
            ('IP-API Pro', f'https://ipapi.co/{ip}/json/'),
            ('IPStack', f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,lat,lon,timezone,isp,org,as'),
        ]

        for name, url in services:
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"\n  {Fore.GREEN}[+] {name} Results:")

                    if 'lat' in data and 'lon' in data:
                        print(f"    {Fore.WHITE}  IP: {data.get('ip', ip)}")
                        print(f"    {Fore.WHITE}  Country: {data.get('country', data.get('country_name', 'N/A'))}")
                        print(f"    {Fore.WHITE}  Region: {data.get('regionName', data.get('region', 'N/A'))}")
                        print(f"    {Fore.WHITE}  City: {data.get('city', 'N/A')}")
                        print(f"    {Fore.WHITE}  Lat: {data.get('lat')}")
                        print(f"    {Fore.WHITE}  Lon: {data.get('lon')}")
                        print(f"    {Fore.WHITE}  Timezone: {data.get('timezone', 'N/A')}")
                        print(f"    {Fore.WHITE}  ISP: {data.get('isp', 'N/A')}")
                        print(f"    {Fore.WHITE}  Org: {data.get('org', 'N/A')}")
                        print(f"    {Fore.WHITE}  AS: {data.get('as', 'N/A')}")

                        lat = data.get('lat')
                        lon = data.get('lon')
                        if lat and lon:
                            print(f"\n    {Fore.GREEN}  Google Maps: https://www.google.com/maps?q={lat},{lon}")
                            print(f"    {Fore.GREEN}  Street View: https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}")

                        self.results['geolocation'] = data
                        break
            except Exception as e:
                print(f"  {Fore.YELLOW}[-] {name}: {e}")

    def ip_reputation(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  IP REPUTATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        ip = self.target
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            return

        services = [
            ('AbuseIPDB', f'https://www.abuseipdb.com/check/{ip}'),
            ('VirusTotal', f'https://www.virustotal.com/gui/ip-address/{ip}'),
            ('Shodan', f'https://www.shodan.io/host/{ip}'),
            ('GreyNoise', f'https://viz.greynoise.io/ip/{ip}'),
            ('Censys', f'https://search.censys.io/hosts/{ip}'),
            ('AlienVault OTX', f'https://otx.alienvault.com/indicator/ip/{ip}'),
            ('Talos', f'https://talosintelligence.com/reputation_center/lookup?search={ip}'),
            ('Scamalytics', f'https://scamalytics.com/ip/{ip}'),
        ]

        for name, url in services:
            print(f"  {Fore.WHITE}  [{name}]")
            print(f"    {Fore.CYAN}  {url}")

    def traceroute(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TRACEROUTE:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target = self.target
        print(f"  {Fore.WHITE}  Running traceroute to {target}...")

        try:
            import subprocess
            result = subprocess.run(
                ['traceroute', '-n', target],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    print(f"    {Fore.WHITE}{line}")
                self.results['traceroute'] = result.stdout
            else:
                print(f"  {Fore.YELLOW}[-] Traceroute failed")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def whois_lookup(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WHOIS LOOKUP:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target = self.target
        try:
            import subprocess
            result = subprocess.run(
                ['whois', target],
                capture_output=True, text=True, timeout=15
            )
            if result.stdout:
                # Extract key info
                output = result.stdout
                fields = ['NetName', 'OrgName', 'City', 'State', 'Country', 'NetRange', 'CIDR']
                for field in fields:
                    for line in output.split('\n'):
                        if field in line:
                            print(f"    {Fore.WHITE}{line.strip()}")

                self.results['whois'] = output[:2000]
            else:
                print(f"  {Fore.YELLOW}[-] No WHOIS data")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def map_visualization(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  MAP VISUALIZATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if 'geolocation' in self.results:
            geo = self.results['geolocation']
            lat = geo.get('lat')
            lon = geo.get('lon')

            if lat and lon:
                print(f"  {Fore.GREEN}  Coordinates: {lat}, {lon}")
                print(f"\n  {Fore.CYAN}  Map Links:")
                print(f"    Google Maps: https://www.google.com/maps?q={lat},{lon}")
                print(f"    Google Earth: https://earth.google.com/web/@{lat},{lon},100a")
                print(f"    OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}")
                print(f"    Yandex Maps: https://yandex.com/maps/?pt={lon},{lat}&z=15")
                print(f"    Bing Maps: https://www.bing.com/maps?q={lat},{lon}")
                print(f"    Mapbox: https://www.mapbox.com/geocoding/#?q={lat},{lon}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Starting geo tracking...\n")

        # Check if it's an IP or domain
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', self.target):
            self.ip_geolocation()
            self.ip_reputation()
        else:
            # It's a domain - resolve IP first
            import socket
            try:
                ip = socket.gethostbyname(self.target)
                print(f"  {Fore.GREEN}[+] Resolved to: {ip}")
                self.target = ip
                self.ip_geolocation()
                self.ip_reputation()
            except:
                print(f"  {Fore.YELLOW}[-] Could not resolve domain")

        self.whois_lookup()
        self.map_visualization()

        # Save results
        with open('/tmp/geo_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/geo_results.json")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  GEO TRACKING COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Geo Tracker')
    parser.add_argument('-t', '--target', required=True, help='Target IP or domain')
    args = parser.parse_args()

    tracker = GeoTracker(args.target)
    tracker.run()
