#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  SUBDOMAIN ENUMERATOR v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Reconnaissance                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import time
import colorama
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import argparse
import dns.resolver

colorama.init(autoreset=True)

BANNER = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ███████╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗     {Fore.BLUE}║
║{Fore.CYAN}  ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗    {Fore.BLUE}║
║{Fore.CYAN}  ███████╗██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝    {Fore.BLUE}║
║{Fore.CYAN}  ╚════██║██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██╗    {Fore.BLUE}║
║{Fore.CYAN}  ███████║██║     ██║  ██║╚██████╔╝██║  ██║███████╗██║  ██║    {Fore.BLUE}║
║{Fore.CYAN}  ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   {Fore.BLUE}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Subdomain Enumerator v2.0                            {Fore.BLUE}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

SUBDOMAINS = [
    "www", "mail", "ftp", "smtp", "pop", "dns", "ns1", "ns2",
    "webmail", "cpanel", "admin", "panel", "dashboard", "portal",
    "api", "app", "dev", "staging", "test", "beta", "demo",
    "blog", "shop", "store", "m", "mobile", "cdn", "static",
    "assets", "media", "images", "img", "files", "upload",
    "db", "database", "mysql", "mongodb", "redis", "cache",
    "proxy", "vpn", "ssh", "sftp", "rtmp", "stream", "video",
    "live", "events", "chat", "support", "help", "docs",
    "wiki", "forum", "community", "social", "auth", "login",
    "sso", "oauth", "api2", "v1", "v2", "v3", "graphql",
    "ws", "websocket", "socket", "io", "push", "notifications",
    "email", "newsletter", "marketing", "crm", "erp",
    "hr", "intranet", "extranet", "partner", "vendor",
    "status", "health", "monitor", "metrics", "analytics",
    "tracking", "ads", "adserver", "pixel", "beacon",
    "backup", "mirror", "archive", "old", "legacy",
    "sandbox", "lab", "research", "science", "data",
    "analytics2", "warehouse", "etl", "pipeline",
    "payment", "checkout", "billing", "invoice", "receipt",
    "ssl", "cert", "certificate", "secure", "security",
    "waf", "firewall", "edge", "cloud", "aws", "azure",
    "gcp", "k8s", "kubernetes", "docker", "container",
    "registry", "artifact", "build", "ci", "cd",
    "jenkins", "gitlab", "github", "bitbucket", "repo",
    "jira", "confluence", "notion", "slack", "discord",
    "webhook", "callback", "redirect", "landing", "promo",
    "campaign", "newsletter2", "unsubscribe", "opt-out",
    "sitemap", "robots", "feed", "rss", "atom",
    "xml", "json", "csv", "export", "import", "migration",
    "staging2", "dev2", "test2", "qa", "uat", "pre-prod",
]

class SubdomainEnum:
    def __init__(self, domain, threads=50, timeout=5):
        self.domain = domain
        self.threads = threads
        self.timeout = timeout
        self.results = []

    def resolve_subdomain(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            try:
                response = requests.get(f"http://{full_domain}",
                    timeout=self.timeout, headers={
                        'User-Agent': 'Mozilla/5.0 HellSociety/2.0'
                    }, allow_redirects=False)
                status = response.status_code
            except:
                status = "N/A"

            result = {
                'subdomain': full_domain,
                'ip': ip,
                'status': status
            }
            return result
        except socket.gaierror:
            return None
        except Exception:
            return None

    def enumerate(self):
        total = len(SUBDOMAINS)
        print(f"{Fore.CYAN}  [*] Testing {total} subdomains with {self.threads} threads\n")

        completed = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.resolve_subdomain, sub): sub
                      for sub in SUBDOMAINS}

            for future in as_completed(futures):
                completed += 1
                progress = (completed / total) * 100
                bar_length = 40
                filled = int(bar_length * completed / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Found: {len(self.results)}", end="", flush=True)

                result = future.result()
                if result:
                    self.results.append(result)
                    print(f"\n  {Fore.GREEN}[+] {Fore.WHITE}{result['subdomain']} {Fore.CYAN}-> {result['ip']} [{result['status']}]")

    def print_results(self):
        if not self.results:
            print(f"\n\n{Fore.YELLOW}  [!] No subdomains found")
            return

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  ENUMERATION COMPLETE - {len(self.results)} SUBDOMAINS FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        for i, r in enumerate(self.results, 1):
            print(f"  {Fore.CYAN}[{i}] {Fore.WHITE}{r['subdomain']}")
            print(f"      {Fore.GREEN}IP: {r['ip']} | Status: {r['status']}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Subdomain Enumerator')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('--timeout', type=int, default=5, help='Request timeout')
    args = parser.parse_args()

    enum = SubdomainEnum(args.domain, args.threads, args.timeout)
    print(f"{Fore.CYAN}  [*] Domain: {Fore.WHITE}{args.domain}")
    print(f"{Fore.CYAN}  [*] Starting enumeration...\n")

    enum.enumerate()
    enum.print_results()

if __name__ == "__main__":
    main()
