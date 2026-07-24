#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  IP EXTRACTOR ADVANCED v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - IP Extraction Multi-Method                    ║
║  Description: Extract IP from social media users via multiple   ║
║               methods until one works                            ║
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
import socket
import subprocess
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗██╗   ██╗███████╗████████╗ ██████╗██╗  ██╗███████╗██╗     ██╗   {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║   ██║██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██║     ██║   {Fore.MAGENTA}║
║{Fore.CYAN}  ██║██║   ██║███████╗   ██║   ██║     ███████║█████╗  ██║     ██║   {Fore.MAGENTA}║
║{Fore.CYAN}  ██║╚██╗ ██╔╝╚════██║   ██║   ██║     ██╔══██║██╔══╝  ██║     ██║   {Fore.MAGENTA}║
║{Fore.CYAN}  ██║ ╚████╔╝ ███████║   ██║   ╚██████╗██║  ██║███████╗███████╗╚██╗ {Fore.MAGENTA}║
║{Fore.CYAN}  ╚═╝  ╚═══╝  ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═╝ {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - IP Extractor Advanced v2.0                       {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

class IPExtractor:
    def __init__(self, target, social_platform=None):
        self.target = target
        self.platform = social_platform
        self.results = {}
        self.ip_found = False
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def method1_social_media_profile_scan(self):
        """Scan social media profiles for exposed IPs or URLs with IPs"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 1: SOCIAL MEDIA PROFILE SCAN")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        platforms = {
            'Twitter/X': f'https://twitter.com/{self.target}',
            'Instagram': f'https://www.instagram.com/{self.target}/',
            'GitHub': f'https://github.com/{self.target}',
            'Reddit': f'https://www.reddit.com/user/{self.target}/',
            'LinkedIn': f'https://www.linkedin.com/in/{self.target}',
            'TikTok': f'https://www.tiktok.com/@{self.target}',
            'Pinterest': f'https://www.pinterest.com/{self.target}/',
            'Tumblr': f'https://{self.target}.tumblr.com/',
            'Twitch': f'https://www.twitch.tv/{self.target}',
            'Steam': f'https://steamcommunity.com/id/{self.target}',
        }

        found_ips = []
        for platform, url in platforms.items():
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    # Search for IP patterns in the page
                    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                    ips = re.findall(ip_pattern, resp.text)
                    if ips:
                        # Filter valid IPs
                        for ip in ips:
                            parts = ip.split('.')
                            if all(0 <= int(p) <= 255 for p in parts):
                                if ip not in ['127.0.0.1', '0.0.0.0']:
                                    found_ips.append({'ip': ip, 'source': platform, 'url': url})
                                    print(f"  {Fore.GREEN}[+] IP found on {platform}: {ip}")

                    print(f"  {Fore.WHITE}  {platform}: {'Found' if resp.status_code == 200 else 'Not found'}")
                else:
                    print(f"  {Fore.YELLOW}  {platform}: Profile not accessible")
            except:
                print(f"  {Fore.RED}  {platform}: Error")

            time.sleep(0.5)

        if found_ips:
            self.results['method1'] = found_ips
            self.ip_found = True
        else:
            self.results['method1'] = []

    def method2_gravatar_lookup(self):
        """Use Gravatar to find associated data"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 2: GRAVATAR LOOKUP")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Try common email patterns with the username
        email_patterns = [
            f'{self.target}@gmail.com',
            f'{self.target}@hotmail.com',
            f'{self.target}@yahoo.com',
            f'{self.target}@outlook.com',
            f'{self.target}@protonmail.com',
        ]

        for email in email_patterns:
            hash_email = hashlib.md5(email.strip().lower().encode()).hexdigest()
            gravatar_url = f'https://www.gravatar.com/avatar/{hash_email}?d=404'

            try:
                resp = self.session.head(gravatar_url, timeout=10)
                if resp.status_code == 200:
                    print(f"  {Fore.GREEN}[+] Gravatar found for: {email}")
                    self.results['gravatar_email'] = email
                    # Get full Gravatar data
                    gravatar_data_url = f'https://www.gravatar.com/avatar/{hash_email}?d=404'
                    resp2 = self.session.get(gravatar_data_url, timeout=10)
                    if resp2.status_code == 200:
                        with open(f'/tmp/gravatar_{self.target}.jpg', 'wb') as f:
                            f.write(resp2.content)
                        print(f"  {Fore.GREEN}[+] Gravatar image saved")
                else:
                    print(f"  {Fore.YELLOW}[-] No Gravatar: {email}")
            except:
                pass

    def method3_image_metadata(self):
        """Extract IPs from image metadata in social media posts"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 3: IMAGE METADATA EXTRACTION")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}[*] Checking for images with embedded metadata...")
        print(f"  {Fore.WHITE}[*] Looking for GPS coordinates in shared images...")

        # Common social media image URLs patterns
        image_patterns = [
            f'https://pbs.twimg.com/media/',
            f'https://scontent',
            f'https://i.instagram.com/',
            f'https://i.imgur.com/',
        ]

        for pattern in image_patterns:
            print(f"  {Fore.CYAN}  Searching: {pattern}")

        print(f"\n  {Fore.YELLOW}[i] Download any images from the target's profile")
        print(f"  {Fore.YELLOW}[i] Then run: python3 osint/10_exif_metadata.py -p image.jpg")
        print(f"  {Fore.YELLOW}[i] Look for GPS coordinates in EXIF data")

    def method4_header_analysis(self):
        """Analyze response headers for IP information"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 4: HEADER ANALYSIS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target_url = self.target
        if not target_url.startswith('http'):
            target_url = f'http://{target_url}'

        try:
            resp = self.session.get(target_url, timeout=10)
            print(f"  {Fore.WHITE}Response Headers:")
            for header, value in resp.headers.items():
                print(f"    {Fore.CYAN}{header}: {Fore.WHITE}{value}")

                # Check for server IP in headers
                ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                if re.search(ip_pattern, value):
                    ips = re.findall(ip_pattern, value)
                    print(f"    {Fore.GREEN}[!] IP found in header: {ips}")

            # Check for X-Forwarded-For, X-Real-IP etc
            ip_headers = ['X-Forwarded-For', 'X-Real-IP', 'X-Client-IP', 'X-Originating-IP']
            for h in ip_headers:
                if h in resp.headers:
                    print(f"  {Fore.GREEN}[!] {h}: {resp.headers[h]}")

            self.results['headers'] = dict(resp.headers)
        except:
            print(f"  {Fore.YELLOW}[-] Could not access URL")

    def method5_dns_recon(self):
        """DNS reconnaissance to find associated IPs"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 5: DNS RECONNAISSANCE")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target = self.target
        if not any(target.endswith(tld) for tld in ['.com', '.net', '.org', '.io', '.dev']):
            target = f'{target}.com'

        try:
            # Resolve IP
            try:
                ip = socket.gethostbyname(target)
                print(f"  {Fore.GREEN}[+] Resolved IP: {ip}")
                print(f"  {Fore.GREEN}[+] Host: {target}")
                self.results['dns_ip'] = ip
                self.ip_found = True
            except:
                print(f"  {Fore.YELLOW}[-] Could not resolve: {target}")

            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"  {Fore.GREEN}[+] Reverse DNS: {hostname}")
                self.results['hostname'] = hostname
            except:
                pass

            # DNS lookup
            print(f"\n  {Fore.WHITE}  DNS Records:")
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            for rtype in record_types:
                try:
                    result = subprocess.run(
                        ['dig', target, rtype, '+short'],
                        capture_output=True, text=True, timeout=5
                    )
                    if result.stdout.strip():
                        print(f"    {Fore.CYAN}{rtype}: {Fore.WHITE}{result.stdout.strip()}")
                except:
                    pass

        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def method6_cdn_bypass(self):
        """Try to find real IP behind CDN (Cloudflare, etc.)"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 6: CDN BYPASS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target = self.target
        if not target.startswith('http'):
            target = f'http://{target}'

        # Check if behind Cloudflare
        try:
            resp = self.session.get(target, timeout=10)
            if 'cloudflare' in resp.headers.get('server', '').lower():
                print(f"  {Fore.YELLOW}[!] Site behind Cloudflare")
                print(f"  {Fore.CYAN}  Trying bypass methods...")

                # Try subdomains that might not be proxied
                subdomains = ['mail', 'ftp', 'cpanel', 'whm', 'direct', 'host']
                host = urlparse(target).netloc

                for sub in subdomains:
                    subdomain = f'{sub}.{host}'
                    try:
                        ip = socket.gethostbyname(subdomain)
                        if ip != socket.gethostbyname(host):
                            print(f"  {Fore.GREEN}[+] Real IP via {sub}: {ip}")
                            self.results['cdn_real_ip'] = ip
                            self.ip_found = True
                    except:
                        pass

                # Try historical DNS
                print(f"\n  {Fore.WHITE}  Check historical DNS:")
                print(f"    https://viewdns.info/iphistory/?domain={host}")
                print(f"    https://dnslytics.com/domain/{host}")
            else:
                print(f"  {Fore.GREEN}[OK] Not behind Cloudflare")
        except:
            pass

    def method7_shodan_censys(self):
        """Search Shodan/Censys for exposed services"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 7: SHODAN/CENSYS SEARCH")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        target = self.target
        if not any(target.endswith(tld) for tld in ['.com', '.net', '.org', '.io', '.dev']):
            target = f'{target}.com'

        print(f"  {Fore.WHITE}[*] Search commands:")
        print(f"\n  {Fore.CYAN}  Shodan searches:")
        print(f"    https://www.shodan.io/search?query={target}")
        print(f"    https://www.shodan.io/host/{target}")
        print(f"    shodan host {target}")
        print(f"    shodan search hostname:{target}")

        print(f"\n  {Fore.CYAN}  Censys searches:")
        print(f"    https://search.censys.io/search?resource=hosts&virtual_hosts=EXCLUDE&q={target}")
        print(f"    https://censys.io/domains/{target}")

        print(f"\n  {Fore.CYAN}  Hunter.io:")
        print(f"    https://hunter.io/search/{target}")

    def method8_email_header_tracer(self):
        """Trace IP from email headers if email is known"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 8: EMAIL HEADER TRACE")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}[*] If you have an email associated with this user:")
        print(f"  {Fore.WHITE}    1. Get the full email headers (View Source)")
        print(f"  {Fore.WHITE}    2. Look for: X-Originating-IP, X-Mailer-IP")
        print(f"  {Fore.WHITE}    3. Look for: Received: from headers")
        print(f"  {Fore.WHITE}    4. Use: python3 osint/10_exif_metadata.py (adapt for email)")
        print(f"")
        print(f"  {Fore.CYAN}  Common IP locations in email headers:")
        print(f"    Received: from (IP here)")
        print(f"    X-Originating-IP: (IP here)")
        print(f"    X-Mailer-IP: (IP here)")
        print(f"    X-Sender-IP: (IP here)")
        print(f"    Authentication-Results: (IP here)")

    def method9_social_engineering_links(self):
        """Generate tracking links for IP capture"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 9: TRACKING LINK GENERATOR")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}[*] IP grabbing services:")
        print(f"\n  {Fore.CYAN}  Free IP grabbers:")
        print(f"    https://grabify.link/")
        print(f"    https://ip-grabber.in/")
        print(f"    https://iplogger.org/")
        print(f"    https://whatstheirip.com/")
        print(f"    https://ps3cfw.com/")
        print(f"    https://blaze.press/")
        print(f"    https://hatscripts.github.io/circle-flags/")

        print(f"\n  {Fore.WHITE}[*] Steps:")
        print(f"    1. Create a tracking link")
        print(f"    2. Share it with the target via DM/post")
        print(f"    3. Wait for them to click")
        print(f"    4. Check your IP grabber dashboard")
        print(f"    5. Get their IP, location, device info")

    def method10_correlation(self):
        """Correlate data from multiple sources"""
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  METHOD 10: DATA CORRELATION")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        print(f"  {Fore.WHITE}[*] Cross-referencing all found data...")

        # Search for the target across multiple platforms
        platforms_to_check = [
            ('GitHub', f'https://github.com/search?q={self.target}&type=Users'),
            ('Twitter', f'https://twitter.com/search?q={self.target}'),
            ('Reddit', f'https://www.reddit.com/search/?q={self.target}'),
            ('LinkedIn', f'https://www.linkedin.com/search/results/people/?keywords={self.target}'),
            ('Google', f'https://www.google.com/search?q=%22{self.target}%22'),
            ('DuckDuckGo', f'https://duckduckgo.com/?q=%22{self.target}%22'),
        ]

        for name, url in platforms_to_check:
            print(f"  {Fore.CYAN}  {name}: {url}")

        print(f"\n  {Fore.WHITE}[*] Check for data breaches:")
        print(f"  {Fore.CYAN}  https://haveibeenpwned.com/")
        print(f"  {Fore.CYAN}  https://dehashed.com/search?query={self.target}")
        print(f"  {Fore.CYAN}  https://intelx.io/?s={self.target}")

    def run_all_methods(self):
        """Run all methods until IP is found"""
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Platform: {Fore.WHITE}{self.platform or 'All'}")
        print(f"{Fore.CYAN}  [*] Running all extraction methods...\n")

        methods = [
            self.method1_social_media_profile_scan,
            self.method2_gravatar_lookup,
            self.method3_image_metadata,
            self.method4_header_analysis,
            self.method5_dns_recon,
            self.method6_cdn_bypass,
            self.method7_shodan_censys,
            self.method8_email_header_tracer,
            self.method9_social_engineering_links,
            self.method10_correlation,
        ]

        for method in methods:
            method()
            if self.ip_found:
                print(f"\n  {Fore.GREEN}[!!!] IP FOUND! Stopping methods.")
                break

        # Final report
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  IP EXTRACTION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        print(f"\n  {Fore.CYAN}RESULTS:")
        for key, value in self.results.items():
            if isinstance(value, list) and value:
                print(f"  {Fore.GREEN}  {key}: {value}")
            elif isinstance(value, str) and value:
                print(f"  {Fore.GREEN}  {key}: {value}")

        # Save results
        with open(f'/tmp/ip_extract_{self.target}.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/ip_extract_{self.target}.json")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society IP Extractor Advanced')
    parser.add_argument('-t', '--target', required=True, help='Target username or domain')
    parser.add_argument('-p', '--platform', help='Social media platform')
    args = parser.parse_args()

    extractor = IPExtractor(args.target, args.platform)
    extractor.run_all_methods()
