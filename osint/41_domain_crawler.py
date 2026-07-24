#!/usr/bin/env python3
"""Domain Crawler - Extract all links, emails, and metadata from a domain."""
import os, sys
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse
except: os.system("pip3 install colorama requests beautifulsoup4 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True); import requests; from bs4 import BeautifulSoup; from urllib.parse import urljoin, urlparse

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;BW=Style.BRIGHT+Fore.WHITE
BR=Style.BRIGHT+Fore.RED;BG=Style.BRIGHT+Fore.GREEN;RS=Style.RESET_ALL

BANNER = f"""{BR}⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄{RS}
  {Y}  Created by: HELL SOCIETY{RS}"""

DISCLAIMER = f"{R}╔══════════════════════════════════════════════════════════════════╗\n║ {BW}DISCLAIMER: Developers assume no liability and are not            ║\n║ {BW}responsible for any misuse or damage caused.                      ║\n║ {BW}Only use for educational purposes!!                               ║\n║ {BG}Attacking targets without mutual consent is illegal!!{RS}  {R}║\n╚══════════════════════════════════════════════════════════════════╝{RS}"

def clear(): os.system('clear' if os.name!='nt' else 'cls')

def crawl(target, max_pages=50):
    visited = set()
    emails = set()
    links = set()
    to_visit = {target}
    domain = urlparse(target).netloc
    
    print(f"  {Y}[+] Crawling: {BW}{target}{RS}")
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited: continue
        visited.add(url)
        
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent":"HellSociety/1.0"})
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find emails
            import re
            text = soup.get_text()
            found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            emails.update(found_emails)
            
            # Find links
            for a in soup.find_all('a', href=True):
                href = urljoin(url, a['href'])
                if domain in href:
                    links.add(href)
                    to_visit.add(href)
            
            print(f"  {G}[+] Crawled: {len(visited)}/{max_pages} - Emails: {len(emails)} - Links: {len(links)}{RS}")
        except: pass
    
    return emails, links

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Domain Crawler{RS}")
    print(f"{Y}{'─'*55}{RS}")
    target = input(f"\n{C}[*] Enter URL to crawl: {RS}").strip()
    if not target: sys.exit(1)
    if not target.startswith("http"): target = "https://" + target
    
    max_pages = int(input(f"{C}[*] Max pages (default 50): {RS}").strip() or "50")
    
    emails, links = crawl(target, max_pages)
    
    print(f"\n{Y}[+] Found {len(emails)} emails:{RS}")
    for e in sorted(emails): print(f"  {G}[+] {BW}{e}{RS}")
    
    print(f"\n{Y}[+] Found {len(links)} internal links{RS}")
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
