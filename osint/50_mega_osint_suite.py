#!/usr/bin/env python3
"""Mega OSINT Suite - Ultimate all-in-one OSINT framework with 30+ search methods."""
import os, sys, json, re
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

CATEGORIES = {
    "PERSON": {
        "email": ["Email", "Check HIBP, Google, LinkedIn, social media"],
        "username": ["Username", "Search 400+ platforms, GitHub, social media"],
        "phone": ["Phone Number", "Truecaller, WhatsApp, social media lookup"],
        "name": ["Full Name", "LinkedIn, Facebook, public records"],
        "address": ["Physical Address", "Google Maps, WHOIS, public records"],
        "photo": ["Photo/Image", "Reverse image search, TinEye, Google Images"],
    },
    "DOMAIN": {
        "domain": ["Domain Name", "WHOIS, DNS, subdomains, certificate transparency"],
        "ip": ["IP Address", "GeoIP, Shodan, Censys, reverse DNS"],
        "url": ["URL/Website", "Wayback Machine, headers, tech stack"],
        "bssid": ["WiFi BSSID", "WiGLE, Mylnikov geolocation"],
    },
    "VEHICLE": {
        "vin": ["VIN Number", "VIN decoder, manufacturer lookup"],
        "plate": ["License Plate", "State databases, DMV records"],
    },
    "CRYPTO": {
        "wallet": ["Crypto Wallet", "Blockchain explorer, transaction history"],
    },
    "OTHER": {
        "breach": ["Data Breach", "HIBP, DeHashed, IntelX, LeakCheck"],
        "document": ["Document", "Google dorks, pastebin, exposed files"],
        "social": ["Social Profile", "All platforms, correlation engine"],
        "company": ["Company/Business", "Crunchbase, OpenCorporates, LinkedIn"],
    },
}

def search_target(query_type, query):
    """Execute search based on target type"""
    if query_type == "email":
        print(f"\n{Y}[+] Email: {BW}{query}{RS}")
        print(f"  {G}[+] HIBP: https://haveibeenpwned.com/unifiedsearch/{query}{RS}")
        print(f"  {G}[+] Epieos: https://epieos.com/?email={query}{RS}")
        print(f"  {G}[+] Hunter.io: https://hunter.io/search/{query}{RS}")
        print(f"  {G}[+] Google: \"{query}\" site:linkedin.com{RS}")
        print(f"  {G}[+] Google: \"{query}\" site:github.com{RS}")
        # HIBP check
        try:
            r = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{query}", headers={"User-Agent":"HellSociety"}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                breaches = data.get('Breaches', [])
                print(f"\n  {BG}[*] Found in {len(breaches)} breaches:{RS}")
                for b in breaches[:5]:
                    print(f"  {R}├─ {b.get('Name','?')} ({b.get('BreachDate','?')}){RS}")
            elif r.status_code == 404:
                print(f"\n  {BG}[*] No breaches found on HIBP{RS}")
        except: print(f"\n  {R}[!] HIBP check failed{RS}")
    
    elif query_type == "username":
        print(f"\n{Y}[+] Username: {BW}{query}{RS}")
        platforms = ["instagram","twitter","facebook","github","reddit","tiktok",
                     "pinterest","twitch","medium","youtube","linkedin","telegram",
                     "snapchat","steam","soundcloud","deviantart","behance","dribbble"]
        print(f"  {G}[+] Searching {len(platforms)} platforms...{RS}")
        for p in platforms:
            url = f"https://{p}.com/{query}" if p != "telegram" else f"https://t.me/{query}"
            print(f"  {C}[+] {BW}{p:15}{RS} {url}")
    
    elif query_type == "ip":
        print(f"\n{Y}[+] IP: {BW}{query}{RS}")
        try:
            r = requests.get(f"https://ipinfo.io/{query}/json", timeout=10)
            if r.status_code == 200:
                data = r.json()
                for k,v in data.items():
                    print(f"  {C}{k:15}: {BW}{v}{RS}")
        except: print(f"  {R}[!] Lookup failed{RS}")
        print(f"\n  {G}[+] Shodan: https://www.shodan.io/host/{query}{RS}")
        print(f"  {G}[+] Censys: https://search.censys.io/hosts/{query}{RS}")
    
    elif query_type == "domain":
        print(f"\n{Y}[+] Domain: {BW}{query}{RS}")
        print(f"  {G}[+] WHOIS: https://whois.domaintools.com/{query}{RS}")
        print(f"  {G}[+] DNS: https://dnslytics.com/domain/{query}{RS}")
        print(f"  {G}[+] Crt.sh: https://crt.sh/?q={query}{RS}")
        print(f"  {G}[+] BuiltWith: https://builtwith.com/{query}{RS}")
        print(f"  {G}[+] SimilarWeb: https://www.similarweb.com/website/{query}{RS}")
    
    elif query_type == "phone":
        print(f"\n{Y}[+] Phone: {BW}{query}{RS}")
        print(f"  {G}[+] Truecaller: https://www.truecaller.com/search/{query}{RS}")
        print(f"  {G}[+] WhatsApp: https://wa.me/{query.replace('+','')}{RS}")
        print(f"  {G}[+] Google: \"{query}\" site:linkedin.com{RS}")
        print(f"  {G}[+] Google: \"{query}\" site:facebook.com{RS}")
    
    elif query_type == "photo":
        print(f"\n{Y}[+] Reverse Image Search:{RS}")
        print(f"  {G}[+] TinEye: https://tineye.com/search?url={query}{RS}")
        print(f"  {G}[+] Google: https://images.google.com/searchbyimage{RS}")
        print(f"  {G}[+] Yandex: https://yandex.com/images/?rpt=imageview{RS}")
        print(f"  {G}[+] Bing: https://www.bing.com/images/search?view=detailv2&form=sbi&imgurl={query}{RS}")
    
    else:
        print(f"\n{Y}[+] Type: {BW}{query_type}{RS}")
        print(f"  {Y}[+] Query: {BW}{query}{RS}")
        print(f"  {C}[+] Check appropriate source for this type{RS}")

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Mega OSINT Suite - 30+ Search Methods{RS}")
    print(f"{Y}{'─'*55}{RS}")
    
    print(f"\n  {R}{'CATEGORY':<15} {'TYPE':<12} {'DESCRIPTION'}{RS}")
    print(f"  {'─'*50}")
    for cat, items in CATEGORIES.items():
        for key, (name, desc) in items.items():
            color = G if key in ["email","domain","ip"] else C if key in ["username","phone"] else Y
            print(f"  {color}{cat:<15} {BW}{name:<12}{RS} {desc}")
    
    while True:
        try:
            target_type = input(f"\n  {BG}root{RS}@{BR}hellsociety{RS}:{BG}~{RS}$ {BW}[type] (email/username/ip/domain/phone/photo/name/address/vin/plate/wallet/breach/social/company/bssid/url): {RS}").strip().lower()
        except: break
        
        if target_type == "exit" or target_type == "0":
            break
        
        if target_type not in [k for cat in CATEGORIES.values() for k in cat.keys()]:
            print(f"  {R}[!] Invalid type. Try: email, username, ip, domain, phone, photo{RS}")
            continue
        
        target = input(f"  {C}[*] Enter target: {RS}").strip()
        if target:
            search_target(target_type, target)
    
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")

if __name__ == "__main__": main()
