#!/usr/bin/env python3
"""OSINT Framework - Central hub for all OSINT resources and tools."""
import os, sys
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    import requests
except: os.system("pip3 install colorama requests 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True); import requests

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;M=Fore.MAGENTA;BW=Style.BRIGHT+Fore.WHITE
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

TOOLS = {
    "1": ("Username Search", "https://whatsmyname.app/", "Search username across 400+ platforms"),
    "2": ("Email Lookup", "https://epieos.com/", "Reverse email lookup + Google/LinkedIn"),
    "3": ("Phone Lookup", "https://www.truecaller.com/", "Phone number reverse lookup"),
    "4": ("IP Lookup", "https://ipinfo.io/", "IP geolocation + ASN + organization"),
    "5": ("Domain Recon", "https://crt.sh/", "Certificate transparency log search"),
    "6": ("Social Media", "https://social-searcher.com/", "Search across all social media"),
    "7": ("Image Search", "https://tineye.com/", "Reverse image search"),
    "8": ("Wayback Machine", "https://web.archive.org/", "Web archive for deleted content"),
    "9": ("Shodan", "https://www.shodan.io/", "Internet-connected device search"),
    "10": ("Censys", "https://search.censys.io/", "Internet asset search engine"),
    "11": ("Have I Been Pwned", "https://haveibeenpwned.com/", "Breach database check"),
    "12": ("VirusTotal", "https://www.virustotal.com/", "File/URL/domain analysis"),
    "13": ("Google Dorks", "https://dorks.faisalahmed.me/", "Google dork generator"),
    "14": ("Maltego", "https://www.maltego.com/", "Link analysis and data mining"),
    "15": ("SpiderFoot", "https://www.spiderfoot.net/", "Automated OSINT collection"),
    "16": ("theHarvester", "https://github.com/laramies/theHarvester", "Email/subdomain/domain search"),
    "17": ("Recon-ng", "https://github.com/lanmaster53/recon-ng", "Full-featured recon framework"),
    "18": ("OSINT Framework", "https://osintframework.com/", "Visual OSINT tool directory"),
    "19": ("IntelX", "https://intelx.io/", "Data leak intelligence platform"),
    "20": ("DeHashed", "https://dehashed.com/", "Breach database search"),
}

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}OSINT Framework - Central Hub{RS}")
    print(f"{Y}{'─'*55}{RS}")
    
    print(f"\n  {Y}{'No.':<4} {BW}{'Tool':<25} {'Description'}{RS}")
    print(f"  {'─'*60}")
    for num, (name, url, desc) in TOOLS.items():
        color = G if int(num) % 3 == 1 else C if int(num) % 3 == 2 else Y
        print(f"  {color}[{num:>2}] {BW}{name:<24}{RS} {desc}")
    
    while True:
        try:
            choice = input(f"\n  {BG}root{RS}@{BR}hellsociety{RS}:{BG}~{RS}$ {BW}")
        except: break
        
        if choice in TOOLS:
            name, url, desc = TOOLS[choice]
            print(f"\n  {G}[+] Opening: {BW}{url}{RS}")
            print(f"  {C}[*] {desc}{RS}")
            try:
                import subprocess
                subprocess.Popen(['xdg-open', url])
            except:
                os.system(f"open {url} 2>/dev/null || echo 'Open manually: {url}'")
        elif choice == "0":
            break
        else:
            print(f"  {R}[!] Invalid option{RS}")
    
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")

if __name__ == "__main__": main()
