#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Phone Number OSINT Toolkit                      ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

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

class PhoneOSINT:
    def __init__(self, phone):
        self.phone = phone.replace(' ','').replace('-','').replace('+','')
        self.results = {}

    def detect_carrier(self):
        print(f"\n{G}[+] Method 1: Carrier Detection{RS}")
        # HLR Lookup services
        services = [
            f"https://www.phone-numbers.info/{self.phone}",
            f"https://www.who-called.us/{self.phone}",
            f"https://us.phone-numbers.info/{self.phone}",
        ]
        for s in services:
            print(f"  {Y}[i] {s[:60]}")

        # NumVerify API (free tier)
        try:
            r = requests.get(f"https://numverify.com/", timeout=10)
            print(f"  {Y}[i] Use numverify.com for carrier lookup")
            self.results['numverify'] = f"https://numverify.com/validate/{self.phone}"
        except: pass

    def social_media_lookup(self):
        print(f"\n{G}[+] Method 2: Social Media Lookup{RS}")
        # WhatsApp
        print(f"  {Y}[i] WhatsApp: https://wa.me/{self.phone}")
        self.results['whatsapp'] = f"https://wa.me/{self.phone}"

        # Telegram
        print(f"  {Y}[i] Telegram: https://t.me/+{self.phone}")
        self.results['telegram'] = f"https://t.me/+{self.phone}"

        # Signal (check via API)
        try:
            url = f"https://signal.org/api/profiles/{self.phone}"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                print(f"  {G}[✓] Signal account found!")
                self.results['signal'] = True
            else:
                print(f"  {Y}[!] Signal: {r.status_code}")
        except: pass

        # Truecaller
        print(f"  {Y}[i] Truecaller: https://www.truecaller.com/search/{self.phone}")
        self.results['truecaller'] = f"https://www.truecaller.com/search/{self.phone}"

    def search_engines(self):
        print(f"\n{G}[+] Method 3: Search Engine Dorks{RS}")
        dorks = [
            f"site:*.com \"{self.phone}\"",
            f"site:*.org \"{self.phone}\"",
            f"site:*.net \"{self.phone}\"",
            f"site:facebook.com \"{self.phone}\"",
            f"site:twitter.com \"{self.phone}\"",
            f"site:linkedin.com \"{self.phone}\"",
            f"site:instagram.com \"{self.phone}\"",
            f"site:whatsapp.com \"{self.phone}\"",
            f"\"{self.phone}\" filetype:pdf",
            f"\"{self.phone}\" filetype:doc",
            f"\"{self.phone}\" filetype:xls",
            f"\"{self.phone}\" intitle:\"contact\"",
        ]
        for d in dorks:
            print(f"  {Y}[d] {d}")
        self.results['dorks'] = dorks

    def reverse_phone_search(self):
        print(f"\n{G}[+] Method 4: Reverse Phone Services{RS}")
        services = [
            f"https://www.411.com/reverse-phone/{self.phone}",
            f"https://www.whitepages.com/phone/1-{self.phone}",
            f"https://www.spokeo.com/phone-number/{self.phone}",
            f"https://www.zabasearch.com/phone/{self.phone}",
            f"https://www.truthfinder.com/phone-lookup/?phone={self.phone}",
            f"https://www.beenverified.com/phone/{self.phone}",
        ]
        for s in services:
            print(f"  {Y}[i] {s[:60]}")
        self.results['reverse_services'] = services

    def check_whatsapp(self):
        print(f"\n{G}[+] Method 5: WhatsApp Verification{RS}")
        # Check if number is registered on WhatsApp
        url = f"https://web.whatsapp.com/send?phone={self.phone}"
        print(f"  {Y}[i] Check: {url[:60]}...")
        self.results['whatsapp_check'] = url

    def google_maps_locate(self):
        print(f"\n{G}[+] Method 6: Google Maps Business Search{RS}")
        url = f"https://www.google.com/maps/search/{self.phone}"
        print(f"  {Y}[i] {url}")
        self.results['maps'] = url

    def data_breach_check(self):
        print(f"\n{G}[+] Method 7: Data Breach Check{RS}")
        # Check if phone appears in known breaches
        print(f"  {Y}[i] Search HaveIBeenPwned for associated emails")
        print(f"  {Y}[i] Search IntelX for phone in breaches")
        print(f"  {Y}[i] Search Snusbase for phone in leaks")
        self.results['breach_links'] = [
            f"https://haveibeenpwned.com/DomainSearch",
            f"https://intelx.io/?s={self.phone}",
            f"https://snusbase.com/{self.phone}",
        ]

    def save_results(self):
        outfile = f"phone_osint_{self.phone}.json"
        with open(outfile, 'w') as f:
            json.dump({'phone': self.phone, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target Phone: {W}+{self.phone}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.detect_carrier()
        self.social_media_lookup()
        self.search_engines()
        self.reverse_phone_search()
        self.check_whatsapp()
        self.google_maps_locate()
        self.data_breach_check()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Phone OSINT Complete          ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='Phone number')
    args = parser.parse_args()
    osint = PhoneOSINT(args.target)
    osint.run_all()

if __name__ == "__main__":
    main()
