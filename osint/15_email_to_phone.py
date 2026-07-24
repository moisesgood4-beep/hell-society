#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Email to Phone Mapper                           ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, requests
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

class EmailPhoneMapper:
    def __init__(self, email):
        self.email = email
        self.user = email.split('@')[0]
        self.domain = email.split('@')[1]
        self.results = {}

    def run_all(self):
        print(f"{B}[*] Email: {W}{self.email}")
        print(f"{B}[*] User:  {W}{self.user}")
        print(f"{B}[*] Domain:{W} {self.domain}")
        print(f"{Y}[~]{'─'*50}{RS}")

        # Method 1: Google search for phone
        print(f"\n{G}[+] Method 1: Google Dork Search{RS}")
        try:
            url = f"https://www.google.com/search?q=%22{self.email}%22+phone+OR+teléfono+OR+cell"
            r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
            phones = re.findall(r'\b[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]*\b', r.text)
            phones = [p.strip() for p in phones if len(p) >= 7][:10]
            if phones:
                print(f"  {G}[✓] Found phones: {phones[:5]}")
                self.results['google_dork'] = phones
            else:
                print(f"  {Y}[!] No phones found via Google")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

        # Method 2: Check public directories
        print(f"\n{G}[+] Method 2: Public Directory Search{RS}")
        dirs = [
            f"https://www.whitepages.com/search/phone/?q={self.user}",
            f"https://www.411.com/name/{self.user}",
        ]
        for d in dirs:
            print(f"  {Y}[i] Check: {d[:60]}...")

        # Method 3: Social media association
        print(f"\n{G}[+] Method 3: Social Media Association{RS}")
        platforms = ['twitter.com', 'facebook.com', 'instagram.com', 'linkedin.com']
        for p in platforms:
            print(f"  {Y}[i] Search {p}/{self.user}")

        # Method 4: HaveIBeenPwned phone check
        print(f"\n{G}[+] Method 4: Breach Phone Association{RS}")
        try:
            r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}",
                           headers={'hibp-api-version':'3'}, timeout=10)
            if r.status_code == 200:
                breaches = r.json()
                print(f"  {G}[✓] {len(breaches)} breaches found - may contain phone numbers")
                for b in breaches[:5]:
                    print(f"  {C}  - {b.get('Name','?')}")
            elif r.status_code == 404:
                print(f"  {Y}[!] No breaches found")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

        # Method 5: Hunter.io domain search
        print(f"\n{G}[+] Method 5: Domain Email Patterns{RS}")
        try:
            print(f"  {Y}[i] Search emails pattern for {self.domain}")
            print(f"  {Y}[i] Use: https://hunter.io/email-finder/{self.domain}/email/{self.user}")
        except: pass

        # Method 6: Phonebook.cz
        print(f"\n{G}[+] Method 6: Phonebook.cz Search{RS}")
        try:
            r = requests.get(f"https://phonebook.cz/api/?email={self.email}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                if 'results' in data and data['results']:
                    print(f"  {G}[✓] {len(data['results'])} results found")
                    self.results['phonebook'] = data['results'][:20]
                else:
                    print(f"  {Y}[!] No results in phonebook")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

        # Save results
        outfile = f"email_phone_{self.user}.json"
        with open(outfile, 'w') as f:
            json.dump({'email': self.email, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

        # Summary
        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Email to Phone Mapper Complete  ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='Email target')
    args = parser.parse_args()
    mapper = EmailPhoneMapper(args.target)
    mapper.run_all()

if __name__ == "__main__":
    main()
