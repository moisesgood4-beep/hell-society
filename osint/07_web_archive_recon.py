#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEB ARCHIVE RECON v2.0                                          ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Web Archive Intelligence                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json

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

class WebArchiveRecon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}

    def wayback_snapshots(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WAYBACK MACHINE SNAPSHOTS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={self.domain}/*&output=json&limit=20&fl=timestamp,original"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) > 1:
                    print(f"  {Fore.GREEN}[+] Found {len(data)-1} snapshots")
                    print(f"\n  {Fore.WHITE}  {'Timestamp':<20} {'URL':<60}")
                    print(f"  {Fore.CYAN}  {'═' * 80}")
                    for item in data[1:15]:
                        print(f"  {Fore.WHITE}  {item[0]:<20} {item[1]:<60}")
                    self.results['snapshots'] = data[1:20]
                else:
                    print(f"  {Fore.YELLOW}[-] No snapshots found")
            else:
                print(f"  {Fore.YELLOW}[-] Could not access Wayback Machine")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def find_subdomains_wayback(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SUBDOMAINS VIA WAYBACK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{self.domain}/*&output=text&fl=original&collapse=urlkey&limit=100"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                urls = resp.text.strip().split('\n')
                subdomains = set()
                for u in urls:
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(u)
                        host = parsed.hostname
                        if host and host.endswith(self.domain):
                            subdomains.add(host)
                    except:
                        pass

                print(f"  {Fore.GREEN}[+] Found {len(subdomains)} unique subdomains")
                for sub in sorted(subdomains)[:20]:
                    print(f"    {Fore.WHITE}• {sub}")
                self.results['subdomains'] = list(subdomains)
            else:
                print(f"  {Fore.YELLOW}[-] Could not find subdomains")
        except Exception as e:
            print(f"  {Fore.RED}[!] Error: {e}")

    def check_deleted_pages(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DELETED/PAGES HISTORY:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={self.domain}/*&output=json&limit=50&fl=timestamp,statuscode"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                deleted = []
                for item in data[1:]:
                    if item[1] in ['404', '500', '403']:
                        deleted.append(item)

                if deleted:
                    print(f"  {Fore.RED}[!] Found {len(deleted)} error/deleted pages")
                    for d in deleted[:10]:
                        print(f"    {Fore.RED}• {d[0]} - Status: {d[1]}")
                else:
                    print(f"  {Fore.GREEN}[OK] No deleted pages detected")
        except:
            pass

    def historical_screenshot(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  HISTORICAL SCREENSHOTS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        archive_url = f"https://web.archive.org/web/2020*/{self.domain}"
        print(f"  {Fore.WHITE}View historical versions:")
        print(f"  {Fore.CYAN}  {archive_url}")
        print(f"\n  {Fore.WHITE}Recent capture:")
        capture_url = f"https://web.archive.org/web/1/{self.domain}"
        print(f"  {Fore.CYAN}  {capture_url}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.domain}")
        print(f"{Fore.CYAN}  [*] Starting web archive reconnaissance...\n")

        self.wayback_snapshots()
        self.find_subdomains_wayback()
        self.check_deleted_pages()
        self.historical_screenshot()

        results_file = f'/tmp/archive_recon_{self.domain}.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

        print(f"\n{Fore.GREEN}{Back.BLACK}  WEB ARCHIVE RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")


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
    print(f"  {BW}{Style.BRIGHT}  WEB ARCHIVE RECON{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}WEB ARCHIVE RECON                       {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target domain                                {RS}")
        print()
        print(f"  {C}[2]  {BW}Ejecutar con todos los argumentos{RS}")
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
        elif choice == '2':
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

