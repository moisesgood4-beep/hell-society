#!/usr/bin/env python3
"""Ultimate Doxing Framework - All-in-one doxing toolkit."""
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

def lookup_email(email):
    print(f"\n{M}[+] Checking email: {BW}{email}{RS}")
    # HIBP check
    try:
        r = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{email}", headers={"User-Agent":"HellSociety/1.0"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"  {G}[+] Found in {len(data.get('Breaches', []))} breaches{RS}")
            for b in data.get('Breaches', [])[:5]:
                print(f"    {R}├─ {b.get('Name','?')} ({b.get('BreachDate','?')}){RS}")
        elif r.status_code == 404:
            print(f"  {G}[+] No breaches found{RS}")
    except: print(f"  {Y}[!] HIBP check failed{RS}")

def lookup_username(username):
    print(f"\n{M}[+] Searching username: {BW}{username}{RS}")
    platforms = {
        "GitHub": f"https://api.github.com/users/{username}",
        "Twitter": f"https://x.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "Medium": f"https://medium.com/@{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "CodePen": f"https://codepen.io/{username}",
        "HackerRank": f"https://hackerrank.com/{username}",
        "Dev.to": f"https://dev.to/{username}",
        "Quora": f"https://quora.com/profile/{username}",
        "Behance": f"https://behance.net/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
    }
    found = 0
    for platform, url in platforms.items():
        try:
            r = requests.head(url, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                print(f"  {G}[+] {platform}: {url}{RS}")
                found += 1
        except: pass
    print(f"\n  {BG}[*] Found on {found}/{len(platforms)} platforms{RS}")

def lookup_phone(phone):
    print(f"\n{M}[+] Phone lookup: {BW}{phone}{RS}")
    try:
        r = requests.get(f"https://api.phoneverification.online/?phone={phone}&key=demo", timeout=10)
        if r.status_code == 200:
            data = r.json()
            for k,v in data.items():
                if v: print(f"  {C}{k}: {BW}{v}{RS}")
    except:
        print(f"  {C}[+] Country: Detected from number format{RS}")
        print(f"  {C}[+] Search on: https://www.truecaller.com/search/{phone}{RS}")

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Ultimate Doxing Framework v2.0{RS}")
    print(f"{Y}{'─'*55}{RS}")
    
    while True:
        print(f"\n  {R}[1] {BW}Email Investigation{RS}")
        print(f"  {G}[2] {BW}Username Recon{RS}")
        print(f"  {C}[3] {BW}Phone Lookup{RS}")
        print(f"  {M}[4] {BW}IP Lookup{RS}")
        print(f"  {Y}[5] {BW}Domain Recon{RS}")
        print(f"  {R}[0] {BW}Exit{RS}")
        
        try:
            choice = input(f"\n  {BG}root{RS}@{BR}hellsociety{RS}:{BG}~{RS}$ {BW}")
        except: break
        
        if choice == "0": break
        elif choice == "1":
            email = input(f"  {C}[*] Email: {RS}")
            if email: lookup_email(email)
        elif choice == "2":
            user = input(f"  {C}[*] Username: {RS}")
            if user: lookup_username(user)
        elif choice == "3":
            phone = input(f"  {C}[*] Phone: {RS}")
            if phone: lookup_phone(phone)
        elif choice == "4":
            ip = input(f"  {C}[*] IP: {RS}")
            if ip:
                try:
                    r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
                    data = r.json()
                    for k,v in data.items():
                        print(f"  {C}{k:15}: {BW}{v}{RS}")
                except: print(f"  {R}[!] Lookup failed{RS}")
        elif choice == "5":
            domain = input(f"  {C}[*] Domain: {RS}")
            if domain:
                print(f"\n  {Y}[+] WHOIS: whois {domain}{RS}")
                print(f"  {Y}[+] DNS: nslookup {domain}{RS}")
                print(f"  {Y}[+] SSL: openssl s_client -connect {domain}:443{RS}")
                print(f"  {Y}[+] Headers: curl -I https://{domain}{RS}")
        else:
            print(f"  {R}[!] Invalid option{RS}")
    
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")

if __name__ == "__main__": main()
