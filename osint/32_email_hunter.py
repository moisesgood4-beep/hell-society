#!/usr/bin/env python3
"""Email Hunter - Find emails associated with a domain using multiple methods."""
import os, sys, re, json
try:
    from colorama import init, Fore, Style; init(autoreset=True)
except: os.system("pip3 install colorama 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True)

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;BW=Style.BRIGHT+Fore.WHITE
BR=Style.BRIGHT+Fore.RED;BG=Style.BRIGHT+Fore.GREEN;BC=Style.BRIGHT+Fore.CYAN;RS=Style.RESET_ALL

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

def generate_emails(domain):
    prefixes = ["admin", "info", "contact", "support", "webmaster", "postmaster",
                "sales", "help", "office", "team", "hello", "noreply", "noreply-no",
                "abuse", "feedback", "press", "media", "jobs", "careers",
                "security", "legal", "privacy", "compliance", "billing"]
    emails = [f"{p}@{domain}" for p in prefixes]
    return emails

def check_email_pattern(domain):
    """Common email patterns based on company name"""
    name = domain.split('.')[0]
    patterns = [
        f"contact@{domain}", f"info@{domain}", f"hello@{domain}",
        f"support@{domain}", f"admin@{domain}", f"team@{domain}",
        f"careers@{domain}", f"jobs@{domain}", f"sales@{domain}",
        f"press@{domain}", f"media@{domain}", f"legal@{domain}",
        f"security@{domain}", f"abuse@{domain}", f"privacy@{domain}",
        f"{name}@{domain}", f"office@{domain}",
    ]
    return patterns

def search_google_dorks(domain):
    """Generate Google dorks for email discovery"""
    dorks = [
        f"@{domain} site:{domain}",
        f"\"@{domain}\" filetype:pdf",
        f"\"@{domain}\" filetype:doc OR filetype:docx",
        f"\"@{domain}\" filetype:xls OR filetype:xlsx",
        f"\"@{domain}\" filetype:ppt OR filetype:pptx",
        f"email @{domain} site:linkedin.com",
        f"email @{domain} site:twitter.com",
        f"\"@{domain}\" site:github.com",
    ]
    return dorks

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Email Hunter - Find emails for a domain{RS}")
    print(f"{Y}{'─'*55}{RS}")
    domain = input(f"\n{C}[*] Enter domain: {RS}").strip()
    if not domain: print(f"{R}[!] No domain provided{RS}"); sys.exit(1)
    
    print(f"\n{Y}[+] Method 1: Common prefixes...{RS}")
    emails = generate_emails(domain)
    for e in emails: print(f"  {G}[+] {BW}{e}{RS}")
    
    print(f"\n{Y}[+] Method 2: Pattern-based...{RS}")
    patterns = check_email_pattern(domain)
    for p in patterns: print(f"  {G}[+] {BW}{p}{RS}")
    
    print(f"\n{Y}[+] Method 3: Google Dorks...{RS}")
    dorks = search_google_dorks(domain)
    for i, d in enumerate(dorks, 1): print(f"  {C}[{i}] {BW}{d}{RS}")
    
    print(f"\n{BG}[*] Total emails generated: {len(emails) + len(patterns)}{RS}")
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
