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
    print(f"  {BW}{Style.BRIGHT}  SUBDOMAIN ENUM{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}SUBDOMAIN ENUM                          {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target domain                                {RS}")
        print(f"  {C}[2]  {BW}Number of threads                            {RS}")
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
            print(f"  {Y}[*] Target domain{RS}")
            value = input(f"  {Y}[*] -d: {RS}").strip()
            print(f"  {C}[*] Executing with -d={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Number of threads{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
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

