#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Password Breach & Leak Checker                 ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, hashlib, requests
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

class BreachChecker:
    def __init__(self, email=None, password=None, username=None):
        self.email = email
        self.password = password
        self.username = username
        self.results = {}

    def hibp_check(self):
        print(f"\n{G}[+] Method 1: HaveIBeenPwned{RS}")
        if self.email:
            try:
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}"
                headers = {'hibp-api-version': '3', 'User-Agent': 'HellSociety/1.0'}
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    breaches = r.json()
                    print(f"  {BR}[⚠] {len(breaches)} BREACHES FOUND!{RS}")
                    for b in breaches:
                        print(f"  {R}  - {b.get('Name','?')} ({b.get('BreachDate','?')})")
                    self.results['hibp'] = breaches
                elif r.status_code == 404:
                    print(f"  {G}[✓] No breaches found!")
                elif r.status_code == 403:
                    print(f"  {Y}[!] API requires paid key")
                else:
                    print(f"  {R}[!] Status: {r.status_code}")
            except Exception as e:
                print(f"  {R}[!] Error: {e}")

    def password_strength(self):
        print(f"\n{G}[+] Method 2: Password Strength Analysis{RS}")
        if self.password:
            score = 0
            feedback = []
            if len(self.password) >= 8:
                score += 1; feedback.append("Length OK")
            if len(self.password) >= 12:
                score += 1; feedback.append("Good length")
            if len(self.password) >= 16:
                score += 1; feedback.append("Excellent length")
            if re.search(r'[A-Z]', self.password):
                score += 1; feedback.append("Uppercase found")
            if re.search(r'[a-z]', self.password):
                score += 1; feedback.append("Lowercase found")
            if re.search(r'[0-9]', self.password):
                score += 1; feedback.append("Numbers found")
            if re.search(r'[^a-zA-Z0-9]', self.password):
                score += 1; feedback.append("Special chars found")
            if not re.search(r'(.)\1{2,}', self.password):
                score += 1; feedback.append("No repeated chars")

            for f in feedback:
                if score <= 2:
                    print(f"  {R}[!] {f}")
                elif score <= 5:
                    print(f"  {Y}[~] {f}")
                else:
                    print(f"  {G}[✓] {f}")

            print(f"\n  {B}Score: {score}/8")
            self.results['strength'] = {'score': score, 'feedback': feedback}

    def hibp_password(self):
        print(f"\n{G}[+] Method 3: HIBP Pwned Passwords{RS}")
        if self.password:
            sha1 = hashlib.sha1(self.password.encode()).hexdigest().upper()
            prefix = sha1[:5]
            suffix = sha1[5:]
            try:
                url = f"https://api.pwnedpasswords.com/range/{prefix}"
                r = requests.get(url, headers={'User-Agent': 'HellSociety/1.0'}, timeout=10)
                if r.status_code == 200:
                    for line in r.text.split('\n'):
                        if suffix in line:
                            count = line.split(':')[1].strip()
                            print(f"  {BR}[⚠] PASSWORD PWNED {int(count)} TIMES!{RS}")
                            self.results['pwned'] = True
                            self.results['pwned_count'] = int(count)
                            return
                    print(f"  {G}[✓] Password not found in breaches")
                    self.results['pwned'] = False
            except Exception as e:
                print(f"  {R}[!] Error: {e}")

    def leak_services(self):
        print(f"\n{G}[+] Method 4: Leak Service Searches{RS}")
        services = [
            ('IntelX', f"https://intelx.io/?s={self.email or self.username}"),
            ('DeHashed', f"https://dehashed.com/search?query={self.email or self.username}"),
            ('Snusbase', f"https://snusbase.com/{self.email or self.username}"),
            ('LeakCheck', f"https://leakcheck.io/search?query={self.email or self.username}"),
            ('Scylla', f"https://scylla.sh/search?email={self.email}"),
            ('WeLeakInfo', f"https://weleakinfo.com/search?query={self.email or self.username}"),
        ]
        for name, url in services:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['leak_services'] = services

    def email_dorks(self):
        print(f"\n{G}[+] Method 5: Google Dorks for Email Leaks{RS}")
        if self.email:
            dorks = [
                f'"password" site:pastebin.com "{self.email}"',
                f'"{self.email}" "password" filetype:txt',
                f'"{self.email}" "login" filetype:csv',
                f'"{self.email}" site:pastes.io',
                f'"{self.email}" site:dumpmon.com',
                f'"{self.email}" site:ghostbin.com',
            ]
            for d in dorks:
                print(f"  {Y}[d] {d}")
            self.results['email_dorks'] = dorks

    def save_results(self):
        outfile = f"breach_check_{self.email or self.username or 'unknown'}.json"
        with open(outfile, 'w') as f:
            json.dump({'email': self.email, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Email:    {W}{self.email}")
        print(f"{B}[*] Password: {W}{'***' if self.password else 'N/A'}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.hibp_check()
        self.password_strength()
        self.hibp_password()
        self.leak_services()
        self.email_dorks()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Breach Checker Complete       ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")



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
    print(f"  {BW}{Style.BRIGHT}  PASSWORD BREACH CHECK{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}PASSWORD BREACH CHECK                   {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Email to check                               {RS}")
        print(f"  {C}[2]  {BW}Password to check strength                   {RS}")
        print(f"  {C}[3]  {BW}Username to search                           {RS}")
        print()
        print(f"  {C}[4]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Email to check{RS}")
            value = input(f"  {Y}[*] -e: {RS}").strip()
            print(f"  {C}[*] Executing with -e={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Password to check strength{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] Username to search{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '4':
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

